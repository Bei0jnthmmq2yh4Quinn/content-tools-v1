from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AnalyzeRequest(BaseModel):
    platform: str
    username: str

@router.post("/benchmark")
async def analyze_benchmark(req: AnalyzeRequest):
    """对标分析"""
    return {
        "success": True,
        "data": {
            "username": req.username,
            "platform": req.platform,
            "followers": 12500,
            "avg_likes": 3200,
            "content_style": "生活分享/干货教程",
            "topics": ["职场", "成长", "好物推荐"]
        }
    }
