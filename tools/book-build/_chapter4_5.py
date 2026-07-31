"""
Ask for Chapter 4: Elements & Forms (6 recipes).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Recipes 1-12 are built and tested! Moving to Part II (Interaction).

Chapter 4: Elements & Forms — 6 recipes
Chapter 5: Authentication & Sessions — 4 recipes

## Chapter 4 needs 6 recipes covering:
- Finding elements (CSS selectors, text content)
- Clicking (buttons, links, overlays)
- Typing and filling forms
- File uploads
- Dropdowns (native + custom)
- Something else? Or combine these into 6?

## Chapter 5 needs 4 recipes covering:
- Login forms
- Cookies and sessions
- Persistent profiles (already done in Recipe 3!)
- Session reuse

**Challenge:** Recipe 3 already covered persistent profiles. Should Chapter 5 be reduced to 3 recipes? Or replace the duplicate with something else (like OAuth, 2FA handling, or multi-account management)?

Give me all 10 recipes (Ch4 + Ch5) with code. Challenge the duplicate."""

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
                print('Ch4+5 sent')
                
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
                        print(f'\n=== CH4+5 ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
