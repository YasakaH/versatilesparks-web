"""
Send Round 2 challenge to ChatGPT.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """You killed your own top 3. Good. Now here's Round 2:

My actual advantage: I have FreeLLMAPI with 62 free AI models running locally. Zero API costs. Every other seller passes on OpenAI/Anthropic bills. I don't.

What product can I build that ONLY I can build because of free AI infra?

Here's my proposal: "AI Trade Journal" that auto-analyzes trades using FreeLLMAPI — no API key needed, no subscription.

But I have questions:
1. Who exactly buys a Trade Journal? A retail trader with 10 trades or a professional with 1000?
2. How do they FIND it? (Gumroad search doesn't work for this)
3. Can I build a MINIMUM version in 3 days that someone would pay $19 for?
4. Or is this another "cool tech, no market" idea?

Be honest. Challenge me back.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=20000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill('')
                await ta.fill(MSG)
                await asyncio.sleep(2)
                btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
                await btn.click()
                print('Round 2 sent')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return msgs[msgs.length - 1]?.innerText || '';
                        }""")
                        print(f'\n=== ROUND 2 ({len(text)} chars) ===')
                        print(text[:1500])
                        break
                    if i % 12 == 0:
                        print(f'  Wait ({i*5}s)')
                break

asyncio.run(main())
