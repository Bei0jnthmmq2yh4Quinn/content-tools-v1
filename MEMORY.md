# MEMORY.md — 热缓存层

> 速查表，覆盖 90% 日常解码。深度信息查 memory/ 子目录。
> 
> 架构：热缓存 (MEMORY.md) → 深度存储 (memory/**/*.md)
> 查找路径 A（确定性）：热缓存 → glossary → 档案
> 查找路径 B（语义）：memory_search → memory_get

## 人物速查
- **老板 / xqp** — Telegram @nianmo173, EST 时区, 做小红书代运营, 偏好稳定不折腾

## 项目速查
- **捻墨** — 小红书代运营品牌 → `memory/projects/nianmo-xhs.md`

## 偏好与协议
- 沟通直接，不喜欢废话
- 不存储/追踪媒体文件
- 不在聊天里处理密码
- 长期记忆尽量多存有用上下文

## 环境速查
- 默认模型：openai-custom/gpt-5.2 (003636)
- 备用模型：anyrouter/claude-opus-4-6
- 搜索：Tavily ✅ / Exa ✅ / Grok ✅ / MinerU ✅ / SearXNG ✅ / Brave ❌（不使用）
- 搜索策略：默认走 search-layer + SearXNG，不用 Brave/web_search
- 小红书 MCP：localhost:18060 ✅
- Twitter/X：bird v0.8.0, @Nian_Mo_ ✅
- 详情 → `memory/context/environment.md`

## 深度存储索引
| 文件 | 内容 |
|------|------|
| `memory/glossary.md` | 缩写/代号/术语解码器 |
| `memory/post-mortems.md` | 经验教训 |
| `memory/projects/nianmo-xhs.md` | 捻墨项目详情 |
| `memory/context/environment.md` | 部署/工具栈/API 配置 |
| `memory/people/` | 人物档案（待补充） |
| `memory/knowledge/` | 可复用知识（待补充） |

## 维护规则
- 高频条目（周 3 次+）晋升到此文件
- 30 天未用条目降级回深度存储
- heartbeat 定期巡检
