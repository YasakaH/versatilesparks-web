"""
Send global digital products strategy question to ChatGPT.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

QUESTION = """I need to pivot strategy. We've been banned from LinkedIn and Fiverr due to aggressive automation from testing. Only Instamojo is working.

New reality: I need to sell DIGITAL PRODUCTS GLOBALLY. Not services. Not freelancing.

My assets:
- FreeLLMAPI (62 free AI models)
- Python, Playwright, automation skills
- Instamojo store (easyautomation.stores.instamojo.com) — India payments only
- 50 AI Prompts pack already created
- Zero audience, zero following, zero website
- Based in India

## I need your help debating these questions:

1. **Which digital products should I create?** My skills are AI, Python, automation. What digital products have global demand that I can build in <1 week each?
   - Notion templates? (huge market)
   - Ready-to-use Python automation scripts? 
   - Canva templates?
   - AI prompt packs for specific industries?
   - n8n/Zapier workflow templates?
   - Spreadsheet templates?
   - Course/ebook?

2. **Global platforms** — Instamojo is India-only. Which platform should I use for GLOBAL sales?
   - Gumroad (10% fee, global, Indian bank withdrawal)?
   - Payhip (5% fee)?
   - Etsy (huge built-in traffic)?
   - All of the above?

3. **Discovery WITHOUT social media** — LinkedIn is banned. No followers anywhere. How do people FIND my products?
   - Etsy marketplace search (built-in traffic)?
   - Gumroad Discover?
   - Product Hunt launches?
   - Google SEO? (takes months)
   - Affiliate programs (let others promote)?
   - What's the FASTEST path to a sale with zero audience?

4. **The hard question** — Is this viable at all? Can someone with zero audience, zero website, and banned from major platforms actually earn from digital products? Or is this hopeless?

5. **What's the ONE product** I should build first that has the best chance of a global sale within 7 days?

Challenge me. Don't sugarcoat. If this is a dead end, say so.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=15000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill('')
                await ta.fill(QUESTION)
                await asyncio.sleep(1.5)
                btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
                await btn.click()
                print('Sent global digital products question')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return msgs[msgs.length - 1]?.innerText || 'NONE';
                        }""")
                        print(f'\n=== CHATGPT ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  Wait... ({i*5}s)')
                break

asyncio.run(main())
