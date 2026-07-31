class GumroadStats:
    """Collect Gumroad referral stats.

    Requires GUMROAD_TOKEN in .env. Returns [] when not configured.
    """

    name = "gumroad"

    def __init__(self, token: str | None):
        self.token = token

    def collect(self) -> list[dict]:
        if not self.token:
            return []
        raise NotImplementedError("Gumroad collection not implemented yet")
