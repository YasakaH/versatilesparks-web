"""Check ChatGPT message count."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url and 'c/' in pg.url:
                c = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'count={c}')
                return

asyncio.run(main())
