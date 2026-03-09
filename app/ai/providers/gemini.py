import json
import logging

from app.ai.providers.base import AiProvider, ParseResult
from app.ai.schemas import ChatMessage

logger = logging.getLogger(__name__)

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key}"


class GeminiProvider(AiProvider):
    def name(self) -> str:
        return "gemini"

    def build_headers(self, api_key: str) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def build_url(self, model: str, api_key: str) -> str:
        return API_URL.format(model=model, api_key=api_key)

    def build_body(
        self, messages: list[ChatMessage], model: str, max_tokens: int, temperature: float
    ) -> dict:
        contents = []
        for msg in messages:
            role = "model" if msg.role == "assistant" else msg.role
            contents.append({"role": role, "parts": [{"text": msg.content}]})
        return {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }

    def parse_line(self, data: str) -> ParseResult:
        try:
            node = json.loads(data)
            candidates = node.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    text = parts[0].get("text")
                    if text:
                        usage_meta = node.get("usageMetadata", {})
                        return ParseResult(
                            text=text,
                            prompt_tokens=usage_meta.get("promptTokenCount", 0),
                            completion_tokens=usage_meta.get("candidatesTokenCount", 0),
                        )
                finish_reason = candidates[0].get("finishReason")
                if finish_reason == "STOP":
                    return ParseResult(is_done=True)
            return ParseResult()
        except Exception:
            logger.debug("Gemini 파싱 무시: %s", data)
            return ParseResult()
