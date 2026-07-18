"""
Recipe 54 (V2): Incremental Scraping

Problem: Full rescrapes waste bandwidth and time. Track content
hashes to collect only what changed since the last run.
"""
import asyncio, hashlib, json
from pathlib import Path
import nodriver as uc

STATE = Path("scrape_state.json")


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2))


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


async def scrape_if_changed(url):
    state = load_state()
    browser = await uc.start(headless=True)
    page = await browser.get(url)
    text = await page.evaluate("document.body.innerText")
    await browser.stop()

    h = content_hash(text)
    if state.get(url) == h:
        return False  # nothing changed
    state[url] = h
    save_state(state)
    return True  # updated


async def main():
    urls = ["https://example.com", "https://httpbin.org"]
    for url in urls:
        changed = await scrape_if_changed(url)
        print(f"{'UPDATED' if changed else 'SKIPPED'}: {url}")
    print(f"State: {len(load_state())} URLs tracked")


if __name__ == "__main__":
    asyncio.run(main())
