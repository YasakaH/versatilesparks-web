"""
Auto-debate: Challenge ChatGPT's top 3 picks relentlessly.
No asking permission. Just execute.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

CHALLENGES = [
    # Round 1: Pressure test top 3
    """Let me challenge your top 3 recommendations.

**#1 TradingAgents One-Click Installer ($29-79)**
Challenge: Who buys a $29 installer for a free open-source tool? The kind of person technical enough to find TradingAgents on GitHub is usually technical enough to run `pip install` and `python main.py`. The ones who can't install it probably can't use it either. Is there actually a paying market for this? Be honest about realistic monthly sales with zero marketing budget.

**#2 Strategy Bundle ($49-99)**
Challenge: Trading strategies need to be PROFITABLE to be worth $99. If I sell "20 tested strategies" and they lose money, I get bad reviews. If they make money, I'm selling a money-making machine for $99 — which means either (a) they don't actually work consistently, or (b) I'm underpricing by 100x. Which is it?

**#3 Local AI Config Bundle ($39)**
Challenge: This is literally a text file with model names and prompt templates. FreeLLMAPI has 62 free models — but that changes weekly. And the config for Ollama is: `ollama pull qwen3.5` and done. Who pays $39 for this?

Be brutal. Find the flaw in each.""",

    # Round 2: Go deeper
    """Good. Now I want you to think about what I CAN actually build that solves a REAL pain.

If these projects (TradingAgents, FinceptTerminal, OpenBB) have GitHub Issues and Discussions — that's where the REAL complaints are.

What are the ACTUAL complaints people have?
- Installation failing on Windows?
- Broker API keys not working?
- LLM tokens cost too much?
- No documentation for beginners?
- Can't run it without an OpenAI key?

**My actual advantage:** I have FreeLLMAPI with 62 free models. I can offer AI-powered tools WITHOUT passing on API costs. Every other seller has to charge enough to cover OpenAI/Anthropic bills. I don't.

What's a product that ONLY I can build because I have free AI infrastructure? That's my real moat.""",

    # Round 3: Find the wedge
    """Let me synthesize:

1. I have free AI (FreeLLMAPI)
2. I can build Python tools fast
3. I can build undetected browser automation (nodriver)
4. Gumroad is my store
5. Zero audience to start

**The wedge product:** What if I build a "Free AI Trading Analyst" that uses FreeLLMAPI to analyze any stock/crypto — no API key needed, no subscription, just download and run? It wraps TradingAgents' prompts but routes through FreeLLMAPI instead of paid providers?

**The hook:** "Run AI hedge fund analysis without paying for OpenAI. Free LLM provider included."

Price: $19 (one-time, since I don't have API costs to cover)
Target: Retail traders tired of paying $20/month for ChatGPT just to analyze stocks

**Challenge this.** Is this actually a defensible product? Or will someone just clone it and offer it for free on GitHub?""",

    # Round 4: Business model debate
    """OK. Say I build the Free AI Trading Analyst ($19). My store sells 0 copies in week 1 because nobody knows it exists.

**The real problem isn't the product. It's distribution.**

With zero audience, zero SEO, zero social media — how do I get the FIRST sale?

Here's my theory: **GitHub as distribution.**

Instead of selling on Gumroad and hoping people find it, I:
1. Build the tool and open-source a BASIC version on GitHub
2. Premium features (extra strategies, priority updates) are on Gumroad for $19
3. GitHub README links to Gumroad
4. Post on Reddit r/algotrading, r/quant, r/IndianStreetBets

**Does this work?** GitHub → README → Gumroad has been done before (many projects do this). Realistically, how many GitHub stars before I get a sale? 100? 1000?

Or is there a better distribution channel I'm missing?""",

    # Round 5: Final decision
    """After 4 rounds of debate, give me a single actionable decision:

**What ONE product do I build THIS WEEK?**

Requirements:
- Can be built in 5 days or less
- Solves a real problem someone will search for
- Uses FreeLLMAPI as a moat (free AI = no API costs)
- Can be discovered WITHOUT social media or ads
- Priced $19-79
- First sale possible within 14 days of publishing

Give me the exact:
- Product name
- What it does (1 sentence)
- Price
- Where I list it
- How the first buyer finds it
- Build plan (what to build each day)

No more analysis. Give me the execution plan.
"""
]

async def debate_round(pg, msg, label):
    ta = await pg.wait_for_selector('#prompt-textarea', timeout=20000)
    await ta.click()
    await asyncio.sleep(0.3)
    await ta.fill('')
    await ta.fill(msg)
    await asyncio.sleep(1.5)
    btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
    await btn.click()
    print(f'[{label}] Sent')
    
    prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
    for i in range(120):
        await asyncio.sleep(5)
        cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
        if cur > prev:
            await asyncio.sleep(10)
            text = await pg.evaluate("""() => {
                const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                return msgs[msgs.length - 1]?.innerText || '';
            }""")
            print(f'[{label}] Response: {len(text)} chars')
            return text
        if i % 12 == 0:
            print(f'  Wait ({i*5}s)')
    return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                for i, challenge in enumerate(CHALLENGES):
                    print(f'\n{"="*50}\nROUND {i+1}/{len(CHALLENGES)}\n{"="*50}')
                    resp = await debate_round(pg, challenge, f'R{i+1}')
                    if resp:
                        if i == len(CHALLENGES) - 1:
                            print(f'\n=== FINAL DECISION ===\n{resp}')
                        else:
                            short = resp[:500]
                            print(f'Preview: {short}...')
                print('\n[DONE] All rounds complete.')
                break

asyncio.run(main())
