"""
LinkedIn login via REAL Brave (bypasses Playwright detection).
Launch Brave directly via subprocess, connect via CDP.
"""
import asyncio, subprocess, urllib.request, os
from playwright.async_api import async_playwright

BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
CDP_PORT = 9237
PROFILE = r'C:\Users\varas\AppData\Local\Temp\linkedin-real-brave'

async def main():
    # Clean profile
    if os.path.exists(PROFILE):
        import shutil
        shutil.rmtree(PROFILE)
    os.makedirs(PROFILE, exist_ok=True)
    
    # Launch REAL Brave (not Playwright's Chromium)
    proc = subprocess.Popen([
        BRAVE, f'--remote-debugging-port={CDP_PORT}',
        f'--user-data-dir={PROFILE}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1200,800',
        'https://www.linkedin.com/login'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for _ in range(30):
        try:
            urllib.request.urlopen(f'http://localhost:{CDP_PORT}/json/version')
            break
        except:
            await asyncio.sleep(1)
    else:
        print('Brave failed')
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        
        print('\n' + '='*60)
        print('REAL BRAVE — LinkedIn Login')
        print('This uses your actual Brave browser (not Playwright Chromium).')
        print('LinkedIn should NOT block this.')
        print('Log in and stay on the feed page.')
        print('='*60)
        
        for i in range(60):
            await asyncio.sleep(5)
            url = page.url
            if 'feed' in url:
                print(f'\nLogged in! Feed loaded.')
                break
            if i % 12 == 0:
                print(f'  Waiting... ({i*5}s)')
        
        print(f'\nFinal: {page.url[:100]}')
        print('\nBrave stays open. Close manually when done.')

asyncio.run(main())
