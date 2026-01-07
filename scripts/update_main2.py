# 读取文件
with open('scripts/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要修改的位置
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. 修改 ContentFetcher.__init__ - 添加 extractor
    if 'class ContentFetcher:' in line:
        new_lines.append(line)
        i += 1
        # 添加 __init__ 直到遇到下一个 def
        while i < len(lines) and 'def fetch_from_source' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        # 在 fetch_from_source 之前插入 extractor 初始化
        new_lines.append('        # 图片提取器\n')
        new_lines.append('        images_dir = state_manager.processed_file.parent.parent / "public" / "images" / "posts"\n')
        new_lines.append('        images_dir.mkdir(parents=True, exist_ok=True)\n')
        new_lines.append('        self.extractor = ContentExtractorV2(images_dir)\n')
        new_lines.append('\n')
        new_lines.append(lines[i])  # def fetch_from_source
        i += 1
        continue
    
    # 2. 替换 fetch_article_content 方法
    if 'def fetch_article_content(self, url: str)' in line:
        new_lines.append('    def fetch_article_content(self, url: str) -> Optional[Dict]:\n')
        new_lines.append('        """使用 ContentExtractorV2 提取内容（带图片）"""\n')
        new_lines.append('        try:\n')
        new_lines.append("            headers = {'User-Agent': self.config.user_agent}\n")
        new_lines.append('            response = requests.get(url, headers=headers, timeout=30)\n')
        new_lines.append('            response.raise_for_status()\n')
        new_lines.append('\n')
        new_lines.append('            html = response.text\n')
        new_lines.append('            result = self.extractor.extract(html, url)\n')
        new_lines.append('\n')
        new_lines.append("            if not result['blocks']:\n")
        new_lines.append('                return None\n')
        new_lines.append('\n')
        new_lines.append("            text_blocks = [b for b in result['blocks'] if b['type'] == 'text']\n")
        new_lines.append("            img_blocks = [b for b in result['blocks'] if b['type'] == 'image']\n")
        new_lines.append('            self.logger.info(f"    提取: {len(text_blocks)} 文本块, {len(img_blocks)} 图片")\n')
        new_lines.append('\n')
        new_lines.append("            content_md = self.extractor.blocks_to_markdown(result['blocks'])\n")
        new_lines.append('\n')
        new_lines.append('            if len(content_md) < 200:\n')
        new_lines.append('                return None\n')
        new_lines.append('\n')
        new_lines.append('            return {\n')
        new_lines.append("                'content': content_md,\n")
        new_lines.append("                'title': result.get('title', ''),\n")
        new_lines.append("                'author': '',\n")
        new_lines.append("                'date': '',\n")
        new_lines.append("                'blocks': result['blocks'],\n")
        new_lines.append('            }\n')
        new_lines.append('\n')
        new_lines.append('        except Exception as e:\n')
        new_lines.append('            self.logger.error(f"内容提取失败: {e}")\n')
        new_lines.append('            return None\n')
        
        # 跳过原来的方法
        i += 1
        while i < len(lines) and not (lines[i].startswith('# ') or lines[i].startswith('class ')):
            if lines[i].strip() == '' and i+1 < len(lines) and (lines[i+1].startswith('# ') or lines[i+1].startswith('class ')):
                break
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

with open('scripts/main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('main.py 修改完成！')
