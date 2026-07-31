from pathlib import Path
from ..publisher import Publisher
from ..models import Article


class GitHubPublisher(Publisher):
    name = "github"

    def __init__(self, docs_dir: str = "docs/articles"):
        self.docs_dir = Path(docs_dir)

    def publish(self, article: Article, config: dict) -> str:
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        slug = article.slug or article.title.lower().replace(" ", "-").replace("/", "-")
        filepath = self.docs_dir / f"{slug}.md"
        filepath.write_text(
            f"""---
title: {article.title}
description: {article.description}
tags: {article.tags}
date: {article.date.isoformat() if article.date else ""}
---

{article.body_markdown}
""",
            encoding="utf-8",
        )
        return str(filepath)

    def update(self, article: Article, config: dict, article_id: str) -> str:
        return self.publish(article, config)

    def delete(self, config: dict, article_id: str) -> None:
        path = Path(article_id)
        if path.exists():
            path.unlink()
