---
id: 2026-06-04-agent-stack-test
created: 2026-06-04
updated: 2026-06-04
status: in_progress
owner: agents/main-claude
assignees:
  - agents/main-claude
  - agents/researcher-1
  - agents/writer-1
depends_on: []
priority: high
goal: 端到端测试整个多 Agent 第二大脑协议栈
tags: [test, e2e, multi-agent, protocol-validation]
---

# Task: 端到端测试多 Agent 第二大脑协议栈

> **这是真任务** — 不是 demo。实际产出要落到 wiki。

## Goal

测完整协议栈:registry → scratchpad → tasks → 6 原语 → frontmatter schema → A2A 兼容。

## Scope

**包含**:
- 3 Agent 注册(orchestrator + 2 worker)
- 1 个 task 全流程
- 测试 6 原语:announce / claim / update / hand-off / archive
- 验证 scratchpad namespace 隔离
- 验证 frontmatter schema 9 字段
- 验证 lock 机制
- 验证 wiki/index.md 更新

**不包含**:
- 真实 web 搜索(用已查到的资料,避免再烧配额)
- 真实写最终 wiki 页(只产中间产物)

## Sub-tasks

| ID | 描述 | Owner | 输出位置 |
|---|---|---|---|
| ST-1 | orchestrator 拆任务,announce protocol | main-claude | `scratchpad/2026-06-04-agent-stack-test/req-01.md` |
| ST-2 | researcher-1 收集 3 工具(wiki 已有) | researcher-1 | `scratchpad/2026-06-04-agent-stack-test/result-01-research.md` |
| ST-3 | writer-1 写报告草稿 | writer-1 | `scratchpad/2026-06-04-agent-stack-test/result-02-draft.md` |
| ST-4 | 交叉验证(hand-off + lock) | main-claude | `scratchpad/2026-06-04-agent-stack-test/result-03-verify.md` |
| ST-5 | archive | main-claude | `tasks/_archive/2026-06-04-agent-stack-test.md` |

## 验收标准

- [ ] 3 agent 全部 status=active
- [ ] task page frontmatter 9 字段全
- [ ] scratchpad 5 个文件,namespace 隔离
- [ ] 至少 1 次 hand-off(lock 字段验证)
- [ ] 至少 1 次 archive(`tasks/_archive/`)
- [ ] `wiki/index.md` 加新条目
- [ ] `wiki/log.md` 追加记录
- [ ] 真死链 = 0

## 进度日志

- 2026-06-04 14:20 — 任务创建,assignees 含 3 agents
