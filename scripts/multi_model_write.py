#!/usr/bin/env python3
"""Call multiple models with the same writing prompt, save results."""
import json, requests, sys, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw"
BASE_URL = "https://api.003636.xyz/v1/chat/completions"

MODELS = {
    "GPT-5.3": "gpt-5.3-codex",
    "Gemini-3-Pro": "gemini-3-pro-preview",
    "DeepSeek-V3.2": "deepseek-ai/DeepSeek-V3.2",
    "Grok-4.1": "grok-4.1-fast",
}

SYSTEM_PROMPT = """你是一个小红书代运营文案写手。请严格按照以下风格档案写作：

## 语气基调
- 像面对面跟人聊天，不是在"写文章"
- 不端着、不教人、不训话
- 用"讲句实话"开头
- 自然、随意、但有逻辑
- 像一个做了很多年的老手在跟你掏心窝子

## 用词习惯
- "比方说"（不用"比如"）
- "就是说"（口语连接词）
- "我见过最多的就是…"（用个人经验带出观点）
- "你要给人一种感觉"
- "讲句实话"（开场白）

## 句式节奏
- 短句为主，但不是刻意每句都短
- 会有自然的长句（口语式的，带"就是说""然后"串联）
- 不用排比、不用对仗、不刻意造金句
- 金句是自然冒出来的，不是设计出来的

## 喜欢用的手法
- 俗语/古话
- 生活化比喻
- 反问
- 个人经验背书："我见过最多的…"

## 口语特征
- "我觉得"高频出现
- "然后"做转折/递进
- "可能还是…会比较好一点"
- "对吧？"结尾寻求共识
- "嘛"做语气软化

## 排版
- 自然分段，不要太多分隔线
- 不用emoji装饰
- 不用markdown标题符号
- 段落之间靠空行呼吸

## CTA风格
- 不喜欢硬CTA
- 结尾要有"格局感"
- 用生活化比喻收束"""

USER_PROMPT = """请写一篇小红书笔记，主题是：

《个人接代运营，一个月3000，不画饼不对赌》

要求：
1. 目标读者是想找代运营但怕被坑的老板
2. 核心卖点：按月付、不套路、帮你理清方向
3. 要有真实感，像个做了很多年的人在聊天
4. 结尾CTA：私信报行业+现状+目标
5. 加上适合的话题标签
6. 字数500-800字

只输出正文内容，不要加任何说明。"""

def call_model(name, model_id):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        "temperature": 0.8,
        "max_tokens": 2000,
    }
    try:
        start = time.time()
        resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=120)
        elapsed = time.time() - start
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return name, content, elapsed, None
        else:
            return name, None, 0, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return name, None, 0, str(e)

def main():
    outdir = "/root/.openclaw/workspace/model_comparison"
    os.makedirs(outdir, exist_ok=True)
    
    print(f"Calling {len(MODELS)} models in parallel...")
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(call_model, name, mid): name for name, mid in MODELS.items()}
        for future in as_completed(futures):
            name, content, elapsed, error = future.result()
            if error:
                print(f"❌ {name}: {error}")
                results[name] = f"ERROR: {error}"
            else:
                print(f"✅ {name}: {len(content)} chars, {elapsed:.1f}s")
                results[name] = content
                # Save individual file
                with open(f"{outdir}/{name}.txt", "w") as f:
                    f.write(content)
    
    # Save combined
    with open(f"{outdir}/all_models.md", "w") as f:
        for name in MODELS:
            f.write(f"\n{'='*60}\n")
            f.write(f"## {name}\n")
            f.write(f"{'='*60}\n\n")
            f.write(results.get(name, "N/A"))
            f.write("\n\n")
    
    print(f"\nDone! Results saved to {outdir}/")

if __name__ == "__main__":
    main()
