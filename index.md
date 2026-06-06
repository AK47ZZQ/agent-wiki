---
title: Wiki Index
created: 2026-05-28
updated: 2026-06-06 00:28
type: meta
tags: [index, wiki, catalog]
---

# Wiki Index

> **2026-06-05 状态**:125 个 .md (新增 5: v1.6 漏洞 + v1.7 修复 + v1.1 增补 + 反思 + Hindsight/gbrain 源仓库 + **DSPy 3.2.1 实战**) / 6 知识类别。死链 0。**DSPy 自动化 mental_model + 标准化 wiki 草稿 + BootstrapFewShot 5 步核验金标准**。
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
- [[agents/hermes-3rd]] — 笔记本协作 Agent(2026-06-04 onboarded, status: active, 5.4K)
- [[entities/hermes-3rd]] — 3rd 详细档案 (8.3K, 10 章节, 协作/能力/踩坑/roadmap)
- [[agents/hermes-kanban-orchestrator]] — Kanban 编排(模板)
- [[agents/hermes-kanban-worker]] — Kanban worker(模板)
- [[agents/hermes-self-check]] — Hermes 自检(模板)
- [[agents/researcher-1]] — researcher 实例(2026-06-04 E2E 测试)
- [[agents/writer-1]] — writer 实例(2026-06-04 E2E 测试)
- [[agents/coordination-cheatsheet]] — 协调速查表(2026-06-04 新)
- [[agents/user-preferences]] — 用户偏好(2026-06-04 新)
- [[agents/tools-gh-cli]] — gh CLI 本机部署(Windows main-claude,2026-06-04 新)
- [[agents/skills-github-gh-cli/SKILL|Skills: github-gh-cli]] — gh CLI skill 镜像(60K,4 references + 1 script + 1 template,3rd 端可拉)
- [[agents/skills-markitdown-converter/SKILL|Skills: markitdown-converter]] — MarkItDown skill 镜像(56K,PDF/DOCX/图片 OCR → Markdown,3rd 端可拉)

### Protocols(4)
- [[protocols/agent-coordination]] — 6 原语 + A2A 兼容映射
- [[protocols/goal-alignment]] — 主动告警机制
- [[multi-agent-communication]] — 4 频道通信协议(根目录,2026-06-04 新)
- [[protocols/multi-agent-detail]] — frontmatter 9 字段 schema
- [[protocols/per-project-claude-md-template]] — Progressive Disclosure 模板
- [[protocols/git-collaboration-multi-agent]] — 多 Agent Git 协作协议(2026-06-04,本机+3rd 共维护 wiki)

## 📊 当前任务

| ID | 状态 | Owner | 主题 |
|---|---|---|---|
| [[tasks/_archive/2026-06-04-agent-stack-test|2026-06-04-agent-stack-test]] | done | main-claude | 端到端测试整个多 Agent 第二大脑协议栈(2026-06-04 实测通过,已 archive) |
| [[tasks/wiki-multi-agent-refactor]] | done | main-claude | Wiki 多 Agent 第二大脑重构(2026-06-04 任务记录) |
| [[tasks/cleanup-worker-debris]] | pending | main-claude | 清理 worker 删除残留 |
| [[tasks/daily-knowledge-curation]] | active | main-claude | 每日新知识推送流程(2026-06-04 启) |
| [[tasks/git-collaboration-rollout]] | active | both | Git 协作协议 v1.1 部署(2026-06-04 启) |

## 📚 知识层(5 类别)

### Method(22) — 可复用方法
- [[methods/agent-safety]] — Agent 安全模型 (5 层防护 + 13 规则表 + 权限模型) (2026-06-05 新)
- [[methods/agent-evaluation]] — Agent 评估方法 (SWE-bench / HumanEval / E2E / Eval-Driven) (2026-06-05 新)
- [[methods/agent-writing-standard]] — **Agent 写入规约** (判断矩阵 + 5 反模式 + 清理协议) (2026-06-05 新)
- [[methods/hermes-workflow-and-exploration]] — 双技能方法(执行+探勘)
- [[methods/ralph-wiggum-loop]] — 背压门控循环 + Hermes 映射
- [[methods/session-to-wiki-archiving]] — Session→Wiki 归档流程
- [[methods/install-hindsight-native-hermes-method]] — Hindsight native 装法
- [[methods/hindsight-4d-retrieval-complete]] — Hindsight 4 维检索
- [[methods/feishu-wiki-pipeline]] — 飞书→Wiki 手动同步
- [[methods/wiki-as-second-brain]] — Wiki 作为第二大脑的方法论(2026-06-04 新)
- [[methods/wiki-code-workflow]] — CODE 4 阶段(Capture/Organize/Distill/Express)工作流(2026-06-04 新)
- [[methods/wiki-curation-guide]] — wiki 策展指南(2026-06-04 新)
- [[methods/curation-checklist]] — 新知识入库清单(2026-06-04 新)
- [[methods/using-knowledge-base]] — 知识库使用指南(2026-06-04 新)
- [[methods/safe-commit-push-protocol]] — 5 步核验协议(2026-06-04 新)
- [[methods/git-push-cheatsheet]] — 1 页速查:5 步核验 + 假成功防御(2026-06-04 新)
- [[methods/ai-coding-tools-2026]] — AI Coding Tools 横评(2026-06-04 新)
- [[methods/git-tutorial]] — Git 协作教程(2026-06-04 新)
- [[methods/feishu-rich-messages]] — 飞书富文本消息(2026-06-04 新)
- [[methods/feishu-group-setup]] — 飞书群聊配置(2026-06-04 新)
- [[methods/lcm-memory-guide]] — LCM 内存管理(2026-06-04 新)
- [[methods/scratchpad-coordination]] — Scratchpad 协调(2026-06-04 新)
- [[methods/hindsight-health-monitoring-protocol]] — Hindsight liveness + auto-restart cron 协议(2026-06-04 新,本会话 20:11 实测)
<!-- BEGIN merge (远端 远端 + 3rd 都保留) -->
- [[methods/gh-extension-development]] — gh CLI extension 开发实战(2026-06-04 新,Go binary 模式)
- [[methods/gh-command-cheatsheet]] — gh CLI 命令速查 L1-L2(2026-06-04 新)- [[methods/hindsight-idle-timeout-watchdog]] — Hindsight idle timeout 笔记本无 cron 守护法(env 改 + foreground 模式,3 方案 5 步实操,2026-06-04 3rd 笔记本实战)<!-- END merge -->

### Concepts(22) — 概念/主题
- [[concepts/agent-reasoning-patterns]] — Agent 推理模式: CoT / ReAct / ToT / Reflexion (2026-06-05 新)
- [[concepts/ai-coding-tools-comparison]] — AI 编码工具对比
- [[concepts/agent-4-tier-memory-architecture]] — Hermes 4-Tier 记忆架构(2026-06-04 整理,根目录)
- [[concepts/wiki-quality-metrics]] — 9 维质量指标仪表盘(2026-06-04 新)
- [[concepts/cli-anything]] — HKUDS 方法论 40.6k⭐
- [[concepts/concept-kanban]] — Kanban 多代理并行调度
- [[concepts/fowler-guides-sensors]] — 控制论 2×2 矩阵
- [[concepts/full-stack-ecosystem]] — 14 节点全栈地图(合并版)
- [[concepts/harness-engineering]] — Harness Engineering 速览 (v2.0 更新)
- [[concepts/harness-engineering-deep-study]] — 完整框架研究 v2.1 (35KB, Agent 开箱即用, 22 篇来源 + 5 旗舰实现, 决策树 + 15 项自检 + Harness 有效性度量 7 指标)
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
- [[concepts/context-engineering]] — 上下文作为工程资源管理 (2026-06-05 新)
- [[concepts/awesome-hermes-agent-ecosystem-2026]] — Awesome Hermes 生态全景(2026-06-05 新)
- [[concepts/hindsight-0.6.1-vs-0.7.2-evolution]] — Hindsight 0.6.1→0.7.2 实战差异 (跨 main-claude 台式 + 3rd 笔记本, 6 维度 + 3 schema 坑 + 2 节点链路, 2026-06-04 3rd 第 2 次 6 步探勘法实战)
<!-- BEGIN merge (远端 远端 + 3rd 都保留) -->
- [[concepts/github-cli-overview]] — GitHub CLI (gh) 概览 / 何时用(2026-06-04 新)
- [[concepts/github-cli-architecture]] — gh CLI 内部架构(Cobra/Factory/go-gh)(2026-06-04 新)- [[concepts/hindsight-0.7.2-idle-timeout-mechanism]] — Hindsight 0.7.2 daemon idle 1800s SIGTERM 机制(4 触发要素 + 笔记本vs台式差异 + 4 隐藏细节,2026-06-04 3rd 笔记本 21:04 实战)<!-- END merge -->

### Comparisons(5) — 对比分析
- [[comparisons/multi-agent-architecture-patterns]] — 多 Agent 架构 6 模式对比与选型 (2026-06-05 新)
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider 对比
- [[comparisons/hindsight-0.6.1-vs-0.7.2-cross-machine-comparison]] — Hindsight 0.6.1 vs 0.7.2 跨机器对比 (台式 + 笔记本, 7 维度 + 守护哲学差异, 2026-06-04 3rd 第 2 次 6 步探勘法实战)
- [[comparisons/hindsight-automation-patterns-2026]] — 4 自动化模式对比
- [[comparisons/hindsight-5-modes-2026]] — 5 mode 横向对比(2026-06-04 baseline-no-skill 独立产出)

### Entities(19) — 人物/工具/框架/模型
- [[entities/codex-cli-deep-dive]] — Codex CLI 深度解析 (沙箱/AGENTS.md/MCP/Hermes协作) (2026-06-05 新)
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

### Notes(9) — 短记录/部署日志
- [[notes/lcm-upgrade-v0.12-to-v0.15]] — LCM 升级记录
- [[methods/hindsight-first-active-workflow]] — Hindsight-first 主动工作流(2026-06-04 整理,根目录)
- [[methods/hindsight-first-memory-pattern]] — Hindsight-first 记忆模式(2026-06-04 整理,根目录)
- [[notes/hindsight-local-deployment-windows-2026]] — Windows 本地部署
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险与优化
- [[notes/search-hermes-workspace-expose]] — 内网穿透方案研究
- [[notes/hindsight-0.7.2-bank-config-migration]] — 0.7.2 bank config 迁移指南 (memory_mode 废弃 + 6 项 PATCH 实操 + 3 schema 坑)
- [[notes/hindsight-semantic-only-mode-2026]] — semantic-only mode(2026-06-04 新装的第 5 种 mode)
- [[notes/hindsight-daemon-fix-2026-06-04]] — Hindsight daemon 修复记录 (14:25-15:13, minimax provider + /v1 端点 + 域名拼写, **main-claude 台式 4 周前成功**)
- [[notes/hindsight-env-truly-fixed-2026-06-05]] — **3rd 笔记本 v0.7.1 env 独立 bug 修复** (10:10-10:15, 6-5 selfcheck, 本机 venv v0.7.1 跟 main-claude v0.7.2 minor 漂移, env 错配独立修, Windows ACL 4 陷阱 + env 注入 5 步法)
- [[notes/hindsight-v072-upgrade-3rd-notebook-2026-06-05]] — **Hindsight v0.7.2 升级 + idle 守护 + LLM 端到端** (10:35-10:45, 4 件套 0.7.1→0.7.2 升级, `--daemon --idle-timeout 1800` 守护, F.1-F.6 5 步核验 100% 成功)
- [[notes/lessons-learned-index]] — 经验教训索引 (含自检方法 + stale 检测经验, 原快照页已归档至 _archive/)
- [[notes/multi-machine-wiki-paths]] — 多机器 Wiki 路径对照表 (笔记本 ZZQ vs 台式 Administrator, 5 项差异)
- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — Hindsight 部署快照 (⚠️ 已 stale, 方法论见 methods/hindsight-health-monitoring-protocol)
- [[notes/lessons-learned-index]] — **经验与教训索引** (2026-06-05 新建,跨 session 沉淀)
- [[notes/auto-apply-mode-best-practices]] — **Auto-Apply 模式最佳实践** (2026-06-05 新建, 5 guard rails + 8 步流程)
- [[notes/git-commit-push-playbook-2026-06-04]] — Git 提交+推送 4 步最佳实践 (3rd 端贡献, 9.3K)
- [[notes/git-push-v16-pitfalls-2026-06-05]] — **v1.6 漏洞实战** (3rd, 22:10, 5 步核验金标准 + v1.7 脚本根因)
- [[notes/safe-commit-push-v17-deep-fix-2026-06-05]] — **v1.7 终极修复 + agent 治理 commit 实战** (3rd, 23:10, mktemp+here-doc+git commit -F file + BRANCH 永远从 git 取 + 3 大坑+ 5 步核验全过)
- [[notes/reflection-hermes-3rd-2026-06-05-2320]] — **自我反思 4 反模式 + 5 改进项** (3rd, 23:20, 工具失败停手 / 贴结果≠用结果 / 一锤改5处 / 9轮patch钻printf + 共同根因"优化轮次=优化做错" + meta对齐"穷尽≠一次")
- [[notes/hindsight-gbrain-source-code-learning-2026-06-05]] — **Hindsight v0.7.2 + gbrain v0.42.10 源仓库学习** (3rd, 23:35, INSTALL 9 步 / _CONFIGURABLE_FIELDS 38 字段全景 / 4 vector ext / 5 text search / 3 bank template + mental_model+directive 实战 200)
- [[notes/dspy-3-2-1-applications-2026-06-06]] — **DSPy 3.2.1 实战** (3rd, 00:25, 4 个应用: 最小调用 / ChainOfThought 4 层架构生成 / BootstrapFewShot 5 步核验优化 / **zzq-preferences mental_model 自动生成** 200)
- [[agents/tools-markitdown]] — MarkItDown 本机部署 (Windows main-claude, 2026-06-04)
- [[concepts/markitdown-overview]] — MarkItDown 概览 (Microsoft 开源文件→Markdown 转换器)
- [[methods/markitdown-cheatsheet]] — MarkItDown CLI/Python/5 实战配方

- [[concepts/agent-governance-framework]] — Agent 治理框架 (2026-06-06 补,3 硬规则 + 5 软规则, 从 reflection 引用反推)
- [[concepts/llm-wiki-pattern]] — LLM Wiki Pattern (2026-06-06 补, Karpathy 风格 LLM 驱动互链, 从 reflection 引用反推)
- [[notes/hindsight-windows-acl-trap]] — Hindsight Windows ACL 陷阱 (2026-06-06 补, daemon log access denied 排查 3 方案, 从 lessons-learned 引用反推)
- [[notes/hindsight-l2-deep-fix-2026-06-05-afternoon]] — Hindsight L2 deep fix 下午场 (3rd, 6-5, mental_models/directives 子表设计 + bank updated_at 区分 + 4 PATCH items 验证, 之前缺索引补)
- [[notes/lessons-learned-2026-06-04-23-50]] — Lessons learned 23:50 快照 (3rd 6-4, 含 5 条本轮铁律, 之前缺索引 + 缺 type 一并修)


- [[notes/dspy-self-evolution-2026-06-06]] — **Hermes 3rd 自我进化** (3rd, 21:30, DSPy ChainOfThought → Hindsight mental_model 4903 chars + BootstrapFewShot 5 步核验训练, "实现自我进化" 任务, mental_model `hermes-self-evolution` 自动 reflect 注入未来 session)
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
- [[indexes/knowledge-map]] — 9 主题知识地图(2026-06-04 新)

---

## 写入协议(摘要)

> 完整协议见 [[CLAUDE]]

1. 任何新页:`Grep` 查重 → 满足 2+ 来源门槛 → 创建 → 写 frontmatter 9 字段 → 加 wikilink × 2+ → 更新本文件
2. 任何修改:bump `updated` 日期,标 `contradictions` if conflict
3. 任何归档:移到 `notes/_archive/` 或删除
