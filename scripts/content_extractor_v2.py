#!/usr/bin/env python3
"""
content_extractor_v2.py - 带图片位置保留的内容提取器 (v2.1 - 增强过滤)

改进:
- 过滤头像、导航图标等非正文图片
- 过滤评论区、相关文章等非正文内容
- 针对 Hugging Face 等特定网站优化
- 去除重复内容
"""

import os
import re
import hashlib
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, Set


class ContentExtractorV2:
    """带图片的内容提取器 - 增强版"""

    # 需要过滤的图片模式 (URL/class/id/alt 中包含这些关键词的图片会被跳过)
    SKIP_IMAGE_PATTERNS = [
        # 头像相关
        'avatar', 'profile', 'author', 'user-pic', 'userpic', 'gravatar',
        'contributor', 'writer', 'person', 'member', 'headshot',
        # 图标相关
        'icon', 'logo', 'badge', 'emoji', 'favicon', 'sprite',
        # UI 元素
        'button', 'arrow', 'chevron', 'caret', 'close', 'menu',
        'nav', 'footer', 'header', 'sidebar', 'widget',
        # 社交媒体
        'twitter', 'facebook', 'linkedin', 'github', 'social',
        'share', 'like', 'comment-avatar',
        # 广告/装饰
        'ad-', 'ads-', 'banner', 'promo', 'sponsor', 'placeholder',
        # Hugging Face 特定
        'huggingface.co/avatars', '/spaces/', 'thumb', 'reaction',
        'cdn-avatars.huggingface.co',  # HF 用户头像 CDN
        '/blog/assets/',  # HF 相关文章缩略图
        '/v1/production/uploads/',  # HF 头像上传路径
    ]

    # 需要移除的容器选择器 (这些区块的内容会被完全跳过)
    SKIP_CONTAINER_SELECTORS = [
        # 评论区
        '.comments', '#comments', '.comment-section', '.discussion',
        '[data-testid="comments"]', '.post-comments', '.comments-section',
        # 相关文章
        '.related', '.more-posts', '.recommended', '.suggested',
        '.you-might-like', '.also-read', '.more-from',
        '.article-card', '.related-articles',
        # 导航/页脚
        'nav', 'footer', 'header', '.navbar', '.navigation',
        '.sidebar', 'aside', '.widget', '.menu',
        # 作者信息区 (通常在文章末尾)
        '.author-bio', '.author-info', '.about-author', '.post-author',
        # 社交分享
        '.share', '.social-share', '.sharing', '.share-buttons',
        # 订阅/CTA
        '.subscribe', '.newsletter', '.cta', '.signup',
        # Hugging Face 特定
        '.BlogCard', '.blog-card', '[class*="BlogCard"]',
        '.user-row', '.reaction-', '.comment-form',
        '[class*="article-card"]', '[class*="ArticleCard"]',
        '[class*="comment"]', '[class*="Comment"]',
        # Databricks 特定
        '[class*="related"]', '[class*="sidebar"]',
    ]

    # 需要过滤的文本模式 (包含这些内容的段落会被跳过)
    SKIP_TEXT_PATTERNS = [
        r'^目录\s*$',  # 单独的"目录"
        r'^Table of Contents\s*$',
        r'^Share\s*$', r'^分享\s*$',
        r'^Related\s*(Posts|Articles)?\s*$',
        r'^更多.*文章\s*$',
        r'^Comments?\s*$', r'^评论\s*$',
        r'^\d+\s*(条回复|replies?|comments?)\s*$',
        r'^注册或登录',
        r'^Sign (up|in)',
        r'^\s*[-·•]\s*$',  # 单独的列表符号
        r'^\+\d+$',  # +292 这种
        # Databricks 页脚垃圾
        r'^产品\s*$',
        r'^\d{4}年\d{1,2}月\d{1,2}日\s*/\s*\d+分钟阅读',
        r'^\d+\s*min\s*read',
        # Hugging Face 相关文章标题（通常出现在侧边栏）
        r'^Smol2Operator',  # 常见的推荐文章
        r'^Gemma\s+\d',
        # 通用垃圾
        r'^Read\s+more\s*$',
        r'^阅读更多\s*$',
        r'^See\s+all\s*$',
        r'^查看全部\s*$',
    ]

    def __init__(self, images_dir: Path, user_agent: str = None):
        self.images_dir = images_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent or 'Mozilla/5.0 (compatible; AI-VC-Bot/2.0)'
        self._seen_texts: Set[str] = set()
        self._seen_images: Set[str] = set()

    def extract(self, html: str, base_url: str) -> Dict:
        """从 HTML 提取内容，保留图片位置"""
        soup = BeautifulSoup(html, 'html.parser')
        title = self._extract_title(soup)

        # 预处理: 移除不需要的容器
        self._remove_skip_containers(soup)

        article = self._find_article_container(soup, base_url)

        if not article:
            return {'blocks': [], 'title': title, 'images': []}

        # 重置去重集合
        self._seen_texts = set()
        self._seen_images = set()

        blocks = []
        images = []

        for element in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'figure', 'pre', 'ul', 'ol']):
            # 检查元素是否在被跳过的容器内
            if self._is_in_skip_container(element):
                continue

            if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = element.get_text(strip=True)

                # 跳过空内容、过短内容、重复内容、匹配跳过模式的内容
                if not text or len(text) < 5:
                    continue
                if text in self._seen_texts:
                    continue
                if self._should_skip_text(text):
                    continue

                self._seen_texts.add(text)
                prefix = '#' * int(element.name[1]) + ' ' if element.name.startswith('h') else ''
                blocks.append({'type': 'text', 'content': prefix + text})

            elif element.name == 'img':
                img_data = self._process_image(element, base_url)
                if img_data and img_data.get('src') not in self._seen_images:
                    self._seen_images.add(img_data.get('src', ''))
                    blocks.append(img_data)
                    if img_data.get('local_path'):
                        images.append(img_data['local_path'])

            elif element.name == 'figure':
                img = element.find('img')
                if img:
                    img_data = self._process_image(img, base_url)
                    if img_data and img_data.get('src') not in self._seen_images:
                        self._seen_images.add(img_data.get('src', ''))
                        caption = element.find('figcaption')
                        if caption:
                            img_data['alt'] = caption.get_text(strip=True)
                        blocks.append(img_data)
                        if img_data.get('local_path'):
                            images.append(img_data['local_path'])

            elif element.name == 'pre':
                code = element.get_text()
                if code and len(code) > 10:
                    # 检测代码语言
                    lang = ''
                    code_tag = element.find('code')
                    if code_tag:
                        classes = code_tag.get('class', [])
                        for cls in classes:
                            if cls.startswith('language-'):
                                lang = cls.replace('language-', '')
                                break
                    blocks.append({'type': 'code', 'content': code, 'language': lang})

            elif element.name in ['ul', 'ol']:
                items = []
                for li in element.find_all('li', recursive=False):
                    item_text = li.get_text(strip=True)
                    # 过滤空列表项和过短项
                    if item_text and len(item_text) > 2 and not self._should_skip_text(item_text):
                        items.append(item_text)
                if items:
                    blocks.append({'type': 'list', 'items': items, 'ordered': element.name == 'ol'})

        # 后处理: 去除连续重复的内容块
        blocks = self._deduplicate_blocks(blocks)

        return {'blocks': blocks, 'title': title, 'images': images}

    def _remove_skip_containers(self, soup: BeautifulSoup):
        """预处理: 移除不需要的容器"""
        for selector in self.SKIP_CONTAINER_SELECTORS:
            try:
                for elem in soup.select(selector):
                    elem.decompose()
            except:
                pass

    def _is_in_skip_container(self, element: Tag) -> bool:
        """检查元素是否在需要跳过的容器内"""
        for parent in element.parents:
            if not isinstance(parent, Tag):
                continue
            parent_classes = ' '.join(parent.get('class', []))
            parent_id = parent.get('id', '')

            # 检查是否匹配跳过模式
            check_str = f"{parent_classes} {parent_id}".lower()
            skip_keywords = ['comment', 'related', 'sidebar', 'footer', 'nav',
                           'author-bio', 'share', 'social', 'subscribe', 'blogcard']
            if any(kw in check_str for kw in skip_keywords):
                return True
        return False

    def _should_skip_text(self, text: str) -> bool:
        """检查文本是否应该被跳过"""
        for pattern in self.SKIP_TEXT_PATTERNS:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False

    def _deduplicate_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """去除连续重复的内容块"""
        if not blocks:
            return blocks

        result = [blocks[0]]
        for block in blocks[1:]:
            # 比较当前块和上一个块
            last = result[-1]
            if block['type'] == last['type']:
                if block['type'] == 'text' and block['content'] == last['content']:
                    continue
                if block['type'] == 'list' and block.get('items') == last.get('items'):
                    continue
            result.append(block)
        return result

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

    def _find_article_container(self, soup: BeautifulSoup, base_url: str = ''):
        """查找文章容器，针对不同网站优化"""
        # Hugging Face Blog 特定处理
        if 'huggingface.co' in base_url:
            # HF 的文章内容通常在特定的容器中
            # 优先查找精确的文章内容容器
            for selector in ['.blog-content', '.prose:not(.prose-sm)',
                           '[class*="prose"]:not([class*="card"])',
                           '.markdown-body', 'article > .container']:
                container = soup.select_one(selector)
                if container:
                    # 对 HF，进一步清理：移除文章末尾的相关内容
                    self._clean_hf_article(container)
                    return container

        # Databricks Blog 特定处理
        if 'databricks.com' in base_url:
            for selector in ['.blog-post-content', '.post-content',
                           'article .content', '.entry-content']:
                container = soup.select_one(selector)
                if container:
                    # 清理 Databricks 文章末尾的导航垃圾
                    self._clean_databricks_article(container)
                    return container

        # 通用选择器
        selectors = [
            'article',
            '[role="main"]',
            '.post-content',
            '.article-content',
            '.entry-content',
            '.prose',
            '.markdown-body',
            '.post-body',
            'main .content',
            'main'
        ]

        for selector in selectors:
            container = soup.select_one(selector)
            if container:
                # 验证容器内有足够的内容
                text_len = len(container.get_text(strip=True))
                if text_len > 500:  # 至少500字符
                    return container

        return soup.find('body')

    def _clean_hf_article(self, container: Tag):
        """清理 Hugging Face 文章中的非正文内容"""
        # 移除包含 "blog/assets" 的图片（相关文章缩略图）
        for img in container.find_all('img'):
            src = img.get('src', '') or img.get('data-src', '')
            if '/blog/assets/' in src or 'cdn-avatars' in src:
                # 移除整个 figure 或图片本身
                parent = img.find_parent('figure')
                if parent:
                    parent.decompose()
                else:
                    img.decompose()

        # 移除看起来像相关文章标题的 h2/h3（通常在文章末尾）
        # 这些标题后面紧跟的是卡片式布局
        for heading in container.find_all(['h2', 'h3']):
            text = heading.get_text(strip=True)
            # 检查是否是非正文内容的标志
            if any(marker in text.lower() for marker in
                   ['related', 'more from', 'you might', 'also read',
                    'trending', 'popular', 'recent posts']):
                # 移除这个标题及其后面的所有兄弟元素
                for sibling in list(heading.find_next_siblings()):
                    sibling.decompose()
                heading.decompose()

    def _clean_databricks_article(self, container: Tag):
        """清理 Databricks 文章中的非正文内容"""
        # 查找并移除文章末尾的导航元素
        # Databricks 文章末尾通常有 "产品" + 日期 的格式
        all_p = container.find_all('p')
        for i, p in enumerate(all_p):
            text = p.get_text(strip=True)
            # 检测 Databricks 特有的页脚模式
            if text == '产品' or re.match(r'^\d{4}年\d{1,2}月\d{1,2}日', text):
                # 移除这个段落及其后面的所有兄弟元素
                for sibling in list(p.find_next_siblings()):
                    sibling.decompose()
                p.decompose()
                break

    def _process_image(self, img_tag: Tag, base_url: str) -> Optional[Dict]:
        """处理图片，过滤非正文图片"""
        src = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy-src')
        if not src:
            return None

        # 获取图片的各种属性用于过滤判断
        alt = img_tag.get('alt', '')
        classes = ' '.join(img_tag.get('class', []))
        img_id = img_tag.get('id', '')

        # 构建检查字符串
        check_str = f"{src} {alt} {classes} {img_id}".lower()

        # 检查是否匹配跳过模式
        for pattern in self.SKIP_IMAGE_PATTERNS:
            if pattern.lower() in check_str:
                return None

        # 跳过 base64 图片、SVG、图标等
        if src.startswith('data:'):
            return None
        if src.endswith('.svg'):
            return None

        # 检查图片尺寸 (如果有的话)
        width = img_tag.get('width', '')
        height = img_tag.get('height', '')
        try:
            w = int(str(width).replace('px', ''))
            h = int(str(height).replace('px', ''))
            # 跳过小图片 (很可能是图标/头像)
            if w < 100 or h < 100:
                return None
            # 跳过明显是头像的正方形小图
            if w == h and w < 200:
                return None
        except:
            pass

        img_url = urljoin(base_url, src)
        local_path = self._download_image(img_url)

        return {
            'type': 'image',
            'src': img_url,
            'alt': alt,
            'local_path': local_path
        }

    def _download_image(self, url: str) -> Optional[str]:
        """下载图片到本地"""
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

            # 更好的扩展名检测
            parsed = urlparse(url)
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
                ext = '.jpg'  # 默认

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

            # 检查文件大小，过小的图片可能是占位符
            if len(response.content) < 500:
                return None

            with open(local_path, 'wb') as f:
                f.write(response.content)

            print(f"    ✓ 下载图片: {filename}")
            return str(local_path)

        except Exception as e:
            print(f"    ✗ 图片下载失败: {e}")
            return None

    def blocks_to_markdown(self, blocks: List[Dict], image_base_path: str = '/images/posts') -> str:
        """将内容块转换为 Markdown"""
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
                lang = block.get('language', '')
                lines.append(f'```{lang}')
                lines.append(block['content'])
                lines.append('```')
                lines.append('')
            elif block['type'] == 'list':
                for i, item in enumerate(block['items']):
                    prefix = f"{i+1}. " if block.get('ordered') else "- "
                    lines.append(prefix + item)
                lines.append('')
        return '\n'.join(lines)
