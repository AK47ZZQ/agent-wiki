---
title: Agent Registry — 多 Agent 注册表
created: 2026-06-04
updated: 2026-06-04
type: meta
tags: [agent, registry, multi-agent, second-brain]
source: local
confidence: high
---

# Agent Registry — 多 Agent 注册表

> 这是多 Agent 协作的"花名册"。每个活跃 Agent 必须在这里注册一页,声明自己的**身份 / 能力 / 接口 / 状态**。

## 架构定位

第二大脑的"脑区"由 3 类节点组成:

| 节点类型 | 物理位置 | 用途 |
|---|---|---|
| **Agent registry** | `wiki/agents/` | 谁存在、能做什么、怎么调用 |
| **共享 scratchpad** | `wiki/scratchpad/` | 短期共享工作记忆(读后即焚) |
| **任务板** | `wiki/tasks/` | 长生命周期任务(跨 session) |

## 协议

所有 Agent 在写入任何 wiki 页面前必须:

1. **先注册** — 在本目录建一个 `<agent-id>.md`,声明 5 件事:
   - **id** — 唯一短名(全小写连字符)
   - **owner** — 谁部署/拥有(人/系统/无主)
   - **capabilities** — 能做什么(动词列表)
   - **interfaces** — 怎么调用(MCP/CLI/REST)
   - **status** — active / paused / deprecated
2. **写任务** — 在 `wiki/tasks/` 建 `<task-id>.md`,声明依赖的 Agent
3. **共享状态** — 短期信息(临时变量/中间结果)写到 `wiki/scratchpad/`,附 TTL
4. **长期沉淀** — 完成后把"值得记的"提炼到 `concepts/` 或 `methods/`

## 当前已注册 Agent

<!-- 启动后由各 Agent 自己添加 -->

- [[agents/main-claude]] — 主对话 Agent(用户直接交互)
- [[agents/hermes-self-check]] — 自检 + 健康审计
- [[agents/hermes-kanban-orchestrator]] — 多任务编排
- [[agents/hermes-kanban-worker]] — 单任务执行(模板,实例化后才有 id)

## 注册模板

```yaml
---
id: <agent-id>
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: <user|system|none>
status: active|paused|deprecated
capabilities: [read-file, write-file, web-search, code-exec, ...]
interfaces: [mcp:tool, cli:cmd, rest:POST /path]
tags: [agent, role]
---

# <agent-id>

## 角色
(一句话说清:这个 Agent 负责什么)

## 能力清单
- 读:能读什么(限制:不能读 hermes/.env 等敏感)
- 写:能写什么(限制:只能写特定目录)
- 调用:能调什么(限制:no terminal 后台 no 网络上传)

## 接口
- MCP tool: ...
- CLI: ...
- REST: ...

## 当前状态
- last_active: ...
- in_flight: ...
- pending: ...

## 历史
- (短日志,超 20 行归档)
```

## 关联

- 协作协议:[[protocols/agent-coordination]]
- 共享空间:[[scratchpad/README]]
- 任务板:[[tasks/README]]
- 写入规则:[[CLAUDE]]
