#!/usr/bin/env python3
"""X / Twitter UI poster (free path — no API credits needed).

Captures a logged-in session once, then posts threads from
articles/derivatives/<slug>/x-thread.md through the X web UI.

Usage:
  python tools/publisher/post_x_ui.py --capture            # login once, saves session
  python tools/publisher/post_x_ui.py --slug <slug> --dry-run
  python tools/publisher/post_x_ui.py --slug <slug> --post
"""
import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from playwright.sync_api import sync_playwright

from tools.publisher.adapters.x import parse_thread_file

DERIVATIVES = REPO_ROOT / "articles" / "derivatives"
SESSION_FILE = REPO_ROOT / "x_session.json"
USERNAME = "fromyasaka"

TWEET_BOX = '[data-testid="tweetTextarea_0"]'
COMPOSE_BUTTON = '[data-testid="SideNav_NewTweet_Button"]'
POST_BUTTON = '[data-testid="tweetButton"]'


def _launch(playwright, headless: bool):
    try:
        return playwright.chromium.launch(channel="msedge", headless=headless)
    except Exception:
        return playwright.chromium.launch(headless=headless)


def capture_session():
    with sync_playwright() as p:
        browser = _launch(p, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://x.com/home")
        deadline = time.time() + 180
        logged_in = False
        while time.time() < deadline:
            try:
                page.wait_for_selector(COMPOSE_BUTTON, timeout=5000)
                logged_in = True
                break
            except Exception:
                pass
        if not logged_in:
            print("timeout: not logged in within 180s — rerun --capture")
            browser.close()
            sys.exit(1)
        context.storage_state(path=str(SESSION_FILE))
        print(f"session saved to {SESSION_FILE}")
        browser.close()


def _newest_tweet_url(page) -> str:
    page.goto(f"https://x.com/{USERNAME}")
    page.wait_for_selector('a[href*="/status/"]', timeout=30000)
    hrefs = page.eval_on_selector_all(
        'a[href*="/status/"]', "els => els.map(e => e.href)"
    )
    hrefs = [h for h in hrefs if f"/{USERNAME}/status/" in h]
    if not hrefs:
        raise Exception("no status links found on profile")
    return hrefs[0]


def _post_text(page, text: str, reply_to: str | None) -> str:
    if reply_to:
        page.goto(reply_to)
        page.wait_for_selector(TWEET_BOX, timeout=30000)
    else:
        page.goto("https://x.com/home")
        page.wait_for_selector(COMPOSE_BUTTON, timeout=30000)
        page.click(COMPOSE_BUTTON)
        page.wait_for_selector(TWEET_BOX, timeout=30000)
    page.click(TWEET_BOX)
    page.keyboard.type(text)
    page.wait_for_timeout(800)
    page.click(POST_BUTTON)
    page.wait_for_timeout(6000)
    return _newest_tweet_url(page)


def post_thread(texts: list[str]):
    with sync_playwright() as p:
        browser = _launch(p, headless=False)
        context = browser.new_context(storage_state=str(SESSION_FILE))
        page = context.new_page()
        url = None
        for text in texts:
            url = _post_text(page, text, url)
            print(f"posted: {url}")
        browser.close()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Post an X thread through the web UI")
    parser.add_argument("--capture", action="store_true", help="Log in and save session")
    parser.add_argument("--slug", help="Article slug (x-thread.md / x-post.md)")
    parser.add_argument("--file", help="Explicit path to the thread file")
    parser.add_argument("--dry-run", action="store_true", help="Print tweets without posting")
    parser.add_argument("--post", action="store_true", help="Actually post")
    args = parser.parse_args()

    if args.capture:
        capture_session()
        return

    if args.file:
        path = Path(args.file)
    elif args.slug:
        thread = DERIVATIVES / args.slug / "x-thread.md"
        single = DERIVATIVES / args.slug / "x-post.md"
        path = thread if thread.exists() else single
    else:
        parser.error("provide --slug, --file, or --capture")

    if not path.exists():
        sys.exit(f"error: no thread file at {path}")

    tweets = parse_thread_file(path)
    print(f"{len(tweets)} tweet(s) from {path.name}")
    for i, t in enumerate(tweets, 1):
        print(f"\n--- Tweet {i} ({len(t)} chars) ---\n{t}")

    if not args.post:
        print("\n(dry run — pass --post to publish)")
        return

    if not SESSION_FILE.exists():
        sys.exit("error: no session — run --capture first")

    if len(tweets) > 8:
        sys.exit("error: refusing to post more than 8 tweets; split the thread")

    post_thread(tweets)


if __name__ == "__main__":
    main()
