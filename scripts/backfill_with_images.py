#!/usr/bin/env python3
"""
backfill_with_images.py - 带图片的文章回填脚本

特点：
1. 保留图片在原文中的位置
2. 优先处理新文章，没有则挖掘历史文章
3. 图片下载到本地
"""

import os
import sys
import json
import time
import hashlib
import yaml
import requests
import feedparser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from openai import OpenAI

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from content_extractor_v2 import ContentExtractorV2

class ImageBackfillPipeline:
    """带图片的回填流水线"""
    
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
        'RLHF': 'RLHF（人类反馈强化学习）',
        'Chain-of-Thought': '思维链',
        'Multimodal': '多模态',
        'Foundation Model': '基础模型',
        'API': 'API',
        'SaaS': 'SaaS',
        'ARR': 'ARR（年度经常性收入）',
        'PMF': 'PMF（产品市场契合）',
        'Product-Market Fit': '产品市场契合',
        'Moat': '护城河',
        'Network Effect': '网络效应',
        'Series A': 'A轮',
        'Seed Round': '种子轮',
        'Venture Capital': '风险投资',
        'VC': 'VC（风险投资）',
    }
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.content_dir = project_root / "content" / "posts"
        self.images_dir = project_root / "public" / "images" / "posts"
        self.data_dir = project_root / "data"
        
        # 创建目录
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载已处理的 URL
        self.processed_file = self.data_dir / "processed_urls.json"
        self.processed_urls = self._load_processed()
        
        # 初始化提取器
        self.extractor = ContentExtractorV2(self.images_dir)
        
        # 初始化翻译客户端
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        self.client = OpenAI(api_key=api_key, base_url='https://api.deepseek.com')
        
        # 加载源配置
        self.sources = self._load_sources()
    
    def _load_processed(self) -> set:
        if self.processed_file.exists():
            with open(self.processed_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _save_processed(self):
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed_urls), f, indent=2)
    
    def _load_sources(self) -> List[Dict]:
        sources_file = self.data_dir / "sources.yaml"
        if not sources_file.exists():
            print(f"警告: {sources_file} 不存在")
            return []
        
        with open(sources_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        sources = []
        for category in ['vc_funds', 'investors', 'ai_research', 'tech_blogs']:
            sources.extend(data.get(category, []))
        
        return [s for s in sources if s.get('enabled', True)]
    
    def fetch_articles_from_source(self, source: Dict, max_items: int = 20) -> List[Dict]:
        """从源获取文章列表（包括历史文章）"""
        feed_url = source.get('feed_url')
        if not feed_url:
            return []
        
        try:
            response = requests.get(feed_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; AI-VC-Bot/2.0)'
            })
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"  RSS 获取失败: {e}")
            return []
        
        articles = []
        for entry in feed.entries[:max_items * 2]:  # 获取更多以便筛选
            url = entry.get('link', '')
            if not url or url in self.processed_urls:
                continue
            
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            
            articles.append({
                'title': entry.get('title', ''),
                'url': url,
                'published': pub_date,
                'source': source
            })
        
        return articles[:max_items]
    
    def fetch_html(self, url: str) -> Optional[str]:
        """获取页面 HTML"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; AI-VC-Bot/2.0)'}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  获取页面失败: {e}")
            return None
    
    def translate_text(self, text: str) -> str:
        """翻译文本"""
        if not text or len(text.strip()) < 10:
            return text
        
        glossary_text = "\n".join([f"- {en} → {zh}" for en, zh in self.GLOSSARY.items()])
        
        prompt = f"""请将以下英文翻译成中文。

要求：
1. 准确传达原意，语言自然流畅
2. 专业术语参考术语表
3. 代码、URL、数字保持原样
4. 只输出翻译结果

术语表：
{glossary_text}

原文：
{text}

翻译："""
        
        try:
            response = self.client.chat.completions.create(
                model='deepseek-chat',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  翻译失败: {e}")
            return text
    
    def translate_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """翻译内容块（跳过图片和代码）"""
        translated = []
        
        for i, block in enumerate(blocks):
            if block['type'] == 'text':
                print(f"    翻译文本块 {i+1}/{len(blocks)}...")
                translated_content = self.translate_text(block['content'])
                translated.append({'type': 'text', 'content': translated_content})
                time.sleep(0.5)  # 避免 API 限流
                
            elif block['type'] == 'list':
                print(f"    翻译列表块 {i+1}/{len(blocks)}...")
                translated_items = []
                for item in block['items']:
                    translated_items.append(self.translate_text(item))
                    time.sleep(0.3)
                translated.append({'type': 'list', 'items': translated_items, 'ordered': block.get('ordered', False)})
                
            else:
                # 图片、代码原样保留
                translated.append(block)
        
        return translated
    
    def generate_metadata(self, title: str, content: str) -> Dict:
        """生成元数据"""
        categories = ['AI研究', 'AI产品', 'AI基础设施', 'VC观点', '创业', '技术趋势', '未分类']
        
        prompt = f"""请为以下文章生成元数据，返回 JSON 格式：

标题：{title}
内容（前1500字）：{content[:1500]}

返回格式：
{{
    "title_zh": "中文标题（不超过30字）",
    "summary_zh": "中文摘要（100-150字）",
    "category": "分类（从以下选择：{', '.join(categories)}）",
    "tags": ["标签1", "标签2", "标签3"]
}}

只返回 JSON："""
        
        try:
            response = self.client.chat.completions.create(
                model='deepseek-chat',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            result = response.choices[0].message.content.strip()
            if result.startswith('```'):
                result = result.split('\n', 1)[1].rsplit('\n', 1)[0]
            return json.loads(result)
        except Exception as e:
            print(f"  元数据生成失败: {e}")
            return {
                'title_zh': title,
                'summary_zh': '',
                'category': '未分类',
                'tags': []
            }
    
    def save_article(self, article: Dict, translated_blocks: List[Dict], metadata: Dict):
        """保存文章为 Markdown"""
        source = article['source']
        date_str = datetime.now().strftime('%Y-%m-%d')
        if article.get('published'):
            date_str = article['published'].strftime('%Y-%m-%d')
        
        url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
        slug = f"{date_str}-{source['name']}-{url_hash}"
        filepath = self.content_dir / f"{slug}.md"
        
        # 生成 Markdown 内容
        content_md = self.extractor.blocks_to_markdown(translated_blocks)
        
        # Front matter
        front_matter = {
            'title': metadata.get('title_zh', article['title']),
            'date': date_str,
            'source': source.get('display_name', source['name']),
            'source_url': article['url'],
            'summary': metadata.get('summary_zh', ''),
            'categories': [metadata.get('category', '未分类')],
            'tags': metadata.get('tags', []),
            'draft': False,
        }
        
        front_matter_yaml = yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False)
        
        full_content = f"""---
{front_matter_yaml}---

{content_md}

---

> 本文由 AI 自动翻译，原文：[{article['title']}]({article['url']})
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"  ✓ 保存: {filepath.name}")
        return filepath
    
    def process_article(self, article: Dict) -> bool:
        """处理单篇文章"""
        url = article['url']
        print(f"\n处理: {article['title'][:50]}...")
        print(f"  URL: {url}")
        
        # 获取 HTML
        html = self.fetch_html(url)
        if not html:
            return False
        
        # 提取内容（带图片）
        print("  提取内容...")
        result = self.extractor.extract(html, url)
        
        if not result['blocks']:
            print("  ✗ 内容提取失败")
            return False
        
        text_blocks = [b for b in result['blocks'] if b['type'] == 'text']
        image_blocks = [b for b in result['blocks'] if b['type'] == 'image']
        print(f"  提取到 {len(text_blocks)} 个文本块, {len(image_blocks)} 张图片")
        
        # 翻译
        print("  翻译中...")
        translated_blocks = self.translate_blocks(result['blocks'])
        
        # 生成元数据
        print("  生成元数据...")
        all_text = '\n'.join([b['content'] for b in translated_blocks if b['type'] == 'text'])
        metadata = self.generate_metadata(article['title'], all_text)
        
        # 保存
        self.save_article(article, translated_blocks, metadata)
        
        # 标记已处理
        self.processed_urls.add(url)
        self._save_processed()
        
        return True
    
    def run(self, target_count: int = 15, sources_to_use: List[str] = None):
        """运行回填"""
        print("=" * 60)
        print(f"开始回填（目标: {target_count} 篇带图片文章）")
        print("=" * 60)
        
        processed = 0
        
        for source in self.sources:
            if sources_to_use and source['name'] not in sources_to_use:
                continue
            
            if processed >= target_count:
                break
            
            print(f"\n{'='*40}")
            print(f"源: {source.get('display_name', source['name'])}")
            print(f"{'='*40}")
            
            # 获取文章（包括历史）
            articles = self.fetch_articles_from_source(source, max_items=10)
            
            if not articles:
                print("  没有未处理的文章")
                continue
            
            print(f"  找到 {len(articles)} 篇未处理文章")
            
            for article in articles:
                if processed >= target_count:
                    break
                
                try:
                    if self.process_article(article):
                        processed += 1
                        print(f"  进度: {processed}/{target_count}")
                    time.sleep(2)  # 礼貌延迟
                except Exception as e:
                    print(f"  ✗ 处理失败: {e}")
                    continue
        
        print("\n" + "=" * 60)
        print(f"完成！共处理 {processed} 篇文章")
        print("=" * 60)
        
        return processed


def main():
    import argparse
    parser = argparse.ArgumentParser(description='带图片的文章回填')
    parser.add_argument('--count', type=int, default=15, help='目标文章数')
    parser.add_argument('--sources', type=str, help='指定源（逗号分隔）')
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    pipeline = ImageBackfillPipeline(project_root)
    
    sources = args.sources.split(',') if args.sources else None
    pipeline.run(target_count=args.count, sources_to_use=sources)


if __name__ == '__main__':
    main()
