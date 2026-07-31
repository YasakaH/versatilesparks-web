"""
Launch fresh Brave + ChatGPT for cookbook building.
User logs in, then we send the blueprint challenges.
"""
import asyncio, subprocess, os, urllib.request
from playwright.async_api import async_playwright

CDP_PORT = 9230
TEMP_DIR = r'C:\Users\varas\AppData\Local\Temp\chatgpt-cookbook-build'
BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

MSG = """I'm building the Python Browser Automation Cookbook and need your guidance.

We already established:
- 50 Production Recipes Using nodriver
- $29 PDF / $59 Bundle
- 8 chapters

## What I need now

**Challenge my TOC suggestions and answer technical decisions.**

My proposed changes to the TOC:
1. Add a **Stealth & Anti-Detection** chapter (nodriver's #1 value)
2. Move **Production Patterns** (retry, timeouts, logging) to Chapter 3, not Chapter 7
3. Recipe 50 should be a **Production Starter Kit** — list every file in it
4. Ship **30 recipes in v1** (5-7 days) → update to 50 in v2

**Technical decisions needed:**
- Python 3.11+ or 3.9+?
- All async or provide sync wrappers?
- nodriver or zendriver?
- One .py per recipe or a package?
- pip install + Chrome detection?
- One retry pattern for all recipes?
- Anti-detection line: explain WHY it works without teaching abuse?
- Production Starter Kit file list?

I will challenge each decision. Start with the TOC changes."""

async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    proc = subprocess.Popen([
        BRAVE, f'--remote-debugging-port={CDP_PORT}',
        f'--user-data-dir={TEMP_DIR}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1200,800',
        'https://chat.openai.com/auth/login'
    ])
    
    for _ in range(30):
        try:
            urllib.request.urlopen(f'http://localhost:{CDP_PORT}/json/version')
            break
        except:
            await asyncio.sleep(1)
    
    await asyncio.sleep(5)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        
        print('\nFresh Brave opened. Log into ChatGPT.')
        for i in range(300):
            try:
                ta = await page.wait_for_selector('#prompt-textarea', timeout=5000)
                if ta:
                    print(f'Logged in! ({i}s)')
                    break
            except:
                pass
            if i % 10 == 0:
                print(f'  Waiting... ({i}s)')
            await asyncio.sleep(1)
        
        # Send the message
        await ta.click()
        await asyncio.sleep(0.5)
        await ta.fill(MSG)
        await asyncio.sleep(1.5)
        await page.keyboard.press('Control+Enter')
        print('Message sent')
        
        # Wait for response
        prev = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
        for i in range(120):
            await asyncio.sleep(5)
            cur = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
            if cur > prev:
                await asyncio.sleep(10)
                text = await page.evaluate("""() => {
                    const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                    return m[m.length-1]?.innerText || '';
                }""")
                print(f'\n=== RESPONSE ({len(text)} chars) ===')
                print(text[:1000])
                break
            if i % 12 == 0:
                print(f'  W ({i*5}s)')
        
        print('\nDone. Browser stays open.')
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
