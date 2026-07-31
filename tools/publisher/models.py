from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import frontmatter


@dataclass
class Article:
    title: str
    description: str
    body_markdown: str
    tags: list[str] = field(default_factory=list)
    published: bool = False
    date: Optional[datetime] = None
    canonical_url: Optional[str] = None
    cover_image: Optional[str] = None
    series: Optional[str] = None
    slug: Optional[str] = None

    @classmethod
    def from_file(cls, path: str) -> "Article":
        with open(path, encoding="utf-8") as f:
            post = frontmatter.load(f)
        metadata = post.metadata
        return cls(
            title=metadata.get("title", ""),
            description=metadata.get("description", ""),
            body_markdown=post.content,
            tags=metadata.get("tags", []),
            published=metadata.get("published", False),
            date=metadata.get("date"),
            canonical_url=metadata.get("canonical_url"),
            cover_image=metadata.get("cover_image"),
            series=metadata.get("series"),
            slug=metadata.get("slug"),
        )
