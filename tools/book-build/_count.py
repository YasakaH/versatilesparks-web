"""Check ChatGPT message count."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[0]
        msgs = await page.query_selector_all('[data-message-author-role]')
        print(len(msgs))

asyncio.run(main())
