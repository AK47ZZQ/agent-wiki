---
title: Goal Alignment Protocol — Agent 主动告警机制
created: 2026-06-04
updated: 2026-06-04
type: protocol
tags: [protocol, goal-alignment, proactive-warning, agent-behavior]
source: myyearindata.com
confidence: high
---

# Goal Alignment Protocol — Agent 主动告警机制

> **问题**:传统 wiki/Agent 是被动响应 — 用户问才答,从不主动说"你 off track"。
> **业界教训**(MyYearInData 4 周案例):
> - Week 1: Agent 告诉用户 off track
> - Week 2: 用户忽略("busy")
> - Week 3: Agent 报告零进展
> - Week 4: 用户调整
> - **系统有效 = 用户听信号;忽略信号 = 系统变成噪音**
> **协议目标**:让 Agent 在以下时机主动警告,**不只响应请求**。

## 1. 触发场景(何时主动警告)

Agent 必须在以下时机主动写一条"警告"消息,即使用户没问:

| 场景 | 信号来源 | 警告级别 | 行动 |
|---|---|---|---|
| **Task 停滞** | `tasks/<id>.md` `updated` > 24h 无变化 | 🟡 | 写到 `scratchpad/<task>/warning-01.md`,在 Feishu 提及 owner |
| **目标偏离** | 当前操作与 task goal 不一致 | 🟡 | 立即在对话中提:"⚠️ 这步离目标 X 远了,理由是 Y" |
| **关键假设失效** | 依赖的 fact/file/process 不存在 | 🔴 | 立即停 + 写 scratchpad + 通知 |
| **冲突出现** | 同一资源 2 个 Agent 竞争 | 🔴 | 写 conflict 报告到 scratchpad |
| **范围蔓延** | 用户说"顺便也加 X"导致 task 范围扩大 | 🟡 | 提醒"这是新 scope,加到 task 还是开新 task?" |
| **重复模式** | 用户第 2 次提相同需求 | 🟡 | "上次 Y 也提过,要不要搜相关 task 页?" |
| **资源耗尽预警** | DB/tokens/disk > 80% | 🔴 | 写到 `agents/<id>.md` 状态字段 + 通知 |
| **机会提示** | 发现用户可能需要的相关页面 | 🟢 | 在对话末尾"相关:[[X]]" |

## 2. 三原则(Meta 规则)

```
原则 1: 主动 ≠ 打扰
  主动警告 = 高信噪比(对用户真有用)
  不是 = 每 5 分钟 ping 一次

原则 2: 警告必带建议
  不只说"有问题",必带"建议怎么修"
  例:❌ "你 off track"
     ✅ "你 off track。建议:把 task X 拆成 X1+X2"

原则 3: 沉默不是金
  看到红旗语言(红旗词:"业界共识""必需""最佳实践")
  → 立即停推销,切到诚实评估
  → 不要等用户问"为什么要 X"
```

## 3. 协议层(如何记录警告)

### 警告文件:`scratchpad/<task-id>/warning-<NN>.md`

```yaml
---
owner: <agent-id>           # 谁发的警告
created: ISO8601            # 警告时间
severity: critical|warn|info  # 严重度
topic: ...                  # 一句话
readers: [<agent-id>, ...]  # 谁必读
level: ephemeral|short|long # 必填
task_id: <task-id>          # 关联 task
---
# Warning: <topic>

## 信号
<触发的具体数据,不是主观判断>

## 影响
<不处理会怎样>

## 建议
<具体修复方案,必带 action items>

## 备选
<如果用户拒绝建议,还有什么选项>
```

### 警告 vs 请求 vs 进度

| 类型 | 文件前缀 | 谁写 | 谁读 | TTL |
|---|---|---|---|---|
| **警告** | `warning-NN.md` | 任何 agent(看到问题) | task owner + 涉及 agent | short |
| **请求** | `request-NN.md` | orchestrator/worker | 被 @ 的 agent | ephemeral |
| **进度** | `result-NN.md` | 任务执行者 | orchestrator | short |
| **最终** | `final.md` | task owner | 所有人 | long |

## 4. 何时该主动提 vs 不提

### ✅ 该提(高信噪比)

- 你**具体知道**问题在哪(不是"感觉不对")
- 你**有建议**(不是"要不要看看?")
- **影响用户决策**的问题(task 方向 / 资源 / 关键假设)
- 用户的**已有偏好**违反(用户说过"我不喜欢 X" → 你看到 X)

### ❌ 不该提(噪音)

- "要不要我顺便做 X?"(没意义)
- 每次都问"你确定吗?"(烦)
- 工具调用失败但能 fallback(不打扰)
- 自己在内部决策(self-manage)
- 看到 wiki 里有 5 个 dead link(除非任务相关)

## 5. 失败兜底

- Agent 主动警告被用户忽略 2 次 → Agent 把警告降级为"建议"(从 🟡 → 🟢),不再主动
- 警告有 30%+ 被忽略 → 协议本身有 bug,要 re-evaluate
- Agent 看到问题不报 → 写进 `agents/<id>.md` 错误账本,作为下次 review 的依据

## 6. 关联

- [[CLAUDE]] — root 协议
- [[protocols/multi-agent-detail]] — 5 层详细
- [[protocols/agent-coordination]] — 6 通信原语
- [[methods/wiki-as-second-brain]] — 元方法论

## 7. 实战案例(2026-06-04)

### Case 1: 用户问"自检",Agent 主动警告
- **触发**: 发现 hermes/state.db-wal 220 MB(stuck writer)
- **Agent 反应**: 不只报告,主动警告"这是 P0 阻塞,建议先 checkpoint 再继续"
- **用户**: "执行 P0-P3" → 接受了警告
- **教训**: Agent 主动警告 = 用户决策速度 +1 步

### Case 2: 用户说"基于已有 X 写 Y",Agent 套了"内部合成"模板
- **触发**: 用户问题有外部参照需求(业界 2026 共识)
- **Agent 错误**: 跳过 web 搜索,纯文件系统操作
- **用户反应**: "为什么没有 web 搜索"
- **教训**: 触发信号是 OR,不是 IF-THEN。多个信号匹配应综合判断,不能因为"产物已存在"就跳
- **协议改进**: 在本协议加"看到外部参照需求 + 产物已存在 → 必须双重验证(web 搜索 + 文件系统)"

### Case 3: 用户说"装 3 仓库"
- **触发**: 红旗模式(单次推销 ≥ 2 个新工具)
- **Agent 反应**: 立即停推销,对每个都做 6 问(Step 0c 必要性门控)
- **结果**: 11 个红旗信号 + 6 问全"否" = 拒绝安装
- **教训**: **主动警告的极简形式 = 一句"这是红旗模式"**
