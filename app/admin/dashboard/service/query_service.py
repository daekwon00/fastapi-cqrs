from app.admin.dashboard.repository.query_repository import AdminDashboardQueryRepository
from app.admin.dashboard.schemas import AdminDashboardStatsResponse, RecentUserResponse


class AdminDashboardQueryService:
    def __init__(self):
        self.repo = AdminDashboardQueryRepository()

    async def get_stats(self) -> AdminDashboardStatsResponse:
        return AdminDashboardStatsResponse(
            totalUsers=await self.repo.select_total_users(),
            todayRegistered=await self.repo.select_today_registered(),
            activeBoards=await self.repo.select_active_boards(),
            todayPosts=await self.repo.select_today_posts(),
        )

    async def get_recent_users(self) -> list[RecentUserResponse]:
        rows = await self.repo.select_recent_users()
        return [
            RecentUserResponse(
                id=r["user_id"], username=r["user_id"], name=r["user_name"],
                email=r["email"],
                createdAt=str(r["created_date"]) if r["created_date"] else None,
            )
            for r in rows
        ]
