"""Launch Brave with its profile to access ChatGPT."""
import asyncio, json
from playwright.async_api import async_playwright

BRAVE_PATH = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
PROFILE_DIR = r'C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data'

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            executable_path=BRAVE_PATH,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
            ]
        )

        page = await context.new_page()
        print('Launching Brave with your profile...')
        await page.goto('https://chatgpt.com/', wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(30000)

        state = await page.evaluate("""() => ({
            title: document.title,
            url: window.location.href,
            hasLoginForm: document.body.innerText.includes("Log in") && document.body.innerText.includes("Sign up"),
            preview: document.body.innerText.substring(0, 400)
        })""")
        print(f'State: {json.dumps(state, indent=2)}')

        # Navigate to conversation
        await page.goto('https://chatgpt.com/c/6a52e616-6410-83ee-bf3d-3aac0bdc6f6a', 
                       wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(10000)
        print(f'Conversation URL: {page.url}')

        # Keep open for user to see
        await page.wait_for_timeout(120000)
        await context.close()

asyncio.run(main())
