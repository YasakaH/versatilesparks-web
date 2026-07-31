"""
Add Operations > Strategic Planning service on LinkedIn.
Already on the profile page, needs to interact with the Add Services popup.
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
            if 'linkedin' in pg.url and 'yasaka' in pg.url:
                li = pg
                break
        
        if not li:
            print('No LinkedIn profile tab found')
            return
        
        await li.bring_to_front()
        print(f'Profile URL: {li.url}')
        
        # Click "Add services" button
        await li.evaluate("""() => {
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            for (const btn of buttons) {
                const t = btn.textContent.toLowerCase();
                if (t.includes('add services') || t.includes('showcase your services')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        }""")
        print('Clicked Add services')
        await asyncio.sleep(3)
        
        # Now the popup should be open. Find and fill the search field
        # First check what's visible
        result = await li.evaluate("""() => {
            const inputs = document.querySelectorAll('input, select, textarea');
            const info = [];
            inputs.forEach(el => {
                if (el.offsetParent !== null) {  // visible
                    info.push({
                        tag: el.tagName,
                        type: el.type || '',
                        placeholder: el.placeholder || '',
                        name: el.name || '',
                        id: el.id || '',
                        label: el.getAttribute('aria-label') || '',
                        value: el.value || ''
                    });
                }
            });
            return info;
        }""")
        print(f'Visible inputs: {len(result)}')
        for r in result:
            print(f'  {r["tag"]} | placeholder="{r["placeholder"]}" | name="{r["name"]}" | label="{r["label"]}"')
        
        # Also check for dialogs/modals
        modals = await li.evaluate("""() => {
            const dialogs = document.querySelectorAll('[role="dialog"], [role="alertdialog"], .artdeco-modal, [data-test-modal]');
            return dialogs.length;
        }""")
        print(f'Dialogs open: {modals}')
        
        if result:
            # Try to fill the search field
            for r in result:
                if 'search' in r['placeholder'].lower() or 'search' in r['label'].lower() or 'search' in r['name'].lower():
                    sel = f'input[name="{r["name"]}"]' if r['name'] else f'input[placeholder="{r["placeholder"]}"]'
                    await li.fill(sel, 'Operations')
                    await asyncio.sleep(1)
                    await li.keyboard.press('Enter')
                    await asyncio.sleep(2)
                    print(f'Filled search with "Operations"')
                    break
        
        # Try alternative: search for "Strategic Planning" directly
        print('Trying to type "Strategic Planning"...')
        await li.keyboard.press('Tab')
        await asyncio.sleep(0.5)
        await li.keyboard.type('Strategic Planning')
        await asyncio.sleep(1)
        await li.keyboard.press('Enter')
        await asyncio.sleep(2)

asyncio.run(main())
