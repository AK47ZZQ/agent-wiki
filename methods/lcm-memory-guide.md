---
title: LCM 内存管理教程
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, lcm, memory, compression, handoff]
sources: [concepts/agent-4-tier-memory-architecture, AGENTS]
---

# LCM 内存管理教程

> LCM (Long Context Manager) 是 Hermes 的 L1 短时记忆引擎 — 上下文压缩 + 摘要节点 + 跨 session 引用。

## TL;DR

- **8 DAG 节点类型**(summary / raw / externalized)
- **压缩触发** = token 阈值 / 时间窗 / 显式调用
- **5 工具** = `lcm_grep` / `lcm_load_session` / `lcm_describe` / `lcm_expand` / `lcm_expand_query`

## 4 层 LCM 角色

| 层 | 名称 | 工具 | 何时用 |
|---|---|---|---|
| **L0** | Working | Hermes messages | 当前 turn |
| **L1** | Short-term | LCM 压缩 | 跨 turn |
| **L2** | Long-term | Hindsight | 跨 session |
| **L3** | Hard-coded | memory tool | 进程常量 |

## 8 DAG 节点类型

| 类型 | 描述 | 何时触发 |
|---|---|---|
| **summary** | 压缩后的摘要 | token 超阈值 |
| **raw** | 原始消息 | 摘要前 |
| **externalized** | 外部化 payload | 单条太大 |
| **ancestor** | 父节点链 | 展开时 |
| **child** | 子节点 | 向下查询 |
| **merge** | 合并节点 | 多 session 合并 |
| **anchor** | 锚点 | 引用点 |
| **root** | 根节点 | session 起点 |

## 5 工具用法

### `lcm_grep` (FTS5 搜索)
```python
lcm_grep(query="git rebase", limit=5, sort="recency")
# 找最近 5 个含 "git rebase" 的节点
```

### `lcm_load_session` (按 session 加载)
```python
lcm_load_session(session_id="abc", limit=100)
# 加载 session abc 的 100 条原始消息
```

### `lcm_describe` (节点元数据)
```python
lcm_describe(node_id=42)
# 看节点 42 的元数据(不加载内容)
```

### `lcm_expand` (展开摘要)
```python
lcm_expand(node_id=42, max_tokens=4000)
# 展开节点 42 的完整内容(限 4000 token)
```

### `lcm_expand_query` (NL 答案)
```python
lcm_expand_query(prompt="用户之前做了什么?", max_tokens=2000)
# LLM 合成答案
```

## 5 防坑

- ❌ 复制 LCM 摘要到 wiki(二次损失)
- ❌ 跨 session 引用 raw(可能丢)
- ❌ 不限 max_tokens(超 context 爆)
- ❌ 误用 `lcm_expand` 给 `lcm_grep`(expand 是展开,grep 是搜索)
- ❌ 忽略 externalized(大 payload 单独看)

## 关联

- [[concepts/agent-4-tier-memory-architecture]] — 4 层设计
- [[AGENTS]] — 整体规约
