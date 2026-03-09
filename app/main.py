from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.exception_handlers import register_exception_handlers
from app.common.middleware import RequestLoggingMiddleware
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

# 요청 로깅
app.add_middleware(RequestLoggingMiddleware)

# 예외 핸들러
register_exception_handlers(app)


# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}


# 라우터 등록
from app.admin.board.router import router as admin_board_router  # noqa: E402
from app.admin.dashboard.router import router as admin_dashboard_router  # noqa: E402
from app.admin.user.router import router as admin_user_router  # noqa: E402
from app.ai.router import router as ai_router  # noqa: E402
from app.auth.router import router as auth_router  # noqa: E402
from app.board.router import router as board_router  # noqa: E402
from app.dashboard.router import router as dashboard_router  # noqa: E402
from app.file.router import router as file_router  # noqa: E402
from app.system.code.router import router as code_router  # noqa: E402
from app.system.menu.router import router as menu_router  # noqa: E402
from app.system.menu_role.router import router as menu_role_router  # noqa: E402
from app.system.position_role.router import router as position_role_router  # noqa: E402
from app.system.role.router import router as role_router  # noqa: E402
from app.user.router import router as user_router  # noqa: E402

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(board_router)
app.include_router(file_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(admin_user_router)
app.include_router(admin_board_router)
app.include_router(admin_dashboard_router)
app.include_router(role_router)
app.include_router(menu_router)
app.include_router(menu_role_router)
app.include_router(code_router)
app.include_router(position_role_router)
