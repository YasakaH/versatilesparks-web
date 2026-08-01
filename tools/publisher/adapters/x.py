#!/usr/bin/env python3
"""X / Twitter thread publisher (OAuth 1.0a, API v2).

Posts a derivative thread file (x-thread.md or x-post.md) from
articles/derivatives/<slug>/ as a chained thread on X.

Usage:
  python tools/publisher/adapters/x.py --slug why-browser-profiles-break --dry-run
  python tools/publisher/adapters/x.py --slug why-browser-profiles-break --post

Credentials come from the cookbook or hermes .env:
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
"""
import argparse
import hashlib
import hmac
import os
import random
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

API_URL = "https://api.x.com/2/tweets"

REPO_ROOT = Path(__file__).resolve().parents[3]
DERIVATIVES = REPO_ROOT / "articles" / "derivatives"

THREAD_HEADER = re.compile(r"^\*\*Tweet \d+\*\*$", re.MULTILINE)


def _load_dotenv():
    from dotenv import load_dotenv

    for env_path in [REPO_ROOT / ".env", Path.home() / "AppData/Local/hermes/.env"]:
        if env_path.exists():
            load_dotenv(env_path)


def _percent_encode(value: str) -> str:
    return urllib.parse.quote(value, safe="-._~")


def _oauth_header(method: str, url: str, params: dict, config: dict) -> dict:
    consumer_key = config["x_api_key"]
    consumer_secret = config["x_api_secret"]
    access_token = config["x_access_token"]
    access_secret = config["x_access_token_secret"]

    oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": "".join(random.choices("0123456789abcdef", k=32)),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }

    all_params = dict(oauth_params)
    all_params.update({k: str(v) for k, v in params.items() if v is not None})
    sorted_params = "&".join(
        f"{_percent_encode(k)}={_percent_encode(v)}"
        for k, v in sorted(all_params.items())
    )
    base_string = "&".join(
        [method.upper(), _percent_encode(url), _percent_encode(sorted_params)]
    )
    signing_key = "&".join([_percent_encode(consumer_secret), _percent_encode(access_secret)])
    signature = hmac.new(
        signing_key.encode(), base_string.encode(), hashlib.sha1
    ).digest()
    oauth_params["oauth_signature"] = __import__("base64").b64encode(signature).decode()

    header = "OAuth " + ", ".join(
        f'{_percent_encode(k)}="{_percent_encode(v)}"'
        for k, v in sorted(oauth_params.items())
    )
    return {"Authorization": header, "Content-Type": "application/json"}


def post_tweet(text: str, config: dict, reply_to: str | None = None) -> str:
    payload = {"text": text}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    resp = requests.post(
        API_URL,
        json=payload,
        headers=_oauth_header("POST", API_URL, {}, config),
    )
    if not resp.ok:
        raise Exception(f"X API {resp.status_code}: {resp.text[:500]}")
    return resp.json()["data"]["id"]


def post_thread(texts: list[str], config: dict) -> list[str]:
    ids = []
    for text in texts:
        ids.append(post_tweet(text, config, reply_to=ids[-1] if ids else None))
    return ids


def parse_thread_file(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    first = THREAD_HEADER.search(content)
    if not first:
        return [content.strip()]
    body = content[first.end():]
    blocks = re.split(r"(?m)^\*\*Tweet \d+\*\*\s*$", body)
    return [b.strip() for b in blocks if b.strip()]


def load_config() -> dict:
    _load_dotenv()
    required = [
        "x_api_key",
        "x_api_secret",
        "x_access_token",
        "x_access_token_secret",
    ]
    config = {
        "x_api_key": os.getenv("X_API_KEY"),
        "x_api_secret": os.getenv("X_API_SECRET"),
        "x_access_token": os.getenv("X_ACCESS_TOKEN"),
        "x_access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET"),
    }
    missing = [k for k in required if not config.get(k)]
    if missing:
        sys.exit(f"error: missing env vars: {', '.join(m.upper() for m in missing)}")
    return config


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Post an X thread from a derivative file")
    parser.add_argument("--slug", help="Article slug (finds x-thread.md / x-post.md)")
    parser.add_argument("--file", help="Explicit path to the thread file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="Print tweets without posting")
    group.add_argument("--post", action="store_true", help="Actually post to X")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
    elif args.slug:
        thread = DERIVATIVES / args.slug / "x-thread.md"
        single = DERIVATIVES / args.slug / "x-post.md"
        path = thread if thread.exists() else single
    else:
        parser.error("provide --slug or --file")

    if not path.exists():
        sys.exit(f"error: no thread file at {path}")

    tweets = parse_thread_file(path)
    print(f"{len(tweets)} tweet(s) from {path.name}")
    for i, t in enumerate(tweets, 1):
        print(f"\n--- Tweet {i} ({len(t)} chars) ---\n{t}")

    if not args.post:
        print("\n(dry run — pass --post to publish)")
        return

    if len(tweets) > 8:
        sys.exit("error: refusing to post more than 8 tweets; split the thread")

    config = load_config()
    ids = post_thread(tweets, config)
    print(f"posted: https://x.com/i/status/{ids[0]}")


if __name__ == "__main__":
    main()
