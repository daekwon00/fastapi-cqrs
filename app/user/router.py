from fastapi import APIRouter, Depends, Query

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user
from app.user.schemas import ChangePasswordRequest, LoginHistoryResponse, UpdateProfileRequest, UserProfileResponse
from app.user.service.command_service import UserCommandService
from app.user.service.query_service import UserQueryService

router = APIRouter(prefix="/api/v1/users", tags=["User"])
query_service = UserQueryService()
command_service = UserCommandService()


@router.get("/me/login-history", response_model=ApiResponse[list[LoginHistoryResponse]])
async def get_my_login_history(
    current_user: CurrentUser = Depends(get_current_user),
    size: int = Query(10, ge=1, le=100),
):
    result = await query_service.get_login_history(current_user.user_id, size)
    return ApiResponse.ok(result)


@router.get("/me", response_model=ApiResponse[UserProfileResponse])
async def get_my_profile(current_user: CurrentUser = Depends(get_current_user)):
    result = await query_service.get_user_profile(current_user.user_id)
    return ApiResponse.ok(result)


@router.put("/me", response_model=ApiResponse[UserProfileResponse])
async def update_my_profile(
    request: UpdateProfileRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await command_service.update_profile(
        current_user.user_id, request.name, request.email, request.phone
    )
    return ApiResponse.ok(result)


@router.put("/me/password", response_model=ApiResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    await command_service.change_password(
        current_user.user_id, request.current_password, request.new_password
    )
    return ApiResponse.ok(message="비밀번호가 변경되었습니다.")
