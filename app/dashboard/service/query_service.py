from app.dashboard.repository.query_repository import DashboardQueryRepository
from app.dashboard.schemas import ChartDataResponse, DashboardStatsResponse


class DashboardQueryService:
    def __init__(self):
        self.repo = DashboardQueryRepository()

    async def get_stats(self, user_id: str) -> DashboardStatsResponse:
        total_posts = await self.repo.select_total_posts()
        today_posts = await self.repo.select_today_posts()
        total_users = await self.repo.select_total_users()
        my_posts = await self.repo.select_my_posts(user_id)

        return DashboardStatsResponse(
            totalPosts=total_posts,
            todayPosts=today_posts,
            totalUsers=total_users,
            myPosts=my_posts,
        )

    async def get_chart_data(self, period: str) -> list[ChartDataResponse]:
        days = 30 if period == "30d" else 7
        rows = await self.repo.select_chart_data(days)
        return [ChartDataResponse(date=row["date"], count=row["count"]) for row in rows]
