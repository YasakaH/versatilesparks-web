"""
Click Digital File option and fill product form.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

PRODUCT_NAME = "AI Business Toolkit: 50 Prompts for Indian Businesses"
PRODUCT_PRICE = "499"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        dash = None
        for pg in ctx.pages:
            if 'instamojo' in pg.url.lower() and 'products' in pg.url:
                dash = pg
                break
        
        if not dash:
            for pg in ctx.pages:
                if 'instamojo' in pg.url.lower():
                    dash = pg
                    break
        
        if not dash:
            print('No Instamojo tab')
            return
        
        await dash.bring_to_front()
        await dash.goto('https://manage.instamojo.com/dashboard/products/types', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Click the parent LI with "openable" class that contains "Digital File"
        clicked = await dash.evaluate("""() => {
            const items = document.querySelectorAll('li.openable');
            for (const li of items) {
                if (li.textContent.includes('Digital File')) {
                    li.click();
                    return true;
                }
            }
            return false;
        }""")
        print(f'Clicked Digital File: {clicked}')
        await asyncio.sleep(5)
        print(f'URL: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Page: {text[:400]}')

asyncio.run(main())
