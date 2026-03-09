from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.ai.schemas import ChatMessage


@dataclass
class ParseResult:
    text: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    is_done: bool = False


class AiProvider(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def build_headers(self, api_key: str) -> dict[str, str]: ...

    @abstractmethod
    def build_url(self, model: str, api_key: str) -> str: ...

    @abstractmethod
    def build_body(
        self, messages: list[ChatMessage], model: str, max_tokens: int, temperature: float
    ) -> dict: ...

    @abstractmethod
    def parse_line(self, data: str) -> ParseResult: ...
