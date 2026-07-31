#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from tools.publisher.config import load_config
from tools.publisher.publish import emit_feedback
from tools.publisher.metrics.devto import DevtoStats
from tools.publisher.metrics.gumroad import GumroadStats
from tools.publisher.metrics.search_console import SearchConsoleStats
from tools.publisher.metrics.github import GithubStats

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RAW_DIR = REPO_ROOT / "metrics" / "raw"


def snapshot_path(date: str) -> Path:
    return RAW_DIR / f"{date}.json"


def write_snapshot(date: str, sources: dict, force: bool) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = snapshot_path(date)
    if path.exists() and not force:
        raise FileExistsError(
            f"{path.name} already exists (immutable snapshot). Use --force to overwrite."
        )
    snapshot = {
        "date": date,
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": sources,
    }
    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return path


def emit_performance_feedback(articles: list[dict]) -> None:
    for a in articles:
        payload = {
            "article_id": a.get("article_id"),
            "article_slug": a.get("slug"),
            "platform": a.get("platform"),
            "url": a.get("url"),
            "canonical_url": a.get("canonical_url"),
            "performance": {
                "views": a.get("views", 0),
                "reactions": a.get("reactions", 0),
                "comments": a.get("comments", 0),
            },
            "questions": [],
            "new_aliases": [],
        }
        emit_feedback(a.get("platform", "publisher"), "metrics_snapshot", payload)


def main():
    parser = argparse.ArgumentParser(description="Collect performance metrics snapshots")
    parser.add_argument("--devto", action="store_true", help="Collect Dev.to stats")
    parser.add_argument("--gumroad", action="store_true", help="Collect Gumroad referrals")
    parser.add_argument("--search-console", action="store_true", help="Collect Search Console stats")
    parser.add_argument("--github", action="store_true", help="Collect GitHub repo stats")
    parser.add_argument("--all", action="store_true", help="Collect from all configured sources")
    parser.add_argument("--force", action="store_true", help="Overwrite existing snapshot for today")
    parser.add_argument("--no-feedback", action="store_true", help="Skip FeedbackRecord emission")
    args = parser.parse_args()

    config = load_config()

    requested = [
        name
        for name, flag in (
            ("devto", args.devto),
            ("gumroad", args.gumroad),
            ("search_console", args.search_console),
            ("github", args.github),
        )
        if flag
    ]
    if args.all:
        requested = ["devto", "gumroad", "search_console", "github"]
    if not requested:
        parser.error("no source specified (use --devto, --gumroad, ... or --all)")

    collectors = {
        "devto": DevtoStats(config.get("devto_api_key") or ""),
        "gumroad": GumroadStats(os.getenv("GUMROAD_TOKEN")),
        "search_console": SearchConsoleStats(os.getenv("GSC_CREDENTIALS")),
        "github": GithubStats(config.get("github_pat")),
    }

    articles: list[dict] = []
    account: dict = {}
    active: list[str] = []
    for name in requested:
        collector = collectors[name]
        try:
            stats = collector.collect()
        except NotImplementedError as e:
            print(f"skip {name}: {e}")
            continue
        if not stats:
            print(f"skip {name}: not configured")
            continue
        for s in stats:
            s["platform"] = name
            articles.append(s)
        if hasattr(collector, "account"):
            account[name] = collector.account
        active.append(name)
        print(f"ok   {name}: {len(stats)} articles")

    if not articles:
        print("nothing collected — no snapshot written")
        return 1

    sources: dict = {}
    for name in active:
        entry: dict = {"articles": [a for a in articles if a.get("platform") == name]}
        if name in account:
            entry["account"] = account[name]
        sources[name] = entry

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        path = write_snapshot(date, sources, args.force)
    except FileExistsError as e:
        print(f"err  {e}")
        return 1
    print(f"wrote {path.relative_to(REPO_ROOT)}")

    if not args.no_feedback:
        emit_performance_feedback(articles)
        print(f"feedback: {len(articles)} metric records emitted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
