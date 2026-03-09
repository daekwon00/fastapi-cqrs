import json
import logging
import uuid
from collections.abc import AsyncGenerator

import httpx

from app.ai.providers.anthropic import AnthropicProvider
from app.ai.providers.base import AiProvider
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.openai import OpenAiProvider
from app.ai.schemas import AiChatEvent, AiChatRequest, AiChatUsage
from app.common.exceptions import BusinessException
from app.config import settings

logger = logging.getLogger(__name__)

PROVIDERS: dict[str, AiProvider] = {
    "anthropic": AnthropicProvider(),
    "openai": OpenAiProvider(),
    "gemini": GeminiProvider(),
}

PROVIDER_CONFIGS: dict[str, dict] = {
    "anthropic": {
        "api_key": lambda: settings.AI_ANTHROPIC_API_KEY,
        "model": lambda: settings.AI_ANTHROPIC_MODEL,
    },
    "openai": {
        "api_key": lambda: settings.AI_OPENAI_API_KEY,
        "model": lambda: settings.AI_OPENAI_MODEL,
    },
    "gemini": {
        "api_key": lambda: settings.AI_GEMINI_API_KEY,
        "model": lambda: settings.AI_GEMINI_MODEL,
    },
}


async def stream_chat(user_id: str, request: AiChatRequest) -> AsyncGenerator[str, None]:
    provider_name = (request.provider or settings.AI_DEFAULT_PROVIDER).lower()
    provider = PROVIDERS.get(provider_name)
    if provider is None:
        raise BusinessException(f"지원하지 않는 AI 프로바이더: {provider_name}")

    config = PROVIDER_CONFIGS.get(provider_name)
    api_key = config["api_key"]()
    model = config["model"]()

    if not api_key:
        raise BusinessException(f"{provider_name} API 키가 설정되지 않았습니다.", 503)

    conversation_id = request.conversation_id or str(uuid.uuid4())

    # start event
    start_event = AiChatEvent(
        type="start", conversationId=conversation_id, provider=provider_name
    )
    yield f"data: {start_event.model_dump_json(exclude_none=True, by_alias=True)}\n\n"

    url = provider.build_url(model, api_key)
    headers = provider.build_headers(api_key)
    body = provider.build_body(request.messages, model, 1024, 0.7)

    prompt_tokens = 0
    completion_tokens = 0

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, headers=headers, json=body) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    logger.error("%s API 오류: %s - %s", provider_name, response.status_code, error_body.decode())
                    error_event = AiChatEvent(type="error", message="AI 서비스 연결에 실패했습니다.")
                    yield f"data: {error_event.model_dump_json(exclude_none=True, by_alias=True)}\n\n"
                    return

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:].strip()
                    if not data:
                        continue

                    result = provider.parse_line(data)

                    if result.text:
                        delta_event = AiChatEvent(type="delta", content=result.text)
                        yield f"data: {delta_event.model_dump_json(exclude_none=True, by_alias=True)}\n\n"
                    if result.prompt_tokens > 0:
                        prompt_tokens = result.prompt_tokens
                    if result.completion_tokens > 0:
                        completion_tokens = result.completion_tokens
                    if result.is_done:
                        break

        done_event = AiChatEvent(
            type="done",
            usage=AiChatUsage(promptTokens=prompt_tokens, completionTokens=completion_tokens),
        )
        yield f"data: {done_event.model_dump_json(exclude_none=True, by_alias=True)}\n\n"

    except Exception as e:
        logger.error("%s 채팅 스트리밍 오류", provider_name, exc_info=e)
        error_event = AiChatEvent(type="error", message="AI 서비스 오류가 발생했습니다.")
        yield f"data: {error_event.model_dump_json(exclude_none=True, by_alias=True)}\n\n"
