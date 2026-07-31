"""
Add digital product on Instamojo.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9235

PRODUCT_NAME = "AI Business Toolkit: 50 Prompts for Indian Businesses"
PRODUCT_PRICE = "499"
PRODUCT_DESC = """Stop wasting hours writing content from scratch. Get AI-powered business outputs in seconds.

This is a complete collection of 50 battle-tested AI prompts designed specifically for Indian small businesses, freelancers, entrepreneurs, and solopreneurs.

Categories include: Marketing & Social Media (8 prompts), Customer Service (6 prompts), Sales & Proposals (5 prompts), Operations & Productivity (6 prompts), Finance & Accounting (4 prompts), Product Descriptions (5 prompts), Email & Communication (5 prompts), Business Strategy (4 prompts), Content Creation (3 prompts), and HR & Recruitment (4 prompts).

India-Specific: Designed for Indian context (Hinglish, UPI, festivals).
Ready in Seconds: Copy, paste, get output.
Works with FREE AI tools: ChatGPT, Gemini, Claude, FreeLLMAPI.
Lifetime Updates Included.

Price: Rs 499 (One-time payment, instant download)"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        dash = None
        for pg in ctx.pages:
            if 'instamojo' in pg.url.lower():
                dash = pg
                break
        
        if not dash:
            print('No Instamojo tab')
            return
        
        await dash.bring_to_front()
        await dash.goto('https://manage.instamojo.com/dashboard/products/types', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(4)
        
        # Click "Digital File"
        await dash.evaluate("""() => {
            const all = document.querySelectorAll('a, button, div[role="button"], span');
            for (const el of all) {
                if (el.textContent.trim().includes('Digital File') && el.offsetParent !== null) {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        await asyncio.sleep(5)
        print(f'URL: {dash.url[:100]}')
        text = await dash.evaluate('document.body.innerText.substring(0, 600)')
        print(f'Digital product page: {text[:400]}')
        
        # Fill product form
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
