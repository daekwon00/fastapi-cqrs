from app.system.menu.repository.command_repository import MenuCommandRepository


class MenuCommandService:
    def __init__(self):
        self.repo = MenuCommandRepository()

    async def create_menu(self, menu_id: str, name: str, path: str | None,
                          icon: str | None, parent_id: str | None, sort_order: int, created_by: str):
        await self.repo.insert_menu(menu_id, name, path, icon, parent_id, sort_order, created_by)

    async def update_menu(self, menu_id: str, name: str, path: str | None,
                          icon: str | None, parent_id: str | None, sort_order: int, modified_by: str):
        await self.repo.update_menu(menu_id, name, path, icon, parent_id, sort_order, modified_by)

    async def delete_menu(self, menu_id: str):
        await self.repo.delete_menu(menu_id)
