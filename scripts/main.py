#!/usr/bin/env python3
#!/usr/bin/env python3
"""
AI/VC前沿观察 - 内容抓取与翻译主脚本 (v2.1 - 并行版本)

新增功能:
- 并行处理文章翻译（默认3个worker）
- --workers 参数控制并发数
- 线程安全的状态管理

使用方法:
    python main.py                                    # 处理所有启用的源（3并发）
    python main.py --workers 5                        # 使用5个并发
    python main.py --source a16z --max-per-source 3  # 只处理a16z，最多3篇
    python main.py --backfill --since 2024-01-01     # 回填历史内容
"""

import os
import sys
import json
import time
import hashlib
import logging
import argparse
import tempfile
import shutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Set, Tuple, Any
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
import feedparser
import requests
from bs4 import BeautifulSoup


# ============================================
# 内容清洗器 (ContentCleaner)
# ============================================

class ContentCleaner:
    """
    内容清洗器 - 清除导航菜单、页脚等垃圾内容
    """
    
    GARBAGE_PATTERNS = {
        'databricks': {
            'header_garbage': [
                '为什么选择 Databricks', '为何选择 Databricks',
                'Why Databricks', '面向高管', '面向初创企业', 
                '湖仓一体架构', '客户案例', '云服务提供商', '平台概览',
                '数据管理', '数据仓库', '数据工程', '商业智能',
                '培训', '认证', '免费版', '试用 Databricks',
                'Databricks 定价', '成本计算器', '咨询与系统集成商',
                'Data + AI 峰会', '博客与播客', '客户支持', '文档', '社区',
                '我们是谁', '我们的团队', '开放职位', '安全与信任',
                '准备开始了吗？', '探索产品定价',
            ],
            'footer_garbage': [
                '© Databricks', '1-866-330-0121',
                'Databricks学院登录', '查看 Databricks 的职位',
                '联系我们', '关于我们', '隐私政策', '使用条款',
                '准备好开始了吗', 'Ready to get started',
            ],
        },
        'sequoia': {
            'header_garbage': ['About', 'Companies', 'Perspectives', 'People'],
            'footer_garbage': ['© Sequoia', 'Privacy Policy', 'All rights reserved'],
        },
        'a16z': {
            'header_garbage': ['About', 'Portfolio', 'News', 'Podcasts', 'Newsletter'],
            'footer_garbage': ['© Andreessen Horowitz', 'Privacy Policy', 'Disclosures'],
        },
        '_default': {
            'header_garbage': ['Skip to content', 'Navigation', 'Menu'],
            'footer_garbage': ['All rights reserved', 'Privacy Policy', 'Terms of Service'],
        },
    }
    
    def __init__(self, source_name, logger=None):
        self.source_name = source_name.lower()
        self.logger = logger
        self.patterns = None
        for key in self.GARBAGE_PATTERNS:
            if key in self.source_name or self.source_name in key:
                self.patterns = self.GARBAGE_PATTERNS[key]
                break
        if self.patterns is None:
            self.patterns = self.GARBAGE_PATTERNS.get('_default', {})
    
    def clean(self, content):
        if not content:
            return content
        original_length = len(content)
        content = self._remove_header_garbage(content)
        content = self._remove_footer_garbage(content)
        cleaned_length = len(content)
        if self.logger and original_length != cleaned_length:
            removed = original_length - cleaned_length
            self.logger.info(f"  [ContentCleaner] 清洗了 {removed} 字符 ({removed*100//original_length}%)")
        return content.strip()
    
    def _remove_header_garbage(self, content):
        header_keywords = self.patterns.get('header_garbage', [])
        if not header_keywords:
            return content
        lines = content.split('\n')
        title_line_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('# ') and len(stripped) > 10:
                is_menu = any(kw.lower() in stripped.lower() for kw in header_keywords[:20])
                if not is_menu:
                    title_line_idx = i
                    break
            if i < 100 and len(stripped) > 80:
                is_garbage = any(kw.lower() in stripped.lower() for kw in header_keywords)
                if not is_garbage:
                    title_line_idx = i
                    break
        if title_line_idx > 5:
            header_content = '\n'.join(lines[:title_line_idx])
            has_garbage = any(kw.lower() in header_content.lower() for kw in header_keywords)
            if has_garbage:
                return '\n'.join(lines[title_line_idx:])
        return content
    
    def _remove_footer_garbage(self, content):
        footer_keywords = self.patterns.get('footer_garbage', [])
        if not footer_keywords:
            return content
        lines = content.split('\n')
        cutoff_idx = len(lines)
        for i in range(len(lines) - 1, max(0, len(lines) - 150), -1):
            line = lines[i].strip()
            if any(kw.lower() in line.lower() for kw in footer_keywords):
                following_lines = '\n'.join(lines[i:i+10])
                footer_indicators = sum(1 for kw in footer_keywords if kw.lower() in following_lines.lower())
                if footer_indicators >= 2:
                    cutoff_idx = i
                    break
        for i in range(cutoff_idx, len(lines)):
            if lines[i].strip() == '---' or '本文由AI自动翻译' in lines[i]:
                cutoff_idx = i
                break
        if cutoff_idx < len(lines):
            return '\n'.join(lines[:cutoff_idx])
        return content

from content_extractor_v2 import ContentExtractorV2
from openai import OpenAI

# ============================================
# 路径探测与初始化
# ============================================

def find_project_root(start_path: Path = None) -> Path:
    if start_path is None:
        start_path = Path(__file__).resolve().parent
    
    current = start_path
    for _ in range(10):
        if (current / "data" / "sources.yaml").exists():
            return current
        if (current / "sources.yaml").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    return Path(__file__).resolve().parent.parent


def setup_directories(project_root: Path) -> Tuple[Path, Path, Path, Path]:
    content_dir = project_root / "content" / "posts"
    data_dir = project_root / "data"
    logs_dir = project_root / "logs"
    
    content_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    return project_root, content_dir, data_dir, logs_dir


def setup_logging(logs_dir: Path) -> logging.Logger:
    log_file = logs_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================
# 配置加载
# ============================================

class Config:
    def __init__(self, sources_path: Path):
        self.sources_path = sources_path
        self._data = None
        self._load()
    
    def _load(self):
        with open(self.sources_path, 'r', encoding='utf-8') as f:
            self._data = yaml.safe_load(f)
    
    @property
    def settings(self) -> Dict:
        return self._data.get('settings', {})
    
    @property
    def user_agent(self) -> str:
        return self.settings.get('user_agent', 
            'Mozilla/5.0 (compatible; AI-VC-Observer/1.0)')
    
    @property
    def request_delay(self) -> float:
        return self.settings.get('request_delay', 2.0)
    
    @property
    def translation_model(self) -> str:
        return self.settings.get('translation_model', 'deepseek-chat')
    
    @property
    def categories(self) -> List[str]:
        return self.settings.get('categories', [
            'AI研究', 'AI产品', 'AI基础设施', 'VC观点', '创业', '技术趋势', '政策监管', '未分类'
        ])
    
    def get_sources(self, category: str = None) -> List[Dict]:
        sources = []
        for cat in ['vc_funds', 'investors', 'ai_research', 'tech_blogs']:
            sources.extend(self._data.get(cat, []))
        
        if category:
            sources = [s for s in sources if s.get('name') == category]
        
        return [s for s in sources if s.get('enabled', True)]


# ============================================
# URL状态管理（线程安全版本）
# ============================================

class URLStateManager:
    def __init__(self, data_dir: Path):
        self.processed_file = data_dir / "processed_urls.json"
        self.failed_file = data_dir / "failed_urls.json"
        self.etag_file = data_dir / "feed_etags.json"
        
        self._processed: Set[str] = set()
        self._failed: Dict[str, Dict] = {}
        self._etags: Dict[str, Dict] = {}
        
        # 线程锁
        self._lock = threading.Lock()
        
        self._load()
    
    def _load(self):
        if self.processed_file.exists():
            with open(self.processed_file, 'r') as f:
                self._processed = set(json.load(f))
        
        if self.failed_file.exists():
            with open(self.failed_file, 'r') as f:
                self._failed = json.load(f)
        
        if self.etag_file.exists():
            with open(self.etag_file, 'r') as f:
                self._etags = json.load(f)
    
    def _atomic_save(self, filepath: Path, data: Any):
        temp_fd, temp_path = tempfile.mkstemp(
            suffix='.json', 
            dir=filepath.parent
        )
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            shutil.move(temp_path, filepath)
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
    
    def is_processed(self, url: str) -> bool:
        with self._lock:
            return url in self._processed
    
    def is_failed(self, url: str, max_retries: int = 3) -> bool:
        with self._lock:
            if url not in self._failed:
                return False
            return self._failed[url].get('count', 0) >= max_retries
    
    def mark_processed(self, url: str):
        with self._lock:
            self._processed.add(url)
            self._atomic_save(self.processed_file, list(self._processed))
    
    def mark_failed(self, url: str, reason: str):
        with self._lock:
            if url not in self._failed:
                self._failed[url] = {'count': 0}
            
            self._failed[url].update({
                'reason': reason,
                'timestamp': datetime.now().isoformat(),
                'count': self._failed[url].get('count', 0) + 1
            })
            self._atomic_save(self.failed_file, self._failed)
    
    def get_etag(self, feed_url: str) -> Tuple[Optional[str], Optional[str]]:
        with self._lock:
            info = self._etags.get(feed_url, {})
            return info.get('etag'), info.get('last_modified')
    
    def set_etag(self, feed_url: str, etag: str = None, last_modified: str = None):
        with self._lock:
            self._etags[feed_url] = {
                'etag': etag,
                'last_modified': last_modified,
                'updated': datetime.now().isoformat()
            }
            self._atomic_save(self.etag_file, self._etags)


# ============================================
# RSS自动发现
# ============================================

class RSSDiscovery:
    COMMON_FEED_PATHS = [
        '/feed', '/feed/', '/rss', '/rss/', '/atom.xml',
        '/feed.xml', '/rss.xml', '/index.xml', '/blog/feed',
        '/blog/rss', '/feeds/posts/default',
    ]
    
    def __init__(self, user_agent: str, cache_file: Path = None):
        self.user_agent = user_agent
        self.cache_file = cache_file
        self._cache: Dict[str, str] = {}
        self._lock = threading.Lock()
        
        if cache_file and cache_file.exists():
            with open(cache_file, 'r') as f:
                self._cache = json.load(f)
    
    def _save_cache(self):
        if self.cache_file:
            with self._lock:
                with open(self.cache_file, 'w') as f:
                    json.dump(self._cache, f, indent=2)
    
    def discover(self, homepage_url: str) -> Optional[str]:
        with self._lock:
            if homepage_url in self._cache:
                return self._cache[homepage_url]
        
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(homepage_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('link', rel='alternate'):
                link_type = link.get('type', '')
                if 'rss' in link_type or 'atom' in link_type or 'xml' in link_type:
                    feed_url = link.get('href')
                    if feed_url:
                        feed_url = urljoin(homepage_url, feed_url)
                        if self._validate_feed(feed_url):
                            with self._lock:
                                self._cache[homepage_url] = feed_url
                            self._save_cache()
                            return feed_url
            
            parsed = urlparse(homepage_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            for path in self.COMMON_FEED_PATHS:
                feed_url = base_url + path
                if self._validate_feed(feed_url):
                    with self._lock:
                        self._cache[homepage_url] = feed_url
                    self._save_cache()
                    return feed_url
            
            with self._lock:
                self._cache[homepage_url] = None
            self._save_cache()
            return None
            
        except Exception:
            return None
    
    def _validate_feed(self, feed_url: str) -> bool:
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(feed_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return False
            
            content_type = response.headers.get('Content-Type', '')
            if any(t in content_type for t in ['xml', 'rss', 'atom']):
                return True
            
            content = response.text[:500].lower()
            return '<rss' in content or '<feed' in content or '<atom' in content
            
        except Exception:
            return False


# ============================================
# 内容抓取器
# ============================================

class ContentFetcher:
    def __init__(self, config: Config, state_manager: URLStateManager, logger: logging.Logger):
        self.config = config
        self.state = state_manager
        self.logger = logger
        self.rss_discovery = RSSDiscovery(
            config.user_agent,
            cache_file=state_manager.processed_file.parent / "rss_cache.json"
        )
    
        # 图片提取器
        images_dir = state_manager.processed_file.parent.parent / "public" / "images" / "posts"
        images_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = ContentExtractorV2(images_dir)

    def fetch_from_source(
        self, 
        source: Dict, 
        max_items: int = 5,
        since_date: datetime = None
    ) -> List[Dict]:
        source_type = source.get('type', 'rss')
        
        if source_type == 'rss' and source.get('feed_url'):
            return self._fetch_rss(source, max_items, since_date)
        
        elif source_type == 'sitemap' and source.get('sitemap_url'):
            return self._fetch_sitemap(source, max_items, since_date)
        
        elif source_type == 'homepage':
            feed_url = self.rss_discovery.discover(source.get('url'))
            if feed_url:
                source = {**source, 'feed_url': feed_url, 'type': 'rss'}
                return self._fetch_rss(source, max_items, since_date)
            else:
                self.logger.warning(f"无法为 {source['name']} 发现RSS，跳过")
                return []
        
        else:
            self.logger.warning(f"不支持的源类型: {source_type}")
            return []
    
    def _fetch_rss(
        self, 
        source: Dict, 
        max_items: int,
        since_date: datetime = None
    ) -> List[Dict]:
        feed_url = source['feed_url']
        
        headers = {'User-Agent': self.config.user_agent}
        etag, last_modified = self.state.get_etag(feed_url)
        if etag:
            headers['If-None-Match'] = etag
        if last_modified:
            headers['If-Modified-Since'] = last_modified
        
        try:
            response = requests.get(feed_url, headers=headers, timeout=30)
            
            if response.status_code == 304:
                self.logger.info(f"[{source['name']}] Feed未更新 (304)")
                return []
            
            response.raise_for_status()
            
            new_etag = response.headers.get('ETag')
            new_last_modified = response.headers.get('Last-Modified')
            if new_etag or new_last_modified:
                self.state.set_etag(feed_url, new_etag, new_last_modified)
            
            feed = feedparser.parse(response.content)
            
        except Exception as e:
            self.logger.error(f"[{source['name']}] RSS获取失败: {e}")
            return []
        
        # 收集所有未处理的文章（不限制数量）
        all_articles = []
        for entry in feed.entries:
            url = entry.get('link', '')

            if self.state.is_processed(url):
                continue
            if self.state.is_failed(url):
                continue

            pub_date = None
            if 'published_parsed' in entry and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif 'updated_parsed' in entry and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            if since_date and pub_date and pub_date < since_date:
                continue

            all_articles.append({
                'title': entry.get('title', ''),
                'url': url,
                'published': pub_date,
                'author': entry.get('author', ''),
                'summary': entry.get('summary', ''),
            })

        # 按发布日期排序（最新的在前），确保优先翻译新文章
        all_articles.sort(
            key=lambda x: x['published'] if x['published'] else datetime.min,
            reverse=True
        )

        # 返回前 max_items 篇
        articles = all_articles[:max_items]
        self.logger.info(f"[{source['name']}] 从RSS获取 {len(articles)} 篇待处理文章（共 {len(all_articles)} 篇未处理）")
        return articles
    
    def _fetch_sitemap(
        self, 
        source: Dict, 
        max_items: int,
        since_date: datetime = None
    ) -> List[Dict]:
        sitemap_url = source['sitemap_url']
        
        try:
            headers = {'User-Agent': self.config.user_agent}
            response = requests.get(sitemap_url, headers=headers, timeout=30)
            response.raise_for_status()

            # 处理gzip压缩的sitemap
            content = response.content
            if sitemap_url.endswith('.gz'):
                import gzip
                content = gzip.decompress(content)

            root = ElementTree.fromstring(content)
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            if root.tag.endswith('sitemapindex'):
                articles = []
                for sitemap in root.findall('.//sm:sitemap', ns):
                    loc = sitemap.find('sm:loc', ns)
                    if loc is not None:
                        sub_source = {**source, 'sitemap_url': loc.text}
                        articles.extend(self._fetch_sitemap(sub_source, max_items - len(articles), since_date))
                        if len(articles) >= max_items:
                            break
                return articles
            
            # 收集所有未处理的文章
            all_articles = []
            for url_elem in root.findall('.//sm:url', ns):
                loc = url_elem.find('sm:loc', ns)
                lastmod = url_elem.find('sm:lastmod', ns)

                if loc is None:
                    continue

                url = loc.text

                # URL模式过滤：如果配置了url_pattern，只抓取匹配的URL
                url_pattern = source.get('url_pattern')
                if url_pattern and url_pattern not in url:
                    continue

                if self.state.is_processed(url):
                    continue
                if self.state.is_failed(url):
                    continue

                pub_date = None
                if lastmod is not None and lastmod.text:
                    try:
                        pub_date = datetime.fromisoformat(lastmod.text.replace('Z', '+00:00'))
                        pub_date = pub_date.replace(tzinfo=None)
                    except:
                        pass

                if since_date and pub_date and pub_date < since_date:
                    continue

                all_articles.append({
                    'title': '',
                    'url': url,
                    'published': pub_date,
                    'author': '',
                    'summary': '',
                })

            # 按发布日期排序（最新的在前）
            all_articles.sort(
                key=lambda x: x['published'] if x['published'] else datetime.min,
                reverse=True
            )

            # 返回前 max_items 篇
            articles = all_articles[:max_items]
            self.logger.info(f"[{source['name']}] 从Sitemap获取 {len(articles)} 篇待处理文章（共 {len(all_articles)} 篇未处理）")
            return articles
            
        except Exception as e:
            self.logger.error(f"[{source['name']}] Sitemap获取失败: {e}")
            return []
    
    def fetch_article_content(self, url: str) -> Optional[Dict]:
        """使用 ContentExtractorV2 提取内容（带图片）"""
        try:
            headers = {'User-Agent': self.config.user_agent}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            html = response.text
            result = self.extractor.extract(html, url)

            if not result['blocks']:
                return None

            text_blocks = [b for b in result['blocks'] if b['type'] == 'text']
            img_blocks = [b for b in result['blocks'] if b['type'] == 'image']
            self.logger.info(f"    提取: {len(text_blocks)} 文本块, {len(img_blocks)} 图片")

            content_md = self.extractor.blocks_to_markdown(result['blocks'])

            if len(content_md) < 200:
                return None

            return {
                'content': content_md,
                'title': result.get('title', ''),
                'author': '',
                'date': '',
                'blocks': result['blocks'],
            }

        except Exception as e:
            self.logger.error(f"内容提取失败: {e}")
            return None

# ============================================
# 翻译器
# ============================================

class Translator:
    GLOSSARY = {
        'LLM': 'LLM（大语言模型）',
        'Large Language Model': '大语言模型',
        'GPT': 'GPT',
        'Transformer': 'Transformer',
        'Fine-tuning': '微调',
        'Prompt': '提示词',
        'RAG': 'RAG（检索增强生成）',
        'Agent': 'Agent（智能体）',
        'Embedding': '嵌入/向量',
        'Vector Database': '向量数据库',
        'Inference': '推理',
        'Token': 'Token',
        'Context Window': '上下文窗口',
        'Hallucination': '幻觉',
        'Alignment': '对齐',
        'RLHF': 'RLHF（人类反馈强化学习）',
        'Chain-of-Thought': '思维链',
        'Multimodal': '多模态',
        'Foundation Model': '基础模型',
        'Open Source': '开源',
        'API': 'API',
        'SaaS': 'SaaS',
        'B2B': 'B2B',
        'B2C': 'B2C',
        'ARR': 'ARR（年度经常性收入）',
        'PMF': 'PMF（产品市场契合）',
        'TAM': 'TAM（总可寻址市场）',
        'Moat': '护城河',
        'Network Effect': '网络效应',
        'Flywheel': '飞轮效应',
        'Series A': 'A轮',
        'Series B': 'B轮',
        'Seed Round': '种子轮',
        'Venture Capital': '风险投资',
        'VC': 'VC（风险投资）',
        'Due Diligence': '尽职调查',
    }
    
    MAX_CHUNK_SIZE = 8000
    
    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        base_url = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        
        if not api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = config.translation_model
    
    def _build_glossary_text(self) -> str:
        lines = []
        for en, zh in self.GLOSSARY.items():
            lines.append(f"- {en} → {zh}")
        return "\n".join(lines)
    
    def _split_content(self, content: str) -> List[str]:
        if len(content) <= self.MAX_CHUNK_SIZE:
            return [content]
        
        chunks = []
        paragraphs = content.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= self.MAX_CHUNK_SIZE:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                if len(para) > self.MAX_CHUNK_SIZE:
                    words = para.split('. ')
                    sub_chunk = ""
                    for sentence in words:
                        if len(sub_chunk) + len(sentence) + 2 <= self.MAX_CHUNK_SIZE:
                            sub_chunk += sentence + ". "
                        else:
                            if sub_chunk:
                                chunks.append(sub_chunk.strip())
                            sub_chunk = sentence + ". "
                    if sub_chunk:
                        current_chunk = sub_chunk
                else:
                    current_chunk = para + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_content(self, content: str, article_title: str = "") -> str:
        chunks = self._split_content(content)
        translated_chunks = []
        
        for i, chunk in enumerate(chunks):
            self.logger.info(f"    翻译第 {i+1}/{len(chunks)} 段...")
            
            prompt = f"""请将以下英文内容翻译成中文。

翻译要求：
1. 准确传达原文含义，语言自然流畅
2. 保持原文的段落结构
3. 专业术语参考以下术语表：
{self._build_glossary_text()}

4. 代码块、公式、URL保持原样不翻译
5. 不要添加任何解释或评论，只输出翻译结果

原文：
{chunk}

翻译："""
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=4000,
                )
                translated = response.choices[0].message.content.strip()
                translated_chunks.append(translated)
                
                if i < len(chunks) - 1:
                    time.sleep(0.5)
                    
            except Exception as e:
                self.logger.error(f"    翻译失败: {e}")
                translated_chunks.append(f"[翻译失败，原文如下]\n\n{chunk}")
        
        return "\n\n".join(translated_chunks)
    
    def generate_metadata(self, content: str, original_title: str) -> Dict:
        categories_list = ", ".join(self.config.categories)
        
        prompt = f"""请为以下文章生成元数据。

文章原标题：{original_title}

文章内容（前2000字）：
{content[:2000]}

请生成以下信息，以JSON格式返回：
{{
    "title_zh": "中文标题（简洁有力，不超过30字）",
    "summary_zh": "中文摘要（100-150字，概括文章核心观点）",
    "category": "分类（从以下选项中选一个：{categories_list}）",
    "tags": ["标签1", "标签2", "标签3"]（3-5个相关标签）
}}

只返回JSON，不要其他内容。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            
            result_text = response.choices[0].message.content.strip()
            
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1]
            if result_text.endswith('```'):
                result_text = result_text.rsplit('\n', 1)[0]
            if result_text.startswith('json'):
                result_text = result_text[4:]
            
            metadata = json.loads(result_text)
            
            if metadata.get('category') not in self.config.categories:
                metadata['category'] = '未分类'
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"    元数据生成失败: {e}")
            return {
                'title_zh': original_title,
                'summary_zh': content[:150] + '...',
                'category': '未分类',
                'tags': []
            }
    
    def translate_article(self, article: Dict) -> Dict:
        content = article.get('content', '')
        title = article.get('title', '')
        
        translated_content = self.translate_content(content, title)
        
        self.logger.info(f"    生成元数据...")
        metadata = self.generate_metadata(translated_content, title)
        
        return {
            'content_zh': translated_content,
            **metadata
        }


# ============================================
# 文章生成器（线程安全）
# ============================================

class ArticleGenerator:
    def __init__(self, content_dir: Path, logger: logging.Logger):
        self.content_dir = content_dir
        self.logger = logger
        self._lock = threading.Lock()
    
    def generate(self, article: Dict, translated: Dict, source: Dict) -> Path:
        date_str = datetime.now().strftime('%Y-%m-%d')
        if article.get('published'):
            date_str = article['published'].strftime('%Y-%m-%d')
        
        url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
        slug = f"{date_str}-{source['name']}-{url_hash}"
        
        filepath = self.content_dir / f"{slug}.md"
        
        front_matter = {
            'title': translated.get('title_zh', article.get('title', '')),
            'title_original': article.get('title', ''),
            'date': date_str,
            'source': source.get('display_name', source['name']),
            'source_url': article['url'],
            'author': article.get('author', ''),
            'summary': translated.get('summary_zh', ''),
            'categories': [translated.get('category', '未分类')],
            'tags': translated.get('tags', []),
            'draft': False,
            'translated_at': datetime.now().isoformat(),
        }
        
        front_matter_yaml = yaml.safe_dump(
            front_matter, 
            allow_unicode=True, 
            default_flow_style=False,
            sort_keys=False
        )
        
        content = f"""---
{front_matter_yaml}---

{translated.get('content_zh', '')}

---

> 本文由AI自动翻译，原文链接：[{article.get('title', '原文')}]({article['url']})
> 
> 翻译时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        with self._lock:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        self.logger.info(f"    ✓ 生成文章: {filepath.name}")
        return filepath


# ============================================
# 主流水线（并行版本）
# ============================================

class Pipeline:
    def __init__(
        self, 
        config: Config, 
        state: URLStateManager,
        content_dir: Path,
        logger: logging.Logger,
        max_workers: int = 3
    ):
        self.config = config
        self.state = state
        self.logger = logger
        self.max_workers = max_workers
        
        self.fetcher = ContentFetcher(config, state, logger)
        self.translator = Translator(config, logger)
        self.generator = ArticleGenerator(content_dir, logger)
    
    def _process_single_article(
        self, 
        article: Dict, 
        source: Dict,
        index: int,
        total: int
    ) -> bool:
        """处理单篇文章（可并行）"""
        url = article['url']
        title_short = article.get('title', url)[:50]
        
        self.logger.info(f"  [{index}/{total}] {title_short}...")
        
        try:
            # 获取完整内容
            full_content = self.fetcher.fetch_article_content(url)
            
            if not full_content:
                self.logger.warning(f"    内容获取失败，跳过")
                self.state.mark_failed(url, "content_extraction_failed")
                return False
            
            # 合并信息
            article.update(full_content)

            # 清洗内容 - 删除导航菜单和页脚垃圾
            cleaner = ContentCleaner(source['name'], self.logger)
            article['content'] = cleaner.clean(article['content'])
            
            # 检查清洗后内容是否足够
            if len(article.get('content', '')) < 200:
                self.logger.warning(f"    清洗后内容过短，跳过")
                self.state.mark_failed(url, "content_too_short_after_cleaning")
                return False
            
            # 翻译
            self.logger.info(f"    开始翻译正文（{len(article.get('content', ''))} 字符）...")
            translated = self.translator.translate_article(article)
            
            # 生成文章
            self.generator.generate(article, translated, source)
            
            # 标记为已处理
            self.state.mark_processed(url)
            
            return True
            
        except Exception as e:
            self.logger.error(f"    处理失败: {e}")
            self.state.mark_failed(url, str(e))
            return False
    
    def process_source(
        self, 
        source: Dict, 
        max_items: int = 5,
        since_date: datetime = None
    ) -> int:
        """处理单个源（并行处理文章）"""
        self.logger.info(f"处理源: {source.get('display_name', source['name'])}")
        
        # 1. 获取文章列表（串行）
        articles = self.fetcher.fetch_from_source(source, max_items, since_date)
        
        if not articles:
            self.logger.info(f"  没有新文章")
            return 0
        
        # 2. 并行处理文章
        processed_count = 0
        total = len(articles)
        
        if self.max_workers <= 1:
            # 串行模式
            for i, article in enumerate(articles):
                if self._process_single_article(article, source, i+1, total):
                    processed_count += 1
                time.sleep(self.config.request_delay)
        else:
            # 并行模式
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(
                        self._process_single_article, 
                        article, 
                        source, 
                        i+1, 
                        total
                    ): article 
                    for i, article in enumerate(articles)
                }
                
                for future in as_completed(futures):
                    try:
                        if future.result():
                            processed_count += 1
                    except Exception as e:
                        self.logger.error(f"  并行处理异常: {e}")
        
        return processed_count
    
    def run(
        self,
        source_filter: str = None,
        max_per_source: int = 5,
        since_date: datetime = None
    ) -> int:
        """运行完整流水线"""
        self.logger.info("=" * 60)
        self.logger.info(f"开始处理 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"参数: source={source_filter}, max={max_per_source}, workers={self.max_workers}")
        self.logger.info("=" * 60)
        
        sources = self.config.get_sources(source_filter)
        
        if not sources:
            self.logger.warning("没有找到匹配的源")
            return 0
        
        total_processed = 0
        
        for source in sources:
            try:
                count = self.process_source(source, max_per_source, since_date)
                total_processed += count
            except Exception as e:
                self.logger.error(f"源 {source['name']} 处理失败: {e}")
                continue
        
        self.logger.info("=" * 60)
        self.logger.info(f"处理完成！共处理 {total_processed} 篇文章")
        self.logger.info("=" * 60)
        
        return total_processed


# ============================================
# 主函数
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description='AI/VC前沿观察 - 内容抓取与翻译脚本 (并行版本)'
    )
    parser.add_argument(
        '--source', 
        type=str, 
        help='只处理指定的源（源名称）'
    )
    parser.add_argument(
        '--max-per-source', 
        type=int, 
        default=5,
        help='每个源最多处理的文章数（默认5）'
    )
    parser.add_argument(
        '--sources', 
        type=str,
        help='指定sources.yaml的路径'
    )
    parser.add_argument(
        '--backfill',
        action='store_true',
        help='回填模式：处理历史文章'
    )
    parser.add_argument(
        '--since',
        type=str,
        help='只处理指定日期之后的文章（格式：YYYY-MM-DD）'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=3,
        help='并行处理的worker数量（默认3）'
    )
    
    args = parser.parse_args()
    
    # 1. 探测项目根目录
    if args.sources:
        sources_path = Path(args.sources)
        project_root = sources_path.parent.parent
    else:
        project_root = find_project_root()
        sources_path = project_root / "data" / "sources.yaml"
    
    if not sources_path.exists():
        print(f"错误: 找不到配置文件 {sources_path}")
        print("请使用 --sources 参数指定路径")
        sys.exit(1)
    
    # 2. 设置目录
    project_root, content_dir, data_dir, logs_dir = setup_directories(project_root)
    
    # 3. 设置日志
    logger = setup_logging(logs_dir)
    logger.info(f"项目根目录: {project_root}")
    logger.info(f"配置文件: {sources_path}")
    
    # 4. 加载配置
    config = Config(sources_path)
    
    # 5. 初始化状态管理器
    state = URLStateManager(data_dir)
    
    # 6. 解析日期参数
    since_date = None
    if args.since:
        try:
            since_date = datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            logger.error(f"无效的日期格式: {args.since}")
            sys.exit(1)
    elif args.backfill:
        since_date = datetime.now() - timedelta(days=365)
    
    # 7. 运行流水线
    pipeline = Pipeline(
        config, 
        state, 
        content_dir, 
        logger,
        max_workers=args.workers
    )
    
    try:
        total = pipeline.run(
            source_filter=args.source,
            max_per_source=args.max_per_source,
            since_date=since_date
        )
        sys.exit(0 if total >= 0 else 1)
    except KeyboardInterrupt:
        logger.info("用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()