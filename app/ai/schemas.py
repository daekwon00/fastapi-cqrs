from pydantic import BaseModel, Field

from app.common.schemas import CamelModel


class ChatMessage(BaseModel):
    role: str
    content: str


class AiChatRequest(CamelModel):
    provider: str | None = None
    messages: list[ChatMessage] = Field(..., min_length=1)
    conversation_id: str | None = Field(None, alias="conversationId")


class AiChatEvent(CamelModel):
    type: str
    content: str | None = None
    conversation_id: str | None = Field(None, alias="conversationId")
    provider: str | None = None
    message: str | None = None
    usage: "AiChatUsage | None" = None


class AiChatUsage(CamelModel):
    prompt_tokens: int = Field(alias="promptTokens")
    completion_tokens: int = Field(alias="completionTokens")
