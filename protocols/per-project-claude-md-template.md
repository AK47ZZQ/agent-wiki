---
title: Per-Project CLAUDE.md 模板(Progressive Disclosure 落地)
created: 2026-06-04
updated: 2026-06-04
type: protocol
tags: [protocol, claude-md, progressive-disclosure, template, project-context]
sources:
  - local
  - https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b
  - https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai
confidence: high
source: per-project-claude-md-2026
---

# Per-Project CLAUDE.md 模板(Progressive Disclosure 落地)

> **问题**:Claude Code / Hermes Agent 启动时只读 root CLAUDE.md。如果所有项目细节都堆在 root,违反 Meta 60K workers 总结的"Progressive Disclosure"原则(lean root + 按 folder drill)。
> **解决**:每个项目目录有自己的 CLAUDE.md,只在打开该目录时加载。
> **本文是模板** — 复制本文件到项目目录,改 4 处占位符即可。

## 1. 模板(可直接复制)

```markdown
# <project-name> — Per-Project CLAUDE.md

> **本文件位置**: `<project-root>/CLAUDE.md`
> **加载时机**: Agent 进入本项目目录时(不是启动时)
> **设计原则**: Progressive Disclosure — 本文件 5-8K,只放项目特定 context,不放通用 schema(那是 root CLAUDE.md 的事)

## Project Overview
- **Name**: <project-name>
- **Type**: <codebase|research|writing|tooling>
- **Created**: YYYY-MM-DD
- **Owner**: <user|team|none>
- **Status**: <active|paused|archived>

## Goal
(一两句话说明这个项目要做什么,why)

## Scope
**包含**:
- <核心能力 1>
- <核心能力 2>

**不包含**:
- <明确边界>
- <明确边界>

## Tech Stack
- **Language**: <Python 3.12|TypeScript 5.4|...>
- **Framework**: <FastAPI|Next.js|...>
- **Build**: <uv|pnpm|cargo>
- **Test**: <pytest|vitest|...>
- **Lint**: <ruff|eslint|...>
- **Deploy**: <Docker|k8s|...>

## 关键文件
| 路径 | 用途 |
|---|---|
| `src/main.py` | 入口 |
| `tests/test_main.py` | 主测试 |
| `pyproject.toml` | 依赖 |

## 约定(本项目特有)
- **代码风格**: <black|rustfmt|...>
- **commit 格式**: <conventional commits|...>
- **PR 流程**: <trunk-based|gitflow>
- **环境变量**: <.env.example 位置>

## 常见陷阱
- ❌ <具体陷阱 1> — 用 <正确做法>
- ❌ <具体陷阱 2> — 用 <正确做法>

## Wiki 关联
- 项目背景:[[concepts/your-domain-concept]]
- 架构图:[[methods/your-architecture-doc]]
- 历史决策:[[log#YYYY-MM-DD-this-project|log.md 链接段]]

## 已知问题 / TODO
- [ ] <issue 1>
- [ ] <issue 2>
```

## 2. 实际案例:hermes-workspace 项目

**位置**:`projects/hermes-workspace/CLAUDE.md`

```markdown
# Hermes Workspace — Per-Project CLAUDE.md

> **本文件位置**: `projects/hermes-workspace/CLAUDE.md`
> **加载时机**: Agent 进入 hermes-workspace 目录时

## Project Overview
- **Name**: hermes-workspace
- **Type**: codebase (React + Vite SPA, Hermes 周边工具)
- **Repo**: outsourc-e/hermes-workspace
- **Status**: paused (2026-05 后未启动)

## Goal
为 Hermes Agent 提供 web 端 dashboard / kanban / swarm 模式编排。
**当前状态**:未启动(workspace:3000 down)。

## Scope
**包含**:
- Dashboard UI (React)
- Kanban 编排
- Swarm 模式

**不包含**:
- 实际 Hermes core(那是 NousResearch/hermes-agent)
- 内部工具(比如 LCM、Hindsight)

## Tech Stack
- **Frontend**: React 19 + Vite
- **Backend**: Hermes Gateway (REST + SSE)
- **Build**: pnpm
- **Test**: vitest (未运行)
- **Lint**: eslint

## 关键文件
| 路径 | 用途 |
|---|---|
| `src/main.tsx` | 入口 |
| `src/components/` | UI 组件 |
| `package.json` | 依赖 |

## 约定
- **TypeScript strict mode**: 必须
- **No any**: 显式类型
- **PR 流程**: trunk-based,无需 review (单 owner)

## 常见陷阱
- ❌ 启动前忘了 `pnpm install` — node_modules 不在 git,必须 install
- ❌ Gateway 未启动时 workspace 显示 502 — 检查 :8642 /health

## Wiki 关联
- 架构:[[entities/hermes-workspace-architecture]]
- 部署:[[entities/hermes-workspace-deployment-guide]]
- 概念:[[concepts/full-stack-ecosystem]]

## 已知问题 / TODO
- [ ] 启动前先 `pnpm install` 验证 node_modules
- [ ] 内部网穿透方案(参考 [[notes/search-hermes-workspace-expose]])
```

## 3. Per-Project vs Root CLAUDE.md 边界

| 内容 | 写到哪里 | 理由 |
|---|---|---|
| **Schema / 协议 / 多 Agent 协调** | Root `wiki/CLAUDE.md` | 全 vault 通用,所有 Agent 启动必读 |
| **项目特定 tech stack / 约定 / 陷阱** | `<project>/CLAUDE.md` | 只有该项目的 Agent 需要 |
| **项目相关的 wiki 链接** | `<project>/CLAUDE.md` § "Wiki 关联" | 按需加载,避免 root 膨胀 |
| **项目相关的 log** | `<project>/CLAUDE.md` § "已知问题" | 短记录,不污染 wiki log.md |
| **项目相关的 concept** | wiki 主目录 | 跨项目共享的知识 |
| **项目相关的 entity** | wiki 主目录 | 跨项目共享的实体 |

## 4. 加载时机与优先级

```
Agent 启动
  │
  ├─ 读 root CLAUDE.md (5-8K) ← 启动时
  │    → schema + 5 层协议
  │
  ├─ 读 index.md (3-5K)
  │    → catalog 定位相关页
  │
  ├─ 进入 <project>/ 目录
  │    │
  │    └─ 读 <project>/CLAUDE.md (5-8K) ← 按需
  │         → 项目特定 context
  │
  └─ 按需 drill 到 wiki 页(<200 行)
       → 详细
```

**总加载量**:
- 启动: ~10K (root + index)
- 进入项目: +5-8K (per-project CLAUDE.md)
- 深入某页: +1-3K (wikilink 跳读)
- **总计: 15-25K** (1 屏内,符合 Meta 60K 模式)

## 5. 创建新项目 CLAUDE.md 的步骤

1. **创建文件**:`<project>/CLAUDE.md`
2. **复制本模板** (上面 § 1)
3. **改 4 处占位符**:
   - `<project-name>` → 项目真实名
   - `<project-root>` → 绝对路径
   - `<goal>` → 项目目标
   - `<user|team|none>` → owner
4. **加 Wiki 关联** (用 `[[wikilink]]` 引用已有 wiki 页)
5. **写已知问题** (从 `git log` / `issue tracker` 同步)
6. **更新 root CLAUDE.md**:在第 5 层"多 Agent 协作"加"per-project drill 模式"段

## 6. 验证清单

新建 per-project CLAUDE.md 后自检:

```
[ ] 文件位置正确(<project>/CLAUDE.md)
[ ] 大小 5-8K(超过 = 该拆 per-section)
[ ] Goal + Scope + Tech stack 都填了
[ ] ≥ 2 条 Wiki 关联(避免孤岛)
[ ] ≥ 1 个"常见陷阱"段(从经验沉淀)
[ ] 没有"通用 schema"(那是 root 的事)
[ ] 没有"目录树"段(那是 root 的事)
[ ] frontmatter 不必有(per-project CLAUDE.md 不是 wiki 页)
```

## 7. 关联

- Root:[[CLAUDE]]
- 元方法论:[[methods/wiki-as-second-brain]]
- Progressive Disclosure:[[protocols/multi-agent-detail]] § 5.1
- 来源:
  - [Meta 60K knowledge workers](https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b)
  - [Eric J Ma — Obsidian + AI PKM](https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai)
