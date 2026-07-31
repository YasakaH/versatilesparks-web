"""
Add product via Instamojo dashboard.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find dashboard tab
        dash = None
        for pg in ctx.pages:
            if 'instamojo.com/dashboard' in pg.url:
                dash = pg
                break
        
        if not dash:
            print('Dashboard tab not found')
            return
        
        await dash.bring_to_front()
        print(f'Dashboard: {dash.url}')
        
        # Look for product creation options
        await dash.goto('https://www.instamojo.com/dashboard/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        text = await dash.evaluate('document.body.innerText.substring(0, 1500)')
        print(f'Dashboard: {text[:800]}')

asyncio.run(main())
