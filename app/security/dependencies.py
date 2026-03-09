from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.exceptions import ForbiddenException, UnauthorizedException
from app.security import jwt as jwt_utils

bearer_scheme = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, user_id: str, roles: list[str]):
        self.user_id = user_id
        self.roles = roles

    @property
    def is_admin(self) -> bool:
        return any("ADMIN" in r for r in self.roles)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    if credentials is None:
        raise UnauthorizedException("인증 토큰이 필요합니다.")
    token = credentials.credentials
    if not jwt_utils.validate_token(token):
        raise UnauthorizedException("유효하지 않은 토큰입니다.")
    user_id = jwt_utils.get_user_id(token)
    roles = jwt_utils.get_roles(token)
    return CurrentUser(user_id=user_id, roles=roles)


async def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not current_user.is_admin:
        raise ForbiddenException("관리자 권한이 필요합니다.")
    return current_user
