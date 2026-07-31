"""HPF v2 ChatGPT submission pipeline v2 - parallel loop"""
import asyncio, os, sys
from playwright.async_api import async_playwright

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt_v2'
CONV_URL = 'https://chatgpt.com/c/6a532496-848c-83ee-9ef6-030394f6eec7'  # Active thread
OUTPUT = r'C:\Users\varas\personalities\_chatgpt_v2_responses.txt'
CDP_PORT = 9224

MAX_CHUNK_SIZE = 15000  # Max chars per chunk for ChatGPT

async def submit_chunk(page, content, chunk_name):
    """Submit a single chunk and wait for response."""
    print(f"\n{'='*60}")
    print(f"CHUNK: {chunk_name} ({len(content)} chars)")
    print(f"{'='*60}")
    
    # Find and fill textarea
    textarea = await page.wait_for_selector('#prompt-textarea', timeout=20000)
    await textarea.click()
    await textarea.fill(content)
    await asyncio.sleep(2)
    
    # Click send button
    send_btn = await page.wait_for_selector('[data-testid="send-button"]', timeout=10000)
    await send_btn.click()
    print("✅ Sent! Saving responses periodically...")
    
    # Wait for response to appear
    prev_assistant = 0
    for wait_cycle in range(10):  # ~5 min total
        await asyncio.sleep(30)
        messages = await page.evaluate('''() => {
            const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
            return msgs.length;
        }''')
        if messages > prev_assistant:
            print(f"  Response detected! ({messages} total)")
            await asyncio.sleep(15)  # Let it finish
            return True
        print(f"  Waiting... ({30*(wait_cycle+1)}s)")
    
    print("  Warning: No new response detected within time limit")
    return False

async def main():
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    # Get sorted chunks
    all_chunks = sorted([f for f in os.listdir(CHUNKS_DIR) if f.endswith('.md') and f != 'MANIFEST.json'])
    
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE,
            executable_path=BRAVE_PATH,
            headless=False,
            args=[f'--remote-debugging-port={CDP_PORT}']
        )
        page = await browser.new_page()
        
        print(f"Navigating to {CONV_URL}...")
        await page.goto(CONV_URL, wait_until='domcontentloaded')
        await asyncio.sleep(10)
        
        for i, chunk_file in enumerate(all_chunks):
            idx = all_chunks.index(chunk_file) + 1
            if idx < start_from:
                continue
            
            filepath = os.path.join(CHUNKS_DIR, chunk_file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split large chunks
            if len(content) > MAX_CHUNK_SIZE:
                print(f"  Splitting {chunk_file} ({len(content)} chars) into parts...")
                # Split by file boundaries
                parts = content.split('\n### ')
                part_batches = []
                current = ""
                for part in parts:
                    if len(current) + len(part) > MAX_CHUNK_SIZE and current:
                        part_batches.append(current)
                        current = part
                    else:
                        current = current + ('\n### ' + part if current else part)
                if current:
                    part_batches.append(current)
                
                for pi, batch in enumerate(part_batches):
                    name = f"{chunk_file.replace('.md','')} (part {pi+1}/{len(part_batches)})"
                    await submit_chunk(page, batch, name)
            else:
                await submit_chunk(page, content, chunk_file)
            
            # Save responses after each chunk
            await asyncio.sleep(5)
            messages = await page.evaluate('''() => {
                const msgs = document.querySelectorAll('[data-message-author-role]');
                return Array.from(msgs).map(m => ({
                    role: m.getAttribute('data-message-author-role'),
                    text: m.innerText.substring(0, 1000)
                }));
            }''')
            
            assistant_count = len([m for m in messages if m['role'] == 'assistant'])
            print(f"📝 So far: {len(messages)} messages ({assistant_count} assistant responses)")
        
        print(f"\n{'='*60}")
        print(f"✅ All {len(all_chunks)} chunks submitted!")
        print(f"🌐 Brave stays open. Extract responses via CDP.")
        print(f"{'='*60}")
        
        # Keep alive until user closes
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
