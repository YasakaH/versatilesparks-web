"""
Inspect the Digital File option element and click it properly.
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
        
        # Navigate to product types
        await dash.goto('https://manage.instamojo.com/dashboard/products/types', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(5)
        
        # Find the Digital File element and log its full HTML structure
        info = await dash.evaluate("""() => {
            const all = document.querySelectorAll('body *');
            const results = [];
            for (const el of all) {
                const t = el.textContent.trim();
                if (t.includes('Digital File') && t.length < 100 && el.offsetParent !== null) {
                    results.push({
                        tag: el.tagName,
                        text: t.substring(0, 80),
                        class: (el.className || '').substring(0, 60),
                        onclick: el.getAttribute('onclick') || '',
                        href: el.getAttribute('href') || '',
                        role: el.getAttribute('role') || '',
                        parent_tag: el.parentElement?.tagName || '',
                        parent_class: (el.parentElement?.className || '').substring(0, 60)
                    });
                }
            }
            return results;
        }""")
        print('Digital File elements:')
        for i in info:
            print(f'  {json.dumps(i, indent=2)}')

import json
asyncio.run(main())
