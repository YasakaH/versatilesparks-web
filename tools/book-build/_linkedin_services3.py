"""
Complete LinkedIn Services setup flow.
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
        print(f'1. URL: {li.url}')
        
        # We're on the services setup page. Click Continue
        cont = await li.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Continue') {
                    btn.click();
                    return 'Clicked Continue';
                }
            }
            return 'No Continue button';
        }""")
        print(f'  {cont}')
        await asyncio.sleep(3)
        print(f'2. URL: {li.url}')
        
        # Step 2: Select service category
        # Look for Operations category options
        cat = await li.evaluate("""() => {
            const els = document.querySelectorAll('label, [role="radio"], [role="checkbox"], button, div[role="button"]');
            const r = [];
            els.forEach(el => {
                const t = el.textContent.trim().substring(0, 60);
                if (t && el.offsetParent !== null) r.push(t);
            });
            return r;
        }""")
        print(f'Available options: {cat[:20]}')
        
        # Check for search/select field
        fields = await li.evaluate("""() => {
            const inputs = document.querySelectorAll('input, select, [role="combobox"]');
            const r = [];
            inputs.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({tag: el.tagName, placeholder: el.placeholder, name: el.name, id: el.id});
                }
            });
            return r;
        }""")
        print(f'Form fields: {fields}')
        
        # Try to search for "Operations" or "Strategic Planning"
        for inp in fields:
            if inp.get('placeholder') == 'Search' or (inp.get('placeholder') and 'search' in inp.get('placeholder','').lower()):
                sel = f'input[placeholder="{inp["placeholder"]}"]'
                try:
                    await li.fill(sel, 'Operations')
                    await asyncio.sleep(1)
                    # Wait for results and click
                    result = await li.evaluate("""() => {
                        const items = document.querySelectorAll('[role="option"], [role="listbox"] option, li');
                        for (const item of items) {
                            if (item.textContent.includes('Operations')) {
                                item.click();
                                return 'Clicked Operations';
                            }
                        }
                        return 'Not found';
                    }""")
                    print(f'  Search result: {result}')
                except:
                    pass

asyncio.run(main())
