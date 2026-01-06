import os
from pathlib import Path
from collections import defaultdict
import re

posts_dir = Path('content/posts')
posts = list(posts_dir.glob('*.md'))

print('=== 文章审计报告 ===')
print(f'文章总数: {len(posts)}')

# 检查重复
url_map = defaultdict(list)
categories = defaultdict(int)
sources = defaultdict(int)

for post in posts:
    content = post.read_text(encoding='utf-8')
    
    # source_url
    m = re.search(r'source_url:\s*["\']?([^"\'\n]+)', content)
    if m:
        url_map[m.group(1).strip()].append(post.name)
    
    # categories
    m = re.search(r'categories:\s*\n\s*-\s*(.+)', content)
    if m:
        categories[m.group(1).strip()] += 1
    
    # source
    m = re.search(r'source:\s*["\']?([^"\'\n]+)', content)
    if m:
        sources[m.group(1).strip()] += 1

print('\n--- 检查重复文章 ---')
duplicates = {k: v for k, v in url_map.items() if len(v) > 1}
print(f'重复的源URL数量: {len(duplicates)}')
for url, files in duplicates.items():
    print(f'  URL: {url}')
    for f in files:
        print(f'    - {f}')

print('\n--- 分类统计 ---')
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')

print('\n--- 信息源统计 ---')
for src, count in sorted(sources.items(), key=lambda x: -x[1]):
    print(f'  {src}: {count}')
