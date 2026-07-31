"""
Pipeline: Recipe 19 login verification.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Critical gaps #1 (retry) and #2 (selectors) fixed. Moving to #3.

## Gap 3: Recipe 19 — Login Verification
Current recipe shows login form patterns but doesn't verify success.

I need:
1. Code showing how to VERIFY login succeeded
2. Methods: check for logout button, user avatar, URL change, account menu
3. What to do when login fails (log, stop, don't retry with same credentials)
4. CAPTCHA detection pattern (detect, log, stop — don't bypass)

Give me updated Recipe 19 code."""

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
                        print(f'\n=== R19 FIX ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
