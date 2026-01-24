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
from typing import List, Dict, Optional, Tuple

class ContentExtractorV2:
    """带图片的内容提取器"""
    
    def __init__(self, images_dir: Path, user_agent: str = None):
        self.images_dir = images_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent or 'Mozilla/5.0 (compatible; AI-VC-Bot/2.0)'
        # 支持的图片类型（用于缓存命中 & 本地探测）
        self._allowed_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']
        
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
        src = self._select_best_image_src(img_tag)
        if not src:
            return None
        
        src_l = src.lower()
        if src_l.startswith('data:') or '.svg' in src_l or 'icon' in src_l:
            return None
        
        img_url = urljoin(base_url, src)
        local_path = self._download_image(img_url)
        
        return {
            'type': 'image',
            'src': img_url,
            'alt': img_tag.get('alt', ''),
            'local_path': local_path
        }
    
    def _select_best_image_src(self, img_tag) -> Optional[str]:
        """
        选择最合适的图片 src：
        - 优先使用 srcset/data-srcset 的“最大”项（很多站点 src 是占位符）
        - 再回退到 src / data-src / data-lazy-src / data-original 等
        """
        candidates: List[Tuple[str, float]] = []

        def add_srcset(value: Optional[str]):
            if not value:
                return
            best = self._pick_best_from_srcset(value)
            if best:
                candidates.append((best, 1000.0))

        add_srcset(img_tag.get('srcset') or img_tag.get('data-srcset'))

        # 常见 lazy-load 字段
        for key in ['src', 'data-src', 'data-lazy-src', 'data-original', 'data-url']:
            v = img_tag.get(key)
            if v:
                candidates.append((v, 1.0))

        if not candidates:
            return None

        # srcset 赋予更高权重
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def _pick_best_from_srcset(self, srcset: str) -> Optional[str]:
        """
        srcset 示例：
        - "a.jpg 320w, b.jpg 640w"
        - "a.webp 1x, b.webp 2x"
        这里选 “最大” 的候选项。
        """
        best_url = None
        best_score = -1.0

        for part in srcset.split(','):
            item = part.strip()
            if not item:
                continue
            pieces = item.split()
            url = pieces[0]
            score = 0.0
            if len(pieces) >= 2:
                d = pieces[1].strip()
                try:
                    if d.endswith('w'):
                        score = float(d[:-1])
                    elif d.endswith('x'):
                        score = float(d[:-1]) * 10000.0
                except Exception:
                    score = 0.0
            if score >= best_score:
                best_score = score
                best_url = url

        return best_url

    def _detect_kind_from_bytes(self, data: bytes) -> str:
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
        # AVIF (ISO BMFF) - 兼容 ftypavif/avis
        if len(data) >= 12 and data[4:8] == b'ftyp' and (b'avif' in data[8:24] or b'avis' in data[8:24]):
            return 'avif'

        s = data.lstrip()
        if s.startswith(b'<!DOCTYPE html') or s.startswith(b'<html') or s.startswith(b'<head'):
            return 'html'
        if s.startswith(b'{') or s.startswith(b'['):
            return 'json'
        return 'unknown'

    def _ext_for_kind(self, kind: str) -> Optional[str]:
        return {
            'jpeg': '.jpg',
            'png': '.png',
            'gif': '.gif',
            'webp': '.webp',
            'avif': '.avif',
        }.get(kind)

    def _kind_from_ext(self, ext: str) -> Optional[str]:
        e = (ext or '').lower()
        if e == '.jpg' or e == '.jpeg':
            return 'jpeg'
        if e == '.png':
            return 'png'
        if e == '.gif':
            return 'gif'
        if e == '.webp':
            return 'webp'
        if e == '.avif':
            return 'avif'
        return None

    def _is_valid_image_bytes(self, kind: str, data: bytes) -> bool:
        # 基础校验：避免“半截/被截断/错误页”等进入仓库
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
            # RIFF chunk size（小端）+ 8 ~= 文件长度
            try:
                riff_size = int.from_bytes(data[4:8], 'little')
                return (riff_size + 8) <= (len(data) + 16)
            except Exception:
                return True
        if kind == 'avif':
            return len(data) >= 12 and data[4:8] == b'ftyp'
        return False

    def _is_valid_image_file(self, path: Path, kind: str) -> bool:
        """避免读全文件的轻量校验（用头尾判断截断/格式）。"""
        try:
            size = path.stat().st_size
            if size < 64:
                return False
            with open(path, 'rb') as f:
                head = f.read(64)
                if size <= 128:
                    data = head
                else:
                    f.seek(max(0, size - 64))
                    tail = f.read(64)
                    data = head + tail
            probe_kind = self._detect_kind_from_bytes(data)
            if probe_kind != kind:
                return False
            # 对截断判断仍需全文件末尾特征；这里用头尾信息 + size 粗判
            if kind == 'jpeg':
                return data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9')
            if kind == 'png':
                return data.startswith(b'\x89PNG\r\n\x1a\n') and (b'IEND' in data)
            if kind == 'gif':
                return (data.startswith(b'GIF87a') or data.startswith(b'GIF89a')) and data.endswith(b'\x3b')
            if kind == 'webp':
                if len(data) < 12 or data[0:4] != b'RIFF' or data[8:12] != b'WEBP':
                    return False
                try:
                    riff_size = int.from_bytes(data[4:8], 'little')
                    return (riff_size + 8) <= (size + 16)
                except Exception:
                    return True
            if kind == 'avif':
                return len(data) >= 12 and data[4:8] == b'ftyp'
            return False
        except Exception:
            return False

    def _download_image(self, url: str) -> Optional[str]:
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            # 1) 本地缓存命中：同一个 hash 可能对应不同扩展名（历史遗留）
            for ext in self._allowed_exts:
                candidate = self.images_dir / f"{url_hash}{ext}"
                if candidate.exists():
                    try:
                        expected = self._kind_from_ext(candidate.suffix)
                        if expected and self._is_valid_image_file(candidate, expected):
                            return str(candidate)
                    except Exception:
                        pass

            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'image/avif,image/webp,image/*,*/*;q=0.8',
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.content
            if not data or len(data) < 256:
                return None

            # 2) 探测真实类型（不要用 URL 猜扩展名）
            kind = self._detect_kind_from_bytes(data[:64] + data[-64:])
            ext = self._ext_for_kind(kind)
            if not ext:
                # 兜底：看 Content-Type
                ct = (response.headers.get('Content-Type') or '').lower()
                if 'image/jpeg' in ct:
                    kind, ext = 'jpeg', '.jpg'
                elif 'image/png' in ct:
                    kind, ext = 'png', '.png'
                elif 'image/gif' in ct:
                    kind, ext = 'gif', '.gif'
                elif 'image/webp' in ct:
                    kind, ext = 'webp', '.webp'
                elif 'image/avif' in ct:
                    kind, ext = 'avif', '.avif'

            if not ext or kind in {'html', 'json', 'unknown'}:
                return None
            if not self._is_valid_image_bytes(kind, data):
                return None

            filename = f"{url_hash}{ext}"
            local_path = self.images_dir / filename
            if local_path.exists():
                return str(local_path)

            with open(local_path, 'wb') as f:
                f.write(data)

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
