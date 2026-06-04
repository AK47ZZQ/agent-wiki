---
title: Wiki 集成模式 — ai-harness-exploration 探勘产物自动落 wiki
created: 2026-06-04
updated: 2026-06-04
type: reference
tags: [ai-harness-exploration, wiki, integration, code-workflow, second-brain]
source: internal-synthesis-2026-06-04
confidence: high
---

# Wiki 集成模式 — ai-harness-exploration 探勘产物自动落 wiki

> **集成时间**:2026-06-04
> **目的**:ai-harness-exploration 跑完任何探勘流程后,**自动**把产物写到 wiki,不留在 chat。
> **核心 3 原则**:
> 1. 探勘产物 = 第二大脑沉淀(不留 chat)
> 2. CODE 4 阶段是骨架(Capture→Organize→Distill→Express)
> 3. 5 评估指标是质量门

## 1. 触发条件(何时启用本模式)

满足任一条件,启用本模式:

- 用户说"探勘wiki" / "改进wiki" / "wiki如何更好" / "怎么用wiki" / "wiki库设计"
- 任务涉及 wiki 的方法/协议/分类法
- 探勘结果包含**新方法/新范式/新原则**(值得沉淀)
- 多个探勘结果需合并到 wiki

不适用(用标准探勘):
- 纯问答("X 是什么?")
- 临时分析(产物只在 chat 用)
- 用户明确说"不要写 wiki"

## 2. 强制流程(8 步)

```
Step 1: 读 SKILL frontmatter → 确认触发模式
        ├─ 探勘 wiki → Wiki 集成模式
        └─ 普通探勘 → 6 步法

Step 2: 读 2 个核心 wiki 页(必读,不读不写)
        ├─ [[methods/wiki-as-second-brain]] — 协议 + DRY + 评估
        └─ [[methods/wiki-code-workflow]] — CODE 4 阶段

Step 3: 评估当前 wiki 状态(CODE 4 阶段盘点)
        ├─ raw/ 有多少? (Capture)
        ├─ concepts|entities|methods|... 有多少? (Organize)
        ├─ methods/ 提炼了多少? (Distill)
        └─ log.md + skills/ 多少? (Express)

Step 4: 跑标准 6 步探勘(分析/搜索/交叉验证)

Step 5: 决定产物类型(6 选 1)
        ├─ 概念 → concepts/X.md
        ├─ 方法 → methods/X.md
        ├─ 实体 → entities/X.md
        ├─ 对比 → comparisons/X.md
        ├─ 短记录 → notes/X.md
        └─ 范式级 → methods/X.md (作为新 skill 候选)

Step 6: 写 frontmatter(9 字段,见协议 § 5.7)

Step 7: 写正文
        ├─ 1-page overview(≤ 200 行)
        ├─ ≥ 2 条 wikilink 出链
        ├─ ≥ 1 条可执行步骤(method 时)
        └─ ≥ 1 个 source 链接

Step 8: 索引 + 同步
        ├─ 更新 wiki/index.md(加条目)
        ├─ 更新 wiki/log.md(记一笔)
        ├─ grep 验证 wikilink 可达
        └─ 报告: 写入了哪些文件 + 删了哪些
```

## 3. 强制阅读(每次 wiki 集成探勘必读)

```
前 3 个必读:
  1. wiki/methods/wiki-as-second-brain
     └─ 5 DRY 原则 + 5 字段铁律 + 6 wikilink 规则 + 3 反模式 + 5 评估指标
  
  2. wiki/methods/wiki-code-workflow
     └─ CODE 4 阶段 (Capture/Organize/Distill/Express) + 各自 4 步 + 7 自检清单

  3. wiki/protocols/multi-agent-detail § 5.7
     └─ 4 类 frontmatter schema 必填字段 + 验证规则

后 3 个按需:
  4. wiki/protocols/goal-alignment — 主动告警机制
  5. wiki/protocols/agent-coordination — 6 原语
  6. wiki/protocols/per-project-claude-md-template — per-project 模板
```

## 4. 5 评估指标(质量门)

任何 wiki 写入后必须自检:

| # | 指标 | 目标 | 检测方法 |
|---|---|---|---|
| 1 | **协议可达性** | Agent 启动 ≤ 2 跳达协议 | index.md + CLAUDE.md 列出 |
| 2 | **内容可达性** | Agent 找页 ≤ 2 跳 | index.md 列出所有内容 |
| 3 | **协作可达性** | 找其他 Agent ≤ 2 跳 | agents/README + agents/<id>.md |
| 4 | **索引更新率** | 写新页后 24h 内 index.md 更新 | git log 检查 |
| 5 | **死链率** | < 1%(非 plain text) | 扫描 [[X]] 真死链 |

## 5. CODE 4 阶段映射

每次 wiki 集成探勘,把产物映射到 CODE 4 阶段:

| 探勘动作 | CODE 阶段 | 写到哪里 |
|---|---|---|
| 抓 web 文章 / 飞书消息 | Capture | `raw/<category>/<source>-<date>.md` |
| 读 5 篇文章找共同主题 | Organize | `concepts/X-2026.md` (聚合) |
| 多个 concept 提炼 | Distill | `methods/X-method.md` (1-page) |
| 提炼完整方法论 | Distill | `methods/X-deep-study.md` (交叉引用页) |
| 跑完任务写总结 | Express | `log.md` (进度更新) |
| 完成 → 公开给用户 | Express | `exports/X.md` 或 `skills/X` |

## 6. 反模式(本模式严禁)

| 反模式 | 后果 | 修法 |
|---|---|---|
| 探勘结果只写 chat 不写 wiki | 等于浪费,下次找不到 | 强制 Step 7-8 写入 + 索引 |
| 大段粘贴原文 | 违反 1-page overview | 写提炼,不超过原文 20% |
| 写新页不更新 index | 找不到 | Step 8 必走 |
| wikilink 引用不存在的源 | 死链 | grep 验证后写 |
| skill 引用用 wikilink | 假死链 | 用反引号 `skill-name` |
| 概念解释用 wikilink | 假死链 | 用反引号 `concept` |
| frontmatter 缺字段 | 协议违规 | 9 字段必填 |
| 不带 source 链接 | 无法追溯 | frontmatter `source:` 必填 |

## 7. 实际案例(2026-06-04)

### Case 1:wiki-as-second-brain 探勘(本会话)

**触发**:用户说"如何创建更好的 wiki 库"
**走模式**:Wiki 集成模式
**实际产物**(6 文件):
- `methods/wiki-as-second-brain.md` (12.6K) — Distill 产物
- `methods/wiki-code-workflow.md` (10.0K) — Distill 产物
- `protocols/goal-alignment.md` (5.5K) — Distill 产物
- `protocols/multi-agent-detail.md` (5.5K) — 已有,扩充
- `protocols/agent-coordination.md` (5.2K) — 已有,加 A2A 段
- `protocols/per-project-claude-md-template.md` (6.7K) — Distill 产物

**同步更新**:
- `index.md` — 4 段新目录入口
- `log.md` — 2 条新记录
- `scratchpad/wiki-multi-agent-refactor/` — 任务 workspace

**5 评估指标**:
- ✅ 协议可达性:1 跳
- ✅ 内容可达性:1 跳
- ✅ 协作可达性:1 跳
- ✅ 索引更新率:本次同步
- ✅ 死链率:0

### Case 2:之前错误示范(本会话)

**触发**:用户说"ai-harness-exploration 继续探索"
**走错模式**:套了"内部合成模式",跳过 web 搜索
**结果**:用户批评"为什么没有 web 搜索"
**教训**:触发信号是 OR 条件,"基于已有 X" 不等于 "不需要外部知识"

**改进**:
- 5 路并行 web 搜索(实际产出 12 模式 × 20 来源)
- 重新合成到 wiki-as-second-brain(12K 含 20 来源 markdown link)
- 加 A2A 映射 + Goal Alignment + CODE 4 阶段

## 8. 自动检测(可机械化)

未来可以写一个 `wiki_lint.py` 自动检测:

```python
# 检测项
checks = [
    "frontmatter_9_fields(content pages)",
    "wikilink_resolves(vs plain text误报)",
    "skill_ref_uses_backtick(not wikilink)",
    "index_md_lists_all_content(无遗漏)",
    "log_md_updated_within_24h_of_new_page",
    "no_orphan_empty_files",
    "A2A_protocol_primitive_named_consistently",
    "namespace_isolation_in_scratchpad(<task-id>/)",
]
```

输出:`{file: [checks_passed], [checks_failed]}` + 修复建议。

## 9. 关联

- 本 skill:[[SKILL.md]] 主页
- 元方法论:[[wiki/methods/wiki-as-second-brain]]
- 工作流:[[wiki/methods/wiki-code-workflow]]
- 协议:[[wiki/protocols/multi-agent-detail]]
- 主动告警:[[wiki/protocols/goal-alignment]]
- 6 原语:[[wiki/protocols/agent-coordination]]
- per-project 模板:[[wiki/protocols/per-project-claude-md-template]]
- 内部合成对比:[[references/internal-synthesis-mode.md]]
- 自优化:[[references/should-i-build-gate.md]]

## 10. 版本历史

- v1.0 (2026-06-04) — 初始版本,从 wiki 集成会话提炼
