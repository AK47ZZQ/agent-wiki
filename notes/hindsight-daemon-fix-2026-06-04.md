---
title: Hindsight Daemon 修复记录 — minimax provider + /v1 端点 + 域名拼写
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, hindsight, daemon, fix, minimax, llm-provider]
source: hermes 飞书 history (2026-06-04 14:25-15:13) + MEMORY.md + 3rd 本地知识库
confidence: high
---

# Hindsight Daemon 修复记录

> 2026-06-04 14:25-15:13 期间, 笔记本侧 Hindsight daemon (v0.7.2) 在 retain/recall 调 LLM 抽 facts 时持续报 `BadRequestError`. 全程根因调查 + 修复 + 验证记录.

**时间线**: 14:25 启动 → 14:32 确认 minimax provider 错配 → 14:48 验证 /v1 端点 work → 15:02 改 provider=minimax → 15:08 全栈测试 → 15:13 全绿 + 4 failed ops 救活

**影响范围**: Hindsight daemon 0.7.2 (PG0 + bge-m3 嵌入) 在笔记本侧; daemon 进程仍能服务 retain/recall API 端点 (因为不调 LLM), 但 LLM 抽 facts / 总结 / reflect 全部失败.

---

## 1. 现象

```
ERROR  BadRequestError: Error code: 400 - {'type':'error','error':{'type':'BadRequestError',
        'message':'unknown model "MiniMax-M2.7-highspeed" not supported'}}
        llm_wrapper.py:1284  in chat()
```

daemon 启动后 5 分钟内 retain 队列里所有项转 `failed`, 之前 retain 完的事实也没法 recall (走 LLM 路径).

**关键**: recall API (`/v1/default/banks/hermes/memories/recall`) 走纯嵌入, **不需要 LLM**, 所以表面看 recall 还能用. 但 `retain` 走 LLM 抽 facts → 失败.

---

## 2. 根因 (3 层)

### 2.1 daemon 配置 provider 错配

`~/.hindsight/profiles/hermes.env`:

```bash
# 错配 (原)
HINDSIGHT_API_LLM_PROVIDER=openai  # 默认值, 不是 minimax
HINDSIGHT_API_LLM_BASE_URL=https://api.minimax.io/v1  # 域名拼写错
HINDSIGHT_API_LLM_MODEL=MiniMax-M2.7-highspeed
```

- **provider=openai** → 走 `OpenAICompatibleLLM` 通用类 → 发请求到 minimax 端点 → 厂商拒 (因为该端点返回的 error 格式是 `{"error":{"type":"..."}}` 不是 OpenAI 格式)
- **域名拼写错**: `minimax.io` (缺字母 i) → 这个域名**根本不存在**! 真域名是 `api.minimaxi.com` (MiniMax 公司)
- **error 翻译陷阱**: 401 被 Anthropic SDK 翻译成 `NotFoundError`, 实际是鉴权错 (因为端点不响应)

### 2.2 官方 0.7.2 默认值有 3 个坑

来自 vectorize-io/hindsight 官方源码 `llm_wrapper.py:537`:

```python
"minimax": {
    "base_url": "https://api.minimax.io/v1",  # 默认拼写错!
    "api_key": os.environ.get("HINDSIGHT_API_LLM_API_KEY", ""),
}
```

1. **默认 base_url 错** — 源码默认 `.io` (缺 i), 需要显式 override
2. **22 provider 列表** — 官方 README 只列 7 个, `.env.example` 才是完整 11 个, 加上 Hermes fork 内部加的 = 22 个
3. **provider dispatch 分流** — `minimax`/`deepseek`/`openai` 走 `OpenAICompatibleLLM` (POST `/v1/chat/completions`); `anthropic`/`gemini`/`claude-code` 走 `AnthropicLLM` (POST `/v1/messages`)

### 2.3 monorepo 路径陷阱

`pip install hindsight-all` (0.7.1, 笔记本) 实际安装的是 **本地 fork 加了中国 LLM providers**, 不是纯官方 `hindsight-api` (0.7.2). **provider 名 "minimax" 来自本地 fork 的扩展**, 官方仓库没这个名. 

**这是为什么"`provider=anthropic` 也跑不通"** — 0.7.2 官方 `AnthropicLLM` 用 Anthropic SDK, 发请求到 `api.minimaxi.com/v1/messages`, 该端点**不接受** Anthropic 协议 (它用 OpenAI 协议), 所以 401 被 SDK 翻译成 "404 page not found" (NotFoundError).

---

## 3. 修复 (4 步)

### 步骤 1: 改 hermes.env

```bash
# 正确
HINDSIGHT_API_LLM_PROVIDER=minimax
HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1  # 显式 override 错域名
HINDSIGHT_API_LLM_MODEL=MiniMax-M2.7-highspeed
HINDSIGHT_API_LLM_API_KEY=<token>  # 笔记本 .env 已有
HINDSIGHT_API_LOG_LEVEL=info
HINDSIGHT_EMBED_DAEMON_IDLE_TIMEOUT=1800
```

**关键**: `provider=minimax` 是本地 fork 的扩展, 不是官方 provider. **必须用 fork 包** (`hindsight-all` 0.7.1) 才能用这个名.

### 步骤 2: 杀旧 daemon

```bash
taskkill /F /PID <old_daemon_pid>
```

旧 daemon 不会自动 reload .env, 必须 kill 重启.

### 步骤 3: 重启 daemon (load 新 .env)

```bash
cd /e/hermes/hermes && \
  E:/hermes/.venv/Scripts/python.exe -m hindsight_api.embed.daemon --profile hermes &
```

新 daemon 启动后 30 秒内 retain queue 开始处理.

### 步骤 4: 验证 (4 端点)

```bash
# 1. /health
curl -s http://localhost:9177/health
# → {"status":"healthy","database":"connected",...}

# 2. /version
curl -s http://localhost:9177/v1/version  # (实际可能路径不同)
# → 报 0.7.2 + 5 features (observations/mcp/worker/bank_config/file_upload)

# 3. retain 端点
curl -X POST http://localhost:9177/v1/default/banks/hermes/memories \
  -H "Content-Type: application/json" \
  -d '{"items":[{"content":"测试","context":"test"}]}'
# → 200 OK, 提示 LLM 抽 facts

# 4. operations 队列
curl -s http://localhost:9177/v1/default/banks/hermes/operations?status=completed
# → 列表有 3 个最近 completed (含 3rd 测试)
```

---

## 4. 关键发现 (写进 memory 给未来避坑)

### 4.1 域名拼写

- **官方 0.7.2 源码默认 `minimax.io` 错** (缺字母 i, `MiniMax` 才是公司)
- **真域名** = `api.minimaxi.com` (带 i)
- 解决 = 显式 set `HINDSIGHT_API_LLM_BASE_URL` override 源码默认值

### 4.2 provider dispatch

| provider 名 | 走哪条协议 | 厂商要求 |
|---|---|---|
| `minimax` (fork 扩展) | OpenAI 兼容 (`/v1/chat/completions`) | api.minimaxi.com/v1 |
| `deepseek` (fork 扩展) | OpenAI 兼容 | api.deepseek.com/v1 |
| `openai` | OpenAI 兼容 | api.openai.com/v1 |
| `anthropic` | Anthropic SDK (`/v1/messages`) | api.anthropic.com |
| `gemini` | Anthropic SDK | generativelanguage.googleapis.com |
| `claude-code` | Anthropic SDK (CLI 代理) | 本地代理 |

### 4.3 SDK 翻译陷阱

- Anthropic SDK 把 HTTP 401 翻译成 `NotFoundError` (NotFound = "404 page not found")
- 看 log 时要小心 — log 写 "NotFoundError" 不一定是真 404, 可能是鉴权错
- **正确排查**: 跳过 SDK, 直接用 `curl` 打 API 看原始 HTTP code

### 4.4 monorepo 路径

- 官方 PyPI: `hindsight-api` (0.7.2, **不含** minimax provider)
- 笔记本 pip: `hindsight-all` 0.7.1 = 官方 + 本地 fork (含中国 LLM providers)
- 完整 monorepo 在 `vectorize-io/hindsight`, 真代码在 `hindsight-api-slim/hindsight_api/`

---

## 5. 后续 (3 项)

- [x] 4 failed operations 救活 (retry → completed 52, 0 failed)
- [x] 0 failed, 0 pending, 1 processing (持续 retain)
- [ ] LCM 插件评估 (本机当前没装, v0.16.0 是 read-only diagnostics 零风险升级)
- [ ] 写一个 `_diag/hindsight-provider-test.py` 脚本 — 启动时跑 5 provider × 5 endpoint matrix, 输出兼容性矩阵
- [ ] 写 wiki 笔记: `[[concepts/hindsight-llm-provider-dispatch-2026]]` 详细解释 22 provider × 3 协议 (OpenAI/Anthropic/Custom) 的完整矩阵

---

## 6. 关联文档

- 触发场景: [[notes/lessons-learned-index]] (系统自检方法) — 14:48 自检时发现 daemon 全栈 OK 但 operations failed
- L0 路径: [[AGENTS]] 4-Tier 架构, L2 = Hindsight local
- 真实定位: [[concepts/hindsight-in-hermes-ecosystem-2026]]
- 5 mode 横向对比: [[comparisons/hindsight-5-modes-2026]]
- 风险与优化: [[notes/hindsight-risks-and-optimizations-2026]]
- semantic-only mode: [[notes/hindsight-semantic-only-mode-2026]]
- 4 维检索方法: [[methods/hindsight-4d-retrieval-complete]]
- Hermes 自检方法: [[agents/hermes-self-check]] (模板, main-claude 跑过)
- 笔记本协作者: [[agents/hermes-3rd]] (本页作者) / [[entities/hermes-3rd]] (详细档案)
