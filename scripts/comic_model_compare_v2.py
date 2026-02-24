#!/usr/bin/env python3
"""Generate comic story scripts with 3 models - client-acquisition industry version."""
import json, requests, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw"
BASE_URL = "https://api.003636.xyz/v1/chat/completions"

MODELS = {
    "GPT-5.3": "gpt-5.3-codex",
    "Gemini-3-Pro": "gemini-3-pro-preview",
    "Grok-4.1": "grok-4.1-fast",
}

SYSTEM_PROMPT = """你是一个小红书条漫脚本写手。你要写8页条漫的对话脚本。

角色设定：
- 墨镜哥：戴着写有"捻墨"的墨镜，穿卫衣，端着咖啡，冷静专业，说话直接有料
- 女老板：短发，做生意的，不懂运营，情绪从生气→困惑→恍然大悟→信任

风格要求：
- 对话要口语化，像真人聊天
- 每页2-4句对话，不要太长
- 要有情绪起伏和节奏感
- 举例用客资类行业（婚纱摄影/装修/教育培训/医美/月子中心这类需要客户主动咨询的行业）
- 最后一页引流到 @捻墨运营笔记
- 需要一句行业金句做标题（要有冲击力，让人想点进来）
- 比喻要生活化，不要太文绉绉"""

USER_PROMPT = """请写一个8页条漫脚本，主题是：「我被上一家代运营坑了八千块」

故事线：
P1 封面：女老板气冲冲出场（配标题金句）
P2 冲突：问清楚上一家做了什么，发了三个月零咨询
P3 诊断：看她的内容，发现问题
P4 核心问题：点明真正问题不是被坑，是没人告诉她关键的事
P5 解法第一步：搞清客户在搜什么
P6 解法第二步：让人想私信你
P7 解法第三步：数据复盘
P8 结尾+引流到@捻墨运营笔记

要求：
1. 先给出一句标题金句（10-15字，有冲击力）
2. 举例要用客资类行业（如婚纱摄影、装修、医美、教培等）
3. 每页格式如下：

**标题金句：** XXXXX

**P1（封面）**
👩 "台词"
🕶️ "台词"

请直接输出，不要加说明。"""

def call_model(name, model_id):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        "temperature": 0.85,
        "max_tokens": 3000,
    }
    try:
        start = time.time()
        resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=120)
        elapsed = time.time() - start
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            return name, content, elapsed, None
        else:
            return name, None, 0, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return name, None, 0, str(e)

def main():
    outdir = "/root/.openclaw/workspace/comic_comparison_v2"
    os.makedirs(outdir, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(call_model, n, m): n for n, m in MODELS.items()}
        for future in as_completed(futures):
            name, content, elapsed, error = future.result()
            if error:
                print(f"❌ {name}: {error}")
            else:
                print(f"✅ {name}: {len(content)} chars, {elapsed:.1f}s")
                with open(f"{outdir}/{name}.txt", "w") as f:
                    f.write(content)

if __name__ == "__main__":
    main()
