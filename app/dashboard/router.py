from fastapi import APIRouter, Depends, Query

from app.common.schemas import ApiResponse
from app.dashboard.schemas import ChartDataResponse, DashboardStatsResponse
from app.dashboard.service.query_service import DashboardQueryService
from app.security.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])
query_service = DashboardQueryService()


@router.get("/stats", response_model=ApiResponse[DashboardStatsResponse])
async def get_stats(current_user: CurrentUser = Depends(get_current_user)):
    result = await query_service.get_stats(current_user.user_id)
    return ApiResponse.ok(result)


@router.get("/chart", response_model=ApiResponse[list[ChartDataResponse]])
async def get_chart_data(
    period: str = Query("7d", description="기간 (7d, 30d)"),
):
    result = await query_service.get_chart_data(period)
    return ApiResponse.ok(result)
