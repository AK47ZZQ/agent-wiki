---
title: wondelai/skills — 跨平台 Agent 技能库
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [tech, hermes, skills, agentskills.io, cross-platform]
source: https://github.com/wondelai/skills
confidence: high
---

# wondelai/skills — 跨平台 Agent 技能库

> **仓库**: [wondelai/skills](https://github.com/wondelai/skills) (380+ stars)
> **作者**: [wondelai](https://github.com/wondelai)
> **成熟度**: production — 持续维护、社区最推荐的 Hermes 第一步

## 定位

面向 Claude Code 和 [agentskills.io](https://agentskills.io) 兼容平台的**跨平台 agent 技能库**。基于 agentskills.io 开放标准构建，可跨 Hermes、Claude Code、Cursor、Codex 等 agent 平台使用。

是 Awesome Hermes Agent 清单中"从哪里开始"三步路径的第 2 步——在安装 Hermes 之后、配置 GUI 之前，社区推荐先安装此技能库作为通用技能底座。

## 核心价值

1. **跨平台兼容**：同一套技能可在多个 agent 平台使用，不绑定特定 agent
2. **开放标准**：基于 agentskills.io 规范，技能格式标准化
3. **社区维护**：380+ stars，持续维护
4. **生产就绪**：成熟度标签为 production，可用于正式工作流

## 在 Hermes 生态中的位置

```
Hermes 官方核心 (NousResearch/hermes-agent)
    │
    ├─ agentskills.io 标准 (Skills Hub)
    │       │
    │       └─ wondelai/skills ─── 跨平台通用技能底座 ★
    │
    ├─ hermes-workspace / mission-control (GUI/编排)
    └─ Hindsight / Honcho (记忆层)
```

在进阶蓝图中，"工作区优先"方案推荐 `hermes-workspace + wondelai/skills` 作为个人开发和日常 agent 协作的标准组合。

## 关联页面

- [[concepts/awesome-hermes-agent-ecosystem-2026]] — Awesome 清单全景，本文在其中
- [[entities/hermes-workspace]] — 推荐搭配的 GUI 工作区
- [[entities/hermes-skill-ai-harness-exploration]] — 本 wiki 中对应的 Hermes 探勘技能
- [[entities/hermes-skill-hermes-workflow]] — 本 wiki 中的 Hermes 工作流执行技能
