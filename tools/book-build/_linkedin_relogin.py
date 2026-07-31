"""
Open fresh LinkedIn login, then start outreach after login.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Open LinkedIn login in new tab
        page = await ctx.new_page()
        await page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        print('LinkedIn login opened in new tab.')
        print('Please log in.')
        print('Waiting up to 5 minutes...')
        
        for i in range(60):
            await asyncio.sleep(5)
            url = page.url
            if 'feed' in url or 'checkpoint' in url or ('login' not in url.lower() and 'authwall' not in url.lower()):
                print(f'Logged in! URL: {url[:80]}')
                break
            if i % 12 == 0:
                print(f'  Waiting... ({i*5}s)')
        else:
            print('Login timeout')
            return
        
        # Now go to profile
        await page.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(3)
        print(f'Profile: {page.url[:80]}')
        
        # Find "Add section" or services
        text = await page.evaluate('document.body.innerText.substring(0, 500)')
        print(f'Page: {text[:300]}')

asyncio.run(main())
