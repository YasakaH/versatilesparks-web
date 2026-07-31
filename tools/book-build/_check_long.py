"""Check for errors and wait for response."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[0]
        await asyncio.sleep(5)
        # Get the assistant message content
        msgs = await page.query_selector_all('[data-message-author-role]')
        if len(msgs) >= 2:
            assistant = msgs[1]
            text = await assistant.inner_text()
            print(f'Assistant text length: {len(text)}')
            if text:
                print(text[:500])
            else:
                # Check for stop button (still generating)
                stop_btn = await page.query_selector('[data-testid="stop-button"], button:has(svg)')
                send_btn = await page.query_selector('[data-testid="send-button"]')
                print(f'Stop btn: {stop_btn is not None}')
                print(f'Send btn: {send_btn is not None}')

asyncio.run(main())
