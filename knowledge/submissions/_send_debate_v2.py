"""Target specific lightweight page to send debate"""
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
        print(f'Total pages: {len(pages)}', flush=True)
        
        # Find lightest CORE Docs page
        target = None
        min_chars = float('inf')
        for pg in pages:
            try:
                url = pg.url
                if '6a532496' not in url and 'chatgpt.com' not in url:
                    continue
                content_len = len(await pg.evaluate('document.body?.innerText || ""'))
                title = await pg.evaluate('document.title')
                print(f'  {content_len:>6} chars - {title}', flush=True)
                if content_len < min_chars and content_len > 1000:
                    min_chars = content_len
                    target = pg
            except Exception as e:
                print(f'  Error: {e}', flush=True)
        
        if not target:
            print('❌ No ChatGPT page found', flush=True)
            return
        
        print(f'✅ Using page with {min_chars} chars', flush=True)
        
        # Send message via native input value setter
        result = await target.evaluate('''(text) => {
            const ta = document.querySelector('#prompt-textarea');
            if (!ta) return 'NO_TEXTAREA';
            
            // Native value setter to trigger React state
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(ta, text);
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            
            // Send
            const btn = document.querySelector('[data-testid="send-button"]');
            if (btn && !btn.disabled) {
                btn.click();
                return 'SENT';
            }
            // Fallback
            ta.dispatchEvent(new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', ctrlKey: true, bubbles: true
            }));
            return 'KEYBOARD';
        }''', DEBATE)
        
        print(f'Result: {result}', flush=True)

asyncio.run(main())
