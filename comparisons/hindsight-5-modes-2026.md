---
title: Hindsight 5 种 Mode 横向对比 (2026-06-04 补充)
created: 2026-06-04
updated: 2026-06-04
type: comparison
tags: [hindsight, memory, mode, semantic-only, comparison, baseline-eval]
sources:
  - notes/hindsight-semantic-only-mode-2026
  - concepts/hindsight-memory-modes-guide
  - methods/install-hindsight-native-hermes-method
  - methods/hindsight-4d-retrieval-complete
confidence: low
source: hindsight-3rd-notebook-2026-06
---

# Hindsight 5 种 Mode 横向对比 (2026-06-04 补充)

> baseline-no-skill producer 的第 2 次尝试产出。与 [[notes/hindsight-semantic-only-mode-2026]] (with-skill producer 的单源 note) 互补, 也与 [[concepts/hindsight-memory-modes-guide]] (5 mode 总览 stub) 互补。**本文件是横向对比**, 不是单源记录, 不是方法论。

## 为什么需要这个对比

`concepts/hindsight-memory-modes-guide` 的表格只列了一行说明, 没做**横向**对比。`notes/hindsight-semantic-only-mode-2026` 是单源 note, 只讲 semantic-only 一个。`methods/hindsight-4d-retrieval-complete` 讲 4 维检索, 跟 mode 是不同维度。

→ **缺口**: 没人把 5 个 mode 放同一张表, 横向比 7 个属性 (auto-recall / 显式工具 / 语义 / 关键词 / 图 / 时间 / 适用场景)。本文件补上。

## 5 个 mode 横向对比表 (核心)

| Mode | 来源 | Auto-recall | 显式工具 | 语义 | 关键词 | 图 | 时间 | 适用场景 | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| `world` | Hindsight 默认 | (未明) | (未明) | ✅ | ✅ | ✅ | ✅ | 客观事实 (世界知识) | medium |
| `agent` | Hindsight | (未明) | (未明) | ✅ | ✅ | ✅ | ✅ | 代理执行上下文 | medium |
| `user` | Hindsight | (未明) | (未明) | ✅ | ✅ | ✅ | ✅ | 用户偏好/历史 | medium |
| `semantic-only` | **2026-06-04 新装** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | 只要语义, 其他全关 | low (新, 单源) |
| (TBD) | — | — | — | — | — | — | — | 第 5 个空位, 待调研 | — |

> 表中 world/agent/user 的 "未明" 单元格, 是因为 stub 没有给完整属性, **不是** 我编的。

## 与现有 4 模式的关系 (重要区分)

`semantic-only` 跟 `world` / `agent` / `user` / TBD **不是同维度**:
- `world` / `agent` / `user` / TBD 是**内容分类** (按 type 分)
- `semantic-only` 是**检索策略限定** (按维度分)
- 不冲突, 但也不互相替代

`semantic-only` 跟 Hermes `memory_mode` 的 `hybrid` / `context` / `tools` 也不是同维度:
- `memory_mode` 控制**Hermes 怎么用 Hindsight** (auto-recall 开不开, 工具可不可见)
- `semantic-only` 控制 **Hindsight 怎么检索** (走哪个维度)
- 正交, 可叠加

→ 用户问"想用 semantic-only 还要 auto-recall 怎么办" → 答案是 "改 `memory_mode=hybrid` 启用 auto-recall, 同时配置 semantic-only 限定检索维度"。

## 与 4 维检索的关系 (Hybrid 是默认)

`methods/hindsight-4d-retrieval-complete` 列出 4 维: semantic / keyword / graph / temporal。

| 4 维 | 默认 (Hybrid) | semantic-only |
|---|---|---|
| semantic (bge 384d) | ✅ | ✅ |
| keyword (PG FTS5) | ✅ | ❌ |
| graph (entities[]) | ✅ | ❌ |
| temporal (query_timestamp) | ✅ | ❌ |
| cross-encoder reranker | ✅ | ✅ (推测) |

→ `semantic-only` = Hybrid 去掉 3 维, 保留 semantic + reranker。

## 决策树 (5 mode 选型)

```
你的需求?
├─ 按内容分类检索 (事实/经验/用户)
│   ├─ 客观事实 → world
│   ├─ 代理执行 → agent
│   └─ 用户偏好 → user
│
├─ 限定检索策略 (不分类, 只走某些维)
│   ├─ 全部 4 维 + reranker → hybrid (默认)
│   └─ 只要 semantic → semantic-only (2026-06-04 新)
│
└─ 限定 Hermes 集成方式
    ├─ auto + 工具 → memory_mode: hybrid
    ├─ auto 不给工具 → memory_mode: context
    └─ 不 auto + 工具 → memory_mode: tools
```

> 3 个维度可叠加: 选 `type=user` + `memory_mode=hybrid` + 4 维全开 = 默认体验。选 `semantic-only` + `memory_mode=context` = 极简体验 (auto + 纯语义, 隐藏工具)。

## 适用 / 不适用场景 (横向)

| 场景 | 推荐 mode | 理由 |
|---|---|---|
| 日常对话 (默认体验) | `user` + `hybrid` + 4 维 | 全功能 |
| 调试 recall 行为 | `world` + `semantic-only` | 单维度好排查 |
| 生产 assistant (隐藏工具) | `user` + `context` + 4 维 | 干净 UX |
| 节省 token (极限) | `user` + `tools` + `semantic-only` | 极简, 但功能受限 |
| 学术分析 (按内容类型) | `world` / `agent` (按需) | 分类清晰 |

## 关键风险 (横向)

| 风险 | 适用 mode | 描述 |
|---|---|---|
| 与 Hindsight 官方 mode 冲突 | semantic-only | 官方文档只列 hybrid/context/tools, semantic-only 可能是用户自定义 |
| L2 token 成本高 | 全部 (默认配置) | hybrid + reflect 自动跑, 月烧 4M+ tokens |
| handoff v1 不兼容 | semantic-only | 现有 handoff 是按 hybrid 设计的 |
| type 过滤会减少 recall | world/agent/user | types 过滤只取 1/3 总数 |
| 3 types vs 4 logical networks 架构偏离 | 全部 | 实际 3 types + entities + disposition, 不是论文的 4 networks |

## 验证清单

- [x] 5 mode 横向对比 (本表)
- [x] 与 4 维检索的关系 (Hybrid 对比)
- [x] 与 3 种 Hermes memory_mode 的正交关系
- [x] 决策树 (3 维度: 内容分类 / 检索策略 / Hermes 集成)
- [x] 适用 / 不适用场景
- [x] 横向风险表
- [ ] 实测 semantic-only (用户后续)

## 与其他 wiki 页的关系

| 页 | 类型 | 关系 |
|---|---|---|
| [[concepts/hindsight-memory-modes-guide]] | concept | 总览, 5 mode 列表 (本文件补全) |
| [[notes/hindsight-semantic-only-mode-2026]] | note | semantic-only 单源 (with-skill producer) |
| [[methods/install-hindsight-native-hermes-method]] | method | 3 种 Hermes memory_mode 详解 |
| [[methods/hindsight-4d-retrieval-complete]] | method | 4 维检索 (Hybrid 默认) |
| [[comparisons/hindsight-automation-patterns-2026]] | comparison | 4 自动化模式 (不同维度, 别混) |
| [[notes/hindsight-risks-and-optimizations-2026]] | note | 风险 (hybrid 下测的) |
| [[concepts/hindsight-in-hermes-ecosystem-2026]] | concept | Hindsight 在 Hermes 生态定位 |

## 与 with-skill / 第一次 attempt 的差异

| 维度 | with-skill (1st) | baseline 1st attempt (被删) | baseline 2nd attempt (本文件) |
|---|---|---|---|
| 页面位置 | `notes/` | `methods/` | `comparisons/` |
| 页面类型 | note | method | comparison |
| 内容重点 | 是什么 (单源) | 怎么用 (复用) | 横向对比 (5 mode 一起) |
| 决策树 | 5 mode 选型 (在 concepts/) | 何时用/不用 | 3 维度叠加 (内容/策略/Hermes) |
| 表格数 | 4 | 6 | 6 |
| wikilink 出链 | 5 | 6 | 7 |
| 置信度 | medium | low | low |

## 关联文档

- [[concepts/hindsight-memory-modes-guide]] — 5 mode 总览 stub
- [[notes/hindsight-semantic-only-mode-2026]] — semantic-only 单源 (with-skill)
- [[methods/install-hindsight-native-hermes-method]] — Hermes 3 memory_mode
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索
- [[comparisons/hindsight-automation-patterns-2026]] — 4 自动化模式 (别混)
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 定位
