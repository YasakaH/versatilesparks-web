"""
Challenge browser.py design, then get final code + move to next file.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Good design for browser.py. I challenge 3 things:

## Challenge 1: Zero exception handling
You said "let exceptions bubble upward" and "Recipe 1 teaches what startup failure looks like." But a bare nodriver failure might show a cryptic traceback. Can I at least wrap in a try/except that prints "nodriver failed to start. Make sure Chrome is installed and up to date." before re-raising? That's not hiding the error — it's explaining it.

## Challenge 2: Only 2 parameters
headless and user_data_dir are useful, but what about BROWSER_LANGUAGE and WINDOW_SIZE from config? Should launch_browser() also accept language and window_size overrides? Or is that config.py's job?

## Challenge 3: No logging at all
Even this would be useful:
async def launch_browser(...):
    logger.debug("Starting browser...")
    browser = await uc.start(...)
    logger.debug("Browser started")
That's 2 lines. It helps debugging without becoming "a framework."

## After you respond, give me the FINAL code for browser.py

Then I'll move to:
2. config.py
3. retry.py
4. Recipe 1 code

One file at a time, challenge each one."""

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
                print('Challenges sent')
                
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
                        print(f'\n=== BROWSER.PY FINAL ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
