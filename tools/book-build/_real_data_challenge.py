"""
Send real market data to ChatGPT - challenge previous assumptions.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I found REAL data that changes everything. Two discoveries:

## Discovery 1: $200+ products sell MORE units than cheap ones
From analysis of 152,362 active Gumroad products:
- $200+ software sells 19.2 units on average
- $1-49 software sells 5.4 units on average
- That's **3.6x MORE units at 4x the price**
- Median revenue climbs with price in 8 out of 8 categories
- The ONLY dead zone is $50-99 (psychological limbo)
- This means your $49 recommendation is WRONG. I should price at $97-199.

## Discovery 2: A real creator made $2,539/month with 50+ products
Only 8 out of 50+ products made money. Winners were:
- "Master Git in Minutes" — 105 sales, $734 — simple 27-page PDF
- "Production Engineering Bundle" — 8 sales at $79 = $445
- "The Backend Failure Playbook" — 24 sales, $311
Pattern: **Educational PDFs/bundles** of niche technical knowledge. NOT tools.

## Discovery 3: LinkedIn automation is saturated
40+ established tools from $7-99/month. Not defensible.

## So my NEW question
Given this real data:
1. The proven earners are **informational PDFs/bundles** ($10-79), NOT desktop tools
2. Higher prices ($100-199) sell better than $49
3. The "Automation Catalog" idea competes in saturated markets
4. Our REAL skill is Python/AI technical knowledge

What's the PROVEN earning path? Should I be writing **technical PDF guides** about Python automation, AI, or nodriver? That's what actually made money for that creator. Price them at $10-79, bundle them.

Or is there another proven-earning product type I'm missing?"""

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
                print('Sent new data')
                
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
                        print(f'\n=== RESPONSE ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
