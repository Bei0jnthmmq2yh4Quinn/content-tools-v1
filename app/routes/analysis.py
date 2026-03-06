"""对标分析相关接口。"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """对标分析请求体。"""

    platform: str
    username: str


@router.post("/benchmark")
async def analyze_benchmark(req: AnalyzeRequest):
    """根据平台和账号名返回示例分析结果。"""
    return {
        "success": True,
        "data": {
            "username": req.username,
            "platform": req.platform,
            "followers": 12500,
            "avg_likes": 3200,
            "content_style": "生活分享/干货教程",
            "topics": ["职场", "成长", "好物推荐"],
        },
    }
