"""
Read full blueprint response and send technical decisions challenge.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Blueprint changes accepted. Now I need the technical decisions frozen.

## Technical decisions needed

1. **Python version**: 3.11+ or 3.9+? (affects async syntax, typing)
2. **Async vs sync**: nodriver is async-first. Do I teach async patterns throughout? Or provide sync wrappers for beginners?
3. **nodriver vs zendriver**: zendriver is the fork with Docker support. Which one?
4. **Project structure**: One .py per recipe in a flat folder? Or a package with reusable utils?
5. **Installation**: pip install nodriver + auto-detect Chrome? What about Windows vs Linux differences?
6. **Error handling**: One retry pattern reused across ALL recipes? Or per-recipe customization?
7. **Anti-detection line in code**: What exactly do I SHOW in the stealth chapter? Browser profile configs? User-agent rotation? What crosses the line?
8. **Testing strategy**: How do I write recipes that won't break when websites change?

## Challenge each decision

For each one, give me:
- Your recommendation
- Why you chose it
- What the alternative is
- Why you rejected the alternative

I will push back on any I disagree with."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                c = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'Messages: {c}')
                
                # Read last response first
                if c > 0:
                    last = await pg.evaluate("""() => {
                        const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                        return m[m.length-1]?.innerText?.substring(0, 500) || '';
                    }""")
                    print(f'Last response preview: {last[:200]}')
                
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=30000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill(MSG)
                await asyncio.sleep(1.5)
                await pg.keyboard.press('Control+Enter')
                print('Tech decisions sent')
                
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
                        print(f'\n=== TECH DECISIONS ({len(text)} chars) ===')
                        print(text[:800])
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
