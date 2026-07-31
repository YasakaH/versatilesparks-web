"""
Ask for Chapter 3: Production Foundations.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Recipes 1-8 built and tested (Chapters 1 and 2 complete). Now Chapter 3: Production Foundations.

The frozen TOC shows 4 recipes:
- Waits
- Retries
- Logging
- Configuration

But we already built retry.py and logging.py in common/. So these recipes should teach HOW to use them in practice.

Give me Recipes 9-12:

9. **Wait for Elements** — nodriver waits, explicit vs implicit, timing out
10. **Retry Failed Operations** — using our common/retry.py helper
11. **Use Logging Effectively** — using our common/logging.py, when to log what
12. **Manage Configuration** — using config.py, .env vs constants, environments

Challenge: Recipe 9 (waits) is fundamental. But nodriver's `page.wait_for()` might work differently than Selenium's WebDriverWait. Does nodriver even NEED explicit waits? Or is it async-first enough that waits are built-in? If nodriver auto-waits, what's left to teach?"""

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
                print('Ch3 sent')
                
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
                        print(f'\n=== CH3 ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
