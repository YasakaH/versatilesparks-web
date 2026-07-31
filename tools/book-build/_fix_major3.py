"""
Pipeline: Major gaps batch 3 - session validation, broken tables, download lifecycle.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """2 batches done (6 major fixes applied). 5 remaining. Send these 3:

## Recipe 21 — Session validation pattern
- Load saved cookies
- Check if session is still valid (visit account page)
- If valid → continue; if expired → re-login
- Decision table

## Recipe 23 — Broken table handling
- colspan and rowspan
- Missing cells
- Data normalization
- Decision table

## Recipe 26 — Download lifecycle
- Chrome download temp file → rename
- Completion detection (poll for file)
- Handle duplicate filenames
- Decision table"""

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
                print('Batch 3 sent')
                
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
                        print(f'\n=== BATCH3 ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
