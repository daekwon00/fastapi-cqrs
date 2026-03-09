from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from app.ai.schemas import AiChatRequest
from app.ai.service import stream_chat
from app.security.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/api/v1/ai", tags=["AI Chat"])


@router.post("/chat")
async def chat(
    request: AiChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    return EventSourceResponse(stream_chat(current_user.user_id, request))
