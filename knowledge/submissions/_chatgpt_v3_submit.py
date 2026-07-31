"""HPF v2 ChatGPT submission v3 — robust pipeline with recovery"""
import asyncio, os, sys
from playwright.async_api import async_playwright, TimeoutError as PwTimeout

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt_v2'
CONV_URL = 'https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7'
CDP_PORT = 9225

async def click_send(page):
    """Try multiple ways to click send"""
    for sel in ['[data-testid="send-button"]', 'button[type="submit"]', 'button:has(svg)', 'button:has-text("Send")']:
        try:
            btn = await page.wait_for_selector(sel, timeout=3000)
            if btn:
                is_disabled = await btn.get_attribute('disabled')
                if not is_disabled:
                    await btn.click()
                    return True
        except:
            continue
    # Fallback: Ctrl+Enter
    await page.keyboard.press('Control+Enter')
    return True

async def wait_for_response(page, timeout_sec=120):
    """Wait for a new assistant message to appear"""
    prev_count = await page.evaluate('''() => {
        return document.querySelectorAll('[data-message-author-role="assistant"]').length;
    }''')
    
    for i in range(timeout_sec // 5):
        await asyncio.sleep(5)
        current = await page.evaluate('''() => {
            return document.querySelectorAll('[data-message-author-role="assistant"]').length;
        }''')
        if current > prev_count:
            await asyncio.sleep(10)  # Let it finish generating
            return True
        # Check for stop button (means generating)
        stop_btn = await page.query_selector('[data-testid="stop-button"]')
        if stop_btn:
            continue
    return False

async def send_to_chatgpt(page, text):
    """Type text and send to ChatGPT"""
    textarea = await page.wait_for_selector('#prompt-textarea', timeout=15000)
    # Clear and fill
    await textarea.click()
    await asyncio.sleep(1)
    await textarea.fill('')
    await asyncio.sleep(1)
    await textarea.fill(text)
    await asyncio.sleep(2)
    await click_send(page)
    return True

async def extract_all_messages(page):
    """Scroll up and extract all messages in the conversation"""
    # Try scrolling up to load history
    for _ in range(5):
        await page.evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(2)
    
    data = await page.evaluate('''() => {
        const msgs = document.querySelectorAll('[data-message-author-role]');
        return Array.from(msgs).map(m => ({
            role: m.getAttribute('data-message-author-role'),
            text: m.innerText
        }));
    }''')
    return data

async def main():
    start_chunk = None
    
    async with async_playwright() as p:
        print(f'Launching Brave (CDP port {CDP_PORT})...')
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE,
            executable_path=BRAVE_PATH,
            headless=False,
            args=[f'--remote-debugging-port={CDP_PORT}']
        )
        page = await browser.new_page()
        
        print(f'Navigating to {CONV_URL}...')
        await page.goto(CONV_URL, wait_until='domcontentloaded')
        await asyncio.sleep(10)
        
        # Dismiss any modals/popups
        try:
            close_btn = await page.wait_for_selector('[aria-label="Close"]', timeout=3000)
            await close_btn.click()
            await asyncio.sleep(1)
        except:
            pass
        
        # See what's already in the conversation
        existing = await extract_all_messages(page)
        assistant_count = len([m for m in existing if m['role'] == 'assistant'])
        print(f'Existing messages: {len(existing)} ({assistant_count} assistant)')
        
        # Determine which chunks to send
        all_chunks = sorted([f for f in os.listdir(CHUNKS_DIR) if f.endswith('.md')])
        
        for chunk_file in all_chunks:
            filepath = os.path.join(CHUNKS_DIR, chunk_file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split large chunks
            if len(content) > 14000:
                parts = [content[i:i+13000] for i in range(0, len(content), 13000)]
            else:
                parts = [content]
            
            for pi, part in enumerate(parts):
                label = f"{chunk_file}" if len(parts) == 1 else f"{chunk_file} (part {pi+1}/{len(parts)})"
                print(f'\n📤 {label} ({len(part)} chars)')
                
                try:
                    success = await send_to_chatgpt(page, part)
                    if not success:
                        print(f'  ⚠️ Send failed, retrying...')
                        await asyncio.sleep(5)
                        success = await send_to_chatgpt(page, part)
                    
                    print(f'  ⏳ Waiting for response...')
                    got_response = await wait_for_response(page, 180)
                    
                    if got_response:
                        print(f'  ✅ Response received')
                    else:
                        print(f'  ⚠️ No response detected, continuing...')
                    
                    # Save progress
                    msgs = await extract_all_messages(page)
                    a_count = len([m for m in msgs if m['role'] == 'assistant'])
                    print(f'  📝 {len(msgs)} messages ({a_count} assistant)')
                    
                except Exception as e:
                    print(f'  ❌ Error: {e}')
                    await asyncio.sleep(10)
                    continue
        
        print(f'\n✅ All chunks sent!')
        print(f'🌐 Brave stays open on port {CDP_PORT}')
        
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
