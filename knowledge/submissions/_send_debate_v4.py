"""Fix React input value setting"""
import asyncio
from playwright.async_api import async_playwright

DEBATE = '''I have read all 71 of your responses. Strong analysis. Now I want to challenge several recommendations before implementing.

**1. 22+ CORE docs is too many.** Navigation overhead, context bloat, maintenance debt. 12-15 well-structured docs is the right max. Which recs need new files vs. sections in existing ones?

**2. 40/30/20/10 routing formula is false precision.** Real routing depends on task type + user preference. Simple rules (security->Security Architect) are more predictable. When is scoring actually necessary?

**3. Complexity L0-L3 - does every task need classification?** Most queries are simple (L0). Rare complex ones have clear signals. Is classification engineering theater?

**4. Execution DAG over-engineers 80% of tasks.** Excellent for multi-step projects. Token waste for single questions. Where's the line?

**5. Memory governance - Chief of Staff or separate meta-personality?** Memory is cross-cutting. Should it be a Memory Curator?

**6. 33-field schema - define minimal required set (10-12 fields) + optional extensions?**

**7. 6-level escalation for single-developer setup - configurable depth?**

Challenge my positions.'''

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9229', timeout=15000)
        target = (await browser.contexts[0].pages)[1]  # page 1 (42K chars page)
        
        title = await target.evaluate('document.title')
        print(f'Using page: {title}', flush=True)
        await asyncio.sleep(2)
        
        # Use keyboard to type the debate message
        ta = await target.wait_for_selector('#prompt-textarea', timeout=15000)
        await ta.click()
        await asyncio.sleep(0.5)
        
        # Type in chunks
        for i in range(0, len(DEBATE), 500):
            chunk = DEBATE[i:i+500]
            await ta.type(chunk, delay=1)
        
        await asyncio.sleep(2)
        
        # Click send button
        send_btn = await target.query_selector('[data-testid="send-button"]')
        if send_btn:
            disabled = await send_btn.get_attribute('disabled')
            if not disabled:
                await send_btn.click()
                print('Sent via button click', flush=True)
            else:
                await target.keyboard.press('Control+Enter')
                print('Sent via keyboard', flush=True)
        else:
            await target.keyboard.press('Control+Enter')
            print('Sent via keyboard (no button)', flush=True)

asyncio.run(main())
