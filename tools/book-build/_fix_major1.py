"""
Pipeline: Major gaps batch.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """All 6 critical gaps fixed (retry taxonomy, selector strategy, login verification, pagination limit, stealth framing, stop-vs-retry). Now moving to major gaps.

## Major gaps to fix:

1. **Recipe 3** — Profile contents: explain WHAT is in a browser profile (cookies, local storage, extensions, cache) and what is NOT (Python variables, automation state)

2. **Recipe 7** — JS exception handling: show try/except around evaluate(), explain serialization limits

3. **Recipe 9** — Wait for text/attribute changes/spinner disappearance, not just elements

4. **Recipe 14** — Click failures: overlays, disabled buttons, animations, stale elements

5. **Recipe 18** — Unexpected modal recovery: try action → modal appears → dismiss → retry

6. **Recipe 20** — Cookie scope: domain, path, expiry, secure, HttpOnly basics

7. **Recipe 21** — Session validation: load cookies → verify still valid → login if not

8. **Recipe 23** — Broken tables: colspan, rowspan, missing cells, normalization

9. **Recipe 25** — Multiple completion strategies: height unchanged, item count unchanged, spinner gone

10. **Recipe 26** — Download lifecycle: temp file, rename, completion detection

11. **Recipe 30** — Project walkthrough: clone → install → config → run → create

Batch into groups of 3-4 to save time. Start with recipes 3, 7, 9."""

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
                print('Major batch 1 sent')
                
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
                        print(f'\n=== MAJOR ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
