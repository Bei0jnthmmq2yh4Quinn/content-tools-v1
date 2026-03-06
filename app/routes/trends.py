from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/douyin")
async def get_douyin_trends():
    """获取抖音热搜"""
    # 简化版本：返回示例数据
    return {
        "success": True,
        "data": [
            {"rank": 1, "title": "春节档电影", "hot": 1250000},
            {"rank": 2, "title": "AI新工具", "hot": 980000},
            {"rank": 3, "title": "打工人的一天", "hot": 850000},
        ]
    }

@router.get("/xiaohongshu")
async def get_xiaohongshu_trends():
    """获取小红书热门"""
    return {
        "success": True,
        "data": [
            {"rank": 1, "title": "年后减脂计划", "likes": 52000},
            {"rank": 2, "title": "ChatGPT使用技巧", "likes": 48000},
            {"rank": 3, "title": "租房改造", "likes": 35000},
        ]
    }
