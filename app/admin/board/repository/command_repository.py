from app.database import get_pool


class AdminBoardCommandRepository:
    async def insert_board(self, board_id: str, board_name: str, description: str | None, created_by: str):
        pool = get_pool()
        await pool.execute(
            "INSERT INTO tb_board (board_id, board_name, description, created_by, modified_by) VALUES ($1,$2,$3,$4,$4)",
            board_id, board_name, description, created_by,
        )

    async def update_board(self, board_id: str, board_name: str, description: str | None, modified_by: str):
        pool = get_pool()
        await pool.execute(
            """UPDATE tb_board SET board_name=$1, description=$2, modified_by=$3,
               modified_date=CURRENT_TIMESTAMP WHERE board_id=$4""",
            board_name, description, modified_by, board_id,
        )

    async def toggle_active(self, board_id: str):
        pool = get_pool()
        await pool.execute(
            "UPDATE tb_board SET use_yn = NOT use_yn, modified_date = CURRENT_TIMESTAMP WHERE board_id = $1",
            board_id,
        )
