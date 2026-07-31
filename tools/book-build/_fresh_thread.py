"""
Start fresh ChatGPT thread with ALL research data.
Uses nodriver (undetected) + fresh page.
"""
import asyncio, subprocess, os, json, urllib.request
from playwright.async_api import async_playwright

CDP_PORT = 9232  
TEMP_DIR = r'C:\Users\varas\AppData\Local\Temp\chatgpt-fresh-thread'
BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

MSG = """I need your help choosing a digital product to build and sell.

I researched TWO datasets:

DATASET 1: Pain points across 8 business domains (real frustrations from Reddit/forums)
DATASET 2: Proven winning digital products with real revenue data

Gumroad ($206M tracked, 146K products):
- Software Development: $65.8M total, $60,814/product
- Writing & Publishing: $15,750/product, 226 products only
- Top product: AI Photoshop Script — $586K at $50
- Digital downloads = 85% of catalog

Etsy best-sellers:
- Wedding invitations ($15-50), planners ($5-30), wall art ($3-25)
- Business templates ($10-40), SVG cut files ($3-20)

Notion templates: Thomas Frank $1M, Easlo $239K

My skills: Python, AI/automation, FreeLLMAPI (free AI), nodriver (undetected browser)
My channels: Instamojo (India), Gumroad (global)
My limits: Zero audience, zero website, can build in 3-5 days

Give me your analysis of where pain points (dataset 1) and proven winners (dataset 2) overlap with my skills. Then recommend ONE specific product with: exact name, price, platform, and how I get my first buyer."""

async def main():
    # Clean and launch
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'brave.exe'], capture_output=True)
    except:
        pass
    await asyncio.sleep(2)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    proc = subprocess.Popen([
        BRAVE, f'--remote-debugging-port={CDP_PORT}',
        f'--user-data-dir={TEMP_DIR}',
        '--no-first-run', '--no-default-browser-check',
        'https://chatgpt.com/auth/login'
    ])
    
    for _ in range(30):
        try:
            urllib.request.urlopen(f'http://localhost:{CDP_PORT}/json/version')
            break
        except:
            await asyncio.sleep(1)
    
    await asyncio.sleep(15)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        
        await page.wait_for_selector('#prompt-textarea', timeout=60000)
        await asyncio.sleep(3)
        
        # Type msg
        ta = await page.wait_for_selector('#prompt-textarea', timeout=10000)
        await ta.click()
        await asyncio.sleep(1)
        await ta.fill(MSG)
        await asyncio.sleep(2)
        
        await page.keyboard.press('Control+Enter')
        print('Sent')
        
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
                print(text[:600])
                break
            if i % 12 == 0:
                print(f'  W ({i*5}s)')
        
        input('Press Enter to close...')
        proc.terminate()

asyncio.run(main())
