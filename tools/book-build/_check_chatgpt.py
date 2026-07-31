"""Check ChatGPT state and navigate there."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9230')
        # Check existing pages
        pages = browser.contexts[0].pages if browser.contexts else []
        print(f"Existing pages: {len(pages)}")
        
        # Use existing page or create new one
        if pages:
            page = pages[0]
        else:
            page = await browser.new_page()
        
        await page.goto('https://chatgpt.com', wait_until='domcontentloaded')
        await page.wait_for_timeout(3000)
        title = await page.title()
        print(f"Title: {title}")
        
        # Check for login state
        textarea = await page.query_selector('textarea, #prompt-textarea')
        login_btn = await page.query_selector('button:has-text("Log in"), button:has-text("Sign up")')
        
        if login_btn:
            print("STATUS: NEEDS_LOGIN - ChatGPT login page detected")
        elif textarea:
            print("STATUS: LOGGED_IN - Textarea found, ready to send prompts")
        else:
            print("STATUS: UNKNOWN - Page loaded but could not determine state")
            await page.screenshot(path='chatgpt_state.png')
            print("Screenshot saved to chatgpt_state.png")

asyncio.run(main())
