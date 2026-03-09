from fastapi import APIRouter, Depends, status

from app.admin.board.schemas import AdminBoardResponse, CreateBoardRequest, UpdateBoardRequest
from app.admin.board.service.command_service import AdminBoardCommandService
from app.admin.board.service.query_service import AdminBoardQueryService
from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin

router = APIRouter(prefix="/api/v1/admin/boards", tags=["Admin Board"], dependencies=[Depends(require_admin)])
query_service = AdminBoardQueryService()
command_service = AdminBoardCommandService()


@router.get("", response_model=ApiResponse[list[AdminBoardResponse]])
async def get_board_list():
    return ApiResponse.ok(await query_service.get_board_list())


@router.post("", response_model=ApiResponse[AdminBoardResponse], status_code=status.HTTP_201_CREATED)
async def create_board(request: CreateBoardRequest, current_user: CurrentUser = Depends(get_current_user)):
    await command_service.create_board(request.id, request.name, request.description, current_user.user_id)
    return ApiResponse.ok(await query_service.get_board_by_id(request.id))


@router.put("/{board_id}", response_model=ApiResponse[AdminBoardResponse])
async def update_board(board_id: str, request: UpdateBoardRequest, current_user: CurrentUser = Depends(get_current_user)):
    await command_service.update_board(board_id, request.name, request.description, current_user.user_id)
    return ApiResponse.ok(await query_service.get_board_by_id(board_id))


@router.patch("/{board_id}/toggle-active", response_model=ApiResponse[AdminBoardResponse])
async def toggle_active(board_id: str):
    await command_service.toggle_active(board_id)
    return ApiResponse.ok(await query_service.get_board_by_id(board_id))
