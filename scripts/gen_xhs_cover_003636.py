#!/usr/bin/env python3
"""Generate XHS covers via 003636 with reference image support."""

import base64
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = "https://api.003636.xyz/v1"
API_KEY = "sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw"
MODEL = "gemini-3-pro-image"

def image_to_data_url(path: str) -> str:
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    # guess mime
    if path.lower().endswith(".png"):
        mime = "image/png"
    else:
        mime = "image/jpeg"
    return f"data:{mime};base64,{b64}"

def generate(prompt: str, ref_image_path: str | None, output_path: str) -> str:
    content = []
    if ref_image_path:
        data_url = image_to_data_url(ref_image_path)
        content.append({
            "type": "image_url",
            "image_url": {"url": data_url}
        })
    content.append({"type": "text", "text": prompt})

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 4096,
    }

    req = Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )

    with urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode())

    # Try to extract image from response
    # Format 1: choices[0].message.images[0].image_url.url
    # Format 2: choices[0].message.content contains data url
    msg = data.get("choices", [{}])[0].get("message", {})
    
    # Try images array first
    imgs = msg.get("images") or []
    if imgs:
        data_url = imgs[0].get("image_url", {}).get("url", "")
    else:
        # Try content directly
        c = msg.get("content", "")
        if isinstance(c, str) and c.startswith("data:image/"):
            data_url = c
        elif isinstance(c, list):
            # multimodal content list
            for item in c:
                if isinstance(item, dict) and item.get("type") == "image_url":
                    data_url = item.get("image_url", {}).get("url", "")
                    break
            else:
                data_url = ""
        else:
            data_url = ""

    if not data_url or not data_url.startswith("data:image/"):
        # dump response for debug
        print(f"DEBUG response: {json.dumps(data, ensure_ascii=False)[:2000]}", file=sys.stderr)
        raise RuntimeError("No image in response")

    b64 = data_url.split(",", 1)[1]
    raw = base64.b64decode(b64)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(f"Image saved: {out.resolve()}")
    print(f"MEDIA: {out.resolve()}")
    return str(out.resolve())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", required=True)
    parser.add_argument("--input", "-i", help="Reference image path")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()
    generate(args.prompt, args.input, args.output)
