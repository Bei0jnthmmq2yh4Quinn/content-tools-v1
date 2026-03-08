# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## GitHub

- **Token (Classic, 满权限)**: `[REDACTED_GITHUB_TOKEN]`

---

### Search Layer

- **Grok API URL**: `https://api.003636.xyz/v1`
- **Grok API Key**: `[REDACTED_GROK_API_KEY]`
- **Grok Model**: `grok-4.1`
- **Exa API Key**: `7931e6ea-e111-4929-a069-9daead49c372`

### SearXNG (Local)

- **URL**: `http://127.0.0.1:8888/search`
- **Script**: `skills/search-layer/scripts/searxng_search.py`
- **Engines**: google, bing, duckduckgo
- **Usage**: `python3 skills/search-layer/scripts/searxng_search.py "查询内容"`

---

### SSH

- **ccs** → `root@23.95.34.155`, pwd: `lmmxqp980706Aa`
  - Debian 5.10, 1G RAM, 25G disk
- **备用服务器** → `root@23.80.89.41`
- **大白服务器** → `root@38.146.29.115`, pwd: `2Kb{e:iF`
- **do服务器** → `root@165.227.185.241`, pwd: `kaikaixinxin@`
  - Debian 13, 4G RAM, 79G disk, Caddy + Docker + PostgreSQL

---

Add whatever helps you do your job. This is your cheat sheet.
