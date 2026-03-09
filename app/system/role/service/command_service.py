from app.system.role.repository.command_repository import RoleCommandRepository


class RoleCommandService:
    def __init__(self):
        self.repo = RoleCommandRepository()

    async def create_role(self, role_id: str, name: str, description: str | None, created_by: str):
        await self.repo.insert_role(role_id, name, description, created_by)

    async def update_role(self, role_id: str, name: str, description: str | None, modified_by: str):
        await self.repo.update_role(role_id, name, description, modified_by)

    async def delete_role(self, role_id: str):
        await self.repo.delete_role(role_id)
