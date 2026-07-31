"""Send debate to fresh ChatGPT session"""
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

Challenge my positions. Not looking for agreement.'''

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9229', timeout=15000)
        ctx = browser.contexts[0]
        target = None
        for pg in ctx.pages:
            if '6a532496' in pg.url:
                target = pg
                break
        if not target:
            print('❌ Page not found', flush=True)
            return
        
        await asyncio.sleep(3)
        ta = await target.wait_for_selector('#prompt-textarea', timeout=20000)
        await ta.click()
        await asyncio.sleep(0.5)
        
        # Use fill instead of type - much faster
        await ta.fill(DEBATE)
        
        await asyncio.sleep(2)
        
        btn = await target.query_selector('[data-testid="send-button"]')
        if btn:
            disabled = await btn.get_attribute('disabled')
            if not disabled:
                await btn.click()
                print('✅ Sent via button', flush=True)
                return
        
        await target.keyboard.press('Control+Enter')
        print('✅ Sent via keyboard', flush=True)

asyncio.run(main())
