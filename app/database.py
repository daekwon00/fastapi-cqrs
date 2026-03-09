import asyncpg

from app.config import settings

pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    global pool
    pool = await asyncpg.create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        server_settings={"search_path": settings.DB_SCHEMA},
        min_size=2,
        max_size=10,
    )
    return pool


async def close_pool():
    global pool
    if pool:
        await pool.close()
        pool = None


def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError("DB pool이 초기화되지 않았습니다.")
    return pool
