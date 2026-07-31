"""
Navigate Instamojo store builder and add products.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        store = None
        for pg in ctx.pages:
            if 'easyautomation.stores.instamojo.com' in pg.url:
                store = pg
                break
        
        if not store:
            print('Store tab not found')
            return
        
        await store.bring_to_front()
        
        # Click "Builder" button
        await store.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.trim() === 'Builder' && b.offsetParent !== null) {
                    b.click();
                    return true;
                }
            }
            return false;
        }""")
        print('Clicked Builder')
        await asyncio.sleep(5)
        print(f'URL: {store.url[:100]}')
        text = await store.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Builder page: {text[:500]}')

asyncio.run(main())
