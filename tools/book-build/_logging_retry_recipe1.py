"""
Ask for logging.py + retry.py + then Recipe 1.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """browser.py and config.py written and frozen. Now I need the next two files, then Recipe 1.

## File: common/logging.py
Give me the exact code. Keep it under 30 lines.
- Expose a `logger` object that other modules import
- Should it log to stdout or a file?
- What level (DEBUG? INFO?)
- Any formatting?
- Challenge: should logging level be configurable without code changes?

## File: common/retry.py
- async retry decorator or function?
- exponential backoff? fixed delay?
- configurable max retries?
- should it log each retry?
- Challenge: is a decorator better than a wrapper function for a cookbook?

## After both files are frozen, give me Recipe 1 (Launch Your First Browser Session)
- Problem statement
- Code
- What to explain in the text

One message: logging.py code, retry.py code, then Recipe 1 code."""

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
                print('Sent')
                
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
                        print(f'\n=== RESPONSE ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
