---
title: Hermes 安装 Hindsight 完整方法 (官方 native 路径)
created: 2026-06-03
updated: 2026-06-03
type: method
tags: [method, install, hermes, hindsight, native-provider, official]
sources:
  - https://hindsight.vectorize.io/sdks/integrations/hermes
  - https://hindsight.vectorize.io/guides/2026/04/14/guide-migrate-hindsight-hermes-to-native-hermes-memory
  - https://hindsight.vectorize.io/developer/api/quickstart
  - https://hindsight.vectorize.io/guides/2026/04/14/guide-hermes-memory-modes-with-hindsight-hybrid-context-tools
confidence: high
---

# Hermes 安装 Hindsight 完整方法 (官方 native 路径)

> **Hindsight 已被 Hermes 官方原生集成**。`pip install hindsight-all` 是**旧路径已弃用**。本方法基于 Hindsight 官方文档 2026-06 实测。

## 路径对比

| 路径 | 状态 | 推荐度 |
|---|---|---|
| **A. Hermes native provider**（`hermes memory setup`） | ✅ 当前推荐 | ⭐⭐⭐⭐⭐ |
| B. pip `hindsight-all` + 自建 server | ⚠️ 旧路径，已弃用 | ⭐⭐ |
| C. Docker `ghcr.io/vectorize-io/hindsight` | ✅ 生产推荐 | ⭐⭐⭐⭐ |

## 路径 A：Hermes Native Provider（推荐）

### Step 1: 前置

```bash
# 确认 Hermes 版本 (需要 2026+)
hermes --version

# 检查当前 memory 状态
hermes memory status
```

### Step 2: 启动 setup wizard

```bash
hermes memory setup
```

**交互流程**：
1. 选 **Hindsight**（不是 hindsight-hermes 旧 plugin）
2. 选 **mode**: `cloud`（推荐）或 `local`
3. 选 `cloud`：
   - 输入 `HINDSIGHT_API_KEY`（从 [hindsight.vectorize.io](https://hindsight.vectorize.io) 控制台拿）
   - API URL 默认 `https://api.hindsight.vectorize.io`
4. 选 `local`：
   - 选 LLM provider（推荐 Groq + `gpt-oss-20b`）
   - 输入 LLM API key
   - 自动启 Docker 容器

### Step 3: 配置 bank_id

```bash
# Wizard 会问 bank_id, 推荐: hermes (和项目同名)
hermes config set memory.bank_id hermes
```

### Step 4: 选 memory mode

```bash
# 推荐默认 hybrid + recall prefetch
# 这条命令实际是直接改 ~/.hermes/hindsight/config.json
python - <<'PY'
import json, os, pathlib
base = pathlib.Path(os.environ.get("HERMES_HOME", pathlib.Path.home() / ".hermes"))
path = base / "hindsight" / "config.json"
cfg = json.loads(path.read_text())
cfg["memory_mode"] = "hybrid"   # auto-recall + 显式工具
cfg["prefetch_method"] = "recall"  # 注入到每 turn 上下文
path.write_text(json.dumps(cfg, indent=2) + "\n")
PY
```

### Step 5: 验证

```bash
hermes memory status
# 期望: Provider: hindsight (native, mode=hybrid)
```

**实测 recall**：
```bash
hindsight memory retain hermes "用户偏好中文表格报告"
sleep 3  # 重要！async retain 延迟
hindsight memory recall hermes "用户偏好什么"
# 期望: 命中"中文表格报告"
```

## 路径 C：自托管 Docker（高级）

适合：
- 不愿用 Cloud
- 多设备自托管
- 数据全本地

### Step 1: 拉镜像

```bash
docker pull ghcr.io/vectorize-io/hindsight:latest
```

### Step 2: 启动容器（关键配置）

```bash
export OPENAI_API_KEY=sk-xxx  # 或 HINDSIGHT_API_LLM_API_KEY
export HINDSIGHT_API_WORKER_ID=hindsight-prod  # 必须！防重启丢任务

docker run --rm -it --pull always -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  -e HINDSIGHT_API_WORKER_ID=hindsight-prod \
  -v $HOME/.hindsight-docker:/home/hindsight/.pg0 \
  --name hindsight \
  ghcr.io/vectorize-io/hindsight:latest
```

**API 可用**：`http://localhost:8888/docs`

### Step 3: 配置 Hermes 走自托管

```bash
hermes config set memory.provider hindsight
hermes config set memory.mode local
hermes config set memory.api_url http://localhost:8888
# API key 可不设（local 不需要认证）
```

## 配置详解：`~/.hermes/hindsight/config.json`

```json
{
  "mode": "cloud",
  "api_url": "https://api.hindsight.vectorize.io",
  "api_key": "hsk_xxx",
  "bank_id": "hermes",
  "memory_mode": "hybrid",
  "prefetch_method": "recall"
}
```

| 字段 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `mode` | ✅ | "cloud" | "cloud" / "local" |
| `api_url` | ✅ | cloud 默认 | Hindsight server URL |
| `api_key` | cloud 必填 | — | Cloud token |
| `bank_id` | ✅ | "default" | 隔离/共享的单位 |
| `memory_mode` | ❌ | "hybrid" | hybrid/context/tools |
| `prefetch_method` | ❌ | "recall" | recall/reflect |

## 三种 Memory Mode 详解

### `hybrid`（官方推荐默认）
- ✅ Auto-recall：每 turn 开头自动拉相关历史
- ✅ 显式工具：模型可调 `hindsight_recall` / `hindsight_retain` / `hindsight_reflect`
- **适合**：大多数用户，要"convenience + control"

### `context`
- ✅ Auto-recall
- ❌ 显式工具不可见（模型不知有 memory tool）
- **适合**：生产 assistant（清洁 UX，少噪音）

### `tools`
- ❌ 无 auto-recall
- ✅ 显式工具
- **适合**：Agent 显式决定何时查

**关键规则**：
> "**`tools` mode is not broken when auto-recall disappears**. That is the design."

## Prefetch Method 详解

| 值 | 行为 |
|---|---|
| `recall` | 每 turn 开头 `recall(query=current_input)`，注入 top-k facts |
| `reflect` | 每 turn 开头 `reflect(query=current_input)`，注入 LLM 合成答案 |

**默认** `recall`（更省 token、更准）

## 3 种核心 API 调用

### Retain (写入)
```bash
hindsight memory retain hermes "Alice 在 Google 当软件工程师"
# 或
hindsight memory retain hermes "会议纪要..." --doc-id meeting-2026-06-03
```

**注意**：
- 异步处理（几秒后索引建好）
- 原文**不存**，只存 LLM 抽取的 facts + entities

### Recall (检索)
```bash
hindsight memory recall hermes "Alice 在哪工作"
# 控制参数
hindsight memory recall hermes "..." --budget low --max-tokens 2048
```

**参数**：
- `max_tokens` (default 4096)
- `budget`: `low`/`mid`/`high`
- `types`: filter by world/experience/entity/belief
- `tags` / `tags_match`

### Reflect (LLM 合成)
```bash
hindsight memory reflect hermes "总结用户偏好"
```

**输出**：带情绪/态度的合成回答（"disposition-aware"）

## 常见配置错误

| 错误 | 表现 | 修复 |
|---|---|---|
| 装错 pip 包 | `hermes memory status` 不认 | `pip uninstall hindsight-all` + 走 native |
| 用了 `context` mode | 模型不知有 memory tool | 改 `hybrid` |
| retain 后立即 recall | 0 结果 | 至少 `sleep 3` |
| 没设 `HINDSIGHT_API_WORKER_ID` (Docker) | 重启后任务丢失 | 加 env var |
| `bank_id` 选错 | 跨用户串记忆 | 用 stable user id 派生 |

## 验证清单

- [ ] `hermes memory status` 显示 `Provider: hindsight`
- [ ] `hindsight memory retain hermes "..."` 成功
- [ ] 等待 3-5 秒
- [ ] `hindsight memory recall hermes "..."` 命中
- [ ] 在新 session 开头，Hermes 自动有历史上下文（hybrid mode 验证）
- [ ] `~/.hermes/hindsight/config.json` 存在且合法
- [ ] 跨 session recall 仍命中（持久化验证）

## 关联文档

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — 真实定位
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider 对比
- [[notes/lcm-upgrade-v0.12-to-v0.15]] — LCM 升级
