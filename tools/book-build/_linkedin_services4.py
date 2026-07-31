"""
Go to the correct services setup page and interact with it.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        li = None
        for pg in ctx.pages:
            if 'linkedin' in pg.url:
                li = pg
                break
        
        if not li:
            print('No LinkedIn tab')
            return
        
        await li.bring_to_front()
        
        # Go to the correct services page
        correct_url = 'https://www.linkedin.com/in/yasaka-hanini-293150422/opportunities/services/education/'
        await li.goto(correct_url, wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'URL: {li.url}')
        
        # Read the page
        text = await li.evaluate('document.body.innerText.substring(0, 1500)')
        print(f'Page:\n{text[:800]}')
        
        # Find interactive elements
        info = await li.evaluate("""() => {
            const all = document.querySelectorAll('button, input, select, [role="button"], a');
            const r = [];
            all.forEach(el => {
                if (el.offsetParent !== null) {
                    const txt = el.textContent?.trim()?.substring(0, 40) || el.placeholder || el.getAttribute('aria-label') || el.tagName;
                    r.push(txt);
                }
            });
            return r;
        }""")
        print(f'\nInteractive: {info}')

asyncio.run(main())
