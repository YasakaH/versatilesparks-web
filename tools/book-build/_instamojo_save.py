"""
Fix validation issues and save Instamojo product.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        prod = None
        for pg in ctx.pages:
            if 'manage.instamojo.com' in pg.url:
                prod = pg
                break
        
        if not prod:
            print('Not found')
            return
        
        await prod.bring_to_front()
        
        # Set unlimited quantity
        await prod.evaluate("""() => {
            const cbs = document.querySelectorAll('input[type="checkbox"]');
            for (const cb of cbs) {
                if (cb.name === 'unlimited_qty' && cb.offsetParent !== null) {
                    cb.checked = true;
                    cb.dispatchEvent(new Event('change', {bubbles:true}));
                    return true;
                }
            }
            return false;
        }""")
        print('Unlimited quantity set')
        await asyncio.sleep(1)
        
        # Click Save
        await prod.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.trim().toLowerCase() === 'save' && b.offsetParent !== null) {
                    b.click();
                    return true;
                }
            }
            return false;
        }""")
        print('Save clicked')
        await asyncio.sleep(5)
        print(f'URL: {prod.url[:100]}')
        
        # Check result
        text = await prod.evaluate('document.body.innerText.substring(0, 400)')
        print(f'Result: {text[:300]}')

asyncio.run(main())
