class SearchConsoleStats:
    """Collect Google Search Console stats.

    Requires GSC OAuth credentials. Returns [] when not configured.
    """

    name = "search_console"

    def __init__(self, credentials: str | None = None):
        self.credentials = credentials

    def collect(self) -> list[dict]:
        if not self.credentials:
            return []
        raise NotImplementedError("Search Console collection not implemented yet")
