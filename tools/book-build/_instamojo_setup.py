"""
Set up Instamojo store with products and branding.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9235

PRODUCT_DESC = """Stop wasting hours writing content from scratch. Get AI-powered business outputs in seconds.

This is a complete collection of 50 battle-tested AI prompts designed specifically for Indian small businesses, freelancers, entrepreneurs, and solopreneurs.

📦 What You Get:
• Marketing & Social Media (8 prompts)
• Customer Service (6 prompts)
• Sales & Proposals (5 prompts)
• Operations & Productivity (6 prompts)
• Finance & Accounting (4 prompts)
• Product Descriptions (5 prompts)
• Email & Communication (5 prompts)
• Business Strategy (4 prompts)
• Content Creation (3 prompts)
• HR & Recruitment (4 prompts)

✅ India-Specific: Designed for Indian context (Hinglish, UPI, festivals)
✅ Ready in Seconds: Copy, paste, get output
✅ Works with FREE AI tools: ChatGPT, Gemini, Claude, FreeLLMAPI
✅ Lifetime Updates Included

Price: ₹499 (One-time payment, instant download)"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find Instamojo dashboard tab
        dash = None
        store = None
        for pg in ctx.pages:
            if 'instamojo.com/dashboard' in pg.url:
                dash = pg
            if 'easyautomation.stores.instamojo.com' in pg.url:
                store = pg
        
        if not dash:
            print('No Instamojo dashboard tab found')
            return
        
        await dash.bring_to_front()
        print(f'Dashboard: {dash.url}')
        
        # Go to products section
        await dash.goto('https://www.instamojo.com/dashboard/products/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        print(f'Products page: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Page: {text[:400]}')
        
        # Check if we need to create a new product
        # Look for "Create Product" or "New Product" button
        btns = await dash.evaluate("""() => {
            const all = document.querySelectorAll('button, a, [role="button"]');
            const r = [];
            all.forEach(el => {
                if (el.offsetParent !== null) {
                    r.push(el.textContent.trim().substring(0, 40));
                }
            });
            return r.filter(t => t.length > 0).slice(0, 20);
        }""")
        print(f'Buttons: {btns}')
        
        # Also check the store tab
        if store:
            await store.bring_to_front()
            await asyncio.sleep(2)
            store_text = await store.evaluate('document.body.innerText.substring(0, 800)')
            print(f'\nStore page:\n{store_text[:500]}')

asyncio.run(main())
