import requests
from ..publisher import Publisher
from ..models import Article

API_BASE = "https://dev.to/api"


class DevtoPublisher(Publisher):
    name = "devto"

    def _headers(self, config: dict) -> dict:
        return {
            "api-key": config["devto_api_key"],
            "content-type": "application/json",
        }

    def publish(self, article: Article, config: dict) -> str:
        body = {
            "article": {
                "title": article.title,
                "description": article.description,
                "body_markdown": article.body_markdown,
                "tags": article.tags[:4],
                "published": article.published,
                "canonical_url": article.canonical_url or None,
                "cover_image": article.cover_image or None,
                "series": article.series or None,
            }
        }
        resp = requests.post(
            f"{API_BASE}/articles",
            json=body,
            headers=self._headers(config),
        )
        if not resp.ok:
            raise Exception(f"422: {resp.text[:500]}")
        return resp.json()["id"]

    def update(self, article: Article, config: dict, article_id: str) -> str:
        body = {
            "article": {
                "title": article.title,
                "description": article.description,
                "body_markdown": article.body_markdown,
                "tags": article.tags[:4],
                "published": article.published,
                "canonical_url": article.canonical_url or None,
                "cover_image": article.cover_image or None,
                "series": article.series or None,
            }
        }
        resp = requests.put(
            f"{API_BASE}/articles/{article_id}",
            json=body,
            headers=self._headers(config),
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def delete(self, config: dict, article_id: str) -> None:
        resp = requests.delete(
            f"{API_BASE}/articles/{article_id}",
            headers=self._headers(config),
        )
        resp.raise_for_status()
