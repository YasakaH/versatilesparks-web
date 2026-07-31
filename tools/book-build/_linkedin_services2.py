"""
Add Operations > Strategic Planning on LinkedIn services page.
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
        print(f'URL: {li.url}')
        
        # Check current page state
        text = await li.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Page text: {text[:500]}')
        
        # Check what's visible
        info = await li.evaluate("""() => {
            const els = document.querySelectorAll('input, select, button, [role="combobox"], [role="listbox"]');
            const r = [];
            els.forEach(el => {
                if (el.offsetParent !== null) {
                    const t = el.textContent?.trim() || el.placeholder || el.getAttribute('aria-label') || el.name || el.id || el.tagName;
                    r.push(t.substring(0, 60));
                }
            });
            return r;
        }""")
        print(f'Visible elements: {info}')
        
        # Try to navigate to the correct services page
        service_urls = [
            'https://www.linkedin.com/in/edit/forms/services/',
            'https://www.linkedin.com/in/yasaka-hanini-293150422/edit/services/',
            'https://www.linkedin.com/in/yasaka-hanini-293150422/details/services/'
        ]
        
        for url in service_urls:
            print(f'\nTrying: {url}')
            try:
                await li.goto(url, wait_until='domcontentloaded', timeout=10000)
                await asyncio.sleep(3)
                print(f'  -> {li.url}')
                t = await li.evaluate('document.body.innerText.substring(0, 300)')
                print(f'  Text: {t[:200]}')
            except:
                print('  Failed')

asyncio.run(main())
