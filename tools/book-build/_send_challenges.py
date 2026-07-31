"""
Read full blueprint and send challenges + technical Qs.
Opens fresh tab to handle page weight.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

CHALLENGE = """Good TOC. Now my challenges before I freeze:

1. **Missing anti-detection chapter** — nodriver's #1 value is passing detection. There's no chapter on stealth. Add one or explain why not.

2. **Recipe 48-50 format** — "Website Monitoring Bot" is vague. Give them the same Problem→Solution→Technique format as the rest.

3. **Recipe 50 as Production Starter Kit** — Good idea. What EXACTLY is in it? List every file.

4. **Ordering** — Retry, timeouts, logging should be EARLY (Chapter 3), not Chapter 7. Readers need these from day one.

5. **50 recipes = 5-7 days?** — That's tight. Can I ship 30 in v1 and update to 50?

## Technical decisions needed

6. **Python version**: 3.11+ or 3.9+? 
7. **Async vs sync**: All async? Or provide sync wrappers for beginners?
8. **nodriver vs zendriver**: Which one for the book?
9. **Project structure**: One .py per recipe? Or a package with common utils?
10. **Installation**: pip install nodriver + Chrome? Windows/Linux/Mac differences?
11. **Error handling**: One retry pattern across all recipes? Or per-recipe?
12. **Anti-detection ethics**: Where's the line? I can explain WHY it works without teaching abuse.

Answer all. I will challenge each decision."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find chatgpt page
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                # Open FRESH tab to the same conversation
                conv_url = pg.url
                new_page = await ctx.new_page()
                await new_page.goto(conv_url, wait_until='domcontentloaded')
                await asyncio.sleep(8)
                
                count = await new_page.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'Fresh page messages: {count}')
                
                if count == 0:
                    # Need to wait more or login
                    print('0 messages - page might need login')
                    for i in range(30):
                        await asyncio.sleep(2)
                        count = await new_page.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                        if count > 0:
                            print(f'Now {count} messages')
                            break
                
                if count > 0:
                    ta = await new_page.wait_for_selector('#prompt-textarea', timeout=30000)
                    await ta.click()
                    await asyncio.sleep(0.5)
                    await ta.fill(CHALLENGE)
                    await asyncio.sleep(1.5)
                    await new_page.keyboard.press('Control+Enter')
                    print('Challenge sent')
                    
                    prev = await new_page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    for i in range(120):
                        await asyncio.sleep(5)
                        cur = await new_page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                        if cur > prev:
                            await asyncio.sleep(10)
                            text = await new_page.evaluate("""() => {
                                const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                                return m[m.length-1]?.innerText || '';
                            }""")
                            print(f'\n=== RESPONSE ({len(text)} chars) ===')
                            print(text[:1000])
                            break
                        if i % 12 == 0:
                            print(f'  W ({i*5}s)')
                break

asyncio.run(main())
