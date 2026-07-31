"""Wait for ChatGPT to finish generating."""
import asyncio, sys, time
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[0]
        max_wait = 300
        waited = 0
        while waited < max_wait:
            await asyncio.sleep(15)
            waited += 15
            msgs = await page.query_selector_all('[data-message-author-role]')
            stop = await page.query_selector('[data-testid=stop-button]')
            if not stop and len(msgs) >= 2:
                text = await msgs[1].inner_text()
                if text:
                    print(f'RESPONSE READY ({waited}s wait)')
                    print(text[:1000])
                    sys.exit(0)
            print(f'...still generating ({waited}s)')
        print('Timed out')

asyncio.run(main())
