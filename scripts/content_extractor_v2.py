#!/usr/bin/env python3
"""
content_extractor_v2.py - 带图片位置保留的内容提取器
"""

import os
import re
import hashlib
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class ContentExtractorV2:
    """带图片的内容提取器"""
    
    def __init__(self, images_dir: Path, user_agent: str = None):
        self.images_dir = images_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent or 'Mozilla/5.0 (compatible; AI-VC-Bot/2.0)'
        
    def extract(self, html: str, base_url: str) -> Dict:
        """从 HTML 提取内容，保留图片位置"""
        soup = BeautifulSoup(html, 'html.parser')
        title = self._extract_title(soup)
        article = self._find_article_container(soup)
        
        if not article:
            return {'blocks': [], 'title': title, 'images': []}
        
        blocks = []
        images = []
        seen_texts = set()
        
        for element in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'figure', 'pre', 'ul', 'ol']):
            if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = element.get_text(strip=True)
                if text and len(text) > 20 and text not in seen_texts:
                    seen_texts.add(text)
                    prefix = '#' * int(element.name[1]) + ' ' if element.name.startswith('h') else ''
                    blocks.append({'type': 'text', 'content': prefix + text})
                    
            elif element.name == 'img':
                img_data = self._process_image(element, base_url)
                if img_data:
                    blocks.append(img_data)
                    if img_data.get('local_path'):
                        images.append(img_data['local_path'])
                        
            elif element.name == 'figure':
                img = element.find('img')
                if img:
                    img_data = self._process_image(img, base_url)
                    if img_data:
                        caption = element.find('figcaption')
                        if caption:
                            img_data['alt'] = caption.get_text(strip=True)
                        blocks.append(img_data)
                        if img_data.get('local_path'):
                            images.append(img_data['local_path'])
                        
            elif element.name == 'pre':
                code = element.get_text()
                if code and len(code) > 10:
                    blocks.append({'type': 'code', 'content': code})
                    
            elif element.name in ['ul', 'ol']:
                items = [li.get_text(strip=True) for li in element.find_all('li', recursive=False)]
                if items:
                    blocks.append({'type': 'list', 'items': items, 'ordered': element.name == 'ol'})
        
        return {'blocks': blocks, 'title': title, 'images': images}
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        return ''
    
    def _find_article_container(self, soup: BeautifulSoup):
        selectors = ['article', '[role="main"]', '.post-content', '.article-content', 
                     '.entry-content', '.content', '.post-body', 'main']
        for selector in selectors:
            container = soup.select_one(selector)
            if container:
                return container
        return soup.find('body')
    
    def _process_image(self, img_tag, base_url: str) -> Optional[Dict]:
        src = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy-src')
        if not src:
            return None
        
        if src.startswith('data:') or '.svg' in src.lower() or 'icon' in src.lower() or 'logo' in src.lower():
            return None
        
        img_url = urljoin(base_url, src)
        local_path = self._download_image(img_url)
        
        return {
            'type': 'image',
            'src': img_url,
            'alt': img_tag.get('alt', ''),
            'local_path': local_path
        }
    
    def _download_image(self, url: str) -> Optional[str]:
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            ext = '.jpg'
            if '.png' in url.lower(): ext = '.png'
            elif '.gif' in url.lower(): ext = '.gif'
            elif '.webp' in url.lower(): ext = '.webp'
            
            filename = f"{url_hash}{ext}"
            local_path = self.images_dir / filename
            
            if local_path.exists():
                return str(local_path)
            
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type and len(response.content) < 1000:
                return None
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"    ✓ 下载图片: {filename}")
            return str(local_path)
            
        except Exception as e:
            print(f"    ✗ 图片下载失败: {e}")
            return None
    
    def blocks_to_markdown(self, blocks: List[Dict], image_base_path: str = '/images/posts') -> str:
        lines = []
        for block in blocks:
            if block['type'] == 'text':
                lines.append(block['content'])
                lines.append('')
            elif block['type'] == 'image':
                alt = block.get('alt', '')
                if block.get('local_path'):
                    filename = Path(block['local_path']).name
                    src = f"{image_base_path}/{filename}"
                else:
                    src = block['src']
                lines.append(f'![{alt}]({src})')
                lines.append('')
            elif block['type'] == 'code':
                lines.append('```')
                lines.append(block['content'])
                lines.append('```')
                lines.append('')
            elif block['type'] == 'list':
                for i, item in enumerate(block['items']):
                    prefix = f"{i+1}. " if block.get('ordered') else "- "
                    lines.append(prefix + item)
                lines.append('')
        return '\n'.join(lines)
