---
title: Agent 治理框架 — 多 Agent 协作的硬规则 + 软规则分层
created: 2026-06-06
updated: 2026-06-06
type: concept
tags: [agent, governance, multi-agent, framework, hermes]
source: multi-agent-design-2026
---

# Agent 治理框架 — 多 Agent 协作的硬规则 + 软规则分层

> 概念补完 (2026-06-06, 从 reflection 笔记引用反推).
> 前置: [[protocols/agent-coordination]] (3 硬规则源头) + [[protocols/multi-agent-detail]] (5 协议展开)

## TL;DR

- **3 硬规则** (违反就报错):
  1. wiki 写入必走 safe-commit-push.sh v1.6
  2. 冲突不擅自修, 报 main-claude
  3. 绝不 force-push
- **5 软规则** (违反 warn):
  1. 写新 wiki 内容必申请 (ai-harness-exploration § 4.0)
  2. 维护豁免: 死链/索引/frontmatter 修复不需申请
  3. 9 字段 frontmatter 必填
  4. 至少 2 wikilink 出链
  5. log.md 每操作必记
- **3 通信原语**: Git remote + scratchpad/ + LCM 摘要 + send_message (4 频道)
- **Hermes 实战**: AGENTS.md v2 (8K, 含 5 步核验 + 仓库清单)

## 1. 硬规则 vs 软规则

| 类型 | 违反后果 | 例子 |
|---|---|---|
| **硬规则** | 中断, 不让继续 | force-push, 裸 git, 改 raw/ |
| **软规则** | warn, 但不阻塞 | 1 wikilink, 6 字段 (允许缺 confidence) |

## 2. 决策树

```
用户指令
├─ 涉及 wiki 写入?
│  ├─ 新内容 (从未写过) → 必申请 (软规则)
│  ├─ 维护 (死链/索引/frontmatter) → 豁免
│  └─ 边界 (scratchpad 工作区) → 豁免
├─ git 操作?
│  ├─ 走 safe-commit-push.sh (硬)
│  ├─ 冲突 → 报 main-claude (硬)
│  └─ 绝不 force-push (硬)
└─ 涉及其他 agent?
   ├─ send_message 协调
   └─ scratchpad/ 共享
```

## 3. 跟 L1/L2/L3 关系

- **L1 MEMORY.md** = Agent 铁律 (硬规则 cross-session 持久化)
- **L2 Hindsight** = Agent 反思 (软规则上下文)
- **L3 wiki** = 公共知识库 (硬规则 5 步核验, 软规则 frontmatter)
- **L4 LCM** = session 实时上下文

## 4. 关联文档

- [[protocols/agent-coordination]] — 3 硬规则源头
- [[protocols/git-collaboration-multi-agent]] — git 协作 3 步
- [[protocols/multi-agent-detail]] — 5 协议展开
- [[concepts/harness-engineering]] — 方法论
- [[AGENTS]] — Hermes Agent 工作环境与协作规约 v2 (8K)
- [[concepts/agent-4-tier-memory-architecture]] — 4 层记忆设计

## 5. 自检

- [x] 6 字段齐
- [x] 至少 2 wikilink 出链 (实际 6+)
- [x] tag: agent + governance + multi-agent + framework + hermes
- [x] source: multi-agent-design-2026
