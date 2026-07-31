import requests


class DevtoStats:
    name = "devto"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _headers(self) -> dict:
        return {"api-key": self.api_key}

    def collect(self) -> list[dict]:
        """Fetch stats for all published articles of the authenticated user."""
        articles = []
        page = 1
        while True:
            resp = requests.get(
                "https://dev.to/api/articles/me/all",
                headers=self._headers(),
                params={"per_page": 100, "page": page},
            )
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            for a in batch:
                articles.append(
                    {
                        "article_id": a["id"],
                        "slug": a.get("slug", ""),
                        "url": a.get("url"),
                        "canonical_url": a.get("canonical_url"),
                        "published_at": a.get("published_at"),
                        "views": a.get("page_views_count", 0) or 0,
                        "reactions": a.get("public_reactions_count", 0) or 0,
                        "positive_reactions": a.get("positive_reactions_count", 0) or 0,
                        "comments": a.get("comments_count", 0) or 0,
                    }
                )
            if len(batch) < 100:
                break
            page += 1

        self.account = self._account_analytics()
        return articles

    def _account_analytics(self) -> dict:
        """Account-wide totals plus read time (analytics API)."""
        result = {"totals": {}, "historical": {}}
        from datetime import datetime, timedelta, timezone

        today = datetime.now(timezone.utc)
        start = (today - timedelta(days=14)).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
        try:
            resp = requests.get(
                "https://dev.to/api/analytics/totals",
                headers=self._headers(),
                timeout=15,
            )
            if resp.ok:
                result["totals"] = resp.json()
        except requests.RequestException:
            pass
        try:
            resp = requests.get(
                "https://dev.to/api/analytics/historical",
                headers=self._headers(),
                params={"start": start, "end": end},
                timeout=15,
            )
            if resp.ok:
                result["historical"] = resp.json()
        except requests.RequestException:
            pass
        return result
