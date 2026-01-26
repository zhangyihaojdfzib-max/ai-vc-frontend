#!/usr/bin/env python3
"""
clean_articles.py - 清理已有文章中的问题内容

功能:
- 删除头像图片 (alt 中包含 "头像"、"avatar" 等)
- 删除重复的内容块
- 删除空列表项
- 删除非正文内容 (评论、相关文章等)
- 清理重复的目录结构
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Set


class ArticleCleaner:
    """文章清理器"""

    # 需要删除的图片模式 (alt 文本中包含这些关键词)
    REMOVE_IMAGE_ALT_PATTERNS = [
        '头像', 'avatar', 'profile', 'author', 'user',
        'contributor', 'writer', 'member',
    ]

    # 需要删除的行模式
    REMOVE_LINE_PATTERNS = [
        # 空列表项
        r'^\s*[-*]\s*$',
        r'^\s*\d+\.\s*$',
        # 单独的符号
        r'^\s*[+]\d+\s*$',  # +292
        r'^\s*[-·•]+\s*$',
        # 导航/UI 文本
        r'^目录\s*$',
        r'^Table of Contents\s*$',
        r'^更多.*文章\s*$',
        r'^Related\s*(Posts|Articles)?\s*$',
        r'^\d+\s*(条回复|replies?|comments?)\s*$',
        r'^注册或登录',
        r'^Sign (up|in)',
        r'^Share\s*$',
        r'^分享\s*$',
    ]

    # 需要删除的内容块开始标记 (从这里到文章结尾或下一个主要标题)
    REMOVE_SECTION_MARKERS = [
        '更多博客文章',
        'More blog posts',
        'Related Posts',
        'Related Articles',
        '相关文章',
        '评论',
        'Comments',
    ]

    def __init__(self, content_dir: str = "content/posts", images_dir: str = "public/images/posts"):
        self.content_dir = Path(content_dir)
        self.images_dir = Path(images_dir)
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'images_removed': 0,
            'lines_removed': 0,
            'duplicates_removed': 0,
        }

    def clean_all(self, source_filter: str = None, dry_run: bool = False) -> Dict:
        """清理所有文章"""
        print("=" * 70)
        print("文章清理工具")
        print(f"模式: {'预览 (不修改文件)' if dry_run else '实际执行'}")
        print("=" * 70)

        if not self.content_dir.exists():
            print(f"文章目录不存在: {self.content_dir}")
            return self.stats

        md_files = sorted(self.content_dir.glob("*.md"))
        print(f"\n找到 {len(md_files)} 篇文章")

        for i, md_file in enumerate(md_files):
            if (i + 1) % 50 == 0:
                print(f"  进度: {i + 1}/{len(md_files)}")

            # 如果指定了来源过滤
            if source_filter:
                content = md_file.read_text(encoding='utf-8')
                if source_filter.lower() not in content.lower():
                    continue

            self._clean_article(md_file, dry_run)

        return self.stats

    def _clean_article(self, md_file: Path, dry_run: bool = False):
        """清理单篇文章"""
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  读取失败: {md_file.name} - {e}")
            return

        self.stats['files_processed'] += 1
        original_content = content

        # 分离 frontmatter 和正文
        frontmatter, body = self._parse_frontmatter(content)
        if frontmatter is None:
            return

        # 清理正文
        cleaned_body, changes = self._clean_body(body)

        if changes['total'] > 0:
            self.stats['files_modified'] += 1
            self.stats['images_removed'] += changes['images_removed']
            self.stats['lines_removed'] += changes['lines_removed']
            self.stats['duplicates_removed'] += changes['duplicates_removed']

            if not dry_run:
                # 重新组装文章
                new_content = self._rebuild_content(content, cleaned_body)
                md_file.write_text(new_content, encoding='utf-8')
                print(f"  ✓ {md_file.name}: 删除 {changes['images_removed']} 图片, "
                      f"{changes['lines_removed']} 行, {changes['duplicates_removed']} 重复")
            else:
                print(f"  [预览] {md_file.name}: 将删除 {changes['images_removed']} 图片, "
                      f"{changes['lines_removed']} 行, {changes['duplicates_removed']} 重复")

    def _parse_frontmatter(self, content: str) -> Tuple:
        """解析 frontmatter"""
        if not content.startswith('---'):
            return None, content
        try:
            end_idx = content.find('---', 3)
            if end_idx == -1:
                return None, content
            yaml_str = content[3:end_idx].strip()
            frontmatter = yaml.safe_load(yaml_str)
            body = content[end_idx + 3:].strip()
            return frontmatter, body
        except:
            return None, content

    def _rebuild_content(self, original_content: str, new_body: str) -> str:
        """重新组装文章内容"""
        # 找到 frontmatter 结束位置
        end_idx = original_content.find('---', 3)
        if end_idx == -1:
            return new_body
        frontmatter_part = original_content[:end_idx + 3]
        return frontmatter_part + '\n\n' + new_body.strip() + '\n'

    def _clean_body(self, body: str) -> Tuple[str, Dict]:
        """清理文章正文"""
        changes = {
            'images_removed': 0,
            'lines_removed': 0,
            'duplicates_removed': 0,
            'total': 0,
        }

        lines = body.split('\n')
        cleaned_lines = []
        seen_lines: Set[str] = set()
        seen_images: Set[str] = set()
        in_remove_section = False
        consecutive_empty = 0

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 检查是否进入需要删除的区块
            for marker in self.REMOVE_SECTION_MARKERS:
                if marker in stripped and (stripped.startswith('#') or stripped == marker):
                    in_remove_section = True
                    break

            # 如果在删除区块内，跳过直到遇到主要标题 (## 或更高级)
            if in_remove_section:
                if stripped.startswith('## ') or stripped.startswith('# '):
                    # 检查是否是文章结尾标记
                    if '本文由AI自动翻译' in stripped or '原文链接' in stripped:
                        in_remove_section = False
                        cleaned_lines.append(line)
                    else:
                        in_remove_section = False
                        cleaned_lines.append(line)
                else:
                    changes['lines_removed'] += 1
                i += 1
                continue

            # 检查是否是需要删除的图片
            img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', stripped)
            if img_match:
                alt_text = img_match.group(1)
                img_src = img_match.group(2)

                # 检查 alt 文本是否包含需要删除的关键词
                should_remove = False
                alt_lower = alt_text.lower()
                for pattern in self.REMOVE_IMAGE_ALT_PATTERNS:
                    if pattern.lower() in alt_lower:
                        should_remove = True
                        break

                # 检查是否是重复图片
                if img_src in seen_images:
                    should_remove = True

                if should_remove:
                    changes['images_removed'] += 1
                    i += 1
                    continue

                seen_images.add(img_src)

            # 检查是否匹配需要删除的行模式
            should_remove_line = False
            for pattern in self.REMOVE_LINE_PATTERNS:
                if re.match(pattern, stripped, re.IGNORECASE):
                    should_remove_line = True
                    break

            if should_remove_line:
                changes['lines_removed'] += 1
                i += 1
                continue

            # 检查是否是重复内容 (对于非空行)
            if stripped and len(stripped) > 20:
                if stripped in seen_lines:
                    changes['duplicates_removed'] += 1
                    i += 1
                    continue
                seen_lines.add(stripped)

            # 控制连续空行数量
            if not stripped:
                consecutive_empty += 1
                if consecutive_empty > 2:
                    i += 1
                    continue
            else:
                consecutive_empty = 0

            cleaned_lines.append(line)
            i += 1

        changes['total'] = changes['images_removed'] + changes['lines_removed'] + changes['duplicates_removed']

        return '\n'.join(cleaned_lines), changes

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 70)
        print("清理完成!")
        print("=" * 70)
        print(f"处理文件数: {self.stats['files_processed']}")
        print(f"修改文件数: {self.stats['files_modified']}")
        print(f"删除图片数: {self.stats['images_removed']}")
        print(f"删除行数: {self.stats['lines_removed']}")
        print(f"删除重复数: {self.stats['duplicates_removed']}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='清理文章中的问题内容')
    parser.add_argument('--source', '-s', help='只处理指定来源的文章 (如 huggingface)')
    parser.add_argument('--dry-run', '-d', action='store_true', help='预览模式，不实际修改文件')
    args = parser.parse_args()

    cleaner = ArticleCleaner()
    cleaner.clean_all(source_filter=args.source, dry_run=args.dry_run)
    cleaner.print_stats()


if __name__ == "__main__":
    main()
