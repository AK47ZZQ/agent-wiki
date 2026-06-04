---
title: Hindsight 主动化方法论（Hindsight-First Memory Pattern）
created: 2026-06-02
updated: 2026-06-02
type: method
tags: [method, workflow, hindsight, memory, pattern, automation]
sources:
  - https://hindsight.vectorize.io/guides/2026/04/23/guide-short-term-vs-long-term-memory-for-ai-agents
  - https://hindsight.vectorize.io/
  - local: ~/hermes-all/hermes/config.yaml
confidence: high
---

# Hindsight 主动化方法论

> 从"Hindsight 已装但被动"到"Hindsight 主动驱动 Agent"的可执行方法论。

## 核心思想

光把 `memory.provider: hindsight` 写进 config.yaml 不够。Hindsight 是**知识库**（L2），它和数据库一样需要**写入**和**读取**两条腿：

```
Hindsight 主动化 = 自动 retain (写入) + 自动 reflect (读取) + 角色分工 (边界)
```

## 与默认行为的差异

| 维度 | 默认（装上但不动） | 主动化 |
|---|---|---|
| Retain 触发 | 用户/Agent 手动调 | cron 批量 + turn 关键节点 |
| Recall 触发 | 用户/Agent 手动调 | session 开场自动 reflect |
| 边界划分 | LCM 和 Hindsight 重叠 | L1=LCM, L2=Hindsight（明确分工） |
| 上下文控制 | 单一路径（LCM） | 4-Tier 分层（见 [[concepts/agent-4-tier-memory-architecture]]） |

## 步骤

### Step 1: 明确分工（边界）

```
L0 Working  = 原生 messages
L1 Short    = LCM (lcm.db, 只写不读主动)
L2 Long     = Hindsight (pg0, 主动 retain + reflect)
L3 Hard     = memory tool (1375 字符)
```

**LCM 不退出，但角色从"主动压缩"改为"被动日志"**——通过 `lcm_doctor` 仍可查，但不挤占 prompt 空间。

### Step 2: 主动 retain（写入）

**实现**：每日 cron 任务，把当天 LCM 新写入的 session 摘要批量 retain 到 Hindsight。

```bash
# scripts/hindsight-nightly-retain.py (伪代码)
for session in lcm_sessions_modified_today():
    summary = lcm_extract_session_summary(session.id)
    # 提取"事实/偏好/教训"三类，丢弃对话流水
    facts = extract_actionable_facts(summary)
    for fact in facts:
        hindsight_retain(bank_id="hermes", content=fact)
```

**触发时机**：
- ⏰ 每日 23:00 批量（覆盖当天所有 session）
- 🔥 单 session 结束实时触发（可选，token 成本高）

### Step 3: 主动 reflect（读取）

**实现**：session 开头自动 reflect。

```python
# session_start_hook.py (伪代码)
context = hindsight_reflect(
    bank_id="hermes",
    query="用户当前关注什么？最近做了什么？有什么持续项目？",
    budget="low"  # 节省 token
)
inject_into_system_prompt(context)
```

**频率控制**：
- 每次新 session 开头调 1 次
- 不要每个 turn 都调（浪费 token）
- 配合 `lcm_status` 监控——如果 context 超过 30%，**主动** reflect 一次拉相关历史

### Step 4: 上下文控制看门狗

由于 LCM 退出"主动压缩"，需要 Agent **自己监控 context**：

```python
# 每次 turn 结束检查
ctx_pct = lcm_status.context_pct
if ctx_pct > 0.5:
    # 主动触发 retain
    hindsight_retain(bank_id="hermes", content=turn_summary)
    # 通知用户
    notify("上下文到 50%，已存档关键结论")
```

**关键**：**不是 cron 监控**，是 Agent 在 turn 内自检。这样零额外 token 成本。

### Step 5: 验证（必须）

- [ ] `hindsight_recall("用户的工作流偏好")` 命中保留的事实
- [ ] `hindsight_reflect("...")` 答案与 LCM session 摘要一致
- [ ] 新 session 开头自动获得历史上下文（不需手动 prompt）
- [ ] context % 超过 50% 时不爆（看门狗介入）

## 关键决策点

### 决策 1: 主 profile vs Worker profile

| Profile | context.engine | memory.provider | 理由 |
|---|---|---|---|
| **main (DM)** | `lcm` | `hindsight` | 完整双引擎（你目前的设置） |
| **minimax-worker1-7** | `lcm` | `hindsight` | 保持（长任务压缩需要） |
| **cron (no_agent)** | 不用 | 不用 | 短脚本不需要 |

**建议**：**主 profile 和 worker 全部保持现状**（已经是最优）。**不删 LCM，不退 context.engine**。

### 决策 2: Hindsight retain 频率

| 策略 | Token 成本 | 召回质量 |
|---|---|---|
| 每 turn 都 retain | 极高 | 最全（噪音也多） |
| 每日 23:00 批量 | 低 | 中（依赖摘要质量） |
| Session 结束实时 | 中 | 高 |
| **混合：每日批量 + 关键决策点** | 低 | 高（推荐） |

### 决策 3: Hindsight 数据清理

- **过期判定**：30 天未 recall 的事实降权
- **删除策略**：人工 review 或置信度 < 0.3 自动归档
- **避免**：自动删除用户偏好（一旦失忆代价高）

## 陷阱

1. **不要 retain 整段对话**——只 retain"事实/偏好/教训"。流水账浪费 token。
2. **不要在 LCM 仍主动压缩时又加 Hindsight 主动 retain**——双倍消耗没双倍价值
3. **不要让 Hindsight reflect 答案替代 L0 工作记忆**——它是知识库，不是上下文
4. **不要每个 turn 都 reflect**——只在 session 开场 + context 压力大时

## 与已有方法的关系

- [[concepts/hermes-workflow]] — Hermes 主工作流（包含 LCM 大量使用技巧）
- `install-hindsight-as-hermes-memory` skill — Hindsight 安装流程（前置）
- [[concepts/hermes-kanban]] — Kanban workers 同样适用此方法论
- [[concepts/agent-4-tier-memory-architecture]] — 本方法论的理论基础

## 验证清单

- [ ] 主 profile config 保持 `context.engine: lcm` + `memory.provider: hindsight`
- [ ] LCM 工具（lcm_grep/lcm_status）仍可用作"翻旧对话"
- [ ] Hindsight retain 有 cron 任务或 session 结束钩子
- [ ] Hindsight reflect 在新 session 开头自动调用
- [ ] 上下文超过 50% 时有自动看门狗
- [ ] 数据清理策略明确（避免无限增长）
