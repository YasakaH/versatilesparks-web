"""
Execute deep research debate using document.execCommand (bypasses Illegal invocation).
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9230

FIRST_MSG = """I did deep market research and found TWO datasets:

## DATASET 1: Pain Points across 8 business domains

## DATASET 2: Proven Winning Products - Real revenue data

### Gumroad ($206M tracked)
- Software Development: $65.8M total, $60,814/product
- Writing & Publishing: $15,750/product, 226 products only
- Top product: AI Photoshop Script - $586K ($50, 11,725 sales)
- Digital downloads = 85% of catalog

### Etsy
- Wedding invitations ($15-50), planners ($5-30), wall art ($3-25)
- Business templates ($10-40), SVG cut files ($3-20)

### Notion Templates
- Thomas Frank: $1M, Easlo: $239K, mid: $500-5K/mo

### My situation
- Python + AI/automation, FreeLLMAPI (free AI)
- Instamojo (India), Gumroad ready (global)
- Zero audience, zero website
- Build in 3-5 days

Which domain's pain points + proven products overlap best with me?"""

FILL_CMD = """(msg) => {
    const ta = document.querySelector('#prompt-textarea');
    if (!ta) return 'NO_TA';
    ta.focus();
    ta.value = msg;
    ta.dispatchEvent(new Event('input', {bubbles:true}));
    ta.dispatchEvent(new Event('change', {bubbles:true}));
    return 'OK';
}"""

SEND_CMD = """() => {
    const btn = document.querySelector('[data-testid="send-button"]');
    if (btn && !btn.disabled) { btn.click(); return 'OK'; }
    return 'NO_BTN';
}"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                count = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'Messages: {count}')
                
                # Fill using direct value set (not native setter)
                r = await pg.evaluate(FILL_CMD, FIRST_MSG)
                print(f'Fill: {r}')
                await asyncio.sleep(2)
                
                # Send
                s = await pg.evaluate(SEND_CMD)
                print(f'Send: {s}')
                if s == 'NO_BTN':
                    await pg.keyboard.press('Control+Enter')
                    print('Used Ctrl+Enter')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(15)
                        full = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return m[m.length-1]?.innerText || '';
                        }""")
                        print(f'\n=== RESPONSE ({len(full)} chars) ===')
                        print(full[:500])
                        
                        # IMMEDIATELY challenge based on actual response
                        first_sentence = full[:150].split('\n')[0] if full else ''
                        challenge = f"I disagree with your suggestion. You said '{first_sentence}'. I think you're missing that trades/contractors have the highest willingness to pay and lowest competition. Why not start there? Explain."
                        
                        c2 = await pg.evaluate(FILL_CMD, challenge)
                        print(f'Challenge fill: {c2}')
                        await asyncio.sleep(2)
                        s2 = await pg.evaluate(SEND_CMD)
                        print(f'Challenge send: {s2}')
                        if s2 == 'NO_BTN':
                            await pg.keyboard.press('Control+Enter')
                        break
                    if i % 12 == 0:
                        print(f'  W ({i*5}s)')
                break

asyncio.run(main())
