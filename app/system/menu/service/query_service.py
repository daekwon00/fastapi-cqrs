from app.system.menu.repository.query_repository import MenuQueryRepository
from app.system.menu.schemas import MenuResponse


class MenuQueryService:
    def __init__(self):
        self.repo = MenuQueryRepository()

    async def get_all_menus(self) -> list[MenuResponse]:
        rows = await self.repo.select_all_menus()
        return self._build_tree(rows)

    async def get_menus_by_role_ids(self, role_ids: list[str]) -> list[MenuResponse]:
        rows = await self.repo.select_menus_by_role_ids(role_ids)
        return self._build_tree(rows)

    async def get_admin_menus(self) -> list[MenuResponse]:
        rows = await self.repo.select_admin_menus()
        return self._build_tree(rows)

    def _build_tree(self, rows) -> list[MenuResponse]:
        items = {}
        for r in rows:
            items[r["menu_id"]] = MenuResponse(
                id=r["menu_id"], name=r["menu_name"], path=r["menu_url"],
                icon=r["menu_icon"], parentId=r["parent_menu_id"],
                sortOrder=r["sort_order"], isActive=bool(r["use_yn"]), children=[],
            )
        roots: list[MenuResponse] = []
        for item in items.values():
            parent_id = item.parent_id
            if parent_id and parent_id in items:
                items[parent_id].children.append(item)
            else:
                roots.append(item)
        return roots
