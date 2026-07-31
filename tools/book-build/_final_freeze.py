"""
Challenge technical decisions + freeze scope.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Good decisions. I challenge 3:

## Challenge 1: Python 3.11+
nodriver's own PyPI page says Python >=3.8. Restricting to 3.11+ cuts out users on Ubuntu 20.04 (default Python 3.8) and older systems. For a $29 PDF, is losing those buyers worth it? Can I support 3.9+ instead? The only real difference is typing syntax and match statements — both easy to avoid.

## Challenge 2: Async only
I agree in principle, BUT: most nodriver beginners come from Selenium (sync). If the first recipe throws async at them, they might bounce. What if Recipe 1-3 use a simple sync wrapper, THEN reveal async in Recipe 4 with "Why async matters"? That's a gentler onboarding curve.

## Challenge 3: Local HTML fixtures
Good for testing, but adds significant build time. For v1 with 30 recipes, I need to ship in 5 days. Can I skip fixtures in v1 and use comments like "# SELECTOR: may need updating" instead? Add fixtures in v2?

## Freeze request
After you respond to these 3 challenges, give me the FINAL frozen spec:
- Book title and subtitle
- Part structure (Part I-IV with chapter names)  
- Recipe count per chapter
- Python version
- Async/sync decision
- Project structure
- Stealth chapter approach
- v1 scope (30 recipes)
- Price: $29 PDF, $59 bundle
- What's explicitly OUT of scope for v1"""

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
                print('Challenges + freeze request sent')
                
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
                        print(f'\n=== FINAL FREEZE ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
