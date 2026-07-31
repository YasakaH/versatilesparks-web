"""
Fill LinkedIn, Fiverr, Instamojo profiles using existing logged-in tabs.
"""
import asyncio, json, time
from playwright.async_api import async_playwright

CDP_PORT = 9235

async def fill(page, sel, val, timeout=8000):
    try:
        el = await page.wait_for_selector(sel, timeout=timeout)
        await el.click()
        await asyncio.sleep(0.3)
        await el.fill('')
        await el.fill(val)
        return True
    except:
        return False

async def click_text(page, text, timeout=5000):
    try:
        el = await page.wait_for_selector(f'text="{text}"', timeout=timeout)
        await el.click()
        return True
    except:
        try:
            el = await page.wait_for_selector(f'text={text}', timeout=3000)
            await el.click()
            return True
        except:
            return False

async def safe_goto(page, url, timeout=15000):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=timeout)
        await asyncio.sleep(3)
        return True
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'http://localhost:{CDP_PORT}')
        ctx = browser.contexts[0]
        tabs = {i: pg for i, pg in enumerate(ctx.pages)}
        
        # ======= LINKEDIN (Tab 2) =======
        li = tabs[2]
        print('=== LINKEDIN ===')
        await li.bring_to_front()
        
        # Profile edit
        await safe_goto(li, 'https://www.linkedin.com/in/edit/intro')
        
        h = await fill(li, 'input[name="headline"]', 
            'I automate repetitive business work with AI & Python | Browser automation | Document workflows | Lead automation | Helping small businesses save hours every week')
        print(f'  Headline: {"✓" if h else "✗"}')
        
        await safe_goto(li, 'https://www.linkedin.com/in/edit/forms/summary/')
        about = '''Most small businesses spend hours every week on repetitive work\u2014copying data, downloading reports, updating spreadsheets, and processing documents.

I build practical automations using Python, AI, and browser automation that remove those repetitive tasks.

Typical projects include:
\u2022 Browser automation for repetitive web tasks
\u2022 AI-assisted document processing
\u2022 Excel and reporting automation
\u2022 Lead capture and follow-up workflows
\u2022 Telegram and messaging automation

My goal is simple: automate the work that people should not have to do manually.'''
        a = await fill(li, '#summary', about)
        print(f'  About: {"✓" if a else "✗"}')
        
        # Add profile picture placeholder text
        print('  LinkedIn: Add a profile photo manually')
        
        # ======= FIVERR (Tabs 0 and 3) =======
        print('\n=== FIVERR ===')
        fiv = tabs[0]  # Gig editor
        fiv2 = tabs[3]  # Dashboard
        
        await fiv2.bring_to_front()
        
        # Go to profile edit
        await safe_goto(fiv2, 'https://www.fiverr.com/users/yasaka_h/edit')
        
        # Description
        desc = 'I help businesses eliminate repetitive work using AI and Python automation. Specializing in browser automation, document processing, lead management, and Telegram bots.'
        d = await fill(fiv2, 'textarea[name="description"]', desc)
        print(f'  Description: {"✓" if d else "✗"}')
        
        # Set up the gig in the gig editor tab
        await tabs[0].bring_to_front()
        await asyncio.sleep(2)
        
        # Gig title
        t = await fill(tabs[0], 'input[name="title"]', 
            'I will automate your repetitive business tasks using AI and Python')
        print(f'  Gig title: {"✓" if t else "✗"}')
        
        # Gig description
        gd = await fill(tabs[0], 'textarea[name="description"]',
            'I help businesses eliminate repetitive manual work using AI and Python automation.\n\nI build practical solutions for:\n- Browser automation (data entry, report downloads, form filling)\n- Document processing (PDF extraction, Excel automation)\n- Lead management (capture, follow-up, CRM integration)\n- Chatbots (Telegram, WhatsApp, website)\n- Workflow automation (connecting apps, scheduling)\n\nHow it works:\n1. You describe the repetitive task\n2. I build the automation\n3. You save hours every week\n\nAll solutions are custom-built for your specific needs.')
        print(f'  Gig description: {"✓" if gd else "✗"}')
        
        print('\nFiverr: User needs to set pricing ($25-$100) and publish the gig')
        
        # ======= INSTAMOJO (Tab 4) =======
        print('\n=== INSTAMOJO ===')
        inst = tabs[4]
        await inst.bring_to_front()
        await asyncio.sleep(2)
        
        # If on onboarding, fill business details
        if 'onboarding' in inst.url:
            # Fill business name
            await fill(inst, 'input[name="business_name"]', 'Yasaka Automation')
            await fill(inst, 'input[name="phone"]', '')  # User fills
            print('  Onboarding: business name set, user fills phone + KYC')
        
        print('\nInstamojo: User needs to complete KYC (PAN + bank), then add product')
        
        # ======= SUMMARY =======
        print('\n' + '='*50)
        print('DONE — Profiles partially filled')
        print('='*50)
        print('Still needs you:')
        print('  1. LinkedIn: Add profile photo, complete onboarding')
        print('  2. Fiverr: Set gig pricing + publish')
        print('  3. Instamojo: KYC + upload product')
        print('  4. Record 30s demo videos from money-maker/demos/')

asyncio.run(main())
