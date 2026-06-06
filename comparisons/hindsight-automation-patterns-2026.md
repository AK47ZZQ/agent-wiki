---
title: Hindsight 自动化方案对比 (2026-06-03)
created: 2026-06-03
updated: 2026-06-03
type: comparison
tags: [hindsight, automation, trigger, cron, anti-deadlock, design-pattern]
sources:
  - https://www.cnblogs.com/qiniushanghai/p/20012754
  - https://cloud.tencent.com/developer/article/2655385
  - https://github.com/dorianlgs/langgraph-mem0
  - local: ~/hermes-all/hermes/skills/autonomous-ai-agents/ai-harness-exploration/references/hindsight-install-uninstall-case-study.md
confidence: high
source: hindsight-3rd-notebook-2026-06
---

# Hindsight 自动化方案对比 (2026-06-03)

> 探索"无 cron 自动化"——既不让 Agent 烧 token 无边界, 也不让用户手动每个 turn retain

## 4 种自动化模式（业界全景）

| 模式 | 实现 | 例子 | 风险 |
|---|---|---|---|
| **Schedule** (cron) | 定时器触发 | Linux cron, Windows Task Scheduler | 烧 token 无边界, 你之前否决过 |
| **Trigger** (event) | 事件 hook (turn-end, session-end) | LangGraph hooks, OpenClaw, Hermes Curator | 频率可控, 但需 framework 支持 |
| **Workflow 节点** (graph) | 在 workflow 中显式调用 | LangGraph + Mem0 graph node, Hermes skill 内部 | 需改 workflow 定义, 但 100% 显式 |
| **Agent 自评** (judge) | Agent 自己判断 "是否值得 retain" | 你现在的 handoff v1 | 0 自动, 但 Agent 认知偏差 |

## 3 个备选方案（针对你的工作流）

### 方案 A: 现状 (handoff v1 守护)

**机制**：Agent 显式调用 `hh.retain()`, 受 4 机制保护 (MAX=3/天, sha256 去重, 长度校验, 人工触发)

| 优点 | 缺点 |
|---|---|
| ✅ 0 自动, 0 烧 token | ❌ Agent 经常忘记 retain |
| ✅ 用户完全控制 | ❌ 关键事实漏 retain |
| ✅ 已部署 (MAX=3) | ❌ 单次 token 成本高 |

**Token 成本**: ~10k tokens/天 (3 retain × 3.3k)

### 方案 B: Hermes Curator 模式 (内置自学习)

**机制**：**Hermes 已经内置 "Curator 后台自学习器"**（参考: 6 层架构包括 "Curator 后台自学习器"）—— 自动将执行经验提炼为 skill

| 优点 | 缺点 |
|---|---|
| ✅ 已内置, 不需额外开发 | ❌ 烧 token 风险 |
| ✅ "自动" 但有 Hermes 自己的限制 | ❌ 你不知道它会 retain 什么 |
| ✅ 业界主流 (OpenClaw 同款) | ❌ 不可控 |

**Token 成本**: 未知（取决于 Hermes Curator 内部频率）

**关键问题**：**Hermes Curator 是 framework 内置，不是 Hindsight 集成**——它 retain 到 skill，不是 Hindsight bank

### 方案 C: 触发式 + Agent 自评 (推荐)

**机制**：**不是每 turn 都判断**，而是**特定 trigger**触发 Agent 自评：
- **Trigger 1**: Session 开场（已发生 1 次）— 拉历史但**不**retain
- **Trigger 2**: Session 结束（用户停 ≥ 30 min）— Agent 自评是否 retain
- **Trigger 3**: 关键决策点（用户做架构决策/踩坑）— Agent 立即判断

| 优点 | 缺点 |
|---|---|
| ✅ 0 定时器, 0 cron | ⚠️ 需识别"用户停 30 min"事件 |
| ✅ Trigger 数 ≤ 3 (不是每 turn) | ⚠️ Agent 自评仍可能误判 |
| ✅ Token 成本可控 (≤ handoff MAX) | ⚠️ 实现复杂 |
| ✅ 不重蹈"主动化失控"覆辙 | |

**Token 成本**: ≤ 10k tokens/天 (受 handoff MAX=3 限制)

## 死循环风险评估

| 方案 | 死循环风险 | 评估 |
|---|---|---|
| **A 现状** | 0 | ✅ Agent 显式, 不会循环 |
| **B Curator 内置** | 中 | ⚠️ Hermes 内置, 你控制不了 |
| **C Trigger+自评** | 低 | ✅ 限频 3/天, sha256 去重 |

## 推荐决策矩阵

| 你的偏好 | 推荐 |
|---|---|
| **零风险** | A (现状) |
| **适度自动化** | **C (Trigger+自评)** ⭐ |
| **深度自动化** | B (Curator) — 但烧 token 风险高 |
| **完全自动化** | B + 每周 1 次 manual review |

## 我的真实建议

**推荐方案 C**（Trigger + Agent 自评）—— 满足：
- "**0 定时器, 0 cron**" 你的根本诉求
- "**主动 retain 关键事实**" 你的工作流需求
- "**严防死循环**" 你的安全要求
- "**限频 3/天**" 你的 token 控制

**3 个 Trigger 都可以在 Hermes 内实现**（不靠 cron）：
- **Trigger 1** (session-end): Hermes 的 session-finalize hook
- **Trigger 2** (用户停顿): 不易检测，**放弃**
- **Trigger 3** (关键决策): Agent 自己判断

**实际建议：只做 Trigger 3 (Agent 关键决策点自评)**，最简单、最安全、最不重蹈覆辙。

## 与 handoff v1 关系

| handoff v1 (现状) | Trigger+自评 (新) |
|---|---|
| Agent **显式**调用 `hh.retain()` | Agent **判断后**调 `hh.retain()` |
| 0 触发器 | 多触发器 (session-end, 关键决策) |
| 0 自动化 | 触发式自动化 (trigger-based) |
| 简单 (直接调) | 复杂 (先判断后调) |

**核心不变**：保留 `hh.retain()` 的 4 机制 (MAX/去重/长度/人工)，**只是触发方式从"显式"变"trigger-based"**。

## 关键陷阱

1. ❌ **不要做"每 turn 自评"** — 1 session 50 turn = 50 次判断 = 烧 token
2. ❌ **不要"session-end 自动 retain 全部"** — 100 turn = 100 retain = 300k tokens
3. ✅ **只对"用户主动决策"trigger** — 用户说"我决定..."时 Agent 才判断
4. ✅ **保留 handoff v1 限频** — 即使 trigger 多, daily MAX=3 不变
5. ⚠️ **Trigger 检测要可靠** — "用户停顿 30 min" 不易检测, 可能漏

## 关联文档

- `hindsight-handoff` skill — 当前 handoff v1
- [[concepts/hindsight-in-hermes-ecosystem-2026]]
- (原始记录已精简移除,合并到 [[concepts/hindsight-in-hermes-ecosystem-2026]])
- [[notes/hindsight-risks-and-optimizations-2026]]
- `hindsight-handoff` skill
- `hindsight-watchdog` skill
