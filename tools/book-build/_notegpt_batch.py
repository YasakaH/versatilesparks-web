"""Get remaining YouTube transcripts via NoteGPT browser automation"""
import asyncio, os
from playwright.async_api import async_playwright

OUT = r'C:\Users\varas\personalities'
videos = {
    'seo_ai_future': '0hgmb5u6Rh0',
    'competitor_intelligence': '1x3qiGtbhtE',
    'digital_pr_strategy': 'y0DGEa_84Mo',
}

async def get_transcript(page, vid, name):
    path = os.path.join(OUT, f'transcript_{name}.txt')
    if os.path.exists(path):
        print(f'⏭️ {name} already exists')
        return True
    
    await page.goto('https://notegpt.io/youtube-transcript-generator', wait_until='domcontentloaded')
    await asyncio.sleep(5)
    
    input_el = await page.query_selector('input[placeholder*="Paste the YouTube"]')
    if not input_el:
        print(f'❌ {name}: Input not found')
        return False
    
    await input_el.click()
    await asyncio.sleep(1)
    await input_el.fill(f'https://www.youtube.com/watch?v={vid}')
    await asyncio.sleep(2)
    
    gen_btn = await page.query_selector('button:has-text("Generate Transcript")')
    if not gen_btn:
        print(f'❌ {name}: Generate button not found')
        return False
    
    await gen_btn.click()
    print(f'  ⏳ {name}: Generating...')
    await asyncio.sleep(20)
    
    text = await page.evaluate('document.body.innerText')
    idx = text.find('00:01')
    transcript = text[idx:] if idx > 0 else text
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    print(f'  ✅ {name}: {len(transcript)} chars saved')
    return True

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9228')
        page = browser.contexts[0].pages[0]
        
        for name, vid in videos.items():
            await get_transcript(page, vid, name)
            await asyncio.sleep(3)
        
        print(f'\n✅ All done!')

asyncio.run(main())
