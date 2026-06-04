---
title: Agent Memory 状态镜像 (2026-06-03)
created: 2026-06-03
updated: 2026-06-03
type: concept
tags: [meta, memory, mirror, agent-state, handoff]
sources:
  - ~/AppData/Local/hermes/memories/MEMORY.md (3448 chars)
  - ~/AppData/Local/hermes/memories/USER.md (1543 chars)
confidence: high
---

# Agent Memory 状态镜像 (2026-06-03)

> **本文件 = MEMORY.md + USER.md 的镜像**, 给其他 agent / 未来 session 看当前状态.
> **改 memory 必同时改本文件** (用 memory-staleness-detection skill 验证).

## MEMORY.md 镜像 (9 段, 3448 chars, 43% of 8000)

### §1 MCP 6 servers
- minimax×2 + tavily-github/google/microsoft/ggc
- 搜索矩阵: MiniMax CN MCP 优先 (150次/5h) → Tavily MCP 3key ~0.3s → DuckDuckGo → REST
- MiniMax MCP 第一优先不限配额 (Tavily REST 已 401)

### §2 Wiki 117页 (2026-06-03)
- archiver.py (--all/--force/--stats/--dry-run/--json), wiki-ingest/query/lint
- Obsidian vault:27124 HTTPS key=hermes-obsidian-local-cli verify=False
- 5 文档导出: `~/hermes-all/exports/hindsight-agent-brief/` (7文件, 61KB)

### §3 Services (3) + Tailscale (未启用)
- Workspace:3000 v2.3.0 (`PROXY_BACKEND_URL=... node server-entry.js`)
- Gateway:8642 (改 .py 流程见 §8)
- Dashboard:9119
- Tailscale=手机方案**未启用** (Frp 已弃用)
- GitHub push SSL 3次重试+5s间隔, backup排除>100MB, git checkout --force 绕锁

### §4 Hindsight v4 (final 精简)
- pip `hindsight-api 0.6.1` + server @ 8888 (模块 `hindsight_api.main`, **不是 `.run`**)
- 3 types + entities[] + disposition
- 内存: rss 9.7MB / peak 1.2GB — **不是泄漏**
- 跨语言: 英文嵌入 + 多语言 reranker 兜底, 92% 命中
- **Hindsight plugin 默认每 turn 静默 retain** (`_auto_retain=True`) — ~10k tokens/天, **用户接受**
- handoff v1.3 (5 重: MAX=5/天 + sha256 + 长度 + 人工 + 幂等) = manual-only
- watchdog = RSS 监控 (1GB warn, 不自动 kill)
- **0 cron, 0 hook, 0 自动 retain (除 plugin 默认)**

### §5 飞书 pipeline 停摆 + 4 层栈
- 飞书: 0 cron / 0 Task Scheduler, 最后更新 2026-05-30
- L3 memory tool 94% 满 (待清理)
- 4 层记忆栈: L0 messages | L1 LCM v0.15.0 | L2 Hindsight | L3 memory tool
- Hermes hooks config 需 Python `Path.write_text` 绕 protected
- 事件命名可能误导 (e.g. on_session_end 实际是 per-turn, payload 无 messages)

### §6 Swarm (过渡期: v2 路由已切, v1 profiles 还在)
- **v2**: 10 个 semantic workers (orchestrator/builder/reviewer/qa/researcher/ops-watch/maintainer/strategist/inbox-triage/km-agent) in `swarm.yaml`
- **v1**: profiles 目录仍 7 个老 `minimax-worker1~7` (未迁移)
- 实际 worker 模型 minimax-cn/MiniMax-M2.7 (fallback_providers:[])
- 派发后 30s 看门狗 → 一次性汇报
- 飞书 "Home" channel (oc_56a22bfc2c7d92617d42ec50f62a5723) = 同步目标
- 入口 wrapper: `orchestrator:plan` (理论) / minimax-worker1~7 (实际)
- 状态: **v2 路由就位, v1 profiles 待迁移**

### §7 Mnemosyne (P1 备用, 未启用)
- pip `mnemosyne-memory` (跳过 [all]) + fastembed
- `hermes config set memory.provider mnemosyne` + restart
- 4 层: working (24h TTL, auto) + episodic (长期, 手动) + scratchpad + legacy
- ⚠️ `mnemosyne delete` 不删 episodic, 要 SQL
- 详见 wiki `concepts/mnemosyne-installation-windows-2026`

### §8 Gateway .py 改流程 (高频)
- 改 `runtime_footer.py` 或 `run.py` → 删 `__pycache__/*.cpython-*.pyc` → `hermes gateway start --replace` 或 `taskkill + start`
- **不删 pycache 新代码不生效**
- 触发: 改 hooks / plugins / memory provider

### §9 Agent 编排规则
- 任务 = 写 plan (Plan mode) → `orchestrator:plan` 路由 → delegate_task / cronjob / terminal bg → wait notify → 一次摘要
- **不用 cron 投进度, 不用 Kanban 中间消息**

## USER.md 镜像 (6 段, 1543 chars, 31% of 5000)

### §1 Footer 格式
`[model, context_pct, context_k, turn_time, api_calls, total_tokens]` 有数据才显示

### §2 结构化知识管理偏好
- session→wiki→Obsidian Graph View
- 看重端到端组件+可复用技能

### §3 DSPy + Harness 兴趣
- DSPy (BootstrapFewShot/CoT/MIPRO/ReAct)
- Harness Engineering → 注入 hermes-workflow

### §4 诚实评估 > 推销
- 偏好 ROI + 现状评估, 不接受 feature 列表
- 关键案例: peak_wset 1.2GB 不是泄漏
- ai-harness-exploration 6 步法是默认工作流
- Destructive 操作必先 ROI 评估
- 4 个反弹信号 → 立即停推销

### §5 默认工作流 (DeepSeek + Swarm)
- DeepSeek 5% 编排 + Swarm 派发 95%
- 入口 wrapper: `orchestrator:plan` (v2) / 实际 minimax-worker1~7 (v1)
- Worker 模型 minimax-cn/MiniMax-M2.7
- 后台看门狗 30s 轮询 → **一次性汇报, 零噪**
- **当前过渡期**: v2 路由 + v1 profiles 并存

### §6 2026-06-03 精简后状态
- 0 cron, 0 hook, 0 自动 retain (除 Hindsight plugin 默认接受)
- 维护 cron (夜间 02:00 + 早晨 08:00) **全删**, 之前"必须每次汇报"规则**作废**
- 飞书 09:00 同步 cron **也停摆**
- Git 仓库作为云端备份可克隆部署
- Swarm 是 v2 架构 (10 semantic workers + swarm.yaml 路由), 不是 v1 numbered lanes

## 容量配置 (config.yaml)

```yaml
memory_char_limit: 8000   # 之前 2200, 扩 3.6× (2026-06-03)
user_char_limit: 5000     # 之前 1375, 扩 3.6×
```

## Memory 验证

```bash
# 用 memory-staleness-detection skill 验证
python ~/.hermes/skills/hermes/memory-staleness-detection/scripts/check.py
# 期望: 11-13 项检查, 0 🔴
```

## 下次 review 触发

- 升级 Hermes 0.16+ 时
- Swarm v1→v2 迁移完成时 (替换 profiles)
- L3 memory tool 清理时
- 飞书 pipeline 修复时
- 用户说"重审"时

## 关联文档

- [[concepts/hindsight-agent-brief-export-2026]] — 5 文档导出
- `memory-maintenance` skill — 修过时内容
- `memory-staleness-detection` skill — 标过时内容
- `~/AppData/Local/hermes/memories/MEMORY.md` (源文件, 不可改)
- `~/AppData/Local/hermes/memories/USER.md` (源文件, 不可改)
- `~/hermes-all/exports/hindsight-agent-brief/` (5 文档导出)
