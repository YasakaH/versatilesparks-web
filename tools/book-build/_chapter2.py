"""
Ask for Chapter 2 recipes.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Chapter 1 complete (4 recipes built and tested). Now Chapter 2: Browser Control.

The frozen TOC shows Chapter 2 has 4 recipes. But Recipe 2 already covered tabs. So Chapter 2 should cover:
- Windows (opening/managing multiple windows vs tabs)
- Navigation (back, forward, refresh, history)
- Screenshots (full page, element, timed)
- What's the 4th? Page info (URL, title, source, cookies)?

Give me Recipes 5-8 with code for each. Keep them practical.

Challenge: How is "windows" different from "tabs" in nodriver? Do they use the same API? If they're the same concept, combine them and use the free slot for something else."""

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
                print('Ch2 sent')
                
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
                        print(f'\n=== CH2 ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
