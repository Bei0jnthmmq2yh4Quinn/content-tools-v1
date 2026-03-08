from __future__ import annotations

import json
import re
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter

router = APIRouter()

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)
DOUYIN_URL = 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/'
XHS_EXPLORE_URL = 'https://www.xiaohongshu.com/explore'


def build_industry_suggestions(industry: str, platform: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    industry = (industry or '通用').strip()
    platform = platform or 'xiaohongshu'
    card_types = [
        ('热点借势', '结合热点借势表达', '适合追热度和拉停留'),
        ('行业观点', '输出判断和立场', '适合建立专业感和差异化'),
        ('接单案例', '把结果和案例讲清楚', '适合服务型账号接咨询'),
        ('避坑反常识', '从错误做法切入', '适合做收藏和转发'),
    ]
    suggestions = []
    for idx, item in enumerate(items[:4]):
        title = item.get('title') or '未命名热点'
        type_name, angle_desc, fit_desc = card_types[idx % len(card_types)]
        suggestions.append(
            {
                'type': type_name,
                'hotspot': title,
                'title': f'{industry}：{title}',
                'reason': f'这条内容和“{title}”有关，但要改成 {industry} 用户真的关心的问题，才有用。',
                'topic': f'{industry}怎么结合「{title}」做一条更容易出反馈的内容',
                'angle': angle_desc if platform == 'xiaohongshu' else f'{angle_desc}（口播版）',
                'fit': fit_desc,
                'action': '先贴行业痛点，再补一个真实场景，最后给具体动作。',
                'draft': f'{industry}行业里，最近很多人都在关注「{title}」。\n\n但真正值得做的，不是复述热点，而是把它改成和客户决策有关的内容。\n\n你可以先讲这个热点背后反映出的用户情绪，再落到你的行业场景里。',
            }
        )
    return suggestions


def build_today_brief(industry: str, platform: str, goal: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    suggestions = build_industry_suggestions(industry, platform, items)
    first = suggestions[0] if suggestions else {
        'topic': f'{industry}今天适合做一条{goal}向内容',
        'reason': '当前没有抓到合适热点，建议先用行业痛点切入。',
        'action': '先讲痛点，再讲方法，最后加行动引导。',
        'hotspot': '通用话题',
        'angle': '通用切入',
        'type': '行业观点',
        'fit': '适合先做一条行业基础表达',
    }
    return {
        'industry': industry,
        'platform': platform,
        'goal': goal,
        'headline': first.get('title') or first['topic'],
        'reason': first['reason'],
        'action': first['action'],
        'hotspot': first['hotspot'],
        'angle': first['angle'],
        'type': first.get('type', '行业观点'),
        'fit': first.get('fit', ''),
        'title_hint': f'{industry}{goal}内容，可以先从「{first["hotspot"]}」切入',
    }


async def _fetch_douyin_trends() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(DOUYIN_URL, headers={'User-Agent': USER_AGENT})
        resp.raise_for_status()
        payload = resp.json()
    results = []
    for item in payload.get('word_list', [])[:10]:
        title = item.get('word')
        if not title:
            continue
        results.append({'rank': len(results) + 1, 'title': title, 'hot': item.get('hot_value') or 0})
    return results


def _clean_xhs_state(raw_state: str) -> str:
    return raw_state.replace(':undefined', ':null').replace('undefined', 'null')


async def _fetch_xiaohongshu_trends() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(XHS_EXPLORE_URL, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html'})
        resp.raise_for_status()
        html = resp.text
    match = re.search(r'__INITIAL_STATE__=(\{.*?\})\s*</script>', html, re.S)
    if not match:
        raise ValueError('未能解析小红书页面数据')
    state = json.loads(_clean_xhs_state(match.group(1)))
    feeds = state.get('feed', {}).get('feeds', [])
    results = []
    for item in feeds:
        note = item.get('noteCard', {})
        title = note.get('displayTitle') or note.get('title')
        if not title:
            continue
        liked = note.get('interactInfo', {}).get('likedCount')
        try:
            liked_value = int(liked) if liked is not None else None
        except (TypeError, ValueError):
            liked_value = None
        results.append({'rank': len(results) + 1, 'title': title, 'likes': liked_value})
        if len(results) >= 10:
            break
    return results


@router.get('/douyin')
async def get_douyin_trends():
    try:
        data = await _fetch_douyin_trends()
        return {'success': True, 'source': 'douyin-web', 'data': data}
    except Exception:
        return {'success': False, 'source': 'douyin-web', 'data': [], 'message': '抖音热搜获取失败。建议先切到“小红书列表”或直接输入你手上的爆款文案继续使用。'}


@router.get('/xiaohongshu')
async def get_xiaohongshu_trends():
    try:
        data = await _fetch_xiaohongshu_trends()
        return {'success': True, 'source': 'xiaohongshu-explore', 'data': data}
    except Exception:
        return {'success': False, 'source': 'xiaohongshu-explore', 'data': [], 'message': '小红书热门获取失败。建议先用“行业 + 痛点”手动生成选题，或稍后重试。'}


@router.get('/suggestions')
async def get_trend_suggestions(industry: str = '通用', platform: str = 'xiaohongshu'):
    try:
        data = await (_fetch_xiaohongshu_trends() if platform == 'xiaohongshu' else _fetch_douyin_trends())
        suggestions = build_industry_suggestions(industry, platform, data)
        return {'success': True, 'industry': industry, 'platform': platform, 'data': suggestions}
    except Exception:
        return {'success': False, 'industry': industry, 'platform': platform, 'data': [], 'message': '热点建议生成失败。你可以先切到“AI 选题”，手动输入行业和热点词继续生成。'}


@router.get('/brief')
async def get_today_brief(industry: str = '通用', platform: str = 'xiaohongshu', goal: str = '涨粉'):
    try:
        data = await (_fetch_xiaohongshu_trends() if platform == 'xiaohongshu' else _fetch_douyin_trends())
        brief = build_today_brief(industry, platform, goal, data)
        return {'success': True, 'data': brief}
    except Exception:
        return {'success': False, 'data': {'industry': industry, 'platform': platform, 'goal': goal, 'headline': f'{industry}今天适合做一条{goal}向内容', 'reason': '热点拉取失败，先用通用痛点切入。', 'action': '先讲用户情绪，再讲方法，最后加行动引导。', 'hotspot': '通用话题', 'angle': '通用切入', 'title_hint': f'{industry}{goal}内容，先从通用痛点切入'}}
