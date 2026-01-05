#!/usr/bin/env python3
"""
YC Library Backfill Script
批量抓取 Y Combinator Library 的历史文章并翻译

使用方法:
    python scripts/backfill_yc.py --max 10       # 测试：只处理10篇
    python scripts/backfill_yc.py --max 100      # 处理100篇
    python scripts/backfill_yc.py                 # 处理全部
"""

import os
import sys
import json
import time
import hashlib
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
import trafilatura
from openai import OpenAI

# ============================================
# 配置
# ============================================

SITEMAP_URL = "https://www.ycombinator.com/library/sitemap.xml"
SOURCE_NAME = "Y Combinator"
USER_AGENT = "Mozilla/5.0 (compatible; AI-VC-Observer/1.0)"
MAX_WORKERS = 3  # 并行翻译数
TRANSLATION_MODEL = "deepseek-chat"

# 术语表
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
}

# ============================================
# 路径设置
# ============================================

def find_project_root() -> Path:
    """找到项目根目录"""
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
# URL 状态管理
# ============================================

class URLState:
    def __init__(self):
        self.processed_file = DATA_DIR / "processed_urls.json"
        self.processed = set()
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
        return url in self.processed
    
    def mark_processed(self, url: str):
        self.processed.add(url)
        self._save()

# ============================================
# 内容抓取
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
            # 只要文章页面，排除分类页和其他页面
            if '/library/' in url and '?' not in url and url.count('/') == 4:
                urls.append(url)
    
    print(f"✅ 找到 {len(urls)} 篇文章")
    return urls

def fetch_article_content(url: str) -> Optional[Dict]:
    """获取单篇文章内容"""
    try:
        response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
        response.raise_for_status()
        
        html = response.text
        
        # 使用 trafilatura 提取正文
        content = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            output_format='txt'
        )
        
        if not content or len(content) < 200:
            return None
        
        # 提取元数据
        metadata = trafilatura.extract_metadata(html)
        
        return {
            'url': url,
            'content': content,
            'title': metadata.title if metadata else '',
            'author': metadata.author if metadata else '',
            'date': metadata.date if metadata else '',
        }
    except Exception as e:
        print(f"  ❌ 获取失败 {url}: {e}")
        return None

# ============================================
# 翻译
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
    
    def _build_glossary_text(self) -> str:
        return "\n".join([f"- {en} → {zh}" for en, zh in GLOSSARY.items()])
    
    def translate(self, content: str) -> str:
        """翻译正文"""
        # 分段处理长文
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
        
        # 翻译每段
        translated = []
        for i, chunk in enumerate(chunks):
            print(f"    翻译第 {i+1}/{len(chunks)} 段...")
            translated.append(self._translate_chunk(chunk))
            if i < len(chunks) - 1:
                time.sleep(0.5)
        
        return "\n\n".join(translated)
    
    def _translate_chunk(self, text: str) -> str:
        prompt = f"""请将以下英文内容翻译成中文。

翻译要求：
1. 准确传达原文含义，语言自然流畅
2. 保持原文的段落结构
3. 专业术语参考以下术语表：
{self._build_glossary_text()}

4. 代码块、公式、URL保持原样不翻译
5. 不要添加任何解释或评论，只输出翻译结果

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
            print(f"    ⚠️ 翻译失败: {e}")
            return f"[翻译失败]\n\n{text}"
    
    def generate_metadata(self, content: str, original_title: str) -> Dict:
        """生成元数据"""
        categories = ['AI研究', 'AI产品', 'AI基础设施', 'VC观点', '创业', '技术趋势', '未分类']
        
        prompt = f"""请为以下文章生成元数据。

文章原标题：{original_title}

文章内容（前2000字）：
{content[:2000]}

请生成以下信息，以JSON格式返回：
{{
    "title_zh": "中文标题（简洁有力，不超过30字）",
    "summary_zh": "中文摘要（100-150字，概括文章核心观点）",
    "category": "分类（从以下选项中选一个：{', '.join(categories)}）",
    "tags": ["标签1", "标签2", "标签3"]（3-5个相关标签）
}}

只返回JSON，不要其他内容。"""
        
        try:
            response = self.client.chat.completions.create(
                model=TRANSLATION_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            
            result = response.choices[0].message.content.strip()
            # 清理 markdown
            if result.startswith('```'):
                result = result.split('\n', 1)[1]
            if result.endswith('```'):
                result = result.rsplit('\n', 1)[0]
            if result.startswith('json'):
                result = result[4:]
            
            return json.loads(result)
        except Exception as e:
            print(f"    ⚠️ 元数据生成失败: {e}")
            return {
                'title_zh': original_title,
                'summary_zh': content[:150] + '...',
                'category': '未分类',
                'tags': []
            }

# ============================================
# 文章生成
# ============================================

def generate_article(article: Dict, translated_content: str, metadata: Dict) -> Path:
    """生成 Markdown 文件"""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 日期
    date_str = datetime.now().strftime('%Y-%m-%d')
    if article.get('date'):
        try:
            date_str = article['date'][:10]
        except:
            pass
    
    # 文件名
    url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
    slug = f"{date_str}-ycombinator-{url_hash}"
    filepath = CONTENT_DIR / f"{slug}.md"
    
    # Front matter
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
    
    front_matter_yaml = yaml.safe_dump(
        front_matter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False
    )
    
    content = f"""---
{front_matter_yaml}---

{translated_content}

---

> 本文由AI自动翻译，原文链接：[{article.get('title', '原文')}]({article['url']})
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

# ============================================
# 处理单篇文章
# ============================================

def process_article(url: str, translator: Translator, state: URLState) -> bool:
    """处理单篇文章，返回是否成功"""
    if state.is_processed(url):
        return False
    
    # 1. 获取内容
    article = fetch_article_content(url)
    if not article:
        return False
    
    print(f"  📝 翻译: {article['title'][:50]}...")
    
    # 2. 翻译
    translated = translator.translate(article['content'])
    
    # 3. 生成元数据
    print(f"    生成元数据...")
    metadata = translator.generate_metadata(translated, article.get('title', ''))
    
    # 4. 生成文件
    filepath = generate_article(article, translated, metadata)
    print(f"  ✅ 完成: {filepath.name}")
    
    # 5. 标记完成
    state.mark_processed(url)
    
    return True

# ============================================
# 主函数
# ============================================

def main():
    parser = argparse.ArgumentParser(description='YC Library Backfill')
    parser.add_argument('--max', type=int, default=0, help='最多处理多少篇（0=全部）')
    parser.add_argument('--skip', type=int, default=0, help='跳过前N篇')
    args = parser.parse_args()
    
    print("=" * 60)
    print("YC Library Backfill")
    print("=" * 60)
    print(f"项目目录: {PROJECT_ROOT}")
    print(f"内容目录: {CONTENT_DIR}")
    
    # 初始化
    state = URLState()
    translator = Translator()
    
    # 获取 URL 列表
    urls = fetch_sitemap_urls()
    
    # 过滤已处理的
    urls = [u for u in urls if not state.is_processed(u)]
    print(f"📊 待处理: {len(urls)} 篇")
    
    # 应用限制
    if args.skip > 0:
        urls = urls[args.skip:]
    if args.max > 0:
        urls = urls[:args.max]
    
    print(f"🎯 本次处理: {len(urls)} 篇")
    print("=" * 60)
    
    # 处理
    success_count = 0
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] {url}")
        try:
            if process_article(url, translator, state):
                success_count += 1
            time.sleep(1)  # 避免请求过快
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断")
            break
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功处理 {success_count} 篇文章")
    print("=" * 60)

if __name__ == "__main__":
    main()
