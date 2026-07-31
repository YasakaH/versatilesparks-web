import asyncio
from playwright.async_api import async_playwright

CDP_PORT = 9230

MSG = '''I need you to craft premium SD3 image prompts for a Python Browser Automation Cookbook.

Context: Product is Python Browser Automation Cookbook (nodriver v0.50.3), $29-$59, for developers. Dark navy/cyber aesthetic. Target quality: Stripe/Linear level.

5 images needed. All 16:9 SD3 digital-art. No text. No sci-fi/robots. Colors: dark navy bg, cyan and amber accents.

1. Hero background - abstract geometric dark navy with subtle grid, cyan/amber glowing shapes suggesting code flow. Premium, minimal, expensive.

2. Selector priority hierarchy - 5 levels: data-testid (best) to XPath (last resort). Layered pyramid or node cascade.

3. Stop vs Retry decision flowchart - operation fails, temporary? retry within budget? success? continue. Green retry path, red stop path.

4. Pagination safety - 3 parallel stop conditions (no next button, button disabled, MAX_PAGES) converging to STOP.

5. Download lifecycle pipeline - click to temp file to growing to rename to done.

Give me the exact Stability AI SD3 prompt for each image. Be detailed, specific, and premium.'''


async def send():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        page = browser.contexts[0].pages[0]
        await page.bring_to_front()
        # Find and type into ChatGPT input
        input_area = await page.find('#prompt-textarea')
        if not input_area:
            input_area = await page.find('textarea, [contenteditable]')
        await input_area.send_keys(MSG)
        await asyncio.sleep(1)
        # Click send button
        send_btn = await page.find('button[data-testid="send-button"], button[aria-label="Send prompt"]')
        await send_btn.click()
        print('Sent')

asyncio.run(send())
