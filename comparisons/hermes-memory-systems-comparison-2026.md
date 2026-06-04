---
title: Hermes 最佳记忆系统对比 (2026-06-02)
created: 2026-06-02
updated: 2026-06-02
type: comparison
tags: [tech, memory, hermes, lcm, openviking, mem0, hindsight, comparison]
sources:
  - https://vectorize.io/articles/hermes-agent-memory-explained
  - https://github.com/stephenschoettler/hermes-lcm
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
  - https://hermesatlas.com/lists/best-memory-providers
  - https://www.reddit.com/r/hermesagent/comments/1tms3g6/memory_providers_i_tested_them_all
confidence: high
contested: false
---

# Hermes 最佳记忆系统对比

> Hindsight 卸载后重新评估：Hermes 默认 + LCM + 各 provider 真实能力对比

## Hermes 真实有的 4 层记忆（Hermes 官方定义）

| Layer | 名称 | 实现 | 容量/限制 | 触发 |
|---|---|---|---|---|
| **L1 Prompt** | Hot Memory | `~/.hermes/memories/MEMORY.md` + `USER.md` | 各 1375 字符 | 每个 session 自动注入 |
| **L2 Session** | Cold Recall | `state.db` (SQLite + FTS5) | 跨所有 session | `session_search` 工具主动调 |
| **L3 Skills** | Procedural | `~/.hermes/skills/*.md` | 92+ 页 | 任务完成时自动 nudge |
| **L4 Provider** | External | 8 个 plugin 中选 1 个 | 视 provider 而定 | 可选 |

**LCM 是什么角色？** LCM 是 **context engine 插件**（不是 memory provider）—— 它替换 Hermes 默认的 `ContextCompressor`，提供**无损可展开的摘要 DAG**。**它和上面 4 层是正交关系**。

## 8 个 Provider 真实能力对比

| Provider | 存储 | LongMemEval | 关键能力 | 适合场景 | 缺点 |
|---|---|---|---|---|---|
| **Hindsight** | 本地/云 | **91.4%** (Gemini-3) | reflect + 知识图谱 | 个人偏好/事实 | 需 320MB 磁盘 + 嵌入模型 |
| **OpenViking** | 自托管 | — | 文件系统 + L0/L1/L2 tier | 多模态/文件型记忆 | 25K stars 但用的人少 |
| **Mem0** | 云 | 67.6% | 服务端 LLM 抽取 | 团队/多 Agent | 强依赖云 |
| **Honcho** | 云/自托管 | — | 对话式用户建模 | 关系型 agent | AGPL 开源限制 |
| **Holographic** | 本地 SQLite | — | FTS5 + trust scoring | 轻量本地 | 功能少 |
| **Supermemory** | 云 | — | <300ms recall | 高频查询 | 强依赖云 |
| **RetainDB** | 云 | — | 混合 vector+BM25 | 工业级 | 付费 |
| **ByteRover** | 本地/云 | — | 知识树 | 编码 agent | 强编码导向 |

## LCM vs Memory Provider：正交关系

```
┌─────────────────────────────────────┐
│  Context Engine (LCM / Compressor)  │  ← 单选, 替换默认
│  - L0 Working Memory                │
│  - 长 session 时如何压缩            │
└─────────────────────────────────────┘
              ↓ 压缩产物可查询
┌─────────────────────────────────────┐
│  Memory Provider (8 选 1)            │  ← 单选, 跨 session
│  - L2 长期知识                       │
│  - 用户/事实/偏好                    │
└─────────────────────────────────────┘
```

**它们解决不同问题**：
- LCM 解决：**单 session 超长** 怎么压缩
- Provider 解决：**跨 session 知识** 怎么存

## 你的真实场景分析

| 你每天做的事 | LCM 解决? | Provider 解决? | 关键词够? |
|---|---|---|---|
| 单 session 长对话 (你的 session 通常 50+ 轮) | ✅ | ❌ | — |
| 找旧 session "上次怎么解决 X" | ❌ | ❌ | ✅ session_search |
| 沉淀决策/偏好 | ❌ | ✅ | ❌ 需结构化 |
| "上次类似报错" | ❌ | ✅ Hindsight 优 | ⚠️ 关键词有时漏 |
| 知识图谱可视化 | ❌ | ❌ (用 Obsidian) | — |
| 自动 LLM 合成历史回答 | ❌ | ✅ reflect | ❌ 手动 lcm_expand_query |

## Reddit/HN 社区共识

> **"Mem0 is the best for personal use"** — r/hermesagent 真实评测 (9d ago)

但 vectorize.io（Hindsight 团队）反驳：
- Hindsight 91.4% vs Mem0 67.6% (LongMemEval)
- 唯一有 reflect 操作
- 唯一存结构化知识（不是文本块）

## 诚实评估：Hindsight 到底该不该装

### 装 Hindsight 的核心理由（**强论据**）

1. **91.4% LongMemEval 准确率**（业界最高）
2. **唯一有 reflect** —— 跨记忆 LLM 合成
3. **唯一结构化知识**（实体/关系/事实）
4. Hermes **官方文档列出**为推荐 provider

### 不装的核心理由（**强论据**）

1. 你有 LCM（无损原文可展开）—— 90% 场景够
2. session_search 关键词够用（你日常用得很顺）
3. 1375+1375 字符 prompt memory 是**有意的设计**（保护 prefix cache）
4. Hindsight 320MB 磁盘 + LLM 调用 token 成本
5. Obsidian 已有可视化图谱
6. wiki 92 页 + skill 机制已用得很熟

### 真正决定因素

| 关键问题 | 答案 | 决策 |
|---|---|---|
| 每周"上次类似情况"出现几次？ | 0-1 次 | 不装 |
| | 3+ 次 | 装 |
| 是否需要"新 session 开场自动拉上下文"？ | 否 | 不装 |
| | 是 | 装 |
| 是否接受每月 500k+ tokens LLM 成本？ | 否 | 不装 |
| | 是 | 装 |

## 我的真实判断

**对你（重度 wiki/LCM/用户）**：

**路径 A：不装 provider**（当前状态）
- ✅ 你已有 LCM + wiki + session_search + Obsidian
- ✅ 0 token 成本
- ✅ 0 维护负担
- ⚠️ "上次类似报错" 这种语义查询偶尔不便

**路径 B：装 Hindsight**（建议先小范围试）
- 装但**不**主动化（不注册 cron、不激活看门狗）
- 只在用户明确说"上次..."时手动调
- 观察 1 个月实际使用频率
- 如果 < 1 次/周 → 卸
- 如果 > 3 次/周 → 启用 cron 主动化

**路径 C：装 OpenViking**（如果你想做文件系统记忆）
- 和你 wiki/Obsidian 工作流冲突
- 不推荐

**路径 D：装 Mem0**（社区共识）
- 67.6% 准确率（vs Hindsight 91.4%）
- 强依赖云
- 不推荐

## 最终建议

**当前 Hindsight 已卸的状态是合理的**——零成本 + 你有 LCM 兜底。

如果 1 个月内发现真有"语义查询高频场景"，**重装 Hindsight**（路径 B）。

不要：
- ❌ 重装 Hindsight + 立刻加 cron（重蹈覆辙）
- ❌ 装 OpenViking（和你 workflow 冲突）
- ❌ 装 Mem0（依赖云 + 准确率低）

## 与已有概念的关系

- [[concepts/hermes-workflow]] — 主工作流
- [[notes/lcm-upgrade-v0.12-to-v0.15]] — context engine (v0.14.0, 当前 0.12.0 过时需升级)
- [[concepts/full-stack-ecosystem]] — 8 个 provider 选 1
- [[agent-4-tier-memory-architecture]] — 通用 4 层模型
