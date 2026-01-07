import re

# 读取文件
with open('scripts/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换 import trafilatura
content = content.replace(
    'import trafilatura',
    'from content_extractor_v2 import ContentExtractorV2'
)

# 2. 在 ContentFetcher 类中添加 extractor 初始化
old_init = '''class ContentFetcher:
    def __init__(self, config: Config, state: URLStateManager, logger: logging.Logger):
        self.config = config
        self.state = state
        self.logger = logger
        self.rss_discovery = RSSDiscovery(
            config.user_agent,
            cache_file=state.processed_file.parent / "rss_cache.json"
        )'''

new_init = '''class ContentFetcher:
    def __init__(self, config: Config, state: URLStateManager, logger: logging.Logger, images_dir: Path = None):
        self.config = config
        self.state = state
        self.logger = logger
        self.rss_discovery = RSSDiscovery(
            config.user_agent,
            cache_file=state.processed_file.parent / "rss_cache.json"
        )
        # 图片提取器
        if images_dir is None:
            images_dir = state.processed_file.parent.parent / "public" / "images" / "posts"
        images_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = ContentExtractorV2(images_dir)'''

content = content.replace(old_init, new_init)

# 3. 替换 fetch_article_content 方法
old_fetch = '''    def fetch_article_content(self, url: str) -> Optional[Dict]:
        try:
            headers = {'User-Agent': self.config.user_agent}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            downloaded = response.text
            result = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                include_images=False,
                output_format='txt'
            )

            if not result or len(result) < 200:
                return None

            metadata = trafilatura.extract_metadata(downloaded)

            return {
                'content': result,
                'title': metadata.title if metadata else '',
                'author': metadata.author if metadata else '',
                'date': metadata.date if metadata else '',
            }

        except Exception as e:
            return None'''

new_fetch = '''    def fetch_article_content(self, url: str) -> Optional[Dict]:
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
            return None'''

content = content.replace(old_fetch, new_fetch)

with open('scripts/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('main.py 已更新！')
