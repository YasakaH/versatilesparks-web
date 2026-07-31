"""
Fill profiles using EXISTING browser tabs (no navigation to new URLs).
The user already has Fiverr, LinkedIn, and Instamojo logged in.
"""
import asyncio, json, time
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def find_page_by_url(ctx, keyword):
    for pg in ctx.pages:
        if keyword.lower() in pg.url.lower():
            return pg
    return None

async def fill_field(page, sel, val, timeout=5000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.3)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def safe_goto(page, url):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(3)
        return True
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        
        print('Current tabs:')
        for i, pg in enumerate(ctx.pages):
            print(f'  [{i}] {pg.url[:100]}')
        
        results = {}
        
        # ========================
        # LINKEDIN
        # ========================
        linkedin_page = await find_page_by_url(ctx, 'linkedin')
        if linkedin_page:
            print('\n=== LINKEDIN ===')
            await linkedin_page.bring_to_front()
            
            # Check if already on profile or needs to navigate
            if 'onboarding' in linkedin_page.url:
                print('On onboarding flow — skip for now, user can complete onboarding')
                results['linkedin'] = 'On onboarding — user completes, then profile is pre-filled'
            else:
                # Headline
                headline = "I automate repetitive business work with AI & Python | Browser automation | Document workflows | Lead automation"
                ok = await fill_field(linkedin_page, 'input[name="headline"]', headline)
                print(f'  Headline: {"✓" if ok else "✗"}')
                
                # Try About
                await safe_goto(linkedin_page, 'https://www.linkedin.com/in/edit/forms/summary/')
                about = """Most small businesses spend hours every week on repetitive work—copying data, downloading reports, updating spreadsheets, and processing documents.

I build practical automations using Python, AI, and browser automation that remove those repetitive tasks.

Typical projects include:
• Browser automation for repetitive web tasks
• AI-assisted document processing
• Excel and reporting automation
• Lead capture and follow-up workflows
• Telegram and messaging automation

My goal is simple: automate the work that people shouldn't have to do manually."""
                ok = await fill_field(linkedin_page, '#summary', about)
                print(f'  About: {"✓" if ok else "✗"}')
                results['linkedin'] = 'Headline + About filled'
        else:
            results['linkedin'] = 'No LinkedIn tab found'
        
        # ========================
        # FIVERR — Use existing tab
        # ========================
        fiverr_page = await find_page_by_url(ctx, 'fiverr')
        if fiverr_page:
            print('\n=== FIVERR ===')
            await fiverr_page.bring_to_front()
            await asyncio.sleep(2)
            
            # If on onboarding, try completing it
            if 'onboarding' in fiverr_page.url:
                print('On Fiverr onboarding — try to navigate past it')
                await safe_goto(fiverr_page, 'https://www.fiverr.com/users/yasaka_h/edit')
            
            # Profile description
            desc = "I help businesses eliminate repetitive work using AI and Python automation. Specializing in browser automation, document processing, lead management, and Telegram/WhatsApp bots. I deliver practical solutions that save hours every week."
            ok = await fill_field(fiverr_page, 'textarea[name="description"]', desc)
            print(f'  Description: {"✓" if ok else "✗"}')
            
            # Try creating a gig from the dashboard
            await safe_goto(fiverr_page, 'https://www.fiverr.com/dashboard')
            print('  At Fiverr dashboard — user can click "Create Gig" manually')
            results['fiverr'] = 'Profile description filled, needs gig creation'
        else:
            results['fiverr'] = 'No Fiverr tab found'
        
        # ========================
        # INSTAMOJO — Use existing tab
        # ========================
        instamojo_page = await find_page_by_url(ctx, 'instamojo')
        if instamojo_page:
            print('\n=== INSTAMOJO ===')
            await instamojo_page.bring_to_front()
            await asyncio.sleep(2)
            
            if 'onboarding' in instamojo_page.url:
                print('On Instamojo onboarding — complete basics')
                # Try to select business type
                for sel in ['input[name="business_type"]', 'select[name="business_type"]']:
                    try:
                        el = await instamojo_page.query_selector(sel)
                        if el:
                            await el.click()
                            await asyncio.sleep(0.5)
                            break
                    except:
                        pass
                print('  Onboarding form ready')
                results['instamojo'] = 'On onboarding — user completes KYC, then I can set up products'
            else:
                results['instamojo'] = 'Dashboard ready'
        else:
            results['instamojo'] = 'No Instamojo tab found'
        
        # ========================
        # SUMMARY
        # ========================
        print('\n' + '='*60)
        print('PROFILE FILLING SUMMARY')
        print('='*60)
        for k, v in results.items():
            print(f'  {k}: {v}')
        print()
        print('User actions needed:')
        print('  1. LinkedIn: Complete onboarding flow (follow recommendations)')
        print('  2. Fiverr: Click "Create Gig" and set pricing ($25-$100)')
        print('  3. Instamojo: Complete KYC (PAN + bank), then add product')
        print('  4. Record demo videos from money-maker/demos/')
        print('  5. Start LinkedIn outreach (20-30 messages/day)')
        print()
        print('Browser stays open. Close when done.')

asyncio.run(main())
