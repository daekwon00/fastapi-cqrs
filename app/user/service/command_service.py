from app.auth.service.query_service import AuthQueryService
from app.common.exceptions import BusinessException
from app.security.password import hash_password, matches_password
from app.user.repository.command_repository import UserCommandRepository
from app.user.schemas import UserProfileResponse
from app.user.service.query_service import UserQueryService


class UserCommandService:
    def __init__(self):
        self.command_repo = UserCommandRepository()
        self.query_service = UserQueryService()
        self.auth_query_service = AuthQueryService()

    async def update_profile(self, user_id: str, name: str, email: str, phone: str | None) -> UserProfileResponse:
        await self.command_repo.update_profile(user_id, name, email, phone)
        return await self.query_service.get_user_profile(user_id)

    async def change_password(self, user_id: str, current_password: str, new_password: str):
        user = await self.auth_query_service.get_user_by_id(user_id)
        if user is None:
            raise BusinessException("사용자를 찾을 수 없습니다.")

        if not matches_password(current_password, user["password"]):
            raise BusinessException("현재 비밀번호가 올바르지 않습니다.")

        encoded = hash_password(new_password)
        await self.command_repo.update_password(user_id, encoded)
