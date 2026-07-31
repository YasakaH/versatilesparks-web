"""
LinkedIn fresh login — completely new profile, no automated history.
Uses launch_persistent_context for a truly clean browser session.
"""
import asyncio, os, shutil
from playwright.async_api import async_playwright

CDP_PORT = 9236
FRESH_PROFILE = r'C:\Users\varas\AppData\Local\Temp\linkedin-fresh'

async def main():
    if os.path.exists(FRESH_PROFILE):
        shutil.rmtree(FRESH_PROFILE)
        print('Deleted old profile')
    os.makedirs(FRESH_PROFILE, exist_ok=True)
    
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=FRESH_PROFILE,
            headless=False,
            args=[f'--remote-debugging-port={CDP_PORT}', '--no-first-run', '--no-default-browser-check'],
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        
        await page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        print('\n' + '='*60)
        print('LINKEDIN — FRESH BROWSER WINDOW OPENED')
        print('This is a clean profile with no automation history.')
        print('Log in with your credentials.')
        print('Do NOT navigate away — just log in and stay on feed.')
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
        print('\nBrowser stays open. Close when done.')

asyncio.run(main())
