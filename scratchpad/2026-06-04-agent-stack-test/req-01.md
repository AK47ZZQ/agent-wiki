---
owner: agents/main-claude
ttl: 2026-06-04T18:00:00
topic: Announce 协议栈测试 — 拆任务给 researcher-1
readers:
  - agents/researcher-1
  - agents/writer-1
created: 2026-06-04T14:25:00
level: long
task_id: 2026-06-04-agent-stack-test
from: agents/main-claude
to: agents/researcher-1
action: request
priority: high
---

# Request: 收集 3 工具(已有 wiki 资料,无 web 搜索)

## 任务

从 wiki 已有内容中提取 3 个 Agent 工具的对比维度,**不**做新 web 搜索(避免烧配额)。

## 必读 3 个工具页

1. [[concepts/ai-coding-tools-comparison]]
2. [[concepts/hermes-kanban]]
3. [[concepts/symphony-spec-as-product]]

## 必输出

写 `result-01-research.md` 包含:
- **frontmatter 9 字段**(title/created/updated/type/tags/source/confidence + 任选)
- **3 工具 × 4 维度对比表**:
  - 工具名 / 定位 / 适用场景 / 已知陷阱
- **≥ 2 条 wikilink 出链**(回指 source 页)
- **≥ 1 个 source URL**(wiki/concepts/X)

## 不要做

- ❌ 跑新 web 搜索(用 wiki 已有)
- ❌ 写最终报告(那是 writer-1 的事)
- ❌ 创建新 wiki 页

## 验收

- 文件在 `scratchpad/2026-06-04-agent-stack-test/result-01-research.md`
- frontmatter 9 字段全
- 3 工具 × 4 维度表完整
- 文件大小 < 5KB(避免过度展开)

## 时间

- TTL: 2026-06-04 18:00(3.5h 内)
- 实际期望 5-10 分钟

## 完成后

写 `result-01-research.md` + 在本文件追加 status 行
