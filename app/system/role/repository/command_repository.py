from app.database import get_pool


class RoleCommandRepository:
    async def insert_role(self, role_id: str, role_name: str, description: str | None, created_by: str):
        await get_pool().execute(
            """INSERT INTO tb_role (role_id, role_name, role_level, description, created_by)
               VALUES ($1, $2, COALESCE((SELECT MAX(role_level) + 1 FROM tb_role), 1), $3, $4)""",
            role_id, role_name, description, created_by,
        )

    async def update_role(self, role_id: str, role_name: str, description: str | None, modified_by: str):
        await get_pool().execute(
            """UPDATE tb_role SET role_name=$1, description=$2, modified_by=$3,
               modified_date=CURRENT_TIMESTAMP WHERE role_id=$4""",
            role_name, description, modified_by, role_id,
        )

    async def delete_role(self, role_id: str):
        await get_pool().execute("DELETE FROM tb_role WHERE role_id = $1", role_id)
