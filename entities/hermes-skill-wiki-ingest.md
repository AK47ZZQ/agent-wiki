---
title: Skill — hermes-skill-wiki-ingest
created: 2026-06-04
updated: 2026-06-04
type: entity
tags: [skill, wiki, ingest, knowledge-pipeline]
source: hermes/skills/hermes-skill-wiki-ingest/SKILL.md
confidence: medium
---

# hermes-skill-wiki-ingest

> 知识摄入管道:把外部源(网页/飞书文档/会话)结构化后写入 Obsidian wiki。

## 用途

- 把飞书文档自动 dump 到 `wiki/raw/` 后,提取关键概念/实体
- 抓取网页并按 LLM Wiki 模式组织到 `wiki/concepts/` 或 `entities/`
- 批量处理多个来源,生成新页面 + 自动 index 更新

## 关联

- 上游:飞书消息 / `mcp_tavily_*` / `feishu_doc_*` 工具
- 下游:`hermes-skill-wiki-archive` skill(归档)
- 配套 wiki 文档:[[concepts/full-stack-ecosystem]]
