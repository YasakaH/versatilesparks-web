class GithubStats:
    """Collect repo-level stats (stars, etc.).

    Requires GITHUB_PAT in .env. Returns [] when not configured.
    """

    name = "github"

    def __init__(self, pat: str | None):
        self.pat = pat

    def collect(self) -> list[dict]:
        if not self.pat:
            return []
        raise NotImplementedError("GitHub collection not implemented yet")
