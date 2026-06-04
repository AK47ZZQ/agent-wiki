---
title: E2E Multi-Agent Protocol Test — 3 Agent 真任务跑通
created: 2026-06-04
updated: 2026-06-04
type: reference
tags: [e2e, multi-agent, protocol-test, validation, hermes-kanban]
source: session-2026-06-04-task-2026-06-04-agent-stack-test
confidence: high
---

# E2E Multi-Agent Protocol Test — 3 Agent 真任务跑通

> **2026-06-04 实测**:3 Agent 协作真任务,15 分钟跑通完整协议栈。
> **本节目的**:作为方法论沉淀,未来类似任务直接套用,不必重新设计。

## 1. 任务设计

**真任务**:`tasks/2026-06-04-agent-stack-test.md`
- **目标**:3 Agent 工具对比报告(用 wiki 已有资料,避免烧搜索配额)
- **Agent 配置**:
  - `orchestrator` = main-claude
  - `worker-1` = researcher-1 (从 hermes-kanban-worker 模板实例化)
  - `worker-2` = writer-1 (从 hermes-kanban-worker 模板实例化)
- **5 个 ST 子任务**:
  - ST-1: orchestrator 拆任务 + announce protocol
  - ST-2: researcher-1 收集 3 工具
  - ST-3: writer-1 写报告草稿
  - ST-4: 交叉验证(hand-off + lock)
  - ST-5: archive

## 2. 6 原语实际执行轨迹(15 分钟)

```
14:25  announce    orchestrator 创建 task + 3 agent + scratchpad ns
14:25  announce    agents/{main-claude,researcher-1,writer-1}.md 注册
14:25  request     main-claude → researcher-1(写 req-01.md)
14:25  claim       researcher-1 接受(assignees 更新)
14:28  update      researcher-1 → result-01-research.md(3 工具 × 4 维度)
14:32  hand-off    writer-1 接管 result-01(lock: writer-1 / 600s)
14:32  update      writer-1 → result-02-draft.md(决策树 + 1-page)
14:35  release     writer-1 release lock(status: done)
14:38  update      main-claude → result-03-verify.md(6 原语验证)
14:40  update      main-claude → final.md(总结)
14:40  archive     任务 → tasks/_archive/2026-06-04-agent-stack-test.md
```

## 3. 关键产物清单

| 类别 | 文件 | 角色 | 关键 frontmatter |
|---|---|---|---|
| Task | `tasks/2026-06-04-agent-stack-test.md` | orchestrator 创建 | 9 字段全 |
| Agent 实例 | `agents/researcher-1.md` | 实例化 | status=active, template=hermes-kanban-worker |
| Agent 实例 | `agents/writer-1.md` | 实例化 | 同上 |
| Scratchpad ns | `scratchpad/2026-06-04-agent-stack-test/` | namespace 隔离 | — |
| Index | `.../index.md` | workspace 入口 | 9 字段 |
| Request | `.../req-01.md` | request 原语 | from/to/readers/action/priority |
| Result-1 | `.../result-01-research.md` | researcher 产出 | task_id/related_to |
| Result-2 | `.../result-02-draft.md` | writer 产出 | **lock/locked_at/lock_ttl/status** |
| Result-3 | `.../result-03-verify.md` | main-claude 验证 | status=passed |
| Final | `.../final.md` | 总结 | status=done |
| Archive | `tasks/_archive/2026-06-04-agent-stack-test.md` | 归档 | — |

## 4. 验证矩阵(8/8 全通过)

| 验收项 | 结果 |
|---|---|
| 3 agent 全部 status=active | ✅ |
| task page frontmatter 9 字段全 | ✅ |
| scratchpad 6 文件,namespace 隔离 | ✅ |
| 1 次 hand-off(lock 字段验证) | ✅ writer-1 → main-claude |
| archive 完成 | ✅ |
| wiki/index.md 更新 | ✅ |
| wiki/log.md 记录 | ✅ |
| 真死链 = 0 | ✅ |

## 5. 5 个发现(下次避免)

1. **Frontmatter schema 在真任务中 100% 命中** — 7 必填 + 12 选填,没漏
2. **Lock 机制有效但没强冲突** — 单 orchestrator 顺序交接,未触发强竞争
3. **Namespace 隔离生效** — 2 个 task namespace 并存,无文件冲突
4. **6 原语全覆盖** — 6/6 触发,无遗漏
5. **失败兜底未触发** — 全部 15 分钟内完成,无 agent 失联/lock 过期

## 6. 3 个改进建议(下次 E2E 测试)

1. **并行加速**:researcher-1 + writer-1 可在 data-flow 允许时并行
2. **冲突演练**:设计 1 个"2 agent 同时写同文件"场景,验证 lock 强冲突
3. **archive 自动化**:task status=done 时,加 cron 自动 archive

## 7. A2A 兼容映射验证(同时验证)

| 我的原语 | A2A 等价 | 实际触发 |
|---|---|---|
| announce | Agent Card | ✅ 3 agent 实体 |
| request | Message (JSON-RPC) | ✅ req-01.md from/to/readers |
| claim | Task Lifecycle Event | ✅ assignees 字段更新 |
| update | Task Status Update | ✅ 3 result 文件 |
| hand-off | Streaming + lock 字段 | ✅ writer-1/600s |
| archive | Task Finalization Event | ✅ task 移到 _archive/ |

## 8. 复用模板(下次 E2E 测试直接套用)

```
1. 设计真任务(用 wiki 已有资料,避免烧配额)
2. 注册 3 Agent(orchestrator + 2 worker 实例化模板)
3. 创建 task page (9 字段 frontmatter)
4. 创建 scratchpad namespace (task-id/)
5. 写 req-01.md (request 原语)
6. 顺序执行:
   - worker-1 写 result-01
   - worker-2 接管 (lock + 600s) 写 result-02
   - orchestrator 验证 result-03
   - final 总结
7. archive task 到 _archive/
8. 更新 index.md + log.md
```

**预计耗时**:15-20 分钟
**预计产出**:10-12 个文件(2 agent + 1 task + 6 scratchpad + 1 archive)
**验证点**:6 原语 + 9 字段 + namespace + lock + A2A 兼容

## 9. 关联

- [[protocols/agent-coordination]] — 6 原语
- [[protocols/multi-agent-detail]] — frontmatter schema + namespace
- [[methods/wiki-as-second-brain]] — 协议 + DRY
- [[methods/wiki-code-workflow]] — CODE 4 阶段
- `agents/hermes-kanban-worker` (template) — 实例化源

## 10. 版本历史

- v1.0 (2026-06-04) — 初始版本,从首次真任务 E2E 测试提炼
