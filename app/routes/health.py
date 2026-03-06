"""健康检查接口。"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """返回服务运行状态，便于探活和监控。"""
    return {"status": "ok", "service": "content-tools"}
