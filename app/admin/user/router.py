from fastapi import APIRouter, Depends, Query, status

from app.admin.user.schemas import AdminUserResponse, CreateUserRequest, UpdateUserRequest
from app.admin.user.service.command_service import AdminUserCommandService
from app.admin.user.service.query_service import AdminUserQueryService
from app.common.schemas import ApiResponse, PageResponse
from app.security.dependencies import require_admin

router = APIRouter(prefix="/api/v1/admin/users", tags=["Admin User"], dependencies=[Depends(require_admin)])
query_service = AdminUserQueryService()
command_service = AdminUserCommandService()


@router.get("", response_model=ApiResponse[PageResponse[AdminUserResponse]])
async def get_user_list(
    page: int = Query(0, ge=0), size: int = Query(10, ge=1), search: str | None = Query(None),
):
    offset = page * size
    content = await query_service.get_user_list(search, size, offset)
    total = await query_service.get_user_count(search)
    return ApiResponse.ok(PageResponse.of(content, total, page, size))


@router.get("/{user_id}", response_model=ApiResponse[AdminUserResponse])
async def get_user_by_id(user_id: str):
    return ApiResponse.ok(await query_service.get_user_by_id(user_id))


@router.post("", response_model=ApiResponse[AdminUserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest):
    await command_service.create_user(
        request.username, request.password, request.name, request.email, request.role, request.department
    )
    return ApiResponse.ok(await query_service.get_user_by_id(request.username))


@router.put("/{user_id}", response_model=ApiResponse[AdminUserResponse])
async def update_user(user_id: str, request: UpdateUserRequest):
    await command_service.update_user(user_id, request.name, request.email, request.role, request.department)
    return ApiResponse.ok(await query_service.get_user_by_id(user_id))


@router.patch("/{user_id}/toggle-active", response_model=ApiResponse[AdminUserResponse])
async def toggle_active(user_id: str):
    await command_service.toggle_active(user_id)
    return ApiResponse.ok(await query_service.get_user_by_id(user_id))
