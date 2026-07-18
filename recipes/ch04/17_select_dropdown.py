"""
Recipe 17: Select Dropdown Options

Select options from native <select> dropdowns.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://httpbin.org/forms/post")

        # Find the select element
        size_select = await page.find("select")
        await size_select.click()

        # Select an option by visible text
        option = await page.find("option[value='large']")
        await option.click()

        print("Dropdown option selected")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
