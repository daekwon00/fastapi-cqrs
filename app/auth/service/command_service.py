from starlette import status

from app.auth.repository.command_repository import AuthCommandRepository
from app.auth.schemas import LoginResponse, UserInfoResponse
from app.auth.service.query_service import AuthQueryService
from app.common.exceptions import BusinessException
from app.security import jwt as jwt_utils
from app.security.password import hash_password, matches_password


class AuthCommandService:
    def __init__(self):
        self.command_repo = AuthCommandRepository()
        self.query_service = AuthQueryService()

    async def login(self, username: str, password: str, login_ip: str) -> LoginResponse:
        user = await self.query_service.get_user_by_id(username)

        if user is None:
            await self._record_login_history(username, login_ip, False, "사용자를 찾을 수 없습니다.")
            raise BusinessException("아이디 또는 비밀번호가 올바르지 않습니다.", status.HTTP_401_UNAUTHORIZED)

        if user["is_active"] is not None and not user["is_active"]:
            await self._record_login_history(username, login_ip, False, "비활성 계정")
            raise BusinessException("비활성화된 계정입니다.", status.HTTP_401_UNAUTHORIZED)

        if not matches_password(password, user["password"]):
            await self._record_login_history(username, login_ip, False, "비밀번호 불일치")
            raise BusinessException("아이디 또는 비밀번호가 올바르지 않습니다.", status.HTTP_401_UNAUTHORIZED)

        roles = await self.query_service.get_roles_by_user_id(username)
        access_token = jwt_utils.create_access_token(username, roles)
        refresh_token = jwt_utils.create_refresh_token(username)

        await self.command_repo.update_last_login_date(username)
        await self._record_login_history(username, login_ip, True, None)

        display_role = "ADMIN" if any("ADMIN" in r for r in roles) else "USER"
        user_info = UserInfoResponse(
            id=user["user_id"],
            username=user["user_id"],
            name=user["user_name"],
            email=user["email"] or "",
            role=display_role,
        )

        return LoginResponse(accessToken=access_token, refreshToken=refresh_token, user=user_info)

    async def register(self, username: str, password: str, name: str, email: str) -> UserInfoResponse:
        if await self.query_service.exists_by_user_id(username):
            raise BusinessException("이미 존재하는 아이디입니다.", status.HTTP_409_CONFLICT)

        encoded_password = hash_password(password)
        await self.command_repo.insert_user(username, name, encoded_password, email)
        await self.command_repo.insert_user_role(username, "ROLE_MEMBER")

        return UserInfoResponse(id=username, username=username, name=name, email=email, role="USER")

    async def _record_login_history(
        self, user_id: str, login_ip: str, success: bool, fail_reason: str | None
    ):
        try:
            await self.command_repo.insert_login_history(user_id, login_ip, success, fail_reason)
        except Exception:
            pass  # FK 제약 등으로 이력 기록 실패 시 무시 (로그인 처리에 영향 없음)
