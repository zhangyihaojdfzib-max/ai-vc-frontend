#!/usr/bin/env python3
"""
文章健康检查脚本
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


IMG_MD_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')


def detect_image_kind(data: bytes) -> str:
    # JPEG
    if data.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    # PNG
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    # GIF
    if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        return 'gif'
    # WebP
    if len(data) >= 12 and data[0:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp'
    # AVIF
    if len(data) >= 12 and data[4:8] == b'ftyp' and (b'avif' in data[8:24] or b'avis' in data[8:24]):
        return 'avif'

    s = data.lstrip()
    if s.startswith(b'<!DOCTYPE html') or s.startswith(b'<html') or s.startswith(b'<head'):
        return 'html'
    if s.startswith(b'{') or s.startswith(b'['):
        return 'json'
    return 'unknown'


def kind_from_ext(ext: str) -> Optional[str]:
    e = (ext or '').lower()
    if e in ('.jpg', '.jpeg'):
        return 'jpeg'
    if e == '.png':
        return 'png'
    if e == '.gif':
        return 'gif'
    if e == '.webp':
        return 'webp'
    if e == '.avif':
        return 'avif'
    if e == '.svg':
        return 'svg'
    return None


def is_valid_image_bytes(kind: str, data: bytes) -> bool:
    if not data or len(data) < 64:
        return False
    if kind == 'jpeg':
        return data.startswith(b'\xff\xd8') and data.rstrip().endswith(b'\xff\xd9')
    if kind == 'png':
        return data.startswith(b'\x89PNG\r\n\x1a\n') and b'IEND' in data[-64:]
    if kind == 'gif':
        return (data.startswith(b'GIF87a') or data.startswith(b'GIF89a')) and data.rstrip().endswith(b'\x3b')
    if kind == 'webp':
        if len(data) < 12 or data[0:4] != b'RIFF' or data[8:12] != b'WEBP':
            return False
        try:
            riff_size = int.from_bytes(data[4:8], 'little')
            return (riff_size + 8) <= (len(data) + 16)
        except Exception:
            return True
    if kind == 'avif':
        return len(data) >= 12 and data[4:8] == b'ftyp'
    # svg 在本站通常被跳过；这里不做严格校验
    if kind == 'svg':
        return True
    return False


class ArticleHealthChecker:
    def __init__(self, content_dir: str = "content/posts", images_dir: str = "public/images/posts"):
        self.content_dir = Path(content_dir)
        self.images_dir = Path(images_dir)
        self.issues = []
        self.stats = defaultdict(int)
        self.source_issues = defaultdict(list)
        
    def check_all(self, source_filter: str = None) -> Dict:
        print("=" * 70)
        print("文章健康检查")
        print("=" * 70)
        
        if not self.content_dir.exists():
            print(f"文章目录不存在: {self.content_dir}")
            return {}
        
        md_files = list(self.content_dir.glob("*.md"))
        print(f"\n找到 {len(md_files)} 篇文章")
        
        for i, md_file in enumerate(md_files):
            if (i + 1) % 100 == 0:
                print(f"  检查进度: {i + 1}/{len(md_files)}")
            self._check_article(md_file, source_filter)
        
        return self._generate_report()
    
    def _check_article(self, md_file: Path, source_filter: str = None):
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append({'file': md_file.name, 'type': 'read_error', 'severity': 'critical', 'message': str(e)})
            self.stats['read_error'] += 1
            return
        
        frontmatter, body = self._parse_frontmatter(content)
        if frontmatter is None:
            self.issues.append({'file': md_file.name, 'type': 'frontmatter_error', 'severity': 'critical', 'message': 'frontmatter解析失败'})
            self.stats['frontmatter_error'] += 1
            return
        
        source = frontmatter.get('source', 'unknown')
        if source_filter and source_filter.lower() not in source.lower():
            return
        
        self.stats['total'] += 1
        
        # 检查内容长度
        if len(body.strip()) < 100:
            self.issues.append({'file': md_file.name, 'source': source, 'type': 'empty_content', 'severity': 'critical', 'message': f'内容过短({len(body.strip())}字符)'})
            self.stats['empty_content'] += 1
        
        # 检查图片
        self._check_images(body, md_file.name, source)
        
        # 检查格式
        self._check_format(body, md_file.name, source)
    
    def _parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
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
    
    def _check_images(self, body: str, filename: str, source: str):
        # 检查图片占位符
        if re.search(r'!\[.*?未转化.*?\]|!\[\s*\]\(\s*\)', body, re.IGNORECASE):
            self.issues.append({'file': filename, 'source': source, 'type': 'image_placeholder', 'severity': 'warning', 'message': '图片占位符未处理'})
            self.stats['image_placeholder'] += 1
        
        # 检查图片：缺失/过小/非图片/格式不匹配/疑似截断
        for match in IMG_MD_RE.finditer(body):
            src = match.group(1).strip()
            if not src.startswith('/images/'):
                continue

            img_path = Path("public") / src.lstrip('/')
            if not img_path.exists():
                self.issues.append({'file': filename, 'source': source, 'type': 'missing_image', 'severity': 'warning', 'message': f'图片不存在: {src}'})
                self.stats['missing_image'] += 1
                continue

            try:
                data = img_path.read_bytes()
            except Exception as e:
                self.issues.append({'file': filename, 'source': source, 'type': 'image_read_error', 'severity': 'warning', 'message': f'图片读取失败: {src} ({e})'})
                self.stats['image_read_error'] += 1
                continue

            if len(data) < 1024:
                self.issues.append({'file': filename, 'source': source, 'type': 'image_too_small', 'severity': 'warning', 'message': f'图片过小({len(data)} bytes): {src}'})
                self.stats['image_too_small'] += 1

            # 用头尾拼接做类型探测（既能识别 magic bytes，也能识别截断特征）
            probe = data[:64] + data[-64:]
            kind = detect_image_kind(probe)
            ext_kind = kind_from_ext(img_path.suffix)

            if kind in ('html', 'json'):
                self.issues.append({'file': filename, 'source': source, 'type': 'image_not_image', 'severity': 'warning', 'message': f'图片文件疑似为 {kind}: {src}'})
                self.stats['image_not_image'] += 1
                continue

            if kind == 'unknown':
                self.issues.append({'file': filename, 'source': source, 'type': 'image_unknown_type', 'severity': 'warning', 'message': f'图片类型未知: {src}'})
                self.stats['image_unknown_type'] += 1
                continue

            if ext_kind and ext_kind != kind and not (ext_kind == 'jpeg' and kind == 'jpeg'):
                self.issues.append({'file': filename, 'source': source, 'type': 'image_type_mismatch', 'severity': 'warning', 'message': f'图片格式与扩展名不匹配({img_path.suffix} vs {kind}): {src}'})
                self.stats['image_type_mismatch'] += 1

            if not is_valid_image_bytes(kind, data):
                self.issues.append({'file': filename, 'source': source, 'type': 'image_possibly_truncated', 'severity': 'warning', 'message': f'图片疑似损坏/截断: {src}'})
                self.stats['image_possibly_truncated'] += 1
    
    def _check_format(self, body: str, filename: str, source: str):
        # 空列表项
        empty_items = len(re.findall(r'(?:^|\n)\s*-\s*(?:\n|$)', body))
        if empty_items > 5:
            self.issues.append({'file': filename, 'source': source, 'type': 'empty_list_items', 'severity': 'warning', 'message': f'{empty_items}个空列表项'})
            self.stats['empty_list_items'] += 1
        
        # 过多加粗
        bold_count = body.count('**')
        if bold_count > 30:
            self.issues.append({'file': filename, 'source': source, 'type': 'excessive_bold', 'severity': 'warning', 'message': f'{bold_count}个加粗标记'})
            self.stats['excessive_bold'] += 1
    
    def _generate_report(self) -> Dict:
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_articles': self.stats.get('total', 0),
                'total_issues': len(self.issues),
                'critical': len([i for i in self.issues if i.get('severity') == 'critical']),
                'warning': len([i for i in self.issues if i.get('severity') == 'warning']),
            },
            'by_type': dict(defaultdict(int, {i['type']: sum(1 for x in self.issues if x['type']==i['type']) for i in self.issues})),
            'issues': self.issues
        }
        
        # 按源统计
        source_counts = defaultdict(lambda: {'count': 0, 'types': defaultdict(int)})
        for issue in self.issues:
            src = issue.get('source', 'unknown')
            source_counts[src]['count'] += 1
            source_counts[src]['types'][issue['type']] += 1
        report['by_source'] = dict(sorted(source_counts.items(), key=lambda x: -x[1]['count']))
        
        return report
    
    def print_report(self, report: Dict):
        print("\n" + "=" * 70)
        print("健康检查报告")
        print("=" * 70)
        
        s = report['summary']
        print(f"\n总文章数: {s['total_articles']}")
        print(f"问题总数: {s['total_issues']}")
        print(f"  - 严重: {s['critical']}")
        print(f"  - 警告: {s['warning']}")
        
        print("\n按问题类型:")
        for t, c in sorted(report['by_type'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        
        print("\n问题最多的来源 (Top 10):")
        for i, (src, data) in enumerate(list(report['by_source'].items())[:10]):
            print(f"  {i+1}. {src}: {data['count']}个问题")
        
        # 严重问题
        critical = [i for i in report['issues'] if i.get('severity') == 'critical']
        if critical:
            print(f"\n严重问题 (前10个):")
            for issue in critical[:10]:
                print(f"  {issue['file']}: {issue['message']}")
    
    def save_report(self, report: Dict, path: str = "data/article_health_report.json"):
        Path(path).parent.mkdir(exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {path}")


def main():
    checker = ArticleHealthChecker()
    report = checker.check_all()
    checker.print_report(report)
    checker.save_report(report)


if __name__ == "__main__":
    main()

