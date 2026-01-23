#!/usr/bin/env python3
"""
图片修复脚本 - 只修复缺失的图片，不改动文字内容
"""

import os
import re
import json
import yaml
import hashlib
import requests
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class ImageFixer:
    def __init__(self):
        self.content_dir = Path("content/posts")
        self.images_dir = Path("public/images/posts")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.fixed = 0
        self.failed = 0
    
    def load_problem_files(self):
        """从健康报告加载有图片问题的文件"""
        report_path = Path("data/article_health_report.json")
        if not report_path.exists():
            print("请先运行 article_health_check.py")
            return []
        
        report = json.load(open(report_path, encoding='utf-8'))
        files = set()
        for issue in report['issues']:
            if issue['type'] == 'missing_image':
                files.add(issue['file'])
        return list(files)
    
    def get_source_url(self, md_file: Path) -> str:
        """从文章提取原文链接"""
        content = md_file.read_text(encoding='utf-8')
        match = re.search(r'source_url:\s*(.+)', content)
        if match:
            return match.group(1).strip()
        return None
    
    def get_missing_images(self, md_file: Path) -> list:
        """获取文章中缺失的图片"""
        content = md_file.read_text(encoding='utf-8')
        missing = []
        
        for match in re.finditer(r'!\[[^\]]*\]\((/images/posts/([^)]+))\)', content):
            full_path, filename = match.groups()
            img_path = self.images_dir / filename
            if not img_path.exists():
                missing.append({'path': full_path, 'filename': filename})
        
        return missing
    
    def fetch_original_images(self, source_url: str) -> dict:
        """从原文获取图片URL映射"""
        try:
            resp = self.session.get(source_url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            images = {}
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    full_url = urljoin(source_url, src)
                    # 生成相同的hash作为key
                    img_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]
                    ext = Path(urlparse(full_url).path).suffix or '.jpg'
                    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                        ext = '.jpg'
                    filename = f"{img_hash}{ext}"
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
            
            # 检查是否是图片
            content_type = resp.headers.get('content-type', '')
            if 'image' not in content_type and len(resp.content) < 1000:
                return False
            
            save_path.write_bytes(resp.content)
            return True
        except:
            return False
    
    def fix_article(self, filename: str) -> dict:
        """修复单篇文章的图片"""
        md_file = self.content_dir / filename
        if not md_file.exists():
            return {'status': 'not_found'}
        
        # 获取缺失的图片
        missing = self.get_missing_images(md_file)
        if not missing:
            return {'status': 'no_missing', 'fixed': 0}
        
        # 获取原文链接
        source_url = self.get_source_url(md_file)
        if not source_url:
            return {'status': 'no_source_url', 'missing': len(missing)}
        
        print(f"  原文: {source_url}")
        print(f"  缺失图片: {len(missing)} 张")
        
        # 从原文获取图片
        original_images = self.fetch_original_images(source_url)
        if not original_images:
            return {'status': 'fetch_failed', 'missing': len(missing)}
        
        # 下载缺失的图片
        fixed_count = 0
        for img in missing:
            filename = img['filename']
            if filename in original_images:
                url = original_images[filename]
                save_path = self.images_dir / filename
                
                if self.download_image(url, save_path):
                    print(f"    ✓ {filename}")
                    fixed_count += 1
                else:
                    print(f"    ✗ {filename} 下载失败")
            else:
                print(f"    ? {filename} 未在原文找到")
        
        return {'status': 'ok', 'fixed': fixed_count, 'missing': len(missing)}
    
    def fix_all(self):
        """修复所有有问题的文章"""
        files = self.load_problem_files()
        print(f"找到 {len(files)} 篇需要修复图片的文章\n")
        
        for i, filename in enumerate(files):
            print(f"[{i+1}/{len(files)}] {filename}")
            result = self.fix_article(filename)
            
            if result.get('fixed', 0) > 0:
                self.fixed += result['fixed']
            if result.get('status') == 'fetch_failed':
                self.failed += result.get('missing', 0)
            
            time.sleep(1)  # 避免请求过快
            print()
        
        print("=" * 50)
        print(f"修复完成！")
        print(f"  成功下载: {self.fixed} 张图片")
        print(f"  失败: {self.failed} 张")


if __name__ == "__main__":
    fixer = ImageFixer()
    fixer.fix_all()
