"""
Ask ChatGPT for config.py design.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """browser.py written and frozen. Now design config.py.

## Requirements for config.py
All cookbook defaults in one file. browser.py imports from it.

What should it contain?
- HEADLESS (default False? True?)
- USER_DATA_DIR (None by default? Or a fixed path?)
- BROWSER_LANGUAGE
- WINDOW_SIZE
- DOWNLOAD_DIR
- TIMEOUT (default seconds?)
- RETRY settings? Or does retry.py own those?

Key decisions:
1. Should config read from .env file or environment variables or just Python constants?
2. Should it support command-line overrides?
3. What defaults make sense for a production cookbook?
4. How do users customize for their setup?

After you design config.py, give me the code. Then I'll challenge it and freeze it."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=30000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill(MSG)
                await asyncio.sleep(1.5)
                await pg.keyboard.press('Control+Enter')
                print('config.py request sent')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return m[m.length-1]?.innerText || '';
                        }""")
                        print(f'\n=== CONFIG.PY ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
