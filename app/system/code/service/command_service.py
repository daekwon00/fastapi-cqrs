from app.system.code.repository.command_repository import CodeCommandRepository


class CodeCommandService:
    def __init__(self):
        self.repo = CodeCommandRepository()

    async def create_code(self, code_id: str, code_group_id: str, code_name: str,
                          code_value: str | None, sort_order: int, description: str | None, created_by: str):
        await self.repo.insert_code(code_id, code_group_id, code_name, code_value, sort_order, description, created_by)

    async def update_code(self, code_id: str, code_group_id: str, code_name: str,
                          code_value: str | None, sort_order: int, description: str | None, modified_by: str):
        await self.repo.update_code(code_id, code_group_id, code_name, code_value, sort_order, description, modified_by)

    async def delete_code(self, code_id: str):
        await self.repo.delete_code(code_id)
