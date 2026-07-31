"""
Add Operations > Strategic Planning service WITH DESCRIPTION on LinkedIn.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

SERVICE_DESC = """I help businesses eliminate repetitive work and optimize operations using AI and Python automation. This includes browser automation, document processing workflows, lead management systems, and custom automation solutions that save hours of manual work every week. Each solution is tailored to the specific needs of the business, focusing on practical outcomes rather than technology for its own sake."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        li = None
        for pg in ctx.pages:
            if 'linkedin.com/in/yasaka' in pg.url:
                li = pg
                break
        
        if not li:
            for pg in ctx.pages:
                if 'linkedin.com' in pg.url:
                    li = pg
                    break
        
        if not li:
            print('No LinkedIn tab')
            return
        
        await li.bring_to_front()
        
        # Navigate to profile services page
        await li.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/details/services/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(3)
        print(f'URL: {li.url}')
        
        # Check what's on the page
        text = await li.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'Text: {text[:500]}')
        
        # Try going to the add service page
        await li.goto('https://www.linkedin.com/in/yasaka-hanini-293150422/opportunities/services/education/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Services URL: {li.url}')
        
        # Click the "Showcase your services" option
        await li.evaluate("""() => {
            const all = document.querySelectorAll('[data-view-name="service-education"], [class*="service"], section, article, div[role="button"]');
            for (const el of all) {
                const t = el.textContent.toLowerCase();
                if ((t.includes('showcase') || t.includes('service')) && el.offsetParent !== null) {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        await asyncio.sleep(3)
        
        # Now the next page should have search field + continue
        # Fill search with Operations
        try:
            await li.fill('input[placeholder="Search"]', 'Operations')
            await asyncio.sleep(2)
            print('Filled Operations in search')
        except:
            print('Could not find search field')
        
        # Check current state
        text2 = await li.evaluate('document.body.innerText.substring(0, 1000)')
        print(f'After fill: {text2[:500]}')
        
        # Look for the search results or category selection
        categories = await li.evaluate("""() => {
            const items = document.querySelectorAll('[role="option"], [role="radio"], [class*="option"], li, [data-test*="option"]');
            const r = [];
            items.forEach(el => {
                if (el.offsetParent !== null) r.push(el.textContent.trim().substring(0, 60));
            });
            return r.slice(0, 15);
        }""")
        print(f'Options: {categories}')

asyncio.run(main())
