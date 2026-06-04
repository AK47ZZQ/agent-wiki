---
title: CODE Workflow — 4 阶段知识流(Capture / Organize / Distill / Express)
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [code, workflow, knowledge-management, second-brain, tiago-forte]
source: buildingasecondbrain.com
confidence: high
---

# CODE Workflow — 4 阶段知识流

> **问题**:我的 wiki 缺 2 阶段 — 只覆盖 Capture + Organize,**没有 Distill 和 Express**。
> **Tiago Forte 的 CODE**(Building a Second Brain):
> - **C**apture — 捕获(随时存)
> - **O**rganize — 组织(按可操作性)
> - **D**istill — 提炼(从原始到精炼)
> - **E**xpress — 表达(输出为作品)
> **本工作流** 把 CODE 4 阶段映射到 wiki + 工具 + agent 协作。

## 1. 4 阶段全景

```
Raw 信息              半成品                 精炼笔记              最终输出
   │                   │                     │                     │
   ▼                   ▼                     ▼                     ▼
CAPTURE          →  ORGANIZE            →  DISTILL           →  EXPRESS
"看到了什么"        "放在哪里"             "怎么用"              "怎么输出"
                                                           
飞书消息          raw/<category>/         concepts/             methods/
clipping          feishu-<date>-X.md       X-2026.md            X-guide.md
mcp 抓取           + frontmatter           1-page overview       可执行步骤
session 摘要        (TTL/lock)             wikilink × 5+         任务板任务
```

## 2. 阶段 1:Capture(捕获)

### 触发

任何有保存价值的信息出现时:
- 用户在飞书说"记一下 X" / "记到 wiki"
- Agent 跑出来的新概念/方法/实体
- 外部文章/视频/对话值得消化
- session 结束时的关键洞察

### 行动

写到 `raw/<category>/<source>-<date>-<id>.md`,**不动 wiki 主结构**。

```markdown
---
source_url: https://...
ingested: 2026-06-04
sha256: <hex>
---
# <source 标题>

<原文/摘要,允许大段粘贴>
```

### Agent 行为

- 不必深度分析,先存
- **不必查重** — Capture 阶段允许重复
- **不写 wikilink** — 留在 raw/ 阶段
- TTL 无限,直到显式提炼或删除

### 常见错误

- ❌ 捕获时就想"放哪个概念下" → 阻塞 Capture 流
- ❌ 追求完美 frontmatter → 浪费 Capture 时间
- ❌ 跳过 Capture 直接进 wiki → 原始信息丢失

## 3. 阶段 2:Organize(组织)

### 触发

- 用户说"整理一下" / "归档"
- 每周/每月 cron 触发
- raw/ 累计 > 50 个文件
- 新的 task 需要相关 raw 资料

### 行动

把 raw/ 中的多个源聚合成 wiki 概念/方法/实体页:

```
raw/tech/ai-2026-04-01.md       ┐
raw/tech/ai-2026-05-15.md       ├──→ concepts/ai-memory-2026.md
raw/work/ai-deployment.md       ┘    (聚合 3 源,1-page overview)
```

### 动作清单

1. 读 raw 中所有相关源(一次读 5-10 个)
2. 识别共同主题(greping 关键词)
3. 选合适的 wiki 子目录:
   - **concepts/** — 跨源综合的主题(抽象)
   - **entities/** — 单一工具/框架/模型(具体)
   - **methods/** — 可复用的步骤序列(操作)
   - **comparisons/** — 对比表
   - **notes/** — 短记录/部署日志
4. 写 frontmatter 9 字段(见 protocols/multi-agent-detail § 5.7)
5. 加 ≥ 2 条 wikilink 出链
6. 更新 `index.md` + `log.md`
7. raw 源保留(不删,作为引用)

### Agent 行为

- 可以用 `ai-harness-exploration` skill 探勘 raw
- 必须**先 grep 查重**(避免重复 page)
- 写完 → **自检清单 5 项**(见 multi-agent-detail § 5.4)

### 常见错误

- ❌ Capture 后直接跳到 Express(跳过 Distill)
- ❌ Organize 时只放 1 个源就建页(不达 2+ 来源门槛)
- ❌ 把 wikilink 写得像目录(不写正文)

## 4. 阶段 3:Distill(提炼)— **我之前缺的核心**

### 触发

- 一个 wiki 页内容 > 200 行 → 该拆
- 任务涉及"总结一下今天的发现"
- 多个 wiki 页交叉主题 → 提炼交叉方法页
- 3 源以上都讲同一现象 → 提炼交叉引用页

### 行动

把 wiki 主结构提炼为**可执行**的精炼产物:

| 输入 | 输出 | 例子 |
|---|---|---|
| 3 个概念页 + 5 个 raw 源 | 1 个 method 页 | "5 步法探勘新工具" |
| 1 个长概念页(>200 行) | 1 个 method + 1 个新概念 | 拆"AI 编码工具对比" 为 "ai-coding-tools-comparison" + "tool-X-deep-dive" |
| 多个 task 记录 | 1 个 method | "如何跑多步 wiki 重构" |
| 2 个 entities 互相冲突 | 1 个 comparison 页 | "8 provider 对比" |

### 提炼 4 步

```
Step 1: 找到共同抽象
  ├─ 3 个页都讲"agent 通信" → 主题 = "inter-agent communication"
  └─ 不止于把 3 页合并,而是找更上层的 pattern

Step 2: 找命名(用已有 taxonomy)
  ├─ type: method|concept|entity|comparison
  └─ tag: 从已有 taxonomy 选,禁止生造

Step 3: 写 1-page overview
  ├─ 不是详细,是可以讲清"这是什么"
  ├─ 含 ≥ 5 条 wikilink(到原材料)
  └─ 含 ≥ 1 条可执行步骤

Step 4: 标 confidence + sources
  ├─ confidence: high (3+ 源一致)
  ├─ sources: [A, B, C, ...]
  └─ contested: true (如果有矛盾源)
```

### Agent 行为

- 这是**最高价值**的阶段 — 一篇 method 页 = N 小时的探索提炼
- 必须**有源**(否则就是编)
- 多个 agent 协同(orchestrator 拆,worker 写)

### 常见错误

- ❌ 把概念页拆成 method 页(类型不对)
- ❌ 提炼时丢失原始引用(读者无法追溯)
- ❌ 提炼成"鸡汤"页(无可操作步骤)

## 5. 阶段 4:Express(表达)— **我之前缺的**

### 触发

- 完成任务后,用户问"总结一下"
- 任务可以复用为"模板"
- 想跟其他人/agent 分享经验
- 月度/季度回顾

### 行动

把 wiki 沉淀转化为**对外可消费的产物**:

| 输入 | 输出 | 例子 |
|---|---|---|
| 1 个 task 完成 | log.md 1 条目 | "## [2026-06-04] wiki 重构完成" |
| 多个 task 累计 | 1 个 methods/X-comparison-2026 | "8 wiki 改进对比" |
| 完整方法论 | 1 个 skill (SKILL.md) | "ai-harness-exploration" |
| 长期工作总结 | 1 个 export 文档 | "hindsight-agent-brief 5 篇" |
| 月度回顾 | 1 个 README/总结 | "monthly-review-2026-06" |

### 表达 4 步

```
Step 1: 选受众
  ├─ 自己看 → scratchpad/long/ 即可
  ├─ 其他 agent 看 → 写到对应 wiki 目录
  ├─ 用户看 → Feishu 回复 / 导出 .md
  └─ 公众看 → 导出为 .md / 公开 README

Step 2: 选载体
  ├─ log 条目:进度更新(50-200 字)
  ├─ wiki 页:知识沉淀(200-2000 字)
  ├─ skill:可执行方法(500-5000 字)
  └─ export:对外文档(任意长度)

Step 3: 加元数据
  ├─ 写 frontmatter 9 字段
  ├─ 标 confidence + sources
  └─ 标 contested/contradictions if applicable

Step 4: 索引 + 通知
  ├─ 更新 index.md
  ├─ 更新 log.md
  └─ 在 Feishu 提及相关 agent
```

### Agent 行为

- Express ≠ 把 wiki 内容复述一遍
- Express = **抽取最有价值的部分,重新组织为受众能用的形式**
- 写完必更新 index/log

### 常见错误

- ❌ Express 完不更新 index(用户找不到)
- ❌ 把所有内容都 export 给用户(信息过载)
- ❌ Express 跳过索引/日志(违背"写完必索引"硬规则)

## 6. CODE 与 4 阶段协议的关系

| 阶段 | 写到哪里 | 协议页 |
|---|---|---|
| **C**apture | `raw/<category>/` | [[CLAUDE]] § 2.5 反模式("先 Grep 查重")|
| **O**rganize | `concepts/entities/methods/...` | [[CLAUDE]] § 2.x 写协议 |
| **D**istill | `methods/ + comparisons/` | 本文件 § 4 |
| **E**xpress | `log.md` + `skills/` + exports/ | 本文件 § 5 |

## 7. 自检清单(每个阶段结束后)

```
CAPTURE 结束:
  [ ] 文件在 raw/<category>/ 下
  [ ] frontmatter 含 source_url + ingested + sha256
  [ ] 不动 wiki 主结构

ORGANIZE 结束:
  [ ] 在正确的 wiki 子目录
  [ ] frontmatter 9 字段齐
  [ ] ≥ 2 条 wikilink 出链
  [ ] index.md / log.md 更新
  [ ] raw 源保留(不删)

DISTILL 结束:
  [ ] 1-page overview 写完
  [ ] ≥ 5 条 wikilink(到原材料)
  [ ] ≥ 1 条可执行步骤
  [ ] confidence + sources 标注
  [ ] 3+ 源才标 high confidence

EXPRESS 结束:
  [ ] 受众明确
  [ ] 载体选对
  [ ] frontmatter 完整
  [ ] index/log 更新
  [ ] 通知到位
```

## 8. 当前 wiki 阶段分布(2026-06-04 盘点)

| 阶段 | 数量 | 例子 |
|---|---|---|
| **Capture** | 1 (raw/tech/) | 空目录,几乎没用 |
| **Organize** | 53 个 .md | concepts/entities/methods/... |
| **Distill** | 2 个 (wiki-as-second-brain, methods/...) | 提炼类较少 |
| **Express** | 1 个 (exports/hindsight-agent-brief/) | 公开文档少 |

**问题**:Distill 阶段(提炼)最弱,Express 几乎没做 → **下一步重点是 Distill + Express**。

## 9. 关联

- [[CLAUDE]] — root 协议
- [[protocols/multi-agent-detail]] — 5 层详细
- [[methods/wiki-as-second-brain]] — 元方法论
- [[protocols/goal-alignment]] — 主动警告机制
- [[log]] — Express 阶段的实际产物

## 10. 历史案例:2026-06-04 wiki 重构的 CODE 路径

实际跑了一遍完整 CODE:

| 阶段 | 动作 | 产物 |
|---|---|---|
| C | 收到用户 wiki 重构请求 | (无 Capture,直接进 Organize) |
| O | 建 4 个目录 + 5 个 README | agents/scratchpad/tasks/protocols |
| O | 写协议 + 注册 agent | protocols/agent-coordination, agents/main-claude 等 |
| **D** | (本步) 提炼 wiki-as-second-brain 方法论 | methods/wiki-as-second-brain.md |
| **D** | (本步) 提炼 multi-agent-detail 协议 | protocols/multi-agent-detail.md |
| D | (本步) 提炼 frontmatter schema | protocols/multi-agent-detail § 5.7 |
| D | (本步) 提炼 namespace 规范 | protocols/multi-agent-detail § 5.8 |
| E | (本步) 写 log.md 记录变更 | log.md +2030 字符 |
| E | (本步) 写本 CODE 工作流 | methods/wiki-code-workflow.md |

**关键洞察**:
- Capture 阶段我没做(用户没提供 raw 源,直接要求 Organize)
- Distill 阶段做了 4 个方法论(本工作流的精华)
- Express 阶段做了 2 个(log + 本文件)
- **完整跑一遍 CODE = 一次成功的"知识循环"**
