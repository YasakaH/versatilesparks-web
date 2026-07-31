"""
Explore Instamojo dashboard - store setup and products.
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
            print('Dashboard tab not found')
            return
        
        await dash.bring_to_front()
        
        # Check Products page
        await dash.goto('https://www.instamojo.com/dashboard/store/products/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Products: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Products page: {text[:600]}')
        
        # Get all visible buttons/links
        btns = await dash.evaluate("""() => {
            const all = document.querySelectorAll('button, a, [role="button"]');
            const r = [];
            all.forEach(el => {
                if (el.offsetParent !== null) {
                    const t = el.textContent.trim();
                    if (t.length > 0 && t.length < 60) r.push(t);
                }
            });
            return r.slice(0, 30);
        }""")
        print(f'Buttons: {btns}')

asyncio.run(main())
