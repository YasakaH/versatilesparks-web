"""
Get ChatGPT to design the cookbook blueprint - sections, approaches, tech debt.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = """We're building the Python Browser Automation Cookbook. But first, I need you to design the blueprint.

## Requirements
- 50 production recipes using nodriver
- $29 PDF / $59 bundle (PDF + code + templates)
- 5-7 day build time

## Phase 1: Freeze the table of contents

Design the FULL 50-recipe structure. Organize into chapters. Each recipe needs:
- Recipe number and title
- Problem statement (1 sentence)
- Solution approach
- Key nodriver technique used
- Edge cases it covers

## Phase 2: Technical decisions

I need you to declare positions on:
1. **Python version** — 3.11+ or 3.9+? What about compatibility?
2. **nodriver vs zendriver** — zendriver is the fork with Docker support. Which one for the book?
3. **Async vs sync** — nodriver is async-first. Do I teach async patterns or provide sync wrappers?
4. **Project structure** — Single script per recipe? Modular package? What structure?
5. **Installation approach** — pip install nodriver + Chrome? What about Windows vs Linux differences?
6. **Error handling patterns** — retry logic, timeout handling, element not found — what's the reusable pattern?
7. **Testing** — How do I write recipes that don't break when websites change?
8. **Anti-detection ethics** — Where's the line between "undetected" and "unethical"? What do I include vs exclude?

## Phase 3: Challenge each decision

As you propose each approach, I will push back. Be ready to defend your choices.

## Phase 4: Freeze scope

After debate, give me the EXACT frozen scope:
- Chapters and recipe titles (all 50)
- Python version decision
- Sync vs async decision
- Project structure
- What's explicitly OUT of scope

Start with the table of contents. I want to see all 50 recipes organized by chapter."""

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
                print('Blueprint request sent')
                
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
                        print(f'\n=== BLUEPRINT ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
