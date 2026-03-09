from pydantic import BaseModel, Field


class DashboardStatsResponse(BaseModel):
    total_posts: int = Field(alias="totalPosts")
    today_posts: int = Field(alias="todayPosts")
    total_users: int = Field(alias="totalUsers")
    my_posts: int = Field(alias="myPosts")

    model_config = {"populate_by_name": True}


class ChartDataResponse(BaseModel):
    date: str
    count: int
