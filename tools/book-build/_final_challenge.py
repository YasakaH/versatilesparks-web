"""
One more challenge round - test if the Affiliate Link Checker holds up.
Then save and build.
"""
import asyncio, json
from playwright.async_api import async_playwright

CDP_PORT = 9230
CONV_FILE = r'C:\Users\varas\personalities\_deep_research_conversation.json'

CHALLENGE = """I'm about to start building the Affiliate Link Checker Pro. Before I code, one final challenge:

You said $39 lifetime license. But I can build this with FreeLLMAPI which costs me $0 to run. Most competitors charge $10-20/month because they have API bills.

What if I price it at:
- **Free tier**: Check 10 links (limited, no export)
- **Pro tier**: $49 unlimited, lifetime

This way every free download IS marketing. People share it. It shows up in search results more. And $49 matches the sweet spot of the top-selling Gumroad products ($50 average for top earners).

Does this change the recommendation? Or should I stick with $39 flat?
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        for pg in ctx.pages:
            if 'chatgpt.com/c/' in pg.url:
                count = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role]\').length')
                print(f'Messages: {count}')
                
                # Send challenge
                ta = await pg.wait_for_selector('#prompt-textarea', timeout=30000)
                await ta.click()
                await asyncio.sleep(0.5)
                await ta.fill(CHALLENGE)
                await asyncio.sleep(1.5)
                await pg.keyboard.press('Control+Enter')
                print('Challenge sent')
                
                prev = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                for i in range(120):
                    await asyncio.sleep(5)
                    cur = await pg.evaluate('document.querySelectorAll(\'[data-message-author-role="assistant"]\').length')
                    if cur > prev:
                        await asyncio.sleep(10)
                        text = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role="assistant"]');
                            return m[m.length-1]?.innerText || '';
                        }""")
                        print(f'\n=== RESPONSE ({len(text)} chars) ===')
                        print(text)
                        
                        # Save full conv
                        all_msgs = await pg.evaluate("""() => {
                            const m = document.querySelectorAll('[data-message-author-role]');
                            return Array.from(m).map(x => ({role: x.getAttribute('data-message-author-role'), text: x.innerText}));
                        }""")
                        with open(CONV_FILE, 'w', encoding='utf-8') as f:
                            json.dump(all_msgs, f, indent=2)
                        print(f'Saved {len(all_msgs)} messages')
                        break
                    if i % 12 == 0:
                        print(f'  Wait ({i*5}s)')
                break

asyncio.run(main())
