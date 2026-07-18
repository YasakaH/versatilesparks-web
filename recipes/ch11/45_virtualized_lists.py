"""
Recipe 45 (V2): Automate Virtualized Lists

Modern apps (Gmail, Slack, dashboards) render only visible rows.
You must scroll, collect, and detect when all items are loaded.
"""
import asyncio
import nodriver as uc


async def collect_virtualized(page, container_sel, item_sel):
    items = []
    prev_count = -1
    while len(items) != prev_count:
        prev_count = len(items)
        elements = await page.find_all(item_sel)
        for el in elements:
            text = await el.text
            if text and text not in items:
                items.append(text)
        await page.scroll_into_view(container_sel, bottom=True)
        await page.sleep(1)
    return items


async def main():
    browser = await uc.start()
    # page = await browser.get("https://example.com/list")
    # items = await collect_virtualized(page, "#scroll-container", ".item")
    # print(f"Collected {len(items)} items")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
