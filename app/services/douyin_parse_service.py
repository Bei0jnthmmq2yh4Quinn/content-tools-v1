from __future__ import annotations

import json
import subprocess
from typing import Any, Dict


class DouyinParseService:
    @staticmethod
    def parse(url: str) -> Dict[str, Any]:
        cmd = [
            'yt-dlp',
            '--dump-single-json',
            '--no-warnings',
            '--skip-download',
            url,
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=40, check=True)
        except Exception as e:
            return {'success': False, 'message': f'链接解析失败: {e}', 'text': '', 'meta': {}}

        try:
            data = json.loads(result.stdout)
        except Exception as e:
            return {'success': False, 'message': f'解析 JSON 失败: {e}', 'text': '', 'meta': {}}

        title = (data.get('title') or '').strip()
        description = (data.get('description') or '').strip()
        uploader = data.get('uploader') or data.get('channel') or ''

        subtitle_texts = []
        subtitles = data.get('subtitles') or {}
        auto_captions = data.get('automatic_captions') or {}
        for bucket in (subtitles, auto_captions):
            for _lang, items in bucket.items():
                for item in items or []:
                    if item.get('ext') == 'json3' or item.get('ext') == 'srv3':
                        continue
                    if item.get('url'):
                        subtitle_texts.append(f"字幕链接: {item['url']}")
                        break
                if subtitle_texts:
                    break
            if subtitle_texts:
                break

        pieces = []
        if title:
            pieces.append(f'标题：{title}')
        if uploader:
            pieces.append(f'作者：{uploader}')
        if description:
            pieces.append(f'简介：{description}')
        if subtitle_texts:
            pieces.append('\n'.join(subtitle_texts))

        text = '\n'.join(pieces).strip()
        return {
            'success': bool(text),
            'message': '已解析链接元信息，可继续拆解' if text else '拿到了链接，但没有足够文本内容',
            'text': text,
            'meta': {
                'title': title,
                'uploader': uploader,
                'has_description': bool(description),
                'has_subtitle_link': bool(subtitle_texts),
            },
        }
