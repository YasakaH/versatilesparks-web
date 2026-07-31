import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = '''I need you to craft premium SD3 image prompts for a Python Browser Automation Cookbook.

Context: Product is Python Browser Automation Cookbook (nodriver v0.50.3), $29-$59, for developers. Dark navy/cyber aesthetic, Stripe/Linear level premium quality.

5 images needed. All 16:9 SD3 digital-art. No text. No sci-fi/robots. Colors: dark navy bg (#020617), cyan (#22d3ee) and amber (#fbbf24) accents.

1. Hero background - abstract geometric dark navy with subtle grid, cyan/amber flowing light shapes suggesting code and data. Premium, minimal, expensive-looking.

2. Selector priority - 5-level hierarchy: data-testid>id>name>CSS class>XPath. Layered pyramid.

3. Stop vs Retry decision flow - operation fails, temporary? retry? success? continue. Green paths, red stop.

4. Pagination safety - 3 parallel stop conditions converging. No next button, disabled, MAX_PAGES.

5. Download lifecycle pipeline - click>temp>growing>rename>done.

Give me the EXACT Stability AI SD3 prompt for each image. Detailed, specific, premium.'''

async def send():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        page = browser.contexts[0].pages[0]
        await asyncio.sleep(2)
        # Find input using Playwright selectors
        input_area = await page.wait_for_selector('#prompt-textarea', timeout=10000)
        if input_area:
            await input_area.fill(MSG)
            await asyncio.sleep(1)
            send_btn = await page.query_selector('button[data-testid="send-button"]')
            if send_btn:
                await send_btn.click()
                print('Sent!')
            else:
                # Try pressing Enter
                await input_area.press('Enter')
                print('Sent via Enter')
        else:
            print('No input found')

asyncio.run(send())
