from app.system.position_role.repository.command_repository import PositionRoleCommandRepository


class PositionRoleCommandService:
    def __init__(self):
        self.repo = PositionRoleCommandRepository()

    async def update_position_roles(self, position_id: str, role_ids: list[str], user_id: str):
        await self.repo.delete_by_position_id(position_id)
        for role_id in role_ids:
            await self.repo.insert_position_role(position_id, role_id, user_id)
