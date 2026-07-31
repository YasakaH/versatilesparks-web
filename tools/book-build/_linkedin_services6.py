"""
Click through LinkedIn services flow properly.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find LinkedIn tab
        li = None
        for pg in ctx.pages:
            u = pg.url
            if 'linkedin.com/in/yasaka' in u:
                li = pg
                break
        
        if not li:
            for pg in ctx.pages:
                if 'linkedin.com' in pg.url:
                    li = pg
                    break
        
        if not li:
            print('No LinkedIn tab')
            return
        
        await li.bring_to_front()
        
        # Navigate to the services page
        await li.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/opportunities/services/education/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'URL: {li.url}')
        
        # Try clicking "Showcase your services" first
        result = await li.evaluate("""() => {
            const all = document.querySelectorAll('button, [role="button"], a, div[tabindex]');
            for (const el of all) {
                const t = el.textContent.toLowerCase();
                if ((t.includes('showcase') || t.includes('service')) && el.offsetParent !== null) {
                    el.click();
                    return 'Clicked: ' + el.textContent.trim().substring(0, 50);
                }
            }
            return 'Not found';
        }""")
        print(f'Step 1: {result}')
        await asyncio.sleep(3)
        
        # Now try clicking "Continue"
        result2 = await li.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.trim() === 'Continue' && b.offsetParent !== null) {
                    b.click();
                    return 'Clicked Continue';
                }
            }
            return 'No Continue button';
        }""")
        print(f'Step 2: {result2}')
        await asyncio.sleep(3)
        
        print(f'After click: {li.url}')
        text = await li.evaluate('document.body.innerText.substring(0, 800)')
        print(f'Page: {text[:500]}')

asyncio.run(main())
