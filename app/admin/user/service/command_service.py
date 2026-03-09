from app.admin.user.repository.command_repository import AdminUserCommandRepository
from app.security.password import hash_password


class AdminUserCommandService:
    def __init__(self):
        self.repo = AdminUserCommandRepository()

    async def create_user(
        self, user_id: str, password: str, name: str, email: str, role: str, department: str | None
    ):
        encoded = hash_password(password)
        await self.repo.insert_user(user_id, name, encoded, email, department)
        role_id = "ROLE_ADMIN" if role == "ADMIN" else "ROLE_MEMBER"
        await self.repo.insert_user_role(user_id, role_id)

    async def update_user(self, user_id: str, name: str, email: str, role: str, department: str | None):
        await self.repo.update_user(user_id, name, email, department)
        await self.repo.delete_user_roles(user_id)
        role_id = "ROLE_ADMIN" if role == "ADMIN" else "ROLE_MEMBER"
        await self.repo.insert_user_role(user_id, role_id)

    async def toggle_active(self, user_id: str):
        await self.repo.toggle_active(user_id)
