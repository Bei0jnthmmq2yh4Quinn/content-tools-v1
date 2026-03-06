"""媒体处理相关接口。"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/download")
async def download_media(url: str):
    """返回视频下载提示，后续可接入真实下载逻辑。"""
    return {
        "success": True,
        "message": "请使用 yt-dlp 命令行工具下载",
        "example": f"yt-dlp '{url}'",
    }
