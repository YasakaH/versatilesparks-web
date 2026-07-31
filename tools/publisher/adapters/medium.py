import requests
from ..publisher import Publisher
from ..models import Article

API_BASE = "https://api.medium.com/v1"


class MediumPublisher(Publisher):
    name = "medium"

    def _headers(self, config: dict) -> dict:
        return {
            "authorization": f"Bearer {config['medium_token']}",
            "content-type": "application/json",
        }

    def _get_user_id(self, config: dict) -> str:
        resp = requests.get(f"{API_BASE}/me", headers=self._headers(config))
        resp.raise_for_status()
        return resp.json()["data"]["id"]

    def publish(self, article: Article, config: dict) -> str:
        user_id = self._get_user_id(config)
        body = {
            "title": article.title,
            "contentFormat": "markdown",
            "content": article.body_markdown,
            "tags": article.tags,
            "publishStatus": "public" if article.published else "draft",
            "canonicalUrl": article.canonical_url,
        }
        resp = requests.post(
            f"{API_BASE}/users/{user_id}/posts",
            json=body,
            headers=self._headers(config),
        )
        resp.raise_for_status()
        return resp.json()["data"]["id"]

    def update(self, article: Article, config: dict, article_id: str) -> str:
        raise NotImplementedError("Medium API does not support updating posts")

    def delete(self, config: dict, article_id: str) -> None:
        raise NotImplementedError("Medium API does not support deleting posts")
