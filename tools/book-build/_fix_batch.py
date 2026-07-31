"""
Batch remaining critical gaps.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """3 critical gaps fixed (retry taxonomy, selector strategy, login verification). 3 remaining:

## Gap 4: Recipe 24 — Pagination Limit
Need: max_pages guard, detecting last page, handling disabled "Next" button

## Gap 5: Recipe 28 — Stealth Explanation
Need: Honest explanation about browser signals, what nodriver does differently (CDP vs WebDriver), no "31/31" claims

## Gap 6: Recipe 29 — Decision Tree
Need: When to STOP vs RETRY flowchart/logic, log failure before stopping

Give me all 3 fixes with updated code for each."""

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
                print('Batch sent')
                
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
                        print(f'\n=== BATCH ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
