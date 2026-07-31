"""
Pipeline: Final major gaps - infinite scroll + project walkthrough.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Almost done with depth refinement. Last 2 major gaps:

## Recipe 25 — Multiple scroll completion strategies
Current recipe uses height unchanged. Need to add:
1. Height unchanged
2. Item count unchanged 
3. Loading spinner gone
4. Timeout safety

## Recipe 30 — Project walkthrough
Instead of just listing files, show:
1. Clone starter kit
2. pip install
3. Edit config.py
4. Run example recipe
5. Create new project from scaffold
6. Add selectors
7. Done in 5 minutes

Give code updates for both."""

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
                print('Final batch sent')
                
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
                        print(f'\n=== FINAL ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
