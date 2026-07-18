"""
Recipe 15: Fill Forms

Enter text into fields, handle checkboxes, radios, and textareas.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://httpbin.org/forms/post")

        # Fill text fields
        custname = await page.find("input[name='custname']")
        await custname.send_keys("Test User")

        tel = await page.find("input[name='custtel']")
        await tel.send_keys("9876543210")

        email = await page.find("input[name='custemail']")
        await email.send_keys("test@example.com")

        # Checkbox
        checkbox = await page.find("input[type='checkbox']")
        await checkbox.click()

        print("Form filled")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
