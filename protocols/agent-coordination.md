---
title: Agent Coordination Protocol — 协作协议(A2A 兼容)
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [protocol, multi-agent, coordination, consensus, a2a-compatible]
sources:
  - local
  - https://gurusup.com/blog/best-multi-agent-frameworks-2026
  - https://medium.com/online-inference/best-practices-for-building-effective-ai-agents-and-multi-agent-systems-2c7fe11c9605
confidence: high
---

# Agent Coordination Protocol — 协作协议(A2A 兼容)

> 多 Agent 如何"说话"。约束:不引入外部 runtime(只用 wiki + 已有工具)。
> **A2A 兼容**:本协议命名/语义与 Google A2A 协议(Agent-to-Agent)概念一致 — 6 原语映射 A2A 的核心消息类型(见 § 7)。
> Gartner 预测 2028 年 60% MAS 用标准协议,本协议是该趋势的文件 + frontmatter 实现。

## 通信原语

Agent 之间的所有"通信"都通过**写文件**完成,无 RPC、无消息队列。

### 1. announce (声明)
Agent 创建/更新自己的 `agents/<id>.md` 声明状态。
- 触发:启动、暂停、恢复、关闭
- 读者:所有 Agent
- 文件:`agents/<id>.md`

### 2. request (请求)
Agent 在 `scratchpad/` 写一个 `request-<date>-<topic>.md`,声明需要什么。
- 触发:需要其他 Agent 帮忙
- 读者:被 @ 的 Agent(`readers` 字段)
- 写法:在 frontmatter 标 `readers: [<agent-id>]`

### 3. claim (认领)
Agent 在 `tasks/<id>.md` 修改 frontmatter,把自己加入 `assignees` 并把 `status` 改为 `claimed`。
- 触发:决定做某任务
- 读者:所有关注该 task 的 Agent

### 4. update (进度)
Agent 在 `tasks/<id>.md` 追加"进度日志"行 + 更新 `updated` 字段。
- 触发:完成任务一部分
- 读者:owner + assignees

### 5. hand-off (移交)
Agent 在目标页 frontmatter 标 `lock: <agent-id>`,锁期间独占写权。
- 触发:长任务防止冲突
- TTL:默认 600 秒(超时自动释放)

### 6. archive (归档)
Agent 把 task 移到 `tasks/_archive/`,更新 `tasks/README` 索引。
- 触发:status=done

## 防冲突

| 场景 | 防冲突方式 |
|---|---|
| 两个 Agent 同时写同一文件 | file lock + claim status |
| 两个 Agent 同时 claim 同一 task | first-write-wins(写入时间戳) |
| 一个 Agent 写时另一个要读 | 读永远允许(只读不冲突) |
| TTL 过期 | 自动释放(下次 update 检查) |

## 共识(多 Agent 决策)

不需要 explicit consensus 协议。**冲突处理**:
1. 后写覆盖前写(append-only 场景不允许)
2. 标 `contested: true` + `contradictions: [other-page]`
3. 触发 [[agents/main-claude]] 仲裁

## 失败兜底

- Agent 失联 > 1 小时:其 `last_active` 字段过期,其他 Agent 跳过依赖
- Lock 过期:任何 Agent 可 claim
- 文件损坏:从 `index.md` 重建

## 7. A2A 协议兼容映射(2026-06-04 补充)

> **目的**:为未来跨 framework 互操作预留映射层。如果以后要接入 Google A2A / LangGraph / AutoGen 框架,本协议可直接对接(不需重写)。
> **Gartner 预测**:2028 年 60% MAS 使用标准化通信协议。

### 6 原语 → A2A 消息类型映射

| 我的原语 | A2A 等价 | 触发场景 | 文件路径 |
|---|---|---|---|
| **announce** | Agent Card | Agent 启动/状态变更 | `agents/<id>.md` |
| **request** | Message (JSON-RPC 风格) | 跨 Agent 异步请求 | `scratchpad/<task-id>/req-<n>.md` |
| **claim** | Task Lifecycle Event | 任务认领 | `tasks/<id>.md` (frontmatter `status: claimed`) |
| **update** | Task Status Update | 进度回报 | `tasks/<id>.md` (追加进度日志) |
| **hand-off** | Streaming/Streaming Subscription | 长任务流/独占写权 | frontmatter `lock` + `lock_ttl` |
| **archive** | Task Finalization Event | 任务结束 | `tasks/_archive/<id>.md` |

### 命名一致性表

| A2A 标准名 | 我的命名 | 用途 |
|---|---|---|
| Agent Card | `agents/<id>.md` | Agent 身份 + 能力声明 |
| Task ID | `tasks/<id>` | 任务唯一标识 |
| Task State (pending/claimed/in_progress/completed/failed) | `status:` frontmatter | 任务生命周期 |
| Message Part (text/file/data) | scratchpad 文件 frontmatter | 消息载荷 |
| Artifact | `result-<n>.md` / `final.md` | 任务输出 |
| Streaming Update | progress 日志行 | 长任务进度 |

### 互操作示例(未来接入 A2A 客户端时)

```yaml
# A2A 客户端发来的 Message(假设 JSON-RPC)
{"jsonrpc": "2.0", "method": "tasks/send", "params": {
  "id": "wiki-update-001",
  "message": {
    "role": "user",
    "parts": [{"type": "text", "text": "更新 wiki 的 CLAUDE.md"}]
  }
}}

# 我的 Agent 接收后:
# 1. 在 tasks/wiki-update-001.md 创建任务
# 2. frontmatter status: pending → claimed
# 3. 执行 → status: in_progress
# 4. 写 result-01.md → status: done
# 5. 触发 A2A 任务完成回调

# 反向:本协议输出可被 A2A 客户端读取
# tasks/<id>.md + result-<n>.md → A2A Artifact
```

### 协议兼容性的 3 个不变量

1. **身份声明**(Agent Card)必填字段一致:`id` / `name` / `description` / `capabilities`
2. **任务状态机**一致:6 状态可映射到 A2A 的 4-5 状态
3. **消息载荷**用 markdown + frontmatter(JSON-like 键值),可双向解析

## 关联

- 注册:[[agents/README]]
- 共享空间:[[scratchpad/README]]
- 任务:[[tasks/README]]
- 写入规则:[[CLAUDE]]
- 详细协议:[[protocols/multi-agent-detail]]
- 元方法论:[[methods/wiki-as-second-brain]]
