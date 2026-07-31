"""
ChatGPT Feedback Pipeline v2 — Fixed bottlenecks.

Fixes:
1. Isolated browser (fresh Chromium, doesn't touch existing Brave)
2. Background-safe (runs independently, doesn't crash on other work)
3. Automated feed → read → debate → return
"""
import asyncio, json, os, sys, time, re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PwTimeout

FOR_CHATGPT = r"E:\Hermes Projects\_for_chatgpt"
FEEDBACK_DIR = r"E:\Hermes Projects\cookbook\knowledge\archived-personas\_chatgpt_feedback"
PROFILE_DIR = r'C:\Users\varas\AppData\Local\Temp\chatgpt-pipeline-profile'
OUTPUT_FILE = r'C:\Users\varas\personalities\_chatgpt_feedback.json'

async def wait_for_response(page, timeout=300):
    """Wait for ChatGPT to finish generating — robust detection with fallbacks."""
    # Wait for the stop button to appear (means generation started)
    try:
        await page.wait_for_selector(
            'button[data-testid="stop-button"], button[aria-label="Stop generating"]',
            timeout=15000
        )
        print('[WAIT] Generation started (stop button visible)...')
    except:
        print('[WAIT] No stop button — response might already be done')

    # Now wait for send button to become enabled (means generation finished)
    try:
        await page.wait_for_function(
            '() => { const btn = document.querySelector(\'[data-testid="send-button"]\'); return btn && !btn.disabled; }',
            timeout=timeout * 1000
        )
        print('[WAIT] Generation finished (send button re-enabled)')
    except PwTimeout:
        print('[WARN] Response timeout — may be incomplete')

    await asyncio.sleep(3)

    # Get the last assistant message via multiple fallback selectors
    response = await page.evaluate('''
        () => {
            const articles = document.querySelectorAll('article');
            if (articles.length > 0) {
                return articles[articles.length - 1].innerText;
            }
            const msgs = document.querySelectorAll('div[data-message-author-role="assistant"]');
            if (msgs.length > 0) {
                return msgs[msgs.length - 1].innerText;
            }
            const prose = document.querySelectorAll('.markdown, .prose, [class*="message"]');
            if (prose.length > 0) {
                return prose[prose.length - 1].innerText;
            }
            return '';
        }
    ''')
    return response

async def send_message(page, text):
    """Send a message to ChatGPT and wait for response."""
    ta = await page.wait_for_selector('#prompt-textarea', timeout=20000)
    await ta.click()
    await asyncio.sleep(0.3)
    await ta.fill(text)
    await asyncio.sleep(0.5)

    btn = await page.wait_for_selector('[data-testid="send-button"]:not([disabled])', timeout=15000)
    await btn.click()

    print('[SENT] Message sent, waiting for response...')
    response = await wait_for_response(page)

    # Fallback: if empty, try extracting main area text
    if not response or len(response.strip()) < 20:
        print('[WARN] Short response, trying alternate extraction...')
        await asyncio.sleep(5)
        response = await page.evaluate('''
            () => {
                const main = document.querySelector('main') || document.querySelector('[role="main"]') || document.body;
                return main.innerText.split('\\n').slice(-200).join('\\n');
            }
        ''')
    return response

async def navigate_with_retry(page, url, max_attempts=5):
    """Navigate with retry for Cloudflare flakiness."""
    await page.add_init_script('''
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    ''')
    for attempt in range(max_attempts):
        print(f'[NAV] Attempt {attempt+1}/{max_attempts}...')
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(5)
            has_textarea = await page.query_selector('#prompt-textarea')
            if has_textarea:
                print(f'[NAV] Connected')
                return True
            if 'login' in page.url.lower() or 'auth' in page.url.lower():
                print('[AUTH] Login page detected.')
                return False
            print(f'[NAV] Blocked/error (attempt {attempt+1})')
        except Exception as e:
            print(f'[NAV] Error (attempt {attempt+1}): {e}')
        if attempt < max_attempts - 1:
            await asyncio.sleep(min(3 * (attempt + 1), 15))
    return False

async def main():
    import re, time
    from pathlib import Path

    content_file = sys.argv[1] if len(sys.argv) > 1 else None
    debate_mode = '--debate' in sys.argv

    if not content_file:
        print('Usage: python chatgpt_pipeline_v2.py <content_file> [--debate]')
        sys.exit(1)

    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()

    source_name = Path(content_file).stem
    print(f'[START] Pipeline for: {content_file}')
    print(f'[INFO] Content size: {len(content)} chars')

    os.makedirs(PROFILE_DIR, exist_ok=True)

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            args=[
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-sync',
                '--disable-blink-features=AutomationControlled',
            ],
            viewport={'width': 1280, 'height': 800},
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        ok = await navigate_with_retry(page, 'https://chatgpt.com')
        if not ok:
            print('[FAIL] Could not reach ChatGPT.')
            await ctx.close()
            sys.exit(1)

        await asyncio.sleep(3)

        prompt = f"""Please review the following content and provide detailed feedback, improvements, and corrections. Be thorough and constructive.

=== CONTENT TO REVIEW ===

{content}

=== END ===

Please give me:
1. Overall assessment
2. Specific feedback on each section
3. Suggestions for improvement
4. Any corrections needed
5. Rating (1-10) for clarity, completeness, and value

Keep the feedback focused and actionable."""

        print('[SEND] Sending content to ChatGPT...')
        response = await send_message(page, prompt)

        result = {
            'file': content_file,
            'response_preview': response[:2000] if response else 'No response',
            'response_length': len(response) if response else 0,
            'timestamp': time.time()
        }

        # Save JSON output
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump([result], f, indent=2, ensure_ascii=False)
        print(f'\n[DONE] Response saved to {OUTPUT_FILE}')
        print(f'[DONE] Response length: {result["response_length"]} chars')

        # Also save markdown to feedback dir
        if response:
            safe_name = re.sub(r'[^\w\-]', '_', source_name)
            feedback_path = os.path.join(FEEDBACK_DIR, f"{safe_name}___feedback.md")
            os.makedirs(FEEDBACK_DIR, exist_ok=True)
            feedback_content = f"""# ChatGPT Feedback: {source_name}

> Submitted: {time.strftime('%Y-%m-%d %H:%M:%S')}
> Source: {content_file}

---

{response}
"""
            with open(feedback_path, 'w', encoding='utf-8') as f:
                f.write(feedback_content)
            print(f'[SAVED] Feedback also written to {feedback_path}')

        # Keep browser open for review if --debate flag
        if debate_mode:
            print('\n[DEBATE] Debate mode — browser stays open. Press Ctrl+C when done.')
            try:
                while True:
                    await asyncio.sleep(10)
            except KeyboardInterrupt:
                pass

        await ctx.close()
        print('[CLEANUP] Browser closed')

if __name__ == '__main__':
    asyncio.run(main())
