---
title: Hindsight Memory Modes Guide
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [hindsight, memory, modes, retrieval]
sources:
  - https://hindsight.vectorize.io/
  - notes/hindsight-semantic-only-mode-2026
confidence: medium
---

# Hindsight Memory Modes Guide

> Hindsight 的 memory mode 选型指南。**5 种 mode**(3 已知 + 1 TBD + 1 新装的 semantic-only)。

## 核心 modes

| Mode | 来源 | 含义 | 备注 |
|---|---|---|---|
| `world` | Hindsight 默认 | 事实/世界知识 | 客观事实库 |
| `agent` | Hindsight | 代理执行上下文 | 主观经验 |
| `user` | Hindsight | 用户偏好/历史 | 跨 session 记忆 |
| `semantic-only` | **2026-06-04 新装** | **仅语义检索**(无 auto-recall / 无显式工具) | 详见 [[notes/hindsight-semantic-only-mode-2026]] |
| (其他 TBD) | — | 调研中 | 之前的第 4 个空位 |

**重要区分**:`semantic-only` **不是** Hermes 的 `hybrid` `context` `tools` 中的任何一个。
那是 [[methods/install-hindsight-native-hermes-method|memory_mode 字段]] 的 3 个值,而 `semantic-only` 是
Hindsight 自身的 mode(独立于 Hermes prefetch 层)。

## 当前 Hermes 集成

参见 [[concepts/hindsight-in-hermes-ecosystem-2026]]。

## 5 mode 选型决策树

```
你的需求是什么?
├─ 想要 auto-recall + 显式工具 → hybrid (Hermes memory_mode)
├─ 想要 auto-recall, 隐藏工具 → context (Hermes memory_mode)
├─ 想要显式工具, 0 自动 → tools (Hermes memory_mode)
├─ 只要语义检索, 啥都不要 → semantic-only (Hindsight 自身, 2026-06-04 新)
└─ (其他) → 等调研
```

## 关联文档

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 在 Hermes 生态定位
- [[methods/install-hindsight-native-hermes-method]] — 安装方法(3 种 memory_mode)
- [[notes/hindsight-semantic-only-mode-2026]] — semantic-only 模式详细说明(2026-06-04 新)
- [[comparisons/hindsight-automation-patterns-2026]] — 4 种自动化模式(不同维度, 不要混淆)
