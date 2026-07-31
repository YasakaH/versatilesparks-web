"""
Ask ChatGPT for Recipes 3 and 4.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Recipes 1 (launch browser) and 2 (tabs) are built and tested. Now:

## Recipe 3 — Use Persistent Profiles
Give me:
1. Title and problem statement
2. Code
3. What to explain (what IS a browser profile? why persist it?)
4. Edge cases (profile corrupted? first run with no profile?)

## Recipe 4 — Configure Browser Startup
Give me:
1. Title and problem statement
2. Code
3. What to explain (headless mode, window size, language settings)
4. Edge cases (headless on Windows vs Linux?)

These are the last two recipes in Chapter 1 (Getting Started). After these, move to Chapter 2 (Browser Control).

Challenge: For Recipe 3, nodriver's `user_data_dir` parameter might create a temporary profile by default. How do I test "persistent profile" without a pre-existing profile? Should the recipe create a temp dir first?"""

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
                        print(f'\n=== RECIPES 3-4 ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
