"""
Fill Instamojo store profile and add product.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def fill(page, sel, val, timeout=8000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.2)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def click_text(page, text):
    return await page.evaluate(f"""() => {{
        const all = document.querySelectorAll('button, a, span, div[role="button"]');
        for (const el of all) {{
            if (el.textContent.trim() === '{text}' && el.offsetParent !== null) {{
                el.click();
                return true;
            }}
        }}
        return false;
    }}""")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        dash = None
        for pg in ctx.pages:
            if 'instamojo.com/dashboard' in pg.url:
                dash = pg
                break
        
        if not dash:
            print('Dashboard not found')
            return
        
        await dash.bring_to_front()
        
        # === STORE PROFILE ===
        print('=== STORE PROFILE ===')
        await dash.goto('https://manage.instamojo.com/dashboard/manage-store', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Fill store name
        f1 = await fill(dash, 'input[name="name"]', 'Easy Automation')
        print(f'Store name: {"OK" if f1 else "FAIL"}')
        
        # Fill tagline if exists
        f2 = await fill(dash, 'input[name="tagline"]', 'AI-Powered Business Automation for Indian Businesses')
        print(f'Tagline: {"OK" if f2 else "SKIP"}')
        
        # Fill about/bio
        about = 'I build practical AI and Python automation solutions that eliminate repetitive business work. Specializing in browser automation, document processing, and workflow optimization for Indian businesses.'
        await dash.evaluate(f"""() => {{
            const tas = document.querySelectorAll('textarea');
            for (const ta of tas) {{
                if (ta.offsetParent !== null) {{
                    const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    s.call(ta, '{about}');
                    ta.dispatchEvent(new Event('input', {{bubbles:true}}));
                    return true;
                }}
            }}
            return false;
        }}""")
        print(f'About: set via JS')
        
        # Save
        await click_text(dash, 'Save')
        await asyncio.sleep(2)
        print('Saved profile')
        
        # === ADD PRODUCT ===
        print('\n=== ADD PRODUCT ===')
        await dash.goto('https://manage.instamojo.com/dashboard/products', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Click "Add Product"
        await click_text(dash, 'Add Product')
        await asyncio.sleep(4)
        print(f'Add Product URL: {dash.url[:100]}')
        
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Add Product page: {text[:400]}')
        
        # Fill product form
        fields = await dash.evaluate("""() => {
            const inputs = document.querySelectorAll('input, textarea, select');
            const r = [];
            inputs.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        ph: (el.placeholder || '').substring(0, 40),
                        name: (el.name || '').substring(0, 40),
                        type: el.type || el.tagName
                    });
                }
            });
            return r;
        }""")
        print(f'Form fields: {json.dumps(fields, indent=2)[:600]}')

asyncio.run(main())
