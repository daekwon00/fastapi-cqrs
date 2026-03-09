from app.database import get_pool


class MenuCommandRepository:
    async def insert_menu(self, menu_id: str, menu_name: str, menu_url: str | None,
                          menu_icon: str | None, parent_menu_id: str | None, sort_order: int, created_by: str):
        await get_pool().execute(
            """INSERT INTO tb_menu (menu_id, menu_name, menu_url, menu_icon, parent_menu_id, sort_order, created_by)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            menu_id, menu_name, menu_url, menu_icon, parent_menu_id, sort_order, created_by,
        )

    async def update_menu(self, menu_id: str, menu_name: str, menu_url: str | None,
                          menu_icon: str | None, parent_menu_id: str | None, sort_order: int, modified_by: str):
        await get_pool().execute(
            """UPDATE tb_menu SET menu_name=$1, menu_url=$2, menu_icon=$3, parent_menu_id=$4,
               sort_order=$5, modified_by=$6, modified_date=CURRENT_TIMESTAMP WHERE menu_id=$7""",
            menu_name, menu_url, menu_icon, parent_menu_id, sort_order, modified_by, menu_id,
        )

    async def delete_menu(self, menu_id: str):
        await get_pool().execute("DELETE FROM tb_menu WHERE menu_id = $1", menu_id)
