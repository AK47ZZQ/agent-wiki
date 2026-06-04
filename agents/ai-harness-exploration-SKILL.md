---
name: ai-harness-exploration
description: "分析 AI 工具/文章并提取可复用模式——从五源融合：deusyu Harness Engineering + OpenAI Codex + Vibe Coding + Mitchell Hashimoto + Harness平台工程。MiniMax MCP优先搜索+ Tavily MCP×4兜底，输出 Skill/Method/Workflow/AGENTS.md 四件套。"
emoji: 🧪
version: 6.18.0
author: Hermes Agent (deep integration + deusyu study)
created_by: agent
platforms: [windows, linux, macos]
triggers:
  - 学习
  - 探勘
  - 分析
  - 研究
  - 提取模式
  - 了解工具
  - 深入挖掘
  - 新来源
  - 优化skill
  - 改进skill
  - 自我优化
  # wiki 集成的额外触发(2026-06-04)
  - 探勘wiki
  - 改进wiki
  - wiki如何更好
  - 怎么用wiki
  - wiki库设计
  - 知识库架构
  # 写入征求同意的额外触发(2026-06-04 v6.15.0)
  - 写入wiki
  - 写到wiki
  - 更新wiki
  - wiki落盘
  - 沉淀到wiki
  - 写入文档
metadata:
  hermes:
    tags: [analysis, pattern-extraction, ai-tools, workflow, research, learning]
    related_skills: [hermes-workflow, writing-plans, deepseek-m2.7-orchestrator, kanban-orchestrator, hermes-self-check]
    changelog:
      6.11.0: "2026-06-04 — Wiki integration (5 wiki pages + 1 reference), 6 new triggers, Step 4 wiki-delivery hard link. See references/wiki-integration-mode.md for full 8-step flow."
      6.12.0: "2026-06-04 — Wiki integration. Added wiki_integration block to frontmatter (5 wiki pages + 1 reference)."
      6.13.0: "2026-06-04 — Search channel reality check. § 9.0 (实测矩阵) added. Tavily REST 401 (not 432), DuckDuckGo needs UA + 短 timeout, terminal curl 4-tier (GitHub raw / arXiv / Bing / DuckDuckGo) becomes the real fallback. Patched '7 路并发' code sample to '4 MCP + 3 curl'. 8.0.7 self-probe script added for monthly re-verification."
      6.14.0: "2026-06-04 — Mode selection decision tree. Added '模式选择决策树 (NEW 2026-06-04 — 用户明确纠正后提炼)' to references/internal-synthesis-mode.md. 3-step check: (1) factual vs methodological, (2) check methodological signals (含'如何'/'更好'/业界术语/用户深化), (3) trigger 6-step if methodological. Concrete mistake catalog: '基于已有 9 份 SOUL.md' = internal-synthesis OK, '如何创建更好的 wiki 库' = must do 6-step with web. Lesson: OR trigger conditions are necessary, not sufficient."
      6.15.0: "2026-06-04 — Wiki write boundary (user-explicit correction). New reference references/wiki-write-boundary.md codifies 3-layer model (LCM / Scratchpad / Wiki) and 3 anti-patterns (LCM summary expansion / meta-method self-add 5+ boundary files / Distill ≠ 5 method pages). E2E test reference references/e2e-multi-agent-test.md preserves 2026-06-04 真任务 3 Agent 协议栈测试结果(15 min, 6/6 原语, 8/8 验收). Wiki integration block updated with 2 new references. Also corrects § 9.0.2 fallback tree (5a-D commands now include DuckDuckGo + UA + 8s). v6.14 changelog preserved per protocol § 5."
      6.16.0: "2026-06-04 — Mid-task self-correction gap. New § 9.1.4 captures user correction #4: 多次任务累积扩张写入 = 缺少'中途自检'. Lesson: '用户没反对' ≠ '用户同意'; each new task that overlaps the previous one should grep own writes + check for unflagged self-adds before proceeding. 5-second self-check protocol added. Bumps references/wiki-write-boundary.md with § 5 'cumulative drift' rule."
      6.17.0: "2026-06-04 — 5-step verification hard rule for all wiki writes. User correction #5: 本会话 5-6 次 commit + push 假成功（commit e59a9e3 输出'成功'但 git cat-file 报 'Not a valid object name'），668 行内容从来没真推。Lesson: wiki 写入 = commit + push, 必须走 5 步核验 (status → add → commit → cat-file -t HEAD → push + rev-parse 对比)。新增 § 4.0.9 硬协议 + § 9.1.5 案例。同时记录用户硬偏好: author name = 'Hermes <hermes@hermes.local>', 唯一远端 = AK47ZZQ/agent-wiki。新增 references/wiki-write-verification-protocol.md (含 11 速查陷阱 + 5 步 bash 模板)。hermes-all 远端已被用户删除, 不再使用 — 所有内容应走 agent-wiki 仓库。"
    wiki_integration:
      # 探勘产物自动写到 wiki(2026-06-04 集成)
      - wiki_page: methods/wiki-as-second-brain
        purpose: wiki 协议 + DRY 原则 + 5 评估指标
      - wiki_page: methods/wiki-code-workflow
        purpose: CODE 4 阶段(Capture/Organize/Distill/Express)落地
      - wiki_page: protocols/agent-coordination
        purpose: 6 原语 + A2A 兼容映射
      - wiki_page: protocols/goal-alignment
        purpose: 主动告警机制
      - wiki_page: protocols/per-project-claude-md-template
        purpose: per-project CLAUDE.md 模板
      - reference: references/wiki-integration-mode.md
        purpose: 集成模式的完整流程
      - reference: references/wiki-write-boundary.md
        purpose: wiki 写入边界(LCM / scratchpad / wiki 三层 + 3 反模式) — 用户2026-06-04 纠正"不要随意写进 wiki"沉淀
      - reference: references/e2e-multi-agent-test.md
        purpose: 多 Agent 协议栈 E2E 真任务测试(2026-06-04, 15 min, 6/6 原语, 8/8 验收) — 复用模板

---

# 🧪 AI Harness 探勘法（Hermes Agent v3.0）

> **本技能注入 Hermes Agent 实际分析模式**——从真实四源学习（OpenAI Codex + Vibe Coding + Mitchell Hashimoto + Harness Engineering）中提取的可复用方法论。

## 何时触发

当用户让你学习/分析/探勘某个新玩意时：

### 模式快速选择

```
用户发来链接/工具/范式
  │
  ├─ "简单说说" / "了解下" / "这是什么"
  │   → 快速分析模式（3-5 分钟，无 wiki）
  │
  ├─ "学习一下" / "深入挖掘" / "分析"
  │   → 全量探勘（15-30 分钟，有 wiki）
  │
  ├─ "继续" / "还有吗" / "再深入看看"
  │   → 深度延续搜索（8-12 分钟，增量）
  │
  ├─ "基于已有的 X 写一份 Y" / "结合文件 + 你的实际" / "整合这几个"
  │   → 内部多源合成模式（10-15 分钟，filesystem 探勘 + read_file 群读，无 web 搜索）— 见 references/internal-synthesis-mode.md
  │
  ├─ "探勘wiki" / "改进wiki" / "wiki如何更好" / "怎么用wiki" / "wiki库设计"
  │   → **Wiki 集成模式(2026-06-04 新增)** — 全量探勘 + 写 wiki(需申请)
  │     必读:[[methods/wiki-as-second-brain]] + [[methods/wiki-code-workflow]]
  │     必走:CODE 4 阶段(Capture→Organize→Distill→Express)
  │     必落:产物写到 wiki/(需走 § 4.0 申请流程)
  │     — 见 references/wiki-integration-mode.md
  │
  ├─ "写入wiki" / "写到wiki" / "更新wiki" / "wiki落盘" / "沉淀到wiki" / "写入文档"
  │   → **Wiki 写入申请(2026-06-04 v6.15.0)** — 必走申请流程
  │     1. 列候选清单(文件/类型/大小/来源/是否用户要求)
  │     2. 每个文件 1 段内容摘要
  │     3. 标注用户显式 vs 边界
  │     4. 询问用户"写哪些/全部/不写"
  │     5. 用户决定后才执行
  │     拒绝的内容移到 `scratchpad/_drafts/`
  │     — 见 § 4.0 详细协议
  │
  ├─ "LCM 摘要" / "压缩归档" / "session 摘要" / "会话历史"
  │   → **LCM 检查模式(2026-06-04 v6.15.0)** — 查 lcm_expand / lcm_grep
  │     1. 读 lcm.db 节点/摘要(只读)
  │     2. 报告发现(在 chat 里说)
  │     3. **不**自动写 wiki
  │     4. 如果摘要值得沉淀 → 走 § 4.0 申请流程
  │
  ├─ "优化skill" / "改进skill" / "自我优化"
  │   → 自我优化 Meta 模式（15-30 分钟）
  │
  ├─ "测试ai-harness-exploration"
  │   → 技能自测试（references/skill-self-testing.md）
  │
  └─ 无明确关键词 → 全量探勘（默认）
```

- 🔗 发来一篇链接 → "学习一下这个"
- 📦 问到某个新工具 → "了解下XXX"
- 💡 问到某种新范式 → "这是什么原理"
- 🛠️ 看到一个新的工作流 → "这个怎么样"
- 🔄 初次探勘后说"继续" → 深度延续搜索流程
- 📂 任务涉及**内部多份现成产物**（SOUL.md / MEMORY.md / skill / wiki 概念页）→ 内部多源合成模式（**最易被漏掉的触发信号**）

### ⏹️ 停止条件（什么时候不该探勘）

并非所有主题都值得使用本技能的完整 6 步探勘法。以下条件满足任意一项 → 改用快速分析模式，跳过 wiki 创建：

```
停止条件清单：
  ├─ 主题太小（单一函数/配置项/单行 bug）→ 直接回答，不需探勘
  ├─ 主题太大（操作系统/AI 全领域）→ 分解为子主题，一次只探勘 1 个
  ├─ 用户只需网址/文档 → 直接给，不分析
  ├─ 主题和已有概念 90% 重复 → 在 log.md 记一笔，不创建新页面
  ├─ 明显是过时/废弃的技术 → 快速确认后标注，不深入
  ├─ 连续 2 次搜索后 < 2 个有效来源 → 快速模式，结束
  └─ 用户说"不用了"/"算了"/"下次" → 立即停止，不追问

当用户明确说某个方向继续时：
  即使符合停止条件也不强行停止——用户的注意力是最稀缺的资源。
  但如果搜索 2 轮后仍无有价值发现，建议用户换个方向。
```

## 核心方法论：6 步探勘法

```
Step 0: 来源质量评估 — 值不值得读？
Step 1: Analyze — 7 个子步骤 + 4 轮递进搜索
Step 2: Extract — 提取 Concept / Method / Workflow
Step 3: Formalize — Skill / Method / Concept / AGENTS.md 四件套
Step 4: Deliver — 报告 + 3 关键洞察
Step 5: Verify — 18 项检查 + Ralph 6 信条
Step 6: Debrief — 记忆 + 同步 + 兜底 + 凝练
```

> **第三种适配模式**（filesystem-only,无 web 搜索）:见 `references/internal-synthesis-mode.md`。当任务"基于已有 N 份产物合成 1 份"时用此模式,跳过 web 搜索轮次,直接 read_file 群读 + taxonomy 建立 + DRY 决策。

---

## Step 0️⃣ 来源质量评估（先判断值不值得读）

不是所有来源都值得深入。读之前先评估：

| 来源特征 | 🔴 跳过 | 🟡 快速读 | 🟢 深入读 |
|:--------|:-------|:---------|:---------|
| 发布时间 | > 2 年 | 6 月 - 2 年 | < 6 月 |
| 作者/组织 | 匿名 | 个人博客 | 官方/知名社区 |
| 内容结构 | 无结构/广告 | 有结构但浅 | 有框架+深度 |
| 相关技能 | 不相关 | 部分相关 | 直接相关工具 |
| 代码示例 | 无 | 伪代码 | 可运行代码 |

**规则：** 3 项以上 🟢 → 深入读。3 项以上 🔴 → 跳过。混合 → 快速读关键部分。

## Step 0a️⃣ 已有知识校验（避免重复创建）

学新东西之前先查知识库里有没有。**避免花费 30 分钟产出已存在的内容。**

```python
# 实际执行流
search_files("*.md", target="files", path="~/wiki/wiki/concepts/")
# 看输出的文件名列表——已有概念一目了然

search_files("*.md", target="files", path="~/wiki/wiki/methods/")
# 看输出的方法列表

# 如果新来源的主题和某概念页重叠
#  → 不是创建新页面，而是追加到现有页面
#  → 在 log.md 记录"更新"
#  → 在摘要里说明"本内容已追加到 [[已有概念]]"

# 如果新来源有独特贡献
#  → 只在已有页面中新增这一段
#  → 在前言标注"新增于 {来源}"
```

**内部合成模式下的 Step 0a**（filesystem-only）：
- 不只查 wiki/concepts/ 和 methods/,还要查 skill/、profiles/*/、memories/、AGENTS.md 等所有可能含相关产物的位置
- **必须建立完整的 source inventory**（不是"看起来对的那一个"）— 见 internal-synthesis-mode.md

### Step 0c 必要性验证 — "该不该做"门控（防止沉没成本推销）

**触发条件**：用户问"要不要装X/上X/做X"或 Agent 自己准备推广一个新工具/系统/范式时。

**核心原则**：在产出 wiki 四件套（concept/method/workflow/AGENTS.md）**之前**，先做一次"必要性验证"。这是过去 Hindsight 案例（用户明确要求卸了重评）暴露的**最大方法论漏洞**：原 6 步法只问"怎么装"，不问"该不该装"。

**6 问清单**（每问必须诚实回答，不能包装）：

```
□ 1. 痛点真实吗？
   用户的实际工作流里这个痛点多久出现一次？(低频=不必要)

□ 2. 边际价值多少？
   装上后比现状好在哪里？是"5% 增量优化"还是"不可替代"？

□ 3. 替代方案是什么？
   现有栈里有什么已经能覆盖？(LCM/session_search/wiki/Obsidian)
   答案如果是"完全覆盖"→ 装 = 0 价值

□ 4. 真实成本是多少？
   不要只看"装一次多少磁盘"——要算"每月多少 tokens/维护/认知负担"

□ 5. 我在推销吗？
   检查自己的语气: 是"诚实推荐"还是"找理由证明它好"?
   如果包装成"业界共识"/"必需组件"→ 立即停

□ 6. 退出成本多大？
   如果半年后想卸, 能卸干净吗? 配置/数据/习惯迁移成本?
   退出成本高 = 装的时候更要谨慎
```

**决策矩阵**：

| 评估结果 | 行动 |
|---|---|
| 痛点 ≤ 1次/周 + 有替代 + 边际价值 < 30% | **不装**——记录到 wiki 为"已评估，结论不装" |
| 痛点 1-3次/周 + 无明显替代 | 装，**但仅当 tool 用**，不主动化 |
| 痛点 > 3次/周 + 不可替代 | 装 + 主动化 (cron/钩子) |
| 评估后发现"我被沉没成本绑架" | 卸，重评 |

**真实案例（2026-06-02 → 2026-06-03 Hindsight 完整装卸循环）**：

完整 5 阶段：

| 阶段 | 我做的事 | 用户反应 | 教训 |
|:----|:---------|:--------|:----|
| 1. 探勘 + 4 件套 | 推荐"4-Tier 架构 + Hindsight 主动化" | "全面拥抱 Hindsight" | 推销过快 |
| 2. 加 cron + skill | 注册 2 个 cron + 主动化 skill | "已重启" | 用户没拒绝，可能不是真的认同 |
| 3. 第一次反思 | "诚实评估是否必需" | "全删 cron" | 触发了"装上就开始烧 token"的反弹 |
| 4. 彻底卸载 | pip + 数据 + wiki 全清 | "好" | 用户愿意从头开始 |
| 5. 重新探勘 | 用 ai-harness-exploration 客观评估 | 选 B：升级 LCM，**不装 provider** | 真实需求是"升级 LCM" 不是"装 Hindsight" |

**关键洞察**（比 6 问清单更深）:

1. **"主动化"是 Hindsight 案例的关键失分点**——装上但手动调, 价值边缘. **主动化后**变成后台烧 token 的噪音源, 用户立即反弹. **Agent 推任何"自动化"前必须算 ROI**: 每次 retain 烧 3000-5000 tokens × 每天几次 × 30 天 = 几十万 tokens/月. **2026-06-04 更新**: minimax m3 订阅制量大管饱 → token 成本不再是主因, 但"主动化失控"的用户偏好 (沉没成本 / 反弹信号) 仍是真因. **该不该主动化的判断从"烧不烧得起 token" 转为 "用户能否接受被动接受结果"**.

2. **"价值评估时机"应该在装之前**——但用户实际体验中**装 → 用 → 重评** 的循环是正常的（因为不上手不知道真价值, Hindsight 案例完整证明了这一点). **Agent 的责任**是：用户开始怀疑时（"评估一下"）, 立即停止辩护, 开启重新评估. **不要 defend sunk cost**.

3. **用户的触发信号有规律**（Hermes 用户偏好）—— **看到立即停推销**:
   - "评估一下到底有没有必要" → 立即停止推销, 切换到 Step 0c 诚实评估
   - "重新审视 X" → 推翻之前决策, 重做必要性门控
   - "诚实评估" → 期待 Agent 承认过度推荐, 立即写诚实报告 (列 ROI/替代/退出成本)
   - "先卸了再调查" / "彻底卸载再重新探勘" → 全面重评, 保留 .bak 退出路径
   - "装 + 测 + 卸" 循环是正常预算, 不是失败

   这 4 个信号出现 = 立即切换到 Step 0c, **不要继续推销**. 红旗语言 ("业界共识"/"必需"/"最佳实践") 也算, 立即停.

**4. **"装了 1 周内不用 = 卸" 启发式**（Hindsight 案例提炼）:
   - 装上后 7 天内没有"自然想起用它" → 边际价值 < 维护成本
   - 用户不会主动卸（沉没成本心理），Agent 应主动提"卸不卸？"

5. **"装了 + 主动化后反弹" 是更深一层的 5 阶段** (Hindsight 案例 2.0 提炼):
   - 阶段 1: 推销 (4-Tier + Hindsight) — 易反弹
   - 阶段 2: 加 cron + 主动化 (2 cron + skill) — **必反弹** (用户偏好)
   - 阶段 3: 反思 (诚实评估) — 转折点
   - 阶段 4: 卸载 (保留 .bak) — 用户奖励 Agent 反思
   - 阶段 5: 重新探勘 (走官方路径) — 找到真实价值 + 隐藏风险 (内存泄漏, 主动化陷阱)
   - **第 2 轮探勘才出真知** (官方文档 + 实际部署). 仅读文档不部署 = 看到的是商家口径, 不是真实价值.

**教训**：原 6 步探勘法的 Step 0 只评估"来源质量",不评估"是否值得为此建系统"。新增 Step 0c 修正这个漏洞。

**关键失败信号**（遇到立即重评）：
- 自己说"业界共识"/"必需" → 包装
- 没算 token 成本就推荐 → 推销
- 替代方案只用 1 句话打发 → 偏袒
- 用户问"必要性" → 立即诚实评估，不要辩护
- 推荐"主动化" 没算 ROI → 100% 过度推销
- **一次性推销 ≥ 2 个新工具/仓库/库** → 立即停推销，对**每个**都做 6 问，**不批量包装**（2026-06-04 真实案例：3 仓库推销 superpowers-zh/gstack/gbrain，11 个红旗信号 + 6 问全"否"= 拒绝安装）
- **"你赢 ≠ 沉默"** → 用户说"我倾向多写"不是"我一定对"；看到重复模式第 2 次应主动警告（错误账本：4 ahead commits AI 越权自己没察觉 = 反身性失败）

### Step 0b 来源多样性检查（避免回声室）

在投入深入分析前，快速评估来源的视角多样性：

```
□ 来源与已有知识库中的观点一致？→ 确认已掌握的内容
□ 来源与已有知识库中的观点冲突？→ 💎 最有价值！（记录冲突）
□ 来源的视角属于哪个"圈子"？
   ├─ 学术界（arXiv/论文）
   ├─ 工业界（公司博客/案例研究）
   ├─ 独立开发者（个人博客/长篇）
   └─ 社区（Reddit/HN/论坛）
   
规则：
  3 个以上来源中，至少覆盖 2 个不同的"圈子"
  如果所有来源来自同一圈子 → 需补充搜索其他圈子的观点
  如果某个圈子完全没有覆盖 → 这是有价值的新视角
```

**实际案例：** deusyu/harness-engineering 的 19 篇文章来自学术界（Stanford）、工业界（OpenAI/Anthropic/LangChain/GitHub）、独立开发者（Fowler/deusyu）、社区（YDD）。覆盖了全部 4 个圈子，所以分析特别全面。

```
来源A 讲了 XXX 概念
来源B 也讲了 XXX 概念（不同名字，同一回事）

→ 不是创建两个概念页
→ 是识别出"这就是同一件事"
→ 在一个方法页中记录"这两个来源描述同一现象" 
→ 保存为 [[concepts/xxx-cross-source.md]]（交叉引用页）

来源A + 来源B 的部分重叠 + 部分互补

→ 重叠部分 → 追加到已有概念页（标注两个来源）
→ 互补部分 → 创建单独的方法页或概念扩展页
→ 在 index.md 中加交叉链接

来源A 讲的概念与已有知识完全重复

→ 不创建任何页面
→ 只在 log.md 记一笔"来源A 的内容已被 [[已有页]] 覆盖"
→ 避免重复劳动
```

**实际案例**（本会话中）：OpenAI 的 "Prompt-in-Loop" 和 Mitchell 的 "P0 Harness"

```
第 1 个来源（OpenAI）：
  创建了 concepts/codex-harness-guide.md

第 2 个来源（Mitchell）：
  检查 concepts/ 目录 → 发现 codex-harness-guide 已存在
  → 把 Mitchell 的 P0 追加到同一 pages 的不同 section
  → 不是创建新页面，是扩展

最终：1 个概念页 + 1 个对比方法页，不是 2 个独立页面
```

**内部合成模式下的多源类型学（taxonomy）建立** — 与 web 探勘的"多圈子检查"类似,但分类维度不同:
- 相同内容多副本（典型：worker 7 份 SOUL.md）→ 识别后**不重复利用**
- 不同类型（identity / operational / template）→ 互补,提取各类型特色
- 显式 vs 隐式（明确文档 vs 嵌入在代码注释）→ 都需要覆盖

### 知识成熟度模型（confidence 升级路径）

每个 wiki 页面不是一蹴而就的。随着更多来源验证，confidence 应自动升级。不是一个静态值。

```
第一来源 → 创建概念页
  confidence: medium（单源，需要验证）
  sources: [来源A]

第二来源证实 → 追加到现有页
  confidence 升级到 high
  sources 追加 [来源A, 来源B]
  log.md 标注"多源支持"
  如果两个来源使用不同术语描述同一现象 → 创建方法页记录"同义不同名"

第三来源反驳 → 标记冲突
  confidence 降级或保持 medium
  contested: true
  contradictions: [source-name]
  log.md 标注"有冲突观点"

三源以上且一致
  → 创建 methods/xxx-cross-source.md（交叉引用页）
  → 记录"多个来源独立描述同一模式"
  → index.md 添加交叉链接
```

**规则：** 每次有新来源涉及已有概念时，不自动升级 confidence。先判断新来源是否可靠（Step 0 质量评估），再判断是否与已有内容一致或冲突。只有**可靠+一致**才升级。

**frontmatter 最佳实践：**
```yaml
# 第一来源（新创建）
confidence: medium

# 第二来源证实后（更新）
confidence: high
sources: [来源A, 来源B]

# 发现冲突后（更新）
confidence: medium
contested: true
contradictions: [other-page]

# 三源以上交叉引用（更新+新建方法页）
confidence: high
sources: [A, B, C, ...]
# 同时创建 methods/xxx-cross-source.md
```

**实际案例：** 本会话中 Fowler 控制论框架先从一个来源（deusyu 仓库的翻译）获得 → confidence: medium。之后读到更多来源（Fowler 原文、Böckeler 文章）证实 → 升级到 high。记录了多源交叉引用页。

---

## Step 1️⃣ Analyze（分析）

从新来源中提取**核心原理**。

### 子步骤

```
1.1 理解来源基本结构
  ├─ 什么类型的资源？(文章/仓库/工具/教程)
  ├─ 目标受众是谁？
  └─ 核心主张是什么？

1.2 **外部搜索补充 — 4 轮递进搜索法**（新！增强版）

搜索不是一次性的，而是分 4 轮递进。每轮有明确的目标和门控条件：

```
Round 1: 广撒网（2-3 次）
  目的：理解基本概念和范围
  方法：
    ├─ `web_search("{核心术语} 概念 / 是什么 / introduction")` → 概念扫盲
    └─ `web_search("{核心术语} 2026 / latest / news")` → 最新动态
  产出：3-5 个关键 URL，1 个初步理解
  ⚠️ **web_extract 试探**：先发 1 个试探看网关是否可用
       → 成功 → Round 2 可批量 web_extract
       → Blocked → 改用 browser + web_search 补充
  门控：找到了 3+ 个独特来源？→ 进入 Round 2
        找不到？→ 换搜索词：加限定词 / 换语言 / 换同义词
        优化 2 次仍无结果 → 四路并发(mcp_minimax + Tavily MCP google/microsoft/ggc,见 § 9.0.2 实际决策树)

Round 2: 深挖（3-4 次）
  目的：深入理解关键方面
  方法：
    ├─ `web_search("{名} best practices / architecture / production")` → 最佳实践
    ├─ `web_search("{名} criticism / limitations / pitfalls / 缺点")` → 批判视角
    ├─ `web_search("{名} vs / comparison / alternatives")` → 对比分析
    └─ `web_search("{名} case study / 实战 / 踩坑")` → 实战案例
  产出：每个方向 1-2 个高质量来源
  门控：观点覆盖了 70% 以上已知维度？→ 进入 Round 3
        发现重大分歧 → 额外搜 1 次验证，标注 contested

Round 3: 交叉验证（1-2 次）
  目的：验证关键观点和数据的可靠性
  方法：对争议点和关键数据做定向搜索
    ├─ `web_search("{争议术语} evidence / research / paper")` → 学术验证
    └─ `web_search("{关键数据} source / origin / 来源")` → 数据溯源
  产出：确认/修正已提取的观点
  门控：所有主要观点都有来源支持？→ 进入 Round 4
        有未解决的矛盾 → wiki 标注 contested: true

Round 4: 补漏（0-1 次）
  目的：检查是否有遗漏维度
  方法：宽泛查询确认无重大遗漏
  产出：确认理解完整
  门控：理解已完整？→ 开始 Analyze 下一步
        发现新维度 → 回到 Round 2 追加
```

**搜索总次数控制在 6-10 次。超过 10 次仍未理解 → 切换策略（太复杂，先建基线再深入）。**

**内部合成模式跳过本节** — 用 `read_file` 群读替代 web 搜索,见 references/internal-synthesis-mode.md。

### 并行搜索模式（合并版）

当需要 3+ 方向同时搜索时，用 `delegate_task` 并行。当前可用两个 Tavily 实例（各 1000次/月），并行搜索时可同时使用分摊配额。

```python
# 基础并行：3 路搜索，各方向独立
delegate_task(tasks=[
    {"goal": "搜索来源A的最佳实践", "toolsets": ["web"]},
    {"goal": "搜索来源A的批判视角", "toolsets": ["web"]},
    {"goal": "搜索来源A的实战案例", "toolsets": ["web"]},
])
```

#### 并行模式选择（3 种策略）

| 模式 | 适用场景 | 任务数 | 墙钟时间 | Tavily 配额消耗 |
|:----|:--------|:-----:|:--------|:--------------|
| 🚀 **快速并行** | 用户说"尽量快"、只是扫盲 | 3 个 | ~30s | 3 次（单 key） |
| 🎯 **标准并行** | 默认，平衡速度与深度 | 3 个 | ~60s | 3 次（单 key） |
| 🧠 **深度并行** | 需要多角度全量分析 | 3-4 个 | ~120s | 最多 6 次（双 key 分摊） |

**快速并行** — 每个子代理只搜 1-2 次，只返回关键点摘要
```python
delegate_task(tasks=[
    {"goal": "快速搜索: {topic} 关键信息", "toolsets": ["web"]},
    {"goal": "快速搜索: {topic} 实际案例", "toolsets": ["web"]},
    {"goal": "快速搜索: {topic} 缺点/陷阱", "toolsets": ["web"]},
])
```

**深度并行** — 每个子代理搜 3-5 次，跨实例用双 Tavily key 分摊配额

⚠️ **前置校验（防止空转）：** 深度并行会消耗 30+ 次搜索配额。发车之前先做 1 次快速校验确认主题存在：

```python
# 前置校验：1 次搜索确认主题可查
quick_check = web_search(f"{topic}")
if not quick_check or len(quick_check.get("data", {}).get("web", [])) < 1:
    # 主题不存在 → 降级为快速分析，不启动深度并行
    run_quick_analysis(topic)
    return  # 避免浪费 30+ 次配额
# 注意：即使主题不存在，对比/生态方向的子代理仍可能产出有价值的竞品对比。
# 如果前置校验确认不存在的主题你还想深挖周边，改用标准并行（3 次配额）开 1 路对比方向
```

```python
delegate_task(tasks=[
    {"goal": "深入搜索: {topic} 架构/设计/原理，至少搜3次", "toolsets": ["web"]},
    {"goal": "深入搜索: {topic} 生产实践/踩坑/性能，至少搜3次", "toolsets": ["web"]},
    {"goal": "深入搜索: {topic} 对比/替代/生态，至少搜3次", "toolsets": ["web"]},
])
```

#### 结果合并策略

子代理返回后需做系统化合并，不是简单拼接：

```python
def merge_parallel_results(results):
    """合并并行搜索结果"""
    merge_strategy = {
        # 方向 1: 提取关键概念和框架 → 创建概念页核心
        "组织架构": lambda r: extract_framework(r),
        
        # 方向 2: 提取具体数据和案例 → 扩展概念页
        "填充数据": lambda r: extract_examples(r),
        
        # 方向 3: 提取对比和批判 → 追加"局限"章节
        "添加限制": lambda r: extract_limitations(r),
    }
```

**部分价值模式（重要！）** — 首个子代理确认主题不存在时，其他子代理仍可能有产出：

```
场景: 深度并行 3 路
  子代理 #1 (架构)  → "仓库404，主题不存在"
  子代理 #2 (实践)  → "无生产证据，主题不存在"
  子代理 #3 (对比)  → "竞品对比完整数据"

实际发生: 所有子代理 completed (failure_count=0)
          但内容上 2/3 是"不存在"结论，1/3 有实际价值

处理规则:
  ├─ 所有子代理 completed → 正常合并，不触发兜底
  ├─ 合并时检查每个子代理的内容是否有实际提取物（不是只有"不存在"结论）
  ├─ 有产出的子代理 → 正常提取（示例中的 #3 对比数据）
  ├─ 无产出的子代理 → 记一笔"主题不存在，已跳过"
  └─ 最终产出可能不是预期的概念页，而是周边生态分析或竞品对比

实际案例（2026-05-29 实测 corona 框架）:
  #1 架构方向: 8 次搜索 → 确认 github.com/apache/corona 不存在
  #2 实践方向: 6 次搜索 → 无生产证据
  #3 对比方向: 6 次搜索 → Airflow/Beam/Dagster/Prefect/Temporal/Kestra 完整对比
  合并结果: corona 概念页降级为 confidence: low，追加竞品对比表
  配额消耗: 37 次 web_search（其中约 3-6 次触发 Tavily 后端）
  墙钟: 62s
```

**上下文溢出防护：**
```
当前 provider: deepseek-v4-flash，上下文窗口 ≈ 128K tokens
  3 路并行每个子代理返回 ~2000 tokens → ~6K tokens（安全）
  3 路并行每个子代理返回 ~8000 tokens → ~24K tokens（安全）
  3 路并行每个子代理返回 15000+ tokens → ~45K+ tokens（⚠️ 需要压缩）

安全规则：
  ├─ 单个子代理返回 > 5000 tokens → 用 extract_framework 压缩再合并
  ├─ 3 路子代理总返回 > 30000 tokens → 总结每个方向，不保留原始内容
  └─ 子代理 goal 中加"只返回关键点摘要，不要原文"
```

#### Tavily 432 自恢复机制（优先MCP通道，MCP配额独立于REST）

当 Tavily 返回 432（配额超限）时，不要报告失败，立即自动切换到 key2：

```python
# ⚠️ 2026-06-04 实测警告:Tavily REST key 实际失效(401),不是 432
# 下面函数仍可用但实际跑不通。优先用 MCP 通道(详见 § 9.0.5)。

def tavily_search_with_fallback(query, max_results=5):
    """Tavily REST 搜索,含 432 切 key2(2026-06-04:实测 REST 401,优先用 MCP)"""
    import httpx, os

    # 先用 key1(默认 TAVILY_API_KEY)
    api_key = os.getenv("TAVILY_API_KEY", "")
    response = _try_tavily_request(api_key, query, max_results)

    # 432 配额超限 → 切 key2
    if response and response.get("status_code") == 432:
        api_key2 = os.getenv("TAVILY_API_KEY_2", "")
        if api_key2:
            response = _try_tavily_request(api_key2, query, max_results)

    # 401 鉴权失败(2026-06-04 实测状态)→ 立即退出,改用 MCP
    if response and response.get("status_code") == 401:
        return {"success": False, "error": "Tavily REST 401 Unauthorized, use MCP instead",
                "fallback": "mcp_tavily_mcp_google_tavily_search", "data": {"web": []}}

    if not response or not response.get("results"):
        return {"success": False, "error": "Tavily exhausted", "data": {"web": []}}

    return _normalize_tavily_search_results(response)


def _try_tavily_request(api_key, query, max_results):
    """尝试 Tavily REST。返回 JSON 响应或 None。"""
    if not api_key:
        return None
    try:
        import httpx
        resp = httpx.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "max_results": max_results},
            timeout=30,
        )
        if resp.status_code in (432, 401):
            return {"status_code": resp.status_code,
                    "error": "432 quota" if resp.status_code == 432 else "401 auth"}
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None
```

**Worker 执行路径**(2026-06-04 更新):Workers 的 `web.search_backend: tavily` 配置在 v6.12.0 之前是预期的 REST 通道。但实测 401 = **REST 通道当前不可用**。Workers 应改用 MCP 通道:
- 改 web.search_backend 留空 → web_search 仍走 Tavily REST(同样 401)
- **正确做法**:在 Worker prompt 里直接调 `mcp_tavily_mcp_google_tavily_search()` 等 MCP 工具,绕过 web_search



```
Worker 搜索流程（MiniMax MCP优先 + Tavily MCP×4 + DuckDuckGo 五重兜底）：
  第1层: mcp_minimax_web_search(query) → MiniMax MCP（150次/5h，CJK最佳）
  第2层: mcp_tavily_search(query) → Tavily MCP Google/Microsoft/GGC（3独立key，MCP配额独立，~0.3s）
  第3层: web_search(query) → DuckDuckGo (免费)
  第4层: terminal(f"curl ...") → Tavily REST key1 (TAVILY_API_KEY, 1000次/月)
  第5层: terminal(f"curl ...") → Tavily REST key2 (TAVILY_API_KEY_2, 1000次/月)
  输出: 先到先得，去重合并

Worker 注意事项：
  - MiniMax MCP 优先，150次/5h，用完等待冷却
  - Tavily MCP 备用（3独立key，MCP配额独立于REST），仅MiniMax冷却时用
  - MCP与REST配额独立：即使REST 432，MCP通道依然正常
  - web_search 后端 = tavily（config.yaml中 web.search_backend: tavily）
  - web_search 返回 432 → 不是MCP问题，是REST单独耗尽
  - 如全部失败 → 报告"网络搜索暂时不可用"
  - tavily-mcp-github key已耗尽(432)，不要优先使用
```

#### 配额感知并行

Tavily 双实例各 1000 次/月（每月 1 号自动重置），并行搜索时可感知配额状态做优化：

```
月初(1-10日): MCP配额充足 → 标准/深度并行，MCP引擎全量使用
月中(11-20日): MCP配额中等 → 标准并行，优先 mcp_minimax + Tavily MCP
月末(21-月底): MCP消耗多 → 降级为 mcp_minimax (无限额) + DuckDuckGo
REST全月: 仅在MCP全灭时使用（REST配额与MCP独立）
MCP优先规则: 即使REST 432，MCP通道依然正常工作
紧急情况: MCP google/microsoft/ggc 3个独立key分摊
```

#### 容错与超时处理

`delegate_task` 子代理可能超时/空搜索/无结果：

```python
def parallel_search_with_fallback(directions):
    """并行搜索 3+ 方向，含超时容错"""
    tasks = [
        {"goal": f"搜索: {dir}", "toolsets": ["web"]}
        for dir in directions
    ]
    results = delegate_task(tasks=tasks)
    
    # 容错处理
    failure_count = sum(1 for r in results if r.status != "completed")
    
    if failure_count == 0:
        # 全部成功 → 合并合成
        results = merge_parallel_results(results)
    elif failure_count <= len(tasks) * 0.5:
        # 部分失败（≤ 50%）→ 用已有结果
        # 失败方向标记"未找到可用信息"
        warnings = [f"⚠️ 方向 '{dir}' 无返回"]
        results = merge_parallel_results([r for r in results if r.status == "completed"])
    else:
        # 多数失败（> 50%）→ 视为引擎故障
        run_fallback_strategy()
```

**超时信号：** 子代理 > 60 秒无返回 → 大概率超时（默认 180 秒）。60 秒后准备替代方案，不干等。

#### 并行度规则（合并版）

```
基本情况:
  ├─ 3 个任务 → 最推荐（平衡速度、token 成本、配额消耗）
  ├─ 4 个任务 → 可接受（用户明确说要多方向）
  ├─ > 4 个 → 分批执行：先 3 个，再搜遗漏方向
  └─ 全量探勘用标准并行，快速分析**绝不用**并行

Token 成本意识:
  ├─ 3 路并行 ≈ 3x token 消耗
  ├─ 收益: 墙钟节约 60%+
  ├─ 风险: 上下文溢出（参考前述防护规则）
  └─ 仅在分析阶段使用，extract/formalize/verify 阶段用串行

Tavily 配额意识:
  并行每日配额 = 2 × 1000 / 30 ≈ 66 次/天
  一次标准并行 ≈ 3 次
  每天最多 ~22 次标准并行（配额安全边界）
  日均 10+ 次并行 → 切换部分到 DuckDuckGo web_search
```

### 全引擎故障兜底策略（并发全灭时使用）

极少数情况下所有引擎全部无结果。此时不要空手返回，执行以下兜底：

```
第 1 层：MCP并发（默认策略）
  ┌─ mcp_tavily_search (Tavily MCP google/microsoft/ggc - 3独立key, MCP配额)
  ├─ mcp_minimax_web_search (MiniMax MCP - 无限额)
  ├─ web_search (DuckDuckGo - 免费)
  ├─ tavily REST key1 (1000次/月)
  └─ tavily REST key2 (1000次/月)
  MCP通道优先于REST，同时发出，先到先用，去重合并

如果五路并发全部无结果：
  全部失败后不重复尝试，改用替代策略：
  ├─ 搜索词过窄 → 放宽：去掉限定词/用更宽泛的上位词
  ├─ 搜索词过宽 → 收窄：加限定词/加时间范围/加具体场景
  ├─ 中文关键词无结果 → 换英文关键词再试 1 轮
  └─ CJK 短词无结果 → 组 4-6 字长词组（"模型上下文" 而非 "MCP"）

第 3 层：来源回退（2 分钟）
  如果搜索引擎确实全灭，改用已知知识库：
  ├─ session_search + lcm_grep（过去会话中有无讨论此主题）
  ├─ wiki/concepts/ 和 wiki/methods/（已有知识能否覆盖）
  └─ 如果确实完全陌生且无结果 → 报告用户"此主题目前无公开可用信息"

第 4 层：兜底交付（1 分钟）
  ├─ 返回已知知识库中最相关的主题 + 已有内容的链接
  ├─ 建议用户提供更具体的搜索词
  └─ 追加到用量追踪（全引擎故障标记）
```

**规则：** 第 1-2 层 2 分钟内完成。第 3 层 2 分钟内完成。总耗时不超过 5 分钟。超时仍未找到 → 正常结束，不空耗。

搜索结果质量评估标准：

| 指标 | 🟢 高质量 | 🟡 可接受 | 🔴 低质量 |
|:----|:---------|:---------|:---------|
| 域名 | .edu / 官方 / 知名作者 | 技术博客 | SEO 农场 |
| 时效 | < 6 月 | 6 月-2 年 | > 2 年 |
| 深度 | 全量+数据 | 有结构 | 表面 |
| 客观 | 平衡 | 有偏向有数据 | 纯推广 |

3+ 高质量 → 高置信度。1-2 高质量 + 多个可接受 → 中置信度。全部低质量 → confidence: low。

CJK 搜索技巧：中文无结果 → 混合英文关键词，短汉语词用长词组替代。

详细搜索策略见 `references/search-depth-strategy.md`

### 并发搜索的结果合并规则

默认策略:**先 MCP 后 terminal curl**,4 路 MCP 顺序 + 3 路 curl 兜底。MCP 通道返回优先(2026-06-04 实测:web_search REST 401 不可用,DuckDuckGo 国内不通,详见 § 9.0):

```
                        ┌─ mcp_minimax_web_search (MiniMax MCP, 150次/5h, CJK最佳, ✅ <1s)
                        ├─ Tavily MCP Google (tavily-mcp-google, 独立key ✅ 0.82s)
  同一关键词 ──优先MCP──┼─ Tavily MCP Microsoft (tavily-mcp-microsoft, 独立key ✅ 0.78s)
                        ├─ Tavily MCP GGC (tavily-mcp-ggc, 独立key ✅ 1.05s)
                        ├─ Tavily MCP GitHub (tavily-mcp-github, key已432 ❌ 备用)
                        ├─ terminal curl GitHub raw (200, 仓库 README 兜底)
                        ├─ terminal curl arXiv (200, 学术论文兜底)
                        ├─ terminal curl Bing (302, 通用 web 兜底)
                        ├─ web_search (Tavily REST, 当前 401 ❌ 跳过)
                        └─ terminal curl DuckDuckGo (国内超时 ❌ 跳过)
                                ↓
                        4 路 MCP 主搜(顺序跑,先到先用),terminal curl 兜底
                        MCP通道优先于terminal,MCP 与 REST 配额独立
                        去重后按质量排序输出
                        详见 § 9.0.2 实际 fallback 决策树
```

  ├─ `mcp_tavily_search(google)` → Tavily MCP Google（独立key, ✅ 0.58s）
  │   MCP通道优先于REST，配额独立，REST 432不影响
  │   适用：英文搜索、技术文档、通用场景
  │
  ├─ `mcp_tavily_search(microsoft)` → Tavily MCP Microsoft（独立key, ✅ 0.59s）
  │   同MCP通道，独立配额不共享
  │   适用：技术栈/企业场景搜索
  │
  ├─ `mcp_tavily_search(ggc)` → Tavily MCP GGC（独立key, ✅ 0.71s）
  │   同MCP通道，独立配额不共享
  │   适用：通用搜索，备用
  │
  ├─ `mcp_minimax_web_search` → MiniMax MCP 搜索（无配额限制）
  │   MCP主力引擎之一，CJK 搜索效果最佳
  │   全年无限额，MCP通道
  │
  ├─ `mcp_tavily_search(github)` → Tavily MCP GitHub（key已432 ❌ 备用）
  │   key与web_search REST共享，已耗尽
  │   仅在其他MCP全灭时尝试
  │
  ├─ `web_search` → DuckDuckGo（免费，回退用）
  │   默认引擎，适用通用场景
  │   仅在MCP通道无结果时使用
  │
  ├─ `tavily REST key1` → Tavily REST（1000次/月，仅MCP全灭时）
  │   REST配额与MCP独立，432不影响MCP
  │   适用: 结构化结果、引用来源优先
  │
  ├─ `tavily REST key2` → Tavily REST备用（1000次/月，key1 432时回退）
  │   独立REST key

**R1 广撒网门控更新(2026-06-04 修正 — 4 路 MCP + 3 路 terminal curl,详见 § 9.0.5):

并发搜索的结果合并规则:
```python
# 4 路 MCP + 3 路 terminal curl 兜底(2026-06-04 实测版)
import httpx

results = []
# 4 路 MCP(独立 key,MCP 通道优先)
r1 = mcp_tavily_mcp_google_tavily_search(query=query, max_results=5, search_depth="basic")
r2 = mcp_tavily_mcp_microsoft_tavily_search(query=query, max_results=5, search_depth="basic")
r3 = mcp_tavily_mcp_ggc_tavily_search(query=query, max_results=5, search_depth="basic")
r4 = mcp_minimax_web_search(query=query)   # 主力,中文强
# ⚠️ web_search(Tavily REST) 当前 401,跳过
# ⚠️ DuckDuckGo 国内超时,跳过

# 去重合并
seen_urls = set()
merged = []
for r in [r1, r2, r3, r4]:
    if not r: continue
    items = r.get("results", []) if isinstance(r, dict) else r
    for item in items:
        url = item.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            merged.append(item)

# MCP 全灭时 → terminal curl 兜底
if not merged:
    try:
        r = httpx.get(f"https://www.bing.com/search?q={query}",
                      headers={"User-Agent": "Mozilla/5.0"},
                      follow_redirects=True, timeout=15)
        if r.status_code == 200:
            merged.append({"title": f"Bing: {query}", "url": "https://www.bing.com",
                          "content": r.text[:3000], "_source": "bing_curl"})
    except: pass

# 按质量排序:官方/知名 > 社区 > 博客
print(f"4 路 MCP + 兜底返回 {len(merged)} 个去重结果")
```
  │
  ├─ `web_extract` → 提取文章全文
  │   ⚠️ 批量 web_extract 全部返回 "Blocked"：
  │      → 飞书/网关级限制，非目标站点问题
  │      → 切换策略：browser 替代，web_search 补充 snippets
  │      → 设计模式：先 1 个试探，成功再批量发送
  │
  ├─ `browser` → 浏览器渲染（JS 页面/登录墙/反爬）
  │   适用于：web_extract 失败、动态页面、需要交互
  │   注意：运行无代理，部分站点会检测 bot
  │
  ├─ 学术查询 → 同时 `web_search`(arxiv) 和常规搜索
  ├─ 需要长时间监控 → `blogwatcher`（RSS 订阅）
  ├─ 回查过往内容 → `session_search`（其他会话）/ `lcm_grep`（本会话）
  │
  ├─ **GitHub 访问镜像替补规则**
  │   **首选直连 github.com**，直连不可用时才尝试替补方案。
  │
  │   替补方案（2026-05-29 实测有效）：
  │
  │   【方案 D】Git 全局代理（推荐长期方案）
  │     `git config --global url."https://ghproxy.net/https://github.com/".insteadOf "https://github.com/"`
  │
  │   【方案 A】文件代理 — 仅终端
  │     `git clone https://ghproxy.net/https://github.com/org/repo`
  │     `curl -L https://ghproxy.net/https://raw.githubusercontent.com/...`
  │
  │   【方案 B】学院镜像 — 仅 Release
  │     `https://mirrors.tuna.tsinghua.edu.cn/github-release/` 搜项目名
  │
  │   【方案 C】码云镜像 — 仅热门项目
  │     `https://gitee.com/organizations/mirrors/projects`
  │
  │   注：浏览器环境下直连 github.com 是唯一可靠方案，第三方镜像均不可用。

1.3 提取关键概念
  ├─ 3-5 个核心术语
  ├─ 2-3 个关键关系
  └─ 1 个核心模型/框架

1.4 反向工程：为什么作者这样设计？
  ├─ 解决什么痛点？
  ├─ 和竞品有什么不同？
  └─ 什么场景下会失效？

1.5 与已有知识对比（最关键！）
  ├─ 这个新概念和 [[已有概念A]] 是同一回事吗？
  │   如果是 → 方法页记录"这个来源用不同名字描述已知现象"
  │   如果不是 → 关键差异是什么？新在哪里？
  ├─ 这个新工具比 [[已有工具B]] 好在哪里？
  │   如果是特化版 → entity/method 页记录适用场景
  │   如果是超越版 → 方法页记录"已知工具B现在可以被C取代了"
  └─ 这个新工作流和 [[已有方法C]] 的关系？
        如果是互补 → 扩展方法C
        如果是替代 → 记录"C 已过时"

1.6 Guides×Sensors 分析（Fowler 控制论维度）
  ├─ 这个系统提供了哪些前馈（Guides）？
  │   ├─ 计算性前馈（bootstrap/模板/脚手架）
  │   └─ 推理性前馈（文档/spec/constraints）
  ├─ 这个系统提供了哪些反馈（Sensors）？
  │   ├─ 计算性反馈（lint/test/type check/CI）
  │   └─ 推理性反馈（code review/LLM judge）
  ├─ 前馈与反馈是否平衡？
  │   只有前馈 → 规则在真空，无法验证是否生效
  │   只有反馈 → 同样的错重复犯，没有预防
  └─ 结果记入概念页的"控制论映射"小节

1.7 学派定位
├─ 这个来源主要属于哪个学派？
│   ├─ 约束学派（OpenAI/HumanLayer）：聚焦解空间过大，模型不可靠
│   ├─ 架构学派（Anthropic）：聚焦单体设计限制可扩展性
│   ├─ 控制论学派（Fowler/Böckeler）：聚焦前馈与反馈控制失衡
│   └─ 怀疑学派（YDD/METR）：聚焦瓶颈根本不在编码阶段
├─ 不同学派解决不同层次的问题：
│   约束 = 战术层（当前模型可靠性）
│   控制论 = 方法层（系统性约束设计）
│   架构 = 战略层（跨模型代际可维护性）
│   怀疑 = 元层（整个范式是否成立）
└─ 记录在方法页的"学派定位"小节

**SOUL/AGENTS.md/CLAUDE.md 的学派归属**：灵魂/规则文档天然属于**约束学派**子分支——通过给 agent 注入"硬规则"缩小解空间（"我信 6 条 / 反对 6 条 / 拒绝 5 条"）。详细 SOUL 设计范式见 `references/soul-design-pattern.md`（5 范式 / 3 误读 / 1 反身性原则）。

⚠️ 不要只记录新知识。始终与已有知识建立连接。
   这是知识库的价值增量——不是有多少新页面，而是有多少新连接。
```

### 来源类型对应的分析方法

| 来源类型 | 分析重点 | 工具序列 | 搜索轮次 |
|:--------|:--------|:--------|:--------|
| **GitHub 仓库** | README → AGENTS.md → 核心目录 → 一致性检查 | AGENTS.md 导向双通道 + `web_search` (社区评价/类似项目) | R1 |
| **博客文章** | 逐段理解 → 提取关键主张 | `web_extract` (全文) → `web_search` (五方向补充) → 逐段分析 | R1-R2 |
| **工具比较** | 对比维度 → 选型因素 | `delegate_task(并行搜多个来源)` | R2-R3 |
| **教程/指南** | 步骤序列 → 关键技巧 → 陷阱 | `web_extract` → `web_search` (五方向补充) → 结构化提取 | R1-R2 |
| **学术论文** | 方法→数据→结论→局限 | `web_search` 论文搜索 → `web_extract` → `arxiv` → `web_search` 交叉验证 | R2-R3 |
| **内部多份现成产物** | inventory → taxonomy → DRY 决策 | `search_files` + `read_file` 群读（**无 web 搜索**） | 0 — 见 internal-synthesis-mode.md |

### GitHub 仓库双通道分析法

对于结构良好的仓库（有 AGENTS.md），使用 AGENTS.md 导向的双通道：

```
第一通道：结构扫描（5 分钟）
  1. 读 README.md → 理解项目定位和核心概念
  2. 读 AGENTS.md → 了解目录结构和导航规则（渐进式披露！）
  3. 扫目录树 → 识别高价值目录（concepts/ > thinking/ > references/ > tools/）
  4. 检查 scripts/ 和 .github/workflows/ 的一致性脚本
  5. 整理出要深入读的文件清单

第二通道：深度提取（15-30 分钟）
  1. 对每个选定的子目录：
     a. 先读该目录的 AGENTS.md（如果有）→ 了解目录目的和约定
     b. 再读核心内容文件（concept note / thinking / reference）
     c. 记录关键主张和相关链接
  2. 跨目录交叉引用（concept 和 thinking 里的观点是否一致？）
  3. 识别重复/冲突/互补的模式

实际案例（deusyu/harness-engineering）：
  第一通道：
    README → 3.2k★, 6 核心概念, 5 个学习阶段
    AGENTS.md → 一致性检查 C1-C7, 每个子目录有 AGENTS.md
    目录扫 → concepts/ ★ / thinking/ ★ / references/ ★ / tools/ 🟡
  第二通道（3 个并行子代理）：
    子代理 1: 8 个 concept 文件 → Fowler 2×2 + Symphony
    子代理 2: 9 个 thinking 文件 → 4 学派 + 5 张力 + 评估问题
    子代理 3: prompts + references + tools → 19 篇数据库 + 有效提示词
```

### 使用的工具

```python
# 并行版（对于跨多个来源的比较分析）
delegate_task(tasks=[
    {"goal": "分析来源A的核心架构...", "context": "..."},
    {"goal": "分析来源B的工作流...", "context": "..."},
    {"goal": "对比A和B的关键差异...", "context": "..."},
], toolsets=["web", "terminal", "file"])

# 串行版（对于单篇深度文章）
web_extract(urls=[url])        # 获取原文
web_search(keywords...)        # 搜索补充资料 (新！交叉验证和补充背景)
# → 逐段读和分析
# → 提取核心概念

# 内部合成模式（filesystem-only,无 web 搜索）
search_files(pattern="*topic*", target="files", path="~/hermes-all")  # inventory
read_file(path=...)             # 群读（一次多 file）
# → taxonomy 建立
# → 模式分组（不是 web 摘录）
# → DRY 决策（写到哪里 / 不写到哪里 / 反向引用）
```

### 内嵌链接处理（重要！）

来源中的链接分三类，只有**灰色链接**值得打开：

| 链接类型 | 示例 | 处理策略 |
|:--------|:----|:--------|
| 🔴 **冗余链接** | GitHub 仓库底部的 License/Badges | 不打开，纯噪音 |
| 🟡 **辅助链接** | "了解更多→" 外部文档 | 快速扫一眼，不深入 |
| 🟢 **核心链接** | 正文中的关键概念链接、引用的核心资源 | **必须打开**，是本源的有机组成部分 |

**实际案例**（来自 Harness Engineering 仓库学习）：

```
README.md
├── 01-Harness核心概念/           ← 🟢 核心子目录 → 全部深入
│   ├── 01-平台工程到底解决了什么问题.md  ← 🟢 核心
│   ├── 02-用K8s到底有没有必要.md        ← 🟢 核心
│   ...
├── 08-进阶资源/                  ← 🟡 辅助 → 快速扫
└── 10-综合评估/                  ← 🟣 整合用 → 最后看
```

**内嵌链接打开规则：**
- 数量 ≤ 5 个 → 全部打开
- 数量 5-15 个 → 只开 🟢 核心链接（约 40-60%）
- 数量 > 15 个 → 只开最核心的 5-8 个
- 每个子代理 delegate_task 最多开 3 个链接

**不要打开的：**
- 广告链接、赞助商链接
- 外部工具的注册/安装页面
- 同一仓库的不同分支
- 已经读过但换个写法的相似内容

### 💰 成本意识（工具调用不是免费的）

每次探勘都消耗 token。不同的工具耗用不同——了解成本有助于做出更经济的决策：

```
工具调用成本金字塔（从低到高）：

  web_search     → 最低成本，文本返回  ← 优先用
  web_extract    → 中成本，全文提取
  browser        → 高成本，JS 渲染+截图
  delegate_task  → 最高成本，每个子代理 ≈ 独立会话

近似比值（单次调用）：
  web_search(1x) < web_extract(3x) < browser(10x) < delegate_task(30-50x)

实际决策规则：
  ├─ 能用 web_search 解决的问题 → 不用 web_extract
  ├─ 能用 web_extract 解决的问题 → 不用 browser
  ├─ 能用串行 5 次搜索解决的 → 不用 delegate_task 并行
  └─ delegate_task 只在以下情况使用：
      ├─ 需要 3+ 方向独立搜索且墙钟时间敏感
      ├─ 需要独立会话隔离（互不干扰的搜索方向）
      └─ 用户明确要"尽量快"

单次探勘总成本上限：
  全量探勘: ≤ 20 次工具调用（超过 → 表示没找到核心，切换策略）
  快速分析: ≤ 5 次工具调用
  深度延续: ≤ 15 次工具调用
  自我优化: ≤ 30 次工具调用（因为包含验证）
  内部合成: ≤ 10 次工具调用（无 web 搜索,search_files + read_file 为主）

⚠️ 3 路 delegate_task 并行 ≈ 90-150 次串行搜索的 token 成本。
  收益是墙钟时间节约 60%+，代价是 token 消耗 3x。
  仅当用户明确等得起时才用并行。快速分析阶段绝不用。

> **关于以上成本的说明：** "30-50x"（delegate_task vs web_search）指的是工具选择层面——能用 web_search 就 web_search，别用 delegate_task。 "3x"（并行 vs 串行）指的是同一个工具的不同用法——如果必须用 delegate_task，3 路并行比 3 路串行快 60%，但 token 多 3x。两个数字不矛盾，指向不同决策层。
```

---

## Step 2️⃣ Extract（提取）

从分析结果中提取可复用模式。

### 提取维度

```
从来源中提取三类产物：

🧠 概念（Concept）—— 新的思维方式/范式
  │ 例如：Mitchell 的 P0 Harness 层级、Vibe Coding 的上下文分层
  │ 存放：wiki/concepts/xxx.md
  │

⚙️ 方法（Method）—— 可重复执行的步骤序列
  │ 例如：AGENTS.md 写法、Prompt 模板公式
  │ 存放：wiki/methods/xxx.md
  │

🛠️ 工作流（Workflow）—— 工具链组合的最佳实践
  │ 例如：Codex + GitHub Actions CI/CD、Claude Code 多文件编辑
  │ 存放：wiki/methods/xxx.md
  │
```

**内部合成模式下的 Extract**（区别于 web 探勘）：
- 不是从 N 篇文章提取 N 个概念,是**从 N 份现有产物提取 1 套一致的设计**
- 输出**模式清单 + 互补点 + 决策矩阵**(写到哪里/不写到哪里/反向引用)
- 避免"看到 9 份 SOUL.md 就建 9 个 wiki 概念页" — 那是过程不是知识

### 从文章中提取 Prompt 模式

这是最有价值的提取——当一篇文章提到某种提示词技巧时：

```
Step 1: 识别模式类型
  ├─ 角色型（"你是一个XXX专家"）
  ├─ 结构型（"按照以下格式输出：..."）
  ├─ 约束型（"不要做XX，必须做YY"）
  └─ 链式型（"先做A，然后B，最后C"）

Step 2: 形式化为模板
  原始："你是一名资深软件架构师..."
  模板："你是一名{角色}，专门{领域}..."

Step 3: 记录适用场景+模型
  → wiki/concepts/vibe-coding-prompt-system.md
```

### 提取深度评估

不是所有来源都值得深入提取。用这个标准判断：

```
值得全量提取（30-60分钟投入）：
  ├─ 提出了全新的范式/框架（如 P0 Harness）
  ├─ 包含 5+ 个可操作技巧
  └─ 工具/方法可立即在 Hermes 中使用

值得部分提取（10-15分钟投入）：
  ├─ 单篇高质量文章
  ├─ 2-3 个可复用模式
  └─ 概念性知识补充

不值得单独提取（快速阅读即可）：
  ├─ 新闻/产品发布
  ├─ 重复已有知识
  └─ 不适用于当前工作流
```

---

## Step 3️⃣ Formalize（形式化）

把提取的模式固化到技能和方法页。

### 产出模板

#### 产出 A：Skill（可加载的 SKILL.md）

对于**操作型**提取（可执行的步骤序列、工具配置）：

```yaml
---
name: xxx-workflow
description: "从{来源}提取的{工作流/模式/方法}"
emoji: 🧰
version: 5.1.0
author: Hermes Agent (from {来源})
created_by: agent
---

# {模式名}

> 从[{来源}]({url})提取的核心模式

## 何时使用
{触发条件和场景}

## 步骤
{编号步骤列表}
```

#### 产出 B：wiki/methods/xxx.md（方法页）

对于**知识型**提取（对比、分析、指南）：

```
# {方法名}

## 来源
- [{来源}]({url})

## 核心思想
一句话概括

## 关键要点
1. {第一点}
2. {第二点}
3. {第三点}

## 与已有知识的关系
- 与 [[concept-a]] 的关系：...
- 与 [[method-b]] 的关系：...

## 陷阱
- {已知问题1}
- {已知问题2}
```

#### 产出 C：wiki/concepts/xxx.md（概念页）

对于**范式级**提取（新的思维框架）：

```
---
title: {概念名}
created: {日期}
updated: {日期}
type: concept
tags: [相关标签]
sources: [{来源URL}]
---

# {概念名}

## 核心定义
一句话定义

## 原理
{详细解释}

## 与已有概念的关系

### [[概念A]]
{如何关联/冲突/补充}

### [[概念B]]
{如何关联/冲突/补充}

## 实践
{如果有具体实践方式}
```

#### 产出 D：AGENTS.md 模板（可选）

如果提取的模式包含具体的工程环境规则：

```markdown
# AGENTS.md 模板

## 核心原则
1. {原则1}
2. {原则2}

## 规则
- ⚡ {规则1}
- ⚡ {规则2}

## 约定
- {约定1}
- {约定2}
```

### 命名规范

| 产物 | 命名规则 | 示例 |
|:----|:--------|:----|
| Skill | `{动作}-{领域}` | `hermes-workflow`, `vibe-coding-prompt` |
| 方法页 | `{领域}-{方法名}` | `mitchell-working-method` |
| 概念页 | `{领域}-{概念名}` | `harness-engineering` |
| 实体页 | `{工具/人名}-{区分}` | `codex`, `claude-code` |

---

## Step 4️⃣ Deliver（交付）

把成果交付给用户。**核心**:产物写到 wiki,不留在 chat。

### 输出格式

```
## ✅ 探勘完成 — {来源名}

### 📚 产出清单（已落 wiki）

| 类型 | 路径 | 说明 |
|:----|:----|:------|
| 🧠 Concept | wiki/concepts/xxx.md | 核心概念解读 |
| ⚙️ Method | wiki/methods/xxx.md | 可复用的步骤序列 |
| 🛠️ Skill | hermes-xxx | 可加载的技能 |

### 🧩 关键洞察

{用于一句话总结来源的核心价值}
```

### 4.0 Wiki 写入申请流程(2026-06-04 v6.15.0 新增)

> **核心原则**:**任何 wiki 写入前必须征求用户同意**。
> **本节是硬约束** — 不写"应该",写"必须"。

#### 4.0.1 为什么需要申请

- wiki 是持久化资产,写入是**不可逆**操作
- 用户要"知识沉淀"但**不要被"顺手"扩张性写入**
- LCM 摘要、对话历史、agent 产出都不应自动进 wiki
- 边界写入(用户没明示)是隐性风险

#### 4.0.2 必须申请的场景

| 场景 | 申请方式 | 用户拒绝后 |
|---|---|---|
| 探勘产物的最终落 wiki | 列清单 + 候选内容摘要 + 询问 | 写到 `scratchpad/`,不写 wiki |
| 元方法论探勘的派生文件 | 先列 3-5 个候选,问"哪些要写" | 写到 `scratchpad/_drafts/`,标 `draft: true` |
| 更新已有 wiki 页 | 写 diff 摘要 + 询问 | 不更新 |
| LCM 摘要 → wiki | **禁止**(LCM 不知道 wiki) | N/A |
| Session 历史 → wiki | **必须申请**,默认拒绝 | 写到 `scratchpad/` |
| 探勘过程中的中间产物 | **禁止** | 写到 `scratchpad/<task-id>/` |

#### 4.0.3 申请格式(模板)

每次申请 wiki 写入,**必须**用这个格式:

```markdown
## Wiki 写入申请(2026-06-04 14:55)

### 候选清单
| # | 文件 | 类型 | 大小 | 来源 | 用户要求? |
|---|---|---|---|---|---|
| 1 | methods/X.md | method | 5K | web search (3 sources) | ✓ 显式 |
| 2 | protocols/Y.md | protocol | 2K | 我自己提炼 | ❌ 边界写入 |

### 内容摘要(每个文件 1 段)
1. methods/X.md — 介绍 X 的 3 步流程...
2. protocols/Y.md — 加 A2A 协议映射段...

### 建议
- ✓ 推荐:文件 1(用户显式要求)
- ⚠️ 边界:文件 2(我自加,用户没明示)
- 建议只写 1,文件 2 移到 `scratchpad/_drafts/`

### 等用户决定
- 全部写?
- 只写显式?
- 都不写,只放 scratchpad?
```

#### 4.0.4 用户可能的回复

- "写" → 执行写入 + 写 log.md
- "只写 1" → 只写 1,其他移到 scratchpad
- "不写" → 全部移到 scratchpad
- "不写 + 不要提醒了" → 写 "DRAFT-NO-WIKI" 标,后续不再申请(直到用户改主意)

#### 4.0.5 例外(不需要申请的写入)

- 用户**显式说**"写 X 到 wiki/concepts/..."
- 任务中**必然的副作用**(如创建任务页、scratchpad namespace)
- 自测试 / 自检过程的临时文件(写到 scratchpad)

#### 4.0.6 违反协议的后果

- 写 wiki 不申请 = **违反 skill 协议**
- 立刻停手 + 标记 violation + 报告用户
- 不可"事后补申请" — 写入一旦发生就是事实

#### 4.0.7 与 LCM 的边界

```
LCM 压缩归档(lcm.db)
  ↓
lcm_expand / lcm_grep 查
  ↓
看到摘要(只读)
  ↓
❌ 禁止把摘要内容写进 wiki
✅ 摘要本身留在 lcm.db
✅ 如果摘要值得沉淀 → 必须走 4.0.2 申请流程
```

#### 4.0.8 与 scratchpad 的关系

**所有 wiki 写入申请被拒绝的内容,默认归档到 `scratchpad/_drafts/`**:

```
scratchpad/
├── _drafts/                        ← 申请被拒的内容
│   ├── 2026-06-04-method-X.md
│   └── 2026-06-04-protocol-Y.md
├── 2026-06-04-agent-stack-test/    ← 任务 workspace
└── wiki-multi-agent-refactor/      ← 之前任务
```

好处:
- 不丢失探索产物(下次用户改主意可激活)
- 不污染 wiki 主结构
- 清晰的"待写"清单

#### 4.0.9 5 步核验硬协议(2026-06-04 v6.17.0 新增)

> **本节是最高优先级** — 任何 wiki 写入 = commit + push, **必须**走 5 步核验, **不**依赖单一信号("git commit 成功" / "git push up-to-date" 都是不可信信号)。

**本会话真实事件(2026-06-04 17:00)**: commit `e59a9e3` 输出"成功" → `git cat-file -t e59a9e3` 报 "Not a valid object name" → commit **从未存在**。5-6 次类似假成功累积 → 668 行内容从来没真推。**直到 3rd 端 wiki-keeper 跑 commit 迫使我 pull rebase,才发现本地和远端不一致**。

**5 步核验流程(任何 wiki 写入必走)**:

```bash
# Step 1: 看本地变更
git status --short

# Step 2: add 所有
git add -A

# Step 3: commit
git commit -m "..."

# Step 4: 验证 commit 真存在(关键!防假成功 #1)
git log --oneline -1
git cat-file -t HEAD
# ↑ 输出 "commit" = 对象真存在
# ↑ 报错 = commit 从未创建, 假成功!

# Step 5: push + 核验远端 hash(关键!防假成功 #2)
git pull --rebase origin main  # 必先拉, 3rd 可能已推
git push origin main
H_LOCAL=$(git rev-parse HEAD)
git fetch origin main
H_REMOTE=$(git rev-parse origin/main)
[ "$H_LOCAL" = "$H_REMOTE" ] && echo "✅ 推送成功" || (echo "❌ 假成功! 本地=$H_LOCAL 远端=$H_REMOTE"; exit 1)
```

**自动化**:`bash scripts/safe-commit-push.sh "msg"` 一步完成 5 步核验 + 失败自动回滚。脚本位置: `~/hermes-all/wiki/scripts/safe-commit-push.sh` (agent-wiki 仓库内, 所有 agent 共享)。

**5 步核验的核心**: **不依赖任何单一信号**。`git commit` 输出"成功" + `git push` 输出"成功" **不**等于真成功。**必须** commit 对象存在 + 远端 hash 一致。

**用户硬偏好(2026-06-04,作者配置)**:
- 唯一远端仓库: `https://github.com/AK47ZZQ/agent-wiki` (本会话用户明确说"我的仓库是 agent-wiki")
- author name: `Hermes` (用户明确说"上传称名称改为 Hermes")
- author email: `hermes@hermes.local`
- 之前 `wiki-keeper@hermes.local` / `main-claude` / `Hermes 3rd` 三个 author 都不再使用
- **hermes-all 远端已被用户彻底删除**, 不再使用 — 所有内容走 agent-wiki

**11 速查陷阱表**(完整 11 项 + bash 命令见 `references/wiki-write-verification-protocol.md`):

| # | 陷阱 | 信号 | 正确动作 |
|---|---|---|---|
| 1 | `origin/HEAD → main` ≠ main 有内容 | `git log origin/main` 是空 | `git ls-remote --heads origin` 核 hash |
| 2 | `curl 401` | API 鉴权失败 | `git ls-remote` 核 hash (API 401 ≠ push 失败) |
| 3 | `error: src refspec main does not match any` | 本地没 main 分支 | `git branch --show-current` |
| 4 | `non-fast-forward` rejected | 远程有新 commit (3rd 推了) | `git pull --rebase origin main` + 看差异 |
| 5 | push 看起来 hang | 12K+ insertions 慢 | background + `ls-remote` 核 |
| 6 | CWD 是错的 | `pwd` 不在 wiki | `find` 找真 wiki,绝对路径 |
| 7 | **`commit 假成功`**(本会话 e59a9e3) | `git log -1` 报 "Not a valid object name" | `git cat-file -t <hash>` 核对象存在 |
| 8 | **`push 假成功`** | `git push` 报 "Everything up-to-date" 但实际没推 | `git rev-parse origin/main` ≠ `git rev-parse HEAD` |
| 9 | **`push 静默非快进`** | `git push` 输出空, 但本地 ≠ 远端 | 必看 5 步核验 step 5 |
| 10 | **403 Write access not granted** | PAT 没 write 权限 | 改 fine-grained token 权限为 `Contents: Read and write` |
| 11 | **5 步核验后假成功诊断** | local = 远端 = 不同 hash | 跑 `safe-commit-push.sh` 自动诊断回滚 |

**何时必须跑 5 步核验**:**永远**。**反例**(本会话 5 次假成功根因):
- ❌ 觉得"commit 信息简单, 不用核"
- ❌ 觉得"push 输出 up-to-date = 成功"
- ❌ 觉得"wiki-keeper 跑了就 OK, 不用我自己核"

**多 Agent 协作场景(3rd + 主对话)**:两台机器的 wiki-keeper 默认都装本协议(v1.5+)。**3 步必走**(协议 v1.1 § 2):
```
[1] git fetch origin main
[2] git log --oneline origin/main ^main   (看远端领先)
    git log --oneline main ^origin/main   (看本地领先)
[3] git pull --rebase origin main
[4] 5 步核验 + push
```

**冲突时**: 不自动 `--theirs` / `--ours` / `--force` / `--force-with-lease`。写 log 标记 + 通知用户决定(参考 `protocols/git-collaboration-multi-agent` v1.1)。

**`safe-commit-push.sh` 位置**:
- 在 agent-wiki 仓库: `wiki/scripts/safe-commit-push.sh` (v1.5, 4403B, 5 步核验自动化)
- 在 hermes-all 仓库: `hermes/skills/autonomous-ai-agents/wiki-keeper/scripts/safe-commit-push.sh` (同源, v1.5 同步)

### 4 联动:Wiki 落地(2026-06-04 集成)

**为什么**:探勘产物如果只留在 chat,下次无法复用 — 等于浪费。落到 wiki = 第二大脑沉淀。

**何时联动**:
- 全量探勘(15-30 分钟)— **必联动**
- 深度延续搜索(8-12 分钟)— **必联动**
- 内部多源合成(10-15 分钟)— **必联动**
- 快速分析(3-5 分钟)— **可选**(除非结果值得沉淀)
- Meta 自优化(15-30 分钟)— **联动到 skill**

**怎么联动**(4 步):

```
Step 4a: 决定产物类型
  ├─ 跨源综合的"主题" → wiki/concepts/
  ├─ 可复用的步骤序列 → wiki/methods/
  ├─ 工具/框架/模型 → wiki/entities/
  ├─ 工具对比 → wiki/comparisons/
  ├─ 短记录/部署日志 → wiki/notes/
  └─ 范式级新框架 → wiki/methods/(作为新 skill 候选)

Step 4b: 写 frontmatter(9 字段)
  - 必填:title / created / updated / type / tags / source / confidence
  - 选填:contested / contradictions
  - 协议见 wiki/protocols/multi-agent-detail § 5.7

Step 4c: 写正文
  - 1-page overview(不是大段粘贴)
  - ≥ 2 条 wikilink 出链
  - ≥ 1 条可执行步骤(如果是 method)

Step 4d: 索引 + 同步
  - 更新 wiki/index.md(加入条目)
  - 更新 wiki/log.md(记一笔)
  - 写完 index 必须 grep 验证可达
```

**反模式**:
- ❌ 探勘结果只写 chat 回复,不动 wiki
- ❌ 大段粘贴原文(违反 1-page overview)
- ❌ 写完不更新 index(下次找不到)
- ❌ 不带 source 链接(无法追溯)

### 最大信息输出

完成探勘后,在回复中提供**最有用的摘要**——不是全部细节,而是:

1. 这个来源对用户**最有用**的 3 个点
2. 与已知知识的**联系**(如果有)
3. 推荐后续**动作**(可选:创建更多页面/尝试实操/深入某个子话题)
4. **写入 wiki 的具体文件路径** (Step 4 联动结果)

---

## 完整示例:四源探勘

以下是来自真实会话的实际产出。展示了如何落地此方法论。

### 场景：用户说"学习一下这个仓库"

```python
# 实际执行（来自真实会话）
# Step 1: web_extract 获取仓库 README
# Step 2: 按目录结构逐个分支深入
# Step 3: 提取核心原理
# Step 4: 产出 wiki 页面

# 检测到隐含的嵌入链接时：
#   → 逐个打开内嵌链接，提取交叉信息
#   → 标记哪些链接是核心/辅助/冗余
```

### 场景：用户说"深入挖掘这4个来源"

```python
# 实际执行（来自真实会话）
# Step 1: 用 delegate_task 并行分析 4 个来源
# Step 2: 每个子代理深入分析一个来源
# Step 3: 整合结果
# Step 4: 创建 4+ wiki 页面
# Step 5: 更新 log.md + index.md
# Step 6: 在回复中呈现"关键洞察提炼"
```

### 场景：用户说"继续深度优化skill"

```python
# 实际执行（来自真实会话）
# Step 1: 分析 skill 当前版本
# Step 2: 从四个来源的知识中提取改进点
# Step 3: 按优先级排序改进
# Step 4: skill_manage(action='patch'/'edit')
# Step 5: 验证新 skill
# Step 6: 报告改进详情（diff 级别）
```

### 场景：用户说"基于已有 9 份 SOUL.md 写一份最好的"

```python
# 实际执行（内部合成模式 — 见 references/internal-synthesis-mode.md）
# Step 1: search_files inventory → 9 份 SOUL.md 候选
# Step 2: read_file 群读 → 建立 4 类 taxonomy
#   (identity seed / instance / operational / profile copies)
# Step 3: 提炼 4 模式（Vibe / 反规则 / 错误账本 / 元规则）
# Step 4: 决策 — 覆盖 instance SOUL.md,不重复其他 3 类
# Step 5: write_file 写出 v3, 104 行
# Step 6: read_file 读回 + 元规则自检（≤ 150 行 / 含错误账本 / 不重复 worker 手册）
```

---

## Step 5️⃣ Verify（验证）

创建页面/skill 后必须验证。跳过验证 = 产出可能不准确。

### 验证清单

```
对于每个产出：
  □ 如果是 wiki 页面 → read_file 读回来检查
  □ 如果是 skill → skill_view(name) 确认加载正常
  □ 如果是方法页 → 检查步骤是否完整、可操作
  □ 如果是概念页 → 检查是否有至少 2 条 [[wikilinks]]
  □ index.md 更新时间/总数是否正确
  □ log.md 是否追加了记录
  □ 涉及重启后存活的产物 → 记录到 memory/Mnemosyne 备忘

对于 wiki 页面：
  □ frontmatter 完整（title/created/updated/type/tags/sources）
  □ 至少 2 条出链 wikilink
  □ 不包含原始内容的大段粘贴
  □ 如果来源 < 2 且涉及仓库/项目声明 → 1 次搜索验证存在性

对于 skill：
  □ 描述准确
  □ 有版本号（bump）
  □ 有 created_by: agent（如果是代理创建的）
  □ 相关 skill 互相引用

对于代理系统的分析，额外验证（Ralph 6 信条检查）：
  □ Fresh Context — 每次迭代重新读取完整上下文？
  □ Backpressure — 有门控拒绝坏结果？
  □ Plan Is Disposable — 重生成成本低？
  □ Disk Is State — 文件作为交接机制？
  □ Steer With Signals — 加路标不加脚本？
  □ Let X X — 人类坐在循环上不在循环里？
```

**内部合成模式下的额外验证**（区别于 wiki 页面验证）:
- □ 元规则自检（如果是写 SOUL 类文件,检查它自己的元约束）
- □ DRY 收尾（不重复 5+ 模板已写过的内容）
- □ 决策追溯（在交付报告里写"为什么不写到 X/Y/Z"）

---

## Step 6️⃣ Post-Analysis Debrief（新！收尾步骤）

创建完 wiki 页面和 skill 后，不要直接报告完成。走完 4 步收尾确保知识留存：

```
Step 6.1: 记忆更新（跨重启存活）
  □ 新创建的 skill 路径 → mnemosyne_remember（首选） / memory（回退）
  □ 新发现的重要陷阱 → mnemosyne_remember（首选） / memory（回退）
  □ 新发现的交叉引用 → mnemosyne_remember（首选） / memory（回退）

Step 6.2: 关联 skill 同步
  □ 有新 skill 创建 → 更新相关 skill 的 related_skills
  □ 需更新已有 skill → patch 注入新陷阱/模式
  □ 检查 hermes-workflow 是否需同步更新

Step 6.3: 质量兜底检查（防遗漏）
  □ index.md 总页数正确（不是声称 64 但实际 66）
  □ log.md 条目与所有产出一致
  □ 所有新页面的 wikilink ≥ 2 条出链
  □ 技能间互相引用（双向）
  □ 新页面的 frontmatter 完整

Step 6.4: 凝练经验（自我改进）
  □ 这次探勘有没有发现可复用的新模式？
    有 → 注入本技能或 hermes-workflow
    无 → 正常，不是每次都有
  □ 工具调用次数？
    > 30 次 → 下次早用 delegate_task 并行
    < 10 次 → 高效
  □ 有没有走弯路？
    有 → 更新本技能的陷阱列表
    无 → 完美
```

**实际收益：** 本次深度优化前，创建了 14 个 wiki 页面但 index.md 漏了 Total pages 更新。Debrief 能抓住这类遗漏。**也避免下次重启后找不到刚创建的 skill（mnemosyne_remember 记录）。**




## 跨来源模式：深度合成法

当用户说"深入挖掘 N 个来源"时，并行分析再合成。

### 实际执行流（来自真实四源探勘）

```python
# Step 1: 用 delegate_task 并行分析 N 个来源
# 每个子代理独立分析一个来源
# 返回结构化笔记

# Step 2: 整合——找出共性模式
# 例如：OpenAI 的 "Prompt-in-Loop" ＝ Mitchell 的 "P0 Harness"
#        都指同一个概念：人类主导工程环境的编排
# Vibe Coding 的 "上下文分层" ＝ Harness 的 "CDLA 层"
# 都是上下文管理的同一种需求

# Step 3: 创建综合产出
# 每个来源 → 独立的 wiki 概念页（来源视角）
# 综合 → 对比页或工具页（交叉视角）

# Step 4: 更新 wiki 完整性
# - 如果是多来源 → 工具对比页（entities/）
# - 如果是单一范式 → 概念页（concepts/）
# - 如果是操作型 → skill（autonomous-ai-agents/）

# Step 5: 报告时用"关键洞察提炼"格式
# 不是贴所有细节，而是：
#   1. 最有用的 3 个点
#   2. 与已有知识的联系
#   3. 推荐后续动作
```

### 交叉引用发现模式

跨来源分析中最有价值的发现：

```
来源 A 的核心概念   →   在来源 B 中有不同命名
  但描述相同的现象   →   说明这是真实模式，不是个例
                  →   用自己的话重新定义（方法页）

来源 C 的某个工具      →   能直接解决来源 D 描述的问题
  但 C 不知道 D 的存在   →   你的组合发现（新 skill）
```

实际案例：OpenAI 的 "Prompt-in-Loop" 和 Mitchell 的 "P0 Harness" 描述的是同一个工程范式，只是命名不同。这个发现直接体现在 hermes-workflow 的 P0 层定义中。

以下是从真实四源学习中创建的 wiki 页面和 skill 列表：

### Wiki 页面

| 页面 | 来源 | 类型 |
|:----|:----|:----|
| `concepts/codex-harness-guide.md` | OpenAI | Concept |
| `concepts/vibe-coding-guide.md` | Vibe Coding | Concept |
| `concepts/mitchell-harness-evolution.md` | Mitchell | Concept |
| `concepts/harness-engineering-advanced.md` | Harness Repo | Concept |
| `concepts/ai-coding-tools-comparison.md` | 综合 | Concept |
| `concepts/harness-engineering-deep-study.md` | deusyu 仓库 | Concept |
| `concepts/symphony-spec-as-product.md` | deusyu 仓库 | Concept |
| `concepts/fowler-guides-sensors.md` | deusyu 仓库 | Concept |
| `methods/vibe-coding-prompt-system.md` | Vibe Coding | Method |
| `methods/mitchell-working-method.md` | Mitchell | Method |
| `methods/vibe-coding-automation.md` | Vibe Coding | Method |
| `methods/harness-deployment-pipeline.md` | Harness Repo | Method |
| `methods/ralph-wiggum-loop.md` | deusyu 仓库 | Method |
| `methods/hermes-workflow-and-exploration.md` | 综合反思 | Method |

### Skills

| Skill | 来源 | 版本 |
|:----|:----|:----|
| `hermes-workflow` (v3.0) | 五源+Agent自省 | 实际行为模式 |
| `ai-harness-exploration` (v3.0) | 五源+Agent自省 | 探勘方法论 |

---

## 陷阱

1. **不要提取得太浅** — 只读了 README 就说"学完了"，可能错过核心价值。必须深入到内部链接。
2. **不要在所有来源上花同样时间** — 有的来源是核心（10 分钟），有的是辅助（2 分钟），有的是冗余（跳过）。
3. **产出时不要**只写一个 wiki 页面**就停** — 如果来源涉及多个子话题（比如一篇文章里既有技术概念又有工作流），需要创建多个页面。
4. **不要忘记更新 index.md + log.md** — 这是 wiki 工作流的完整性检查。
5. **不要**把原始内容大段粘贴到 wiki 页面 — Wiki 是提炼后的知识，不是转载。
6. **提取得足够快** — 不要在分析阶段过度花费。如果 3 次工具调用后仍然看不到核心模式，切换策略。
7. **信息来源冲突时，用置信度排序：** 官方文档 > 知名作者 > 社区共识 > 单个博客 > 匿名来源。在 wiki 页面前言标注 `confidence: high|medium|low`。
8. **不要轻信来源中的统计数据** — 声称的百分比、下载量、采用率常常无源或夸大。必须追溯原始调查报告；无法追溯的一律标注"无可靠来源"并查找替代数据。参见 `references/skill-self-testing.md`。

9. **编号一致性检查** — 修改 SKILL.md 或 reference 文件后，检查所有编号是否连续一致。常见的断裂模式：`### X.X` 标题在代码块外（正确应为代码块内纯文本）；引擎计数与实际个数不匹配（写"6 引擎"但实际 8 个）。每次 patch 后手动检查受影响区域的编号链。

22. **🔴 写新 markdown 必跑反斜杠-u 字面检查(2026-06-04 v6.18 自踩,扩展 v1.4 #13)**。本会话 22:39 写 `agents/main-claude.md` 时,pitfall #13 表格里我自己写了反斜杠-u2014 而不是真 em-dash。**强制流程**(写完立刻跑,不要等 push 时发现):
```bash
# 任何新 .md / .sh / .py 写完, 立即跑
grep -F '\u' <file>        # F 标志防正则解释反斜杠-u
# 命中 → 用真字符替换 em-dash / → / &nbsp; (或 raw f-string 让 Python 转义)
# 关键:本会话踩过 4 次同类型 bug(feishu-rich-messages / lcm-memory-guide / git-push-cheatsheet / main-claude.md)
# 写完 1 个新 markdown 立刻 grep 必走,不依赖写完后脑记忆
```
**meta-pitfall(本会话最痛)**: skill **作者自己** 写完 pitfall #13 描述"不该写反斜杠-u2014"后,下次写新文件**就**踩。**修法**: 写完任何新 .md 立即 `grep -F '反斜杠-u' <file>`,**不**相信"我记得规则"。**写文件前的脑 = 不可信**,**写完后的 grep = 唯一可信**。
**跨 skill 适用**: wiki-keeper v1.4 #13 / hermes-agent-skill-authoring / 任何 write_file 后必跑。
**作者自检流程(NEW)**: patch 任何 skill 之后,patch **自己**必跑一遍 grep 反斜杠-u 核验。**否则 pitfall #22 的描述本身就违反 pitfall #22**。

10. **不要相信单一来源的仓库/项目声明** — 当单个来源声称某个 GitHub 仓库或开源项目存在时，在创建概念页前先做 1 次存在性验证。搜索仓库名 + 作者确认是否存在。如果搜索后仓库不存在 → 不创建概念页，将信息标注为"unverified"，在 log.md 记录"单一来源声称 {项目} 但未发现存在"。实际案例：本会话中单一来源声称 corona 框架 (encoding+observation+reasoning+optimization+agent) 存在 Apache 仓库，但 3 路并行搜索 37 次确认无对应仓库。

11. **MCP与REST配额独立，不要混为一谈** — Tavily REST 432 不影响 Tavily MCP。两个通道使用不同配额池。当 web_search 返回 432 时，MCP 通道仍可正常搜索（实测 ~0.6s）。搜索失败时先确认是 REST 还是 MCP 问题，不要一刀切认为"Tavily挂了"。优先使用 MCP 通道，REST 仅做兜底。

12. **`skill_manage(action='edit')`对 reference 文件无效** — `edit` action 只作用于 SKILL.md。更新 `references/` 下的文件需要用 `write_file` 工具写入绝对路径。Patch reference 文件时用 `skill_manage(action='patch', file_path='references/xxx.md')` 模式。在 Meta 自优化流程中，Step 4 的 reference 同步检查已覆盖此规则。

13. **MCP Python SDK 版本兼容性** — `hermes mcp test <server>` 报 `errlog` 参数错误时，通常是 MCP Python SDK 版本过旧（<1.0）。升级即可：`pip install -U mcp`（0.9.1→1.27.2 已验证修复）。不影响 MCP 运行时连通性——仅影响 CLI 测试命令。

15. **装之前先过 Step 0c 必要性验证** — 用户偏好诚实评估而非推销（反复触发信号："评估一下"/"重新审视"/"诚实评估"）。推广任何新工具/系统/范式时，必须先回答 6 问（痛点/边际价值/替代/成本/推销自检/退出成本），再决定装不装。Hindsight 案例（2026-06-02 完整装卸循环）已写入 `references/should-i-build-gate.md`，作为失败案例参考。红旗语言："业界共识"/"必需"/"最佳实践" → 立即停。

16. **内部合成模式不要重复"已知模板已写"的内容** — DRY 原则。新产物只写它独特负责的部分,主 SOUL 不写"我能做什么"（那是 worker-soul 模板的工作）,worker-soul 不写"我是谁"（那是主 SOUL 的工作）。违反 → 8 个 profile 副本同时变 3 倍,臃肿放大器。

16. **SOUL 自指 critique 必须真改进** — 写完 v3 后重读，问"v3 的真实缺口是什么？"——不是为优化而优化。**找不到真缺口 = 不出 v4**。v3→v4 真实缺口清单：位置错 / Vibe > 12 字 / 错误账本 > 3 行 / 含具体版本号 / 含 "snapshot" 时态词 / 重复节。

17. **暂停决策类指令的"测你边界"模式** — 用户说"暂停维护"30 秒后再说"装 3 仓库"，再 5 分钟后说"重新优化 SOUL"。这是**测 agent 是否被反复指令牵着走**。正确做法：每次新指令**回到 Step 0a 元评估**——上次决策的真实理由没变就保持，没变就不动。**不因为时间近 = 应该改**。**变更的理由 = 痛点变了，不是时间**。

18. **"你赢"元规则的反向解读陷阱** — SOUL 中"分歧区:你赢"被读成"你说我做=沉默"是错的。真意："看到重复模式第 2 次应主动警告"。诊断：问自己"用户说 X 时我应主动停还是立即执行？"答：显式指令=已确认立即执行；红旗语言=立即停评估；**重复模式 = 主动警告**。误读这条 = 反身性失败 #16 的具体表现。

19. **LCM 摘要扩张到 wiki 是隐性陷阱**（2026-06-04 用户纠正）— 看到 `lcm_expand` 摘要时"顺手"写 wiki 是常见冲动。架构上 LCM 不知道 wiki 存在（源码 grep 0 匹配），但 Agent 看到摘要后可能自我合理化写 wiki。**禁止**:看到 LCM 摘要,看完即可,不写任何 wiki 文件。**详见 `references/wiki-write-boundary.md` § 1, § 3 反模式 A**。

20. **元方法论探勘"自加 5+ 边界文件"是过度推销**（2026-06-04 自我纠错）— 用户问"如何 X 更好"时,Agent 倾向写 1+5 个 wiki 页。但实际用户可能只想要 1-2 个核心页。**修正**:列候选清单(3-5 个,带"为什么需要")→ 让用户选 1-3 个 → 未选进 scratchpad/_drafts/。**详见 `references/wiki-write-boundary.md` § 3 反模式 B**。

21. **Distill 产物 ≠ 5 个方法论页**（2026-06-04 自我纠错）— CODE 4 阶段的 Distill 阶段= 1 个核心 method + 1-2 个配套 protocol + 其余 scratchpad/_drafts/。不要把"提炼"等同于"新建 5 个 wiki 页"。**详见 `references/wiki-write-boundary.md` § 3 反模式 C**。

15. **装之前先过 Step 0c 必要性验证**

16. **内部合成模式不要重复"已知模板已写"的内容** — DRY 原则。新产物只写它独特负责的部分,主 SOUL 不写"我能做什么"（那是 worker-soul 模板的工作）,worker-soul 不写"我是谁"（那是主 SOUL 的工作）。违反 → 8 个 profile 副本同时变 3 倍,臃肿放大器。

16. **SOUL 自指 critique 必须真改进** — 写完 v3 后重读，问"v3 的真实缺口是什么？"——不是为优化而优化。**找不到真缺口 = 不出 v4**。v3→v4 真实缺口清单：位置错 / Vibe > 12 字 / 错误账本 > 3 行 / 含具体版本号 / 含 "snapshot" 时态词 / 重复节。

17. **暂停决策类指令的"测你边界"模式** — 用户说"暂停维护"30 秒后再说"装 3 仓库"，再 5 分钟后说"重新优化 SOUL"。这是**测 agent 是否被反复指令牵着走**。正确做法：每次新指令**回到 Step 0a 元评估**——上次决策的真实理由没变就保持，没变就不动。**不因为时间近 = 应该改**。**变更的理由 = 痛点变了，不是时间**。

18. **"你赢"元规则的反向解读陷阱** — SOUL 中"分歧区:你赢"被读成"你说我做=沉默"是错的。真意："看到重复模式第 2 次应主动警告"。诊断：问自己"用户说 X 时我应主动停还是立即执行？"答：显式指令=已确认立即执行；红旗语言=立即停评估；**重复模式 = 主动警告**。误读这条 = 反身性失败 #16 的具体表现。

19. **LCM 摘要扩张到 wiki 是隐性陷阱**（2026-06-04 用户纠正）— 看到 `lcm_expand` 摘要时"顺手"写 wiki 是常见冲动。架构上 LCM 不知道 wiki 存在（源码 grep 0 匹配），但 Agent 看到摘要后可能自我合理化写 wiki。**禁止**:看到 LCM 摘要,看完即可,不写任何 wiki 文件。**详见 `references/wiki-write-boundary.md` § 1, § 3 反模式 A**。

20. **元方法论探勘"自加 5+ 边界文件"是过度推销**（2026-06-04 自我纠错）— 用户问"如何 X 更好"时,Agent 倾向写 1+5 个 wiki 页。但实际用户可能只想要 1-2 个核心页。**修正**:列候选清单(3-5 个,带"为什么需要")→ 让用户选 1-3 个 → 未选进 scratchpad/_drafts/。**详见 `references/wiki-write-boundary.md` § 3 反模式 B**。

21. **Distill 产物 ≠ 5 个方法论页**（2026-06-04 自我纠错）— CODE 4 阶段的 Distill 阶段= 1 个核心 method + 1-2 个配套 protocol + 其余 scratchpad/_drafts/。不要把"提炼"等同于"新建 5 个 wiki 页"。**详见 `references/wiki-write-boundary.md` § 3 反模式 C**。

15. **装之前先过 Step 0c 必要性验证**

```
Step 1: 建立基线认知（5 分钟）
  ├─ web_search("{名} 是什么") → 快速了解
  └─ web_extract(官方首页) → 核心概念

Step 2: 找 1 个 hello world
  ├─ web_search("{名} quickstart / getting started")
  └─ 理解基本用法

Step 3: 找 2 个 最佳实践
  ├─ web_search("{名} best practices / production")
  └─ 提取关键技巧

Step 4: 找 1 个 常见陷阱
  ├─ web_search("{名} pitfalls / common mistakes / 踩坑")
  └─ 避免重复踩坑

Step 5: 产出
  ├─ 如果是一键工具类型 → 尝试安装/运行
  ├─ 如果是概念/理论 → 创建 wiki 概念页
  └─ 如果是工作流 → 创建方法页或 skill
```

**规则：** 30 分钟内完成全流程，产出至少一个 wiki 页面。如果 30 分钟后仍然没有清晰的理解，说明要么是个复杂工具（需要更长时间），要么是个不成熟项目（不值得深入）。

## 深度延续搜索流程（初始探勘后的迭代深化）

> **当用户说"继续"、"再多查点"、"再深入看看"时使用。**
> 初始探勘只建立了基线认知，深度延续搜索才是真正发现新连接的地方。

### 触发条件

初次探勘完成后，用户明确要求继续深入时：

| 用户说 | 含义 |
|:------|:-----|
| "继续" / "还有吗" | 当前深度不够，需要更多内容 |
| "再找找XXX方面的资料" | 需要特定角度的补充 |
| "这个工具的实际案例呢" | 需要实践证据 |
| "对比一下A和B" | 需要交叉对比搜索 |
| "还有其他类似的吗" | 需要横向替代方案 |

### 核心流程：6 步迭代搜索

```
Phase 1: 缺口分析（1 分钟）
  → 当前已知什么？还缺什么？
  → 从 3 个维度评估深度

Phase 2: 多角度搜索（3-5 分钟）
  → 按 5 个搜索域并行搜索
  → 快速筛选值得深入的内容

Phase 3: 横向扩展（5-10 分钟）
  → 找替代方案、相关工具、批评观点
  → 扩展知识边界

Phase 4: 纵向深入（10-20 分钟）
  → 对最值得深入的内容做全量分析
  → 逐篇提取新概念

Phase 5: 交叉合成（5 分钟）
  → 新内容 vs 已有知识库
  → 发现新连接、更新已有页面

Phase 6: 交付（2 分钟）
  → 新发现 → 新连接 → 新动作
```

### Phase 1: 缺口分析

逐步问自己：

```
① 当前认知到了什么程度？
   基线：知道它是什么、怎么用
   🟢 中等：知道核心原理和 2-3 个关键技巧
   🔵 深入：知道架构细节、适用边界、常见陷阱

② 从哪些维度还缺少信息？
   □ 技术原理（底层架构 / 算法 / 设计决策）
   □ 最佳实践（生产环境 / 真实案例 / 经验教训）
   □ 横向对比（同类工具 / 替代方案 / 优劣势）
   □ 批判视角（缺点 / 失败场景 / 被弃用的风险）
   □ 生态整合（与其他工具的配合 / 社区活跃度）

③ 当前知识中最薄弱的维度是哪个？
   在确认可搜索的前提下，优先补最弱的维度。

④ 已有的 wiki 页面中哪些可能被新搜索更新？
   列出页面名 → 作为后续更新的目标清单
```

输出：缺口清单（2-3 个搜索方向） + 目标更新页面清单

### Phase 2: 多角度搜索

针对缺口清单中的每个方向，从不同角度搜索：

```python
# 实际搜索序列（并行或串行，取决于可用工具）
# 角度 1: 核心技术
web_search(f"{topic} architecture design principles")
web_search(f"{topic} how it works internals")

# 角度 2: 实践案例
web_search(f"{topic} production use case case study")
web_search(f"{topic} real world example")

# 角度 3: 横向对比
web_search(f"{topic} vs alternative comparison")
web_search(f"{topic} competitor review")

# 角度 4: 陷阱与局限
web_search(f"{topic} limitations pitfalls cons")
web_search(f"{topic} when not to use")

# 角度 5: 生态与趋势
web_search(f"{topic} community roadmap 2026")
web_search(f"{topic} ecosystem integration")

# 角度 6: 中文社区（如用户用中文）
web_search(f"{topic} 实践 踩坑 经验")
web_search(f"{topic} 深入 原理解析")
```

**搜索结果筛选规则：**

| 来源特征 | 优先级 | 处理 |
|:--------|:-----:|:----|
| 官方文档 / 技术报告 | 🥇 | 深读，优先提取 |
| 知名作者 / 公司博客 | 🥇 | 深读 |
| GitHub 仓库（>1k★） | 🥇 | 扫 README + 核心目录 |
| 社区教程 / Medium | 🥈 | 快速扫，提取实用技巧 |
| Stack Overflow / 论坛 | 🥈 | 只读高赞 + 近期 |
| 新闻 / 产品发布 | 🥉 | 快速扫，只存链接 |
| AI 生成内容（明显） | ❌ | 跳过 |

**搜索收敛规则：** 搜索 3 轮后如果新结果已有 80%+ 重复已知内容 → 停止搜索，进入 Phase 4。

### Phase 3: 横向扩展

在核心内容之外，找那些**不在你预期路径上但可能重要**的东西：

```
① 替代方案搜索
   ├─ 用户提到的工具 / 框架有哪些直接竞品？
   ├─ 它们各自的优势场景是什么？
   └─ 有没有开源替代品？

② 相关领域搜索
   ├─ 这个工具解决了什么问题？
   ├─ 其他领域有没有类似问题 + 解决方案？
   └─ 能不能跨领域借模式？

③ 批评与对比
   ├─ 找 1-2 篇批评性文章（Hacker News 评论区很有价值）
   ├─ 找 1 篇"为什么我们用 X 而不是 Y"的对比
   └─ 找 1 篇"X 的十大陷阱"类文章

④ 上下游生态
   ├─ 这个工具的前置依赖是什么？
   ├─ 它配合什么工具效果最好？
   └─ 它的输出能被什么工具消费？

⑤ 跨来源验证
   ├─ 初次探勘中提取的核心观点 → 在其他来源被确认了吗？
   ├─ 有没有来源提出互相矛盾的主张？
   └─ 矛盾 → 哪个来源更可信？（按置信度排序原则）
```

**产出：** 横向扩展的发现清单（每个条目：来源链接 + 一句话总结 + 是否值得深入）

### Phase 4: 纵向深入

对 Phase 2-3 中筛选出的 **最有价值的 1-3 个来源**执行全量分析：

```
对每个选定来源：
  ① 完整阅读（web_extract 全文）
  ② 使用 5 步探勘法的 Step 1-2（Analyze + Extract）
  ③ 提取新概念、新方法、新模式
  ④ 与已有知识对比：
      新概念 vs [[已知概念A]] → 同义不同名？
      新方法 vs [[已知方法B]] → 互补还是替代？
      新模式 vs [[已有模式C]] → 更优还是特例？
  ⑤ 产出格式：
      每个新发现 → 1 个 wiki 页面或 1 个 wiki 页面更新
```

**深入深度判断：**

| 来源价值 | 投入时间 | 产出 |
|:--------|:-------:|:----|
| 🔴 增量内容 | 5 分钟 | 追加到已有页面 |
| 🟡 重要补充 | 15 分钟 | 更新已有页面 + 新增 subsection |
| 🟢 全新范式 | 30 分钟+ | 创建新 wiki 页面 + 更新 index/log |

**效率规则：**
- 如果 Phase 2 搜索结果中 70%+ 内容已在已有知识库中 → 跳过 Phase 4，直接进入 Phase 5
- 如果 Phase 3 横向扩展发现了全新领域 → 把这个领域标记为"后续探索"，先不深入
- 最多深入 3 个来源（超过 3 个 → 选最相关的 3 个，其余存到"待探索"清单）

### Phase 5: 交叉合成

将新发现与已有知识库建立连接：

```
① 更新已有 wiki 页面
  ├─ 对每个找到的新信息：
  │   ├─ 是否已有对应 wiki 页面？
  │   │   ├─ 有 → 追加新内容，bump updated 日期
  │   │   └─ 无 → 判断是否值得新建页面（阈值：2+ 来源提及 或 对用户有显著价值）
  │   └─ 是否与已有内容冲突？
  │       ├─ 是 → 标注矛盾，标注 confidence
  │       └─ 否 → 正常追加
  └─ 更新 index.md + log.md

② 建立新连接
  ├─ 新页面之间的 [[wikilinks]]
  ├─ 新页面与已有页面之间的 [[wikilinks]]
  └─ 对比页面（如果现有知识间出现新的对比维度）

③ 识别模式
  ├─ 是否有跨来源的共同主题？（"多个来源都提到同一种模式"）
  ├─ 是否有跨来源的矛盾？（"权威来源之间存在分歧"）
  └─ 是否有知识蒸馏机会？（"3 个来源的不同观点可以合并为 1 个综合判断"）

④ 更新追踪器（如果使用深度研究追踪法）
  ├─ 新增 tracker entries
  ├─ 更新已有 tracker 的计数和状态
  └─ 检查脉络冲突和跨脉络关联
```

### Phase 6: 交付

对比初次探勘的交付，深度延续搜索的交付强调**增量**：

```
## 🔍 深度延续搜索 — {主题名}

### 📊 搜索范围
| 维度 | 本轮 | 累计 |
|:----|:----|:----|
| 新搜索 | N 个搜索结果 | M 个总来源 |
| 新深入 | N 篇全量分析 | M 篇累计 |
| 新来源质量 | 🟢 🟡 各 N 个 | — |

### ✨ 新发现
| 类型 | 内容 | 来源 |
|:----|:----|:-----|
| 🧠 新概念 | {概念名} — 一句话 | {来源链接} |
| 🔗 新连接 | {已有页A} ←→ {新页B} | — |
| ⚠️ 新矛盾 | {来源A} 说 X, {来源B} 说 ¬X | — |
| 🆕 新更新 | {页面名} 追加了 {内容} | — |

### 🧩 增量洞察
{比初次探勘多了什么？—— 3 句话}
  1. {超出预期的发现}
  2. {已有认知被修正的部分}
  3. {新出现的行动建议}

### 📋 后续建议
- 如果还想继续 → 建议深入 {具体子话题}
- 如果够了 → 知识已在 wiki 中固化：[[link1]]、[[link2]]
- 如果发现重要矛盾 → 建议人工判断
```

**交付验证（Verify 子步骤）：**
```
□ 新页面有至少 2 条 [[wikilinks]]
□ 已有页面已追加新内容
□ index.md 更新计数
□ log.md 追加记录
□ 没有重复创建已有内容
```

### 完整示例：从"继续"到"交付"

**场景：** 用户说"好，分析完了，继续看看还有什么"（来自 8 项目探勘的真实案例）

```
Phase 1 缺口分析：
  已知道：8 个项目的核心能力、安装方式、推荐优先级
  缺：项目之间的实际互动关系、生态整合度、各项目的社区活跃度趋势
  目标：补充横向对比和生态视角

Phase 2 多角度搜索：
  → 搜索每个项目的 GitHub 活跃度、最近更新
  → 搜索项目之间的已知集成方式
  → 搜索社区关于这些项目的讨论热度

Phase 3 横向扩展：
  → 发现 SkillClaw 和 hermes-dojo 的互补关系（dojo 识别问题 → self-evolution 解决）
  → 发现 Mnemosyne 和 wiki-* 系列可以组成完整记忆层

Phase 4 纵向深入：
  → 深入 SkillClaw 的架构文档
  → 深入 hermes-agent-self-evolution 的 GEPA 算法

Phase 5 交叉合成：
  → 创建 comparison/hermes-evolution-stack.md（进化闭环全景）
  → 更新现有概念页补充集成关系

Phase 6 交付：
  → "进化循环全景图" + 各项目角色定位 + 组件间依赖关系
```

### 与已有工作流的关系

```
首次探勘（5 步法）
  → Analyze → Extract → Formalize → Deliver → Verify
       ↓ (用户说"继续")
深度延续搜索（6 步迭代）
  → 缺口分析 → 多角度搜索 → 横向扩展 → 纵向深入 → 交叉合成 → 交付
       ↓ (用户又说"继续")
深度延续搜索（再次迭代）
  → 重新缺口分析 → 搜索新角度 → ...
       ↓ (搜索收敛 = 新结果 80%+ 重复已知内容)
停止迭代
  → 报告完整覆盖度，建议进入长期追踪模式
```

**规则：**
- 首次探勘用 5 步法（种子分析）
- 后续迭代用深度延续搜索 6 步法（增量深化）
- 当 2 次连续迭代都产生 < 2 个新发现 → 建议改为深度研究追踪法（长期监控）
- 每次迭代都更新 wiki，但不创建重复的"继续"记录

## 深度研究追踪法（长期跟踪主题）

当用户持续关注某个主题（如 Harness Engineering），使用多层追踪结构：

```
第一层：每日自动监控（5 分钟/天）
  ├─ 固定在 7+ 来源搜索最新内容（GitHub Trending, arXiv, Twitter, 博客）
  ├─ 与已有知识库去重（检查 19+ 已知文章）
  ├─ 结果汇总到 tracker.md
  └─ Hermes 实现：cronjob + blogwatcher

第二层：产出 ← 改为"内部合成模式"路径,因为大多是更新已有产物
```

### 内部合成（filesystem-only 路径）

**触发信号**:用户说"基于已有的 X 写一份 Y" / "结合文件 + 你的实际" / "整合这几个"。

```
首次探勘（5 步法）
  → Analyze → Extract → Formalize → Deliver → Verify
       ↓ (用户说"继续")
深度延续搜索（6 步迭代）
  → 缺口分析 → 多角度搜索 → 横向扩展 → 纵向深入 → 交叉合成 → 交付
       ↓ (用户又说"继续")
深度延续搜索（再次迭代）
  → 重新缺口分析 → 搜索新角度 → ...
       ↓ (搜索收敛 = 新结果 80%+ 重复已知内容)
停止迭代
  → 报告完整覆盖度，建议进入长期追踪模式
```

**规则：**
- 首次探勘用 5 步法（种子分析）
- 后续迭代用深度延续搜索 6 步法（增量深化）
- 当 2 次连续迭代都产生 < 2 个新发现 → 建议改为深度研究追踪法（长期监控）
- 每次迭代都更新 wiki，但不创建重复的"继续"记录

## 深度研究追踪法（长期跟踪主题）

当用户持续关注某个主题（如 Harness Engineering），使用多层追踪结构：

```
第一层：每日自动监控（5 分钟/天）
  ├─ 固定在 7+ 来源搜索最新内容（GitHub Trending, arXiv, Twitter, 博客）
  ├─ 与已有知识库去重（检查 19+ 已知文章）
  ├─ 结果汇总到 tracker.md
  └─ Hermes 实现：cronjob + blogwatcher

第二层：双周深度搜索（30 分钟）
  ├─ 5 个搜索域：新概念、新工具、实践案例、批判、对比
  ├─ 3 级来源优先级：官方 > 知名作者 > 社区
  ├─ 去重：对照已知文章 + 跟踪项目
  └─ 产出：概念页更新或方法页

第三层：按需深入分析（1-2 小时）
  ├─ 当新文章提出新范式 → 使用本技能的完整 5 探勘法
  ├─ 当新工具发布 → 使用未知→已知过渡模式
  └─ 产出：新概念页 + 方法页 + 可能的 skill
```

**实际案例**（deusyu/harness-engineering 的 19 篇数据库）：
```
脉络一：AI 时代 Harness Engineering（16 篇）→ 核心追踪
脉络二：云原生 Harness.io（2 篇）→ 同名但不同义，辅助
脉络三：效率悖论与能力进化（1 篇）→ 批判视角
延伸阅读：Mitchell Hashimoto / Context Engineering（3 篇）
每个脉络有自己的计数和跨文章关联
```

## 快速分析模式（轻量版）

当用户只需要快速了解而非全量探勘时使用。跳过 wiki 创建，只出摘要。

**触发条件：** 用户说"简单说说"、"了解下"、"这是什么"而非"学习一下"、"深入挖掘"

| 维度 | 全量探勘（默认） | 快速分析（轻量） |
|:----|:---------------|:----------------|
| 搜索轮次 | R1+R2+R3+R4 (6-10 次) | R1 仅广撒网 (2-3 次) |
| 产出 | wiki 概念页 + index/log 更新 | 纯文本摘要，无 wiki |
| 验证 | 18 项完整 | 跳过 index/log 检查 |
| 耗时 | 15-30 分钟 | 3-5 分钟 |

**执行流：**
```
1. Step 0 质量评估（5 秒快速判断）
2. R1 广撒网搜 2-3 次
3. 提取 2-3 个关键点
4. 一句话总结 → 交付
```

**什么时候用快速模式：**
- 用户发链接但说"简单看看"
- 用户问新工具但明显只想知道"它是什么"
- 主题明显是增量内容（已有概念页的新变体）

### 快速分析 → 全量过渡模式

快速分析后用户说"继续"时的过渡策略：

```python
# 用户说"继续" / "详细说说" / "再深入看看"
def quick_to_full(topic, quick_knowledge):
    """快速分析 → 全量探勘的过渡"""
    
    # Phase 1: 评估快速分析的质量
    if quick_knowledge was summarized:
        # 快速分析只留了摘要 → 需要重新搜索
        # 起始：从 R2 深挖开始，跳过 R1 广撒网
        run_deep_dive(R2_only=True)  # 节省 2-3 次搜索
    else:
        # 快速分析包含 2-3 个关键点 → 从缺口分析开始
        run_gap_analysis(
            existing=quick_knowledge,
            missing=["技术细节", "最佳实践", "实战案例"]
        )
    
    # Phase 2: 创建 wiki 页面（快速分析时跳过了）
    create_wiki_page(topic, quick_knowledge + new_depth)
    update_index_and_log()
    
    # Phase 3: 16 项验证
    # 跳过 R1 验证（已经在快速分析时完成）
    verify(quick_level=False)
```

**过渡时间估算：**
- 快速分析（3-5 分钟）+ "继续"（8-12 分钟）= 全量（11-17 分钟）
- 比单独全量（15-30 分钟）节省约 30% 时间
- 因为 R1 搜索 + Step 0 评估已经完成

**规则：** 快速分析产出的摘要保留在会话上下文中。用户说"继续"时：
1. 如果是同一次会话 → 直接过渡，使用内存中的摘要
2. 如果是新会话 → session_search 找回上次的快速分析结果
3. 两次都找不到 → 重建：R1 重新搜 1 次确认 + 再深入

## 用量追踪

每次探勘完成后，自动记录调用数据到内存，用于自我改进：

```python
# 记录格式（每轮探勘追加 1 条）
ai-harness-exploration call log:
  #N: {主题} | 引擎使用: {web_search:N, web_extract:N, browser:N} | 
  搜索轮次: R1/R2/R3/R4 | 搜索次数: N | 耗时: Ns | 产出: {page types}
```

**用途：**
- 超过 10 次搜索 → 下次早用 delegate_task 并行
- web_extract 调用 > web_search → 检查是否过度依赖提取
- browser 调用 > 2 → 说明内容有反爬，需调整策略

## 自我优化 Meta 模式（改进本技能自身的方法论）

当用户说"优化skill"、"改进skill"、"深度优化ai-harness-exploration"时——即需要本技能自我改进——使用以下方法论：

### 触发条件

| 用户说 | 含义 | 启动哪个流程 |
|:------|:-----|:------------|
| "优化skill" / "改进skill" | 改进任意技能 | 缺口排查（5 分钟） |
| "深度优化ai-harness-exploration" | 改进本技能自身 | **Meta 6 步法** |
| "测试ai-harness-exploration" | 验证技能功能 | 技能自测试（`references/skill-self-testing.md`） |

### Meta 6 步法：自我优化流程

```
Step 1: 缺口排查（3 分钟）
  ├─ 读 SKILL.md 头部（frontmatter + 核心方法论）
  ├─ 检查编号是否一致（`### 1.5` 是否在代码块外？9 引擎还是 8 引擎？）
  ├─ 检查 reference 文件是否与 SKILL.md 同步
  ├─ 检查版本号是否过旧
  └─ 输出：缺口清单

Step 2: 实测验证（5-10 分钟）
  ├─ 对每个缺口执行 1 次最小化验证（不是全量探勘）
  ├─ 例如：引擎计数 → 打开 SKILL.md 确认数量
  ├─ 例如：子代理容错 → delegate_task 发 2 个简单任务看是否正常
  └─ 输出：实测结果（哪些缺口成立，哪些误判）

Step 3: 排序（1 分钟）
  ├─ 🔴 阻塞性 bug（语法错误/编号断裂/流程无法执行）
  ├─ 🟡 功能性不足（缺少必要模式/容错缺失）
  └─ 🟢 增量改进（更好但不是必须）
  分批：先修 🔴，再补 🟡，最后加 🟢

Step 4: 注入改进（5-15 分钟）
  ├─ 每个改进 1 次 patch，单次批量最多 4 个
  ├─ 每 2-3 个 patch 后 skill_view 确认格式未断裂
  ├─ 改进后的 SKILL.md 结构化检查：
  │   ├─ frontmatter 完整无断裂
  │   ├─ 所有代码块正确闭合
  │   ├─ 所有编号连续（无 `### X.X` 在代码块外）
  │   ├─ 关键术语/计数与 SKILL.md 正文一致（引擎数、步数、版本标题）
  │   └─ version bump
  ├─ reference 文件同步检查：
  │   对 linked_files 中的每个 reference 文件：
  │   ├─ 引用名词（引擎名、步骤数、API key 名）是否与 SKILL.md 一致
  │   ├─ 描述的流程是否包含 SKILL.md 中新增的步骤/模式
  │   └─ 引用的文件路径是否真实存在
  └─ 输出：完整的 patch 序列 + reference 同步状态

Step 5: 全量验证（2 分钟）
  ├─ skill_view(name) 确认加载正常
  ├─ 检查 linked_files 列表完整
  ├─ 检查 triggers 确认被命中
  └─ 输出：验证通过/失败

Step 6: 交付报告（2 分钟）
  ├─ 每项改进的摘要（类型+变更位置+原因）
  ├─ 版本号变更（X.Y.Z → X.Y.Z）
  ├─ 已修复问题数量统计
  └─ 输出：6 步执行日志

**规则：**
- 总耗时 ≤ 30 分钟。超时未完成 → 报告已完成的改进，剩余放入"待改进清单"
- 不要一次性全量重写 skill
- 每次优化至少发现 1 个问题——如果没有，说明检查不够深入
- 优化后的陷阱列表更新：如果本次优化中走弯路，追加到陷阱
```

### 内部合成模式作为 Meta 自优化的延伸

`internal-synthesis-mode.md` 本身是**对 ai-harness-exploration 的元贡献**（meta-self-improvement 的具体应用）:

```
Meta 6 步法优化本 skill 时
  ├─ 缺口排查发现: "SKILL.md 是 web 探勘导向,缺少内部合成模式"
  ├─ 注入改进: 新增 reference/internal-synthesis-mode.md + SKILL.md 决策树分支
  ├─ 验证: skill_view 加载正常,triggers 命中
  └─ 沉淀: 下次用户说"基于已有 X 写 Y"时,自动加载该模式
```

下次做 Meta 自优化时,如果发现"内部合成模式还有 X 没覆盖",追加新一节到 internal-synthesis-mode.md 而不是新建文件。

---

## 9.0 实际可用搜索通道(2026-06-04 实测)

> **本节是硬数据** — 不写"应该用什么",写"实际跑通什么"。
> **修正历史**:v6.11.0 之前 SKILL 文档写"7 路并发"+"REST 432 配额耗尽"是**部分错误**:
> - Tavily REST key 实际失效(`web_search` 401),**不是 432 配额**
> - DuckDuckGo 在本机环境**默认 curl 不可达**(要 UA + 短 timeout)— 见 § 9.0.3 二次实测
> - Tavily MCP×3 + MiniMax MCP 才是真正主力

### 9.0.1 实测矩阵(2026-06-04 13:50)

| 通道 | 状态 | 延迟 | 配额 | 关键观察 |
|---|---|---|---|---|
| `mcp_minimax_web_search` | ✅ 正常 | < 1s | 150/5h | 主力,中文强,无评分 |
| `mcp_tavily_mcp_google` | ✅ 正常 | 0.82s | 独立 MCP key | 通用英文 |
| `mcp_tavily_mcp_microsoft` | ✅ 正常 | 0.78s | 独立 MCP key | 英文/技术栈 |
| `mcp_tavily_mcp_ggc` | ✅ 正常 | 1.05s | 独立 MCP key | 通用英文 |
| `mcp_tavily_mcp_github` | ⚠️ 备用 | — | key 432 已耗尽 | GitHub-specific |
| `web_search` (Hermes REST 工具) | ❌ **401** | — | Tavily REST key 失效 | **不可用** |
| `terminal curl DuckDuckGo` | 🟡 需 UA | 8s | 无限 | 不加 UA 超时;UA + 短 timeout 可用(30KB) |
| `terminal curl GitHub raw` | ✅ 200 | < 1s | 无限 | 仓库 README/源文件 |
| `terminal curl arXiv` | ✅ 200 | < 1s | 无限 | 学术论文 |
| `terminal curl Wikipedia` | ❌ 000 | 10s+ | 无限 | 国内不通 |
| `terminal curl Bing` | 🟡 302 | — | 无限 | 需 -L follow |

### 9.0.2 实际 fallback 决策树(2026-06-04 版)

```
尝试搜索"X"
  │
  ├─ 1️⃣ mcp_minimax_web_search(X)         [主力,150次/5h,中文最佳]
  │   ├─ 命中 → 结束(去重合并)
  │   └─ 未命中 / 配额冷却 → 2️⃣
  │
  ├─ 2️⃣ mcp_tavily_mcp_google(X)          [MCP key 独立,~0.8s]
  │   ├─ 命中 → 结束
  │   └─ 失败 → 3️⃣
  │
  ├─ 3️⃣ mcp_tavily_mcp_microsoft(X)       [独立 key,~0.8s]
  │   ├─ 命中 → 结束
  │   └─ 失败 → 4️⃣
  │
  ├─ 4️⃣ mcp_tavily_mcp_ggc(X)             [独立 key,~1.0s]
  │   ├─ 命中 → 结束
  │   └─ 失败 → 5️⃣
  │
  ├─ 5️⃣ terminal curl 兜底(2026-06-04 新增)
  │   ├─ 5a: GitHub raw  (https://raw.githubusercontent.com/...)
  │   │   适合:已知仓库/项目 README
  │   ├─ 5b: arXiv       (https://export.arxiv.org/api/query?...)
  │   │   适合:学术论文 / 深度研究
  │   ├─ 5c: Bing + UA  (https://www.bing.com/search?q=...)  ← 需 -L + UA
  │   │   适合:通用 web 搜索(实测 115KB 完整结果)
  │   └─ 5d: DuckDuckGo + UA + 短 timeout  ← 8s 内 30KB
  │       适合:隐私搜索备选
  │
  └─ 6️⃣ web_search 工具   [❌ 401 当前不可用,跳过]
```

**5a/5b/5c/5d 标准 curl 命令**:
```bash
# 5a GitHub raw
curl -m 10 "https://raw.githubusercontent.com/{org}/{repo}/main/README.md"

# 5b arXiv
curl -m 10 "https://export.arxiv.org/api/query?search_query=all:{query}&max_results=5"

# 5c Bing (need -L + UA)
curl -m 15 -L -A "Mozilla/5.0" "https://www.bing.com/search?q={query}"

# 5d DuckDuckGo (need -L + UA + 短 timeout)
curl -m 8 -A "Mozilla/5.0" "https://html.duckduckgo.com/html/?q={query}"

### 9.0.3 DuckDuckGo 的真实状态(2026-06-04 二次实测更正)

> **更正**:首次测试(8.0.1 矩阵)显示 DuckDuckGo "❌ 超时",**这是测试方法问题**。
> **二次实测**(`curl -m 8 -A "Mozilla/5.0"` 短 timeout + UA):
> - DuckDuckGo ✅ **200, 30KB**(8 秒内返回)
> - 之前 30s 超时是因为用 `curl` 默认行为(没 UA + 长 timeout)
>
> **真实结论**:
> - DuckDuckGo **可达但需要正确的请求头**
> - 默认 `curl` 不行(被当 bot 屏蔽)
> - 加 `-A "Mozilla/5.0"` + 短 `-m 8` timeout 即可
>
> **替代方案**:
> - **GitHub raw curl** — 已知仓库时最稳
> - **Bing 302 follow + UA** — 通用 web 搜索(115KB 完整结果)
> - **DuckDuckGo + UA + 短 timeout** — 隐私搜索备选
> - **session_search / lcm_grep** — 已有知识兜底
> - **已知链接直接 web_extract** — 不搜索,只提取

### 9.0.4 1 次 mcp_minimax 返回 10 条 vs Tavily MCP 3 条

| 维度 | MiniMax | Tavily MCP |
|---|---|---|
| **结果数** | 10 | 3 (max_results=3) |
| **质量评分** | 无 score | 有 score 0.0-1.0 |
| **中文** | 优秀 | 一般 |
| **学术/技术** | 中等 | 优秀 |

**实践**:中文/通用查 → `mcp_minimax_web_search` 一次顶 3 次 Tavily;英文/技术栈 → Tavily MCP(配 score 过滤)。

### 9.0.5 5 路并发 + terminal 兜底标准代码(2026-06-04 实测版)

```python
def search_with_fallback(query: str, max_per: int = 5):
    """4 路 MCP 优先 + 3 路 terminal curl 兜底,先到先合并"""
    engines = [
        ("minimax", lambda: mcp_minimax_web_search(query=query)),
        ("tavily_google", lambda: mcp_tavily_mcp_google_tavily_search(
            query=query, max_results=max_per, search_depth="basic")),
        ("tavily_microsoft", lambda: mcp_tavily_mcp_microsoft_tavily_search(
            query=query, max_results=max_per, search_depth="basic")),
        ("tavily_ggc", lambda: mcp_tavily_mcp_ggc_tavily_search(
            query=query, max_results=max_per, search_depth="basic")),
    ]
    
    seen_urls = set()
    merged = []
    failed = []
    
    # 顺序跑 4 路 MCP(节省配额 + 故障转移)
    for name, fn in engines:
        try:
            r = fn()
            results = r.get("results", []) if isinstance(r, dict) else r
            for item in results:
                url = item.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    item["_source"] = name
                    merged.append(item)
        except Exception as e:
            failed.append((name, str(e)[:100]))
    
    # terminal curl 兜底
    if not merged:
        import httpx
        # 5a: GitHub raw (已知仓库时)
        if query.startswith("github:"):
            repo = query[7:].strip()
            try:
                r = httpx.get(f"https://raw.githubusercontent.com/{repo}/main/README.md", timeout=10)
                if r.status_code == 200:
                    merged.append({
                        "title": f"{repo} README",
                        "url": f"https://github.com/{repo}",
                        "content": r.text[:5000],
                        "_source": "github_raw"
                    })
            except: pass

        # 5b: arXiv (学术查询)
        elif any(kw in query.lower() for kw in ['paper', 'arxiv', 'research', 'study']):
            try:
                r = httpx.get(f"https://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_per}", timeout=10)
                if r.status_code == 200:
                    merged.append({
                        "title": f"arXiv: {query}",
                        "url": "https://arxiv.org",
                        "content": r.text[:5000],
                        "_source": "arxiv"
                    })
            except: pass

        # 5c: Bing (通用 web 搜索,需要 UA + follow_redirects)
        else:
            for source, url_fn in [
                ("bing", lambda q: f"https://www.bing.com/search?q={q}"),
                ("duckduckgo", lambda q: f"https://html.duckduckgo.com/html/?q={q}"),
            ]:
                try:
                    r = httpx.get(
                        url_fn(query),
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                        follow_redirects=True,
                        timeout=8 if source == "duckduckgo" else 15
                    )
                    if r.status_code == 200:
                        # Bing/DDG 返回 HTML,需要进一步解析(留 TODO)
                        merged.append({
                            "title": f"{source}: {query}",
                            "url": url_fn(query),
                            "content": r.text[:3000],
                            "_source": f"{source}_curl"
                        })
                        break  # 第一个成功的就够
                except: pass

    return merged, failed
```

### 9.0.6 历史教训

- ❌ SKILL 文档 v6.11.0 写"7 路并发" — 实际只有 4 路(MCP) + 0 路(REST,因 401)
- ❌ SKILL 文档写"REST 432 配额耗尽自动切 key2" — 实际是 401 key 失效,key2 也没用
- ❌ SKILL 文档写"DuckDuckGo 免费兜底" — 实际默认 curl 不可达,加 UA + 短 timeout 后可用(§ 9.0.3)
- ✅ **修正方案**:本节以实测为准,文档与现实对齐

### 9.0.7 自检脚本(每月 1 号重测)

```python
# search_channels_probe.py — 验证当前环境所有搜索通道
import json
import subprocess

results = {}

# 1. MCP channels (通过 Hermes tools)
# 实际由 Agent 执行,这里只描述流程
results['mcp_minimax_web_search'] = "✅ if 10 organic results, else ❌"
results['mcp_tavily_google'] = "✅ if 3 results, else ❌"
results['mcp_tavily_microsoft'] = "✅ if 3 results, else ❌"
results['mcp_tavily_ggc'] = "✅ if 3 results, else ❌"
results['web_search'] = "✅ if not 401"

# 2. terminal channels
import httpx
for name, url in [
    ("github_raw", "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md"),
    ("arxiv", "https://export.arxiv.org/api/query?search_query=ai&max_results=1"),
    ("bing", "https://www.bing.com/search?q=test"),
]:
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        results[name] = f"✅ {r.status_code}" if r.status_code == 200 else f"⚠️ {r.status_code}"
    except Exception as e:
        results[name] = f"❌ {type(e).__name__}"

print(json.dumps(results, indent=2, ensure_ascii=False))
```

### 9.0.8 何时重测本节

- MCP server 配置变更(增加/删除通道)
- web_search 工具 backend 改回 tavily / 换其他后端
- 网络环境变更(国内/国外切换)
- 每月 1 号(配额重置后)

**重测触发**:每月 cron 1 号自动跑 9.0.7 自检脚本,结果写入 log.md。

---

## 9.1 用户纠正案例(2026-06-04 沉淀)

> 本节记录 2 个用户实际纠正的决策陷阱,未来 Agent 必须避免。

### 9.1.1 触发信号是 OR 条件,不是 IF-THEN 模板(用户纠正 #1)

**错误**:
- 用户说"ai-harness-exploration 继续探索 agent 如何使用 wiki"
- Agent 套"内部合成模式"模板,因产物已存在而**跳过 web 搜索**
- 用户立即纠正:"为什么没有 web 搜索"

**根因**:
- 内部合成模式触发条件:产物已存在 → filesystem-only
- 但用户的**第二个问题**"如何创建更好的 wiki 库"是**元方法论问题**,需要业界参照系
- **AI 把 OR 条件当 IF-THEN 跑** — 看到"基于已有 X"就跳到"不需要外部知识"

**修正**(写入决策树):
```
判断"是否需要 web 搜索" = OR 多个信号:
  ├─ 信号 1: 元方法论问题?(例如"如何做 X 更好")
  ├─ 信号 2: 需要业界 2026 共识?
  ├─ 信号 3: 产物已存在(可减搜索量,不可全跳)?
  └─ 任一信号命中 → 必须 web 搜索

错误反模式:
  看到"产物已存在" → 完全跳过 web 搜索  ← 错
  看到"产物已存在" → 减搜索量 + 重点放在合成  ← 对
```

**应用到未来**:
- 用户说"基于已有 X 写 Y" → 仍要判断是否需要外部参照
- 元方法论/范式/原则类问题 → web 搜索必走
- 纯内部合成(整理已有产物)→ 可不搜

### 9.1.2 测试方法错误 ≠ 通道不可达(用户纠正 #2)

**错误**:
- 第一次测 DuckDuckGo:`curl` 默认 + 30s timeout → 超时
- SKILL 文档说"DuckDuckGo 不可达"
- 二次实测:`-A "Mozilla/5.0"` + 8s 短 timeout → **200, 30KB**
- 之前 30s 超时 = 配置错,不是不可用

**根因**:
- 默认 `curl` 没 UA → 被搜索引擎当 bot 屏蔽
- 默认 30s timeout → 哪怕能通也浪费 22s
- AI 看到"超时"就判定"不可达",没意识到**测试方法本身有问题**

**修正**(写入 SKILL § 9.0.3):
```
判断"通道不可达" = 必须三重确认:
  ├─ 测试 1: 默认 curl (30s)        → 超时?
  ├─ 测试 2: -A "Mozilla/5.0" + 短 timeout  → 仍超时?
  └─ 测试 3: 浏览器模拟(高保真)     → 仍超时?
  
  3 个测试都失败 → 真不可达
  任一测试成功 → 测试方法错,通道实际可用
```

**应用到未来**:
- 通道"不可达"判定必须用**至少 2 种方法**测试
- 搜索引擎类通道默认需要 `User-Agent: Mozilla/5.0`
- 8s 短 timeout 是 30s 失败后的**重新评估信号**,不是"放弃"信号
- "不可达"结论写入文档前必须 2 次验证

### 9.1.3 Wiki 写入不申请 = 违反 skill 协议(用户纠正 #3,2026-06-04 v6.15.0)

**错误**:
- 用户之前说"如何创建更好的 wiki 库" — 元方法论问题
- Agent 跑了 5 路 web 搜索 → 6 个 wiki 写入(2 显式 + **4 边界**)
- 4 个边界写入(`goal-alignment` / `multi-agent-detail` / A2A 段 / `per-project-claude-md-template`)用户**没明示**
- Agent 没问"这 4 个写不写",直接写
- 然后用户说"跑 1 个真多 Agent 任务" — E2E 写了 10 个文件
- 然后**用户提醒**:"检查 lcm 压缩归档,不要随意写进 wiki 中"

**根因**:
- "Wiki 集成模式"v6.12.0 写"必落:产物写到 wiki/" → **强制写**没申请
- AI 把"产物该沉淀"理解为"立即写" — 没意识到**写入是不可逆操作**
- 边界写入 = 用户没明示,但 Agent 觉得"既然谈到了就写吧"
- 多次累积 → 用户感觉"被扩张性写入"

**修正**(写入 SKILL § 4.0 + 决策树):
```
任何 wiki 写入 = 必须申请(不可绕过)

申请格式(必走):
  1. 列候选清单(文件/类型/大小/来源/是否用户要求)
  2. 每个文件 1 段内容摘要
  3. 标注用户显式 vs 边界
  4. 询问"写哪些/全部/不写"
  5. 用户决定后才执行
  6. 拒绝内容移到 `scratchpad/_drafts/`

例外(不需要申请):
  - 用户显式说"写 X 到 wiki/concepts/..."
  - 任务中必然的副作用(如创建任务页)
  - 自测试临时文件(写到 scratchpad)
```

**应用到未来**:
- ❌ "产物该沉淀" ≠ "立即写" — 写入是不可逆
- ✅ 元方法论探勘:先列 3-5 个候选,问用户"哪些要写"
- ✅ LCM 摘要 / Session 历史 → 禁止写 wiki(LCM 不知道 wiki 存在)
- ✅ 边界写入 = "我自己觉得有用" ≠ "用户要"

### 9.1.4 多次纠正才停 = 缺少"中途自检"(用户纠正 #4,2026-06-04 v6.15.0+)

**错误**:
- 用户说"如何创建更好的 wiki 库" — 我跑了 5 路 web 搜索 → 6 个 wiki 写入(2 显式 + 4 边界)
- 之后用户说"跑 1 个真多 Agent 任务" — 我又写了 10 个 E2E 文件
- 之后**用户提醒**:"检查 lcm 压缩归档,不要随意写进 wiki 中"
- 实际上**前两个任务**就已经存在扩张性写入,但用户直到第 3 次才明确说

**根因**:
- 每次新任务开始 → 我**没有回头检视**之前的写入是否在用户预期内
- "用户没反对" ≠ "用户同意" — 用户可能没注意到
- 多次任务累积 → 用户感觉"被扩张性写入",才明确纠正

**修正**(在每次新任务开头加 5 秒自检):
```
新任务开始(尤其和前次任务有重叠时):
  ├─ 上次我写了什么?grep 一下 " 1.5 小时内" 的写入记录
  ├─ 哪些是用户显式要?哪些是"我自加"?
  ├─ 上次用户有任何提醒/批评吗?
  ├─ 如果上次有自加文件 → 这次更克制,先问清单
  └─ 自加倾向指数: 3+ 边界文件 = 立即停下申请,不写
```

**应用到未来**:
- ❌ "用户没反对" ≠ "用户同意" — 沉默不是同意
- ✅ 多次任务累积 = 收紧边界,不是放宽
- ✅ 第 1 次自加 OK,第 2 次自加要申请,第 3 次自加完全停止
- ✅ 回头 grep 自己最近的写入 = 5 秒自检成本低,信息量大

### 9.1.5 commit + push 假成功 = 输出截断 + 单一信号依赖(用户纠正 #5,2026-06-04 v6.17.0)

**错误**:
- 本会话 5-6 次 commit + push 报告"成功" → 实际 git 没记录
- 累积 668 行内容从来没真推
- 直到 3rd 端 wiki-keeper 跑 commit 迫使我 `git pull --rebase`,发现本地和远端不一致 → 才意识到假成功

**根因**:
- `branch.main.merge = refs/heads/master` 残留 bug → `git pull --rebase` 失败被静默忽略
- `git commit` 因 LF/CRLF 警告 / untracked 干扰 / 其他原因**失败**但**输出截断**显示成功
- `git push` 报 "Everything up-to-date" → 我以为成功
- 关键:**没核 `git cat-file -t <hash>` 验证 commit 对象存在**
- 关键:**没核 `git rev-parse origin/main` 跟 `git rev-parse HEAD` 对比**

**修正**(写入 § 4.0.9 5 步核验硬协议):
```
任何 wiki 写入 = commit + push, 必须走 5 步核验:
  [1] git status --short
  [2] git add -A
  [3] git commit -m "..."
  [4] git cat-file -t HEAD   ← 核对象存在
  [5] git push + rev-parse 对比  ← 核远端 hash 一致
```

**应用到未来**:
- ❌ `git commit` 输出"成功" = 不可信
- ❌ `git push` 输出"Everything up-to-date" = 不可信
- ❌ 信任 shell 输出, 没核 hash = 假成功高发
- ✅ `git cat-file -t HEAD` 输出 "commit" = commit 真存在
- ✅ `git rev-parse origin/main` = `git rev-parse HEAD` = push 真成功
- ✅ 自动化 `safe-commit-push.sh` = 5 步核验 + 失败自动回滚

**用户硬偏好**(写入 § 4.0.9):
- 唯一远端: `https://github.com/AK47ZZQ/agent-wiki` (用户明确说"我的仓库是 agent-wiki")
- author: `Hermes <hermes@hermes.local>` (用户明确说"上传称名称改为 Hermes")
- hermes-all 远端已被用户**彻底删除**, 不再使用 — 所有内容走 agent-wiki

## 9.2 内部合成模式的 4 个反模式(已写入 references/internal-synthesis-mode.md,此处提示)

详见 `references/internal-synthesis-mode.md` 的"6 反模式"段。

**关键 2 个本次会话验证过的**:
- A: OR 条件被当 IF-THEN 模板(就是 9.1.1)
- B: 产物已存在 = 跳 web 搜索(就是 9.1.1 的子模式)

---

## 参考资料

| 来源 | 参考位置 |
|:----|:--------|
| Harness Engineering 完整框架 | wiki/concepts/harness-engineering-deep-study.md |
| Ralph Wiggum Loop | wiki/methods/ralph-wiggum-loop.md |
| Guides×Sensors 控制论 | `skill_view("hermes-workflow", "references/guides-sensors.md")` |
| 搜索深度与广度策略（含 MCP 优先架构） | `skill_view`("ai-harness-exploration", "references/search-depth-strategy.md") |
| 内部多源合成模式（filesystem-only,无 web 搜索） | `skill_view`("ai-harness-exploration", "references/internal-synthesis-mode.md") |
- 快速启动卡 | `skill_view`("ai-harness-exploration", "references/quickstart.md")
- 必要性验证门控 (Step 0c) | `references/should-i-build-gate.md`
- 深度研究方法论 | `skill_view`("ai-harness-exploration", "references/deep-research-methodology.md")`
- **SOUL 设计范式（5 范式 / 3 误读 / 1 反身性原则）** | `references/soul-design-pattern.md`（2026-06-04 沉淀自 v1→v5 SOUL 迭代）
- **Agent SOUL.md 写作方法论** (8 段结构 + 自指 critique + 4 范式) | `references/agent-soul-authoring.md`（v1 早期版,与 soul-design-pattern.md 互补：前者讲"如何写",后者讲"写错了怎么真改"）
- 技能自测试方法论 | `skill_view`(references/skill-self-testing.md) |
| 镜像测试协议与结果 | `skill_view`(references/mirror-testing-protocol.md) |
| 故障排除手册 | `skill_view`("ai-harness-exploration", "references/troubleshooting.md") |
| Hermes Workspace 部署与远程访问 | `skill_view`("ai-harness-exploration", "references/hermes-workspace-deployment.md") |
| **Wiki 写入边界** (LCM/Scratchpad/Wiki 三层 + 3 反模式) | `references/wiki-write-boundary.md`（2026-06-04 用户"不要随意写进 wiki"纠正沉淀） |
| **E2E 多 Agent 协议测试** (3 Agent 真任务 15 min 跑通) | `references/e2e-multi-agent-test.md`（2026-06-04 实测, 6/6 原语, 8/8 验收） |
| **Wiki 写入 5 步核验协议** (commit+push 假成功防御 + 11 速查陷阱) | `references/wiki-write-verification-protocol.md`（2026-06-04 v6.17.0 用户硬偏好: author=Hermes, 远端=agent-wiki, hermes-all 已删） |

## 内部合成模式版本元数据

- **v1** (2026-06-04): 首次添加,基于 SOUL.md 多源合成会话
  - 触发信号清单（"基于已有 X 写 Y" 等 3 个核心句式）
  - 6 步探勘法的 filesystem-only 适配（inventory → taxonomy → DRY 决策 → meta 验证）
  - SOUL.md 工作示例（9 源 → 4 类 taxonomy → 1 个 v3 SOUL）
  - 6 个反模式（避免堆叠/自动同步/新建 wiki 概念页/重复模板内容等）
