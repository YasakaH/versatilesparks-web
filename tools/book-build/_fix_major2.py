"""
Pipeline: Major gaps batch 2 - click failures, modal recovery, cookie scope.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """3 major fixes done (profiles, JS errors, wait strategies). Next batch:

## Recipe 14 — Click failures
- Overlays intercepting clicks
- Disabled buttons
- Animations in progress
- Stale element references
- Scroll into view before clicking

## Recipe 18 — Unexpected modal recovery
- Modal appears mid-automation
- Dismiss → retry pattern
- Cookie banners blocking clicks

## Recipe 20 — Cookie scope explained
- Domain, path, expiry, secure, HttpOnly
- Why cookies don't always transfer between sites
- Cookie file save/restore pattern

Give updated code and decision tables for each."""

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
                print('Major batch 2 sent')
                
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
                        print(f'\n=== MAJOR2 ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
