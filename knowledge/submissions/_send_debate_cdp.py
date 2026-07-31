"""Target the freshly loaded page via CDP websocket"""
import asyncio, json, requests
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
        
        # Find the page with just "ChatGPT" title (lightweight new load)
        pages = ctx.pages
        print(f'Total pages: {len(pages)}', flush=True)
        
        target = None
        for pg in pages:
            try:
                title = await pg.evaluate('document.title')
                url = pg.url
                print(f'  [{len(await pg.evaluate("document.body.innerText"))} chars] {title[:40]}', flush=True)
                if 'ChatGPT' == title or 'CORE Docs' in title:
                    target = pg
            except:
                continue
        
        if not target:
            target = pages[0]
        
        print(f'Using: {await target.evaluate("document.title")}', flush=True)
        
        # Simple direct approach - inject a script that fills textarea
        result = await target.evaluate('''(debateText) => {
            const ta = document.querySelector('#prompt-textarea');
            if (!ta) return 'NO_TEXTAREA';
            
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(ta, debateText);
            
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Try clicking send
            const btn = document.querySelector('[data-testid="send-button"]');
            if (btn && !btn.disabled) {
                btn.click();
                return 'SENT_BTN';
            }
            
            // Fallback: Enter key
            ta.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', ctrlKey: true, bubbles: true}));
            return 'SENT_KEYBOARD';
        }''', DEBATE)
        
        print(f'Result: {result}', flush=True)

asyncio.run(main())
