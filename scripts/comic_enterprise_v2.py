#!/usr/bin/env python3
"""Enterprise account comic v2 - with persona + soft CTA."""
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
- 墨镜哥（"捻墨"墨镜、卫衣、咖啡）：做新媒体运营快3年，起过好几个万粉企业号，最近又从0起号一周涨粉近千。说话直白有料，不装逼。
- 女老板（短发）：开了家小公司，企业号交给员工做但做不起来，压力大，从迷茫→被点醒→知道怎么做

风格：口语化、像真人聊天、每页2-4句、有节奏感、比喻生活化。"""

USER = """请写8页条漫脚本。

故事线：
P1 封面：墨镜哥简单自我介绍（做运营快3年，起过好几个万粉企业号），引出话题"经常看到老板抱怨企业号做不起来"
P2 女老板出场，吐槽自己企业号花了几万块请人做，结果数据很差
P3 墨镜哥诊断三个常见错误：①目的不明确（既想变现又想曝光）②全是广告笔记用户观感差 ③选题排版不符合小红书调性
P4 墨镜哥说自己的经历："我最近又从0起了个号，一周涨粉近一千"，女老板震惊问怎么做到的
P5 方法一：先做商业定位（品牌宣传？引流获客？老板IP？选一个方向死磕）
P6 方法二：找20个对标账号拆解+建爆款选题库（小红书爆款内容很多是重复的，这就是捷径）
P7 方法三：做集合式清单比单品更容易爆+每周看数据复盘
P8 结尾要软：女老板感慨学到了，墨镜哥说"觉得有用就点个赞，我会持续分享这些实操经验"。不要硬推账号，不要说"关注我""来找我"，语气自然轻松，像朋友聊完天的结尾。

要求：
1. 给一句标题金句（有冲击力，适合封面）
2. 花费要写实：几万块，不要写几十万
3. 对话自然真实
4. P8结尾一定要软！不能硬推！就是"点赞关注+持续分享"这种语气

格式：
**标题金句：** XXXXX

**P1（封面）**
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
    outdir = "/root/.openclaw/workspace/comic_enterprise_v2"
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
