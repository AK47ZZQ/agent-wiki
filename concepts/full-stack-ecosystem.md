---
title: Full Stack Ecosystem
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [tech, ecosystem, model, tool, ai-stack]
confidence: medium
related:
  - concepts/mcp-ecosystem-2026.md
  - concepts/harness-engineering-deep-study.md
---

# Full Stack Ecosystem

> AI/LLM 全栈技术地图，整合 14 个核心节点。
> 本页合并了 14 个原本只有一句话描述的薄 concept 页（2026-06-04 整理）。

## 14 个核心节点

| 节点 | 类型 | 简述 | 详细页 |
|:----|:-----|:-----|:-------|
| **Anthropic** | 公司 | Claude 模型家族 | — |
| **Claude** | 模型 | Anthropic LLM, API + Claude Code CLI | [[concepts/harness-engineering-deep-study]] |
| **ComfyUI** | 工具 | 节点式 Stable Diffusion 图像生成工作流 | — |
| **DeepSeek** | 公司/模型 | V3 / R1 / V4 Flash | — |
| **Docker** | 工具 | 容器运行时,用于打包部署 | — |
| **DSPy** | 框架 | 声明式 LM 编程框架,优化 prompt + pipeline | — |
| **FLUX** | 模型 | Black Forest Labs 图像生成模型 | — |
| **GitHub** | 平台 | 代码托管 + PR + CI/CD + Actions | — |
| **Grok** | 模型 | xAI 的 LLM,集成 X/Twitter | — |
| **LLM** | 概念 | 大语言模型,AI 助手基础 | — |
| **MCP** | 协议 | Model Context Protocol,LLM 工具集成标准 | [[concepts/mcp-ecosystem-2026]] |
| **Obsidian** | 工具 | Markdown 知识库 + Graph View + Wikilinks | [[entities/tool-cli-anything-obsidian]] |
| **OpenAI** | 公司 | GPT / DALL-E / Whisper | [[entities/codex]] |
| **Python** | 语言 | 通用 AI/ML 编程语言 | — |

## 节点间关系图

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│Anthropic │  │ OpenAI   │  │ DeepSeek │  ← 模型/公司
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │ Claude      │ Codex       │ V4 Flash
     ▼             ▼             ▼
┌─────────────────────────────────────┐
│  LLM 层                             │
└──────────────┬──────────────────────┘
               │ 通过 MCP 协议集成
               ▼
┌──────────────────────────────────────┐
│  工具层: GitHub, Docker, Obsidian,   │
│  ComfyUI, FLUX, DSPy, Python, Grok   │
└──────────────────────────────────────┘
```

## 关联页面

- [[concepts/mcp-ecosystem-2026]] — MCP 生态深度研究（15,930+ servers / 安全分析）
- [[concepts/harness-engineering-deep-study]] — AI 编码时代工程约束
- [[concepts/cli-anything]] — Agent-native CLI 转换方法论
