"""
Upload product file and save on Instamojo.
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
            print('No Instamojo tab')
            return
        
        await prod.bring_to_front()
        if 'products/create' not in prod.url:
            await prod.goto('https://manage.instamojo.com/dashboard/products/create?type=digital-product', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
        
        print(f'URL: {prod.url[:80]}')
        
        # Find file input
        file_input = await prod.query_selector('input[type="file"]')
        if file_input:
            # Upload the product file
            file_path = r'C:\Users\varas\money-maker\digital-products\ai-business-toolkit\50-prompts.md'
            await file_input.set_input_files(file_path)
            print(f'File uploaded: {file_path}')
            await asyncio.sleep(3)
        else:
            print('File input not found')
        
        # Check for Save button
        save_btn = await prod.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                const t = b.textContent.trim().toLowerCase();
                if (t === 'save' && b.offsetParent !== null) {
                    b.click();
                    return 'Clicked Save';
                }
            }
            return 'NOT_FOUND';
        }""")
        print(f'Save: {save_btn}')
        await asyncio.sleep(4)
        print(f'After save URL: {prod.url[:100]}')

asyncio.run(main())
