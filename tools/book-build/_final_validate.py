"""
Challenge: validate the Technical Implementation Kit idea.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I like the Technical Implementation Kit concept but I need to challenge it:

1. **$97-199 price for a first product with no audience** — The data shows $200+ products sell 3.6x more UNITS, but those products have ratings, reviews, and algorithmic history. A brand-new product with zero history at $97 — will it convert? Or should I start at $49 to get first 10 sales + reviews, THEN raise to $97?

2. **"Undetected Browser Automation Kit"** — Who searches for this? The creator in my data succeeded because "Master Git in Minutes" matches an exact search. "Undetected Browser Automation Kit" doesn't match any common search phrase. Should I name it after a search term?

3. **Downloading vs SaaS concern** — A $97 one-time download seems high for a first-time unknown seller. Would a $29 PDF + $79 code bundle (two separate products) convert better?

4. **The real gap in my research** — I haven't found any products LIKE this that are PROVEN to sell. Got any real examples of "technical kit" products on Gumroad that are earning?

Give me the specific search-optimized name, the exact price ladder, and what a proven-earning example looks like."""

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
                print('Challenge sent')
                
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
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
