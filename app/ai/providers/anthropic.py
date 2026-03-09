import json
import logging

from app.ai.providers.base import AiProvider, ParseResult
from app.ai.schemas import ChatMessage

logger = logging.getLogger(__name__)

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


class AnthropicProvider(AiProvider):
    def name(self) -> str:
        return "anthropic"

    def build_headers(self, api_key: str) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        }

    def build_url(self, model: str, api_key: str) -> str:
        return API_URL

    def build_body(
        self, messages: list[ChatMessage], model: str, max_tokens: int, temperature: float
    ) -> dict:
        return {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }

    def parse_line(self, data: str) -> ParseResult:
        try:
            node = json.loads(data)
            event_type = node.get("type", "")

            if event_type == "message_start":
                pt = node.get("message", {}).get("usage", {}).get("input_tokens", 0)
                return ParseResult(prompt_tokens=pt)
            elif event_type == "content_block_delta":
                text = node.get("delta", {}).get("text", "")
                return ParseResult(text=text or None)
            elif event_type == "message_delta":
                ct = node.get("usage", {}).get("output_tokens", 0)
                return ParseResult(completion_tokens=ct)
            elif event_type == "message_stop":
                return ParseResult(is_done=True)
            return ParseResult()
        except Exception:
            logger.debug("Anthropic 파싱 무시: %s", data)
            return ParseResult()
