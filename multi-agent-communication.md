---
title: Multi-Agent Communication — 通信协议
created: 2026-06-04
updated: 2026-06-04
type: protocol
tags: [wiki, multi-agent, communication, protocol, scratchpad, lcm]
sources: [protocols/multi-agent-detail, methods/using-knowledge-base]
---

# Multi-Agent Communication Protocol

> 多 Agent 之间的 4 通信频道 + 5 消息类型 + 7 状态机 + 3 失败模式 + 5 度量。

## TL;DR

- **4 频道** = git remote / scratchpad/ / LCM 摘要 / send_message
- **5 消息类型** = announce / request / claim / update / hand-off
- **7 状态** = pending → claimed → in_progress → review → done → archived / failed

## 4 频道对比

| 频道 | 介质 | 何时用 | 延迟 |
|---|---|---|---|
| **git remote** | GitHub wiki | 长效内容(wiki) | 异步,分钟级 |
| **scratchpad/** | 本地文件 | 短期协调(任务上下文) | 实时(同 repo) |
| **LCM 摘要** | L1 内存 | 跨 session 上下文 | session 级 |
| **send_message** | 飞书/IM | 用户通知 | 实时(网络) |

## 5 消息类型

| 类型 | 用途 | 例子 |
|---|---|---|
| **announce** | 任务发布 | "我开了一个 2026-06-04 任务" |
| **request** | 资源请求 | "我需要 hermes-3rd 帮 review" |
| **claim** | 任务认领 | "我 claim 这个 ticket" |
| **update** | 进度更新 | "我做了 50%,遇到 X 问题" |
| **hand-off** | 任务交接 | "我做完了,给 reviewer" |

## 7 状态机

```
pending → claimed → in_progress → review → done → archived
                ↓                 ↓
              failed            failed
```

## 3 失败模式

1. **race condition** — 两个 agent 同时 claim → 取 first-push
2. **stale lock** — agent crash 没 release → 600s 超时
3. **context drift** — scratchpad 没及时更新 → 其他 agent 看到旧状态

## 5 度量

| 指标 | 计算 | 健康阈值 |
|---|---|---|
| **响应时间** | request → claim | ≤ 5 min |
| **任务完成率** | done / total | ≥ 80% |
| **冲突率** | 冲突 / 总 commit | ≤ 5% |
| **平均任务时长** | done - pending | ≤ 1h |
| **hand-off 失败** | 失败 hand-off / 总 | ≤ 10% |

## 关联

- [[protocols/multi-agent-detail]] — 详细
- [[protocols/git-collaboration-multi-agent]] — git 协议
- [[methods/scratchpad-coordination]] — scratchpad 教程
