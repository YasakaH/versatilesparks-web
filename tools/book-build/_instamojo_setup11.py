"""
Fill Instamojo store profile fields.
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
            if 'manage.instamojo.com' in pg.url or 'instamojo.com/dashboard' in pg.url:
                dash = pg
                break
        
        if not dash:
            print('No Instamojo tab')
            return
        
        await dash.bring_to_front()
        
        # Navigate to store profile
        await dash.goto('https://manage.instamojo.com/dashboard/manage-store', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Store profile: {dash.url[:80]}')
        
        # Fill email
        await dash.evaluate("""() => {
            const inputs = document.querySelectorAll('input[name="shop_communication_email"]');
            if (inputs[0]) {
                const s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                s.call(inputs[0], 'yasaka.hanini@protonmail.com');
                inputs[0].dispatchEvent(new Event('input', {bubbles:true}));
                return true;
            }
            return false;
        }""")
        print('Email set')
        
        # Fill contact info
        await dash.evaluate("""() => {
            const inputs = document.querySelectorAll('input[name="shop_contact_info"]');
            if (inputs[0]) {
                const s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                s.call(inputs[0], 'AI-Powered Business Automation for Indian Businesses');
                inputs[0].dispatchEvent(new Event('input', {bubbles:true}));
                return true;
            }
            return false;
        }""")
        print('Contact info set')
        
        # Find and fill textarea (About Us)
        await dash.evaluate("""() => {
            const tas = document.querySelectorAll('textarea');
            for (const ta of tas) {
                if (ta.offsetParent !== null) {
                    const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    s.call(ta, 'I build practical AI and Python automation solutions that eliminate repetitive business work. I specialize in browser automation, document processing, and workflow optimization for Indian businesses.');
                    ta.dispatchEvent(new Event('input', {bubbles:true}));
                    return true;
                }
            }
            return false;
        }""")
        print('About/Description set')
        
        # Try to find and click Save button
        saved = await dash.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                const t = b.textContent.trim().toLowerCase();
                if ((t === 'save' || t.includes('save') || t === 'update') && b.offsetParent !== null) {
                    b.click();
                    return b.textContent.trim();
                }
            }
            return 'NOT_FOUND';
        }""")
        print(f'Save button: {saved}')
        await asyncio.sleep(3)
        
        # Now go to Add Product page
        print('\n--- ADDING PRODUCT ---')
        await dash.goto('https://manage.instamojo.com/dashboard/products', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Click Add Product
        await dash.evaluate("""() => {
            const all = document.querySelectorAll('a, button, span');
            for (const el of all) {
                if (el.textContent.trim() === 'Add Product' && el.offsetParent !== null) {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        await asyncio.sleep(5)
        print(f'Add Product URL: {dash.url[:80]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Page: {text[:400]}')
        
        # Check form fields
        fields = await dash.evaluate("""() => {
            const r = [];
            document.querySelectorAll('input, textarea, select').forEach(el => {
                if (el.offsetParent !== null) {
                    r.push({
                        name: (el.name || '').substring(0, 30),
                        ph: (el.placeholder || '').substring(0, 30),
                        id: (el.id || '').substring(0, 30),
                        type: el.type || el.tagName
                    });
                }
            });
            return r;
        }""")
        print('Fields:')
        for f in fields:
            print(f'  name="{f["name"]}" ph="{f["ph"]}" id="{f["id"]}" type="{f["type"]}"')

asyncio.run(main())
