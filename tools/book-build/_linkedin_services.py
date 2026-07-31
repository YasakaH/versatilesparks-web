"""
Add Operations > Strategic Planning service on LinkedIn.
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
            print('No LinkedIn tab found')
            return
        
        await li.bring_to_front()
        print(f'LinkedIn URL: {li.url}')
        
        # Navigate to services section
        print('Navigating to services editor...')
        try:
            await li.goto('https://www.linkedin.com/in/edit/forms/services/', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
        except:
            print('Navigation failed, trying alternative URL')
            await li.goto('https://www.linkedin.com/in/edit/intro/', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
        
        print(f'URL after nav: {li.url}')
        text = await li.evaluate('document.body.innerText')
        print(f'Page text (first 500): {text[:500]}')
        
        # Check if we're on the right page
        if 'service' not in text.lower():
            print('Services section not accessible directly. Trying to add via profile...')
            # Try going to profile and finding services
            await li.goto('https://www.linkedin.com/in/', wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(4)
            print(f'Profile URL: {li.url}')
            
            # Try clicking "Add service" button
            clicked = await li.evaluate("""() => {
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                for (const btn of buttons) {
                    const t = btn.textContent.toLowerCase();
                    if (t.includes('service') || t.includes('add profile')) {
                        btn.click();
                        return 'Clicked: ' + btn.textContent.trim();
                    }
                }
                return 'No matching button found';
            }""")
            print(f'Button click: {clicked}')
            await asyncio.sleep(3)
            
            # Look for service section in the edit popup
            result = await li.evaluate("""() => {
                const inputs = document.querySelectorAll('input, select, textarea');
                const info = [];
                inputs.forEach(el => {
                    const label = el.placeholder || el.name || el.id || el.getAttribute('aria-label') || '';
                    info.push(label.substring(0, 50));
                });
                return info.filter(s => s.length > 0).slice(0, 30);
            }""")
            print(f'Form fields: {result}')

asyncio.run(main())
