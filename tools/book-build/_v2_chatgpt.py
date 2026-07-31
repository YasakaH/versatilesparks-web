"""Send prompt to ChatGPT."""
import asyncio
from playwright.async_api import async_playwright

PROMPT = """Review this V2 cookbook chapter plan. For each chapter, give me: (1) critique, (2) missing recipes, (3) one edge case, (4) overlap with existing.

Ch 9: Advanced Browser Control
- Network interception (CDP): modify requests, inject headers, block resources
- Mobile device emulation: override viewport, UA, device metrics
- WebSocket monitoring: capture WebSocket frames for debugging
- Device rotation: rotate viewport/UA/locale across sessions
- Console log monitoring: capture JS errors and warnings  
- CDP performance metrics: LCP, FCP, TTFB via CDP Performance API

Ch 10: Anti-Detection & Evasion
- Fingerprint analysis: what websites see (navigator, screen, plugins)
- Canvas/WebGL fingerprint spoofing: override canvas fingerprint
- Locale spoofing: timezone, language, geolocation overrides
- Proxy rotation: rotate proxies across sessions without restarting
- Session diversity: fresh profile + fingerprint per session

Ch 11: Advanced Interaction
- Drag and drop: HTML5 drag/drop with CDP input events
- iFrame/Shadow DOM: navigate into nested contexts
- Keyboard shortcuts: Ctrl+S, Cmd+Shift+I, Tab navigation
- Hover/tooltip: mouseover events, tooltip content extraction
- Clipboard: read/write system clipboard via CDP

Ch 12: Production Systems
- Docker: package Chrome + Python in container
- K8s scheduling: CronJob for daily automation runs  
- Database: store scraped data in SQLite
- Alerting: Slack/email notifications on failure
- Webhooks: trigger automation via HTTP endpoint
- Health checks: auto-restart on crash, heartbeat monitoring

Ch 13: Data Processing
- Data cleaning: dedup, normalize, validate scraped data
- Export: CSV, JSON, Parquet with proper encoding
- Incremental: scrape only new/changed pages using hashes
- Visual diffing: compare screenshots to detect page changes

Ch 14: Case Studies
- E-commerce: monitor product prices, alert on drops
- SaaS: authenticated dashboard data collection
- Social media: schedule and publish content
- Internal tool: file uploads, forms, multi-step approvals"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        page = browser.contexts[0].pages[-1]
        
        if 'chatgpt.com' not in page.url:
            await page.goto('https://chatgpt.com', wait_until='domcontentloaded')
            await page.wait_for_timeout(3000)
        
        # Find and focus textarea via click on page first
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        
        ta = await page.query_selector('textarea')
        if not ta:
            print("ERROR: No textarea")
            await page.screenshot(path='err.png')
            return
        
        await ta.hover()
        await ta.click()
        await page.wait_for_timeout(300)
        
        # Type prompt
        await page.keyboard.type(PROMPT, delay=1)
        await page.wait_for_timeout(500)
        await page.keyboard.press("Enter")
        print("Sent!")
        
        # Wait for response
        for i in range(300):
            await page.wait_for_timeout(2000)
            sb = await page.query_selector('button:has-text("Stop")')
            if not sb:
                await page.wait_for_timeout(2000)
                break
            if i % 15 == 0:
                print(f"  {i*2}s...")
        
        msgs = await page.query_selector_all('[data-message-author-role="assistant"]')
        print(f"Messages: {len(msgs)}")
        if msgs:
            t = await msgs[-1].inner_text()
            with open('cookbook/chatgpt_v2_response.md','w',encoding='utf-8') as f:
                f.write(t)
            print(f"Saved ({len(t)} chars)")
        else:
            print("No response")

asyncio.run(main())
