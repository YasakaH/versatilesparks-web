"""
Comprehensive debate with ChatGPT about everything built so far.
"""
import asyncio, json, time
from playwright.async_api import async_playwright

CDP_PORT = 9230

DEBATE_QUESTIONS = """I need you to challenge everything I've built. Be brutally honest — don't spare my feelings.

## Context of what's been done

I created accounts on Fiverr, LinkedIn, and Instamojo (yasaka.hanini@protonmail.com). Upwork blocked registration. The store is at easyautomation.stores.instamojo.com.

I built:
1. An AI Service Dashboard (local web tool connected to FreeLLMAPI for generating client deliverables)
2. A digital product pack "50 AI Prompts for Indian Businesses" (₹499)
3. 2 demo automation scripts (browser automation + document processing)
4. LinkedIn profile with headline and about section filled
5. Outreach templates for CAs, clinics, real estate agents
6. The Instamojo store has profile set up and a product form filled (but can't publish until KYC/payments are enabled)
7. Fiverr account created, seller onboarding not yet complete

But my LinkedIn session expired (authwall from too much automated navigation).

You said earlier: "You're about 80% infrastructure and 20% customer acquisition. For someone trying to earn quickly, I'd want almost the opposite."

## Challenge these decisions

1. **The digital product (₹499 prompt pack)** — You said earlier this solves the wrong problem and I should focus on services instead. But Instamojo is set up. Should I abandon the prompt pack entirely? Or keep it as passive income while focusing on services? Be specific.

2. **LinkedIn profile content** — I set the headline to "I automate repetitive office work with AI & Python | Browser automation | Document workflows | Lead management | Helping Indian businesses save hours weekly". You said earlier to optimize for OUTBOUND conversion, not inbound. Is this headline actually good for outbound? Would a CA or clinic owner in India understand what I do from this?

3. **Service offering** — I consolidated to "Business Process Automation" as one umbrella service. But you said earlier the offer should be specific: "I'll eliminate one repetitive task within 5 business days for a fixed price." Should I offer this as a single fixed-price package, or should I list multiple services? If one package, what's the right price point for the Indian market?

4. **Fiverr vs direct outreach** — Fiverr onboarding isn't complete. You ranked Fiverr 3/10 for first payment. Should I bother completing it? Or just focus 100% on LinkedIn outreach and Instamojo?

5. **The demos** — I built 2 demo scripts (browser automation + document processing). You said to record 30-second videos. What should the FIRST LinkedIn post actually say? Give me the exact text/post content for the first 3 posts.

6. **Upwork blocked** — Registration didn't work. Should I try again with a different approach, or permanently skip it?

7. **What am I STILL missing?** — I keep building infrastructure. What's the ONE thing I should do TODAY that would get me closer to ₹5,000 than anything else?

Don't agree with me. Challenge every assumption. Give me the honest tradeoffs.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        # Find ChatGPT page
        page = None
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url or 'chat.openai.com' in pg.url:
                page = pg
                break
        
        if not page:
            print('No ChatGPT page found! Creating new...')
            page = await ctx.new_page()
            await page.goto('https://chat.openai.com', wait_until='domcontentloaded')
            await asyncio.sleep(10)
        
        print(f'ChatGPT URL: {page.url[:80]}')
        
        # Check current conversation
        msgs = await page.evaluate("""
            () => Array.from(document.querySelectorAll('[data-message-author-role]'))
                .map(m => m.getAttribute('data-message-author-role'))
        """)
        print(f'Current conversation: {len(msgs)} messages')
        
        # Send the debate
        ta = await page.wait_for_selector('#prompt-textarea', timeout=20000)
        await ta.click()
        await asyncio.sleep(1)
        await ta.fill('')
        await asyncio.sleep(0.5)
        await ta.fill(DEBATE_QUESTIONS)
        await asyncio.sleep(2)
        
        btn = await page.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
        await btn.click()
        print('[SENT] Debate questions submitted!')
        
        # Wait for response with multiple detection methods
        prev_count = len(msgs)
        for i in range(120):  # 10 min
            await asyncio.sleep(5)
            try:
                current = await page.evaluate(
                    'document.querySelectorAll(\'[data-message-author-role="assistant"]\').length'
                )
                if current > prev_count:
                    print(f'New response detected after {i*5}s')
                    await asyncio.sleep(20)
                    break
            except:
                pass
            try:
                disabled = await page.evaluate(
                    'document.querySelector("#prompt-textarea")?.getAttribute("disabled")'
                )
                stop = await page.evaluate(
                    'document.querySelector(\'[data-testid="stop-button"]\') === null'
                )
                if not disabled and stop and i > 4:
                    await asyncio.sleep(10)
                    break
            except:
                pass
            if i % 12 == 0:
                print(f'  Waiting... ({i*5}s)')
        
        # Save conversation
        all_msgs = await page.evaluate("""
            () => Array.from(document.querySelectorAll('[data-message-author-role]'))
                .map(m => ({role: m.getAttribute('data-message-author-role'), text: m.innerText}))
        """)
        
        # Show latest response
        for m in reversed(all_msgs):
            if m['role'] == 'assistant':
                print(f'\n=== CHATGPT DEBATE ({len(m["text"])} chars) ===')
                print(m['text'])
                break
        
        with open(r'C:\Users\varas\personalities\_chatgpt_final_debate.json', 'w', encoding='utf-8') as f:
            json.dump({
                'total_messages': len(all_msgs),
                'conversation': all_msgs,
                'timestamp': time.time()
            }, f, indent=2, ensure_ascii=False)
        
        print(f'\n[DONE] Full conversation saved. Browser stays open.')

asyncio.run(main())
