"""
Ask ChatGPT for final 8 recipes (Chapters 6-8).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """22 recipes built and tested. Need the final 8 for v1.

## Chapter 6: Extraction & Downloads — 5 recipes
Recipes 23-27 covering:
- Extract tables from pages
- Pagination (clicking "Next" through multiple pages)
- Infinite scroll (loading dynamic content)
- File downloads (PDFs, CSVs)
- Something with images/media?

## Chapter 7: Stealth & Reliable Automation — 2 recipes
Recipes 28-29 covering:
- Browser profiles (fingerprinting, webdriver detection — what nodriver handles)
- Resilient automation (handling CAPTCHAs gracefully, rate limiting, retry on failure)

Challenge: "Stealth" is nodriver's biggest selling point. What EXACTLY do I teach? The fact that nodriver passes 31/31 detection tests is the VALUE, but explaining the internals is beyond scope. Should this chapter focus on "automation that doesn't trigger alarms" — proper timing, human-like behavior, session persistence?

## Chapter 8: Production Starter Kit — 1 recipe
Recipe 30: Complete reusable project scaffold. Give me the EXACT file list and contents.

For all recipes: code, problem statement, edge cases, what to explain."""

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
                print('Ch6-8 sent')
                
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
                        print(f'\n=== CH6-8 ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
