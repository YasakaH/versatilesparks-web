"""
Pipeline: Recipe 13 selector strategy.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Critical gap #1 (Retry taxonomy) fixed. Moving to #2.

## Gap 2: Recipe 13 — Selector Strategy
Current recipe shows `page.find()` with CSS selectors but doesn't teach WHAT makes a good selector.

I need:
1. A selector priority hierarchy (data-testid → id → name → class → CSS → XPath)
2. Updated Recipe 13 code that uses data-* attributes
3. A "Which Selector?" decision table

The updated code should show:
- Finding by data-testid (highest priority)
- Finding by text content
- Finding by CSS when necessary
- What NOT to do (brittle selectors based on position)

Give me the exact Recipe 13 code."""

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
                        print(f'\n=== R13 FIX ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
