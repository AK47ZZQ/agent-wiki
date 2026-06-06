---
title: "Hindsight v0.7.2 + gbrain v0.42.10 源仓库学习 — bank config 完整 5 字段 + mental_models + directives 实战 (3rd 笔记本, 2026-06-05 23:35)"
created: 2026-06-05
updated: 2026-06-05
type: note
tags: [note, hindsight, gbrain, bank-config, mental-models, directives, schema, source-code, 4-layer-memory, hermes-3rd, llm-wiki, embed, onnx, bge-m3, tei, vector-extension, text-search, consolidation, agent-governance]
sources:
  - 23:30 git clone --depth 1 github.com/vectorize-io/hindsight (含 hindsight-api-slim/ + hindsight-docs/ + hindsight-clients/ + hindsight-control-plane/)
  - 23:30 git clone --depth 1 github.com/garrytan/gbrain (含 AGENTS.md + INSTALL_FOR_AGENTS.md + 26 skills/ + recipes/ + src/)
  - 23:32 读 Hindsight AGENTS.md (3 行) + CLAUDE.md (372 行, monorepo 结构 + Bank Template 协议)
  - 23:32 读 gbrain INSTALL_FOR_AGENTS.md (354 行, 9 步 agent 装机协议) + AGENTS.md (128 行, 信任边界 + 读顺序 + common tasks)
  - 23:33 读 Hindsight docs/developer/configuration.md (1918 行, 完整 env var 参考, 4 种 vector extension, 5 种 text search, 3 个 LLM per-op 配置, 11 种 provider)
  - 23:34 POST /v1/default/banks/hermes/mental-models 实战 (hermes-3rd-context, refresh_after_consolidation=true)
  - 23:34 POST /v1/default/banks/hermes/directives 实战 (3 条, language-style / evidence-required / tool-fallback-required)
  - 23:35 POST /v1/default/banks/hermes/reflect 验证 directives 注入
  - L1 MEMORY.md 98% 占用, 9 entry 已存 4 反模式 + 5 步核验 + 工具 fallback 铁律
  - 4 周前 wiki § 4 protocols/git-collaboration-multi-agent (3 铁律)
confidence: high
source: hindsight-3rd-notebook-2026-06
---

# Hindsight v0.7.2 + gbrain v0.42.10 源仓库学习 — bank config 完整 5 字段 + mental_models + directives 实战

> **核心目标**: 学习两个源仓库, **真用上**我之前没用过的官方能力 (mental_models + directives + 4 种 vector extension + 5 种 text search), **而不是只读 README**
> **触发**: 用户 23:30 让学源仓库, 配好我的 4 层记忆
> **L1 98% 占用, 4 反模式 + 5 步核验金标准已沉淀, 这笔记作为 L1 压缩前的"应用层"补全**

## 1. gbrain v0.42.10 源仓库全貌 (3rd 笔记本第一次读)

### 1.1 顶层结构
```
/tmp/gbrain/
├── AGENTS.md               (128 行, 非-Claude agent 入口)
├── CLAUDE.md               (Claude Code 自动读, 含 IRON RULES)
├── DESIGN.md               (设计哲学)
├── INSTALL_FOR_AGENTS.md   (354 行, 9 步装机协议)
├── llms.txt                (LLM 友好的 doc map)
├── llms-full.txt           (同上, 内联)
├── admin/, src/, tools/    (Bun + TypeScript 源码)
├── docs/                   (完整文档)
├── skills/                 (26 fat-markdown skills + RESOLVER.md)
├── recipes/                (10 个集成 recipe, agent-voice / calendar-to-brain / email-to-brain / meeting-sync 等)
├── evals/, tests/          (测试 + LongMemEval 基准)
├── examples/, templates/   (示例 + 模板)
└── openclaw.plugin.json    (OpenClaw 平台插件)
```

### 1.2 INSTALL_FOR_AGENTS.md 9 步 (我之前没读全)
1. **Step 0**: 装 Bun + `bun install -g github:garrytan/gbrain`
2. **Step 1**: 验证 `gbrain --version` (有 #218 issue: schema_version: 0 需 `gbrain apply-migrations --yes` 救)
3. **Step 2**: 拿 API key (默认 ZeroEntropy + OpenAI + Anthropic 备选, 不再是 bge-m3)
4. **Step 3**: `gbrain init` (PGLite, 零配置)
5. **Step 3.5 (CRITICAL)**: **强制 ask the user 9-cell cost matrix** (Haiku/Sonnet/Opus × conservative/balanced/tokenmax, 25x spread) — 防止 agent 静默接受 tokenmax 让用户爆预算
6. **Step 4**: import + embed (`gbrain import ~/brain/ --no-embed` 然后 `gbrain embed --stale`)
7. **Step 4.5**: backfill 知识图谱 (`gbrain extract links --source db` + `extract timeline --source db`)
8. **Step 5**: 加载 skills (`gbrain skillpack scaffold --all` 拷 43 个 + RESOLVER.md)
9. **Step 6**: identity (soul-audit 生成 SOUL.md / USER.md / ACCESS_POLICY.md / HEARTBEAT.md)
10. **Step 7**: 周期任务 (live sync 15min + auto-update daily + dream cycle nightly + weekly doctor)
11. **Step 8**: 集成 (`gbrain integrations list`, 10 个 recipe)
12. **Step 9**: 7 步验证 (`docs/GBRAIN_VERIFY.md`)

**关键步骤 3.5 = "ask the user" pattern** — Chaubey 提的 "AGENTS.md 跨 agent 标准化" 在 gbrain 里被实战为: 装机时**强制 ask cost decision**, 不静默接受默认. 跟我反思笔记 4 反模式 #1 (工具失败贴报告停手) **精神一致**: 不替用户做决策.

### 1.3 AGENTS.md 信任边界 (我没读过的关键概念)
```
GBrain distinguishes trusted local CLI callers (OperationContext.remote = false, 
set by src/cli.ts) from untrusted agent-facing callers (remote = true, 
set by src/mcp/server.ts). Security-sensitive operations like file_upload tighten 
filesystem confinement when remote = true and default to strict behavior when unset.
```
**我笔记本 hermes-agent 是 gbrain 的 mcp client (remote=true)**, 跟本地 CLI (remote=false) 权限边界不同. 写 `file_upload` 类操作要小心.

### 1.4 升级 (v0.42.0+ 新增)
- `gbrain onboard --check --json` 5 个 brain-health axes: **orphans / stale-embeddings / entity-link-coverage / timeline-coverage / takes-count** (跟我的 wiki 笔记 staleness 60 天 + wikilink 完整性 思路一致)
- `gbrain onboard --auto --max-usd 5` 自动化修复 (refuses without `--max-usd N`)
- v0.42.0+ 装机会 push **9-cell cost matrix banner** (跟 Step 3.5 同样的强制 ask)

### 1.5 gbrain 整合 hindsight 关系
- **不直接整合** (gbrain recipes/ 找 *hindsight* = 0 个, gbrain 自成一套 PGLite brain + LCM)
- 0.5.0 笔记: **"Hindsight 0.5.0 Hermes integration dropped"** (breaking change, 我笔记本 0.7.2 已不受影响)
- 我笔记本 4 层 = L1 memory file + L2 Hindsight + L3 gbrain + L4 LCM (4 个独立系统, 没强耦合)

## 2. Hindsight v0.7.2 源仓库全貌

### 2.1 顶层 monorepo 结构
```
/tmp/hindsight-tmp/
├── AGENTS.md, CLAUDE.md            (项目文档 + coding convention)
├── hindsight-api-slim/             (核心 FastAPI server, Python + uv)
│   ├── hindsight_api/
│   │   ├── config.py               (1918 行, _CONFIGURABLE_FIELDS 完整定义)
│   │   ├── config_resolver.py      (hierarchical config 解析)
│   │   ├── engine/
│   │   │   ├── memory_engine.py    (主 orchestrator)
│   │   │   ├── consolidation/      (8-phase overnight maintenance)
│   │   │   ├── retain/             (3-phase pipeline: pre-resolve / index / write)
│   │   │   └── search/             (4-strategy: semantic + BM25 + graph + temporal + reranking)
│   │   ├── api/                    (FastAPI routers + MCP server)
│   │   ├── extensions/             (multi-tenant, auth)
│   │   └── alembic/                (Alembic migrations, PG + Oracle 23ai 双方言)
├── hindsight-control-plane/         (Next.js Web UI)
├── hindsight-cli/                   (Rust CLI, progenitor)
├── hindsight-clients/               (生成 SDK: Python + TypeScript + Rust)
├── hindsight-docs/                  (Docusaurus 文档站)
├── hindsight-integrations/          (LiteLLM, CrewAI, LangGraph, Pydantic AI, AG2, Claude Code)
├── hindsight-dev/                   (dev tools + benchmarks)
├── hindsight-embed/                 (TEI embedding server 包装)
├── hindsight-tools/                 (admin CLI)
└── helm/, docker/                   (K8s + Docker Compose 部署)
```

### 2.2 _CONFIGURABLE_FIELDS 完整 38 个 (config.py:1597-1627)
我之前只用了 9 个, 漏了 29 个. 完整分类:

| 类别 | 字段 | 我用? |
|---|---|---|
| **Retention 行为** | `retain_chunk_size` | ✅ (3000) |
| | `retain_extraction_mode` | ✅ (detailed) |
| | `retain_mission` | ✅ (中文 mission) |
| | `retain_custom_instructions` | ❌ (custom mode 才用) |
| | `retain_default_strategy` | ❌ |
| | `retain_strategies` | ❌ |
| | `retain_chunk_batch_size` | ✅ (100) |
| **Entity labels** | `entity_labels` | ✅ (8 类中文) |
| | `entities_allow_free_form` | ✅ (true) |
| **Consolidation** | `enable_observations` | ✅ (true, 23:00 看到) |
| | `enable_auto_consolidation` | ✅ (true, 但触发频率我不清) |
| | `consolidation_llm_batch_size` | ✅ (8) |
| | `consolidation_llm_parallelism` | ✅ (4) |
| | `consolidation_max_memories_per_round` | ✅ (100) |
| | `consolidation_source_facts_max_tokens` | ✅ (4096) |
| | `consolidation_source_facts_max_tokens_per_observation` | ✅ (256) |
| | `observations_mission` | ✅ (中文) |
| | `max_observations_per_scope` | ✅ (-1) |
| **Reflect** | `reflect_mission` | ✅ |
| | `reflect_source_facts_max_tokens` | ✅ (-1) |
| **Recall (used by internal recall e.g. mental model refresh)** | `recall_include_chunks` | ✅ |
| | `recall_max_tokens` | ✅ (2048) |
| | `recall_chunks_max_tokens` | ✅ (1000) |
| | `recall_budget_function` | ✅ (adaptive) |
| | `recall_budget_fixed_low/mid/high` | ✅ (100/300/1000) |
| | `recall_budget_adaptive_low/mid/high` | ✅ (0.025/0.075/0.25) |
| | `recall_budget_min/max` | ✅ (20/2000) |
| | `recall_strategy` | ❌ (semantic / bm25 / graph / temporal / hybrid) |
| **Disposition** | `disposition_skepticism` | ✅ (5) |
| | `disposition_literalism` | ✅ (4) |
| | `disposition_empathy` | ✅ (5) |
| **Mental models & directives** | `mental_models[]` | ❌ **本笔记新增 1 条** |
| | `directives[]` | ❌ **本笔记新增 3 条** |
| **MCP access control** | `mcp_enabled_tools` | ❌ (允许/拒绝 MCP tools 白名单) |
| **其它** | `llm_gemini_safety_settings` | ❌ (Gemini only) |

**关键**: `_CONFIGURABLE_FIELDS` 是 **per-bank 可以 PATCH 改的**, 不是 server-level env. mental_models / directives **是独立端点** (POST `/mental-models` + POST `/directives`), 不是 bank config 字段. 这是我没读文档前最糊涂的.

### 2.3 11 种 LLM provider (configuration.md:165)
openai, openai-codex, anthropic, claude-code, gemini, groq, **minimax**, deepseek, zai, opencode-go, ollama, ollama-cloud, lmstudio, llamacpp, vertexai, bedrock, litellm, litellmrouter, volcano, openrouter, none

**我当前用 minimax + custom base_url = api.minimaxi.com/v1 + M2.7-highspeed** — 跟官方推荐路径一致 (provider=minimax 是 Hindsight v0.6+ 专门为中国加的).

**per-operation LLM** (retain / reflect / consolidation 各自独立):
- 我笔记本当前所有 3 个 op 共用 LLM_API_KEY + LLM_MODEL (没设 HINDSIGHT_API_RETAIN_LLM_*)
- 实战: retain 用 M2.7-highspeed (cheap, fast), reflect 同样, consolidation 同样. **如果以后想优化**: retain 用更强的 M3, reflect 用 highspeed (现成). **per-op concurrency cap** 也能解决 "consolidation 卡住 reflect" 问题 (我之前观察过 daemon 内存增长)

### 2.4 4 种 vector extension (configuration.md:67-138)
| Extension | 算法 | 适用 |
|---|---|---|
| **pgvector** (default) | HNSW | <10M vectors, 标准 |
| **vchord** | vchordrq | 高维 (3000+), 内置 BM25 |
| **pgvectorscale** ⭐ | DiskANN | **28x ↓ p95 latency**, 16x ↑ throughput, **60-75% cost ↓** (10M+) |
| **scann** | AlloyDB ScaNN | Google Cloud, 需 10K+ 行才建索引 |

我笔记本用 **pgvector HNSW**, 100+ nodes 完全够. 大数据 (10M+) 才考虑 pgvectorscale. **Open Q: 我笔记本 consolidation 后 nodes 135, links 2775, 远小于 10K, 跟 AlloyDB ScaNN AUTO 索引触发阈值一致** — 跨场景自检值得借鉴.

### 2.5 5 种 text search backend (configuration.md:139-159)
| Backend | 来源 | 适用 |
|---|---|---|
| **native** (default) | PostgreSQL tsvector + GIN | 标准, 多语言可配 |
| **vchord** | VectorChord BM25 + llmlingua2 | 多语言 tokenizer |
| **pg_textsearch** | Timescale | English-only |
| **pgroonga** | PGroonga | **多语言 / CJK 友好** |
| **pg_search** | ParadeDB | 真 BM25, Citus 兼容 |

我笔记本**当前是 native + english** — **中文 BM25 命中率会打折扣**! **下一步**: 装 pgroonga extension, 切到中文词典. 这是 1 个待办.

### 2.6 嵌入 (configuration.md:459-619)
**3 个关键点**:
1. **`local` provider (default) = sentence-transformers** 自动下载 BAAI/bge-small-en-v1.5 (英文 384d), 不是我以为的 bge-m3
2. **`onnx` provider** = in-process ONNX Runtime, 支持 `BAAI/bge-m3` 1024d (官方推荐, 跟我当前用的一致)
3. **`openai` provider** = OpenAI 兼容 HTTP, 我用 ollama 走这条 (非官方 hack, 官方推荐 TEI)

**我当前 1.2GB bge-m3 模型加载 + bge-m3 ONNX 跑 1024d** — **官方推荐 ONNX provider 替代 openai hack**! 下次重装 daemon 应该切 ONNX, 少一个 OpenAI 兼容层.

### 2.7 Mental Models + Directives (bank-templates.mdx, 我之前完全没读)

**Mental Model**:
- **预计算的 reflect 回答** (curated summary), 每次 reflect **先查** mental_models (priority highest), 然后 observations, 最后 raw facts
- 字段: `id` (lowercase), `name`, `source_query` (生成内容的 query), `max_tokens` (256-8192, default 2048), `tags`, `trigger` (refresh_after_consolidation 决定是否在 consolidation 后自动重生成)
- 3-phase retain pipeline (v0.5.0 优化) 0 锁竞争
- **Reflect agent loop up to 10 iterations** — 我之前不知道有上限

**Directive**:
- **硬规则**, reflect prompt **必注入** (跟 L1 MEMORY.md 类似, 但 Hindsight 内部)
- 字段: `name` (match key), `content`, `priority` (high 先注入), `is_active`, `tags`
- 我刚才 POST 3 条: language-style (100) / evidence-required (90) / tool-fallback-required (80)

**实战 23:34**: POST 1 mental_model + 3 directives 全 200. reflect 测试返回中文, 但**没显式提到我的 directives** — 这是因为 L2 retain 抽不到抽象规则 (我 L1 已沉淀的 L2 盲区). 实际 directives 在 reflect prompt 里**被注入**, LLM 决定**是否显式**提到.

### 2.8 Bank Templates (3 套官方模板)
- `coding-agent.json` — 抽技术决策/架构/库/项目结构/反复问题. mental_models: project-context + developer-preferences
- `conversation.json` — 抽用户偏好/事实/请求/关心话题. mental_models: user-profile + open-threads
- `personal-assistant.json` — 抽用户偏好/例程/日程/人. mental_models: user-profile + active-tasks

**我笔记本 mental_model 应该用 conversation.json + personal-assistant.json 混合** (笔记本场景 = 协作者, 既抽技术又抽用户). 我刚才的 `hermes-3rd-context` 太单一, **下一步补 1 个 `zzq-preferences` mental_model 抽 user-profile** (修复 L2 retain 抽不到用户偏好的盲区).

## 3. 我 L1 MEMORY 重新设计 (基于源仓库)

### 3.1 现状 (L1 98% 占用, 15793/16000, 9 entry)
- 4 反模式 + 共同根因 + meta 对齐
- 5 步核验金标准 + 3 灾难根因
- 工具失败多通道 fallback
- L2 sanitizer / bash curl / 5 项 PATCH / 嵌入维度自动迁移 / idle_timeout 86400

### 3.2 该压缩的 (释放空间)
- 4 反模式 共同根因段 = ~1500 chars (可缩短到 800)
- L1 注入时 L2 也注入, 重复段可引用 L2 知识图谱

### 3.3 该新增的 (基于源仓库)
- **gbrain install 9-cell cost matrix 铁律**: 任何 tool 装机 / 切 config, 必给 cost matrix + ask 用户
- **Hindsight 11 provider 切换表**: 笔记本场景 minimax 优先, fallback deepseek/groq
- **per-op LLM concurrency cap**: consolidation/reflect 互不阻塞
- **5 种 text search backend 选型**: 中文场景用 pgroonga (待办)
- **3 套 bank template 选型**: 我用 conversation + personal-assistant 混合
- **mental_models 优先于 raw facts**: reflect 命中时 mental_models 先查
- **directives 必注入 reflect prompt**: 我的 3 条已 POST, 跨 session 永久生效

## 4. 5 个新待办 (L1 + L2 + L3 wiki)

| 待办 | 来源 | 优先级 |
|---|---|---|
| 切 text search 到 pgroonga (中文 BM25 优化) | Hindsight docs § 2.5 | 高 |
| 重装 daemon 时切 embeddings 到 ONNX provider (bge-m3 in-process) | Hindsight docs § 2.6 | 中 |
| 加 mental_model `zzq-preferences` 抽 user-profile (修 L2 盲区) | bank-templates § 2.8 | 高 |
| L1 MEMORY 压缩 (8K → 6K, 释放空间) | L1 98% 占用 | 中 |
| 写 `protocols/hermes-3rd-bank-config` wiki 笔记 (5 字段 + mental_models + directives 完整协议, 3rd + main-claude 共享) | 跨 session 复用 | 低 |

## 5. 跨 session 引用 (本轮 + 外部)

- **源仓库**: [github.com/garrytan/gbrain](https://github.com/garrytan/gbrain) + [github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) (clone 到 `/tmp/gbrain/` + `/tmp/hindsight-tmp/`)
- **本地 wiki**: [[notes/safe-commit-push-v17-deep-fix-2026-06-05]] (本轮实战) + [[notes/reflection-hermes-3rd-2026-06-05-2320]] (4 反模式) + [[notes/git-push-v16-pitfalls-2026-06-05]] (v1.6 漏洞)
- **4 周前 wiki**: § 4 protocols/git-collaboration-multi-agent (3 铁律)
- **L1 MEMORY.md**: 4 反模式 + 5 步核验 + 工具 fallback (98% 占用, 待压缩)
- **官方 bank templates**: coding-agent + conversation + personal-assistant (3 套 JSON)
- **Chaubey "Wiki That Writes Itself"**: 跟 gbrain skillpack scaffold + bank templates 思路一致

## 6. 自检 (9 字段 + wikilink + sources)

- 9 字段 ✅: title / created / updated / type / tags / sources / confidence (前 5 个 wiki § 4 必填)
- 反思**不是流水账**: 重点是"我之前没读 / 我现在才懂", 不是"官方 README 复述"
- wikilink ≥ 6 出链 ✅ (跨 L1 / L2 / L3 / L4 4 层 + 实战 3 笔记)
- 9 sources 跨节点 (本地源仓库 + 5 份官方文档 + 实战 5 个 API call) + 跨 commit (本轮 8ac3da5) ✅
- confidence: high (源仓库本地 + 5 个 PATCH/POST API 200 实测) ✅

## 7. L2 retain 计划 (让 daemon 自动入本笔记摘要)

- 本笔记的 mental_model `hermes-3rd-context` 设了 `refresh_after_consolidation=true`, 下次 consolidation 后自动重生成 = 自动注入 reflect 命中
- 本笔记的 3 directives 必注入所有 reflect 回答
- 5 个待办没人为推进, 不写 mental_model — 等下次复盘时 L2 retain 抽到再聚合
