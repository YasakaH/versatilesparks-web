"""
Pipeline for critical gap fixes - start with Recipe 10 (Retry taxonomy).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Starting depth refinement. Let's fix the critical gaps one at a time.

## Gap 1: Recipe 10 — Retry Taxonomy
Current recipe shows retry() usage but doesn't teach WHAT to retry vs what NOT to.

I need:
1. A decision table: "Retry vs Don't Retry" with clear categories
2. Updated retry.py if needed (to support distinguishing error types)
3. Updated Recipe 10 code

The table should cover:
- Timeout → Retry
- Temporary network error → Retry
- Transient navigation failure → Retry
- Syntax error in selector → DON'T retry
- 404 / 5xx → DON'T retry (unless temporary)
- CAPTCHA detected → DON'T retry (log and stop)
- Invalid credentials → DON'T retry

Give me the exact updated code for retry.py (if changes needed) and Recipe 10."""

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
                        print(f'\n=== FIX ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
