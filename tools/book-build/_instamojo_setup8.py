"""
Set up Instamojo - add product, store profile, etc.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

PRODUCT_DESC = """Stop wasting hours writing content from scratch. Get AI-powered business outputs in seconds.

This is a complete collection of 50 battle-tested AI prompts designed specifically for Indian small businesses, freelancers, entrepreneurs, and solopreneurs.

What You Get:
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

India-Specific: Designed for Indian context (Hinglish, UPI, festivals)
Ready in Seconds: Copy, paste, get output
Works with FREE AI tools: ChatGPT, Gemini, Claude, FreeLLMAPI
Lifetime Updates Included

Price: ₹499 (One-time payment, instant download)"""

ABOUT_STORE = """I help businesses eliminate repetitive work and optimize operations using AI and Python automation. I build practical automation solutions including browser automation, document processing, workflow automation, and custom integrations that save hours of manual work every week."""

async def click_menu_item(page, text):
    return await page.evaluate(f"""() => {{
        const items = document.querySelectorAll('a, span, div, button');
        for (const el of items) {{
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
        
        # Step 1: Go to Products > All Products
        await dash.goto('https://www.instamojo.com/dashboard/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(3)
        
        # Click Products to expand
        await click_menu_item(dash, 'Products')
        await asyncio.sleep(1)
        # Click All Products
        await click_menu_item(dash, 'All Products')
        await asyncio.sleep(4)
        print(f'Products page: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Text: {text[:400]}')
        
        # Step 2: Store Profile
        await dash.goto('https://www.instamojo.com/dashboard/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(3)
        await click_menu_item(dash, 'Store')
        await asyncio.sleep(1)
        await click_menu_item(dash, 'Profile')
        await asyncio.sleep(4)
        print(f'\nStore Profile: {dash.url[:100]}')
        text2 = await dash.evaluate('document.body.innerText.substring(0, 800)')
        print(f'Text: {text2[:500]}')

asyncio.run(main())
