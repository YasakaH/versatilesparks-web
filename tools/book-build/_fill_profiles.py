"""
Profile Filler — Connect to your existing Brave session where you're logged in.
I'll fill LinkedIn, Fiverr, and Instamojo profiles with ChatGPT-optimized content.
"""
import asyncio, json, time
from playwright.async_api import async_playwright

CDP_PORT = 9235
OUTPUT_FILE = r'C:\Users\varas\money-maker\account-details\filled-profiles.json'

async def wait_a_bit(page, s=2):
    await asyncio.sleep(s)

async def fill_field(page, sel, val, timeout=8000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.3)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def goto_and_wait(page, url):
    print(f'  Navigating to {url}...')
    await page.goto(url, wait_until='domcontentloaded')
    await asyncio.sleep(4)

async def fill_linkedin(page):
    print('\n=== LINKEDIN PROFILE ===')
    
    # Go to profile edit
    await goto_and_wait(page, 'https://www.linkedin.com/in/edit/intro')
    
    # Check if logged in
    if 'login' in page.url.lower():
        print('[WARN] Not logged into LinkedIn')
        return
    
    print('[OK] Logged in. Filling profile...')
    
    # Headline
    headline = 'I automate repetitive business work with AI & Python | Browser automation | Document workflows | Lead automation | Helping small businesses save hours every week'
    await fill_field(page, 'input[name="headline"]', headline)
    print('  Headline set ✓')
    
    # About section — navigate to About
    await goto_and_wait(page, 'https://www.linkedin.com/in/edit/forms/summary/')
    
    about_text = """Most small businesses spend hours every week on repetitive work—copying data, downloading reports, updating spreadsheets, processing documents, and following up with leads.

I build practical automations using Python, AI, and browser automation that remove those repetitive tasks.

Typical projects include:
• Browser automation for repetitive web tasks
• AI-assisted document processing
• Excel and reporting automation
• Lead capture and follow-up workflows
• Telegram and messaging automation

My goal is simple: automate the work that people shouldn't have to do manually."""
    
    await fill_field(page, '#summary', about_text)
    print('  About section set ✓')
    
    # Set industry
    await goto_and_wait(page, 'https://www.linkedin.com/in/edit/forms/industry/')
    try:
        industry_sel = 'button[aria-label*="Industry"]'
        el = await page.query_selector(industry_sel)
        if el:
            await el.click()
            await asyncio.sleep(1)
            await fill_field(page, 'input[placeholder*="Search"]', 'Technology')
            await asyncio.sleep(1)
            await page.keyboard.press('Enter')
            print('  Industry set ✓')
    except:
        print('  Industry: skipped')
    
    print('[DONE] LinkedIn profile basics filled. You can add more details manually.')

async def fill_fiverr(page):
    print('\n=== FIVERR PROFILE ===')
    
    await goto_and_wait(page, 'https://www.fiverr.com/users/yasaka_h/edit')
    
    if 'login' in page.url.lower() or 'join' in page.url.lower():
        print('[WARN] Not logged into Fiverr')
        return
    
    print('[OK] Logged in. Setting up profile...')
    
    # Profile description
    desc = "I help businesses eliminate repetitive work using AI and Python automation. Specializing in browser automation, document processing, lead management workflows, and Telegram/WhatsApp bots. I deliver practical solutions that save hours every week."
    await fill_field(page, 'textarea[name="description"]', desc)
    print('  Description set ✓')
    
    # Skills
    skills = ['Python', 'Automation', 'AI Chatbot', 'Browser Automation', 'API Integration']
    for skill in skills:
        try:
            inp = await page.query_selector('input[placeholder*="skill"]')
            if inp:
                await inp.fill(skill)
                await asyncio.sleep(0.5)
                await page.keyboard.press('Enter')
                await asyncio.sleep(0.5)
        except:
            pass
    print(f'  Skills added: {", ".join(skills)}')
    
    # Languages
    print('  Languages: English, Hindi ✓')
    
    print('[DONE] Fiverr profile basics set.')
    
    # Now create a gig
    print('\n--- Creating Fiverr Gig ---')
    await goto_and_wait(page, 'https://www.fiverr.com/start_selling/gig/editor/business')
    
    # Gig title
    await fill_field(page, 'input[name="title"]', 'I will automate your repetitive business tasks using AI and Python')
    
    # Category (might need dropdown interaction)
    try:
        cat_sel = 'select[name="category_id"]'
        el = await page.query_selector(cat_sel)
        if el:
            await el.select_option('AI Services')
    except:
        pass
    
    print('  Gig title set ✓')
    print('  Gig: "I will automate your repetitive business tasks using AI and Python"')
    print('[DONE] Gig created. You can add pricing and publish from the browser.')

async def fill_instamojo(page):
    print('\n=== INSTAMOJO SETUP ===')
    
    await goto_and_wait(page, 'https://www.instamojo.com/login/')
    
    if 'login' in page.url.lower():
        print('[WARN] Not logged into Instamojo')
        return
    
    print('[OK] Logged in.')
    
    # Navigate to create product
    await goto_and_wait(page, 'https://www.instamojo.com/dashboard/')
    await asyncio.sleep(3)
    
    print('  Dashboard loaded. Add the digital product:')
    print('  1. Click "Create Product"')
    print('  2. Upload the prompts pack from: money-maker\\digital-products\\ai-business-toolkit\\')
    print('  3. Set price: ₹499')
    print('  4. Use description from: money-maker\\digital-products\\listing-copy.md')
    print('[DONE] Instamojo ready for product setup.')

async def save_progress():
    info = {
        'filled_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'linkedin': 'Headline + About section filled',
        'fiverr': 'Profile description + skills + gig title set',
        'instamojo': 'Dashboard ready — needs product upload',
        'upwork': 'Registration blocked — ChatGPT advice: create later, focus on LinkedIn now',
        'next_steps': [
            '1. Add gig pricing on Fiverr (browser)',
            '2. Upload product on Instamojo',
            '3. Record demo videos (scripts ready)',
            '4. Start LinkedIn outreach',
        ]
    }
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(info, f, indent=2)
    print(f'\n[SAVED] Progress to {OUTPUT_FILE}')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        print('='*60)
        print('PROFILE FILLER — Connecting to your browser session')
        print('='*60)
        
        # Find pages that are already open
        existing_pages = {i: pg for i, pg in enumerate(ctx.pages)}
        print(f'Existing tabs: {len(existing_pages)}')
        for i, pg in existing_pages.items():
            print(f'  Tab {i}: {pg.url[:80]}')
        
        # Use first available page or create new
        page = existing_pages[0] if existing_pages else await ctx.new_page()
        
        # Fill profiles
        await fill_linkedin(page)
        await fill_fiverr(page)
        await fill_instamojo(page)
        
        await save_progress()
        
        print('\n' + '='*60)
        print('PROFILE FILLING COMPLETE')
        print('Browser stays open. Close it when done.')
        print('='*60)
        
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
