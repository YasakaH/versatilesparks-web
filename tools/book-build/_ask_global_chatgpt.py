"""
Send global digital products question to existing ChatGPT thread.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

QUESTION = """I need to pivot strategy hard. LinkedIn and Fiverr accounts got banned due to aggressive automation testing. Only Instamojo is working.

New reality: I need to sell DIGITAL PRODUCTS GLOBALLY. Not services. Not freelancing.

## My actual assets right now:
- FreeLLMAPI (62 free AI models, local)
- Python + nodriver (undetected browser automation — just installed)
- Instamojo store (easyautomation.stores.instamojo.com) — India payments only
- 50 AI Prompts pack already created
- Zero audience, zero following, zero website
- Based in India
- Can build almost anything technical in <1 week

## Questions I need debated:

1. **What digital products have global demand that match my skills?** I can build: AI tools, automation scripts, Notion templates, Canva templates, spreadsheet templates, ebooks/courses, workflow templates, prompt packs. What actually SELLS globally RIGHT NOW without needing a following?

2. **Which global platform?** Instamojo is India-only. For global: Gumroad (10% fee, Indian bank withdrawal), Payhip (5% fee), Etsy (built-in traffic), Amazon KDP. Which one should I use and why?

3. **Discovery with ZERO audience** — No LinkedIn, no Twitter, no Instagram, no blog. How do people find my products? Etsy search? Gumroad Discover? Product Hunt? Quora? Reddit? Affiliate programs? What's the FASTEST path to a first sale?

4. **The hard truth check** — Can someone with no audience, no website, and banned from major platforms actually make money from digital products? Is this viable or am I chasing another dead end?

5. **If viable — what's the ONE product I should build THIS WEEK** that gives the best chance of a global sale within 7 days?

Challenge every assumption. If this is hopeless, say so bluntly. I'd rather hear it now than waste weeks.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                msg_before = await pg.evaluate("document.querySelectorAll('[data-message-author-role]').length")
                print(f'Messages before: {msg_before}')
                
                # Ask first
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=20000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill('')
                await ta.fill(QUESTION)
                await asyncio.sleep(2)
                btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
                await btn.click()
                print('Sent')
                
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
                        print(f'\n=== CHATGPT ({len(text)} chars) ===')
                        print(text[:2000])
                        print(f'\n... ({len(text)} total chars)')
                        break
                    if i % 12 == 0:
                        print(f'  Wait ({i*5}s)')
                break

asyncio.run(main())
