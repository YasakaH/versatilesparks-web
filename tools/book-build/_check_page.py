"""Check what's on the page."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[0]
        # Wait for response
        await asyncio.sleep(10)
        # Check for elements
        btns = await page.query_selector_all('button')
        print(f'Buttons: {len(btns)}')
        for b in btns:
            text = await b.inner_text()
            if text.strip():
                print(f'  Button: {text[:50]}')
        # Check messages
        msgs = await page.query_selector_all('[data-message-author-role]')
        print(f'Messages: {len(msgs)}')
        for m in msgs:
            role = await m.get_attribute('data-message-author-role')
            content = await m.inner_text()
            print(f'  [{role}]: {content[:80]}')

asyncio.run(main())
