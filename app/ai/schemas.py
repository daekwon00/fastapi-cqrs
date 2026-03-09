from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class AiChatRequest(BaseModel):
    provider: str | None = None
    messages: list[ChatMessage] = Field(..., min_length=1)
    conversation_id: str | None = Field(None, alias="conversationId")


class AiChatEvent(BaseModel):
    type: str
    content: str | None = None
    conversation_id: str | None = Field(None, alias="conversationId")
    provider: str | None = None
    message: str | None = None
    usage: "AiChatUsage | None" = None

    model_config = {"populate_by_name": True}


class AiChatUsage(BaseModel):
    prompt_tokens: int = Field(alias="promptTokens")
    completion_tokens: int = Field(alias="completionTokens")

    model_config = {"populate_by_name": True}
