import asyncio
from playwright.async_api import async_playwright

async def go():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        ctx = browser.contexts[0]
        # Navigate existing page or create new
        if ctx.pages:
            page = ctx.pages[0]
            await page.goto('https://chatgpt.com', timeout=30000)
        else:
            page = await ctx.new_page()
            await page.goto('https://chatgpt.com', timeout=30000)
        await asyncio.sleep(8)
        print(f'Title: {await page.title()} | URL: {page.url[:80]}')
        # Wait for login or page load
        content = await page.content()
        if 'login' in content.lower()[:500]:
            print('Login page detected')
        else:
            print('Page loaded')

asyncio.run(go())
