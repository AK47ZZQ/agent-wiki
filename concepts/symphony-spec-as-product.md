---
title: Symphony Spec-as-Product
created: 2026-06-02
updated: 2026-06-02
type: concept
tags: [symphony, spec-as-product, openai, codex-orchestration]
confidence: high
source: works/openai-codex-symphony-translation.md
---

# Symphony Spec-as-Product

> OpenAI 2026-04-27 发布的开源 Codex 编排规约。核心思想：**Issue tracker 变成控制面，Spec 变成可交付产品。**

## 关键数据

| 指标 | 数据 |
|:----|:----|
| 团队 | Kotliarskyi / Zhu / Brock |
| 合并 PR 增量 | **+500%**（前三周） |
| 核心创新 | `SPEC.md` + `WORKFLOW.md` + 多语言验证 |
| 交互模式转变 | 从交互式指导 → 目标设定 |

## 核心架构

```
Linear Issue (控制面)
  → 每个开放任务获得独立 Agent 工作空间
    → Agent 读取 SPEC.md（目标/约束/边界）
      → Agent 读取 WORKFLOW.md（流程/步骤）
        → Agent 生成代码
          → CI/lint/测试 背压门控
            → 人类审核 → 合并
```

## SPEC.md — 约束即产品

当代码几乎免费时，可交付产品从"代码+文档"反转为**"规约即产品"**。

| 传统 | Symphony |
|:----|:--------|
| 工程师写代码 | 工程师写约束系统 |
| 交付 = 代码 | 交付 = SPEC.md |
| 另一种实现用另一种语言重写 | 另一种实现读取同一 SPEC 生成 |

多语言验证：在 Elixir/TypeScript/Go/Rust/Java/Python 中实现同一 SPEC → 实现差异暴露规约歧义。这是"压力测试"。

## WORKFLOW.md — 使隐式显式

将人类隐式工作流（"先做 A，然后 B，最后 C"）从大脑中提取为可审计的文本文件。Orchestrator 确保每一步都执行。

## 与 [[concepts/harness-engineering-deep-study]] 的关系

| Symphony 概念 | Harness Engineering 对应 |
|:-------------|:------------------------|
| SPEC.md | 最高层 Guide（前馈） |
| WORKFLOW.md | 过程性 Guide |
| 多语言验证 | 计算性 Sensor |
| Issue 作为控制面 | 仓库即记录系统 |

## 关键见解

- **交互式指导 → 目标设定**：不再告诉 Agent "怎么做"，而是告诉它"做成什么样"
- **吞吐量从 PR 级跃升到 Issue 级**：一个 ticket 可以自动产生 0..N 个 PR
- **技术栈分化**：当代码几乎免费时，工程师根据问题域适配度选择语言，而非技术栈趋同
