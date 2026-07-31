"""
Challenge TOC and get technical decisions from ChatGPT.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """Good TOC but I have challenges before freezing:

## Challenges
1. **Recipe 48-50 are too vague** — "Website Monitoring Bot" and "Automated Report Downloader" don't match the recipe format (Problem → Solution → Technique). Give them the same format as the rest.
2. **Production Starter Kit (Recipe 50)** — Good idea but what EXACTLY is in it? List the files.
3. **Missing chapter**: Where's anti-detection? nodriver's #1 value is being undetected. Recipe 1 says "Launch without detection" but there's no dedicated chapter on stealth patterns.
4. **Ordering**: Chapter 7 (Production Patterns) has retry, timeouts, logging — these should be EARLY (Chapter 3) since readers need them from the start.
5. **50 recipes is a LOT for 5-7 days** — Can I ship 30 recipes in v1 and update to 50 in v2? Or is 50 the minimum viable?

## Phase 2: Technical decisions (answer ALL)
1. **Python version**: 3.11+ or 3.9+?
2. **Async vs sync**: All async? Or provide sync wrappers?
3. **nodriver vs zendriver**: Which one?
4. **Project structure**: Single .py per recipe? Or a package?
5. **Installation**: pip install nodriver + Chrome detection? What about Linux/Mac?
6. **Error handling**: One retry pattern used everywhere? Or per-recipe?
7. **Testing**: How to prevent bitrot when websites change?
8. **Anti-detection ethics**: Where's the line? nodriver passes 31/31 detection tests — do I explain WHY or just HOW?

Answer all 8. I will challenge each."""

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
                print('Challenges + technical Qs sent')
                
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
