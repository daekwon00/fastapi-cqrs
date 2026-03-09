from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.exception_handlers import register_exception_handlers
from app.database import close_pool, create_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_pool()
    yield
    await close_pool()


app = FastAPI(
    title="FastAPI CQRS",
    description="Spring Boot CQRS 프로젝트의 FastAPI 재구현",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 예외 핸들러
register_exception_handlers(app)


# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}


# 라우터 등록
from app.auth.router import router as auth_router  # noqa: E402
from app.board.router import router as board_router  # noqa: E402
from app.user.router import router as user_router  # noqa: E402

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(board_router)
