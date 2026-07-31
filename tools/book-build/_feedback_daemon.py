"""
Hermes Persistent Feedback Loop — cron-ready.
Runs every new-content check and processes through ChatGPT.
"""
import asyncio, json, os, sys, time
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PwTimeout

CDP_PORT = 9230
PROFILE_DIR = Path(os.environ.get('CHATGPT_PROFILE', 
    r'C:\Users\varas\AppData\Local\Temp\chatgpt-pipeline-profile'))
FEEDBACK_DIR = Path(r'C:\Users\varas\personalities\_for_chatgpt')
RESPONSES_DIR = Path(r'C:\Users\varas\personalities\_chatgpt_responses')

def get_pending_content():
    """Find files in _for_chatgpt/ that haven't been processed yet."""
    responses_dir = Path(r'C:\Users\varas\personalities\_chatgpt_feedback')
    processed = set()
    if responses_dir.exists():
        for f in responses_dir.glob('*'):
            processed.add(f.stem)
    
    pending = []
    if FEEDBACK_DIR.exists():
        for f in sorted(FEEDBACK_DIR.glob('*.md')):
            if f.stem not in processed:
                pending.append(f)
    return pending

async def send_to_chatgpt(page, content: str):
    """Send content to ChatGPT and get response."""
    ta = await page.wait_for_selector('#prompt-textarea', timeout=15000)
    await ta.click()
    await asyncio.sleep(0.3)
    await ta.fill(content)
    await asyncio.sleep(0.5)
    
    btn = await page.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=30000)
    await btn.click()
    
    # Wait for response
    await page.wait_for_function(
        '() => document.querySelector(\'[data-testid="send-button"]\') && !document.querySelector(\'[data-testid="send-button"]\').disabled',
        timeout=180000
    )
    await asyncio.sleep(2)
    
    # Get response text
    response = await page.evaluate('''
        () => {
            const articles = document.querySelectorAll('article');
            const last = articles[articles.length - 1];
            return last ? last.innerText.substring(0, 100000) : '';
        }
    ''')
    return response

async def main():
    pending = get_pending_content()
    print(f'[FEEDBACK] {len(pending)} items pending review')
    
    if not pending:
        print('[FEEDBACK] Nothing to process')
        return
    
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                f'--remote-debugging-port={CDP_PORT}',
                f'--user-data-dir={str(PROFILE_DIR)}',
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )
        try:
            ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await ctx.new_page()
            await page.goto('https://chat.openai.com', wait_until='domcontentloaded')
            
            if 'login' in page.url.lower():
                print('[AUTH] Please log in...')
                await page.wait_for_url('**/chat/**', timeout=300000)
            
            for item in pending:
                print(f'[FEEDBACK] Processing: {item.name}')
                content = item.read_text(encoding='utf-8')[:30000]  # Keep under 30K chars
                
                prompt = f"Please review and provide improvement suggestions for the following:\n\n{content}"
                response = await send_to_chatgpt(page, prompt)
                
                # Save response
                output = RESPONSES_DIR / f'{item.stem}_response.md'
                output.write_text(f'# Response for: {item.name}\n\n{response}', encoding='utf-8')
                print(f'[FEEDBACK] Saved: {output.name}')
                
                await asyncio.sleep(5)  # Rate limit between chunks
            
            print(f'[FEEDBACK] Done. Processed {len(pending)} items')
            
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
