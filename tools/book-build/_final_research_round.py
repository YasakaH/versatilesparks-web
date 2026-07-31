"""
Final debate round - send all market research data.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I did the research. Here's what the ACTUAL data says:

## What ACTUALLY sells on Gumroad in our space

**Tools/Software Kits: DID NOT SELL**
One creator had "Selenium Automation Kit" — 0 sales. Another "Test Data Generator" — 1 sale. Pure tools from unknown creators don't convert.

**Educational PDFs/Focused Guides: DID SELL**
- "Master Git in Minutes" (27-page PDF, $10) — 105 sales, $734 revenue
- Production checklists (free) — 400+ downloads as lead magnets
- Backend Failure Playbook — 24 sales, $311

**Amazon has proven books in this space:**
- "Python Web Scraping Cookbook" (O'Reilly) — 90+ recipes, established format
- "Web Scraping with Python" — consistent seller

**nodriver is a HOT topic but has zero Gumroad products:**
- It passed 31/31 anti-detection tests in benchmarks
- Multiple articles being written about it
- But NOBODY is selling a nodriver guide or cookbook on Gumroad

## The market gap I found
There are ZERO products on Gumroad for nodriver. The term has growing search interest (Instagram reels, Medium articles, GitHub discussions). The anti-detect browser benchmark article explicitly names nodriver as the only tool passing all tests.

## My proposed product
**"Python Browser Automation Cookbook: 50 Recipes with nodriver"**

- $19-29 PDF (knowledge only)
- $49 bundle with code + templates
- Solves: People searching for "browser automation python", "nodriver guide", "undetected browser automation"
- Competition: ZERO nodriver-specific products on Gumroad
- Proven format: Cookbooks sell (Amazon has multiple in this category)
- Build time: 5-7 days (I already know nodriver)

Is this the one? Or is the gap misleading?"""

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
                print('Final research sent')
                
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
                        print(f'\n=== FINAL VERDICT ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
