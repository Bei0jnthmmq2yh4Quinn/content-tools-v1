#!/usr/bin/env python3
"""
Direct Xiaohongshu API client using cookies (no MCP server needed).
"""

import json
import requests
import hashlib
import time
import random
import string

# Cookie 配置
COOKIES = {
    "a1": "19ac07e314d4g34oon6es9ui0h5nislrd3anmww2950000918347",
    "web_session": "0400698fd749d356ed9479edbd3b4bd9440b5f",
    "webId": "3e4cb84f0247ccc11844f11126bf5d43",
    "gid": "yj0S8WdWDif0yj0S8WdqyqEE4f4kq4llIKdM0Jjj738x2I28I3M1F6888jyYq4W84fJdjfjd",
    "xsecappid": "xhs-pc-web",
}

BASE_URL = "https://edith.xiaohongshu.com"
WEB_URL = "https://www.xiaohongshu.com"

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://www.xiaohongshu.com",
        "Referer": "https://www.xiaohongshu.com/",
        "Content-Type": "application/json;charset=UTF-8",
    }

def check_login():
    """检查登录状态"""
    url = f"{BASE_URL}/api/sns/web/v2/user/me"
    
    try:
        resp = requests.get(
            url,
            headers=get_headers(),
            cookies=COOKIES,
            timeout=30
        )
        data = resp.json()
        
        if data.get("success"):
            user = data.get("data", {})
            print(f"✅ 已登录")
            print(f"   用户ID: {user.get('user_id', 'Unknown')}")
            print(f"   昵称: {user.get('nickname', 'Unknown')}")
            return True, data
        else:
            print(f"❌ 未登录或 session 已过期")
            print(f"   错误: {data.get('msg', 'Unknown error')}")
            return False, data
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False, None

def search_notes(keyword, page=1, page_size=20):
    """搜索笔记"""
    url = f"{BASE_URL}/api/sns/web/v1/search/notes"
    
    payload = {
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
        "search_id": ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
        "sort": "general",
        "note_type": 0,
    }
    
    try:
        resp = requests.post(
            url,
            headers=get_headers(),
            cookies=COOKIES,
            json=payload,
            timeout=30
        )
        data = resp.json()
        
        if data.get("success"):
            items = data.get("data", {}).get("items", [])
            print(f"🔍 搜索 '{keyword}' 找到 {len(items)} 条结果:\n")
            
            for i, item in enumerate(items, 1):
                note = item.get("note_card", {})
                user = note.get("user", {})
                interact = note.get("interact_info", {})
                
                print(f"[{i}] {note.get('display_title', '无标题')}")
                print(f"    作者: {user.get('nickname', 'Unknown')}")
                print(f"    点赞: {interact.get('liked_count', '0')}")
                print(f"    note_id: {item.get('id')}")
                print()
            return True, data
        else:
            print(f"❌ 搜索失败: {data.get('msg', 'Unknown')}")
            return False, data
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False, None

def get_user_info():
    """获取当前用户信息"""
    url = f"{BASE_URL}/api/sns/web/v1/user/selfinfo"
    
    try:
        resp = requests.get(
            url,
            headers=get_headers(),
            cookies=COOKIES,
            timeout=30
        )
        data = resp.json()
        
        if data.get("success"):
            user = data.get("data", {})
            print(f"✅ 用户信息:")
            print(f"   昵称: {user.get('nickname', 'Unknown')}")
            print(f"   粉丝: {user.get('fansCount', 0)}")
            print(f"   关注: {user.get('follows', 0)}")
            print(f"   获赞: {user.get('likedCount', 0)}")
            return True, data
        else:
            print(f"❌ 获取失败: {data.get('msg', 'Unknown')}")
            return False, data
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False, None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python xhs_direct.py login     # 检查登录状态")
        print("  python xhs_direct.py search <关键词>  # 搜索笔记")
        print("  python xhs_direct.py user      # 获取用户信息")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "login":
        check_login()
    elif cmd == "search" and len(sys.argv) > 2:
        search_notes(sys.argv[2])
    elif cmd == "user":
        get_user_info()
    else:
        print(f"未知命令: {cmd}")
