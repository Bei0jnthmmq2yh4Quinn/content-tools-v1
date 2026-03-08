from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.douyin_parse_service import DouyinParseService
from app.services.mobang_service import MobangService

router = APIRouter()


class ProviderBody(BaseModel):
    api_key: str = ''
    base_url: str = ''
    model: str = ''


class AnalyzeBody(BaseModel):
    text: str = ''
    url: str = ''
    industry: str = ''
    platform: str = 'xiaohongshu'
    goal: str = '涨粉'
    provider: Optional[Dict[str, Any]] = None


class RewriteBody(BaseModel):
    text: str = ''
    url: str = ''
    mode: str = 'douyin'
    industry: str = ''
    platform: str = 'xiaohongshu'
    goal: str = '涨粉'
    provider: Optional[Dict[str, Any]] = None


def normalize_text(text: str, url: str) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    text = (text or '').strip()
    url = (url or '').strip()
    if text:
        return text, None, None
    if url:
        if 'douyin.com' in url or 'iesdouyin.com' in url:
            parsed = DouyinParseService.parse(url)
            if parsed.get('success') and parsed.get('text'):
                return parsed['text'], None, parsed.get('meta', {})
            return None, parsed.get('message') or '当前抖音链接解析失败，请先把字幕/文案贴进来。', parsed.get('meta', {})
        return None, '暂不支持该链接类型，请先粘贴文本内容。', None
    return None, '请先输入爆款文案、字幕或链接。', None


@router.post('/config')
async def config(provider: ProviderBody):
    ok = bool(provider.api_key and provider.base_url and provider.model)
    return {'success': True, 'configured': ok, 'message': '已读取当前用户渠道配置' if ok else '未配置 AI 渠道，将使用规则兜底'}


@router.post('/analyze')
async def analyze(body: AnalyzeBody):
    text, err, meta = normalize_text(body.text, body.url)
    if err:
        return {'success': False, 'message': err, 'data': None, 'meta': meta or {}}
    api_key, base_url, model = MobangService.resolve_provider(body.provider)
    try:
        data = await MobangService.llm_analyze(text, api_key=api_key, base_url=base_url, model=model, industry=body.industry, platform=body.platform, goal=body.goal)
        if data:
            return {'success': True, 'message': '拆解完成（LLM）', 'data': data, 'meta': meta or {}}
    except Exception:
        pass
    return {'success': True, 'message': '拆解完成（规则兜底）', 'data': MobangService.rule_analyze(text, industry=body.industry, platform=body.platform, goal=body.goal), 'meta': meta or {}}


@router.post('/rewrite')
async def rewrite(body: RewriteBody):
    text, err, meta = normalize_text(body.text, body.url)
    if err:
        return {'success': False, 'message': err, 'data': None, 'meta': meta or {}}
    api_key, base_url, model = MobangService.resolve_provider(body.provider)
    try:
        data = await MobangService.llm_rewrite(text, body.mode, api_key=api_key, base_url=base_url, model=model, industry=body.industry, platform=body.platform, goal=body.goal)
        if data:
            return {'success': True, 'message': '改写完成（LLM）', 'data': data, 'meta': meta or {}}
    except Exception:
        pass
    return {'success': True, 'message': '改写完成（规则兜底）', 'data': MobangService.rule_rewrite(text, body.mode, industry=body.industry, platform=body.platform, goal=body.goal), 'meta': meta or {}}
