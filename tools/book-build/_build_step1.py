"""
Ask ChatGPT to guide the build - start with project structure + Recipe 1.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I'm starting to build the cookbook. Guide me through the first step.

## Step 1: Project structure

Give me the EXACT files I need to create:
- common/browser.py
- common/retry.py  
- common/logging.py
- common/config.py
- common/selectors.py
- common/timeouts.py
- common/session.py
- common/utils.py
- common/exceptions.py

For each file, tell me:
1. What functions/classes it contains
2. Key design decisions
3. What NOT to include (avoid over-engineering)

## Step 2: Recipe 1 — Launch Your First Browser Session

Give me the EXACT code for:
- Problem statement (1 sentence)
- Solution approach
- Code (complete, runnable)
- Edge cases covered
- What happens if Chrome isn't installed
- What happens if nodriver fails to start

## Challenge me

After you give me the code, I will challenge:
1. Error handling approach
2. What if user is on Windows vs Linux?
3. What if they don't have Chrome installed?

Start with the common/ files. Give me browser.py first."""

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
                print('Build guide request sent')
                
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
                        print(f'\n=== BUILD GUIDE ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
