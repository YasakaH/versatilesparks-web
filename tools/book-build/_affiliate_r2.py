"""
Continue affiliate debate - send round 2 challenge.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

ROUND_2 = """Good analysis. I mostly agree. But let me challenge a few points:

1. **Instamojo referral** — You said ₹500/referral after KYC. That's decent but requires traffic. However, I'm ALREADY talking to businesses for automation services. Every potential client who needs payment processing is a referral opportunity. Should I add "BTW, I use Instamojo for my store — here's a referral link if you want to set up payments" to my service conversations? That's zero extra effort.

2. **You said "cold outreach is poor for affiliate products."** I agree for selling random Amazon products. But what about this: I make my FIRST outreach message about SOLVING a problem (automation), and only if they decline, I say "No problem, by the way I also have this prompt pack/affiliate link if useful." Is that viable as a fallback?

3. **Timeline** — You said no affiliate program pays within 7 days. What about digital products on Instamojo? If someone buys my ₹499 prompt pack, I get paid when? Is that faster than affiliate?

4. **The BIG challenge:** You recommended: Services first → trust → recommend tools → affiliate income. But HOW long does this take? I could spend months building a service business before I have enough client trust for meaningful affiliate income. Is there ANY affiliate shortcut that works within 2 weeks from zero?

Don't soften your answers. Be honest about what's realistically achievable.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                await pg.bring_to_front()
                
                # Send round 2
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=15000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill('')
                await ta.fill(ROUND_2)
                await asyncio.sleep(1)
                btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
                await btn.click()
                print('Round 2 sent')
                
                # Wait with better detection
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(8)
                        break
                    if i % 12 == 0:
                        print(f'  Waiting... ({i*5}s)')
                
                # Read response
                text = await pg.evaluate("""() => {
                    const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                    return msgs[msgs.length - 1]?.innerText || 'NONE';
                }""")
                print(f'\n=== ROUND 2 ({len(text)} chars) ===')
                print(text)
                break

asyncio.run(main())
