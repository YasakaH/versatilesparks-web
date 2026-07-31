"""
Send video research to ChatGPT - define Browser Operator Studio.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I watched 5 digital product videos. Key takeaways:

1. "7 Digital Product Ideas Using AI" (500K views) — Clipart, coloring pages, wall art, patterns, t-shirt designs, wedding invitations, business cards. All sellable on Etsy/Gumroad. Made with AI tools.

2. "FULL COURSE: Build & Sell Digital Products With AI" (2026) — Micro-niche AI apps built with no-code tools. Key quote: "What almost nobody explains is that those are the actual business. People quietly winning aren't digging for gold. They're selling the shovels."

3. "Low Competition Digital Product Ideas" — Baby shower e-vites, digital planners. $2K/month on Etsy.

4. "How to Start a Digital Product Business" (2026) — Tips on picking niche, getting sales WITHOUT social media audience.

5. "I Tried Selling Digital Products for 90 Days" (1.8M views) — $1,165 in 3 months selling digital stickers on Etsy. Key: traffic comes from Etsy search, not outside.

Earlier you suggested "Browser Operator Studio" — a desktop app where users describe browser tasks in plain English and it generates/runs nodriver automations locally at $99 lifetime.

Now I need you to give me the FULL detailed definition of what Browser Operator Studio IS. Not a one-paragraph idea — a real product specification covering:

1. What it does (exact user workflow, step by step)
2. Who it's for (exact target customer)
3. How it's different from existing tools (Playwright, Selenium, Puppeteer, Browserbase, etc.)
4. What the MVP looks like (minimum buildable version)
5. Pricing model details
6. How the first buyer finds it (specific Reddit/GitHub strategy)
7. Build time estimate
8. Why it's defensible

Be specific and practical. No theory."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                count = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'Messages: {count}')
                
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=30000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill(MSG)
                await asyncio.sleep(1.5)
                await pg.keyboard.press('Control+Enter')
                print('Sent')
                
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
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
