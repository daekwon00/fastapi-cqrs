from fastapi import APIRouter, Depends

from app.admin.dashboard.schemas import AdminDashboardStatsResponse, RecentUserResponse
from app.admin.dashboard.service.query_service import AdminDashboardQueryService
from app.common.schemas import ApiResponse
from app.security.dependencies import require_admin

router = APIRouter(prefix="/api/v1/admin/dashboard", tags=["Admin Dashboard"], dependencies=[Depends(require_admin)])
query_service = AdminDashboardQueryService()


@router.get("/stats", response_model=ApiResponse[AdminDashboardStatsResponse])
async def get_stats():
    return ApiResponse.ok(await query_service.get_stats())


@router.get("/recent-users", response_model=ApiResponse[list[RecentUserResponse]])
async def get_recent_users():
    return ApiResponse.ok(await query_service.get_recent_users())
