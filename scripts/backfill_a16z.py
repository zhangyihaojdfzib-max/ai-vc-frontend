#!/usr/bin/env python3
"""
a16z 文章回填脚本 - 使用 Playwright 突破反爬虫
"""
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
import trafilatura
from openai import OpenAI

# 配置
CONTENT_DIR = Path("content/posts")
DATA_DIR = Path("data")
PROCESSED_FILE = DATA_DIR / "processed_urls.json"

def load_processed():
    if PROCESSED_FILE.exists():
        return set(json.loads(PROCESSED_FILE.read_text()))
    return set()

def save_processed(urls):
    PROCESSED_FILE.write_text(json.dumps(list(urls), ensure_ascii=False, indent=2))

def get_a16z_articles(max_articles=20):
    """获取 a16z 文章链接"""
    print("正在获取 a16z 文章列表...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://a16z.com/news-content/', timeout=30000)
        page.wait_for_timeout(3000)
        
        # 滚动加载更多
        for i in range(10):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(800)
        
        html = page.content()
        browser.close()
    
    # 提取文章链接
    articles = re.findall(r'href="(https://a16z\.com/[a-z0-9\-]+/)"', html)
    
    # 过滤有效文章
    valid = []
    seen = set()
    skip_patterns = ['news-content', 'portfolio', 'team', 'about', 'podcasts', 
                     'subscription', 'search', 'newsletter', 'connect', 'speedrun', 
                     'growth', 'clf', 'txo', 'perennial', 'ai', 'bio-health',
                     'consumer', 'enterprise', 'fintech', 'infra', 'american-dynamism']
    
    for url in articles:
        if url in seen:
            continue
        seen.add(url)
        
        # 获取路径部分
        path = url.replace('https://a16z.com/', '').rstrip('/')
        
        # 跳过非文章页面
        if path in skip_patterns:
            continue
        
        # 文章路径通常有连字符且较长
        if '-' in path and len(path) > 15:
            valid.append(url)
            print(f"  找到: {path}")
            if len(valid) >= max_articles:
                break
    
    print(f"共找到 {len(valid)} 篇文章")
    return valid

def fetch_article_content(url):
    """用 Playwright 获取文章内容"""
    print(f"  获取: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(2000)
        
        # 获取标题
        title = ""
        try:
            title_el = page.query_selector('h1')
            if title_el:
                title = title_el.inner_text()
        except:
            pass
        
        html = page.content()
        browser.close()
    
    # 用 trafilatura 提取正文
    content = trafilatura.extract(html, include_comments=False, include_tables=True)
    
    if not content or len(content) < 500:
        print(f"  内容太短 ({len(content) if content else 0} 字符)，跳过")
        return None
    
    return {
        'title': title,
        'content': content,
        'url': url
    }

def translate_article(content, title):
    """翻译文章"""
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url='https://api.deepseek.com'
    )
    
    print(f"  翻译中...")
    
    # 分段翻译
    max_chunk = 6000
    chunks = []
    if len(content) > max_chunk:
        paragraphs = content.split('\n\n')
        current = ""
        for p in paragraphs:
            if len(current) + len(p) < max_chunk:
                current += p + "\n\n"
            else:
                if current:
                    chunks.append(current)
                current = p + "\n\n"
        if current:
            chunks.append(current)
    else:
        chunks = [content]
    
    translated_chunks = []
    for chunk in chunks:
        prompt = f"""请将以下英文内容翻译成中文，保持原文的段落结构，专业术语可保留英文：

{chunk}

翻译："""
        
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000,
        )
        translated_chunks.append(response.choices[0].message.content.strip())
    
    translated_content = "\n\n".join(translated_chunks)
    
    # 生成元数据
    meta_prompt = f"""为以下文章生成中文标题、摘要和分类，以JSON格式返回：
{{
    "title_zh": "中文标题（不超过30字）",
    "summary_zh": "中文摘要（100-150字）",
    "category": "从以下选择：AI研究、AI产品、AI基础设施、VC观点、创业、技术趋势",
    "tags": ["标签1", "标签2", "标签3"]
}}

原标题：{title}
内容：{translated_content[:2000]}

只返回JSON："""

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{"role": "user", "content": meta_prompt}],
        temperature=0.3,
        max_tokens=500,
    )
    
    try:
        meta_text = response.choices[0].message.content.strip()
        if meta_text.startswith('```'):
            meta_text = meta_text.split('\n', 1)[1].rsplit('\n', 1)[0]
        metadata = json.loads(meta_text)
    except:
        metadata = {
            'title_zh': title,
            'summary_zh': translated_content[:150],
            'category': 'VC观点',
            'tags': ['a16z']
        }
    
    return {
        'content_zh': translated_content,
        **metadata
    }

def save_article(article, translated, source_name="Andreessen Horowitz (a16z)"):
    """保存文章为 Markdown"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
    slug = f"{date_str}-a16z-{url_hash}"
    
    filepath = CONTENT_DIR / f"{slug}.md"
    
    content = f"""---
title: "{translated.get('title_zh', article['title'])}"
title_original: "{article['title']}"
date: {date_str}
source: "{source_name}"
source_url: "{article['url']}"
summary: "{translated.get('summary_zh', '')}"
categories:
  - {translated.get('category', 'VC观点')}
tags: {json.dumps(translated.get('tags', ['a16z']), ensure_ascii=False)}
draft: false
---

{translated.get('content_zh', '')}

---

> 本文由AI自动翻译，原文链接：[{article['title']}]({article['url']})
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"  ✓ 保存: {filepath.name}")
    return filepath

def main():
    print("=" * 50)
    print("a16z 文章回填脚本")
    print("=" * 50)
    
    # 加载已处理的 URL
    processed = load_processed()
    print(f"已处理 URL: {len(processed)}")
    
    # 获取文章列表
    articles = get_a16z_articles(max_articles=30)
    
    # 过滤已处理的
    new_articles = [a for a in articles if a not in processed]
    print(f"新文章: {len(new_articles)}")
    
    if not new_articles:
        print("没有新文章")
        return
    
    # 处理每篇文章
    success = 0
    for i, url in enumerate(new_articles[:15]):
        print(f"\n[{i+1}/{min(15, len(new_articles))}] {url}")
        
        try:
            # 获取内容
            article = fetch_article_content(url)
            if not article:
                continue
            
            # 翻译
            translated = translate_article(article['content'], article['title'])
            
            # 保存
            save_article(article, translated)
            
            # 标记已处理
            processed.add(url)
            save_processed(processed)
            
            success += 1
            
        except Exception as e:
            print(f"  错误: {e}")
            continue
    
    print(f"\n完成！成功处理 {success} 篇文章")

if __name__ == "__main__":
    main()
