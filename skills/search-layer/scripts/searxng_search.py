#!/usr/bin/env python3
"""SearXNG local search - wrapper for OpenClaw usage."""
import sys
import json
import urllib.request
import urllib.parse

SEARXNG_URL = "http://127.0.0.1:8888/search"
DEFAULT_ENGINES = "google,bing,duckduckgo"

def search(query, count=10, engines=None, freshness=None):
    params = {
        "q": query,
        "format": "json",
        "engines": engines or DEFAULT_ENGINES,
    }
    if freshness == "day":
        params["time_range"] = "day"
    elif freshness == "week":
        params["time_range"] = "week"
    elif freshness == "month":
        params["time_range"] = "month"
    elif freshness == "year":
        params["time_range"] = "year"

    url = f"{SEARXNG_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-search/1.0"})
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    
    results = []
    seen = set()
    for r in data.get("results", []):
        u = r.get("url", "")
        if u in seen:
            continue
        seen.add(u)
        results.append({
            "title": r.get("title", ""),
            "url": u,
            "snippet": r.get("content", ""),
            "engine": r.get("engine", ""),
            "score": r.get("score", 0),
        })
        if len(results) >= count:
            break
    
    return {"query": query, "count": len(results), "results": results}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "test"
    out = search(query)
    print(json.dumps(out, ensure_ascii=False, indent=2))
