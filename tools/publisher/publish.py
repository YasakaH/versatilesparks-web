#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tools.publisher.config import load_config
from tools.publisher.models import Article
from tools.publisher.adapters.devto import DevtoPublisher
from tools.publisher.adapters.medium import MediumPublisher
from tools.publisher.adapters.website import WebsitePublisher
from tools.publisher.adapters.github import GitHubPublisher

PUBLISHERS = {
    "devto": DevtoPublisher(),
    "medium": MediumPublisher(),
    "website": WebsitePublisher(),
    "github": GitHubPublisher(),
}

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def emit_feedback(
    source: str,
    signal_type: str,
    payload: dict,
    domain: str = "publisher",
) -> Path:
    """Write a feedback record for HPF (flat directory, domain in metadata)."""
    feedback_dir = REPO_ROOT / "knowledge" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "id": f"{domain}-{signal_type}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source": source,
        "domain": domain,
        "domain_hierarchy": {
            "primary": domain,
            "medium": source,
            "channel": signal_type,
        },
        "signal_type": signal_type,
        "payload": payload,
        "received": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "processed": False,
        "notes": None,
    }
    path = feedback_dir / f"{record['id']}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return path


def find_matching_brief(slug: str) -> dict | None:
    manifest_path = REPO_ROOT / "articles" / "json" / "manifest.json"
    if not manifest_path.exists():
        return None
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = raw if isinstance(raw, list) else raw.get("articles", [])
    for entry in entries:
        if entry.get("slug") == slug:
            return entry
    return None


def move_draft_to_published(file: Path):
    published_dir = REPO_ROOT / "articles" / "published"
    published_dir.mkdir(parents=True, exist_ok=True)
    dest = published_dir / file.name
    file.rename(dest)
    return dest


def main():
    parser = argparse.ArgumentParser(description="Publish articles to platforms")
    parser.add_argument("platform", choices=list(PUBLISHERS.keys()) + ["all"])
    parser.add_argument("file", help="Path to the article markdown file")
    parser.add_argument("--id", help="Article ID for update/delete")
    parser.add_argument("--action", choices=["publish", "update", "delete"], default="publish")
    parser.add_argument("--draft", action="store_true", help="Publish as draft (unlisted)")
    parser.add_argument("--feedback", action="store_true", help="Emit feedback records for HPF")
    parser.add_argument("--views", type=int, default=0, help="Article views (for feedback)")
    parser.add_argument("--reads", type=int, default=0, help="Article reads (for feedback)")
    parser.add_argument("--book-clicks", type=int, default=0, help="Gumroad link clicks (for feedback)")
    parser.add_argument("--sales", type=int, default=0, help="Book sales attributed (for feedback)")
    args = parser.parse_args()

    config = load_config()

    file_path = Path(args.file)
    slug = file_path.stem
    brief = find_matching_brief(slug)

    if args.action == "delete":
        if not args.id:
            print("error: --id required for delete action")
            sys.exit(1)
        platforms = [args.platform] if args.platform != "all" else list(PUBLISHERS.keys())
        for name in platforms:
            publisher = PUBLISHERS[name]
            publisher.delete(config, args.id)
            print(f"deleted from {name}")
        return

    article = Article.from_file(str(file_path))
    if args.draft:
        article.published = False

    platforms = [args.platform] if args.platform != "all" else list(PUBLISHERS.keys())
    results = {}
    all_ok = True
    for name in platforms:
        publisher = PUBLISHERS[name]
        try:
            if args.action == "update" and args.id:
                result = publisher.update(article, config, args.id)
            else:
                result = publisher.publish(article, config)
            results[name] = result
            print(f"ok  {name}: {result}")
        except Exception as e:
            results[name] = str(e)
            all_ok = False
            print(f"err {name}: {e}")

    if all_ok and not args.draft and args.action == "publish":
        published_path = move_draft_to_published(file_path)
        print(f"Moved to published/: {published_path.name}")

    if args.feedback:
        base_payload = {
            "article_slug": slug,
            "platforms": platforms,
            "brief_id": brief.get("id", slug) if brief else slug,
            "concepts": brief.get("concepts", []) if brief else [],
            "action": args.action,
            "is_draft": args.draft,
        }

        if all_ok:
            feedback_payload = {
                **base_payload,
                "result": "published" if not args.draft else "draft",
                "performance": {
                    "views": args.views,
                    "reads": args.reads,
                    "book_clicks": args.book_clicks,
                    "sales": args.sales,
                },
                "questions": [],
                "new_aliases": [],
            }
            p = emit_feedback("publisher", "article_published", feedback_payload)
            print(f"Feedback: {p.name}")
        else:
            errors = {k: v for k, v in results.items() if isinstance(v, str)}
            feedback_payload = {
                **base_payload,
                "result": "failed",
                "errors": errors,
            }
            p = emit_feedback("publisher", "publish_failure", feedback_payload)
            print(f"Feedback (error): {p.name}")

    return results


if __name__ == "__main__":
    main()
