from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

DEFAULT_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
DEFAULT_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.003636.xyz/v1')
DEFAULT_API_KEY = os.getenv('OPENAI_API_KEY', '')


class MobangService:
    @staticmethod
    def split_sentences(text: str) -> list[str]:
        parts = re.split(r'[。！？!?.\n]+', text)
        return [p.strip() for p in parts if p.strip()]

    @classmethod
    def rule_analyze(cls, text: str) -> dict[str, Any]:
        sentences = cls.split_sentences(text)
        hook = sentences[0] if sentences else text[:30]
        topic = ' / '.join(sentences[:2])[:60] if sentences else '未识别'
        emotion = '情绪刺激强，适合做开头钩子' if any(k in text for k in ['一定', '千万', '真的', '立刻', '马上', '为什么']) else '偏理性表达，可加强冲突感'
        cta = '结尾补一句“你更适合哪种做法？评论区聊聊”。'
        structure = []
        if sentences:
            structure.append(f'1. 开头钩子：{sentences[0]}')
        if len(sentences) > 1:
            structure.append(f'2. 问题展开：{sentences[1]}')
        if len(sentences) > 2:
            structure.append(f'3. 解决方案/案例：{"；".join(sentences[2:4])}')
        if len(sentences) > 4:
            structure.append(f'4. 收尾总结：{sentences[-1]}')
        why = '这类内容容易传播，因为它有明确钩子、具体场景、低理解门槛，并且能让用户迅速代入自己的处境。'
        return {'hook': hook, 'topic': topic, 'emotion': emotion, 'cta': cta, 'structure': structure, 'why_it_works': why, 'fallback': True}

    @classmethod
    def rule_rewrite(cls, text: str, mode: str) -> dict[str, Any]:
        base = cls.rule_analyze(text)
        hook = base['hook']
        title_map = {'douyin': '抖音口播改写版', 'xiaohongshu': '小红书图文改写版', 'spoken': '更口语的表达版', 'lead': '更适合接单转化版', 'opinion': '更适合观点输出版'}
        intro_map = {'douyin': '开头直接抛观点，节奏更快，适合 30~60 秒口播。', 'xiaohongshu': '加强标题感与结构感，更适合图文或口播转图文。', 'spoken': '整体更像真人说话，减少书面感。', 'lead': '强化结果、信任和案例表达，更适合转化与接单。', 'opinion': '加强态度和判断，更适合做观点型内容。'}
        if mode == 'douyin':
            script = f"{hook}。\n\n很多人做内容没结果，不是因为不努力，而是第一句就没人想听。\n\n你要先把问题说到用户心里，再给一个马上能用的做法，最后再补一句让人愿意互动的话。"
        elif mode == 'xiaohongshu':
            script = f"标题建议：{hook}\n\n今天想聊一个很多人都会踩的点。\n\n为什么同样的内容，别人发了有反馈，你发了却没动静？问题往往不在内容本身，而在表达顺序。\n\n更好的写法是：先抛痛点，再给方法，最后给一个能马上照做的小动作。"
        elif mode == 'spoken':
            script = f"其实很多人都忽略了一个点：{hook}。\n你先把用户最痛的那个点说出来，再往下讲方法，别人就更容易听进去。"
        elif mode == 'lead':
            script = f"{hook}。\n真正能带来转化的内容，通常都有三个点：先说结果，再说过程，再说你能怎么帮到别人。"
        else:
            script = f"先说结论：{hook}。\n一条内容之所以能爆，不只是因为信息对，而是它把用户的情绪、立场和场景一下子拉进来了。"
        return {'mode': mode, 'title': title_map.get(mode, '改写版'), 'summary': intro_map.get(mode, '根据原内容做出的改写。'), 'script': script, 'fallback': True}

    @classmethod
    async def _chat_json(cls, prompt: str, *, api_key: str, base_url: str, model: str) -> dict[str, Any]:
        payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': '你是结构化 JSON 输出助手，只输出合法 JSON。'},
                {'role': 'user', 'content': prompt},
            ],
            'temperature': 0.7,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f'{base_url.rstrip("/")}/chat/completions', headers={'Authorization': f'Bearer {api_key}'}, json=payload)
            r.raise_for_status()
            data = r.json()
        content = data['choices'][0]['message']['content']
        return json.loads(content)

    @classmethod
    async def llm_analyze(cls, text: str, *, api_key: str, base_url: str, model: str) -> dict[str, Any] | None:
        if not api_key:
            return None
        prompt = f'你是内容拆解助手。请把下面文本拆成 JSON，字段必须包含：hook, topic, emotion, cta, structure(数组), why_it_works。只返回 JSON。\n\n文本：{text}'
        obj = await cls._chat_json(prompt, api_key=api_key, base_url=base_url, model=model)
        obj['fallback'] = False
        return obj

    @classmethod
    async def llm_rewrite(cls, text: str, mode: str, *, api_key: str, base_url: str, model: str) -> dict[str, Any] | None:
        if not api_key:
            return None
        prompt = f'你是内容改写助手。请把下面文本改写成{mode}模式，返回 JSON，字段必须包含：mode, title, summary, script。只返回 JSON。\n\n原文：{text}'
        obj = await cls._chat_json(prompt, api_key=api_key, base_url=base_url, model=model)
        obj['fallback'] = False
        return obj

    @classmethod
    def resolve_provider(cls, provider: dict[str, Any] | None) -> tuple[str, str, str]:
        provider = provider or {}
        api_key = (provider.get('api_key') or '').strip() or DEFAULT_API_KEY
        base_url = (provider.get('base_url') or '').strip() or DEFAULT_BASE_URL
        model = (provider.get('model') or '').strip() or DEFAULT_MODEL
        return api_key, base_url, model
