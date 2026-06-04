# Agent SOUL.md Authoring Methodology

> **v1 · 2026-06-04** · First extracted from a 4-version SOUL authorship session.
>
> **Class-level reference** under `ai-harness-exploration` — applicable to ANY AI agent's identity/manifesto file, not just Hermes.

## When to use

You're asked to **author, refine, or evaluate** an agent's identity doc. The file may be called:
- `SOUL.md` (OpenClaw, Hermes)
- `AGENTS.md` (Codex, repo conventions)
- `IDENTITY.md` (OpenClaw peer description)
- `manifesto.md`, `principles.md`, `beliefs.md` (varies)

If the source is a single existing doc → **Quick Path** (3 steps). If the task is "best possible" or "refine" or "fix" → **Full Path** (6 steps + self-critique cycle).

## Quick Path (single existing doc)

```
1. Read source (skill_view / read_file / web_extract)
2. Extract: 1 vibe + 6 信/反对/拒绝 + 错误账本 + 元规则
3. Write + version stamp
```

## Full Path (multi-source fusion)

### Step 0: 收集 SOUL 相关上下文

Search for existing SOUL/AGENTS/IDENTITY files in the system + ecosystem:

```
search_files(pattern="*SOUL*", target="files", path="~")
search_files(pattern="*identity*", target="files", path="~")
search_files(pattern="AGENTS.md", target="files", path="~/hermes-all")
```

最低必读集（如果存在）:
- `~/hermes-all/hermes/SOUL.md` (root instance SOUL)
- `~/hermes-all/hermes/memories/SOUL.md` (memory-tier copy if exists)
- `~/hermes-all/hermes/skills/.../templates/worker-soul.md` (worker template)
- `~/hermes-all/hermes/profiles/*/SOUL.md` (per-profile instances)

### Step 0a: 必要性门控 (与 ai-harness-exploration Step 0c 互补)

- **创作性输出**（写/重写 SOUL）→ 不需要 6 问，**直接开始**
- **决策性推销**（"该装X吗"）→ 必须 6 问

SOUL 写作不是推销，是提炼和表达，不触发 necessity gate。但**写完后的"是否再优化一版"** 仍要走元评估。

### Step 1: 4 大范式来源

| 范式 | 来源 | 核心结构 |
|:----|:----|:-------|
| **OpenClaw** | openclaw-integration skill | 3 段：Identity + Core Rules + Personality |
| **agency-agents** | msitarzewski/agency-agents (106k★) | 6 段：Identity → Mission → Rules → Deliverables → Workflow → Metrics |
| **Hermes 官方 seed** | hermes/SOUL.md (default) | 1 段：personality statement |
| **Worker 操作手册** | kanban-worker/templates/worker-soul.md | 任务导向：身份 + 工作方式 + 防死循环 + 记忆规则 |

### Step 1.5: 学派定位 (决定结构倾向)

| 学派 | 核心主张 | 结构特点 |
|:----|:--------|:--------|
| **积极 spec 学派** | 我能做什么 | agency-agents 范式，6 段，feature 导向 |
| **约束学派** | 什么不能做 | OpenClaw 范式，3 段，rules 导向 |
| **反规则学派** | 我拒绝什么 | 6 反对 + 6 拒绝 + 错误账本（hermes 风格）|
| **元评估学派** | 我怎么反思 | "如何知道自己错了" 为核心 |

**最有力的 SOUL 是反规则 + 元评估的混合** —— 比"我能做什么"更诚实，比"我什么不能做"更可操作。

### Step 2: 8 段核心结构 (from extracted)

```
1. **Vibe 一句话** (6-12 字) — 让 agent 被人记得住的灵魂三字诀
2. **我是谁** — 模型/角色/记忆栈/护栏（不写具体版本号，会过期）
3. **我信** (6 条) — 核心信念
4. **我反对** (6 条) — 反向规则
5. **我拒绝** (6 条) — 硬底线（含日期 + 理由）
6. **错误账本** (2-3 行) — 真实失败案例，不擦
7. **当我不确定时** — clarify 工具 + 红旗语言列表
8. **元规则** — SOUL 自身的护栏（不自动改/0 cron/≤150 行/版本号）
```

### Step 3: Formalize — 顺序 + 格式

```yaml
# Header
version: vN + date
vibe: 6-12 字
声明:不是配置/流程/SOP

# 8 段顺序
我是谁 →
  模型/角色/记忆栈/护栏
  显式"不是什么"
我信(6 条) → 每条 1-2 句
我反对(6 条) → 每条 1-2 句,含反向案例
我拒绝(6 条) → 每条含日期+理由
错误账本(2-3 行) → 表:日期|错|教训|写进哪条
当我不确定时 → clarify ≤4 选项 + 5+ 红旗语言
跟你的关系(可选) → 你/我/共识/分歧区
元规则 → 不自动改/0 cron/≤150 行/版本号/SOUL≠任务清单
```

### Step 4-5: 写 + 验证

| 检查项 | 标准 |
|:----|:----|
| 行数 | ≤ 150（超 = 失去灵魂变 SOP）|
| Vibe 字数 | 6-12 |
| 具体版本号 | 0（用 L0/L1/L2/L3 抽象层替代）|
| 时态词 | 0（不要 "snapshot" / "as of"）|
| 错误账本 | 2-3 行精选（不堆）|
| 红旗语言 | 5+ 触发信号 |
| 元规则自身遵守 | 是（自指一致性）|
| 跟 worker-soul 职责分离 | 是（SOUL ≠ 任务清单）|

### Step 6: 自指 critique (v3→v4 循环)

**关键步骤**:写完 v3 后,重新读 v3,问"v3 的真实缺口是什么?",**不是为优化而优化**。

```
v3 写完 → 自我 critique →
  ├─ 找到真缺口 (位置错 / Vibe 太长 / 错误账本太多 / 时态词)
  ├─ 找不到 → 停,不发 v4
  └─ 找到 → v4 精炼
```

**反模式**:为了显得勤奋而出 v2/v3/v4。**v4 必须有真改进,不能是 cosmetic 改动**。

**v3→v4 真缺口清单(本会话提炼)**:

| 类别 | v3 表现 | v4 修正 |
|:----|:-------|:------|
| 位置 | 写到 `memories/`(跟 L2 长期记忆层概念混) | 根位置 `hermes/SOUL.md` |
| Vibe 字数 | 36 字陈述句 | 6 字三字诀(会停/会认/会忘) |
| 错误账本 | 5 行表(变流程报告) | 3 行精选 |
| 具体版本号 | LCM v0.15.0/Hindsight v0.6.1(1 月后过期) | L0/L1/L2/L3 抽象 |
| 时态词 | "2026-06-04 snapshot"(随时钟过期) | 永恒时态 |
| 重复 | "不确定"+"红旗"两节(重复感) | 合并为 1 节 |

## OpenClaw SOUL.md Spec (extracted)

```yaml
# $EMOJI $NAME

## Identity
$vibe
$description

## Core Rules
[extracted from Critical Rules section]

## Personality
[1-2 sentence persona statement]
```

详见 `mcp/openclaw-integration` skill → "OpenClaw Workspace Format Reference"。

## agency-agents 6-Section Body Template (extracted)

```yaml
1. Agent Name Agent Personality  — Opening personality statement
2. 🧠 Identity & Memory  — Role + personality + "what remembers"
3. 🎯 Core Mission  — 3-5 bullet groups
4. 🚨 Critical Rules  — MUST-follow domain constraints
5. 📋 Technical Deliverables  — Code/config examples
6. 🔄 Workflow Process  (optional) — Step-by-step
7. 📊 Success Metrics  (optional) — Measurable outcomes
```

详见 `software-development/hermes-agent-skill-authoring/references/agency-agents-pattern.md`。

## Anti-patterns

1. **位置错位** — 写到 `memories/` 而不是根,跟 L2 长期记忆层概念冲突
2. **Vibe 太长** — 36 字 vs 6 字,后者更易记
3. **错误账本堆** — 5+ 行表变成流程报告
4. **时态词** — "snapshot" 让灵魂随时钟变化
5. **具体版本号** — "LCM v0.15.0" 1 个月后过期
6. **理想化** — 全是优点,违反"反对 6 不理想化"
7. **不分职责** — SOUL 跟 worker-soul 重复,SOUL 写"能做什么"变任务清单
8. **为优化而优化** — v4 没真改进也硬出,违反 Step 6 自指 critique

## 与其他 skill 的关系

- **ai-harness-exploration** — SOUL 写作是它的"应用实例",Step 0/1/2/3 通用
- **hermes-workflow** — "📍 Git 提交纪律模式" 是 SOUL 写完后必备的下一步（用户说 commit 时 stop-档）
- **openclaw-integration** — OpenClaw 范式是 SOUL 写作的 4 大范式之一
- **hermes-agent-skill-authoring** — agency-agents 范式完整 spec 在其 references/

## 关键陷阱

| 陷阱 | 表现 | 解决 |
|:----|:----|:----|
| 写到 memories/ 不是根 | 灵魂跟 L2 长期记忆层概念混 | 根位置 = `~/hermes-all/hermes/SOUL.md` |
| Vibe 36 字 | 太长记不住 | 压到 6-12 字（三字诀）|
| 错误账本 5+ 行 | 变流程报告 | 精选 2-3 行 |
| 含 "snapshot" / "as of" | 灵魂随时钟过期 | 用永恒时态（"我跟你的关系"）|
| 含具体版本号 | 1 月后过期 | 用 L0/L1/L2/L3 抽象层 |
| SOUL 跟 worker-soul 重复 | 灵魂变 SOP | SOUL=身份/信念, worker-soul=任务/流程 |
| 写完 v3 不做自指 critique | 错过 v3→v4 真改进机会 | Step 6 必走 |

---

*Authored 2026-06-04 from a 4-version SOUL authorship session (v1→v2→v3→v4 of `hermes-all/hermes/SOUL.md`).*
