"""
Adaptive debate loop - continues until ChatGPT gives a clear go-ahead.
Introduces new ideas/tools as the debate evolves.
"""
import asyncio, json, os, random
from playwright.async_api import async_playwright

CDP_PORT = 9230
CONV_FILE = r'C:\Users\varas\personalities\_deep_research_conversation.json'

# New angles to introduce during debate when needed
NEW_ANGLES = [
    # Angle: What about using FreeLLMAPI as an advantage?
    "What if I use FreeLLMAPI as my pricing moat? Most similar tools charge $10-20/month because they pay OpenAI API costs. I have 62 free models. I can charge $29 ONE-TIME and never have recurring costs. That's a pricing advantage no competitor can match. Does this change the product recommendation?",
    
    # Angle: n8n workflow templates instead of standalone tool
    "What about selling n8n workflow templates instead? I know n8n well. Pre-built, importable workflow templates that do specific jobs — affiliate link checking, CSV processing, etc. Templates sell on Gumroad as digital downloads (85% of catalog). No desktop app complexity, instant delivery, easier to build. Is this better than a Python desktop tool?",
    
    # Angle: Bundle approach
    "What if I bundle 3 small tools together for $49? Affiliate Link Checker + CSV Cleaner + Folder Organizer. A 'Productivity Toolbox' for freelancers. Higher perceived value, less competition for a bundle vs a single tool. Or is focus better?",
    
    # Angle: nodriver for browser automation product
    "I have nodriver installed — undetected browser automation. What if I build a 'Browser Automation Blueprint' — a ready-to-run Python script pack that automates common web tasks? Downloads files, fills forms, scrapes data. Target: non-technical business owners who want automation but can't code. Price: $49. Does this beat the affiliate tool idea?",
    
    # Angle: Two-sided marketplace approach
    "What if instead of selling TO contractors, I build a tool that connects contractors with customers? Like a quote generator that also sends the quote AND follows up automatically via SMS. A local service tool. More complex but higher value. Thoughts?",
    
    # Angle: Challenge response with counter-data
    "I keep hearing you recommend tools, but the real money on Gumroad is in the 'Other' category - $88,048 per product. These are unusual high-ticket items that don't fit labels. Should I be thinking about a HIGH-priced product ($197-497) that solves a very specific problem for a tiny audience, rather than a $39 product for a broad audience?",
]

async def get_count(page):
    return await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')

async def get_last_response(page):
    return await page.evaluate("""() => {
        const m = document.querySelectorAll('[data-message-author-role="assistant"]');
        return m[m.length-1]?.innerText || '';
    }""")

async def send_and_detect(page, msg, prev_count=None):
    if prev_count is None:
        prev_count = await get_count(page)
    
    ta = await page.wait_for_selector('#prompt-textarea', timeout=30000)
    await ta.click()
    await asyncio.sleep(0.5)
    await ta.fill(msg)
    await asyncio.sleep(1.5)
    
    btn = await page.query_selector('[data-testid="send-button"]')
    if btn and not await btn.get_attribute('disabled'):
        await btn.click()
    else:
        await page.keyboard.press('Control+Enter')
    
    for i in range(120):
        await asyncio.sleep(5)
        cur = await get_count(page)
        if cur > prev_count:
            await asyncio.sleep(10)
            return await get_last_response(page)
        if i % 12 == 0:
            print(f'  Wait ({i*5}s)')
    return None

def has_go_ahead(text):
    """Check if ChatGPT gave a definitive go-ahead."""
    signals = [
        'build this', 'start building', 'go ahead', 'i would build',
        'here is what i would do', 'my recommendation is', 'build it',
        'starting tomorrow', 'this is the one', 'i would start with',
        'the product i would build', 'this is what i recommend',
        'definitive answer', 'one product', 'here is your answer'
    ]
    lower = text.lower()
    for s in signals:
        if s in lower:
            return True
    return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                page = pg
                break
        if not page:
            page = ctx.pages[0]
        
        count = await get_count(page)
        print(f'Starting from {count} assistant messages')
        
        round_num = 4  # Continue from where we left off
        used_angles = set()
        
        while True:
            # Get the last response
            last = await get_last_response(page)
            print(f'\n{"="*60}')
            print(f'ROUND {round_num} — Current response ({len(last)} chars)')
            print(f'{"="*60}')
            print(last[:500])
            
            # Check if ChatGPT already gave a go-ahead
            if has_go_ahead(last):
                print('\n>>> Go-ahead detected! Verifying it\'s decisive enough...')
                # Check if it gives a specific product name and price
                if '$' in last and any(word in last.lower() for word in ['gumroad', 'product', 'tool', 'app']):
                    print('\n*** DEFINITIVE GO-AHEAD ***')
                    print('ChatGPT gave a specific recommendation with price and platform.')
                    print('Saving final conversation...')
                    break
            
            # Build a responsive challenge based on what was said
            lower = last.lower()
            
            if 'affiliate' in lower and ('link' in lower or 'check' in lower):
                # It's talking about the affiliate tool — introduce a new angle
                if round_num >= 5:
                    # Try introducing FreeLLMAPI pricing moat
                    chosen = NEW_ANGLES[0]
                    print(f'\nIntroducing new angle: FreeLLMAPI pricing moat')
                else:
                    chosen = "I like the affiliate tool idea but let me push back on price. You said $39. But the top Gumroad products are priced at $50 (the $586K AI script). Why $39 and not $50? And what about a FREE version that checks 10 links, then $49 for unlimited? Would that sell better?"
                    print(f'\nChallenging price point...')
                    
            elif 'contractor' in lower or 'quote' in lower or 'estimator' in lower:
                # It's talking about contractor tool — challenge with affiliate angle
                print(f'\nIntroducing affiliate tool as alternative...')
                chosen = "Interesting, but I also found that affiliate marketers CONSTANTLY complain about broken links and lost commissions. And I actually built a small prototype of an affiliate link checker using FreeLLMAPI — it works with zero API costs. Should I pivot to that instead? It's a smaller build, easier to sell, and I have data showing affiliate marketers search for this daily."
                
            elif 'audience' in lower or 'discovery' in lower or 'reach' in lower:
                # It's talking about distribution — introduce a specific strategy
                chosen = "What about this specific distribution strategy: I build a FREE version first. Free checks 10 links. Paid checks unlimited at $49. I post the free version on GitHub as an open-source tool. The README mentions the paid version on Gumroad. GitHub stars → organic search → Gumroad. Has this worked for similar tools?"
                print(f'\nIntroducing GitHub distribution strategy...')
                
            else:
                # General push
                chosen = random.choice(NEW_ANGLES)
                print(f'\nIntroducing new angle: {chosen[:60]}...')
            
            # Send challenge
            prev_count = await get_count(page)
            response = await send_and_detect(page, chosen, prev_count)
            if not response:
                print('No response received. Page might be stuck.')
                break
            
            round_num += 1
        
        # Save final conversation
        all_msgs = await page.evaluate("""() => {
            const m = document.querySelectorAll('[data-message-author-role]');
            return Array.from(m).map(x => ({role: x.getAttribute('data-message-author-role'), text: x.innerText}));
        }""")
        with open(CONV_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_msgs, f, indent=2)
        print(f'\nSaved {len(all_msgs)} messages to {CONV_FILE}')
        
        print(f'\n{"="*60}')
        final = await get_last_response(page)
        print('FINAL ANSWER:')
        print(final)
        print(f'\nBrowser stays open. Close when done.')
        
        while True:
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
