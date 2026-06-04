---
title: 多 Agent 协作协议(详细)
created: 2026-06-04
updated: 2026-06-04
type: protocol
tags: [protocol, multi-agent, coordination, a2a-compatible]
source: claude-md-5.1-5.6
confidence: high
---

# 多 Agent 协作协议(详细)

> 这是 [[CLAUDE]] 第 5 层的展开版。Agent 启动只读 root (5-8K lean),按需 drill 到本文件。
> **A2A 兼容**:本协议命名/语义与 Google A2A 协议保持概念一致,但实现是文件 + frontmatter(无 RPC)。

## 5.1 节点类型

| 节点 | 位置 | 用途 | 寿命 |
|---|---|---|---|
| **Agent registry** | `wiki/agents/` | 谁存在、能做什么、怎么调用 | 长 |
| **Scratchpad** | `wiki/scratchpad/<task-id>/` | 短期共享中间状态(per-task namespace) | ephemeral→7d→永久 |
| **Task board** | `wiki/tasks/` | 跨 Agent 长生命周期任务 | 中 |
| **Protocol** | `wiki/protocols/` | 协作原语定义 | 长 |

## 5.2 通信原语(无 RPC)

```
announce:   agents/<id>.md              声明自己
request:    scratchpad/<task-id>/req-<n>.md    @ 其他 Agent
claim:      tasks/<id>.md frontmatter   认领任务
update:     tasks/<id>.md 追加日志      进度
hand-off:   frontmatter lock: <id>      独占写权(TTL=600s)
archive:    tasks/_archive/             任务结束
```

**A2A 映射**(参考 Google A2A 协议):
| 我的原语 | A2A 等价 | 说明 |
|---|---|---|
| announce | Agent Card | 身份 + 能力声明 |
| request | Message | 异步消息 |
| claim | Task Lifecycle | 任务状态机 |
| update | Task Status Update | 进度回报 |
| hand-off | Streaming/Streaming Subscription | 长任务流 |
| archive | Task Finalization | 终态 |

## 5.3 三条硬规则

1. **先注册,后行动** — 任何 Agent 在动笔前必须先在 `agents/<id>.md` 注册
2. **先 grep,后写** — 写任何文件前 grep 目录,看是否有锁/在途任务
3. **写完必索引** — 任何写入必须在 `index.md` 加条目(否则等同不存在)

## 5.4 自检清单(每次跨 Agent 协作前)

```
[ ] 我注册了吗? (agents/<id>.md 存在且 status=active)
[ ] 我读 scratchpad/index 了吗? (有 in-flight 任务吗)
[ ] 我读 tasks/index 了吗? (有未认领的相关任务吗)
[ ] 写新页前查重了吗? (避免重写)
[ ] 完成后我更新了 index 吗? (active 段还是空的就是失败)
```

## 5.5 失败兜底

- Agent 失联 > 1 小时:其 `last_active` 过期,其他 Agent 跳过依赖
- Lock 过期(>600s):任何 Agent 可 claim
- 文件损坏:从 `index.md` 重建

## 5.6 关联文档

- 协议详细:[[protocols/agent-coordination]]
- 注册表:[[agents/README]]
- Scratchpad:[[scratchpad/README]]
- 任务板:[[tasks/README]]
- 首次演示:[[tasks/wiki-multi-agent-refactor]]

## 5.7 Frontmatter Schema(2026-06-04 补充)

来自业界 consensus(OACP / fme.safe.com / MongoDB Memory Engineering),所有跨 Agent 消息必须 typed。

### Agent 页 schema(`agents/<id>.md`)

```yaml
---
id: <agent-id>              # 必填,小写连字符
created: YYYY-MM-DD         # 必填
updated: YYYY-MM-DD         # 必填
owner: user|system|none    # 必填
status: active|paused|deprecated|template  # 必填
capabilities: [...]         # 必填,动词列表
interfaces: [...]           # 必填,接口列表
last_active: ISO8601        # 选填(自动更新)
---
```

### Task 页 schema(`tasks/<id>.md`)

```yaml
---
id: <task-id>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: pending|claimed|in_progress|review|done|blocked  # 必填
owner: <agent-id>           # 必填
assignees: [...]            # 必填,空数组需 `[]` 显式
depends_on: [...]           # 必填,可空
priority: high|medium|low   # 必填
lock: <agent-id>            # 选填,独占写权
locked_at: ISO8601          # 选填,lock 配对
lock_ttl: 600               # 选填,默认 600s
---
```

### Scratchpad 页 schema(`scratchpad/<task-id>/<N>.md`)

```yaml
---
owner: <agent-id>           # 必填
ttl: ISO8601                # 必填,到期时间
topic: ...                  # 必填,一句话
readers: [...]              # 必填,谁能读
created: YYYY-MM-DD         # 必填
level: ephemeral|short|long # 必填
---
```

### Content 页 schema(`concepts|entities|methods|.../<name>.md`)

```yaml
---
title: ...                  # 必填
created: YYYY-MM-DD         # 必填
updated: YYYY-MM-DD         # 必填
type: entity|concept|method|comparison|note|meta|protocol|source  # 必填
tags: [...]                 # 必填,从 taxonomy
source: ...                 # 必填
confidence: high|medium|low # 必填
contested: true             # 选填
contradictions: [...]       # 选填
---
```

### Schema 验证规则

- 4 类必填字段缺一 = lint 失败
- `status` 必须在枚举值内
- `lock` 设置时必须同时有 `locked_at` 和 `lock_ttl`
- `ttl` 必须是未来时间(过去时间 = 已过期,应自动 archive)

## 5.8 Namespace 隔离(2026-06-04 补充)

来自 fme.safe.com + MongoDB Memory Engineering:

```
scratchpad/
├── ephemeral-{date}-{topic}.md  # 顶层:跨任务临时
└── {task-id}/                   # 每任务独立 namespace
    ├── req-01.md                # request
    ├── result-01.md             # result
    ├── intermediate-01.md       # 中间状态
    └── final.md                 # 最终输出
```

**好处**:
- 多任务并发不会覆盖彼此文件
- 任务结束 = 直接 rm -rf `<task-id>/`(自动 archive)
- 其他 Agent 通过读 `<task-id>/index.md` 知道这任务的所有状态文件

## 关联

- Root:[[CLAUDE]]
- 方法论:[[methods/wiki-as-second-brain]]
- 注册:[[agents/README]]
- 任务:[[tasks/README]]
- Scratchpad:[[scratchpad/README]]
