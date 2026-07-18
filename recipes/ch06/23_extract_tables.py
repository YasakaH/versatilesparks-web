"""
Recipe 23 (revised): Extract Structured Tables

Real HTML tables are imperfect — missing cells, colspan, rowspan.
Normalize your data before saving it.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        rows = await page.find_all("tr")
        data = []

        for row in rows:
            cells = await row.find_all("td, th")
            values = [cell.text.strip() for cell in cells if cell.text.strip()]
            if values:
                data.append(values)

        # Normalize: ensure all rows have same column count
        max_cols = max(len(r) for r in data) if data else 0
        for row in data:
            while len(row) < max_cols:
                row.append(None)

        print(f"Extracted {len(data)} rows ({max_cols} columns)")
        for row in data[:3]:
            print(f"  {row}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
