from app.system.menu_role.repository.query_repository import MenuRoleQueryRepository
from app.system.menu_role.schemas import MenuRoleResponse


class MenuRoleQueryService:
    def __init__(self):
        self.repo = MenuRoleQueryRepository()

    async def get_all_menu_roles(self) -> list[MenuRoleResponse]:
        rows = await self.repo.select_all_menu_roles()
        return [MenuRoleResponse(menuId=r["menu_id"], roleId=r["role_id"]) for r in rows]
