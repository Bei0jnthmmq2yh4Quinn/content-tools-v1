from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.mobang_service import MobangService

router = APIRouter()


class ProviderBody(BaseModel):
    api_key: str = ''
    base_url: str = ''
    model: str = ''


class AnalyzeBody(BaseModel):
    text: str = ''
    url: str = ''
    provider: Optional[Dict[str, Any]] = None


class RewriteBody(BaseModel):
    text: str = ''
    url: str = ''
    mode: str = 'douyin'
    provider: Optional[Dict[str, Any]] = None


def normalize_text(text: str, url: str):
    text = (text or '').strip()
    url = (url or '').strip()
    if text:
        return text, None
    if url:
        if 'douyin.com' in url or 'iesdouyin.com' in url:
            return None, '当前抖音链接解析先留占位，建议先把字幕/文案贴进来再拆解。'
        return None, '暂不支持该链接类型，请先粘贴文本内容。'
    return None, '请先输入爆款文案、字幕或链接。'


@router.post('/config')
async def config(provider: ProviderBody):
    ok = bool(provider.api_key and provider.base_url and provider.model)
    return {'success': True, 'configured': ok, 'message': '已读取当前用户渠道配置' if ok else '未配置 AI 渠道，将使用规则兜底'}


@router.post('/analyze')
async def analyze(body: AnalyzeBody):
    text, err = normalize_text(body.text, body.url)
    if err:
        return {'success': False, 'message': err, 'data': None}
    api_key, base_url, model = MobangService.resolve_provider(body.provider)
    try:
        data = await MobangService.llm_analyze(text, api_key=api_key, base_url=base_url, model=model)
        if data:
            return {'success': True, 'message': '拆解完成（LLM）', 'data': data}
    except Exception:
        pass
    return {'success': True, 'message': '拆解完成（规则兜底）', 'data': MobangService.rule_analyze(text)}


@router.post('/rewrite')
async def rewrite(body: RewriteBody):
    text, err = normalize_text(body.text, body.url)
    if err:
        return {'success': False, 'message': err, 'data': None}
    api_key, base_url, model = MobangService.resolve_provider(body.provider)
    try:
        data = await MobangService.llm_rewrite(text, body.mode, api_key=api_key, base_url=base_url, model=model)
        if data:
            return {'success': True, 'message': '改写完成（LLM）', 'data': data}
    except Exception:
        pass
    return {'success': True, 'message': '改写完成（规则兜底）', 'data': MobangService.rule_rewrite(text, body.mode)}
