"""
Execute deep research debate - first input with ALL research.
Uses evaluate() with arguments (no f-string escaping issues).
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

FIRST_MSG = """I did deep market research and found TWO datasets:

## DATASET 1: Pain Points — 8 domains with missing solutions

## DATASET 2: Proven Winning Products — Real earnings data

### Gumroad ($206M tracked, 146K products)
- Software Development: $65.8M total, $60,814/product
- Writing & Publishing: $15,750/product, only 226 products
- Top product: AI Photoshop Script — $586K ($50)
- Digital downloads = 85% of catalog, 293 avg sales

### Etsy Top Sellers
- Wedding invitations ($15-50), wall art ($3-25), planners ($5-30)
- Business templates ($10-40), SVG cut files ($3-20)

### Notion Templates
- Thomas Frank: $1M, Easlo: $239K, mid-tier: $500-5K/mo

## My Situation
- Python + AI/automation, FreeLLMAPI (free AI), Instamojo + Gumroad
- Zero audience, zero website, can build in 3-5 days

Which domain's pain points + proven products overlap best with my skills?"""

FILL_JS = """(msg) => {
    const ta = document.querySelector('#prompt-textarea');
    if (!ta) return 'NO_TEXTAREA';
    ta.focus();
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    setter.call(ta, msg);
    ta.dispatchEvent(new Event('input', {bubbles:true}));
    ta.dispatchEvent(new Event('change', {bubbles:true}));
    return 'FILLED';
}"""

SEND_JS = """() => {
    const btn = document.querySelector('[data-testid="send-button"]');
    if (btn && !btn.disabled) { btn.click(); return 'CLICKED'; }
    return 'NO_BTN';
}"""

GET_LAST_JS = """() => {
    const m = document.querySelectorAll('[data-message-author-role="assistant"]');
    const last = m[m.length - 1];
    return last ? last.innerText : '';
}"""

GET_COUNT_JS = """() => {
    return document.querySelectorAll('[data-message-author-role="assistant"]').length;
}"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                count = await pg.evaluate(GET_COUNT_JS)
                print(f'Messages: {count}')
                
                result = await pg.evaluate(FILL_JS, FIRST_MSG)
                print(f'Fill: {result}')
                await asyncio.sleep(2)
                
                send = await pg.evaluate(SEND_JS)
                print(f'Send: {send}')
                
                prev = count
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate(GET_COUNT_JS)
                    if cur > prev:
                        await asyncio.sleep(15)
                        full = await pg.evaluate(GET_LAST_JS)
                        print(f'\n=== FIRST RESPONSE ({len(full)} chars) ===')
                        print(full[:600])
                        
                        # IMMEDIATELY challenge
                        # Build challenge from what ChatGPT actually said
                        first_line = full[:100].split('\n')[0] if full else ''
                        challenge = f"I challenge your suggestion. You said roughly: '{first_line}...'. But my pain point data across 8 domains shows that trades/contractors have the most UNPAID willingness to pay. And the winning products data shows software development tools earn 60K+ per product. Why do you recommend against focusing there? Explain your reasoning."
                        
                        c2 = await pg.evaluate(FILL_JS, challenge)
                        print(f'Challenge fill: {c2}')
                        await asyncio.sleep(2)
                        s2 = await pg.evaluate(SEND_JS)
                        print(f'Challenge send: {s2}')
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
