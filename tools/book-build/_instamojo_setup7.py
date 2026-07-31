"""
Click through Instamojo dashboard sections.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        dash = None
        for pg in ctx.pages:
            if 'instamojo.com/dashboard' in pg.url:
                dash = pg
                break
        
        if not dash:
            print('Dashboard not found')
            return
        
        await dash.bring_to_front()
        await dash.goto('https://www.instamojo.com/dashboard/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Click "Products" in manage section
        clicked = await dash.evaluate("""() => {
            const links = document.querySelectorAll('a, span, div');
            for (const l of links) {
                if (l.textContent.trim() === 'Products' && l.offsetParent !== null) {
                    l.click();
                    return true;
                }
            }
            return false;
        }""")
        print(f'Clicked Products: {clicked}')
        await asyncio.sleep(4)
        print(f'URL: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Text: {text[:400]}')
        
        # Also try "Store"
        await dash.evaluate("""() => {
            const links = document.querySelectorAll('a, span, div');
            for (const l of links) {
                if (l.textContent.trim() === 'Store' && l.offsetParent !== null) {
                    l.click();
                    return true;
                }
            }
            return false;
        }""")
        await asyncio.sleep(4)
        print(f'\nAfter clicking Store: {dash.url[:100]}')
        text2 = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Text: {text2[:400]}')

asyncio.run(main())
