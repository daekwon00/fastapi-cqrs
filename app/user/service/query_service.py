from app.common.exceptions import NotFoundException
from app.user.repository.query_repository import UserQueryRepository
from app.user.schemas import UserProfileResponse


class UserQueryService:
    def __init__(self):
        self.repo = UserQueryRepository()

    async def get_user_profile(self, user_id: str) -> UserProfileResponse:
        row = await self.repo.select_user_profile(user_id)
        if row is None:
            raise NotFoundException("사용자를 찾을 수 없습니다.")
        return UserProfileResponse(**dict(row))
