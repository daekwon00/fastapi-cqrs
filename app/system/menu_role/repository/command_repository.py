from app.database import get_pool


class MenuRoleCommandRepository:
    async def delete_by_role_id(self, role_id: str):
        await get_pool().execute("DELETE FROM tb_role_menu WHERE role_id = $1", role_id)

    async def insert_menu_role(self, role_id: str, menu_id: str, created_by: str):
        await get_pool().execute(
            """INSERT INTO tb_role_menu (role_id, menu_id, can_read, can_create, can_update, can_delete, created_by)
               VALUES ($1, $2, true, true, true, true, $3)""",
            role_id, menu_id, created_by,
        )
