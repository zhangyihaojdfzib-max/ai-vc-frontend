from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://a16z.com/news-content/', timeout=30000)
    page.wait_for_timeout(3000)
    
    # 滚动加载更多内容
    for i in range(5):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1000)
    
    # 打印页面 HTML 片段，找文章结构
    html = page.content()
    
    # 查找包含文章的部分
    import re
    articles = re.findall(r'href="(https://a16z\.com/[^"]+)"', html)
    
    seen = set()
    for url in articles:
        if url not in seen and '/news-content/' not in url and len(url) > 25:
            seen.add(url)
            print(url)
            if len(seen) > 20:
                break
    
    browser.close()
