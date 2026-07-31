"""Direct send - skip page iteration, target known lightweight page ID"""
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
        pages = ctx.pages
        
        # Use the SECOND page (index 1) which is likely the lighter CORE Docs page
        # (page 0 = 20K chars, page 1 = 42K chars based on previous output)
        # Actually let's try the FIRST one that's likely lighter
        target = None
        for pg in pages[:2]:  # Only check first 2 pages
            try:
                url = pg.url
                if '6a532496' in url:
                    target = pg
                    break
            except:
                continue
        
        if not target:
            # Just use first page
            target = pages[0]
        
        title = await target.evaluate('document.title')
        print(f'Using: {title}', flush=True)
        
        # Wait a moment then send
        await asyncio.sleep(3)
        
        result = await target.evaluate('''(text) => {
            const ta = document.querySelector('#prompt-textarea');
            if (!ta) return 'NO_TEXTAREA';
            
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(ta, text);
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            
            const btn = document.querySelector('[data-testid="send-button"]');
            if (btn && !btn.disabled) {
                btn.click();
                return 'SENT_BTN';
            }
            return 'NO_BUTTON';
        }''', DEBATE)
        
        print(f'Result: {result}', flush=True)

asyncio.run(main())
