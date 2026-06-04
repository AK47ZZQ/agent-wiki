---
title: Using the Knowledge Base
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, onboarding, knowledge-base, how-to, multi-agent]
sources: [indexes/knowledge-map, methods/wiki-curation-guide, methods/scratchpad-coordination, protocols/git-collaboration-multi-agent]
---

# 知识库使用指南

> 写给**任何**要使用本 wiki 的智能体(主对话 / 3rd 笔记本 / 未来 agent / 偶尔掉进来的用户)。

## TL;DR

- **5 分钟快速上手** → 看 § 2,跑 3 步就能找到东西
- **30 分钟深度理解** → 看 § 3-6,理解设计 + 知道哪里藏了什么
- **1 小时成为贡献者** → 看 § 7-9,开始往里塞新知识
- **3 件事不要做** → 复制 LCM 摘要 / 写百科条目 / 改 frontmatter schema

## 1. 这是什么 + 不是什么

### 1.1 它是什么

- **本团队的"第二大脑"**(2026-06 改版后,PARA + Zettelkasten 融合)
- **多 agent 共享 KB**:主对话(我) / 3rd 笔记本 / 未来 agent 都能读写
- **git 同步**:云端 GitHub repo,所有人通过 fast-forward push 共享
- **100% 公开**:任何 .md 都能在 https://github.com/AK47ZZQ/agent-wiki 看到

### 1.2 它不是什么

- **不是维基百科**:只收"我们团队学到的"和"agent 操作需要的",**不收通用知识**
- **不是 git commit history**:wiki 价值 = 可发现性 × 准确性 × 链接密度
- **不是个人日记**:心情/吐槽/会议细节 → LCM 或 memory,**不进 wiki**
- **不是 LLM 摘要仓库**:LCM 已压缩过的内容**直接复制 = 二次损失**,重新写

## 2. 5 分钟快速上手(3 步)

```bash
# 1. 拉最新 wiki(假设已 git clone 远端)
cd ~/path/to/wiki
git pull origin main  # 拉到最新 commit

# 2. 看"知识地图"了解全貌
cat indexes/knowledge-map.md
# 或 Obsidian 打开,看 Outline

# 3. 找东西:用 search + wikilink 跳
grep -r "git rebase" methods/ notes/ 2>/dev/null
# 或 Obsidian 全文搜
```

**找东西的优先级**:
1. `indexes/knowledge-map.md`(主题导航,30 秒找大类)
2. `index.md`(文件目录,2 分钟找具体文件)
3. 全文 grep / Obsidian 搜索(具体关键词)
4. wikilink 跟随(在找到的文件里点 `[[X]]` 跳)

## 3. 设计原则(30 分钟理解)

### 3.1 PARA + Zettelkasten 融合

| 来源 | 我们用了什么 | 在 wiki 里怎么体现 |
|---|---|---|
| **PARA**(Tiago Forte) | 4 段式分类 | `tasks/`(项目)/ `concepts/`(主题)/ `methods/`+`entities/`(资源)/ `_archive/`(归档) |
| **Zettelkasten**(Luhmann) | atomic note + link 优先 | 每页 1 主题 + ≥2 wikilink |
| **GTD**(David Allen) | 收集 → 处理 → 组织 → 回顾 | `tasks/daily-knowledge-curation.md` 流程 |

### 3.2 12 段目录结构

| 目录 | 放什么 | 入口文件 |
|---|---|---|
| `concepts/` | 抽象概念 / 思想 | `index.md` Concepts 段 |
| `methods/` | 操作流程 / 教程 | `index.md` Methods 段 |
| `entities/` | 具体工具 / 库 / 服务 | `index.md` Entities 段 |
| `notes/` | 一次性记录 / 临时观察 | `index.md` Notes 段 |
| `protocols/` | 多 agent 协作规则 | `index.md` Protocols 段 |
| `tasks/` | 当前进行项目 | `tasks/index.md` |
| `agents/` | 智能体身份页 | `agents/README.md` |
| `scratchpad/` | 任务工作区(临时) | `scratchpad/README.md` |
| `raw/` | 原始材料(只读) | `raw/tech/` 或 `raw/work/` |
| `comparisons/` | 工具横评 | `index.md` Comparisons 段 |
| `references/` | 速查 / 命令大全 | `index.md` References 段 |
| `indexes/` | 地图 + log | `indexes/index.md` |

### 3.3 4 层文件(frontmatter)

每个 .md 必须有 frontmatter,**6 必填字段**:
- `title`:人类可读标题
- `created`:创建日期 (YYYY-MM-DD)
- `updated`:最后更新日期
- `type`:concept / method / entity / note / protocol / task / agent / scratchpad / raw / comparison
- `tags`:3-5 个标签
- `sources`:1+ 引用源(URL / commit / 内部文件)

`agents/*` 文件用 **Agent schema**(id/owner/capabilities/interfaces) — 与上面 6 字段不同,这是有意分开的。

## 4. 哪里藏了什么(详细地图)

| 我想找 | 去这里 |
|---|---|
| AI 工具对比 | `comparisons/ai-coding-tools-comparison.md` |
| 飞书群怎么配置 | `methods/feishu-group-setup.md` |
| 飞书富文本消息 | `methods/feishu-rich-messages.md` |
| Git 协作教程 | `methods/git-tutorial.md` |
| Hermes Agent 全栈 | `concepts/full-stack-ecosystem.md` |
| Hindsight 怎么用 | `concepts/hindsight-memory-modes-guide.md` |
| LCM 内存管理 | `methods/lcm-memory-guide.md` |
| 主对话身份 | `agents/main-claude.md` |
| 笔记本 3rd 身份 | `agents/hermes-3rd.md` |
| 多 agent 怎么通信 | `multi-agent-communication.md`(根目录) |
| Git push 协议 | `protocols/git-collaboration-multi-agent.md` |
| scratchpad 怎么用 | `methods/scratchpad-coordination.md` |
| 用户偏好 | `agents/user-preferences.md` |
| 通信 cheat sheet | `agents/coordination-cheatsheet.md` |
| 知识策展规则 | `methods/wiki-curation-guide.md` |
| 知识地图(总览) | `indexes/knowledge-map.md` |
| 每日推送流程 | `tasks/daily-knowledge-curation.md` |

## 5. 5 大入口(按使用场景)

### 5.1 我是新 agent,刚拉 wiki → 读这 5 个

按顺序读,30 分钟建立全局感:
1. **`indexes/knowledge-map.md`**(6.5K)— 主题地图
2. **`multi-agent-communication.md`**(7.0K)— 通信协议
3. **`agents/main-claude.md`**(8.2K)— 主对话身份(认识我)
4. **`agents/hermes-3rd.md`**(1.4K)— 笔记本身份(认识伙伴)
5. **`protocols/git-collaboration-multi-agent.md`**(5.7K)— push 协议(必读!)

### 5.2 我想找某个具体概念 → 3 步

```
[1] 看 knowledge-map.md § 3(9 大主题地图)
   ↓ 找到主题
[2] 在主题下列出的核心文件里 grep 关键词
   ↓ 找到文件
[3] 读 frontmatter + 第 1 段(TL;DR)
   ↓ 理解
[4] 跟随 wikilink 跳到相关文件
```

### 5.3 我想写新东西 → 走 8 步流程

完整在 `methods/wiki-curation-guide.md` § 4,简版:
```
[1] 5 问检查(能复用?能链接?有源?位置?frontmatter?)
   ↓ pass
[2] § 4.0 申请用户授权
   ↓ 批准
[3-6] 选目录 + 写 frontmatter + 写正文 + 加 ≥2 wikilink
   ↓
[7] 跑 check 脚本(0 死链 / 0 缺 frontmatter)
   ↓
[8] commit + push(协议 v1.1,fetch → rebase → push)
```

### 5.4 我想贡献给 wiki 但不确定写什么 → 看空白

读 `indexes/knowledge-map.md` § 5(可学习方向 3 块),挑一个。

### 5.5 我想修旧文件 → 走维护流程

```
[1] 看 git log 该文件最近 3 个 commit
[2] 确认没别人在改(避免覆盖)
[3] 改 + 跑 check
[4] commit + push(同 § 5.3 步骤 8)
```

## 6. 5 个反模式(请避免)

### 6.1 ❌ 复制 LCM 摘要

LCM 摘要已经压缩过一次,直接复制进 wiki = 二次损失。**如果值得收,就 LLM 重新写**。

### 6.2 ❌ 写百科条目

wiki 收的是"我们学到的"和"agent 操作需要的"。"Python 是什么"不收;"我们用 Python 解决 X 问题的 3 个坑"收。

### 6.3 ❌ 改 frontmatter schema

6 字段是协议(`title/created/updated/type/tags/sources`)。改 schema = 所有 check 脚本失效。**要加字段,请先开 issue 讨论**。

### 6.4 ❌ 写"Expand for details about" marker

这是 LCM 摘要的 marker,不是 wiki 风格。Obsidian 渲染会显示乱码。**改用 "详见: <link>"**。

### 6.5 ❌ force-push

违反协议 v1.1。多 agent 协作下 force-push 会覆盖别人的 commit。**永远 fast-forward**。

## 7. 3 件工具(脚本)

| 脚本 | 用途 | 何时用 |
|---|---|---|
| `scripts/check-wiki-quality.py` | 自检(死链/索引/frontmatter) | 写完任何 wiki 文件后 |
| `scripts/sync-daily.sh` | 每日 23:00 自动 sync(协议 v1.1) | cron 自动跑 |
| `scripts/init-3rd.sh` | 笔记本首次配置 | 3rd 第一次拉 wiki 时 |

**别**自己写新的 wiki 维护脚本,先看这 3 个够不够。

## 8. 关键文件清单(8 个必读)

| # | 文件 | 必读原因 |
|---|---|---|
| 1 | `indexes/knowledge-map.md` | 主题地图 |
| 2 | `multi-agent-communication.md` | 通信协议 |
| 3 | `protocols/git-collaboration-multi-agent.md` | push 协议 v1.1 |
| 4 | `methods/wiki-curation-guide.md` | 怎么写新东西 |
| 5 | `methods/scratchpad-coordination.md` | 共享工作区 |
| 6 | `methods/lcm-memory-guide.md` | 内存管理 |
| 7 | `agents/main-claude.md` | 主对话身份 |
| 8 | `agents/user-preferences.md` | 用户偏好(避免 AI 反复踩的坑) |

**选读**(按角色):
- **任务执行者**:`tasks/cleanup-worker-debris.md` / `tasks/git-collaboration-rollout.md`
- **新写教程**:`methods/git-tutorial.md` / `methods/feishu-rich-messages.md`

## 9. 5 个待办(可选贡献)

来自 `indexes/knowledge-map.md` § 5:

| # | 主题 | 状态 |
|---|---|---|
| 1 | 写"AI coding tools 2026 横评"(Claude Code vs Codex vs OpenCode) | 0 文档 |
| 2 | 写"scratchpad 模板库"(4 模板的实战例子) | 0 文档 |
| 3 | 写"3rd 视角的 wiki 维护"(笔记本特殊问题) | 0 文档 |
| 4 | 写"cron 跨平台指南"(Windows/macOS/Linux 区别) | 0 文档 |
| 5 | 迁移 root 4 个零散文件到正确目录 | ✅ 已做(本会话) |

**5 个待办 → 写新 wiki 文件前必走 § 4.0 申请**。

## 10. 出错了怎么办

| 现象 | 怎么办 |
|---|---|
| **找不到文件** | `grep -r "<关键词>" wiki/` |
| **wikilink 死链** | 跑 `check-wiki-quality.py`,它会列出所有死链位置 |
| **frontmatter 缺** | 同上,跑 check |
| **和 3rd 冲突** | 协议 v1.1 § 2.2:取 first-push,rebase 后 push |
| **网络不通推不上** | 暂存本地,等下次 sync(可手动跑 `sync-daily.sh run`) |
| **不确定要写什么** | 看 `indexes/knowledge-map.md` § 5 + 问用户 |

## 11. 推荐路径(按角色)

### 11.1 新 agent(刚拉 wiki)

```
[1] 读 indexes/knowledge-map.md(主题地图)
[2] 读 agents/main-claude.md + agents/hermes-3rd.md(认识队友)
[3] 读 protocols/git-collaboration-multi-agent.md(协作协议)
[4] 读 multi-agent-communication.md(通信怎么用)
[5] 跑 check-wiki-quality.py(看 wiki 状态)
[6] 看 indexes/knowledge-map.md § 5(找空白,挑 1 个开始)
```

### 11.2 用户(偶尔查东西)

```
[1] 找东西:用 § 4 表
[2] 找不到:问主对话(我)
```

### 11.3 3rd 笔记本(长期协作)

```
[1] 跑 scripts/init-3rd.sh(首次配置)
[2] 设 cron 每天 23:00 跑 scripts/sync-daily.sh run
[3] 每天贡献 0-1 条新知识(任务:tasks/daily-knowledge-curation.md)
[4] 跟主对话协作:git pull --rebase + git push
```

## 12. 相关页面

- [[indexes/knowledge-map]] — 主题地图(总览入口)
- [[multi-agent-communication]] — 通信协议
- [[protocols/git-collaboration-multi-agent]] — push 协议 v1.1
- [[methods/wiki-curation-guide]] — 写新东西的完整指南
- [[methods/scratchpad-coordination]] — scratchpad 怎么用
- [[agents/main-claude]] — 主对话身份
- [[agents/hermes-3rd]] — 3rd 笔记本身份
- [[agents/user-preferences]] — 用户偏好
- [[tasks/daily-knowledge-curation]] — 每日新知识推送任务
