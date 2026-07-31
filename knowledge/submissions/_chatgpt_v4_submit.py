"""HPF v2 ChatGPT submission v4 — robust response detection"""
import asyncio, os, json
from playwright.async_api import async_playwright, TimeoutError as PwTimeout

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt_v2'
CONV_URL = 'https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7'
CDP_PORT = 9227
PROGRESS_FILE = r'C:\Users\varas\personalities\_chatgpt_progress.json'

async def wait_generating_done(page, timeout=300):
    """Wait until ChatGPT finishes generating (stop btn gone, textarea enabled)"""
    for _ in range(timeout):
        await asyncio.sleep(2)
        # Check if stop button is present → generating
        stop = await page.query_selector('[data-testid="stop-button"]')
        if stop:
            continue  # still generating
        # Check if textarea is enabled → done
        ta = await page.query_selector('#prompt-textarea')
        if ta:
            disabled = await ta.get_attribute('disabled')
            if not disabled:
                await asyncio.sleep(3)
                return True
    return False

async def get_all_messages(page):
    """Get all messages from the conversation"""
    data = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('[data-message-author-role]')).map(m => ({
            role: m.getAttribute('data-message-author-role'),
            text: m.innerText
        }));
    }''')
    return data

async def send_chunk(page, text):
    """Send a chunk to ChatGPT"""
    ta = await page.wait_for_selector('#prompt-textarea', timeout=15000)
    await ta.click()
    await asyncio.sleep(1)
    await ta.fill('')
    await asyncio.sleep(1)
    await ta.fill(text)
    await asyncio.sleep(2)
    # Click send
    for sel in ['[data-testid="send-button"]', 'button[aria-label="Send prompt"]', 'button[type="submit"]']:
        try:
            btn = await page.query_selector(sel)
            if btn:
                disabled = await btn.get_attribute('disabled')
                if not disabled:
                    await btn.click()
                    return True
        except:
            continue
    await page.keyboard.press('Control+Enter')
    return True

async def main():
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
        
        # Load progress
        sent_chunks = set()
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE) as f:
                sent_chunks = set(json.load(f).get('sent', []))
            print(f'Resuming: {len(sent_chunks)} chunks already sent')
        
        all_chunks = sorted([f for f in os.listdir(CHUNKS_DIR) if f.endswith('.md')])
        
        for chunk_file in all_chunks:
            if chunk_file in sent_chunks:
                print(f'⏭️ Skipping {chunk_file} (already sent)')
                continue
            
            filepath = os.path.join(CHUNKS_DIR, chunk_file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split if large
            parts = [content[i:i+14000] for i in range(0, len(content), 14000)] if len(content) > 14000 else [content]
            
            for pi, part in enumerate(parts):
                label = chunk_file.replace('.md', '') if len(parts) == 1 else f"{chunk_file.replace('.md','')} (part {pi+1}/{len(parts)})"
                print(f'\n📤 {label} ({len(part)} chars)')
                
                try:
                    ok = await send_chunk(page, part)
                    if not ok:
                        print('  ⚠️ Send failed, retrying...')
                        await asyncio.sleep(5)
                        await send_chunk(page, part)
                    
                    print('  ⏳ Waiting for generation to finish...')
                    done = await wait_generating_done(page, 300)
                    
                    if done:
                        print('  ✅ Response received!')
                    else:
                        print('  ⚠️ Timeout waiting for response, continuing...')
                    
                    msgs = await get_all_messages(page)
                    print(f'  📝 {len(msgs)} messages total')
                    
                except Exception as e:
                    print(f'  ❌ Error: {e}')
                    await asyncio.sleep(15)
            
            # Mark chunk as sent
            sent_chunks.add(chunk_file)
            with open(PROGRESS_FILE, 'w') as f:
                json.dump({'sent': list(sent_chunks), 'last': chunk_file}, f)
            print(f'  💾 Progress saved: {len(sent_chunks)}/{len(all_chunks)} chunks')
        
        print(f'\n✅ All {len(all_chunks)} chunks sent!')
        
        # Final save
        msgs = await get_all_messages(page)
        with open(r'C:\Users\varas\personalities\_chatgpt_all_responses.txt', 'w', encoding='utf-8') as f:
            for m in msgs:
                f.write(f'\n--- [{m["role"]}] ---\n{m["text"]}\n')
        print(f'📁 All responses saved to _chatgpt_all_responses.txt')
        
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
