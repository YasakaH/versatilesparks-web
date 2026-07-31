"""Send debate via brand new tab"""
import asyncio
from playwright.async_api import async_playwright

DEBATE = '''I have read all 71 of your responses. Strong analysis. Now I want to challenge several recommendations before implementing.

**1. 22+ CORE docs is too many.** Navigation overhead, context bloat, maintenance debt. 12-15 well-structured docs is the right max. Which recs need new files vs. sections in existing ones?

**2. 40/30/20/10 routing formula is false precision.** Real routing depends on task type + user preference. Simple rules (security→Security Architect) are more predictable. When is scoring actually necessary?

**3. Complexity L0-L3 — does every task need classification?** Most queries are simple (L0). Rare complex ones have clear signals. Is classification engineering theater?

**4. Execution DAG over-engineers 80% of tasks.** Excellent for multi-step projects. Token waste for single questions. Where's the line?

**5. Memory governance — Chief of Staff or separate meta-personality?** Memory is cross-cutting. Should it be a Memory Curator?

**6. 33-field schema — define minimal required set (10-12 fields) + optional extensions?**

**7. 6-level escalation for single-developer setup — configurable depth?**

Challenge my positions.'''

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9229', timeout=15000)
        ctx = browser.contexts[0]
        
        # Open a fresh page
        page = await ctx.new_page()
        await page.goto('https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7', wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(5)
        
        print(f'Page: {await page.evaluate("document.title")}', flush=True)
        
        # Wait for textarea
        await page.wait_for_selector('#prompt-textarea', timeout=20000)
        
        # Focus
        await page.evaluate('document.querySelector("#prompt-textarea").focus()')
        await asyncio.sleep(1)
        
        # Type the debate
        await page.keyboard.type(DEBATE, delay=1)
        await asyncio.sleep(2)
        
        # Try send button
        sent = await page.evaluate('''() => {
            const btn = document.querySelector('[data-testid="send-button"]');
            if (btn && !btn.disabled) { btn.click(); return true; }
            return false;
        }''')
        
        if not sent:
            await page.keyboard.press('Control+Enter')
        
        print(f'✅ Sent! ({len(DEBATE)} chars)', flush=True)

asyncio.run(main())
