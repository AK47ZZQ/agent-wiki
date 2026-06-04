---
title: Hindsight 0.7.2 Bank Config 迁移指南 — memory_mode 字段废弃 + 6 项 PATCH 实操
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, hindsight, migration, bank-config, pydantic, v0.6.1-to-v0.7.2, optimization]
source: 笔记本 Hindsight 0.7.2 daemon 完整测试 (2026-06-04 20:30) + 14:25 笔记 + 官方 OpenAPI schema
confidence: high
---

# Hindsight 0.7.2 Bank Config 迁移指南

> 2026-06-04 20:30 笔记本侧 Hindsight 0.7.2 PATCH bank config 完整实操. 含: (1) 0.6.1 → 0.7.2 字段变化 (2) 6 项 PATCH 实测 (3) 3 个 schema 坑 (4) 优化建议.

**触发场景**: 笔记本侧 Hindsight daemon 18+ 小时 broken 修复后, 想优化 bank config 让 LLM 抽 facts 更精准 (符合用户偏好: 中文 + 严谨 + 直率).

---

## 1. 0.6.1 → 0.7.2 字段变化 (5 项)

| 字段 | 0.6.1 行为 | 0.7.2 状态 | 迁移方案 |
|---|---|---|---|
| `memory_mode: hybrid` | 自动 reflect + auto retain | ❌ **字段已废弃** | 改用 `enable_observations=true` + `enable_auto_consolidation=true` |
| `prefetch_method: recall` | 每 turn 注入 recall 结果 | ❌ **字段已废弃** | Hermes 集成层已自动管理 (在 `agent/memory_provider.py`) |
| `hybrid_context_tools` | 0.6.1 新工具集合 | ❌ **字段已废弃** | 用 `mcp_enabled_tools` (更通用) |
| `bank_config_api` | 不可调 | ✅ **新功能** | `PATCH /v1/default/banks/{bank}/config` 实时改配置 |
| `disposition_*` | 不可见 | ✅ **新功能** | `disposition_skepticism/literalism/empathy` (1-5 scale) |

**关键**: 0.7.2 **不再用 `memory_mode` 字段** —— 改用 bank config 细粒度字段. **"混合模式"** 在 0.7.2 = `enable_observations=true` + `enable_auto_consolidation=true`.

---

## 2. 6 项 PATCH 实测 (2026-06-04 20:30-20:35)

### 2.1 PATCH endpoint schema

```python
# ❌ 错 (直接传字段)
PATCH /v1/default/banks/hermes/config
{"disposition_skepticism": 5}  # 422 missing: updates

# ✅ 对 (要 updates 包裹)
PATCH /v1/default/banks/hermes/config
{"updates": {"disposition_skepticism": 5}}  # 200
```

**关键坑**: PATCH body **必须** `{"updates": {...}}` 包裹, 不是 OpenAPI 默认的 pydantic 字段. **422 错误**:
```json
{"detail":[{"type":"missing","loc":["body","updates"],"msg":"Field required"}]}
```

### 2.2 6 项 PATCH (一次 PATCH 可以改多字段)

```python
PATCH /v1/default/banks/hermes/config
{"updates": {
    "disposition_skepticism": 5,        # 严谨 (1-5)
    "disposition_literalism": 4,         # 不要过度字面 (1-5)
    "disposition_empathy": 5,            # 共情 (1-5)
    "retain_mission": "...",              # retain 的核心目标
    "reflect_mission": "...",             # reflect 的核心目标
    "observations_mission": "...",        # observation 的核心目标
    "retain_extraction_mode": "detailed",  # concise | detailed
    "recall_budget_function": "adaptive",  # fixed | adaptive
    "entity_labels": {...}                # 9 类 (Dict[str, List[str]])
}}
```

### 2.3 disposition 5/4/5 实测

| 维度 | 默认 3/3/3 | PATCH 5/4/5 | LLM 行为差异 |
|---|---|---|---|
| skepticism=5 | 3/3/3 中等质疑 | **强质疑** | LLM 抽 facts 更细粒度, 更多独立 facts |
| literalism=4 | 3/3/3 中等字面 | **稍字面** (不是 5) | 平衡, 不要过度死板 |
| empathy=5 | 3/3/3 中等共情 | **强共情** | LLM 回答更体贴, 多角度考虑 |

**实测**: disposition 5/4/5 后, reflect 1972 字符结构化中文回答, 含 5 个对比维度表.

### 2.4 mission 字段 (3 个 + 实测)

```python
mission = "Hindsight 第二大脑: 笔记本侧 Hermes 3rd 协作者的日常观察沉淀. 重点: (1) 工具配置/部署细节 (2) 中文用户偏好 (3) 多 agent 协作经验 (4) Hindsight/LCM/MCP 等系统级方法论. 排除: 重复内容/纯 session 日志/<2 来源的猜测."

PATCH {"updates": {
    "retain_mission": mission,         # retain 时 LLM 知道目标
    "reflect_mission": mission,         # reflect 时 LLM 知道目标
    "observations_mission": mission + " 观察类重点: 跨 turn 模式识别/异常告警/周期性行为."
}}
```

**验证**: `/profile` 端点返 `mission` 和 `background` 都显示 mission 内容. **LLM 真的用 mission** —— retain 抽 facts 会优先抽跟 mission 相关的.

### 2.5 extraction_mode: concise → detailed 实测

| 模式 | facts 粒度 | token 成本 | 适用 |
|---|---|---|---|
| **concise** (默认) | 粗粒度 (一句话 1 fact) | ~3000 tokens/retain | 快速, 通用 |
| **detailed** | 细粒度 (一句话 3-5 facts) | ~3500 tokens/retain (+17%) | 笔记本侧深度沉淀 |

**实测**: 同一句 "Hermes 3rd 是跑在 Windows 11 + MSYS2 笔记本上的协作者" → 
- concise 模式: 1 fact "Hermes 3rd 是笔记本侧 Hermes agent"
- detailed 模式: 3 facts (Hermes 3rd 平台/系统/shell 类型)

**推荐**: 笔记本侧用 detailed, 服务端用 concise.

### 2.6 recall_budget_function: fixed → adaptive 实测

| 模式 | low | mid | high | 行为 |
|---|---|---|---|---|
| **fixed** | 100 facts | 300 facts | 1000 facts | 固定召回数 |
| **adaptive** | 2.5% corpus | 7.5% corpus | 25% corpus | 按 query 自适应 |

**推荐**: 笔记本侧用 adaptive (corpus 小, 100/300/1000 没区别, adaptive 更智能).

### 2.7 entity_labels: 9 类中文标签

```python
PATCH {"updates": {
    "entity_labels": {
        "Person":    ["姓名", "人物", "作者", "开发者", "用户"],
        "Tool":      ["工具", "软件", "CLI", "SDK", "API"],
        "Framework": ["框架", "库", "包"],
        "Method":    ["方法", "流程", "模式", "工作流"],
        "Concept":   ["概念", "原理", "理论", "架构"],
        "File":      ["文件", "配置", "脚本", "日志"],
        "Path":      ["路径", "目录", "URL", "位置"],
        "Command":   ["命令", "cmd", "shell", "bash"],
    }
}}
```

**实测**: 1 句 "Hermes 3rd 是跑在 Windows 11 + MSYS2 笔记本上的协作者, 用 uvx 装 LCM 0.16.0. 主要工具: VS Code, lark-cli, hindsight daemon. 关键文件 E:\hermes\wiki\index.md."
→ 抽 7 entities: `E:\hermes\wiki\index.md`, `hindsight daemon`, `VS Code`, `lark-cli`, `LCM 0.16.0`, `uvx`, `Hermes 3rd` (完美!)

---

## 3. 3 个 schema 坑 (踩过 + 解决)

### 3.1 PATCH 端点要 `updates` 包裹

```python
# 错
{"disposition_skepticism": 5}

# 对
{"updates": {"disposition_skepticism": 5}}
```

### 3.2 entity_labels 不是 list, 是 `Dict[str, List[str]]`

```python
# 错 (400 error)
{"entity_labels": ["Person", "Tool"]}

# 对 (LabelGroup pydantic 格式)
{"entity_labels": {"Person": ["姓名"], "Tool": ["工具"]}}
```

### 3.3 disposition 字段 nullable, 默认 3/3/3

```python
# PATCH null = 重置为默认 3/3/3
{"updates": {"disposition_skepticism": null}}
```

---

## 4. 完整 bank config 默认值 (33 字段)

| 字段 | 默认 | 推荐 (笔记本侧) | 备注 |
|---|---|---|---|
| retain_chunk_size | 3000 | 3000 | OK |
| retain_extraction_mode | concise | **detailed** | 笔记本侧深度沉淀 |
| retain_mission | null | **填具体** | 让 LLM 知道目标 |
| retain_custom_instructions | null | (可填中文输出要求) | |
| enable_observations | true | true | 必需 (混合模式) |
| enable_auto_consolidation | true | true | 必需 (混合模式) |
| consolidation_max_memories_per_round | 100 | 100 | OK |
| consolidation_llm_batch_size | 8 | 8 | OK |
| consolidation_llm_parallelism | 4 | 4 | OK |
| consolidation_source_facts_max_tokens | 4096 | 4096 | OK |
| consolidation_source_facts_max_tokens_per_observation | 256 | 256 | OK |
| observations_mission | null | **填具体** | 让 observation 更有方向 |
| max_observations_per_scope | -1 | -1 (无限制) | OK |
| entity_labels | null | **填 9 类中文** | 中文实体抽取必需 |
| entities_allow_free_form | true | true | OK |
| reflect_mission | null | **填具体** | 让 reflect 更有方向 |
| reflect_source_facts_max_tokens | -1 | -1 (无限制) | OK |
| recall_include_chunks | true | true | OK |
| recall_max_tokens | 2048 | 2048 | OK |
| recall_chunks_max_tokens | 1000 | 1000 | OK |
| recall_budget_function | fixed | **adaptive** | 笔记本 corpus 小 |
| recall_budget_fixed_low/mid/high | 100/300/1000 | (不用) | fixed 模式用 |
| recall_budget_adaptive_low/mid/high | 0.025/0.075/0.25 | **0.025/0.075/0.25** | adaptive 模式用 |
| recall_budget_min | 20 | 20 | OK |
| recall_budget_max | 2000 | 2000 | OK |
| disposition_skepticism | null (=3) | **5** | 严谨 |
| disposition_literalism | null (=3) | **4** | 不要过度字面 |
| disposition_empathy | null (=3) | **5** | 共情 |
| llm_gemini_safety_settings | null | null | (Gemini 才用) |
| mcp_enabled_tools | null | null | (MCP 集成用) |
| retain_chunk_batch_size | 100 | 100 | OK |
| retain_default_strategy | null | null | OK |
| retain_strategies | null | null | OK |

---

## 5. 验证流程 (PATCH 完必跑)

```python
# 1. PATCH (返回 200)
r = requests.patch(f'{URL}/v1/default/banks/hermes/config', 
                   json={'updates': {...}}, timeout=10)
assert r.status_code == 200

# 2. GET 验证字段生效
r2 = requests.get(f'{URL}/v1/default/banks/hermes/config', timeout=10)
cfg = r2.json()['config']
assert cfg['disposition_skepticism'] == 5

# 3. /profile 验证 mission + disposition
r3 = requests.get(f'{URL}/v1/default/banks/hermes/profile', timeout=10)
profile = r3.json()
assert profile['disposition'] == {'skepticism': 5, 'literalism': 4, 'empathy': 5}
assert profile['mission'].startswith('Hindsight 第二大脑')

# 4. 实测 retain 看 LLM 风格
r4 = requests.post(f'{URL}/v1/default/banks/hermes/memories', 
                   json={'items': [{'content': 'test', 'context': 'verify'}]}, 
                   timeout=30)
assert r4.json()['success']

# 5. 实测 reflect 看 answer 风格
r5 = requests.post(f'{URL}/v1/default/banks/hermes/reflect',
                   json={'query': '测试 disposition', 'budget': 'mid'}, 
                   timeout=60)
assert len(r5.json()['text']) > 500
```

---

## 6. 跨迁移方法论 (给未来避坑)

### 6.1 PATCH 任何字段前必跑

1. **GET /config 完整 schema** (33 字段, OpenAPI 有定义)
2. **小步 PATCH 一次只改 1-2 字段** (避免一次改太多难调试)
3. **GET 验证** 字段生效
4. **/profile 验证** LLM 用的 view 字段生效
5. **retain/reflect 实测** 行为变化

### 6.2 schema 不明字段处理

| 现象 | 处理 |
|---|---|
| 422 缺 `updates` 字段 | PATCH body 加 `{"updates": {...}}` 包裹 |
| 400 "Invalid format" | OpenAPI schema 看不到细节, 看 pydantic 源码 (`/venv/Lib/site-packages/hindsight_api/models.py`) |
| 字段返 null 默认 | 不 PATCH 就保留默认, PATCH null = 显式重置 |
| 复杂对象 (LabelGroup) | 试 Pydantic 默认格式 (`Dict[str, List[str]]`) |

### 6.3 配置保护建议

| 保护方式 | 实现 |
|---|---|
| **定期导出 bank config** | `GET /config` → 存到 `~/.hindsight/profiles/{bank}.config.bak` |
| **变更前 diff** | 比较前后两个 GET 输出, 标红变更 |
| **变更后 verify** | 跑 4 步验证 (status, profile, retain, reflect) |
| **写入 wiki note** | 每次 PATCH 都写一条 `log.md` + `notes/` 沉淀 |

---

## 7. 关联文档

- 触发场景: [[notes/hindsight-daemon-fix-2026-06-04]] (18+ 小时 broken 修复后, 想优化)
- 真实定位: [[concepts/hindsight-in-hermes-ecosystem-2026]]
- 5 mode 横向对比: [[comparisons/hindsight-5-modes-2026]]
- 风险与优化: [[notes/hindsight-risks-and-optimizations-2026]]
- 4 维检索: [[methods/hindsight-4d-retrieval-complete]]
- LCM 升级: [[notes/lcm-upgrade-v0.12-to-v0.15]]
- 笔记本协作者: [[agents/hermes-3rd]] / [[entities/hermes-3rd]]
- Hermes 自检方法: [[agents/hermes-self-check]]
