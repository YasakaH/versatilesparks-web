"""Submit HPF v2 framework content to ChatGPT conversation in chunks."""
import asyncio, json, os, time
from playwright.async_api import async_playwright

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE_DIR = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CONV_URL = 'https://chatgpt.com/c/6a52e616-6410-83ee-bf3d-3aac0bdc6f6a'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt'

async def send_chunk(page, chunk_num, text):
    """Send a text chunk to the ChatGPT input."""
    print(f'\n--- Submitting chunk {chunk_num} ---')
    
    # Wait for the input box to be ready
    await page.wait_for_timeout(3000)
    
    # Find the input box using multiple selectors
    input_box = None
    for selector in [
        '#prompt-textarea',
        'textarea[placeholder*="Message"]',
        'textarea[placeholder*="Send"]',
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'div.ProseMirror[role="textbox"]'
    ]:
        try:
            el = await page.wait_for_selector(selector, timeout=5000)
            if el:
                input_box = el
                print(f'Found input with: {selector}')
                break
        except:
            continue
    
    if not input_box:
        print('ERROR: Could not find input box!')
        # Dump page structure for debugging
        html = await page.content()
        # Look for any textarea or contenteditable
        for match in ['textarea', 'contenteditable', 'textbox', 'prompt', 'ProseMirror', 'input']:
            count = html.count(match)
            print(f'  HTML mentions of "{match}": {count}')
        return False
    
    # Click the input box to focus it
    await input_box.click()
    await page.wait_for_timeout(500)
    
    # Type the text character by character (to look human)
    await input_box.fill(text)
    await page.wait_for_timeout(1000)
    
    # Try to click send button
    sent = False
    for send_selector in [
        'button[data-testid="send-button"]',
        'button[aria-label*="Send"]',
        'button[class*="send"]',
        'button[class*="Submit"]',
        'button:has(svg use[href*="send"])'
    ]:
        try:
            send_btn = await page.query_selector(send_selector)
            if send_btn and await send_btn.is_visible():
                await send_btn.click()
                sent = True
                print(f'Clicked send via: {send_selector}')
                break
        except:
            continue
    
    if not sent:
        # Try pressing Enter (Shift+Enter for newline, Enter for send)
        await page.keyboard.press('Enter')
        print('Pressed Enter to send')
    
    print(f'Chunk {chunk_num} submitted. Waiting for response...')
    return True

async def main():
    async with async_playwright() as p:
        print('Launching Brave with your profile...')
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            executable_path=BRAVE_PATH,
            headless=False,
            args=['--disable-blink-features=AutomationControlled', '--no-first-run']
        )

        page = await context.new_page()
        
        # First chunk: send the overview
        print(f'Navigating to conversation: {CONV_URL}')
        await page.goto(CONV_URL, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(10000)
        
        # Read and send the first chunk
        chunk_path = os.path.join(CHUNKS_DIR, '00-HPFv2-Overview.md')
        if os.path.exists(chunk_path):
            with open(chunk_path, 'r', encoding='utf-8') as f:
                content = f.read()
            await send_chunk(page, 1, content)
        
        # Wait for response (keep browser open for user to see)
        print('\nFirst chunk sent! Keeping browser open for you...')
        print('The browser will stay open until you close it.')
        await page.wait_for_timeout(300000)  # 5 minutes
        await context.close()

asyncio.run(main())
