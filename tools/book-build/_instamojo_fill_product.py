"""
Fill digital product form on Instamojo.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def fill(page, sel, val, timeout=5000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.2)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        prod = None
        for pg in ctx.pages:
            if 'products/create' in pg.url:
                prod = pg
                break
        
        if not prod:
            print('Product creation tab not found')
            for pg in ctx.pages:
                if 'manage.instamojo.com' in pg.url:
                    prod = pg
                    break
        
        if not prod:
            print('No Instamojo manage tab')
            return
        
        await prod.bring_to_front()
        if 'products/create' not in prod.url:
            await prod.goto('https://manage.instamojo.com/dashboard/products/create?type=digital-product', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
        
        print(f'URL: {prod.url[:100]}')
        
        # Get all form fields
        fields = await prod.evaluate("""() => {
            const r = [];
            document.querySelectorAll('input, textarea, select').forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        name: (el.name || '').substring(0, 30),
                        id: (el.id || '').substring(0, 30),
                        ph: (el.placeholder || '').substring(0, 40),
                        type: el.type || el.tagName
                    });
                }
            });
            return r;
        }""")
        print('Form fields:')
        for f in fields:
            print(f'  name="{f["name"]}" id="{f["id"]}" ph="{f["ph"]}" type="{f["type"]}"')
        
        # Fill product name (field name is "title")
        f1 = await fill(prod, 'input[name="title"]', 'AI Business Toolkit: 50 Prompts for Indian Businesses')
        print(f'Name: {"OK" if f1 else "FAIL"}')
        
        # Fill price
        f2 = await fill(prod, 'input[name="price"]', '499')
        print(f'Price: {"OK" if f2 else "FAIL"}')
        
        # Fill description via JS
        desc = "50 ready-to-use AI prompts for Indian businesses. Covers marketing, customer service, sales, operations, finance, product descriptions, email, strategy, content, and HR. India-specific (Hinglish, UPI, festivals). Works with ChatGPT, Gemini, Claude. Lifetime updates. Instant download."
        await prod.evaluate(f"""() => {{
            const tas = document.querySelectorAll('textarea');
            for (const ta of tas) {{
                if (ta.offsetParent !== null) {{
                    const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    s.call(ta, `{desc}`);
                    ta.dispatchEvent(new Event('input', {{bubbles:true}}));
                    return true;
                }}
            }}
            return false;
        }}""")
        print('Description: set via JS')
        
        print('\nProduct form filled! Now needs:')
        print('1. Upload the product file (50-prompts.md + README.md)')
        print('2. Click "Save"')
        print('File location: C:\\Users\\varas\\money-maker\\digital-products\\ai-business-toolkit\\')

asyncio.run(main())
