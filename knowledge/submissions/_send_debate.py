"""Send debate message to ChatGPT via existing Brave session"""
import asyncio, json, sys
from playwright.async_api import async_playwright

DEBATE = '''I have read all 71 of your responses. Strong analysis overall. Now I want to challenge several of your recommendations before I implement anything.

**1. CORE doc count — 22+ docs is too many**
You recommended splitting into more small documents. I disagree. 22+ docs creates navigation overhead, context window bloat, and maintenance debt. I believe 12-15 well-structured CORE documents is the right max. Which recommendations specifically require new files vs. sections in existing files?

**2. Routing algorithm — the 40/30/20/10 formula is too rigid**
You proposed: expertise_match 40%, capability_match 30%, risk_alignment 20%, historical_success 10%. This looks like false precision. Real routing depends on task type, user preference, and context that can't be scored numerically. A simpler priority-based selector (if security → Security Architect, if finance → Financial Analyst) would be more predictable. When is a formal scoring model actually necessary vs. simple rule-based routing sufficient?

**3. Complexity L0-L3 — does every task need classification?**
Classifying every request adds overhead. Most queries are simple (L0). The rare complex ones already have clear domain signals. Is a formal classification tier a genuine improvement or engineering theater?

**4. Execution DAG — over-engineering for 80% of tasks**
A formal DAG with nodes, dependencies, and outputs is excellent for multi-step projects. But for a single-question task, it wastes tokens. Where should we draw the line?

**5. Memory governance — part of Chief of Staff or separate?**
You recommended Chief of Staff owns memory governance. But memory is a cross-cutting concern. Should it be a separate meta-personality (Memory Curator)?

**6. Schema v2 — 33 fields is ambitious**
Not every persona needs all 33 fields. Should we define a minimal required set (10-12 fields) with optional extensions?

**7. Escalation model — 6 levels for small teams?**
Escalation defines 6 levels. For a single-developer setup, levels 5-6 are never reached. Should the model have a configurable depth?

I want your best counter-arguments. Not looking for agreement — challenge my positions.'''

async def main():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp('http://localhost:9229')
                ctx = browser.contexts[0]
                
                # Find ChatGPT page
                target_page = None
                for pg in ctx.pages:
                    url = pg.url
                    if 'chatgpt.com/c/6a532496' in url:
                        target_page = pg
                        break
                
                if not target_page:
                    # Try all pages
                    for pg in ctx.pages:
                        try:
                            title = await pg.evaluate('document.title')
                            if 'CORE Docs' in title or 'ChatGPT' in title:
                                target_page = pg
                                break
                        except:
                            continue
                
                if not target_page:
                    print('❌ ChatGPT page not found')
                    sys.exit(1)
                
                print(f'✅ Found ChatGPT page: {await target_page.evaluate("document.title")}')
                
                # Navigate to refresh if needed
                if 'just a moment' in (await target_page.evaluate('document.title')).lower():
                    await target_page.goto('https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7', wait_until='domcontentloaded')
                    await asyncio.sleep(10)
                
                # Find textarea
                ta = await target_page.query_selector('#prompt-textarea')
                if not ta:
                    print('❌ Textarea not found')
                    sys.exit(1)
                
                await ta.click()
                await asyncio.sleep(1)
                
                # Clear with Ctrl+A + Delete
                await target_page.keyboard.press('Control+a')
                await asyncio.sleep(0.5)
                await target_page.keyboard.press('Delete')
                await asyncio.sleep(0.5)
                
                # Type in chunks (Playwright types character by character)
                chunk_size = 2000
                for i in range(0, len(DEBATE), chunk_size):
                    chunk = DEBATE[i:i+chunk_size]
                    await ta.fill(chunk)
                    await asyncio.sleep(0.5)
                    # We need to append - fill replaces. So let's type
                
                # Actually, use keyboard typing instead
                await ta.click()
                await asyncio.sleep(1)
                await target_page.keyboard.press('Control+a')
                await asyncio.sleep(0.5)
                await target_page.keyboard.press('Delete')
                await asyncio.sleep(1)
                
                # Type text
                await target_page.keyboard.type(DEBATE, delay=10)
                await asyncio.sleep(3)
                
                # Send
                send_btn = await target_page.query_selector('[data-testid="send-button"]')
                if send_btn:
                    disabled = await send_btn.get_attribute('disabled')
                    if not disabled:
                        await send_btn.click()
                    else:
                        await target_page.keyboard.press('Control+Enter')
                else:
                    await target_page.keyboard.press('Control+Enter')
                
                print(f'✅ Debate sent! ({len(DEBATE)} chars)')
                return
                
        except Exception as e:
            print(f'⚠️ Attempt {attempt+1} failed: {e}')
            if attempt < max_retries - 1:
                await asyncio.sleep(5)
    
    print('❌ All attempts failed')

asyncio.run(main())
