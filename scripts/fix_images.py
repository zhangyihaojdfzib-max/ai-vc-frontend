#!/usr/bin/env python3
"""
fix_images.py - 图片修复脚本 (v2.0)

功能:
- 扫描所有文章，找出缺失的图片
- 从原文重新下载缺失的图片
- 支持并行下载提高效率
- 可选择只处理特定来源的文章
"""

import os
import re
import json
import yaml
import hashlib
import requests
import time
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Set, Optional, Tuple


class ImageFixer:
    """图片修复器"""

    def __init__(self, content_dir: str = "content/posts", images_dir: str = "public/images/posts"):
        self.content_dir = Path(content_dir)
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        self.stats = {
            'files_scanned': 0,
            'files_with_missing': 0,
            'images_missing': 0,
            'images_fixed': 0,
            'images_failed': 0,
        }

    def scan_all_articles(self, source_filter: str = None) -> List[Dict]:
        """扫描所有文章，找出缺失图片的文章"""
        print("扫描文章中的图片...")

        articles_with_missing = []
        md_files = sorted(self.content_dir.glob("*.md"))

        for md_file in md_files:
            self.stats['files_scanned'] += 1

            try:
                content = md_file.read_text(encoding='utf-8')
            except:
                continue

            # 如果指定了来源过滤
            if source_filter and source_filter.lower() not in content.lower():
                continue

            # 获取 source_url
            source_url_match = re.search(r'source_url:\s*(.+)', content)
            source_url = source_url_match.group(1).strip() if source_url_match else None

            # 查找所有图片引用
            missing_images = []
            for match in re.finditer(r'!\[[^\]]*\]\((/images/posts/([^)]+))\)', content):
                full_path, filename = match.groups()
                img_path = self.images_dir / filename
                if not img_path.exists():
                    missing_images.append({
                        'path': full_path,
                        'filename': filename,
                    })

            if missing_images:
                self.stats['files_with_missing'] += 1
                self.stats['images_missing'] += len(missing_images)
                articles_with_missing.append({
                    'file': md_file.name,
                    'source_url': source_url,
                    'missing': missing_images,
                })

        print(f"扫描完成: {self.stats['files_scanned']} 篇文章, "
              f"{self.stats['files_with_missing']} 篇有缺失图片, "
              f"共 {self.stats['images_missing']} 张缺失")

        return articles_with_missing

    def fetch_original_images(self, source_url: str) -> Dict[str, str]:
        """从原文获取所有图片URL，返回 {filename: url} 映射"""
        if not source_url:
            return {}

        try:
            resp = self.session.get(source_url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            images = {}
            for img in soup.find_all('img'):
                # 尝试多种属性获取图片URL
                src = (img.get('src') or img.get('data-src') or
                       img.get('data-lazy-src') or img.get('data-original'))

                if not src or src.startswith('data:'):
                    continue

                full_url = urljoin(source_url, src)

                # 生成与 content_extractor_v2 相同的文件名
                url_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]

                # 确定扩展名
                parsed = urlparse(full_url)
                path_lower = parsed.path.lower()
                if '.png' in path_lower:
                    ext = '.png'
                elif '.gif' in path_lower:
                    ext = '.gif'
                elif '.webp' in path_lower:
                    ext = '.webp'
                elif '.jpeg' in path_lower or '.jpg' in path_lower:
                    ext = '.jpg'
                else:
                    ext = '.jpg'

                filename = f"{url_hash}{ext}"
                images[filename] = full_url

            return images

        except Exception as e:
            print(f"    获取原文失败: {e}")
            return {}

    def download_image(self, url: str, save_path: Path) -> bool:
        """下载单张图片"""
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()

            content_type = resp.headers.get('content-type', '')

            # 检查是否是有效图片
            if len(resp.content) < 500:
                return False

            if 'image' not in content_type and len(resp.content) < 5000:
                return False

            save_path.write_bytes(resp.content)
            return True

        except Exception as e:
            return False

    def fix_article(self, article: Dict) -> Dict:
        """修复单篇文章的缺失图片"""
        filename = article['file']
        source_url = article['source_url']
        missing = article['missing']

        result = {
            'file': filename,
            'missing_count': len(missing),
            'fixed': 0,
            'failed': 0,
            'not_found': 0,
        }

        if not source_url:
            result['failed'] = len(missing)
            result['error'] = 'no_source_url'
            return result

        # 从原文获取图片映射
        original_images = self.fetch_original_images(source_url)

        if not original_images:
            result['failed'] = len(missing)
            result['error'] = 'fetch_failed'
            return result

        # 下载缺失的图片
        for img in missing:
            img_filename = img['filename']

            if img_filename in original_images:
                url = original_images[img_filename]
                save_path = self.images_dir / img_filename

                if self.download_image(url, save_path):
                    result['fixed'] += 1
                    print(f"    ✓ {img_filename}")
                else:
                    result['failed'] += 1
                    print(f"    ✗ {img_filename} (下载失败)")
            else:
                result['not_found'] += 1
                print(f"    ? {img_filename} (原文未找到)")

        return result

    def fix_all(self, source_filter: str = None, max_articles: int = None):
        """修复所有缺失图片"""
        print("=" * 70)
        print("图片修复工具 v2.0")
        print("=" * 70)

        # 扫描找出缺失图片的文章
        articles = self.scan_all_articles(source_filter)

        if not articles:
            print("\n没有找到缺失图片的文章!")
            return

        if max_articles:
            articles = articles[:max_articles]

        print(f"\n开始修复 {len(articles)} 篇文章的图片...\n")

        for i, article in enumerate(articles):
            print(f"[{i+1}/{len(articles)}] {article['file']}")
            if article['source_url']:
                print(f"  原文: {article['source_url'][:60]}...")
            print(f"  缺失: {len(article['missing'])} 张")

            result = self.fix_article(article)

            self.stats['images_fixed'] += result['fixed']
            self.stats['images_failed'] += result['failed'] + result['not_found']

            print()
            time.sleep(0.5)  # 避免请求过快

        self.print_stats()

    def print_stats(self):
        """打印统计信息"""
        print("=" * 70)
        print("修复完成!")
        print("=" * 70)
        print(f"扫描文章数: {self.stats['files_scanned']}")
        print(f"有缺失图片的文章: {self.stats['files_with_missing']}")
        print(f"总缺失图片数: {self.stats['images_missing']}")
        print(f"成功修复: {self.stats['images_fixed']}")
        print(f"修复失败: {self.stats['images_failed']}")

        if self.stats['images_missing'] > 0:
            success_rate = self.stats['images_fixed'] / self.stats['images_missing'] * 100
            print(f"成功率: {success_rate:.1f}%")


def main():
    parser = argparse.ArgumentParser(description='修复文章中缺失的图片')
    parser.add_argument('--source', '-s', help='只处理指定来源的文章 (如 huggingface, databricks)')
    parser.add_argument('--max', '-m', type=int, help='最多处理的文章数')
    args = parser.parse_args()

    fixer = ImageFixer()
    fixer.fix_all(source_filter=args.source, max_articles=args.max)


if __name__ == "__main__":
    main()
