---
title: Wiki Index
created: 2026-05-28
updated: 2026-06-04
type: meta
tags: [index, wiki, catalog]
---

# Wiki Index

> **2026-06-04 状态**:73 个 .md / 4 知识类别 + 4 多 Agent 节点。死链 0(plain text 误报除外)。
> 启动一个 Agent 后,先读 [[CLAUDE]],再读本文件,再读 [[agents/README]]。

## 📐 协议层(启动必读)

| 文档 | 用途 | 何时读 |
|---|---|---|
| [[CLAUDE]] | Schema + 5 层协议(读/写/索引/反模式/多 Agent) | Agent 启动第一读 |
| [[AGENTS]] | Hermes 4-Tier 记忆系统(LCM/Hindsight/memory tool) | 涉及 memory 操作时 |
| [[README]] | 快速开始(打开 Obsidian、看 graph、跑 archiver) | 第一次访问 vault |

## 🤖 多 Agent 第二大脑(2026-06-04 新)

| 节点 | 注册/入口 | 用途 |
|---|---|---|
| [[agents/README|Agent registry]] | agents/main-claude + 4 模板 + 2 实例(researcher-1/writer-1,2026-06-04 测试新增) | 谁存在、能做什么、怎么调用 |
| [[scratchpad/README|Scratchpad]] | scratchpad/index.md | 短期共享中间状态(ephemeral/short/long 3 类 TTL) |
| [[tasks/README|Task board]] | tasks/index.md | 跨 Agent 长生命周期任务 |
| [[protocols/agent-coordination|Protocols]] | protocols/agent-coordination.md | 6 通信原语(announce/request/claim/update/hand-off/archive) |

### Agent 实例(7)
- [[agents/main-claude]] — orchestrator,主控
- [[agents/hermes-kanban-orchestrator]] — Kanban 编排(模板)
- [[agents/hermes-kanban-worker]] — Kanban worker(模板)
- [[agents/hermes-self-check]] — Hermes 自检(模板)
- [[agents/researcher-1]] — researcher 实例(2026-06-04 E2E 测试)
- [[agents/writer-1]] — writer 实例(2026-06-04 E2E 测试)

### Protocols(4)
- [[protocols/agent-coordination]] — 6 原语 + A2A 兼容映射
- [[protocols/goal-alignment]] — 主动告警机制
- [[protocols/multi-agent-detail]] — frontmatter 9 字段 schema
- [[protocols/per-project-claude-md-template]] — Progressive Disclosure 模板

## 📊 当前任务

| ID | 状态 | Owner | 主题 |
|---|---|---|---|
| [[tasks/2026-06-04-agent-stack-test\|2026-06-04-agent-stack-test]] | done | main-claude | 端到端测试整个多 Agent 第二大脑协议栈(2026-06-04 实测通过) |
| [[tasks/wiki-multi-agent-refactor]] | done | main-claude | Wiki 多 Agent 第二大脑重构(2026-06-04 任务记录) |
| [[tasks/cleanup-worker-debris]] | pending | main-claude | 清理 worker 删除残留 |

## 📚 知识层(5 类别)

### Method(6) — 可复用方法
- [[methods/hermes-workflow-and-exploration]] — 双技能方法(执行+探勘)
- [[methods/ralph-wiggum-loop]] — 背压门控循环 + Hermes 映射
- [[methods/session-to-wiki-archiving]] — Session→Wiki 归档流程
- [[methods/install-hindsight-native-hermes-method]] — Hindsight native 装法
- [[methods/hindsight-4d-retrieval-complete]] — Hindsight 4 维检索
- [[methods/feishu-wiki-pipeline]] — 飞书→Wiki 手动同步
- [[methods/wiki-as-second-brain]] — Wiki 作为第二大脑的方法论(2026-06-04 新)
- [[methods/wiki-code-workflow]] — CODE 4 阶段(Capture/Organize/Distill/Express)工作流(2026-06-04 新)

### Concepts(17) — 概念/主题
- [[concepts/ai-coding-tools-comparison]] — AI 编码工具对比
- [[agent-4-tier-memory-architecture]] — Hermes 4-Tier 记忆架构(2026-06-04 整理,根目录)
- [[concepts/cli-anything]] — HKUDS 方法论 40.6k⭐
- [[concepts/concept-kanban]] — Kanban 多代理并行调度
- [[concepts/fowler-guides-sensors]] — 控制论 2×2 矩阵
- [[concepts/full-stack-ecosystem]] — 14 节点全栈地图(合并版)
- [[concepts/harness-engineering]] — Harness Engineering 速览
- [[concepts/harness-engineering-deep-study]] — 完整框架研究
- [[concepts/hermes-codex-runtime]] — Codex Runtime 架构
- [[concepts/hermes-kanban]] — Durable Kanban 编排
- [[concepts/hermes-workflow]] — P0-P4 工作流
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 真实定位
- [[concepts/hindsight-agent-brief-export-2026]] — 5 文档导出
- [[concepts/agent-memory-state-2026]] — MEMORY/USER 镜像
- [[concepts/mcp-ecosystem-2026]] — MCP 生态全景
- [[concepts/mcpb-bundle-format]] — MCP Bundle 格式
- [[concepts/symphony-spec-as-product]] — Symphony 编排规约
- [[concepts/hindsight-memory-modes-guide]] — Hindsight 4 模式选型(2026-06-04 stub)
- [[concepts/awesome-hermes-agent-ecosystem-2026]] — Awesome Hermes 生态全景(2026-06-05 新)

### Comparisons(3) — 对比分析
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider 对比
- [[comparisons/hindsight-automation-patterns-2026]] — 4 自动化模式对比
- [[comparisons/hindsight-5-modes-2026]] — 5 mode 横向对比(2026-06-04 baseline-no-skill 独立产出)

### Entities(18) — 人物/工具/框架/模型
- [[entities/codex]] — OpenAI Codex 生态
- [[entities/smithery-cli]] — Smithery CLI 工具
- [[entities/tool-cli-anything-obsidian]] — Obsidian CLI
- [[entities/hermes-workspace]] — Workspace 实体
- [[entities/hermes-workspace-architecture]] — 架构深度分析
- [[entities/hermes-workspace-deployment-guide]] — Windows 部署
- [[entities/wondelai-skills]] — 跨平台 Agent 技能库(380★)
- [[entities/mission-control]] — Agent Fleet 编排仪表盘(3.7k★)

#### Skill 索引(7) — 对 hermes/skills/* 的 wiki 索引
- [[entities/hermes-skill-ai-harness-exploration]] — 探勘 v6.0
- [[entities/hermes-skill-hermes-workflow]] — 执行 v4.9
- [[entities/hermes-skill-kanban-orchestrator]] — 编排 v5.2
- [[entities/hermes-skill-kanban-worker]] — Worker v3.1
- [[entities/hermes-skill-database-operations]] — DB v2.0
- [[entities/hermes-skill-api-integration]] — API 集成
- [[entities/hermes-skill-cli-anything-methodology]] — CLI-Anything
- [[entities/hermes-skill-wiki-ingest]] — 知识摄入(2026-06-04 stub)
- [[entities/hermes-skill-wiki-archive]] — 会话归档(2026-06-04 stub)
- [[entities/hermes-skill-llm-wiki]] — LLM Wiki 模式(2026-06-04 stub)

### Notes(5) — 短记录/部署日志
- [[notes/lcm-upgrade-v0.12-to-v0.15]] — LCM 升级记录
- [[hindsight-first-active-workflow]] — Hindsight-first 主动工作流(2026-06-04 整理,根目录)
- [[hindsight-first-memory-pattern]] — Hindsight-first 记忆模式(2026-06-04 整理,根目录)
- [[notes/hindsight-local-deployment-windows-2026]] — Windows 本地部署
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险与优化
- [[notes/search-hermes-workspace-expose]] — 内网穿透方案研究
- [[notes/hindsight-semantic-only-mode-2026]] — semantic-only mode(2026-06-04 新装的第 5 种 mode)

### References(1) — 长引用
- [[references/hermes-commands-full|hermes-commands-full]] — Hermes 命令大全 V2 提炼版

## 🗑️ Archive

历史 session 已精简移除(无需保留归档)。

## 📥 Source

- `raw/work/hermes命令大全v2-...-1780136199.md` — 最新源文件
- `raw/tech/awesome-hermes-agent-zh.md` — Awesome Hermes 清单源文件(30KB, 2026-06-05 摄入)

## 📋 日志与索引子页

- [[log|log.md]] — 完整操作日志(写读删改全部记录)
- [[indexes/index|indexes/]] — 主题子索引
- [[indexes/log|indexes/log.md]] — 子索引日志

---

## 写入协议(摘要)

> 完整协议见 [[CLAUDE]]

1. 任何新页:`Grep` 查重 → 满足 2+ 来源门槛 → 创建 → 写 frontmatter 9 字段 → 加 wikilink × 2+ → 更新本文件
2. 任何修改:bump `updated` 日期,标 `contradictions` if conflict
3. 任何归档:移到 `notes/_archive/` 或删除
