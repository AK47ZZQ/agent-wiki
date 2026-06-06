---
title: LLM Wiki Pattern — Karpathy 风格 LLM 驱动的互链知识库
created: 2026-06-06
updated: 2026-06-06
type: concept
tags: [llm-wiki, karpathy, knowledge-base, pattern]
source: wiki-second-brain-2026-06
---

# LLM Wiki Pattern — Karpathy 风格 LLM 驱动的互链知识库

> 概念补完 (2026-06-06, 从 reflection 笔记引用反推).
> 前置: [[methods/wiki-as-second-brain]] (wiki 整体定位)

## TL;DR

- **来源**: Andrej Karpathy 公开推崇的 LLM Wiki 模式 (类似 llm-wiki 仓库)
- **核心**: 不用传统标签/分类,而用 LLM 互链 (`[[wikilink]]`) 形成语义图谱
- **特征**:
  - 实体/概念/方法 在 2+ 来源时建页
  - 每页至少 2 条 wikilink 出链 (避免孤岛)
  - frontmatter 9 字段 + provenance markers
  - confidence 单源 = low, 3+ 源 = high
- **Hermes 实践**: 跟 PARA + Zettelkasten 融合, 见 [[methods/wiki-as-second-brain]]
- **对比**: [[concepts/harness-engineering]] (方法论 vs 知识库)

## 1. 3 核心原则

1. **互链 > 分类** — 用 `[[wikilink]]` 形成图谱, 而不是 folder/label 树
2. **2+ 来源 = 建页门槛** — 单源只在 notes/ 写短记录
3. **LLM 主动探勘** — `ai-harness-exploration` skill 主动 grep + 写

## 2. 跟传统 wiki 区别

| 维度 | 传统 wiki | LLM Wiki Pattern |
|---|---|---|
| 编辑者 | 人类 | 人类 + LLM 协作 |
| 链接 | MD 链接 | wikilink (语义图谱) |
| 分类 | folder 树 | tags + wikilink |
| 检索 | 全文搜索 | LLM 语义召回 |
| 质量 | 人工 review | `check-wiki-quality.py` 自检 |

## 3. Hermes 实践

- [[methods/wiki-as-second-brain]] — wiki 当第二大脑
- [[methods/wiki-curation-guide]] — 策展指南
- [[methods/curation-checklist]] — 自检清单
- `scripts/check-wiki-quality.py` — 5 项自检

## 4. 关联文档

- [[methods/wiki-as-second-brain]] — 整体定位 (实际是 methods/ 目录)
- [[concepts/harness-engineering]] — 方法论
- [[protocols/per-project-claude-md-template]] — per-project 模板
- [[concepts/context-engineering]] — 上下文工程

## 5. 自检

- [x] 6 字段齐
- [x] 至少 2 wikilink 出链 (实际 5+)
- [x] tag: llm-wiki + karpathy + knowledge-base + pattern
- [x] source: wiki-second-brain-2026-06
