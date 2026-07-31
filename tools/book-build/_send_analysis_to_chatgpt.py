"""
Send comprehensive analysis to ChatGPT for deep debate.
"""
import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

PAYLOAD = """I've analyzed 4 key videos about open-source financial tools. Here's what I found:

## Video Analysis

### 1. FinceptTerminal (27K stars)
Open-source Bloomberg Terminal alternative. C++20/Qt6 desktop app. 423K instruments, 100+ data connectors, 16 brokers (Zerodha, IBKR, Alpaca), 37 AI agents (Buffett/Graham/Munger personas), MCP integration, node editor, AI Quant Lab. AGPL-3.0 license.

### 2. TradingAgents (92.9K stars, Apache 2.0)  
Multi-agent LLM hedge fund framework. 4 analysts + bull/bear debate rounds + trader + risk team + portfolio manager. LangGraph orchestration. Supports all LLM providers including local via Ollama. Persistent decision log that learns from past trades. v0.3.1 just released.

### 3. OpenBB (open-source investment research)
Financial platform for equity, options, crypto, forex. Has AI financial analyst agent. AGPLv3.

## My Skills & Constraints
- Python, AI/LLM integration, FreeLLMAPI (62 free models), n8n, Playwright/nodriver
- Zero audience, zero website
- Instamojo store works, Gumroad ready to set up
- Banned from LinkedIn/Fiverr (automation)
- Can build almost anything in <1 week

## Now I need you to generate EVERY possible product/service/info product idea from these:

Think across these categories:
A) **Ready-to-run products** - Bundles, scripts, templates people can download and use
B) **Setup/configuration services** - "I'll set this up for you"
C) **Information products** - Guides, tutorials, comparisons
D) **Simplified/packaged versions** - Take the complex open-source tool, make it simple
E) **Complementary tools** - Things these projects are missing
F) **Educational content** - Courses, blogs, YouTube scripts

## For each idea, give me:
1. What it is (exact name and description)
2. Target buyer (who pays for this?)
3. Price point
4. Build time
5. Discovery channel (how do they find it?)
6. Why it's defensible (why won't AI/competition kill it next month?)
7. Your challenge to this idea (what's wrong with it?)

Generate at least 15 ideas. Then for each one, challenge it. Find the flaws. Then give me your top 3 recommendations.

Be exhaustive. Don't skip any category. Challenge every assumption.
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com' in pg.url:
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=20000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill('')
                await ta.fill(PAYLOAD)
                await asyncio.sleep(2)
                btn = await pg.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
                await btn.click()
                print('Sent comprehensive analysis')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(180):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return msgs[msgs.length - 1]?.innerText || '';
                        }""")
                        print(f'\n=== CHATGPT ({len(text)} chars) ===')
                        print(text)
                        break
                    if i % 12 == 0:
                        print(f'  Wait ({i*5}s)')
                break

asyncio.run(main())
