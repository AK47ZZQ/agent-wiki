---
title: Agent 四层记忆架构（4-Tier Memory Model）
created: 2026-06-02
updated: 2026-06-02
type: concept
tags: [tech, architecture, memory, agent, hindsight, lcm]
sources:
  - https://www.cloudidr.com/blog/ai-memory-architecture
  - https://hindsight.vectorize.io/guides/2026/04/23/guide-short-term-vs-long-term-memory-for-ai-agents
  - https://mem0.ai/blog/short-term-vs-long-term-memory-in-ai
  - https://blog.devgenius.io/ai-agent-memory-systems-in-2026-mem0-zep-hindsight-memvid-and-everything-in-between-compared-96e35b818da8
  - https://www.cnblogs.com/deephub/p/19740751
confidence: high
contested: false
---

# Agent 四层记忆架构

## 核心定义

任何 LLM Agent 的记忆系统**不应该是一个大杂烩**，而应该分为**4 个明确分层的 Tier**，每层有独立的存储、生命周期和查询路径。混淆层级会导致：token 浪费、查询不准、跨 session 丢失。

## 4-Tier 模型（业界共识）

| Tier | 名称 | 存储位置 | 生命周期 | 谁负责查询 | 经济成本 |
|---|---|---|---|---|---|
| **L0** | Working Memory | 原生 prompt 上下文 | 1 个 turn | Agent 直接读 | 最高（每 token 都花钱） |
| **L1** | Short-term | 摘要 DAG / session-bound DB | 1 个 session（自动清） | 上下文压缩引擎 | 中（摘要时调 LLM） |
| **L2** | Long-term | 知识图谱 + 向量索引 | 跨 session 永久 | LLM 合成查询 | 中（按需 recall） |
| **L3** | Hard-coded Facts | prompt 字符串硬塞 | 进程内常量 | 每次都注入 | 低（但吃 token） |

## 各层职责边界

### L0 Working Memory（原生上下文）

- **是什么**：当前 message list 里所有 user/assistant/tool 消息
- **何时用**：当前对话的"工作台"
- **何时失效**：超出 context_length（512K for M3）
- **不要做**：把"历史结论"塞 L0（应该 promote 到 L2）

### L1 Short-term（短期压缩）

- **是什么**：当 L0 接近 50% 时，**把早期消息压缩成摘要**，保留近 20 轮原文
- **存储**：摘要节点（带 token 数 + 原始消息引用）
- **何时用**：单 session 长对话、深度调试、复杂多步任务
- **何时失效**：session 结束（自动清理）
- **风险**：摘要失真（信息丢失）、token 双计入（摘要+原文）

### L2 Long-term（长期知识）

- **是什么**：跨 session 持久化的事实/偏好/教训
- **存储**：知识图谱（实体-关系-事实三元组）+ 向量索引
- **何时用**：新 session 开头拉上下文、用户问"上次我们..."、自动 enrich 当前对话
- **何时失效**：几乎不过期，但可手动删低分记忆
- **关键约束**：**不替代 L0**——L2 是"知识库"，L0 才是"工作台"

### L3 Hard-coded Facts（硬塞事实）

- **是什么**：高频必用的关键信息（路径、API、用户 ID），直接拼到 system prompt
- **存储**：~1500 字符字符串
- **何时用**：30 秒内必查的事实
- **何时失效**：信息变更时手动更新
- **限制**：容量小，不能超过 2-3K 字符

## 业界来源对照

| 来源 | 命名 | 4-Tier 映射 |
|---|---|---|
| cloudidr.com "The Memory Architecture of AI" | Working / Short-term / Long-term / Infinite | L0 / L1 / L2 / (无 L3) |
| Hindsight 官方文档 | Short-term context / Long-term memory | L0+L1 合并 / L2 |
| mem0.ai | Ephemeral context / Persistent index | L0 / L2 |
| devgenius.io 2026 综述 | 4-store (Hindsight 实际就是 4-store 设计) | L0 / L1 / L2 / 元数据 |
| cnblogs "理解 Agent 记忆" | 短期 / 长期 + 外部存储 | L0+L1 / L2 |

**共识**：**Working/Short-term/Long-term 三层必须有**。**分歧**：是否需要独立的"硬塞层"（L3）——这是工程妥协，不是逻辑必需。

## 与已有概念的关系

- [[concepts/hermes-workflow]] — Hermes 的工作流大量依赖 L1（LCM）和 L2（默认走 Honcho/Mem0/Hindsight）
- `install-hindsight-as-hermes-memory` skill — Hindsight 安装与配置（已经在 L2 落地）
- [[concepts/hermes-kanban]] — Workers 也使用 L1（context.engine: lcm）做长任务压缩

## 实战对应表（你的 Hermes 系统）

| Tier | 你当前的实现 | 状态 | 调整建议 |
|---|---|---|---|
| L0 | 原生 messages | ✅ | 保持 |
| L1 | `context.engine: lcm` + `compression.threshold: 50%` | ✅ | 保持（Kanban workers 需要） |
| L2 | `memory.provider: hindsight` + pg0 | ✅ 已部署 | 加"主动化"机制（cron + 开场 reflect） |
| L3 | `memory_char_limit: 2200` + `user_char_limit: 1375` | ✅ | 保持 |

## 关键洞察

1. **Hindsight 不替代 LCM**——它们各管一层。Hindsight 是 L2，LCM 是 L1。
2. **关掉 LCM 不会解放 token**——压缩是 Hermes 自己的事（走 deepseek-v4-flash），LCM 只负责"用什么方式"组织压缩产物
3. **Hindsight "主动拥抱" = 主动喂数据 + 主动拉数据**——光打开 provider 没意义，要配 cron + 钩子
4. **L3 的存在是因为 LLM context 贵**——理论上 L2 也能查任何事实，但每次都查就破产了，所以高频事实硬塞

## 陷阱

- **不要让 L2 替代 L0**：Hindsight reflect 答案可以注入 L0，但**不能**作为"上下文"——它是"知识"
- **不要让 L1 写 L2**：LCM 摘要是临时的，不应该 retain 到 Hindsight（除非显式 promote）
- **不要让 L3 装太多**：> 5K 字符就开始抢 L0 空间，得不偿失
