from pathlib import Path
from ..publisher import Publisher
from ..models import Article


class WebsitePublisher(Publisher):
    name = "website"

    def __init__(self, content_dir: str = "website-next/content/articles"):
        self.content_dir = Path(content_dir)

    def publish(self, article: Article, config: dict) -> str:
        self.content_dir.mkdir(parents=True, exist_ok=True)
        slug = article.slug or article.title.lower().replace(" ", "-").replace("/", "-")
        filepath = self.content_dir / f"{slug}.mdx"
        tags_yaml = ", ".join(article.tags) if article.tags else ""
        mdx = f"""---
title: {article.title}
description: {article.description}
tags: [{tags_yaml}]
date: {article.date.isoformat() if article.date else ""}
canonical_url: {article.canonical_url or ""}
cover_image: {article.cover_image or ""}
---

{article.body_markdown}
"""
        filepath.write_text(mdx, encoding="utf-8")
        return str(filepath)

    def update(self, article: Article, config: dict, article_id: str) -> str:
        return self.publish(article, config)

    def delete(self, config: dict, article_id: str) -> None:
        path = Path(article_id)
        if path.exists():
            path.unlink()
