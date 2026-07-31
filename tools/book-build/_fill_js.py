"""
Fill profiles via JavaScript injection.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9235

def escape_js(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')

async def js_fill(page, selector, value):
    escaped = escape_js(value)
    result = await page.evaluate(f"""() => {{
        const find = (sel) => {{
            let el = document.querySelector(sel);
            if (!el) el = document.querySelector('[name="' + sel.replace(/[#.]/g,'') + '"]');
            if (!el) el = document.querySelector('[placeholder*="' + sel.replace(/[#.]/g,'') + '"]');
            if (!el) el = document.querySelector('[aria-label*="' + sel.replace(/[#.]/g,'') + '"]');
            return el;
        }};
        const el = find('{selector}');
        if (!el) return 'NOT_FOUND';
        el.click();
        const s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        s.call(el, '{escaped}');
        el.dispatchEvent(new Event('input', {{bubbles:true}}));
        el.dispatchEvent(new Event('change', {{bubbles:true}}));
        return 'OK';
    }}""")
    return result == 'OK'

async def js_set_textarea(page, value):
    escaped = escape_js(value)
    result = await page.evaluate(f"""() => {{
        let el = document.querySelector('textarea');
        if (!el) return 'NOT_FOUND';
        el.click();
        const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        s.call(el, '{escaped}');
        el.dispatchEvent(new Event('input', {{bubbles:true}}));
        el.dispatchEvent(new Event('change', {{bubbles:true}}));
        return 'OK';
    }}""")
    return result == 'OK'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        for i, pg in enumerate(ctx.pages):
            print(f'[{i}] {pg.url[:100]}')
        
        # LINKEDIN
        li = next((pg for pg in ctx.pages if 'linkedin.com' in pg.url and pg.url != 'chrome-error://chromewebdata/'), None)
        if li and 'linkedin' in li.url:
            print('\n=== LINKEDIN ===')
            await li.bring_to_front()
            try:
                await li.goto('https://www.linkedin.com/in/', wait_until='domcontentloaded', timeout=15000)
                await asyncio.sleep(4)
                
                hl = "I automate repetitive business work with AI & Python | Browser automation | Document workflows"
                r = await js_fill(li, 'input[name="headline"]', hl)
                print(f'  Headline: {"OK" if r else "FAIL"}')
                
                # Check what page we're on now
                print(f'  URL: {li.url}')
            except Exception as e:
                print(f'  Error: {e}')
        else:
            print('\n=== LINKEDIN: Skip (no tab) ===')
        
        # FIVERR
        fiv = next((pg for pg in ctx.pages if 'fiverr.com' in pg.url and 'gig' not in pg.url), None)
        if fiv:
            print('\n=== FIVERR ===')
            await fiv.bring_to_front()
            try:
                await fiv.goto('https://www.fiverr.com/users/yasaka_h/edit', wait_until='domcontentloaded', timeout=15000)
                await asyncio.sleep(4)
                
                desc = "I automate repetitive business work using AI and Python. Specializing in browser automation, document processing, lead management, and chatbots."
                r = await js_set_textarea(fiv, desc)
                print(f'  Description: {"OK" if r else "FAIL"}')
                print(f'  URL: {fiv.url}')
            except Exception as e:
                print(f'  Error: {e}')
        else:
            print('\n=== FIVERR: Skip (no tab) ===')
        
        # INSTAMOJO
        inst = next((pg for pg in ctx.pages if 'instamojo.com' in pg.url), None)
        if inst:
            print('\n=== INSTAMOJO ===')
            await inst.bring_to_front()
            await asyncio.sleep(2)
            try:
                r = await js_fill(inst, 'input[name="business_name"]', 'Yasaka Automation')
                print(f'  Business name: {"OK" if r else "FAIL"}')
            except Exception as e:
                print(f'  Error: {e}')
        else:
            print('\n=== INSTAMOJO: Skip (no tab) ===')
        
        print('\n[DONE]')

asyncio.run(main())
