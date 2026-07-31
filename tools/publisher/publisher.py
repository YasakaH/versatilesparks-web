from abc import ABC, abstractmethod
from .models import Article


class Publisher(ABC):
    name: str = "base"

    @abstractmethod
    def publish(self, article: Article, config: dict) -> str:
        ...

    @abstractmethod
    def update(self, article: Article, config: dict, article_id: str) -> str:
        ...

    @abstractmethod
    def delete(self, config: dict, article_id: str) -> None:
        ...
