"""
Use Instamojo dashboard - click sidebar items to find product creation.
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
        
        # Get all clickable sidebar elements
        sidebar = await dash.evaluate("""() => {
            const links = document.querySelectorAll('nav a, aside a, [class*="sidebar"] a, [class*="menu"] a, li a');
            const r = [];
            links.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        text: el.textContent.trim().substring(0, 40),
                        href: el.href?.substring(0, 100) || ''
                    });
                }
            });
            return r;
        }""")
        print(f'Sidebar links:')
        for link in sidebar:
            print(f'  {link["text"]:30s} → {link["href"]}')
        
        # Try clicking "Create New"
        await dash.evaluate("""() => {
            const btns = document.querySelectorAll('button, a, [role="button"]');
            for (const b of btns) {
                if (b.textContent.trim() === 'Create New' && b.offsetParent !== null) {
                    b.click();
                    return true;
                }
            }
            return false;
        }""")
        await asyncio.sleep(3)
        print(f'\nAfter Create New: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Text: {text[:400]}')

asyncio.run(main())
