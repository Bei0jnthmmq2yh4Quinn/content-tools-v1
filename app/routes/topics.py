from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TopicRequest(BaseModel):
    niche: str
    benchmark_topics: list[str]
    trends: list[str]

@router.post("/generate")
async def generate_topics(req: TopicRequest):
    """AI生成选题"""
    topics = [
        {"title": f"{req.niche} + {req.trends[0] if req.trends else '热点'}", "type": "蹭热点"},
        {"title": f"{req.benchmark_topics[0] if req.benchmark_topics else '干货'} + 实战", "type": "干货教程"},
        {"title": "90%人都不知道的技巧", "type": "悬念引导"},
    ]
    return {"success": True, "data": topics}
