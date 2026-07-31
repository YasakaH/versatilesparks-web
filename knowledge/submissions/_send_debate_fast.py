"""Fast debate message via CDP direct eval - no Playwright waits"""
import asyncio, json, sys
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
        browser = await p.chromium.connect_over_cdp('http://localhost:9229', timeout=30000)
        ctx = browser.contexts[0]
        
        # Find ChatGPT page
        target = None
        for pg in ctx.pages:
            if '6a532496' in pg.url:
                target = pg
                break
        if not target:
            target = await ctx.new_page()
            await target.goto('https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7', wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(8)
        
        print(f'Page: {await target.evaluate("document.title")}', flush=True)
        
        # Find textarea via JS evaluation - faster than selectors
        has_ta = await target.evaluate('!!document.querySelector("#prompt-textarea")')
        if not has_ta:
            print('❌ No textarea found', flush=True)
            sys.exit(1)
        
        # Focus and fill via JS
        await target.evaluate('''() => {
            const ta = document.querySelector('#prompt-textarea');
            ta.focus();
            ta.value = '';
        }''')
        await asyncio.sleep(1)
        
        # Type via keyboard
        await target.keyboard.type(DEBATE, delay=2)
        await asyncio.sleep(2)
        
        # Send via JS
        sent = await target.evaluate('''() => {
            const btn = document.querySelector('[data-testid=\"send-button\"]');
            if (btn && !btn.disabled) { btn.click(); return 'clicked'; }
            return 'no_button';
        }''')
        print(f'Send: {sent}', flush=True)
        
        if sent == 'no_button':
            await target.keyboard.press('Control+Enter')
            print('Sent via keyboard', flush=True)
        
        print(f'✅ Sent {len(DEBATE)} chars', flush=True)

asyncio.run(main())
