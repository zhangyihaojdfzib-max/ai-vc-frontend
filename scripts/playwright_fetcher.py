#!/usr/bin/env python3
"""
playwright_fetcher.py - Playwright-based content fetcher for anti-bot sites

Handles sites that require JavaScript rendering or have anti-bot measures:
- OpenAI Blog
- Meta AI Blog
- Sam Altman's Blog (Posthaven)
- First Round Review
- And other JS-heavy sites

Usage:
    from playwright_fetcher import PlaywrightFetcher

    fetcher = PlaywrightFetcher()
    html = fetcher.fetch_page("https://openai.com/blog/...")
    # Then use ContentExtractorV2 to extract content from HTML
"""

import time
import random
import logging
from typing import Optional, Dict, List
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class PlaywrightFetcher:
    """
    Playwright-based fetcher for JavaScript-rendered and anti-bot protected sites.

    Features:
    - JavaScript rendering
    - Human-like behavior simulation
    - Cookie/session management
    - Stealth mode to avoid detection
    """

    # Site-specific configurations
    SITE_CONFIGS = {
        'openai.com': {
            'wait_selector': 'article, .prose, [class*="blog"]',
            'wait_time': 3000,
            'scroll': True,
            'block_resources': ['image', 'media', 'font'],  # Speed up, images fetched separately
        },
        'ai.meta.com': {
            'wait_selector': '[class*="blog"], article, main',
            'wait_time': 5000,
            'scroll': True,
            'block_resources': [],
        },
        'blog.samaltman.com': {
            'wait_selector': '.post, article, .entry',
            'wait_time': 2000,
            'scroll': False,
            'block_resources': [],
        },
        'review.firstround.com': {
            'wait_selector': 'article, .post-content, main',
            'wait_time': 3000,
            'scroll': True,
            'block_resources': [],
        },
        'www.bvp.com': {
            'wait_selector': 'article, .content, main',
            'wait_time': 3000,
            'scroll': True,
            'block_resources': [],
        },
        '_default': {
            'wait_selector': 'article, main, .content',
            'wait_time': 3000,
            'scroll': True,
            'block_resources': [],
        }
    }

    # Common user agents for rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    ]

    def __init__(self, headless: bool = True, logger: logging.Logger = None):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is not installed. Run: pip install playwright && playwright install chromium"
            )

        self.headless = headless
        self.logger = logger or logging.getLogger(__name__)
        self._browser: Optional[Browser] = None
        self._playwright = None

    def __enter__(self):
        self._start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_browser()

    def _start_browser(self):
        """Start the browser instance"""
        if self._browser is not None:
            return

        self._playwright = sync_playwright().start()

        # Launch with stealth settings
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-size=1920,1080',
            ]
        )
        self.logger.info("Playwright browser started")

    def _stop_browser(self):
        """Stop the browser instance"""
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None
        self.logger.info("Playwright browser stopped")

    def _get_site_config(self, url: str) -> Dict:
        """Get site-specific configuration"""
        domain = urlparse(url).netloc

        for site, config in self.SITE_CONFIGS.items():
            if site in domain:
                return config

        return self.SITE_CONFIGS['_default']

    def _create_stealth_context(self):
        """Create a browser context with stealth settings"""
        user_agent = random.choice(self.USER_AGENTS)

        context = self._browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            # Mimic real browser
            java_script_enabled=True,
            has_touch=False,
            is_mobile=False,
            device_scale_factor=1,
        )

        # Add stealth scripts to avoid detection
        context.add_init_script("""
            // Override webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            // Override chrome property
            window.chrome = {
                runtime: {}
            };

            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)

        return context

    def _simulate_human_behavior(self, page: Page, config: Dict):
        """Simulate human-like browsing behavior"""
        # Random initial delay
        time.sleep(random.uniform(0.5, 1.5))

        # Scroll behavior if enabled
        if config.get('scroll', True):
            self._smooth_scroll(page)

        # Random mouse movements
        try:
            page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600)
            )
        except:
            pass

    def _smooth_scroll(self, page: Page):
        """Perform smooth scrolling to trigger lazy-loaded content"""
        try:
            # Get page height
            page_height = page.evaluate("document.body.scrollHeight")
            viewport_height = page.evaluate("window.innerHeight")

            # Scroll in increments
            current_position = 0
            scroll_step = viewport_height // 2

            while current_position < page_height:
                current_position += scroll_step
                page.evaluate(f"window.scrollTo(0, {current_position})")
                time.sleep(random.uniform(0.1, 0.3))

            # Scroll back to top
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(0.5)

        except Exception as e:
            self.logger.debug(f"Scroll error (non-fatal): {e}")

    def fetch_page(self, url: str, timeout: int = 30000) -> Optional[str]:
        """
        Fetch a page using Playwright and return the rendered HTML.

        Args:
            url: The URL to fetch
            timeout: Maximum time to wait for page load (ms)

        Returns:
            The rendered HTML content, or None if failed
        """
        if self._browser is None:
            self._start_browser()

        config = self._get_site_config(url)
        context = None
        page = None

        try:
            context = self._create_stealth_context()
            page = context.new_page()

            # Block unnecessary resources for speed (optional)
            if config.get('block_resources'):
                def handle_route(route):
                    if route.request.resource_type in config['block_resources']:
                        route.abort()
                    else:
                        route.continue_()
                page.route("**/*", handle_route)

            # Navigate to page
            self.logger.info(f"  [Playwright] Fetching: {url}")
            response = page.goto(url, wait_until='domcontentloaded', timeout=timeout)

            if response and response.status >= 400:
                self.logger.warning(f"  [Playwright] HTTP {response.status} for {url}")
                return None

            # Wait for content to load
            try:
                page.wait_for_selector(
                    config['wait_selector'],
                    timeout=config['wait_time']
                )
            except PlaywrightTimeout:
                self.logger.debug(f"  [Playwright] Selector timeout, continuing anyway")

            # Simulate human behavior
            self._simulate_human_behavior(page, config)

            # Wait for any lazy-loaded content
            time.sleep(1)

            # Get the fully rendered HTML
            html = page.content()

            self.logger.info(f"  [Playwright] Successfully fetched {len(html)} bytes")
            return html

        except PlaywrightTimeout:
            self.logger.error(f"  [Playwright] Timeout fetching {url}")
            return None
        except Exception as e:
            self.logger.error(f"  [Playwright] Error fetching {url}: {e}")
            return None
        finally:
            if page:
                page.close()
            if context:
                context.close()

    def fetch_multiple(self, urls: List[str], delay: float = 2.0) -> Dict[str, Optional[str]]:
        """
        Fetch multiple pages with delay between requests.

        Args:
            urls: List of URLs to fetch
            delay: Delay between requests (seconds)

        Returns:
            Dict mapping URL to HTML content (or None if failed)
        """
        results = {}

        for i, url in enumerate(urls):
            if i > 0:
                time.sleep(delay + random.uniform(0, 1))

            results[url] = self.fetch_page(url)

        return results


class PlaywrightContentFetcher:
    """
    High-level integration of Playwright with ContentExtractorV2.

    This class provides a drop-in replacement for requests-based fetching
    that can handle JavaScript-rendered and anti-bot protected sites.
    """

    def __init__(self, images_dir: Path, logger: logging.Logger = None):
        from content_extractor_v2 import ContentExtractorV2

        self.images_dir = images_dir
        self.logger = logger or logging.getLogger(__name__)
        self.extractor = ContentExtractorV2(images_dir)
        self._pw_fetcher = None

    def __enter__(self):
        self._pw_fetcher = PlaywrightFetcher(headless=True, logger=self.logger)
        self._pw_fetcher._start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pw_fetcher:
            self._pw_fetcher._stop_browser()

    def fetch_article(self, url: str) -> Optional[Dict]:
        """
        Fetch and extract article content using Playwright.

        Returns the same format as ContentFetcher.fetch_article_content()
        to ensure compatibility with the existing pipeline.
        """
        if self._pw_fetcher is None:
            self._pw_fetcher = PlaywrightFetcher(headless=True, logger=self.logger)
            self._pw_fetcher._start_browser()

        html = self._pw_fetcher.fetch_page(url)

        if not html:
            return None

        # Use existing content extractor
        result = self.extractor.extract(html, url)

        if not result['blocks']:
            self.logger.warning(f"  [Playwright] No content blocks extracted from {url}")
            return None

        text_blocks = [b for b in result['blocks'] if b['type'] == 'text']
        img_blocks = [b for b in result['blocks'] if b['type'] == 'image']
        self.logger.info(f"  [Playwright] Extracted: {len(text_blocks)} text blocks, {len(img_blocks)} images")

        content_md = self.extractor.blocks_to_markdown(result['blocks'])

        if len(content_md) < 200:
            self.logger.warning(f"  [Playwright] Content too short ({len(content_md)} chars)")
            return None

        return {
            'content': content_md,
            'title': result.get('title', ''),
            'author': '',
            'date': '',
            'blocks': result['blocks'],
        }


# Standalone test
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    test_urls = [
        "https://openai.com/index/introducing-operator/",
        "https://blog.samaltman.com/the-gentle-singularity",
    ]

    with PlaywrightFetcher(headless=True) as fetcher:
        for url in test_urls:
            print(f"\n{'='*60}")
            print(f"Testing: {url}")
            html = fetcher.fetch_page(url)
            if html:
                print(f"Got {len(html)} bytes of HTML")
                # Print first 500 chars
                print(html[:500])
            else:
                print("Failed to fetch")
