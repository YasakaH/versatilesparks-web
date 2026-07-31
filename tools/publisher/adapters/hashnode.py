from ..publisher import Publisher
from ..models import Article


class HashnodePublisher(Publisher):
    name = "hashnode"

    def publish(self, article: Article, config: dict) -> str:
        raise NotImplementedError(
            "Hashnode API publishing requires a Hashnode Pro publication. "
            "See https://hashnode.com/pro"
        )

    def update(self, article: Article, config: dict, article_id: str) -> str:
        raise NotImplementedError("Hashnode API publishing requires Hashnode Pro.")

    def delete(self, config: dict, article_id: str) -> None:
        raise NotImplementedError("Hashnode API publishing requires Hashnode Pro.")
