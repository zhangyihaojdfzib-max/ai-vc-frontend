#!/usr/bin/env python3
"""
YC Library Backfill Script - Playwright 高并发版本
使用无头浏览器抓取 JS 渲染的页面

特性：
- Playwright 处理 JS 渲染
- 多浏览器实例并行（默认 4 个）
- 自动过滤视频/播客页面
- 智能内容提取

使用方法:
    python scripts/backfill_yc_playwright.py --max 10 --workers 4   # 测试
    python scripts/backfill_yc_playwright.py --max 100 --workers 6  # 100篇
    python scripts/backfill_yc_playwright.py --workers 4            # 全部
"""

import os
import sys
import json
import time
import hashlib
import argparse
import requests
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import yaml
from openai import OpenAI
from playwright.sync_api import sync_playwright, Browser, Page

# ============================================
# 配置
# ============================================

SITEMAP_URL = "https://www.ycombinator.com/library/sitemap.xml"
SOURCE_NAME = "Y Combinator"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
DEFAULT_WORKERS = 4  # Playwright 并发数（每个需要一个浏览器实例）
TRANSLATION_MODEL = "deepseek-chat"
MIN_CONTENT_LENGTH = 500  # 最小内容长度，过滤视频页面

# 术语表
GLOSSARY = {
    'LLM': 'LLM（大语言模型）',
    'GPT': 'GPT',
    'Transformer': 'Transformer',
    'Fine-tuning': '微调',
    'Prompt': '提示词',
    'RAG': 'RAG（检索增强生成）',
    'Agent': 'Agent（智能体）',
    'Product-Market Fit': '产品市场契合',
    'PMF': 'PMF（产品市场契合）',
    'Runway': '现金跑道',
    'Burn Rate': '烧钱速度',
    'Series A': 'A轮',
    'Series B': 'B轮',
    'Seed Round': '种子轮',
    'MVP': 'MVP（最小可行产品）',
    'YC': 'YC（Y Combinator）',
    'Y Combinator': 'Y Combinator',
    'Startup': '创业公司',
    'Founder': '创始人',
    'Co-founder': '联合创始人',
    'Pitch': '路演/推介',
    'Pivot': '转型',
    'Traction': '增长势头',
    'Valuation': '估值',
    'SAFE': 'SAFE（未来股权简单协议）',
    'Equity': '股权',
    'Dilution': '稀释',
}

# ============================================
# 路径设置
# ============================================

def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for _ in range(5):
        if (current / "content" / "posts").exists():
            return current
        if (current / "package.json").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent

PROJECT_ROOT = find_project_root()
CONTENT_DIR = PROJECT_ROOT / "content" / "posts"
DATA_DIR = PROJECT_ROOT / "data"

# ============================================
# 线程安全的 URL 状态管理
# ============================================

class URLState:
    def __init__(self):
        self.processed_file = DATA_DIR / "processed_urls.json"
        self.processed = set()
        self._lock = threading.Lock()
        self._load()
    
    def _load(self):
        if self.processed_file.exists():
            with open(self.processed_file, 'r') as f:
                self.processed = set(json.load(f))
    
    def _save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed), f, indent=2)
    
    def is_processed(self, url: str) -> bool:
        with self._lock:
            return url in self.processed
    
    def mark_processed(self, url: str):
        with self._lock:
            self.processed.add(url)
            self._save()

# ============================================
# 进度计数器
# ============================================

class ProgressCounter:
    def __init__(self, total: int):
        self.total = total
        self.completed = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0  # 跳过的视频页面
        self._lock = threading.Lock()
        self.start_time = time.time()
    
    def increment(self, status: str = 'success'):
        with self._lock:
            self.completed += 1
            if status == 'success':
                self.success += 1
            elif status == 'skipped':
                self.skipped += 1
            else:
                self.failed += 1
    
    def get_stats(self) -> str:
        with self._lock:
            elapsed = time.time() - self.start_time
            rate = self.completed / elapsed * 60 if elapsed > 0 else 0
            remaining = (self.total - self.completed) / rate if rate > 0 else 0
            return f"[{self.completed}/{self.total}] ✅{self.success} ⏭️{self.skipped} ❌{self.failed} | {rate:.1f}/min | ETA: {remaining:.0f}min"

# ============================================
# Sitemap 获取
# ============================================

def fetch_sitemap_urls() -> List[str]:
    """从 sitemap 获取所有文章 URL"""
    print(f"📡 获取 sitemap: {SITEMAP_URL}")
    
    response = requests.get(SITEMAP_URL, headers={'User-Agent': USER_AGENT}, timeout=30)
    response.raise_for_status()
    
    root = ElementTree.fromstring(response.content)
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for url_elem in root.findall('.//sm:url', ns):
        loc = url_elem.find('sm:loc', ns)
        if loc is not None and loc.text:
            url = loc.text.strip()
            # 只要文章页面
            if '/library/' in url and '?' not in url and url.count('/') == 4:
                urls.append(url)
    
    print(f"✅ 找到 {len(urls)} 个页面")
    return urls

# ============================================
# Playwright 内容抓取
# ============================================

# 浏览器实例池
_browser_pool = {}
_browser_lock = threading.Lock()
_playwright_instance = None

def get_browser(worker_id: int) -> Browser:
    """获取或创建浏览器实例"""
    global _playwright_instance
    
    with _browser_lock:
        if _playwright_instance is None:
            _playwright_instance = sync_playwright().start()
        
        if worker_id not in _browser_pool:
            _browser_pool[worker_id] = _playwright_instance.chromium.launch(
                headless=True,
                args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
            )
    
    return _browser_pool[worker_id]

def cleanup_browsers():
    """清理所有浏览器实例"""
    global _playwright_instance
    
    with _browser_lock:
        for browser in _browser_pool.values():
            try:
                browser.close()
            except:
                pass
        _browser_pool.clear()
        
        if _playwright_instance:
            try:
                _playwright_instance.stop()
            except:
                pass
            _playwright_instance = None

def fetch_article_with_playwright(url: str, worker_id: int) -> Optional[Dict]:
    """使用 Playwright 获取文章内容"""
    try:
        browser = get_browser(worker_id)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(1500)  # 等待 JS 渲染
            
            # 获取标题
            title = ""
            try:
                title_elem = page.query_selector('h1')
                if title_elem:
                    title = title_elem.inner_text().strip()
            except:
                pass
            
            # 获取主要内容区域
            content = ""
            
            # 尝试多种选择器
            selectors = [
                'article',
                'main',
                '.prose',
                '.content',
                '[class*="article"]',
                '[class*="content"]',
            ]
            
            for selector in selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem:
                        text = elem.inner_text()
                        if len(text) > len(content):
                            content = text
                except:
                    continue
            
            # 如果特定选择器没找到，用 body
            if len(content) < MIN_CONTENT_LENGTH:
                content = page.inner_text('body')
            
            # 清理内容
            content = clean_content(content)
            
            # 检查是否是视频页面（内容太短）
            if len(content) < MIN_CONTENT_LENGTH:
                return None
            
            return {
                'url': url,
                'content': content,
                'title': title,
                'author': 'Y Combinator',
                'date': None,
            }
            
        finally:
            page.close()
            
    except Exception as e:
        return None

def clean_content(text: str) -> str:
    """清理页面内容"""
    # 移除导航、页脚等
    lines = text.split('\n')
    
    # 过滤掉太短的行和导航行
    skip_patterns = [
        'Log in', 'Apply', 'Table of Contents', 'Footer',
        'Y Combinator', 'Programs', 'Company', 'Resources',
        'Privacy Policy', 'Terms of Use', '© 2026',
        'Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Youtube',
        'Startup Directory', 'Startup Library', 'Hacker News',
        'Up next', 'Related', 'views', 'Over 1 year ago',
    ]
    
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 10:
            continue
        if any(pattern in line for pattern in skip_patterns):
            continue
        cleaned_lines.append(line)
    
    return '\n\n'.join(cleaned_lines)

# ============================================
# 翻译器
# ============================================

class Translator:
    def __init__(self):
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        )
        self._lock = threading.Lock()
    
    def _build_glossary_text(self) -> str:
        return "\n".join([f"- {en} → {zh}" for en, zh in GLOSSARY.items()])
    
    def translate(self, content: str) -> str:
        """翻译正文"""
        max_chunk = 8000
        if len(content) <= max_chunk:
            return self._translate_chunk(content)
        
        # 分段
        paragraphs = content.split('\n\n')
        chunks = []
        current = ""
        
        for para in paragraphs:
            if len(current) + len(para) + 2 <= max_chunk:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                current = para + "\n\n"
        if current.strip():
            chunks.append(current.strip())
        
        translated = []
        for chunk in chunks:
            translated.append(self._translate_chunk(chunk))
        
        return "\n\n".join(translated)
    
    def _translate_chunk(self, text: str) -> str:
        prompt = f"""请将以下英文内容翻译成中文。

翻译要求：
1. 准确传达原文含义，语言自然流畅
2. 保持原文的段落结构
3. 专业术语参考术语表：
{self._build_glossary_text()}
4. 代码块、URL保持原样
5. 只输出翻译结果

原文：
{text}

翻译："""
        
        try:
            response = self.client.chat.completions.create(
                model=TRANSLATION_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[翻译失败]\n\n{text}"
    
    def generate_metadata(self, content: str, original_title: str) -> Dict:
        categories = ['AI研究', 'AI产品', 'VC观点', '创业', '技术趋势', '产品', '增长', '融资', '团队管理', '未分类']
        
        prompt = f"""为以下文章生成元数据，JSON格式返回：

原标题：{original_title}
内容（前1500字）：{content[:1500]}

返回格式：
{{"title_zh": "中文标题", "summary_zh": "100字摘要", "category": "分类", "tags": ["标签1", "标签2"]}}

分类选项：{', '.join(categories)}
只返回JSON。"""
        
        try:
            response = self.client.chat.completions.create(
                model=TRANSLATION_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            
            result = response.choices[0].message.content.strip()
            if '```' in result:
                result = re.search(r'\{.*\}', result, re.DOTALL).group()
            
            return json.loads(result)
        except:
            return {
                'title_zh': original_title,
                'summary_zh': content[:150] + '...',
                'category': '未分类',
                'tags': ['YC', '创业']
            }

# ============================================
# 文章生成
# ============================================

_file_lock = threading.Lock()

def generate_article(article: Dict, translated_content: str, metadata: Dict) -> Path:
    """生成 Markdown 文件"""
    with _file_lock:
        CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
    slug = f"{date_str}-ycombinator-{url_hash}"
    filepath = CONTENT_DIR / f"{slug}.md"
    
    front_matter = {
        'title': metadata.get('title_zh', article.get('title', '')),
        'title_original': article.get('title', ''),
        'date': date_str,
        'source': SOURCE_NAME,
        'source_url': article['url'],
        'author': article.get('author', ''),
        'summary': metadata.get('summary_zh', ''),
        'categories': [metadata.get('category', '未分类')],
        'tags': metadata.get('tags', []),
        'draft': False,
    }
    
    front_matter_yaml = yaml.safe_dump(front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    content = f"""---
{front_matter_yaml}---

{translated_content}

---

> 本文由AI自动翻译，原文链接：[{article.get('title', '原文')}]({article['url']})
"""
    
    with _file_lock:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return filepath

# ============================================
# Worker 函数
# ============================================

def process_single_article(args: Tuple[str, int, Translator, URLState, ProgressCounter]) -> Tuple[str, str, str]:
    """处理单篇文章"""
    url, worker_id, translator, state, progress = args
    
    if state.is_processed(url):
        return (url, 'skip', "已处理")
    
    try:
        # 1. 获取内容
        article = fetch_article_with_playwright(url, worker_id)
        if not article:
            progress.increment('skipped')
            return (url, 'skipped', "⏭️ 视频/播客页面，跳过")
        
        title = article.get('title', '')[:35]
        
        # 2. 翻译
        translated = translator.translate(article['content'])
        
        # 3. 元数据
        metadata = translator.generate_metadata(translated, article.get('title', ''))
        
        # 4. 生成文件
        filepath = generate_article(article, translated, metadata)
        
        # 5. 标记完成
        state.mark_processed(url)
        progress.increment('success')
        
        return (url, 'success', f"✅ {title}...")
    
    except Exception as e:
        progress.increment('failed')
        return (url, 'failed', f"❌ {str(e)[:40]}")

# ============================================
# 主函数
# ============================================

def main():
    parser = argparse.ArgumentParser(description='YC Library Backfill - Playwright版')
    parser.add_argument('--max', type=int, default=0, help='最多处理多少篇（0=全部）')
    parser.add_argument('--skip', type=int, default=0, help='跳过前N篇')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS, help=f'并发数（默认{DEFAULT_WORKERS}）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 YC Library Backfill - Playwright 版")
    print("=" * 60)
    print(f"📁 项目目录: {PROJECT_ROOT}")
    print(f"📁 内容目录: {CONTENT_DIR}")
    print(f"⚡ 并发数: {args.workers}")
    
    # 初始化
    state = URLState()
    translator = Translator()
    
    # 获取 URL 列表
    urls = fetch_sitemap_urls()
    
    # 过滤已处理的
    urls = [u for u in urls if not state.is_processed(u)]
    print(f"📊 待处理: {len(urls)} 篇")
    
    if args.skip > 0:
        urls = urls[args.skip:]
    if args.max > 0:
        urls = urls[:args.max]
    
    if not urls:
        print("✅ 没有需要处理的文章！")
        return
    
    print(f"🎯 本次处理: {len(urls)} 篇")
    print("=" * 60)
    
    progress = ProgressCounter(len(urls))
    
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            # 分配 worker_id
            tasks = [(url, i % args.workers, translator, state, progress) for i, url in enumerate(urls)]
            futures = {executor.submit(process_single_article, task): task[0] for task in tasks}
            
            for future in as_completed(futures):
                try:
                    _, status, msg = future.result()
                    print(f"{progress.get_stats()} | {msg}")
                except Exception as e:
                    print(f"{progress.get_stats()} | ❌ Error: {e}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    
    finally:
        print("\n🧹 清理浏览器...")
        cleanup_browsers()
    
    # 统计
    elapsed = time.time() - progress.start_time
    print("\n" + "=" * 60)
    print(f"🎉 完成！")
    print(f"   ✅ 成功翻译: {progress.success} 篇")
    print(f"   ⏭️ 跳过视频: {progress.skipped} 篇")
    print(f"   ❌ 失败: {progress.failed} 篇")
    print(f"   ⏱️ 耗时: {elapsed/60:.1f} 分钟")
    if progress.success > 0:
        print(f"   📈 速度: {progress.success / elapsed * 60:.1f} 篇/分钟")
    print("=" * 60)

if __name__ == "__main__":
    main()
