"""
Use sidebar navigation to set up Instamojo store (no direct URL navigation).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def click_sidebar(page, parent_label, child_label):
    """Click a sidebar menu item. First click parent to expand, then child."""
    # Click parent
    await page.evaluate(f"""() => {{
        const all = document.querySelectorAll('a, span, div, button, li');
        for (const el of all) {{
            if (el.textContent.trim() === '{parent_label}' && el.offsetParent !== null) {{
                el.click();
                return true;
            }}
        }}
        return false;
    }}""")
    await asyncio.sleep(1)
    # Click child
    return await page.evaluate(f"""() => {{
        const all = document.querySelectorAll('a, span, div, button, li');
        for (const el of all) {{
            if (el.textContent.trim() === '{child_label}' && el.offsetParent !== null) {{
                el.click();
                return true;
            }}
        }}
        return false;
    }}""")

async def fill_field(page, selector, value):
    try:
        el = await page.wait_for_selector(selector, timeout=5000)
        await el.click()
        await asyncio.sleep(0.2)
        await el.fill('')
        await el.fill(value)
        return True
    except:
        return False

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
            # Find any instamojo tab
            for pg in ctx.pages:
                if 'instamojo' in pg.url.lower():
                    dash = pg
                    break
        
        if not dash:
            print('No Instamojo tab')
            return
        
        await dash.bring_to_front()
        await dash.goto('https://www.instamojo.com/dashboard/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Dashboard: {dash.url[:80]}')
        
        # Navigate: Store > Profile
        ok = await click_sidebar(dash, 'Store', 'Profile')
        print(f'Store > Profile: {"OK" if ok else "FAIL"}')
        await asyncio.sleep(4)
        print(f'URL: {dash.url[:100]}')
        
        text = await dash.evaluate('document.body.innerText.substring(0, 800)')
        print(f'Profile page: {text[:500]}')
        
        # Try to find and fill form fields
        inputs = await dash.evaluate("""() => {
            const r = [];
            document.querySelectorAll('input').forEach(el => {
                if (el.offsetParent !== null) {
                    const label = document.querySelector(`[for="${el.id}"]`);
                    r.push({
                        id: el.id.substring(0, 30),
                        name: (el.name || '').substring(0, 30),
                        placeholder: (el.placeholder || '').substring(0, 40),
                        value: (el.value || '').substring(0, 40),
                        label: label ? label.textContent.trim().substring(0, 40) : ''
                    });
                }
            });
            return r;
        }""")
        print(f'Inputs:')
        for inp in inputs:
            print(f'  id="{inp["id"]}" name="{inp["name"]}" placeholder="{inp["placeholder"]}" value="{inp["value"]}" label="{inp["label"]}"')

asyncio.run(main())
