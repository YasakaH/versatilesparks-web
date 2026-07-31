"""
Launch fresh Brave + ChatGPT thread for deep research debate.
User logs in once, then the automation takes over.
"""
import asyncio, subprocess, os, urllib.request, json
from playwright.async_api import async_playwright

CDP_PORT = 9230
TEMP_DIR = r'C:\Users\varas\AppData\Local\Temp\chatgpt-deep-research'
BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

FIRST_MSG = """I have two datasets from deep research and need your analysis:

## DATASET 1: Pain Points — Missing Solutions Across 8 Business Domains

I found these specific grievances from Reddit/forums:

1. Real Estate — CRMs too bloated for agents; landlords managing <10 units have no simple tool for rent reminders, maintenance, lease storage
2. Trades/Contractors — Hours wasted creating quotes; quoting tools email wrong clients; no simple estimate generator
3. Sales — CRMs track what managers want, not what reps need; reps want inbox-first workspace
4. IT/Tech Support — Helpdesk tools too complex; client onboarding painful for MSPs
5. Legal — Solo lawyers can't afford AI tools; intake still handled by phone/paper
6. E-commerce — Shopify shipping rules complex; Etsy sellers fear suspension; Airbnb turnover scheduling chaos
7. Creators/Freelancers — Affiliate links break silently; sponsorship deadlines missed; client approval/ payment chasing
8. Accounting — Tax season booking chaos; client communication scattered across email/QB/text

## DATASET 2: Proven Winning Digital Products (Real Revenue)

Gumroad ($206M tracked, 146K products):
- Software Development: $65.8M total, $60,814/product — #1 category
- Writing & Publishing: $15,750/product, only 226 products — best entry odds
- Top product: AI Photoshop Script sold $586K at $50
- Digital downloads = 85% of catalog, 293 avg sales
- Key insight: Price matters more than volume. $50 product = real revenue. $0.50 product = vanity.

Etsy best-sellers ($10-50K/month):
- Wedding invitations ($15-50), wall art ($3-25), planners ($5-30)
- Business templates ($10-40), SVG cut files ($3-20)

Notion Templates: Thomas Frank $1M, Easlo $239K, typical $500-5K/month

## My Situation
- Python, AI/automation, FreeLLMAPI (62 free models, zero API cost)
- nodriver for undetected browser automation
- Instamojo (India payments), Gumroad ready for global
- Zero audience, zero website
- Can build a tool/script in 3-5 days
- Zero budget

## The Question
Where do these two datasets overlap with my specific skills? Give me:
1. Which domain/pain point should I target FIRST?
2. What's the ONE specific product?
3. Exact name (optimized for what people search)
4. Price
5. Platform to sell on
6. How I get my first buyer with zero audience

Be specific and actionable. No theory."""

async def wait_for_login(page, timeout=300):
    """Wait for user to log in by checking for textarea."""
    for i in range(timeout):
        try:
            ta = await page.wait_for_selector('#prompt-textarea', timeout=5000)
            if ta:
                return True
        except:
            pass
        print(f'  Waiting for login... ({i}s)')
        await asyncio.sleep(1)
    return False

async def detect_new_response(page, prev_count, timeout_sec=600):
    """Wait for ChatGPT to finish responding."""
    for i in range(timeout_sec // 5):
        await asyncio.sleep(5)
        cur = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
        if cur > prev_count:
            await asyncio.sleep(10)
            text = await page.evaluate("""() => {
                const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                return m[m.length-1]?.innerText || '';
            }""")
            print(f'Response detected: {len(text)} chars')
            return text
        if i % 12 == 0:
            print(f'  Waiting for response... ({i*5}s)')
    return None

async def send_and_wait(page, msg, prev_count=None):
    """Send a message and wait for response."""
    if prev_count is None:
        prev_count = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
    
    ta = await page.wait_for_selector('#prompt-textarea', timeout=30000)
    await ta.click()
    await asyncio.sleep(1)
    await ta.fill(msg)
    await asyncio.sleep(2)
    
    btn = await page.query_selector('[data-testid="send-button"]')
    if btn and not await btn.get_attribute('disabled'):
        await btn.click()
    else:
        await page.keyboard.press('Control+Enter')
    
    return await detect_new_response(page, prev_count)

async def main():
    # Launch fresh Brave with temp profile
    os.makedirs(TEMP_DIR, exist_ok=True)
    proc = subprocess.Popen([
        BRAVE, f'--remote-debugging-port={CDP_PORT}',
        f'--user-data-dir={TEMP_DIR}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1200,800',
        'https://chat.openai.com/auth/login'
    ])
    
    # Wait for CDP endpoint
    for _ in range(30):
        try:
            urllib.request.urlopen(f'http://localhost:{CDP_PORT}/json/version')
            break
        except:
            await asyncio.sleep(1)
    
    await asyncio.sleep(5)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        
        print('\n' + '='*60)
        print('FRESH BRAVE WINDOW OPENED')
        print('Log into ChatGPT in the window that just opened.')
        print('Stay on the page after login.')
        print('='*60 + '\n')
        
        # Wait for login
        logged_in = await wait_for_login(page)
        if not logged_in:
            print('Login timeout. Exiting.')
            return
        
        print('\nLogin detected! Sending research data...')
        
        # Send FIRST comprehensive message with ALL research
        first_response = await send_and_wait(page, FIRST_MSG)
        if not first_response:
            print('No response to first message')
            return
        
        print(f'\n{"="*60}')
        print(f'CHATGPT FIRST RESPONSE ({len(first_response)} chars)')
        print(f'{"="*60}')
        print(first_response[:800])
        
        # Build challenge based on what ChatGPT specifically said
        # Extract the key recommendation
        sentences = first_response.split('.')
        key_point = sentences[0] if sentences else first_response[:100]
        
        challenge_2 = f"I challenge your approach. You said: '{key_point}'. But my data shows Software Development on Gumroad earns $60,814 per product — the #1 category. And I can build Python tools. Why would I start with {sentences[1] if len(sentences) > 1 else 'your suggestion'} instead of building a simple Python tool that solves one of the pain points I listed? What's the evidence for your recommendation over mine?"
        
        print(f'\nSENDING CHALLENGE (Round 2)...')
        response_2 = await send_and_wait(page, challenge_2)
        if response_2:
            print(f'\n{"="*60}')
            print(f'CHATGPT RESPONSE 2 ({len(response_2)} chars)')
            print(f'{"="*60}')
            print(response_2[:500])
            
            # Now challenge AGAIN based on what it said in response 2
            # Build challenge from specific content of response 2
            sentences_2 = response_2.split('.')
            challenge_3 = f"I see you're recommending {sentences_2[0] if sentences_2 else 'that direction'}. But here's the problem: I have zero audience. No SEO. No ads. How does your recommendation solve the DISTRIBUTION problem? Be specific — not 'build content' or 'grow audience'. Where exactly do I find my first 10 buyers in the first week?"
            
            print(f'\nSENDING CHALLENGE (Round 3)...')
            response_3 = await send_and_wait(page, challenge_3)
            if response_3:
                print(f'\n{"="*60}')
                print(f'CHATGPT RESPONSE 3 ({len(response_3)} chars)')
                print(f'{"="*60}')
                print(response_3[:500])
                
                # Save full conversation
                all_msgs = await page.evaluate("""() => {
                    const m = document.querySelectorAll('[data-message-author-role]');
                    return Array.from(m).map(x => ({role: x.getAttribute('data-message-author-role'), text: x.innerText}));
                }""")
                with open('_deep_research_conversation.json', 'w', encoding='utf-8') as f:
                    json.dump(all_msgs, f, indent=2)
                print(f'\nSaved {len(all_msgs)} messages to _deep_research_conversation.json')
                
                # Final: get conclusive answer
                challenge_4 = f"Give me ONE definitive answer. One product. One name. One price. One platform. One specific way I get my first buyer. No theory, no options, no 'it depends'. What do I build starting tomorrow?"
                
                print(f'\nSENDING FINAL ROUND...')
                response_4 = await send_and_wait(page, challenge_4)
                if response_4:
                    print(f'\n{"="*60}')
                    print(f'FINAL ANSWER ({len(response_4)} chars)')
                    print(f'{"="*60}')
                    print(response_4)
        
        print(f'\n{"="*60}')
        print('DEBATE COMPLETE')
        print('Browser stays open for your review.')
        print(f'Conversation saved to _deep_research_conversation.json')
        print(f'{"="*60}')
        
        # Keep alive
        while True:
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
