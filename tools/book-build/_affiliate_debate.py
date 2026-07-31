"""
Deep debate with ChatGPT on affiliate marketing - 10+ iterations.
Sends challenges, gets responses, challenges again, repeats.
"""
import asyncio, json, time
from playwright.async_api import async_playwright

CDP_PORT = 9230

ITERATIONS = 12

OPENING = """I need to thoroughly explore affiliate marketing as an income stream. Do NOT give me generic advice. Challenge everything I say. This is the first of many rounds - I will challenge your responses.

## My Research So Far

Platforms we have: Fiverr, LinkedIn, Instamojo (easyautomation.stores.instamojo.com)
No website. No audience. Based in India. FreeLLMAPI available.

Affiliate programs available in India:
- Amazon Associates India (up to 10% commission)
- Flipkart Affiliate (up to 12% commission)  
- Instamojo Affiliate (pays for referrals to their platform)
- Cashfree Payments
- Cuelinks (aggregator)
- vCommission (aggregator)
- ClickBank (digital products, international)
- Razorpay Affiliate

## My First Question

Can we SELL affiliate products ON the platforms we already have (Fiverr, Instamojo, LinkedIn)? Specifically:

1. **Instamojo store** — Can we list affiliate links/products? Does Instamojo allow affiliate link promotion on store pages? Instamojo itself has an affiliate program — can we join that and promote it?

2. **Fiverr** — Can we offer "affiliate marketing setup" as a service? Or does Fiverr prohibit this?

3. **LinkedIn** — Can we use LinkedIn posts and outreach to share affiliate links without violating policies?

4. **No website, no audience** — All affiliate guides say you need traffic. Where do we get traffic with zero existing audience, zero budget?

5. **Fastest first payment** — Which affiliate program could pay out in under 7 days with minimal effort?

Be specific. Give me real numbers - commission rates, payout thresholds, payment timelines for Indian users. Do NOT say "research more" — give me your best analysis based on available information.
"""

CHALLENGES = [
    # Round 2
    """I want to challenge a few assumptions you may have raised:

1. **Amazon Associates & similar programs** — They require a website to join. I don't have one. And even if approved, posting links on LinkedIn/WhatsApp with zero audience means zero clicks. Cold traffic doesn't convert for affiliate.

2. **Fiverr** — Can I sell "affiliate link promotion" as a service? Or list affiliate products as gig extras? I need to know the actual policy.

3. **Instamojo** — I already have a store there. Can I embed affiliate links in product descriptions or store pages? Does Instamojo's TOS allow using their store as an affiliate link hub?

4. **Commission timelines** — Most Indian affiliate programs pay 30-60 days after sale. I need money faster than that. Which programs (if any) pay faster?
""",

    # Round 3
    """Let me pressure test this more:

1. **Traffic is the bottleneck.** I have zero followers, zero website, zero email list. The ONLY channels are LinkedIn DMs (1:1 outbound) and maybe WhatsApp groups. For affiliate marketing to work through DMs, the product needs to be:
   - Impulse-buyable (under ₹1,000)
   - Solves an urgent problem
   - Requires zero trust (they don't need to trust ME, just need the product)
   
   Does such a product exist in any Indian affiliate program?

2. **Conversion math:** If I send 100 LinkedIn DMs with an affiliate link, how many clicks? How many sales? Give me realistic numbers, not optimistic ones.

3. **Is there an affiliate product I can literally sell through my Instamojo store?** Like, I list a product that's actually an affiliate link to a SaaS tool? Or does Instamojo prohibit this?

Be brutally realistic. If the math doesn't work, say so.""",

    # Round 4
    """I want to compare two paths with actual math:

**Path A: Service selling (automation)**
- Send 100 LinkedIn DMs offering automation services at ₹4,999
- Estimated: 5-10 replies, 2-3 discovery calls, 1-2 sales
- Revenue: ₹4,999 - ₹9,998
- Time to first payment: 3-10 days

**Path B: Affiliate marketing**
- Send 100 LinkedIn DMs with affiliate links to [some product]
- Estimated: 2-5 clicks, 0-1 sales
- Revenue: ₹0 - ₹500
- Time to first payment: 30-60 days (if any)

**If this math is roughly correct, then affiliate marketing is 10-20x LESS effective than service selling for someone starting from zero. Do you agree or disagree? Where is my math wrong?**""",

    # Round 5
    """Let me push further:

If we agree that service selling beats affiliate for immediate income, the question becomes:

**Should I invest ANY time in affiliate marketing right now?**

My argument: No. Zero time. Because:
- Every hour spent on affiliate setup/learning is an hour NOT spent on outreach for service selling
- At my stage, the opportunity cost of NOT doing outreach is my biggest loss
- Affiliate can come AFTER i have cash flow from services

**Challenge this.** Is there ANY affiliate action that takes <30 minutes and could generate income WITHOUT distracting from service selling? Like... joining Instamojo's affiliate program and just putting the link in my store footer? No extra effort?

If there's a truly passive 30-minute action, tell me. Otherwise, tell me to drop affiliate entirely for now.""",

    # Round 6
    """Let me challenge my own argument:

Maybe affiliate marketing via LinkedIn content (not DMs) is viable because:
1. I'm already posting on LinkedIn (service demos)
2. I can add affiliate links to relevant tools in my posts
3. Content has compounding effects — a post from week 1 can still generate clicks in week 4

So instead of cold DM affiliate promotion, it's CONTENT-BASED affiliate marketing through LinkedIn posts.

**Questions:**
1. Does LinkedIn penalize posts with affiliate links? 
2. Would adding "I use X tool, try it here: [link]" hurt credibility when I'm also selling services?
3. Which tools that I actually use have affiliate programs? (I use: FreeLLMAPI, Brave, n8n, Python, VSCode, Playwright)
4. Can I earn from tools I already recommend?

Tell me which of the tools I use have affiliate programs and their commission rates.""",

    # Round 7
    """I checked on the tools I use. Let me challenge:

1. **n8n** — No affiliate program for self-hosted version
2. **Brave** — Has a Brave Creators program but it's for BAT tokens, not direct commissions
3. **VSCode / Python / Playwright** — No affiliate programs (open source)
4. **FreeLLMAPI** — Probably no affiliate program since it's a free API gateway

So the tools I actually use don't pay commissions. Unless I start promoting tools I DON'T use just for commission — which feels dishonest.

**Question:** Is it worth promoting tools I don't personally use just for affiliate income? Won't my audience (clients/business owners) see through this and trust me less?

Alternatively — are there tools I SHOULD be using that have good affiliate programs? Like... Canva, Hostinger, Notion, Jasper AI, etc.?""",

    # Round 8
    """Let me consider a specific angle:

**Promoting business tools to my target audience (Indian SMBs) via LinkedIn content.**

If I'm already posting about automation and efficiency, I can naturally recommend:
- **Zoho** (affiliate program for Indian SaaS) — CRM, Books, etc.
- **Hostinger/Namecheap** — web hosting (high commission, Indian audience buys this)
- **Canva** — design tool (many business owners use it)
- **Notion** — productivity (growing in India)

**Real questions:**
1. Do these programs accept Indian affiliates without a website?
2. What's the commission? Cookie duration? Payout threshold?
3. How many LinkedIn followers do I need before posts with affiliate links convert?
4. One good post with an affiliate link — what's a realistic earning? ₹500? ₹5,000?

Give me HONEST numbers. If a post gets 1,000 views and has 1 affiliate link, what's the realistic commission?""",

    # Round 9
    """I want to stress-test the MOST promising option:

**Instamojo's own affiliate program** — because I already have a store there.

If I refer someone to create an Instamojo store:
1. What's the payout? One-time or recurring?
2. Can I put the referral link in my store description or checkout page?
3. What's a realistic conversion rate? (Someone visits store → reads → clicks referral → signs up)
4. If my store gets 100 visitors/month and 2% click the referral link, and 10% of those sign up — that's 0.2 signups/month. At ₹500 each, that's ₹100/month. Is this math right?

**Also** — once I start getting automation clients, I can recommend Instamojo as a payment solution to THEM. That's a natural upsell. Same for Zoho, Hostinger, etc.

**Thesis: Affiliate works best as a BYPRODUCT of service delivery, not as a standalone strategy for someone with zero audience. Agree or disagree?**""",

    # Round 10 — FINAL
    """**FINAL VERDICT REQUIRED**

Based on 9 rounds of debate, give me a definitive actionable answer:

**Should I pursue affiliate marketing in my current situation (zero audience, zero website, need fast income)?**

Yes or No.

If YES:
- Exact first step (what program, what link, where to post)
- Time investment required
- Expected first payout amount and timeline

If NO:
- Under what specific conditions should I revisit this? (e.g. "after you close 5 clients" or "when you have 500 LinkedIn followers")
- What's the ONE thing I should do today instead?

BE DEFINITIVE. No equivocation. No "it depends."
""",
]

async def debate_round(page, message, round_num):
    """Send a message to ChatGPT and wait for response."""
    ta = await page.wait_for_selector('#prompt-textarea', timeout=20000)
    await ta.click()
    await asyncio.sleep(0.5)
    await ta.fill('')
    await asyncio.sleep(0.5)
    await ta.fill(message)
    await asyncio.sleep(2)
    
    btn = await page.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
    await btn.click()
    print(f'[SENT] Round {round_num}')
    
    # Wait for response
    prev = await page.evaluate(
        'document.querySelectorAll(\'[data-message-author-role="assistant"]\').length'
    )
    for i in range(120):
        await asyncio.sleep(5)
        try:
            current = await page.evaluate(
                'document.querySelectorAll(\'[data-message-author-role="assistant"]\').length'
            )
            if current > prev:
                await asyncio.sleep(10)
                return True
        except:
            pass
        if i % 12 == 0:
            print(f'  Waiting... ({i*5}s)')
    return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        page = None
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url or 'chat.openai.com' in pg.url:
                page = pg
                break
        
        if not page:
            print('Creating new ChatGPT page...')
            page = await ctx.new_page()
            await page.goto('https://chat.openai.com', wait_until='domcontentloaded')
            await asyncio.sleep(10)
        
        print(f'ChatGPT: {page.url[:80]}')
        
        # Check current conversation
        msgs = await page.evaluate(
            'document.querySelectorAll(\'[data-message-author-role]\').length'
        )
        print(f'Starting conversation: {msgs} messages')
        
        # Round 1: Opening
        print(f'\n=== ROUND 1/10 ===')
        ok = await debate_round(page, OPENING, 1)
        print(f'Round 1: {"OK" if ok else "TIMEOUT"}')
        
        # Save after each round
        def save_conversation(round_num):
            return page.evaluate(f"""() => {{
                const msgs = Array.from(document.querySelectorAll('[data-message-author-role]'))
                    .map(m => ({{role: m.getAttribute('data-message-author-role'), text: m.innerText.substring(0, 200)}}));
                return JSON.stringify({{total: msgs.length, round: {round_num}, preview: msgs.slice(-2)}});
            }}""")
        
        preview = await save_conversation(1)
        print(f'After round 1: {preview[:200]}')
        
        # Rounds 2-10: Challenge and counter-challenge
        for i, challenge in enumerate(CHALLENGES):
            round_num = i + 2
            print(f'\n=== ROUND {round_num}/10 ===')
            
            # Before sending, read the last assistant response to tailor challenge
            last_response = await page.evaluate("""() => {
                const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                const last = msgs[msgs.length - 1];
                return last ? last.innerText.substring(0, 300) : 'NO RESPONSE';
            }""")
            
            # Customize challenge with context from last response
            # (Using a generic challenge since we can't dynamically rewrite the script mid-run)
            ok = await debate_round(page, challenge, round_num)
            print(f'Round {round_num}: {"OK" if ok else "TIMEOUT"}')
            
            preview = await save_conversation(round_num)
            print(f'After round {round_num}: {preview[:200]}')
        
        # Save final conversation
        all_msgs = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('[data-message-author-role]'))
                .map(m => ({role: m.getAttribute('data-message-author-role'), text: m.innerText}));
        }""")
        
        # Show latest response
        for m in reversed(all_msgs):
            if m['role'] == 'assistant':
                print(f'\n=== FINAL RESPONSE ({len(m["text"])} chars) ===')
                print(m['text'])
                break
        
        with open(r'C:\Users\varas\personalities\_chatgpt_affiliate_debate.json', 'w', encoding='utf-8') as f:
            json.dump({
                'total_messages': len(all_msgs),
                'conversation': all_msgs,
                'timestamp': time.time()
            }, f, indent=2, ensure_ascii=False)
        
        print(f'\n[DONE] Final conversation: {len(all_msgs)} messages. Browser stays open.')

asyncio.run(main())
