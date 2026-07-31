"""HPF v2 ChatGPT submission v5 — robust, patient, saves everything"""
import asyncio, os, json, time
from playwright.async_api import async_playwright

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt_v2'
CONV_URL = 'https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7'
CDP_PORT = 9229
PROGRESS_FILE = r'C:\Users\varas\personalities\_chatgpt_progress.json'
RESPONSES_FILE = r'C:\Users\varas\personalities\_chatgpt_all_responses.txt'

async def send_and_wait(page, text, timeout=600):
    """Send text, wait for response, return True if response detected"""
    ta = await page.wait_for_selector('#prompt-textarea', timeout=20000)
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
                d = await btn.get_attribute('disabled')
                if not d:
                    await btn.click()
                    break
        except:
            continue
    else:
        await page.keyboard.press('Control+Enter')
    
    # Wait for response with multiple detection methods
    start = time.time()
    prev_count = await page.evaluate(
        'document.querySelectorAll(\'[data-message-author-role="assistant"]\').length'
    )
    
    while time.time() - start < timeout:
        await asyncio.sleep(5)
        
        # Method 1: New assistant message appeared
        current = await page.evaluate(
            'document.querySelectorAll(\'[data-message-author-role="assistant"]\').length'
        )
        if current > prev_count:
            print(f'  ✅ New message detected ({current} total)')
            await asyncio.sleep(8)
            return True
        
        # Method 2: Stop button present means still generating
        stop = await page.query_selector('[data-testid="stop-button"]')
        if stop:
            continue
        
        # Method 3: Textarea enabled means generation done
        ta = await page.query_selector('#prompt-textarea')
        if ta:
            d = await ta.get_attribute('disabled')
            if not d:
                await asyncio.sleep(5)
                return True
        
        # Method 4: Check if error / rate limit page
        body = await page.evaluate('document.body.innerText.substring(0,200)')
        if 'rate limit' in body.lower() or 'too many' in body.lower():
            print('  ⚠️ Rate limited! Waiting 60s...')
            await asyncio.sleep(60)
    
    return False

async def save_all_responses(page):
    """Save all messages to file"""
    msgs = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('[data-message-author-role]')).map(m => ({
            role: m.getAttribute('data-message-author-role'),
            text: m.innerText
        }));
    }''')
    with open(RESPONSES_FILE, 'w', encoding='utf-8') as f:
        for m in msgs:
            f.write(f'\n{"="*60}\n[{m["role"].upper()}]\n{"="*60}\n{m["text"]}\n')
    print(f'  💾 All responses saved ({len(msgs)} messages)')
    return msgs

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE,
            executable_path=BRAVE_PATH,
            headless=False,
            args=[f'--remote-debugging-port={CDP_PORT}']
        )
        page = await browser.new_page()
        await page.goto(CONV_URL, wait_until='domcontentloaded')
        await asyncio.sleep(10)
        
        # Load progress
        sent_chunks = set()
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE) as f:
                sent_chunks = set(json.load(f).get('sent', []))
        print(f'Sent so far: {len(sent_chunks)} chunks')
        
        all_chunks = sorted([f for f in os.listdir(CHUNKS_DIR) if f.endswith('.md')])
        print(f'Total chunks: {len(all_chunks)}')
        
        for chunk_file in all_chunks:
            if chunk_file in sent_chunks:
                print(f'⏭️ {chunk_file} already sent')
                continue
            
            with open(os.path.join(CHUNKS_DIR, chunk_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split large chunks
            parts = [content[i:i+14000] for i in range(0, len(content), 14000)] if len(content) > 14000 else [content]
            
            for pi, part in enumerate(parts):
                label = chunk_file.replace('.md','') if len(parts) == 1 else f"{chunk_file.replace('.md','')} (p{pi+1}/{len(parts)})"
                print(f'\n{"="*50}')
                print(f'📤 {label} ({len(part)} chars)')
                
                success = False
                retries = 3
                while retries > 0 and not success:
                    try:
                        result = await send_and_wait(page, part, timeout=600)
                        if result:
                            success = True
                        else:
                            retries -= 1
                            if retries > 0:
                                print(f'  🔄 No response, retrying ({retries} left)...')
                                await asyncio.sleep(10)
                            else:
                                print(f'  ⚠️ Giving up after timeout, saving what we have')
                                success = True  # move on
                    except Exception as e:
                        retries -= 1
                        print(f'  ❌ Error: {e}')
                        if retries > 0:
                            await asyncio.sleep(20)
                
                await save_all_responses(page)
            
            # Mark chunk sent
            sent_chunks.add(chunk_file)
            with open(PROGRESS_FILE, 'w') as f:
                json.dump({'sent': list(sent_chunks), 'last': chunk_file}, f)
            print(f'✅ {len(sent_chunks)}/{len(all_chunks)} chunks done')
        
        print(f'\n🎉 ALL {len(all_chunks)} CHUNKS SENT!')
        await save_all_responses(page)
        
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
