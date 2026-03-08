# 墨榜本轮可提交范围（最小集）

## 目标
把“拆脚本工具”收口成一版可交付的内容工作台最小版本，避免把无关记忆文件、图片产物、技能目录、临时脚本一起提交。

## 建议纳入提交的文件
- `mobang_index_v2.html` — 前端内容工作台页面
- `mobang_main_fixed.py` — FastAPI 主入口（已接入 subscriptions）
- `mobang_route_v5.py` — 内容拆解/改写路由最终版
- `mobang_service_v3.py` — 内容拆解/改写服务最终版
- `topics_v2.py` — AI 选题生成
- `trends_v3.py` — 热点查询 / suggestions / brief
- `subscriptions_v2.py` — 订阅草稿与推送预览
- `douyin_parse_service.py` — 抖音链接解析支持（若线上代码库没有现成同名服务）

## 暂不纳入提交的文件
- `mobang_route_v2.py`
- `mobang_route_v3.py`
- `mobang_route_v4.py`
- `mobang_service.py`
- `mobang_service_v2.py`
- `mobang_v1_index.html`
- `mobang_v2_index.html`
- `subscriptions.py`
- `patch_main.py`

## 原因
这些文件更像演进过程中的中间版本或临时脚本，不适合和最终版一起进同一次提交。

## 注意
当前 workspace 的 git 状态很脏，包含大量无关删除/记忆文件改动；提交时必须按文件白名单精确 add，不能直接 `git add .`。
