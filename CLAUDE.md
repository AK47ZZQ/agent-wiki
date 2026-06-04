# Wiki Schema — CLAUDE.md

## Domain
Hermes Agent 使用日志 + Obsidian 个人知识库

## Directory Layout
```
wiki/
├── raw/              # Layer 1: 源文件（Agent 只读，永不修改）
│   ├── tech/         # 技术文章、论文、教程
│   ├── work/         # 工作相关
│   ├── reading/      # 阅读笔记
│   └── assets/       # 图片附件
├── agents/           # 多 Agent 注册表 (新)
├── scratchpad/       # 短期共享工作记忆 (新)
├── tasks/            # 跨 Agent 任务板 (新)
├── protocols/        # 协作协议定义 (新)
├── concepts/         # 概念/主题页（跨源综合）
├── entities/         # 人物/工具/框架/模型
├── methods/          # 方法论：可复用流程、最佳实践、反模式
├── comparisons/      # 对比分析（table format 优先）
├── notes/            # 短记录/部署日志/问题排查
├── references/       # 长引用（命令大全等）
├── .obsidian/        # Obsidian 配置（不修改）
├── index.md          # 主索引（前 50 条目/section，超则建 _meta/topic-map.md）
├── log.md            # 操作日志（超 500 条则 rotate 为 log-YYYY.md）
├── CLAUDE.md         # Layer 3: 本 Schema + 5 层协议
└── README.md
```

> **2026-06-04 重构备注**: 顶层 6 类别目录已稳定(concepts/entities/methods/comparisons/notes/indexes)。
> 2026-06-04 新增 4 类"多 Agent 第二大脑"节点:agents/ scratchpad/ tasks/ protocols/(详见第 5 层)。
> 历史嵌套 `wiki/wiki/` 已于 2026-06-04 平铺。

## Conventions
- 文件名: 小写 + 连字符, 如 `transformer-architecture.md`
- 每个 wiki 页面必须有 YAML frontmatter
- 使用 `wikilink` 链接其他页面（**每页至少 2 条出链**）
- 更新页面时 bump `updated` 日期
- 新页面必须加入 `index.md`
- 每条操作必须记录到 `log.md`
- **Provenance markers**: 3+ 来源的页面，在段尾用 `^[raw/articles/source.md]` 标注来源
- **Confidence**: 单源/快变动话题建议 `medium` 或 `low`，多源验证后才设 `high`

## Page Thresholds
- **创建页面**: 实体/概念出现在 2+ 来源中，或对单个来源至关重要
- **追加到已有页**: 来源提及已覆盖的内容时
- **不要创建**: 顺带提及、无关细节、域外内容
- **拆分**: 超 200 行时拆分子话题，加交叉链接
- **归档**: 完全被取代时移到 `_archive/`，从 index 移除

## Frontmatter 模板
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | summary | method | comparison | analysis
tags: [from taxonomy]
source: raw/xxx.md
confidence: high | medium | low
contested: true                    # 有争议的内容
contradictions: [other-page-slug]  # 冲突页面
---
```

### raw/ Frontmatter（用于源文件）
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body below frontmatter>
---
```

## Tag Taxonomy
- tech: architecture, tool, framework, model, protocol
- workflow: automation, integration, pipeline, cron, ingest
- method: best-practice, pattern, workflow, convention
- meta: comparison, timeline, decision, note, query
- quality: confidence, contested, provenance, stale

## 更新策略
- 新信息与已有内容冲突时：标注两个立场 + 日期 + 来源
- 在 frontmatter 标记 `contradictions: [page-name]`
- 不在 `raw/` 中修改源文件——修正写在 wiki 页面中

---

## 第 4 层:Agent 使用协议 (2026-06-04 制定)

> **定位**: 知识库作为 Agent **外接大脑**的运行规则，所有 Agent 行为需遵守。
> **核心原则 (4 条)**: **先查后答 / 边做边记 / 拒绝孤岛 / 留下日志**

### 1. 读协议 (Read Protocol)

#### 1.1 何时自动查询 (强制触发)

以下场景**必须**先查知识库再回答，不允许凭印象作答：

| 场景 | 触发词 / 信号 | 默认动作 |
|:----|:-------------|:--------|
| **已索引实体** | Hermes / Hindsight / Harness / Codex / LCM / L0-L3 / P0-P4 / MCP / Spec-as-Product / Symphony / Ralph Loop | `query_knowledge_base` |
| **历史上下文** | "我之前..." / "上次..." / "我们做过..." / "按照惯例..." | `search_knowledge_base` |
| **任务启动** | 新 session 第一个任务涉及已有页面覆盖的话题 | `Read` 该页 frontmatter 判断相关度 |
| **歧义消除** | 用户指令模糊,可能命中多个知识 | `Grep` 关键词定位 |
| **方法论引用** | 提到 best practice / pattern / convention | `Read` `wiki/methods/` 下的相关页 |

#### 1.2 双通道选择 (MCP 检索 vs 直读)

| 场景 | 通道 | 理由 |
|:----|:-----|:----|
| 开放性查询 (什么/怎么/为什么) | **`query_knowledge_base`** | 跨页综合，带 LLM 总结 |
| 跨页扫词 (找特定 API/参数) | **`search_knowledge_base`** | 纯检索，无 LLM 开销 |
| 已知具体页名 | **`Read` 精确读** | 零开销，直接拿内容 |
| 跨页找特定模式 | **`Grep` 关键词** | 例：找所有 `memory_mode` 出现处 |
| 跟随 wikilink 跳读 | **`Read` 链接目标** | 深度 ≤ 2 跳，避免无限递归 |

**通道优先级 (默认顺序)**：
1. `query_knowledge_base` (MCP, 开放查询)
2. `search_knowledge_base` (MCP, 纯检索)
3. `index.md` 浏览定位
4. `Grep` 关键词精确匹配
5. `Read` 精读具体页

#### 1.3 读取深度 (Token 预算)

```
1. 先读 frontmatter (10-20 行) → 判断 relevance
2. 再读主体相关 section → 不全量通读
3. 跟随 wikilink → 深度 ≤ 2 跳
4. 不要一次性 Read 25 页 index 全表
5. 复杂任务拆子查询, 每次 ≤ 5 页
```

#### 1.4 读取结果处理

- ✅ **完全命中** → 继续任务，引用 `[[wikilink]]` 作为依据
- ⚠️ **部分命中** → 补充外部检索，标注"知识库未覆盖 X"
- ❌ **未命中** → 在回复中明确"知识库无相关记录"，**严禁编造**

---

### 2. 写协议 (Write Protocol)

#### 2.1 何时能写 (允许场景)

| 场景 | 前置条件 | 写入位置 |
|:----|:---------|:--------|
| 用户明确要求 | "记一下" / "补充" / "保存" / "归档" | 按主题分类 |
| Session 结束洞察 | 用户说"总结一下今天的发现" | `wiki/notes/` |
| 新概念 / 新实体 | 满足"2+ 来源"或"对单源至关重要" | `wiki/concepts/` 或 `entities/` |
| 矛盾检测 | 发现新信息与已存内容冲突 | 标 `contested` + 写两侧 |
| 过期检测 | 页面 `updated` > 6 月 | 重读后 bump `updated` |

#### 2.2 写入位置规则 (强约束)

| 内容类型 | 目录 | 命名约定 |
|:---------|:-----|:--------|
| 概念 / 主题 | `wiki/concepts/` | 小写-连字符 |
| 实体 (工具/框架/模型) | `wiki/entities/` | 实体原名 |
| 可复用方法 | `wiki/methods/` | 动作-对象 |
| 对比分析 | `wiki/comparisons/` | 主题-comparison-年份 |
| 短记录 / 部署日志 | `wiki/notes/` | 事件简述 |
| 源文件摘要 | `wiki/summaries/` | 源文件名 (1:1) |
| 🚫 **绝不允许** | `raw/` (永远只读) | — |
| 🚫 **绝不允许** | 根目录 `concepts/`, `entities/` (已废弃) | — |

#### 2.3 Frontmatter 强制要求

新页面 / 重大修改必须满足：

- ✅ **9 字段齐全**: `title / created / updated / type / tags / source / confidence / [contested] / [contradictions]`
- ✅ **至少 2 条 wikilink 出链** (避免孤岛)
- ✅ `source` 指向 `raw/xxx` 或权威 URL
- ✅ `confidence`: 单源/快变动 → `medium`/`low`；3+ 源验证 → `high`
- ✅ `tags` 从 Tag Taxonomy 选，**禁止生造**

#### 2.4 必须同步更新 (4 件套)

每次写入必须：

1. **`index.md`** 增条目 (按分类加入链接)
2. **`log.md`** 增一行 (格式: `## [YYYY-MM-DD] action | 描述`)
3. 旧页面的 `updated` bump (如果是修正 / 追加)
4. 矛盾时，在双方 frontmatter 标 `contradictions: [slug]`

#### 2.5 不要写 (反模式清单)

- ❌ 重复内容 (先 `Grep` 查重)
- ❌ 纯 session 日志 (归档到 `wiki/_archive/sessions/`)
- ❌ 没有 wikilink 的孤岛
- ❌ 改写 `raw/` 源文件
- ❌ 一次性写 5+ 页大改 (分批，每批更新 index)
- ❌ 创建 < 10 行的薄页面 (合并到上级概念)
- ❌ 创建重复 concept (查 `wiki/concepts/` 已存列表)

---

### 3. 决策树 (Decision Tree)

```
用户提问 / 启动任务
   │
   ├─ 关键词命中知识库索引? (Hermes/Hindsight/Harness/Codex/LCM/P0-P4/MCP/...)
   │   ├─ YES → query_knowledge_base 检索
   │   │         ├─ 命中 → Read 精读 → 回答 + 引用 [[wikilink]]
   │   │         └─ 未命中 → Grep 关键词 → 仍未命中 → 外部检索 + 标注"未覆盖"
   │   │
   │   └─ NO → 是否需要历史上下文?
   │           ├─ YES → search_knowledge_base
   │           └─ NO  → 直接回答
   │
用户要求"记一下/补充/归档"
   │
   ├─ Grep 查重 → 命中已有页?
   │   ├─ YES → Edit 追加 → bump updated → 简短 log
   │   └─ NO  → 满足"2+ 来源"门槛?
   │           ├─ YES → 新建页 → 写 frontmatter → 更新 index + log
   │           └─ NO  → 写 notes/ (短记录) → 更新 index + log
   │
Session 结束
   │
   └─ 有新洞察? → 总结到 notes/ → log
```

---

### 4. 反模式 (Anti-Patterns)

| 反模式 | 后果 | 正确做法 |
|:-------|:-----|:---------|
| 一次性 Read 25 页 index | 浪费 token, 大量无关内容 | 按需精确读 + wikilink 跳读 |
| 写入 `raw/` | 破坏源文件不可变性 | 只在 `wiki/` 写, 修正写在 wiki 页 |
| 创建无 wikilink 孤岛 | 知识碎片化,无法形成网络 | 至少 2 条出链 |
| 跳过 `log.md` | 失去审计轨迹 | 每操作必记 |
| 单源就建 concept | 噪声, 概念未成熟 | 等 2+ 来源或写到 notes/ |
| 不更新 `updated` 日期 | 时间线混乱 | 修改即 bump |
| 改写旧内容而非追加 | 失去历史 | 追加 + `contradictions` 标注 |
| 用 MD 链接 `[](path)` 而非 wikilink | 失去 Obsidian 图谱优势 | 用 `[[wikilink]]` |
| 凭印象答索引实体 | 与知识库冲突, 用户体感差 | 强制先查 |

---

### 5. 协议例外 (Edge Cases)

- **用户明确说"不要查"** → 跳过读协议，直接答
- **用户明确说"全部重写"** → 跳过查重，但仍要更新 index/log
- **紧急修复 (debug)** → 写到 `wiki/notes/`，标注 `stale` tag，事后回填
- **实验性新方法** → 写到 `wiki/methods/`，标 `confidence: low`，验证后再升级
- **Token 预算紧张** → 优先 `search_knowledge_base` (纯检索无 LLM) 而非 `query_knowledge_base`

---

### 6. 协议自检清单 (Agent 每次操作前自问)

```
[ ] 我需要先查知识库吗? (1.1 触发场景)
[ ] 我选了正确的通道吗? (1.2 优先级)
[ ] 我读得够深但不过度吗? (1.3 token 预算)
[ ] 我要写新页前查重了吗? (2.5 反模式)
[ ] frontmatter 9 字段齐了吗? (2.3)
[ ] 至少 2 条 wikilink 出链了吗? (2.3)
[ ] index.md 和 log.md 更新了吗? (2.4)
[ ] updated 日期 bump 了吗? (2.4)

---

## 第 5 层:多 Agent 协作 (2026-06-04 制定)

> **定位**: 把 wiki 从"个人知识库"升级为"多 Agent 共享第二大脑"。
> **核心思想**: 不用外部 runtime,只用文件 + frontmatter 字段做协调。
> **详细协议** 见 [[protocols/multi-agent-detail]](5.1-5.6 全展开)。
> **总览**:4 类节点(agents/scratchpad/tasks/protocols)+ 6 通信原语 + 3 硬规则。

