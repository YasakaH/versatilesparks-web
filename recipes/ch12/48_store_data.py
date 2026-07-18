"""
Recipe 48 (V2): Store Automation Data

Problem: Scraped data needs a home. SQLite provides a portable,
zero-config database that travels with your automation.
"""
import asyncio, sqlite3, json
from pathlib import Path
import nodriver as uc

DB_PATH = Path("automation.db")


def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE NOT NULL,
        title TEXT,
        html_hash TEXT,
        extracted TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON pages(url)")
    conn.commit()
    return conn


def store_page(conn, url, title, data):
    conn.execute(
        "INSERT OR REPLACE INTO pages (url, title, extracted) VALUES (?, ?, ?)",
        (url, title, json.dumps(data))
    )
    conn.commit()


async def main():
    conn = init_db()
    browser = await uc.start()
    page = await browser.get("https://example.com")
    store_page(conn, page.url, await page.title(), {"h1": (await page.find("h1")).text if await page.find("h1") else None})
    conn.close()
    print(f"Stored in {DB_PATH}")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
