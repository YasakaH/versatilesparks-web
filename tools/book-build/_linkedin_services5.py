"""
Step through LinkedIn Services setup.
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
            if 'linkedin' in pg.url and 'opportunities' in pg.url:
                li = pg
                break
        
        if not li:
            for pg in ctx.pages:
                if 'linkedin' in pg.url:
                    li = pg
                    break
        
        if not li:
            print('No LinkedIn tab')
            return
        
        await li.bring_to_front()
        
        # Go to services setup if not already there
        if 'opportunities/services' not in li.url:
            await li.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/opportunities/services/education/', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(3)
        
        print(f'URL: {li.url}')
        
        # Step 1: Click Continue
        await li.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.trim() === 'Continue' && b.offsetParent !== null) {
                    b.click();
                    return true;
                }
            }
            return false;
        }""")
        print('Clicked Continue')
        await asyncio.sleep(4)
        print(f'After Continue: {li.url}')
        
        # Step 2: Check what's on the next page
        text = await li.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Page 2: {text[:600]}')
        
        # Look for search/select fields
        fields = await li.evaluate("""() => {
            const inputs = document.querySelectorAll('input, select, [role="combobox"]');
            const r = [];
            inputs.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        ph: el.placeholder || '',
                        name: el.name || '',
                        label: el.getAttribute('aria-label') || '',
                        tag: el.tagName
                    });
                }
            });
            return r;
        }""")
        print(f'Fields: {fields}')
        
        # If there's a search field, use it
        for f in fields:
            if f['ph'] == 'Search' or 'search' in f['ph'].lower() or 'search' in f['label'].lower():
                sel = f'input[placeholder="{f["ph"]}"]' if f['ph'] else f'input'
                try:
                    await li.fill(sel, 'Operations')
                    await asyncio.sleep(2)
                    print('Filled "Operations"')
                    
                    # Check for dropdown results
                    options = await li.evaluate("""() => {
                        const items = document.querySelectorAll('[role="option"], li, [role="listbox"] > *');
                        const r = [];
                        items.forEach(el => {
                            if (el.offsetParent !== null) r.push(el.textContent.trim().substring(0, 50));
                        });
                        return r;
                    }""")
                    print(f'Options: {options[:10]}')
                except Exception as e:
                    print(f'Error: {e}')

asyncio.run(main())
