---
title: Hindsight 本地部署 (Windows + Hermes native provider)
created: 2026-06-03
updated: 2026-06-03
type: note
tags: [tech, hindsight, local-deployment, hermes, native-provider, windows]
sources:
  - https://hindsight.vectorize.io/developer/api/quickstart
  - https://hindsight.vectorize.io/guides/2026/04/14/guide-migrate-hindsight-hermes-to-native-hermes-memory
  - local: C:\Python314\start_hindsight_local.py
confidence: high
---

# Hindsight 本地部署 (Windows + Hermes native provider)

> 2026-06-03 实测成功: Hindsight 0.6.1 local server + Hermes 2026 native provider

## 部署栈

| 组件 | 版本 | 来源 |
|---|---|---|
| `hindsight-api` | 0.6.1 | `pip install hindsight-api` (官方 Quick Start Option 1) |
| `hindsight-api-slim` | 0.6.1 | 依赖 |
| `pg0-embedded` | 0.14.2 | 内嵌 PostgreSQL |
| `sentence-transformers` | 5.5.1 | 嵌入模型 |
| Hermes | 2026+ | native provider |
| Python | 3.14.5 | Windows |
| LLM | MiniMax-M2.5-highspeed | OpenAI 兼容协议 |

## 为什么用 pip 不用 Docker

- ❌ **Docker 不可用**（Windows 无 Docker daemon）
- ✅ **官方 Quick Start Option 1** 就是 `pip install hindsight-api`
- ✅ 比 Docker 更轻量

## 启动步骤

### 1. 装 pip 包
```bash
pip install hindsight-api
# 自动装: hindsight-api-slim, pg0-embedded, sentence-transformers
```

### 2. 启 server (后台)
```bash
python -m hindsight_api.main --host 0.0.0.0 --port 8888
```

**必设 env vars**（用 `start_hindsight_local.py` 包装）：
- `HINDSIGHT_API_LLM_API_KEY` — LLM 用的 key
- `HINDSIGHT_API_LLM_BASE_URL` — LLM endpoint
- `HINDSIGHT_API_LLM_MODEL` — LLM 名
- `HINDSIGHT_API_WORKER_ID=hindsight-local` — **必设！防重启丢任务**

### 3. 验证 server
```bash
curl http://localhost:8888/health
# {"status":"healthy","database":"connected"}
```

### 4. 配 Hermes native provider

`~/AppData/Local/hermes/hindsight/config.json`:
```json
{
  "mode": "local",
  "apiKey": "",
  "apiUrl": "http://localhost:8888",
  "llmApiKey": "***",
  "llmBaseUrl": "https://api.minimaxi.com/v1",
  "llmModel": "MiniMax-M2.5-highspeed",
  "memory_mode": "hybrid",
  "prefetch_method": "recall",
  "banks": {
    "hermes": {"bankId": "hermes", "budget": "mid", "enabled": true}
  }
}
```

`~/.hermes/config.yaml` (或 `~/hermes-all/hermes/config.yaml`):
```yaml
memory:
  provider: hindsight
```

## 3 个 API 端点（实测工作）

| 操作 | 端点 | Schema 关键字段 |
|---|---|---|
| **Retain** | `POST /v1/default/banks/{bank}/memories` | `items: [{content, context}]`, `async: false` (同步) |
| **Recall** | `POST /v1/default/banks/{bank}/memories/recall` | `query`, `budget` (low/mid/high), `max_tokens` |
| **Reflect** | `POST /v1/default/banks/{bank}/reflect` | `query`, `budget`, `max_tokens` |
| **List** | `GET /v1/default/banks/{bank}/memories/list?limit=N` | 返回 `items[].text, .entities, .type` |

**关键字段**：memory unit 用 **`text`** 字段（不是 `content`）—— 之前 schema 假设错了

## 实测结果（2026-06-03）

### Retain → Recall 链路
```bash
# Retain
POST /v1/default/banks/hermes/memories
{"items": [{"content": "用户偏好中文表格报告..."}], "async": false}
→ {"success": true, "items_count": 1, "usage": {total_tokens: 3324}}

# Recall (sync retain 后立即命中, 不需 sleep!)
POST /v1/default/banks/hermes/memories/recall
{"query": "用户偏好什么", "budget": "mid"}
→ 4 results, 含 "用户偏好中文表格报告"
```

### Reflect (LLM 合成)
```bash
POST /v1/default/banks/hermes/reflect
{"query": "总结用户工作流偏好", "budget": "mid"}
→ 结构化中文回答, 含 4 个偏好总结
```

## 关键文件

| 文件 | 路径 | 用途 |
|---|---|---|
| 启动脚本 | `C:\Python314\start_hindsight_local.py` | 后台启 server |
| Server log | `C:\Users\Administrator\hindsight-local.log` | 实时日志 |
| PID | 6224 (当前) | 用 tasklist 查 |
| Hermes config | `~/AppData/Local/hermes/hindsight/config.json` | 8.2 KB |

## 关键陷阱（本次遇到）

1. **模块名错**：`hindsight_api.run` → 实际是 `hindsight_api.main`
2. **字段错**：`content` → memory unit 用 `text`
3. **Schema 错**：`{content: ...}` → 实际是 `{items: [{content, context}], async: false}`
4. **路径错**：`/memories/reflect` → 实际是 `/reflect` (顶级)

## 验证清单

- [x] `pip install hindsight-api` 装好
- [x] Server 跑 8888 端口
- [x] `curl /health` 返 `healthy`
- [x] Worker 跑了 (`worker_id=hindsight-local`)
- [x] Retain sync 成功
- [x] Recall 立即命中（不需 sleep）
- [x] Reflect LLM 合成返回中文结构化答案
- [x] Hermes plugin 标记 `active`
- [x] `hermes memory status` 报 `Provider: hindsight`

## 关联文档

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — 真实定位
- [[methods/install-hindsight-native-hermes-method]] — 完整方法
- `install-hindsight-as-hermes-memory` skill
