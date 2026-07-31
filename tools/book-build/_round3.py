"""
Send Round 3 via script file - handles ChatGPT heavy page.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230
MSG = """Round 3 — No audience, no ads, no SEO. How do I get first 10 users?

Also what's my real advantage if not free AI?
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                msg_count = await pg.evaluate("document.querySelectorAll('[data-message-author-role]').length")
                print(f'Messages: {msg_count}')
                
                # Fill via keyboard typing (more reliable than value setter)
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=15000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.type(MSG, delay=10)
                await asyncio.sleep(2)
                
                # Send via keyboard shortcut
                await pg.keyboard.press('Control+Enter')
                print('R3 sent via Ctrl+Enter')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return m[m.length-1]?.innerText?.substring(0, 400) || '';
                        }""")
                        print(f'R3 done: {text[:200]}')
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
