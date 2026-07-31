"""
Ask ChatGPT for Recipe 2 (Connect to existing browser / tabs).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Recipe 1 written and tested (launch_browser → get page → close). Now I need Recipe 2.

According to the frozen TOC, Chapter 1 (Getting Started) has:
- Recipe 1: Launch Your First Browser Session ✅ DONE
- Recipe 2: Connect to an Existing Browser (or tabs/windows?)
- Recipe 3: Use Persistent Profiles
- Recipe 4: Configure Browser Startup

## Recipe 2 — Connect to an Existing Browser / Tabs & Windows

The TOC shows "Connect to an Existing Browser" for Recipe 2, but also mentions tabs/windows. What's the exact recipe?

Give me:
1. Exact title
2. Problem statement
3. Code (complete, runnable)
4. What to explain in the text
5. Edge cases (no browser running? multiple tabs? tab crashes?)

Challenge: If the recipe is "Connect to Existing Browser" — how do I test this without an already-running browser? Should Recipe 2 instead be about tabs and windows (which naturally follows Recipe 1)?

I'll push back if the recipe doesn't flow naturally from Recipe 1."""

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
                print('Recipe 2 request sent')
                
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
                        print(f'\n=== RECIPE 2 ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
