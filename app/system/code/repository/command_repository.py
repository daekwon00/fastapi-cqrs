from app.database import get_pool


class CodeCommandRepository:
    async def insert_code(self, code_id: str, code_group_id: str, code_name: str,
                          code_value: str | None, sort_order: int, description: str | None, created_by: str):
        await get_pool().execute(
            """INSERT INTO tb_common_code (code_id, code_group_id, code_name, code_value, sort_order, description, created_by)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            code_id, code_group_id, code_name, code_value, sort_order, description, created_by,
        )

    async def update_code(self, code_id: str, code_group_id: str, code_name: str,
                          code_value: str | None, sort_order: int, description: str | None, modified_by: str):
        await get_pool().execute(
            """UPDATE tb_common_code
               SET code_group_id = $1, code_name = $2, code_value = $3, sort_order = $4,
                   description = $5, modified_by = $6, modified_date = CURRENT_TIMESTAMP
             WHERE code_id = $7""",
            code_group_id, code_name, code_value, sort_order, description, modified_by, code_id,
        )

    async def delete_code(self, code_id: str):
        await get_pool().execute("DELETE FROM tb_common_code WHERE code_id = $1", code_id)
