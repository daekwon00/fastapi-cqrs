from fastapi import APIRouter, Request, status

from app.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserInfoResponse,
)
from app.auth.service.command_service import AuthCommandService
from app.common.exceptions import BusinessException
from app.common.schemas import ApiResponse
from app.security import jwt as jwt_utils

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
command_service = AuthCommandService()


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(request: LoginRequest, http_request: Request):
    login_ip = http_request.client.host if http_request.client else "unknown"
    result = await command_service.login(request.username, request.password, login_ip)
    return ApiResponse.ok(result)


@router.post("/register", response_model=ApiResponse[UserInfoResponse], status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    result = await command_service.register(request.username, request.password, request.name, request.email)
    return ApiResponse.ok(result)


@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh(request: RefreshRequest):
    if not jwt_utils.validate_token(request.refresh_token):
        raise BusinessException("유효하지 않은 리프레시 토큰입니다.", status.HTTP_401_UNAUTHORIZED)

    user_id = jwt_utils.get_user_id(request.refresh_token)
    roles = jwt_utils.get_roles(request.refresh_token)
    new_access_token = jwt_utils.create_access_token(user_id, roles)

    return ApiResponse.ok(TokenResponse(accessToken=new_access_token))
