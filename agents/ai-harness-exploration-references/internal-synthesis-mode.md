# Internal Synthesis Mode（内部多源合成）

> 6 步探勘法的第三种模式 — 区别于"未知→已知"和"深度延续搜索"。

## 何时触发

- 用户说 **"基于已有的 X 写一份 Y"** / **"结合文件 + 你的实际"** / **"整合这几个"**
- 主题在系统内已有 ≥ 2 份现成产物（SOUL.md / MEMORY.md / skill / wiki 概念页 / AGENTS.md 等）
- **不需要外部 web 研究**（或只需补充 1-2 次验证）
- 多份产物彼此**有重叠也有差异**,需要融合

## 与另外两种模式的差异

| 模式 | 触发信号 | 工具链 | 耗时 |
|:----|:--------|:-----|:----|
| 未知→已知 | 主题完全陌生 | 5 次 web_search + web_extract | 30 分钟 |
| 深度延续搜索 | "继续" / "再深入" | 多角度 web + 横向扩展 | 8-12 分钟 |
| **内部合成** | "基于已有写一份" | **filesystem 探勘 + read_file + 模式提取** | **10-15 分钟** |

## 适配的 6 步法

### Step 0a — Source inventory（替代 web 搜索）
```
search_files(pattern="*<topic>*", target="files", path=~/hermes-all)
search_files(pattern="*<related>*", target="files", path=~/hermes-all)
```
- 列出**所有相关文件**（不只"看起来对"的那一个）
- **不要跳过这一步**,即使你"已经知道系统长什么样" — 清点本身就是基础

### Step 0b — 必要性验证（仍然适用）
- 6 问清单：痛点 / 边际价值 / 替代 / 成本 / 推销自检 / 退出成本
- 内部合成也要问"该不该写" — 不要"因为有现成的就值得新写"

### Step 1 — Analyze（替换 web_extract 为 read_file 群读）
- **群读所有候选**（read_file 并行,不是先读一个再读下一个）
- **建立分类学 (taxonomy)** — 类型化区分
  - 例: 9 个 SOUL.md → identity / instance / operational / profile 4 类
- **识别重叠 vs 差异** — 重叠的提取公共模式,差异的提取"互补点"

### Step 2 — Extract（模式分组,不是 web 摘录）
- 按类型分组模式
- 标注**哪个模式唯一 / 哪个跨源共有**
- 标注"现有产物中**缺什么**" — 这就是新产物的差异化空间

### Step 3 — Formalize（决策优先于写作）
- **决策 1**: 写到哪里（覆盖现有 / 新建 / 合并多个）
- **决策 2**: 目标读者和使用场景
- **决策 3**: 模式 → 章节的映射（不要"全塞进去"）
- **DRY 原则**: 不要复制"已经在模板里的内容" — 让新产物只写它独特负责的部分

### Step 4-5 — Deliver + Verify（标准）
- 写文件 + 读回检查
- 验证结构（行数、章节、出链、错误账本等）

### Step 6 — Debrief（加强版）
- 列出"哪些现有产物现在变成新产物的下游"（DRY 收尾）
- 列出"哪些产物可以**反向引用**新产物"

---

## 工作示例:SOUL.md 多源合成

**任务**: "结合其他 soul 相关信息和你的实际情况写一份最好的 soul"

### 探勘结果（8 源）

| 文件 | 类型 | 角色 |
|:----|:----|:----|
| `hermes/SOUL.md`（根）| Identity seed | 官方 1 段,通用 Hermes Agent 人设 |
| `hermes/memories/SOUL.md`（旧版）| Instance | "我信/反对/拒绝"+ 错误账本 |
| `hermes/profiles/minimax-worker{1..7}/SOUL.md` | Profile copies | 7 份相同 worker 配置 |
| `hermes/skills/devops/kanban-worker/templates/worker-soul.md` | Operational | worker 任务手册 + 防死循环 |
| `hermes/skills/mcp/openclaw-integration/SKILL.md` | External schema | OpenClaw SOUL.md/IDENTITY.md/AGENTS.md 转换 |
| `hermes/skills/.../agency-agents-pattern.md` | External schema | agency-agents 范式（106k★）|
| `hermes-workflow` SKILL.md | Internal behavior | 实际行为模式 + 工具决策 |
| `wiki/concepts/concept-kanban.md` | Wiki concept | Kanban 系统架构 |

### 提炼的 4 大模式

1. **Vibe 一句话**（来自 agency-agents）— 顶部 blockquote,让人一眼记住
2. **反规则 > spec**（来自旧版 instance SOUL）— "我不做什么"比"我能做什么"更暴露身份
3. **错误账本**（来自旧版 instance SOUL）— 历史错误可见,永远不擦
4. **元规则**（来自信 6 "护栏双向性"）— SOUL 自身的约束（不自动改 / 不被 cron 写 / ≤ 150 行）

### 关键决策

- **写到哪里**：`hermes/memories/SOUL.md`（覆盖旧版,不是新建）— 旧版位置正确,只是要升级
- **不写到哪里**：`hermes/SOUL.md` 根（是 seed template）/ worker-soul.md（是任务手册）/ 7 个 profile 副本（是 worker 配置）
- **职责分离**：
  - 主 SOUL = "我是谁、信什么、拒什么"
  - worker-soul = "能做什么、怎么防死循环"
  - profile SOUL = "运行配置（模型、降级链）"
- **不复制已有内容**:主 SOUL 不重复 worker 手册,worker 手册不重复主灵魂

### 验证

- 行数 ≤ 150（SOUL 自身的元规则,违反 = 失去灵魂变 SOP）
- 6+6+6 结构（信/反对/拒绝）
- 错误账本 5 条（跨 4 源: Hindsight/cron/4 文档/corona 搜索/反弹信号）
- 跟你的关系部分（人味,不是孤立 agent）

---

## 反模式（避免）

- ❌ 把所有 N 份候选当作同等重要（绝大多数是重复副本）
- ❌ 新文档比模板长 5 倍（违反 SOUL ≤ 150 行 / SKILL.md ≤ 600 行原则）
- ❌ 写完就自动同步到 cron / 触发其他子流程（违反"反对自动维护"）
- ❌ 为这次合成再建一个 wiki 概念页（违反 4 文档→1 文档教训）
- ❌ 跳过 inventory 步骤因为"我以为我知道"

### 输出形状：1 文档 vs "1 摘要页 + N 处补丁"（NEW 2026-06-04, wiki 第二大脑案例）

内部合成不总是"覆盖一个文件"。当任务是**"用 N 份已有产物回答一个新问题"**（不是"升级 X 文档"），输出形状是：

```
1 篇综合方法论页（提炼模式，不是复制原文）
+ N 处针对性 patch（修复 1 处不一致、补 1 个缺失段、合并 1 个 stub）
+ index.md 重写（catalog 必须包含新内容，否则"看不见"，见 wiki-lint pitfall #18）
+ log.md 追加（1 段记录本次合成）
```

**案例：2026-06-04 wiki 第二大脑探勘**

输入：11 份产物（CLAUDE.md/AGENTS.md/agents/*/scratchpad/*/tasks/*/protocols/*）
任务："agent 如何正确使用 wiki + 如何创建更好的 wiki 库"

| 输出类型 | 文件 | 角色 |
|---|---|---|
| **新方法论页** | `methods/wiki-as-second-brain.md` (8.3K) | 4 步启动序列 + 5 DRY + 5 字段铁律 + 6 wikilink 规则 + 5 评估指标 |
| **重写** | `index.md` | 加 4 段新目录(agents/scratchpad/tasks/protocols) |
| **补丁** | `agents/hermes-kanban-worker.md` | 补实例化命名 + 模板/实例关系 |
| **补丁** | `tasks/cleanup-worker-debris.md` | assignees 修正 |
| **状态更新** | `scratchpad/ephemeral-...md` | todo 全部 done |
| **关闭任务** | `tasks/wiki-multi-agent-refactor.md` | status → done |
| **追加日志** | `log.md` | 2030 字本次探勘记录 |

**关键判断**："要不要新建 11 份产物对应的 11 个新概念页？" — 不要。那是"过程"不是"知识"。**1 篇综合方法论页 + N 处针对性 patch** 才是知识库该长成的样子。

**何时用 "1 文档覆盖"形状**：源是"同一事物的不同表达"（9 份 SOUL.md → 1 份最佳 SOUL，参见上方案例）
**何时用 "1+N 形状"**：源是"不同事物回答同一类问题"（agents/scratchpad/tasks/protocols/ → 1 篇方法论 + N 处更新）

判断标准：合并后是否产生**新概念**？是 → 1 文档；否 → 1+N。

## 何时不用

- 主题是纯外部（无内部文件存在）→ 走"未知→已知"模式
- 快速事实问题（"X 是什么"）→ 走 Quick Analysis 模式
- 一个源明显权威（无合成必要）→ 直接采用,不强求融合
- 用户说"算了不改了" → 立即停,不写

---

## 4 大反模式（NEW 2026-06-04 — 来自"为什么没有 web 搜索"事件）

> 这 4 条都是**同一次失败**的不同侧面：用户问"agent 如何使用 wiki + 如何创建更好的 wiki 库"，我看到内部已有 11 份产物就套了 internal-synthesis 模式（filesystem-only），完全跳过 web 搜索。用户反问"为什么没有 web 搜索"——这是首次明确拒绝我的模式选择。

### 反模式 A：触发信号 = 模板（OR-条件被当 IF-THEN）

internal-synthesis 模式的**触发信号**有 3 个 OR-条件：
1. "基于已有的 X 写一份 Y"
2. "结合文件 + 你的实际"
3. "整合这几个"

我看到 11 份产物就自动套了，**没有**问"用户的需求是文件系统操作能完全覆盖吗？"

**正确做法** — 触发信号是 OR，不是 IF-THEN 模板：
- 即使所有 3 个 OR-条件都命中，只要还有**外部参照需求**（如"如何创建更好的 X 库"这种**元方法论**问题），就**必须双重验证**（web 搜索 + filesystem）
- 元方法论问题（如何做 X、什么是 X 的最佳实践）= 永远需要外部参照
- 增量更新问题（"X 文件加上 Y 段"）= filesystem-only 可能够
- 决策清单：
  ```
  □ 1. 用户的问题是关于"已有产物"（factual）还是"如何做得更好"（methodological）？
       factual → filesystem-only
       methodological → 必须 web 搜索
  □ 2. 用户提的关键词是否包含业界通用术语（"knowledge graph" "second brain" "agent coordination"）？
       含 → 用户期待业界共识,不是内部答案
       不含 → 内部答案可能够
  □ 3. 问"如何"（how）/ "最佳"（best）/"更好"（better）？
       含 → 元问题,需要外部参照
  ```

**实际案例**（2026-06-04）：用户说"继续探索 agent 如何正确使用 wiki 以及如何创建更好的 wiki 库"——"如何"+"更好"两个信号命中 = 元问题。正确做法是 **6 步迭代搜索（带 web 搜索轮次）**，不是 internal-synthesis。

### 反模式 B：产物已存在 = 跳 web 搜索

我观察到"vault 里已经有 CLAUDE.md、AGENTS.md、agents/README.md..."→ 推断"信息足够"→ 跳过 web。

**这是错的**：
- 内部产物回答"我们当前长什么样"（what-we-have）
- web 回答"业界长什么样"（what-best-practice-says）
- "如何创建更好的 wiki 库" = "我们 + 业界 哪个好？差距在哪？改进方向？"→ **必须双向参照**

**铁律**：看到产物已存在 ≠ 跳过 web。**每 3 个问题至少 1 个问题应该带 web 搜索轮次**，即使其他用了 internal-synthesis。

### 反模式 C：方法论页 = 简单复述内部产物

我写出 `methods/wiki-as-second-brain.md` 12.6K 后，用户批评"为什么没有 web 搜索"——意思是这页**应该是**"我们 + 业界 12 来源交叉验证后的方法论"，实际却是"11 份产物的内部总结"。

**正确做法**：方法论页（method/concept 页）必须**至少 50% 内容来自外部 web 来源**。验证：`grep -c 'https://' file.md` ≥ 5（粗略指标）。

**反例 v1**：12.6K `wiki-as-second-brain.md` 0 个外部 URL（v1 内部合成版）→ 0 / 12.6K
**正例 v2**：v2 加 20 个外部 URL（20 来源）→ 20 / 14K

**判定方法**：写完方法论页后跑 `grep -c 'https://' <file>`，< 5 = 警告"这页内部依赖过重，需要外部验证"。

### 反模式 D：外部 URL 写成 wikilink（"假死链"）

我写了 `[[source-gurusup-multi-agent-frameworks-2026]]` 想引用外部 URL，**没建对应 wiki 页** → 17 个**假死链**。

**正确做法**：
- 外部 URL → markdown link: `[title](url)`
- 内部 wiki 页 → wikilink: `[[page]]` 或 `[[page|alias]]`
- 绝对规则：**不要把外部 URL 编码进 wikilink**

```python
# 错误
"[[source-xxx-multi-agent]]"
# 正确
"[Source X — Multi-Agent](https://example.com/source-xxx)"
```

**自检**：写完方法论页后跑 `grep -n 'https' file.md | grep -v '\[.*\](http'` → 任何 URL 出现在裸文本（无 markdown link 包裹）= 警告。

### 一句话总结（4 反模式合并）

> **元方法论问题 + 产物已存在 ≠ 跳过 web 搜索**。每 3 个问题至少 1 个带 web 搜索，方法论页外部 URL ≥ 5 个，外部 URL 永远用 markdown link 不用 wikilink。

---

## 工具-使用反模式（NEW 2026-06-04 — 来自 write_file backslash 转义）

> **write_file + `[[path|alias]]` 会字面写入反斜杠**：`[[path\|alias]]`。Obsidian 不解析 `\|`，产生死链/解析错误。
> **复现路径**：
> 1. `write_file(path, "...[[my-page|alias]]...")` → 文件里实际是 `[[my-page\|alias]]`
> 2. wikilink 解析失败 → 灰链 / 不显示
> 3. wiki-lint 报死链（如使用严格正则）
>
> **解决**：
> - **首选 `patch` 工具** 而不是 `write_file` 写含 wikilink 的内容（patch 直接是字面替换，无转义）
> - 用 `write_file` 时**避免 `[[path|alias]]` 形式**（改用无 alias 的 `[[path]]`）
> - 写完后立即 `grep -n '\\\\|' file.md` 验证 = 没有匹配 = 干净
>
> **更广的教训**：所有含特殊字符的 markdown 语法（`[[`、`|`、`*` 强调、`>` 引用、`-` 列表符）都可能被工具转义。**写完必须 grep 验证**，不能信任 write_file 的字面字符串就是文件内容。

---

## 模式选择决策树（NEW 2026-06-04 — 用户明确纠正后提炼）

> **问题场景**：用户问"如何创建更好的 wiki 库"——表面看像 internal-synthesis 触发（"结合已有的"），实际是元方法论问题，需要 web 搜索。
> **根因**：我**套了 OR 条件模板**而非综合判断。
> **正确做法**：3 步走。

### Step 1：判断问题类型

```
□ 用户问题是关于"已有产物"还是"如何做得更好"？
  │
  ├─ factual（"X 是什么"/"我们有没有 Y"/"X 文档怎么写"）
  │   → filesystem-only 够
  │   → internal-synthesis 或 quick analysis
  │
  └─ methodological（"如何 X"/"为什么 X"/"更好的 X"/"X 的最佳实践"）
      → 永远需要外部参照
      → 必须 web 搜索 + filesystem 双重验证
```

### Step 2：检查元方法论信号

**任何 1 个命中 → 元方法论 = 必须 web 搜索**:

| 信号 | 例子 |
|---|---|
| 关键词含"如何"/"为什么"/"更好"/"最佳" | "如何创建更好的 wiki 库" |
| 关键词含业界通用术语 | "knowledge graph" / "second brain" / "agent coordination" / "multi-agent" |
| 用户在追问/深化前一次回答 | "继续探索 agent 怎么用 wiki" |
| 用户引用了外部权威/趋势 | "业界共识"/"2026 趋势"/"X 团队说" |

### Step 3：触发模式选择

```
信号全空（factual）→  internal-synthesis / quick analysis
至少 1 个命中（methodological）→ 6 步探勘（带 web 搜索）
```

### 实际案例对照

| 用户说 | 我的旧选择 | 正确选择 |
|---|---|---|
| "基于已有 9 份 SOUL.md 写一份最好的" | internal-synthesis ✅ | internal-synthesis（factual:已有产物升级） |
| "如何创建更好的 wiki 库" | internal-synthesis ❌ | 6 步探勘 + web 搜索（methodological） |
| "继续探索 agent 怎么用 wiki" | internal-synthesis ❌ | 6 步探勘（user 在深化前次回答 = meta） |
| "看看某个仓库" | unknown→known ✅ | 5 步探勘 + 5 web search |

### 一句话规则

> **OR 触发条件 = 必要条件，不充分**。3 个 OR 信号全中 + 1 个元方法论信号 = 必须 web 搜索。**产物已存在 ≠ 跳 web**。每 3 个问题至少 1 个带 web 搜索。

