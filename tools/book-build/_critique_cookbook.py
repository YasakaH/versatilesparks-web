"""
Send all 30 recipes to ChatGPT for deep critique and improvement.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """I need you to critique the entire cookbook for DEPTH. Not surface-level — REAL depth.

## What's been built
30 recipes across 8 chapters. Every recipe has: problem statement, code, and runs.

But I'm worried some are superficial — just code that "works" without teaching real problem-solving.

## I need you to critique EVERY chapter:

**Chapter 1 (Getting Started):** Recipes 1-4
- Does Recipe 1 explain WHY async? Or just show the pattern?
- Does Recipe 2 cover what happens when a tab crashes?
- Does Recipe 3 explain what browser profiles ARE (Chrome user-data-dir, cookies, extensions)?
- Does Recipe 4 cover headless detection? Some sites block headless Chrome.

**Chapter 2 (Browser Control):** Recipes 5-8
- Does Recipe 5 explain navigation timeouts? What if back() throws because there's no history?
- Does Recipe 6 explain full-page vs viewport screenshots? File naming conflicts?
- Does Recipe 7 cover JavaScript errors? What if evaluate() throws?
- Does Recipe 8 explain readyState differences (loading vs interactive vs complete)?

**Chapter 3 (Production Foundations):** Recipes 9-12
- Does Recipe 9 show how to wait for TEXT, not just elements?
- Does Recipe 10 show how to distinguish retryable vs non-retryable errors?
- Does Recipe 11 show structured logging vs print()? Log levels?
- Does Recipe 12 show how to switch between dev/production configs?

**Chapter 4 (Elements & Forms):** Recipes 13-18
- Does Recipe 13 teach STABLE selectors vs brittle ones? What about data-* attributes?
- Does Recipe 14 cover overlays intercepting clicks? Stale element references?
- Does Recipe 15 cover clearing fields before typing? What if fields have validation?
- Does Recipe 16 cover drag-and-drop upload zones vs simple file inputs?
- Does Recipe 17 cover custom JS dropdowns vs native <select>?
- Does Recipe 18 cover unexpected popups? What if a modal appears mid-automation?

**Chapter 5 (Authentication):** Recipes 19-22
- Does Recipe 19 cover login failure detection? CAPTCHA detection? Rate limiting?
- Does Recipe 20 cover cookie expiry? Domain-scoped cookies?
- Does Recipe 21 explain how to verify a session is STILL valid before reusing?
- Does Recipe 22 cover what happens when two profiles conflict?

**Chapter 6 (Extraction):** Recipes 23-27
- Does Recipe 23 cover broken tables (missing cells, colspan)?
- Does Recipe 24 cover infinite pagination loops? What if "Next" never disables?
- Does Recipe 25 cover how to detect when infinite scroll is truly done?
- Does Recipe 26 cover how Chrome downloads actually work? Waiting for completion?
- Does Recipe 27 cover lazy-loaded images (data-src)?

**Chapter 7 (Reliable Automation):** Recipes 28-29
- Does Recipe 28 actually explain what nodriver does differently? Or is it vague?
- Does Recipe 29 cover when to STOP vs when to RETRY?

**Chapter 8 (Starter Kit):** Recipe 30
- Does it actually explain HOW to start a new project from the scaffold?

## For each gap you find, tell me:
1. What's MISSING
2. What to ADD (exact code/examples)
3. How serious the gap is (minor / major / critical)

Be thorough. Don't spare my feelings. I want this cookbook to be genuinely valuable."""

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
                print('Critique sent')
                
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
                        print(f'\n=== CRITIQUE ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
