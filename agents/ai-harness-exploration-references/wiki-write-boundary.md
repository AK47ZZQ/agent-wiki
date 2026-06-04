---
title: Wiki Write Boundary — 何时写/不写 wiki
created: 2026-06-04
updated: 2026-06-04
type: reference
tags: [wiki, boundary, lcm, user-correction, restrained-write]
source: user-feedback-2026-06-04
confidence: high
---

# Wiki Write Boundary — 何时写/不写 wiki

> **用户原话**(2026-06-14): "检查 lcm 压缩归档,**不要随意写进 wiki 中**"
> **本节目的**:明确 wiki 写入的边界,防止 LCM 摘要扩散 + 自我合理化扩张。

## 1. 三层写入模型(LCM / Scratchpad / Wiki)

| 层 | 位置 | 用途 | 寿命 | 谁决定 |
|---|---|---|---|---|
| **LCM 摘要** | `hermes/lcm.db` (SQLite) | 对话压缩归档 | 长(永久) | LCM 引擎自动 |
| **Scratchpad** | `wiki/scratchpad/<task-id>/` | 任务中间产物 | ephemeral/short/long | orchestrator + worker |
| **Wiki** | `wiki/{concepts,methods,entities,...}/` | 知识沉淀 | 永久 | Distill 决策 + 用户显式 |

**关键边界**:
- LCM 不知道 wiki 存在(架构上解耦,**源码 grep 验证 0 匹配**)
- LCM 摘要查到即可,**不**自动展开成 wiki 页
- Scratchpad 是 wiki 的"工作区",**不**等于 wiki 主结构
- Wiki 是**精炼**层,不是"全部对话历史"层

## 2. 何时写 wiki — 决策树

```
新内容出现
  │
  ├─ 是 LCM 摘要节点?
  │   └─ ❌ 不写。lcm_expand 看一眼即可,不扩张
  │
  ├─ 是任务中间产物(scratchpad 文件)?
  │   └─ ❌ 不写主 wiki。归档到 scratchpad/_archive/
  │
  ├─ 是用户显式要的产物?
  │   └─ ✅ 写。trust user intent
  │
  ├─ 是 1-2 个新概念/方法/实体?
  │   └─ ✅ 写 wiki/ 单一文件(精炼)
  │
  └─ 是 5+ 个 Distill 产物(元方法论探勘)?
      ├─ 用户问"如何 X 更好" — ✅ 写,但 1-3 个核心页
      └─ 用户问"X 是什么" — 仅 scratchpad 1 个 result 文件
```

## 3. 反模式(从 2026-06-04 会话提炼)

### 反模式 A:LCM 摘要扩张到 wiki

**症状**:
```python
# 危险模式
lcm_expand(node_id=96)  # 看到摘要
# 然后立即:
write_file("wiki/concepts/摘要要点-X.md")  # 错
```

**正确做法**:
```python
lcm_expand(node_id=96)
# 看完即可,关掉
# 不写任何文件
```

**为什么禁止**:
- LCM 摘要是**压缩过的对话**,不是用户要保存的"知识"
- 写出来 = 变相保存原始 session(违反 LCM 的压缩意图)
- 真正"值得保留的知识"在原始 wiki 节点(已存在)或 LCM 摘要在数据库里
- 用户原话:"不要随意写进 wiki 中" — 包含此类

### 反模式 B:元方法论探勘"自加"5+ 边界文件

**症状**:
```
用户问:"如何创建更好的 wiki 库"
Agent 写:
  - methods/wiki-as-second-brain.md    (✓ 用户隐式支持)
  - methods/wiki-code-workflow.md      (✓ 配套工作流)
  - protocols/goal-alignment.md        (❓ 自加,从 MyYearInData 提炼)
  - protocols/multi-agent-detail.md    (❓ 自加,拆 CLAUDE.md 第 5 层)
  - protocols/per-project-claude-md-template.md  (❓ 自加,Meta 60K 模板)
  - protocols/agent-coordination.md 改 A2A 段   (❓ 自加,业界共识)
```

**问题**:
- 5 个 ❓ 文件都是 Agent "自我合理化" 加的
- 用户的实际意图可能是"写 1-2 个核心页就够"
- Agent 没问清单,直接 5 个都写

**正确做法**:
```
1. 列出候选产物清单(3-5 个,带"为什么需要")
2. 让用户选 1-3 个最优先
3. 写完后,标"未选"的进 scratchpad/_drafts/ 暂存
4. 用户没选的不要写 wiki
```

### 反模式 C:"Distill 产物" ≠ "5 个方法论页"

**Distill 阶段(CODE 4 阶段)的正确做法**:
- 1 个核心 method 页(用户主要问的)
- 1-2 个配套 protocol 页(直接必要)
- 其余进 scratchpad/_drafts/(DRAFT 标记)
- 真正"范式级"才进 wiki methods/

## 4. 4 个写 wiki 前的诚实自检

每次准备写 wiki 文件,先问:

```
□ 1. 用户显式要这个文件吗?
      → 是 → 写
      → 否 → 进入 □ 2

□ 2. 这个文件是 Distill 产物吗(提炼,不是搬运)?
      → 是 → 进入 □ 3
      → 否 → scratchpad

□ 3. 之前 wiki 没有这个内容吗?
      → 没有 → 写
      → 已有(90% 重叠)→ 追加到已有页,不新建

□ 4. 写完后 index.md + log.md 同步了吗?
      → 是 → 完成
      → 否 → 补
```

**任一不通过,不写 wiki。**

## 5. 累积漂移规则(NEW 2026-06-04 v6.16.0 — 用户纠正 #4)

> **第 4 个用户纠正**:多次任务累积扩张写入 = 缺少中途自检。
> **背景**:用户 2026-06-04 在 1 个会话内连发 3 个相关任务,Agent 在前 2 个任务中各自加了多个文件,直到第 3 个任务用户才说"不要随意写进 wiki"。

**核心原则**:**用户没反对 ≠ 用户同意**。沉默不等于同意。

**累积漂移指数**:
```
会话开始时 = 0
每次自加 wiki 文件(用户没明示)= +1
每次自加但用户提醒过 = +3
指数 ≥ 3 → 立即停止所有自加,只写用户显式要的文件
指数 ≥ 5 → 进入"全申请模式"(每个文件前都列清单,等用户确认)
```

**新任务开始时的 5 秒自检**(尤其和前次任务有重叠时):
```
□ 上次我写了什么? grep 自己 1.5 小时内的写入记录
□ 哪些是用户显式要? 哪些是"我自加"?
□ 上次用户有任何提醒/批评吗?
□ 如果上次有自加文件 → 这次更克制,先问清单
□ 自加倾向指数 ≥ 3 → 立即停下申请,不写
```

**第 1 次自加 OK,第 2 次自加要申请,第 3 次自加完全停止**。

**反例(本次会话)**:
- 任务 1:"如何创建更好的 wiki 库" → 6 个写入(2 显式 + 4 边界)
- 任务 2:"跑 1 个真多 Agent 任务" → 10 个写入(用户显式 E2E)
- 任务 3:"检查 lcm 压缩归档" → **用户明确说"不要随意写进 wiki"** ← 应该在前 2 个任务就识别

**正确做法**:任务 1 完成后 grep 自己,看到 4 边界文件 → 任务 2 收紧,只写 E2E 必要的,不重复"自加"模式。

## 6. LCM 隐性风险(2026-06-04 会话检查发现)

| 风险 | 实际状态 | 应对 |
|---|---|---|
| LCM 自动写 wiki | ✅ 不可能(源码 grep 0 匹配) | 无需处理 |
| Agent 读 lcm_expand 后"顺手"写 wiki | ⚠️ 隐性,本次会话未触发 | 本节就是约束 |
| 多次压缩后 LCM 摘要被误当知识 | 🟡 取决于 Agent 判断 | 决策树第 1 项("是 LCM 摘要? → 不写") |
| 跨 session 复用 LCM 摘要 | 🟡 正常用途,但不要转 wiki | 用 lcm_expand_query,不要 write_file |

## 7. 关联

- [[CLAUDE]] — root 协议
- [[protocols/multi-agent-detail]] — § 5.7 frontmatter schema
- [[protocols/agent-coordination]] — 6 原语(announce/claim/update/hand-off/archive)
- [[protocols/goal-alignment]] — 主动告警(类似精神:不要沉默,要克制)
- [[methods/wiki-as-second-brain]] — wiki 元方法论
- [[methods/wiki-code-workflow]] — CODE 4 阶段

## 8. 版本历史

- v1.0 (2026-06-04) — 初始版本,从用户"不要随意写进 wiki"纠正提炼
- v1.1 (2026-06-04) — 加 § 5 累积漂移规则(用户纠正 #4),"用户没反对 ≠ 用户同意"核心原则
