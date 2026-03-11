from pydantic import BaseModel, Field

from app.common.schemas import CamelModel


class DashboardStatsResponse(CamelModel):
    total_posts: int = Field(alias="totalPosts")
    today_posts: int = Field(alias="todayPosts")
    total_users: int = Field(alias="totalUsers")
    my_posts: int = Field(alias="myPosts")


class ChartDataResponse(BaseModel):
    date: str
    count: int
