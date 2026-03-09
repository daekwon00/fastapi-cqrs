from app.system.menu_role.repository.command_repository import MenuRoleCommandRepository


class MenuRoleCommandService:
    def __init__(self):
        self.repo = MenuRoleCommandRepository()

    async def update_menu_roles(self, role_id: str, menu_ids: list[str], user_id: str):
        await self.repo.delete_by_role_id(role_id)
        for menu_id in menu_ids:
            await self.repo.insert_menu_role(role_id, menu_id, user_id)
