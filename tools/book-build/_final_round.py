"""
Final round - get definitive product decision.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

FINAL = """After all debate, I need ONE definitive answer:

What ONE product do I build THIS WEEK?

Constraints: zero audience, zero budget, can build in 3-5 days, should use my skills (Python, AI, nodriver).

Give me:
1. Exact product name (optimized for search)
2. Price
3. Where to list it
4. How first buyer finds it
5. Build plan (3 days max)
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                # Type keyboard shortcut for new paragraph
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=30000)
                await asyncio.sleep(2)
                await ta.click()
                await asyncio.sleep(1)
                await ta.press('Control+a')
                await asyncio.sleep(0.5)
                await ta.press('Delete')
                await asyncio.sleep(0.5)
                
                # Type slowly
                await ta.type(FINAL, delay=5)
                await asyncio.sleep(2)
                
                # Send
                await pg.keyboard.press('Control+Enter')
                print('Final sent')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(15)
                        text = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return m[m.length-1]?.innerText || '';
                        }""")
                        print(f'\n=== FINAL DECISION ===\n{text}')
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
