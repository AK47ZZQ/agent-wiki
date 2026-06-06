---
title: Agent Writing Standard — 知识库写入规约
created: 2026-06-05
updated: 2026-06-05
type: method
tags: [method, writing, standard, wiki, agent, curation, quality]
sources:
  - internal: 2026-06-04~05 实战中发现的 5 类写入反模式
  - [[CLAUDE]] § 2.1-2.5
  - [[methods/wiki-curation-guide]]
  - [[notes/lessons-learned-index]]
confidence: high
source: hermes-3rd-context-2026-06
---

# Agent Writing Standard — 知识库写入规约

> **写给**: 任何往本 wiki 写内容的 Agent（main-claude / hermes-3rd / future-agent）。
> **核心原则**: wiki 是知识的蒸馏产物，不是会话的副产物。

---

## TL;DR 3 条铁律

| # | 规则 | 违反后果 |
|:--|:-----|:---------|
| 1 | **只写"可被未来 Agent 复用"的知识** | 噪声 → 搜索污染 → 信任崩塌 |
| 2 | **每页必须有 wikilink ≥ 2** | 孤岛 → 图谱断裂 → 无法发现 |
| 3 | **绝不复制 session 日志到 wiki** | LCM 摘要泄漏 → 上下文污染 |

---

## 1. 判断矩阵：这该不该进 wiki？

| 内容类型 | 进 wiki？ | 去哪里 |
|:---------|:---------|:------|
| **可复用方法**（如 "5 步核验 git push"） | ✅ 必进 | `methods/` |
| **概念/框架**（如 "Harness Engineering"） | ✅ 必进 | `concepts/` |
| **踩坑教训**（如 "MSYS bash `{}` 被破坏"） | ✅ 必进 | `notes/lessons-learned-index.md` 或 `notes/` |
| **部署步骤**（如 "Hindsight v0.7.2 升级"） | ✅ 可进 | `notes/`（标注日期和版本） |
| **对比分析**（如 "Hindsight 5 modes"） | ✅ 可进 | `comparisons/` |
| **工具/实体档案**（如 "gh CLI"） | ✅ 可进 | `entities/` |
| **Agent 身份/能力** | ✅ 可进 | `agents/` |
| | | |
| **会话日志**（"我今天 14:30 做了什么"） | ❌ 不进 | LCM 或 memory |
| **Token 计数 / API 调用细节** | ❌ 不进 | LCM |
| **一次性诊断报告**（"AGENTS.md 某天 stale 了"） | ❌ 不进 | 问题修复后删除 |
| **系统健康快照**（"某天 Hermes 7 层都正常"） | ❌ 不进 | LCM / 飞书 |
| **临时的中间状态** | ❌ 不进 | `scratchpad/`（TTL 后清理） |
| **重复已有内容** | ❌ 不进 | 追加到已有页 |

### 1.1 嗅觉测试

写之前问自己：
> **3 个月后，另一个 Agent 启动时读到这页，会不会觉得有用？**

- ✅ "会，我现在就想要这个" → 写
- 🟡 "可能吧……" → 写进 `notes/` 并标 `confidence: low`
- ❌ "不会，这只是当时的情况" → 不写，用 LCM/memory

---

## 2. 禁止写入的内容（反模式清单）

### 反模式 #1: LCM 摘要泄漏

**症状**: wiki 页面中出现 "Expand for details about:"、LCM 压缩标记、`compressed_at:` 时间戳。

**为什么有害**: 其他 Agent 读到这些标记会困惑——这不是知识，是系统内部元数据。会污染 Agent 的上下文理解。

**正确做法**: 从 LCM 摘要中提取**知识**重写，不复制原文。

### 反模式 #2: Session 日志冒充知识

**症状**: 
```
今天 15:00 我开始排查 Hindsight 的问题。
先跑了 healthcheck，发现返回 500。
然后我查了 env var……
```

**为什么有害**: 这是故事，不是知识。其他 Agent 需要的是 "Hindsight healthcheck 返回 500 的原因和修复方法"，不是你的排查时间线。

**正确做法**: 提炼为 "现象→根因→修复→预防" 四段式。

### 反模式 #3: Token 计数 / API 细节进 wiki

**症状**: "本次调用消耗 2841 input / 676 output tokens"

**为什么有害**: 这些数据只在当时有意义，3 个月后毫无价值。污染搜索索引。

**正确做法**: token 数据留在 LCM/memory。wiki 只保留 "用哪个模型、为什么" 的决策理由。

### 反模式 #4: 带日期的"快照报告"

**症状**: `hermes-selfcheck-2026-06-04.md`、`agents-md-stale-detect-2026-06-04.md`

**为什么有害**: 快照过期后不再准确，保留会误导未来 Agent（看到 "AGENTS.md 有 9 项偏差" 以为现在还这样）。

**正确做法**: 
- 快照问题 → 修复 → 报告归档 / 删除
- 如果是**持续指标** → 写成方法论而非快照
- 如果是**一次性修复** → 在 `log.md` 记一行就够了

### 反模式 #5: 未消化的技能镜像

**症状**: `agents/ai-harness-exploration-SKILL.md` (132KB) — 完整 skill 源码直接放 agents/ 下。

**为什么有害**: 这不是知识——这是源码。Agent 启动时可能会被加载进上下文，浪费 token。

**正确做法**: skill 源码 → `hermes/skills/`；wiki 只保留对 skill 的**索引和解释**（几百字即可）。

---

## 3. 质量自检清单（每次写入前）

```
[ ] 3 个月后另一个 Agent 会觉得有用？
[ ] 是"可复用知识"而非"一次性报告"？
[ ] 不是 session 日志或排查时间线？
[ ] 不含 LCM 压缩标记或 token 计数？
[ ] 不含 unicode escape (\u2014, \u00a0)？
[ ] frontmatter 9 字段齐全？（title/created/updated/type/tags/sources/confidence）
[ ] 至少 2 条 wikilink 出链？
[ ] 文件名小写连字符？（不是 2026-06-04-xxx.md 除非在 notes/）
[ ] 位置正确？（concepts/methods/notes/entities/comparisons）
[ ] 更新了 index.md + log.md？
```

---

## 4. 文件命名规范

| 目录 | 命名格式 | 示例 |
|:-----|:---------|:-----|
| `concepts/` | `{概念名}.md`（小写连字符） | `harness-engineering.md` |
| `methods/` | `{动作}-{对象}.md` | `safe-commit-push-protocol.md` |
| `notes/` | `{主题}-{日期}.md` | `hindsight-daemon-fix-2026-06-04.md` |
| `entities/` | `{实体原名}.md` | `codex.md` |
| `comparisons/` | `{主题}-comparison-{年}.md` | `hindsight-5-modes-2026.md` |
| `protocols/` | `{涉及方}-{主题}.md` | `git-collaboration-multi-agent.md` |
| `agents/` | `{agent-名}.md` 或 `README.md` | `main-claude.md` |

**禁止**:
- ❌ 中文文件名（`学习笔记.md`）
- ❌ 空格或特殊字符
- ❌ 以日期开头的文件名（除 `notes/` 外）

---

## 5. 写什么 vs 不写什么 — 实例对照

### 场景: Hindsight daemon 挂了

| 不要写（session 日志） | 要写（可复用知识） |
|:----------------------|:------------------|
| "今天 14:25 daemon 挂了，我先跑了 healthcheck，发现 500。然后查了 log，发现是 env var 没配。花了 20 分钟修好。" | "**现象**: daemon 返回 500。**根因**: HINDSIGHT_API_KEY 未设。**修复**: `hermes.env` 加 `HINDSIGHT_API_KEY=xxx` + 重启 daemon。**预防**: 每次升级后跑 `check-hindsight-env.sh`。" |

### 场景: git push 假成功

| 不要写 | 要写 |
|:--------|:-----|
| "git push 报 Everything up-to-date 但我明明刚 commit 了。然后我 pull rebase 失败，commit 丢了。查 reflog 才找回来。" | "**假成功 #5**: `pull --rebase` 吞 commit。**诊断**: `git reflog -5`。**恢复**: `git reset --hard <hash>`。**预防**: 永远先 `git stash` 再 `pull --rebase`。" |

### 场景: 系统自检通过了

| 不要写 | 要写 |
|:--------|:-----|
| "2026-06-04 14:48 Hermes 7 层自检，全部通过。MEMORY.md 83% 满。daemon RSS 1.2GB。" | 不写页面。在 `log.md` 记一行。如果发现**新教训** → 写到 `lessons-learned-index.md`。如果不是 → 不留。 |

---

## 6. 清理协议（定期 + 触发式）

### 6.1 触发清理

Agent 发现以下情况时**立即清理**：

| 发现 | 动作 |
|:-----|:-----|
| LCM 压缩标记出现在 wiki 正文 | 重写该段，删除标记 |
| Unicode escape (`\u2014` 等) | 替换为正常字符 |
| 死链 | 修复目标或删除链接 |
| 重复页面 | 合并到质量更高的那页，另一页加 redirect wikilink |
| scratchpad TTL 过期 | 移入 `_archive/` |

### 6.2 定期清理

| 频率 | 动作 |
|:-----|:-----|
| **每次 session 结束** | 检查 scratchpad/ 是否有 ephemeral 文件 → 删除 |
| **每周** | `notes/` 中标记 `stale` 的页面 → 评估是否归档 |
| **log.md > 500 行** | rotate → `log-YYYY-MM.md`，重置 `log.md` 只保留最近 50 条 |
| **每月** | 全域死链扫描 + frontmatter 补全 + 重复检测 |

---

## 7. 与其他协议的优先级

本规约与以下协议互补：

| 协议 | 覆盖范围 |
|:-----|:---------|
| [[CLAUDE]] § 2 | 写入位置、frontmatter 格式、更新策略 |
| [[methods/wiki-curation-guide]] | 知识获取 5 问、策展流程、冲突解决 |
| [[AGENTS]] § 4 | 5 反模式（本规约是 5 反模式的详细操作版） |
| [[notes/lessons-learned-index]] | 教训的**存储位置**（本规约定义教训的**格式**） |

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：基于 2026-06-04~05 实战中识别的 5 类写入反模式 |

---

> **核心洞见**: wiki 不是 Agent 的记忆转储，而是 Agent 之间的**知识接口**。一页噪音不仅浪费读者的时间，更危险的是让读者对整本 wiki 失去信任——"上次读到的都是过程日志，这次还信吗？"
