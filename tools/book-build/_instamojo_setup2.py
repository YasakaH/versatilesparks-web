"""
Set up Instamojo store - branding, products, details.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def fill(page, sel, val, timeout=8000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.3)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find the store tab
        store = None
        for pg in ctx.pages:
            if 'easyautomation.stores.instamojo.com' in pg.url:
                store = pg
                break
        
        if not store:
            print('Store tab not found')
            return
        
        await store.bring_to_front()
        print(f'Store URL: {store.url}')
        
        # Click "Customize Store" or "Builder"
        clicked = await store.evaluate("""() => {
            const btns = document.querySelectorAll('button, a, [role="button"]');
            for (const b of btns) {
                const t = b.textContent.trim().toLowerCase();
                if ((t.includes('customize') || t.includes('builder')) && b.offsetParent !== null) {
                    b.click();
                    return b.textContent.trim();
                }
            }
            return 'NOT_FOUND';
        }""")
        print(f'Clicked: {clicked}')
        await asyncio.sleep(4)
        print(f'URL after: {store.url[:100]}')
        
        # Check what's available in builder
        text = await store.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Builder: {text[:500]}')
        
        # Look for store name/settings
        fields = await store.evaluate("""() => {
            const inputs = document.querySelectorAll('input, textarea, select');
            const r = [];
            inputs.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        ph: el.placeholder?.substring(0, 40) || '',
                        name: el.name?.substring(0, 40) || '',
                        id: el.id?.substring(0, 40) || '',
                        val: el.value?.substring(0, 40) || ''
                    });
                }
            });
            return r;
        }""")
        print(f'Fields: {json.dumps(fields, indent=2)[:500]}')

import json
asyncio.run(main())
