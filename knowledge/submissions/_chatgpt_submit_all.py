"""Submit HPF v2 chunks to ChatGPT, save responses between each chunk."""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE_DIR = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'
CONV_URL = 'https://chatgpt.com/c/6a52e616-6410-83ee-bf3d-3aac0bdc6f6a'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt'
OUTPUT_FILE = r'C:\Users\varas\personalities\_chatgpt_responses.txt'

CHUNKS = [
    ('00-HPFv2-Overview.md', 'Architecture Overview'),
    ('01-CORE-Documents.md', '16 CORE Documents'),
    ('02-BASE-PERSONALITY-Schema.md', 'Base Personality Schema'),
    ('03-Persona-Inventory.md', '34 Persona Inventory'),
    ('04-Governance-Eval-Plugin-CapReg.md', 'Governance, Eval, Plugin API'),
    ('05-Policies-and-Architecture-Questions.md', 'Policies & Design Questions'),
]

async def extract_assistant_responses(page):
    """Extract all assistant responses from the conversation."""
    try:
        texts = await page.evaluate('''
            () => {
                const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                const result = [];
                for (const m of msgs) {
                    result.push(m.innerText);
                }
                return result;
            }
        ''')
        return texts if texts else []
    except Exception as e:
        print(f'  Error extracting responses: {e}')
        return []

def save_responses(responses, output_file):
    """Save responses to file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, resp in enumerate(responses):
            f.write(f'\n===== ChatGPT Response {i+1} =====\n')
            f.write(resp)
            f.write('\n')
    print(f'Saved {len(responses)} responses to {output_file}')

async def main():
    start_chunk = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    async with async_playwright() as p:
        print(f'Launching Brave with CDP (start chunk {start_chunk+1}/{len(CHUNKS)})...')
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            executable_path=BRAVE_PATH,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--remote-debugging-port=9223',  # CDP port for external connection
            ]
        )
        page = await context.new_page()
        page.set_default_timeout(30000)
        
        print('Navigating to conversation...')
        await page.goto(CONV_URL, wait_until='domcontentloaded')
        await page.wait_for_timeout(10000)
        
        # Extract any existing responses first (from previous chunks)
        existing = await extract_assistant_responses(page)
        if existing:
            print(f'Found {len(existing)} existing assistant responses')
            save_responses(existing, OUTPUT_FILE)
        
        for i in range(start_chunk, len(CHUNKS)):
            filename, description = CHUNKS[i]
            chunk_path = os.path.join(CHUNKS_DIR, filename)
            
            if not os.path.exists(chunk_path):
                print(f'WARNING: {filename} not found, skipping')
                continue
            
            with open(chunk_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f'\n{"="*60}')
            print(f'CHUNK {i+1}/{len(CHUNKS)}: {description} ({len(content)} chars)')
            print(f'{"="*60}')
            
            # Find input box
            input_box = None
            for selector in ['#prompt-textarea', 'textarea[placeholder*="Message"]', 'div[contenteditable="true"]']:
                try:
                    el = await page.wait_for_selector(selector, timeout=5000)
                    if el:
                        input_box = el
                        break
                except:
                    continue
            
            if not input_box:
                print('ERROR: No input box. Aborting.')
                await page.screenshot(path='/c/Users/varas/personalities/_chatgpt_error.png')
                break
            
            await input_box.click()
            await page.wait_for_timeout(500)
            await input_box.fill(content)
            await page.wait_for_timeout(1000)
            
            # Send
            sent = False
            for send_sel in ['button[data-testid="send-button"]', 'button[aria-label*="Send"]']:
                try:
                    btn = await page.query_selector(send_sel)
                    if btn and await btn.is_visible():
                        await btn.click()
                        sent = True
                        break
                except:
                    continue
            if not sent:
                await page.keyboard.press('Enter')
            
            print('✅ Sent! Waiting 120s for response...')
            await page.wait_for_timeout(120000)
            
            # Extract ALL responses (include the new one)
            latest = await extract_assistant_responses(page)
            save_responses(latest, OUTPUT_FILE)
            
            print(f'📝 Total responses saved: {len(latest)}')
        
        # Final extraction
        final = await extract_assistant_responses(page)
        save_responses(final, OUTPUT_FILE)
        
        print(f'\n✅ All {len(CHUNKS)} chunks submitted!')
        print('📁 Responses saved to _chatgpt_responses.txt')
        print('🌐 Brave stays open. Close it manually when done.')
        
        # Keep open indefinitely
        while True:
            await page.wait_for_timeout(60000)

asyncio.run(main())
