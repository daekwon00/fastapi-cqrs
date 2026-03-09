from app.database import get_pool


class PositionRoleCommandRepository:
    async def delete_by_position_id(self, position_id: str):
        await get_pool().execute("DELETE FROM tb_position_role WHERE position_id = $1", position_id)

    async def insert_position_role(self, position_id: str, role_id: str, created_by: str):
        await get_pool().execute(
            """INSERT INTO tb_position_role (position_id, role_id, created_by)
               VALUES ($1, $2, $3)""",
            position_id, role_id, created_by,
        )
