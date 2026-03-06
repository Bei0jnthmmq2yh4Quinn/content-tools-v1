from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/download")
async def download_media(url: str):
    """下载视频"""
    return {
        "success": True,
        "message": "请使用 yt-dlp 命令行工具下载",
        "example": f"yt-dlp '{url}'"
    }
