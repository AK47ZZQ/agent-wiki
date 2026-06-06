---
title: Hindsight 4 维检索 (完整版) - 实测全功能
created: 2026-06-03
updated: 2026-06-03
type: method
tags: [hindsight, retrieval, 4d, types, tags, observation, world, experience]
sources:
  - https://github.com/vectorize-io/hindsight
  - local: http://localhost:8888/docs
  - local: C:\Python314\test_hindsight_full.py
confidence: high
source: hindsight-deployment-2026-06
---

# Hindsight 4 维检索 (完整版) - 实测全功能

> 2026-06-03 实测 Hindsight v0.6.1 完整检索能力 —— **3 types + 4 维检索策略 + 完整 metadata**

## 3 Types (不是 4)

**官方说 4 logical networks** (world/experience/entity/belief)，**但 v0.6.1 实际暴露 3 types**：

| Type | 含义 | 实测数量 |
|---|---|---|
| **world** | 客观事实（用户偏好/部署/事实） | 5 |
| **experience** | 主观经历（用户操作/对话记录） | 8 |
| **observation** | 观察/衍生（LLM 抽取的元数据） | 主要部分 |
| ~~entity~~ | ~~实体摘要~~ | 实际是 metadata 而非 type |
| ~~belief~~ | ~~演化信念~~ | 实际是 metadata 而非 type |

## 4 维检索策略

Hindsight 实际用 **4 维度并行检索** + **cross-encoder reranker**：

| 维度 | 实现 | 配置 |
|---|---|---|
| **语义检索** | bge-small-en-v1.5 (384维) | `HINDSIGHT_API_EMBEDDINGS_LOCAL_MODEL` |
| **关键词检索** | PG FTS5 | 内置 |
| **图谱检索** | entities[] 字段 | 实体抽取 |
| **时间检索** | `query_timestamp` 参数 | ISO 8601 |

**5th: cross-encoder reranker** (ms-marco-MiniLM-L-6-v2) —— **二次重排**

## Recall API 完整参数

```python
POST /v1/default/banks/{bank}/memories/recall
{
    "query": "...",                    # 必填, 限 500 tokens
    "types": ["world"],                 # 可选: world/experience/observation
    "budget": "low|mid|high",           # 默认 mid
    "max_tokens": 4096,                 # 默认 4096
    "query_timestamp": "2026-...",      # 可选: ISO 8601
    "tags": ["decision"],               # 可选
    "tags_match": "any|all|...",        # 默认 any
    "include": {...},                   # 可选: entities/observations
    "trace": false                      # 可选: debug
}
```

## 完整 Memory Unit 字段

实测从 `GET /v1/default/banks/{bank}/memories/{id}` 拿到的字段：

```json
{
    "id": "747ab678-7e54-44bc-a12b-3464cd86f8cb",
    "text": "Hindsight 支持 update_mode=append 模式, 用于追加内容到现有记忆",
    "context": "",
    "date": "2026-06-03T14:44:57.482913+00:00",
    "type": "observation",
    "mentioned_at": "2026-06-03T14:44:57.482913+00:00",
    "occurred_start": "2026-06-03T14:44:57.482913+00:00",
    "occurred_end": "2026-06-03T14:44:57.482913+00:00",
    "entities": ["hybrid mode", "hindsight"]
}
```

| 字段 | 含义 | 关键用途 |
|---|---|---|
| `id` | UUID | 唯一标识 |
| `text` | LLM 抽取的 fact | 搜索匹配用 |
| `context` | 用户原始 context | 追溯 |
| `date` / `mentioned_at` | retain 时间 | 时间过滤 |
| `occurred_start/end` | 真实事件时间 | 事件追溯 |
| `type` | world/experience/observation | 分类 |
| `entities[]` | 提取的实体 | 图检索 |

## Bank Metadata

```bash
GET /v1/default/banks/{bank}
{
    "bank_id": "hermes",
    "name": "hermes",
    "disposition": {
        "skepticism": 3,    // 怀疑度
        "literalism": 3,    // 字面度
        "empathy": 3        // 共情度
    },
    "mission": "",        // 银行使命
    "created_at": "...",
    "fact_count": 53,
    "last_document_at": "..."
}
```

**disposition 是什么？** —— 推测是 Hindsight reflect 的"性格参数"，控制合成答案的语气（官方未明确文档）

## Document API

```bash
GET /v1/default/banks/{bank}/documents/{doc_id}
{
    "id": "doc-2026-06-03-append",
    "bank_id": "hermes",
    "original_text": "Append test: ...",
    "content_hash": "7aeed58a...",
    "created_at": "..."
}
```

**应用场景**：
- 关联多次 retain 到同一 document（multi-retain 模式）
- 用 `--doc-id` retain + 后续 GET document 查整体内容
- update document（retain 同 doc_id 替换）

## Timeseries Stats

```bash
GET /v1/default/banks/{bank}/stats/memories-timeseries
# 返回 7 天按天分桶, 含 world/experience/observation 计数
```

**应用**：dashboard 显示记忆增长曲线

## 4 维 vs 实测 3 types 关系

| 4 logical networks (论文) | 3 types (实际 API) | 关系 |
|---|---|---|
| World facts | `type=world` | 直接对应 |
| Agent experiences | `type=experience` | 直接对应 |
| Entity summaries | `entities[]` (不是 type) | metadata 字段 |
| Evolving beliefs | `disposition` (bank-level) | 性格参数 |

**修正之前错误**：4 logical networks 实际是 **3 types + 1 metadata (entities) + 1 bank-level (disposition)** —— 不是 4 个独立 types

## 实战建议

| 场景 | 推荐配置 |
|---|---|
| 找客观事实 | `types=["world"]` |
| 找用户行为 | `types=["experience"]` |
| 找 LLM 推断/标签 | `types=["observation"]` |
| 时间窗口过滤 | `query_timestamp` |
| 按决策/事实标签 | `tags=["decision"]` |
| 复杂场景 | types + tags + timestamp 三者结合 |

## 关键陷阱

1. ❌ **types 过滤会减少 recall** —— 不到 1/3 总数
2. ❌ **query_timestamp 必须是未来时间** 才能查"之前"的内容
3. ⚠️ **budget 越高越贵**（low/mid/high 检索深度递增）
4. ⚠️ **max_tokens 限制输出** —— 不是 limit 总数，是 limit 输出字符
5. ⚠️ **tags 区分大小写** —— 之前用 "Decision" 不匹配

## 验证清单

- [x] types 过滤工作 (world=5, experience=8)
- [x] query_timestamp 工作
- [x] tags 过滤工作
- [x] update_mode='append' 工作
- [x] Document API 工作 (get 完整内容)
- [x] Memory unit 完整字段 (entities/mentioned_at/occurred_*)
- [x] Bank metadata (disposition/mission/fact_count)
- [x] Timeseries stats

## 关联文档

- [[concepts/hindsight-in-hermes-ecosystem-2026]]
- [[methods/install-hindsight-native-hermes-method]]
- `hindsight-handoff` skill
- [[notes/hindsight-local-deployment-windows-2026]]
- (原始记录已精简移除)
