import json
import logging

from app.ai.providers.base import AiProvider, ParseResult
from app.ai.schemas import ChatMessage

logger = logging.getLogger(__name__)

API_URL = "https://api.openai.com/v1/chat/completions"


class OpenAiProvider(AiProvider):
    def name(self) -> str:
        return "openai"

    def build_headers(self, api_key: str) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
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
            if data.strip() == "[DONE]":
                return ParseResult(is_done=True)
            node = json.loads(data)
            choices = node.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                text = delta.get("content")
                if text:
                    return ParseResult(text=text)
            usage = node.get("usage")
            if usage:
                return ParseResult(
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                )
            return ParseResult()
        except Exception:
            logger.debug("OpenAI 파싱 무시: %s", data)
            return ParseResult()
