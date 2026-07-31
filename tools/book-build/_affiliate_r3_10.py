"""
Send consolidated challenges 3-9, then final round 10.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

ROUNDS_3_9 = """Let me push on several points. Challenge each:

**1. "Delay affiliate until 10 clients"** — At 1-2 clients/month, that's 5-10 months. By then, the affiliate programs might change their terms. What's a FASTER milestone? Like... "after your first INR 10,000 in service revenue" instead of "10 clients"?

**2. Trust is contextual — I agree.** But here's the challenge: if I recommend a tool to a client and they sign up via my affiliate link, the cookie might expire before they actually purchase (many SaaS tools have 30-day cookies but business decisions take longer). Is this a real problem or am I overthinking it?

**3. Concrete numbers — give me real figures.** For a typical Indian automation client (say a CA firm paying ₹4,999 for a workflow), what adjacent tools would they naturally need? And what would the affiliate commission be for each?
- Payment gateway (Instamojo/Razorpay) — ₹___ per referral
- Cloud hosting — ₹___ per referral
- Email service — ₹___ per referral
- CRM — ₹___ per referral
- Total potential upsell per client: ₹___

**4. The prompt pack** — You said digital products pay faster (T+3). But can I SELL it without traffic? I listed it on Instamojo but nobody visits my store. How do I get the FIRST sale?

**5. Where do people who need automation HANG OUT online in India?** Give me specific:
- LinkedIn groups (names)
- Facebook groups (names)  
- Telegram channels
- Reddit communities
- Offline: which cities, which business associations

**6. The real question** — Should I even THINK about affiliate marketing in my first month, or is it a complete distraction? Give me a definitive cutoff: "Don't touch affiliate until you've earned your first ₹15,000 from services."

**7. If you could only give me ONE piece of advice for this week** — not about affiliate, but about getting my first client — what would it be? The single most effective action.

Be blunt. Don't pad.
"""

FINAL_ROUND = """**FINAL VERDICT — MUST PICK ONE PATH**

After everything we've debated, I need a single clear answer:

**Path A: Pure Service Focus**
- Zero time on affiliate/prompts/content
- 100% of time on LinkedIn outreach + demos
- Target: 1st client at ₹4,999 within 14 days
- Revisit affiliate only after ₹15,000 in service revenue

**Path B: Hybrid**
- Primary: service outreach
- Secondary: set up Instamojo referral link in store footer (no extra time)
- Post LinkedIn content that builds expertise (which doubles as service marketing)

**Path C: Affiliate-First**
- Use my technical skills to create content ranking on Google/YouTube
- Build traffic first, monetize via affiliate
- Services as secondary offer

Which path? Path A, B, or C. No "it depends." No "a mix of all three."
"""

async def send_and_wait(page, msg, label):
    ta = await page.wait_for_selector('#prompt-textarea', timeout=20000)
    await ta.click()
    await asyncio.sleep(0.5)
    await ta.fill('')
    await ta.fill(msg)
    await asyncio.sleep(1.5)
    btn = await page.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
    await btn.click()
    print(f'[SENT] {label}')
    
    prev = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
    for i in range(120):
        await asyncio.sleep(5)
        cur = await page.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
        if cur > prev:
            await asyncio.sleep(10)
            return True
        if i % 12 == 0:
            print(f'  Wait... ({i*5}s)')
    return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                msg_len = await pg.evaluate("document.querySelectorAll('[data-message-author-role]').length")
                print(f'Messages: {msg_len}')
                
                # Rounds 3-9 consolidated
                print('\n=== ROUNDS 3-9 (Consolidated) ===')
                ok = await send_and_wait(pg, ROUNDS_3_9, 'Rounds 3-9')
                if ok:
                    text = await pg.evaluate("""() => {
                        const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                        return msgs[msgs.length - 1]?.innerText || 'NONE';
                    }""")
                    print(f'\nResponse ({len(text)} chars):\n{text[:1000]}...\n')
                else:
                    print('Timeout on rounds 3-9')
                
                # Round 10 - Final Verdict
                print('\n=== ROUND 10 (FINAL) ===')
                ok = await send_and_wait(pg, FINAL_ROUND, 'Final')
                if ok:
                    text = await pg.evaluate("""() => {
                        const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                        return msgs[msgs.length - 1]?.innerText || 'NONE';
                    }""")
                    print(f'\n=== FINAL VERDICT ({len(text)} chars) ===')
                    print(text)
                
                print('\n[DONE] Debate complete. Browser stays open.')
                break

asyncio.run(main())
