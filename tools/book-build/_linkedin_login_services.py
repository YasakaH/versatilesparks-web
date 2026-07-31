"""
Open LinkedIn login, wait for user to log in, then add services.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Create new tab for LinkedIn
        page = await ctx.new_page()
        await page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        print('LinkedIn login page opened in new tab')
        print('Log in with your credentials...')
        
        # Wait for user to log in (checking URL change)
        for i in range(120):
            await asyncio.sleep(5)
            if 'feed' in page.url or 'checkpoint' in page.url or 'login' not in page.url.lower():
                print(f'Logged in! URL: {page.url[:80]}')
                break
            if i % 12 == 0:
                print(f'  Waiting for login... ({i*5}s)')
        else:
            print('Login timeout')
            return
        
        # Now go to services page
        await page.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/opportunities/services/education/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Services page: {page.url[:100]}')
        
        if 'authwall' in page.url or 'login' in page.url:
            print('Still blocked. Trying direct profile navigation...')
            await page.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
            
            # Try adding services from profile
            text = await page.evaluate('document.body.innerText.substring(0, 1000)')
            print(f'Profile text: {text[:400]}')
            
            # Look for "Add services" section
            has_services = await page.evaluate("""() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.textContent.toLowerCase().includes('service') && b.offsetParent !== null) {
                        b.click();
                        return b.textContent.trim();
                    }
                }
                return 'NOT_FOUND';
            }""")
            print(f'Services button: {has_services}')
            await asyncio.sleep(2)

asyncio.run(main())
