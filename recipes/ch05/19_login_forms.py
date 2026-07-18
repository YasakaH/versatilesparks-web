"""
Recipe 19 (revised): Log In and Verify Authentication

Submit a login form and verify that authentication actually
succeeded before continuing automation.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger

USERNAME = "demo@example.com"
PASSWORD = "correct-horse-battery-staple"


async def login_succeeded(page) -> bool:
    """Verify authentication succeeded using multiple signals."""

    # 1. Logout button present
    logout = await page.find("[data-testid='logout']", timeout=2)
    if logout:
        return True

    # 2. Account menu / avatar visible
    account = await page.find("[data-testid='account-menu']", timeout=2)
    if account:
        return True

    # 3. URL changed to dashboard
    url = await page.evaluate("location.href")
    if "/dashboard" in url or "/account" in url:
        return True

    return False


async def captcha_detected(page) -> bool:
    """Detect common signs automation has been challenged."""
    challenge = await page.find(
        "iframe[title*='captcha'], iframe[src*='recaptcha']",
        timeout=2,
    )
    return challenge is not None


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://httpbin.org/forms/post")

        await (await page.find("input[name='custname']")).send_keys(USERNAME)
        await (await page.find("input[name='custtel']")).send_keys(PASSWORD)
        await (await page.find("button[type='submit']")).click()

        if await captcha_detected(page):
            logger.error("CAPTCHA detected. Stopping automation.")
            return

        if not await login_succeeded(page):
            logger.error("Login verification failed.")
            return

        logger.info("Login verified successfully.")
        print("Authenticated and ready.")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
