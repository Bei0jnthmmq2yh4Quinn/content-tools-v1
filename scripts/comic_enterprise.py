#!/usr/bin/env python3
"""3-model comic scripts based on enterprise account operations content."""
import json, requests, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw"
BASE_URL = "https://api.003636.xyz/v1/chat/completions"

MODELS = {
    "GPT-5.3": "gpt-5.3-codex",
    "Gemini-3-Pro": "gemini-3-pro-preview",
    "Grok-4.1": "grok-4.1-fast",
}

SYSTEM = """你是一个小红书条漫脚本写手。

角色：
- 墨镜哥（"捻墨"墨镜、卫衣、咖啡）：运营老手，说话直白有料
- 女老板（短发）：企业号做不起来，压力大，从迷茫→被点醒→知道怎么做

风格：口语化、像真人聊天、每页2-4句、有节奏感、比喻生活化、不要太书面。"""

USER = """请把以下企业号运营干货改编成8页条漫脚本。

原始内容要点：
1. 很多企业号数据差的原因：目的不明确（既想变现又想曝光），全是广告笔记用户观感差，选题排版不符合小红书调性
2. 运营思路：先做商业定位（品牌宣传？引流获客？老板IP？），竞品分析（找20个对标账号），搭建爆款选题库（小红书爆款内容很多是重复的，这就是捷径），做集合式清单（比单一产品更容易爆），数据复盘（看点赞收藏转发增粉）

要求：
1. 给一句标题金句（10-15字，有冲击力，适合做封面）
2. 故事线：P1封面（女老板抱怨企业号做不起来）→ P2问题暴露（全是广告没人看）→ P3诊断（目的不清/调性不对）→ P4核心（先定位再动手）→ P5竞品分析（抄作业的正确方式）→ P6选题库（爆款是可以复制的）→ P7集合式清单→ P8数据复盘+引流@捻墨运营笔记
3. 对话自然，女老板反应真实
4. 引流到 @捻墨运营笔记

格式：
**标题金句：** XXXXX

**P1（封面）**
👩 "台词"
🕶️ "台词"

直接输出脚本。"""

def call_model(name, model_id):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
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
    outdir = "/root/.openclaw/workspace/comic_enterprise"
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
