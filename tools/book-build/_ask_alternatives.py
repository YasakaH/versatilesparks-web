"""
Send alternative ideas challenge to ChatGPT.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """OK the Affiliate Link Checker Pro at $49 sounds solid. But before I commit — give me 3 ALTERNATIVE ideas that are FAR from this one.

Not variations of affiliate tools. Not pricing tweaks. Completely different directions using the same skill set (Python, AI, nodriver, FreeLLMAPI) and the same constraints (zero audience, global digital products).

Examples of directions you haven't explored:
- Educational products (tutorials, blueprints)
- Something from the PAIN POINTS data we haven't discussed
- A completely different customer segment
- A tool that solves a problem NONE of my research covered
- A product that uses nodriver's undetected browser capability
- Something AI-related that uses FreeLLMAPI's free models
- An n8n workflow pack

For each alternative, give me:
1. Product name
2. What it does (1 sentence)
3. Price
4. How first buyer finds it
5. Why it's BETTER or WORSE than the Affiliate Link Checker Pro

I want to genuinely evaluate options before building."""

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
                print('Alternatives question sent')
                
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
                        print(f'\n=== ALTERNATIVES ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  Wait ({i*5}s)')
                break

asyncio.run(main())
