# Hindsight × Hermes 2026-06-03 探索纠正笔记

> **为什么这个 references 重要**: 本会话产生了一系列**颠覆之前认知**的发现, 必须留作未来 5 步法探勘 Hindsight 类工具时的纠正点.

## 颠覆清单 (vs 之前理解)

### 1. **Hindsight plugin 默认 auto-retain = Hermes 默认行为**

**之前理解**:
- 以为 Hindsight bank 里的内容是 Agent 显式 retain
- 以为"hybrid mode prefetch 未触发" = plugin 没在跑

**真实**:
- Hermes 内部 Hindsight plugin 默认配置:
  ```python
  # /c/Python314/Lib/site-packages/plugins/memory/hindsight/__init__.py:572-575
  self._auto_retain = True       # ← 每 turn 自动 retain
  self._retain_every_n_turns = 1 # ← 每 1 turn 1 次
  self._retain_async = True
  self._auto_recall = True
  self._recall_types = ["observation"]
  ```
- Server log 中 `STREAMING RETAIN BATCH` 频繁出现, 但来源是 plugin auto-retain, 不是用户操作
- 5 turns session = 5 batches = 10-13秒/batch = 50-65秒总延迟
- **每 turn 都烧 2-3k tokens (LLM 抽取 + 嵌入)**

**Acceptance 决策**:
- 你**接受这个默认行为** — 不改 plugin 源码, 不加关闭 cron
- 因为改 plugin 要动 Hermes 内部 (高风险)
- token 成本 ~10k/天 已成"已知成本"

**Future 探勘提示**:
- 探勘任何 Hermes plugin 时, **先看 plugin 源码默认行为**, 不要假设"显式触发"
- 探勘 Hindsight 类工具时, **第一步**: `grep -nE "_auto_retain|_auto_recall|_every_n_turns" <plugin_path>`

---

### 2. **on_session_end hook 实际是 per-turn, payload 不含 messages**

**之前理解**:
- 以为 `on_session_end` = "session 真结束时触发" (低频, 1次/session)
- payload 含 messages

**真实**:
- 触发位置: `agent/conversation_loop.py:4587` — "Fired at the very end of every run_conversation call"
- **per-turn 触发** (高频, 1次/turn)
- Payload 字段 (line 4592-4598):
  ```python
  _invoke_hook("on_session_end",
      session_id=agent.session_id,
      completed=completed,
      interrupted=interrupted,
      model=agent.model,
      platform=getattr(agent, "platform", None) or "")
  ```
- **完全不含 messages** — 写 hook 时基于"hook 能拿到 messages"的所有逻辑都失效

**教训**:
- 事件名**有误导**: "session_end" 实际是 "turn_end"
- 写 hook 前**必须看 invoke_hook 调用点**, 不要凭事件名假设
- payload schema 决定 hook 能做什么, 缺失 messages = hook 退化

**Acceptance 决策**:
- 卸 hook (per-turn 0.25s + 0 candidates = 纯浪费)
- 保留 handoff v1.2 作为 manual API (不与 plugin 竞争)

**Future 探勘提示**:
- 任何 hook/事件探索: **Step 1 必看 invoke_hook 调用点**, 确认 payload schema
- 钩子命名约定 vs 实际触发时机**可能不一致** (Hermes 这里就是反例)

---

### 3. **memory unit 字段是 `text` 不是 `content`**

**之前理解**:
- 以为 memory unit 用 `content` 字段 (类比一般文档)

**真实**:
- 实测 `GET /v1/default/banks/{bank}/memories/{id}` 返回:
  ```json
  {
    "id": "747ab678-7e54-44bc-a12b-3464cd86f8cb",
    "text": "Hindsight 支持 update_mode=append 模式, 用于追加内容到现有记忆",  ← text
    "context": "",
    "date": "2026-06-03T14:44:57.482913+00:00",
    "type": "observation",
    "mentioned_at": "2026-06-03T14:44:57.482913+00:00",
    "occurred_start": "2026-06-03T14:44:57.482913+00:00",
    "occurred_end": "2026-06-03T14:44:57.482913+00:00",
    "entities": ["hybrid mode", "hindsight"]
  }
  ```
- `content` 是 **input 字段** (POST /memories items=[{content, context}])
- `text` 是 **output/存储字段** (GET 返回)
- **Schema 不对称** — 输入输出用不同字段名

**Future 探勘提示**:
- 写 API wrapper 前**先看 input 和 output schema 完整对比**
- 不要假设对称 (一个字段在两边同名)

---

### 4. **3 memory modes (hybrid/context/tools) + recall 行为**

| Mode | auto-recall | tool 暴露 | 适合 |
|---|---|---|---|
| **hybrid** | ✅ 静默 | ✅ 显式 | 推荐默认, Agent 平衡 |
| **context** | ✅ 静默 | ❌ 隐藏 | 生产 assistant (避免 tool overload) |
| **tools** | ❌ 无 | ✅ 显式 | Agent 显式控制 (高级) |

**Acceptance**: hybrid (官方推荐) + prefetch_method=recall (省 token)

---

### 5. **Hindsight 在 Hermes 中的实际负担**

```
Server: PID 6224, port 8888, healthy
Bank 'hermes': 81 facts (大部分 plugin auto-retain 加的)
Embeddings: bge-small-en-v1.5 (en, 384 维)
Reranker: ms-marco-MiniLM-L-6-v2 (multilingual, 兜底跨语言)
Token 成本: ~10k/天 (plugin auto-retain)
人工 token: 0 (handoff v1.2 = 0 uses today)
```

**决策**: 接受 plugin auto-retain (你已说 OK)

---

## Future 探勘行动指南 (Hindsight 类工具)

```
1. Step 0: 是否值得探勘?
   - 痛点真实? (低频=不必要)
   - 边际价值多少? (vs LCM/session_search/wiki 已覆盖)
   - 退出成本多大? (改 plugin 源码 = 高退出成本)

2. Step 1: 必看源码
   - 找 plugin 源码: <hermes>/Lib/site-packages/plugins/memory/<name>/__init__.py
   - grep "_auto_retain|_auto_recall|_every_n_turns" → 知道默认行为
   - 找 hook 调用点: grep "invoke_hook.*<event_name>"
   - 确认 payload schema (input/output 字段)

3. Step 2: 必测真实 retention
   - 跑 1 个真 session, 看 server log
   - 区分: 哪些是 plugin auto, 哪些是 user manual
   - 算真实 token 成本 (不是声称的)

4. Step 3: 必做成本对比
   - plugin auto-retain N tokens/turn × M turns/day
   - handoff/manual cost vs plugin cost
   - 接受/不接受, 都要明确写出

5. Step 4: 必明确 ownership
   - "你控制 vs plugin 控制" — 写进 AGENTS.md
   - 不要在"我以为" 和 "实际" 之间留下歧义
```

## 关键经验 (纳入 5 步探勘通用法则)

### 经验 A: "看起来的默认 ≠ 实际的默认"

- 任何 plugin/skill/config 标"default":
  - **查源码**确认
  - **跑真 session** 确认
  - **看 log** 确认
- 3 步都做了才能写"X 是默认行为"

### 经验 B: "事件命名可能误导"

- 看到 hook 事件名 (e.g. `on_session_end`):
  - **查 invoke_hook 调用点**
  - **看 payload schema**
  - **跑 1 次 test 验证**
- 命名约定 vs 实际行为**经常不一致**

### 经验 C: "API 字段名不对称"

- input 和 output schema **可能用不同字段名**
- POST items=[{content}] 但 GET 返回 {text} — 这种不对称常见
- **写代码前先全 schema 对比**

## 关联文件

- `wiki/concepts/hindsight-in-hermes-ecosystem-2026.md` (官方视角定位)
- `wiki/notes/hindsight-exploration-2026-06-03.md` (本会话全记录)
- `wiki/methods/hindsight-4d-retrieval-complete.md` (4 维检索完整)
- `wiki/notes/hindsight-risks-and-optimizations-2026.md` (风险与优化)
- `wiki/wiki/AGENTS.md` (精简版架构说明)
- skill: `hindsight-handoff` (manual API), `hindsight-watchdog` (监控), `install-hindsight-as-hermes-memory` (安装)
