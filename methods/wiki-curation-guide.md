---
title: Wiki Curation Guide
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, curation, knowledge-management, multi-agent]
sources: [internal-wiki-audit, gtd-2002-david-allen, zettelkasten-1970s-niklas-luhmann, para-tiago-forte, second-brain-github-topic-2026]
---

# Wiki Curation Guide

> 写给每天往 wiki 塞新知识的智能体:怎么判断、怎么写、怎么避免污染。

## TL;DR

1. **进 wiki 前 3 问**:能复用吗?能交叉链接吗?有源吗?3 问都过才收。
2. **每条新知识必须 4 字段**:title / type / tags / sources(frontmatter)。
3. **写完必交叉链接**(至少 2 个 wikilink),孤立页面是 wiki 衰败的第 1 步。
4. **冲突用 4 步解决**:看时间 → 看规模 → 看权威 → 看先 push。
5. **每周日 23:00 自动 sync**(协议 v1.1)。

## 1. 为什么要策展

wiki 不是 git commit history — 它的**价值 = 可发现性 × 准确性 × 链接密度**。一篇没 wikilink 的页面 = 0 价值(无法被检索到)。一篇重复的页面 = -1 价值(浪费搜索时间)。

**GTD 视角**(David Allen 2002,《Getting Things Done》):**收集 → 处理 → 组织 → 回顾 → 行动**。wiki 策展 = 把"信息收集"和"任务处理"合并的版本。

**Zettelkasten 视角**(Niklas Luhmann 1970s):**atomic note**(一卡片一概念)+ **link 优先**(没有 link 的 note = 死笔记)+ **index 入口**。

**PARA 视角**(Tiago Forte):**Projects / Areas / Resources / Archive**。我们 wiki 用的是 PARA 变体:`tasks/` = Projects / `concepts/` = Areas / `methods/` + `entities/` = Resources / `_archive/` = Archive。

**second-brain 实践**(GitHub 890+ repo,2025-2026):**多 agent 共享 KB 的核心 = 一致性协议**(命名/位置/链接规则),不是工具。

## 2. 知识采集 5 问

每条新知识塞进 wiki 前,问 5 个问题:

| # | 问 | 不通过怎么办 |
|---|---|---|
| 1 | **能复用吗?** — 3 个月内我/其他 agent 会再次用? | 不能 → 扔(留 LCM 或 memory) |
| 2 | **能交叉链接吗?** — 至少能 link 到 1 个现有 page? | 不能 → 写完后强制加 2 个 wikilink |
| 3 | **有源吗?** — 有 1+ URL / 文档 / commit 引用? | 没有 → 标 `(unverified)` 或加 `[needs-source]` tag |
| 4 | **位置正确吗?** — `concepts/`(抽象) / `methods/`(流程) / `entities/`(具体) / `notes/`(一次性) / `protocols/`(规则)? | 不确定 → 放 `notes/` 临时,1 周后归档 |
| 5 | **frontmatter 完整?** — title/type/created/updated/tags/sources 6 字段? | 缺 → wiki-keeper check 脚本会报 |

**反面教材**(本 wiki 早期): 21 真死链(指向不存在页面)= 违反 #2;65 缺 frontmatter = 违反 #5。

## 3. 知识类型与目录映射

| 类型 | 目录 | 例子 | frontmatter type |
|---|---|---|---|
| 抽象概念 | `concepts/` | harness-engineering, agent-memory | `concept` |
| 操作方法 | `methods/` | git-tutorial, feishu-rich-messages | `method` |
| 具体实体 | `entities/` | hermes-skill-*, codex | `entity` |
| 一次性记录 | `notes/` | hindsight-risks-2026 | `note` |
| 协议/规则 | `protocols/` | git-collaboration, agent-coordination | `protocol` |
| 任务/项目 | `tasks/` | cleanup-worker-debris | `task` |
| 智能体身份 | `agents/` | main-claude, hermes-3rd | `agent` |
| 协作工作区 | `scratchpad/<task-id>/` | agent-stack-test | `scratchpad` |
| 原始材料 | `raw/tech/` 或 `raw/work/` | awesome-hermes-zh | `raw` |

## 4. 写入流程(8 步)

```
新知识发现
   ↓
[1] 5 问检查(§2)
   ↓ pass
[2] § 4.0 申请(写新 wiki 文件需用户授权)
   ↓ 批准
[3] 选位置(§3 目录映射)
   ↓
[4] 写 frontmatter(6 字段)
   ↓
[5] 写正文(一段一段,不分长文)
   ↓
[6] 加 ≥2 wikilink
   ↓
[7] 跑 check 脚本:bash scripts/check-wiki-quality.py
   ↓ 0 死链 / 0 缺 frontmatter
[8] commit + push(等 3rd 端的 rebase)
```

## 5. 去重与冲突解决

多 agent 同时塞知识 → 必然有重叠。**4 步解决**:

### 5.1 检测

- **同标题**:`find wiki -name "<title>.md"`
- **同关键词**:`grep -r "<key>" wiki/ --include="*.md"`
- **wiki-keeper check 脚本** + 自定义 dedup 报告

### 5.2 4 步决策树

```
[冲突] → 概念相同?
   ├─ YES → 合并(取更全的版本,加 stub 链到旧)
   │         例:`hermes-kanban` 1 个,删 `concept-kanban` 重复
   └─ NO → 概念不同 → 互相加 wikilink(交叉引用)
              例:`concepts/hermes-kanban` + `methods/kanban-execution`
```

### 5.3 合并模板

```bash
# 旧文件保留 + 链到新文件
echo "[[methods/<新文件>|合并: 见新版本]]" >> wiki/<旧文件>.md
git add wiki/<旧文件>.md
git commit -m "merge: <旧> → <新> (新版本更完整)"
```

### 5.4 弃用 vs 删除

**永远不直接删**。先 `mv file.md file.md.deprecated`,1 个月后 git rm。理由:其他 agent 可能还在引用。

## 6. 知识生命周期

| 阶段 | 状态 | 触发 | 动作 |
|---|---|---|---|
| **draft** | scratchpad/ | 新建时 | 写到 scratchpad/,不发布 |
| **active** | concepts/ / methods/ | 通过 5 问 | 写到正式位置 + 加 wikilink |
| **indexed** | index.md 引用 | 跨链接完成 | 在 index.md 出现 |
| **mature** | ≥5 wikilink | 长期活跃 | 加 "core" tag |
| **deprecated** | .deprecated 后缀 | 被新版本取代 | 在文件顶部加 `> 已弃用,请见 <新>` |
| **archived** | _archive/ | >6 月无引用 | git mv 到 _archive/ |

## 7. 写 wiki 的 5 防坑

1. **别写"百科条目"** — wiki 收的是"我们团队学到的"和"agent 操作需要的",不是维基百科。
2. **别复制 LCM 摘要** — LCM 摘要已经压缩过了,直接复制 = 二次损失。**如果值得收,就 LLM 重新写**。
3. **别忘记 4.0 申请** — 写新 wiki 文件必须先列候选清单征得用户同意。**本规则来自 `ai-harness-exploration` v6.15.0 § 4.0**。
4. **别用"Expand for details about" marker** — 这是 LCM 摘要的 marker,不是 wiki 风格。Obsidian 渲染会显示乱码。
5. **别用 `\u2014` 等 unicode escape** — 写文件时 Python 会转义,但 markdown 渲染可能保留字面字符串。**用真字符 em dash (—)**。

## 8. 与多 Agent 协调

- **写新 wiki 文件前** → § 4.0 申请(主对话必做,3rd 同样)。
- **修改现有文件前** → 看 git log 是否别人刚改(避免覆盖)。
- **commit 前** → `git fetch origin main` 看是否有 3rd 提交。
- **push 前** → `git pull --rebase` 然后 `git push`(**永远不 force-push**,协议 v1.1 § 2.2)。
- **冲突时** → 用本文件 § 5.3 模板。
- **完结后写 log** → `indexes/log.md` 追加 1 段(日期 + 事件 + commit hash)。

## 9. 度量

wiki 健康度 5 指标(每周 cron 跑一次):

| 指标 | 阈值 | 工具 |
|---|---|---|
| 死链数 | <5 | `check-wiki-quality.py` |
| 缺 frontmatter 数 | <10 | 同上 |
| 缺索引数 | <5 | 同上 |
| wikilink 平均度 | >2.5 | 自写脚本:`grep -o '\[\[' *.md | wc -l` / 文件数 |
| 30 天内新建页面数 | 3-10 | `git log --since=30days --diff-filter=A` |

## 10. 推荐阅读

- David Allen,《Getting Things Done》(2002)— 5 步流程(收/处/组/回/行)
- Sönke Ahrens,《How to Take Smart Notes》(2017)— Zettelkasten 现代版
- Tiago Forte,《Building a Second Brain》(2022)— PARA 方法
- 890+ public second-brain repos on GitHub(2025-2026)— 多种工具实践
- **本 wiki**:`methods/wiki-as-second-brain.md`(184 行,设计文档)

---

**相关 wiki 页面**:
- [[protocols/git-collaboration-multi-agent]] — 多人 push 协议
- [[methods/wiki-as-second-brain]] — 我们的设计依据
- [[methods/session-to-wiki-archiving]] — 会话内容怎么入库
- [[tasks/daily-knowledge-curation]] — 每日新知识推送流程
