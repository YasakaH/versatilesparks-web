"""Stop ChatGPT and regenerate with direct high-quality prompts."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[0]
        # Hit stop button
        stop = await page.query_selector('[data-testid=stop-button]')
        if stop:
            await stop.click()
            print('Stopped generation')
            await asyncio.sleep(2)
        # Send shorter test message
        input_area = await page.query_selector('#prompt-textarea')
        if input_area:
            await input_area.fill('Give me one SD3 prompt for a premium dark tech book cover image. Abstract geometric, dark navy, cyan amber lights, no text. Short and specific.')
            await asyncio.sleep(1)
            send = await page.query_selector('[data-testid=send-button], button:has([data-testid=send-button])')
            if send:
                await send.click()
            else:
                await input_area.press('Enter')
            print('Sent short test')

asyncio.run(main())
