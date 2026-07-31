"""
Challenge Browser Operator Studio definition - build time and scope.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Good definition, but I have challenges:

1. **3-4 week build time** — Too long. I need a sale in 7-14 days, not a month. Can I strip the MVP to something buildable in 5-7 days?

2. **Natural language understanding** — You said "Describe any browser task in plain English and it just works" is a HARD problem. I agree. So why not skip NLU entirely in v1 and just sell **pre-built nodriver automation templates** instead? Like "Shopify Invoice Downloader.exe" that just works? That's a 2-day build.

3. **Electron + Python** — Complex stack. What if v1 is just a Python script with a CLI/GUI, no Electron? Use tkinter or a simple HTML wrapper?

4. **Target customer** — Marketing agencies and ecommerce owners don't browse Gumroad for tools. They Google "how to automate Shopify invoices." So the product name should be searchable. What's the SEO-friendly name?

5. **Pricing** — $99 lifetime for something that took 4 weeks to build. The AI Photoshop Script earned $586K at $50. What if I price it HIGHER — $199 — since it saves hours/week?

Challenge these assumptions. I want a version I can ship in 5-7 days."""

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
                        print(f'\n=== CHALLENGE RESPONSE ({len(text)} chars) ===')
                        print(text[:600])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
