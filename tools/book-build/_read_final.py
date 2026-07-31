"""Read final ChatGPT response."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                text = await pg.evaluate("""() => {
                    const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                    return m[m.length-1]?.innerText || '';
                }""")
                print(text)
                break

asyncio.run(main())
