---
title: Scratchpad 协调教程
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, scratchpad, multi-agent, coordination, file-based]
sources: [protocols/multi-agent-detail, methods/using-knowledge-base]
---

# Scratchpad 协调教程

> 多 Agent 共享工作区 — 文件级协议,读/写/锁/命名/生命周期。

## TL;DR

- **位置** = `wiki/scratchpad/<task-id>/`
- **生命周期** = announce → work → release
- **lock 机制** = 600s 超时
- **frontmatter 必填** 6 字段

## 目录结构

```
scratchpad/
  <task-id>/
    announce.md     # 任务发布
    <agent>.md      # 各 agent 工作区
    final.md        # 任务总结
    meta.json       # 元数据(状态/lock/时间)
```

## 5 命名规则

1. `<task-id>` 用 `kebab-case`(例:`2026-06-04-agent-stack-test`)
2. agent 文件用 agent 名(例:`main-claude.md`)
3. frontmatter 必填: title/created/updated/type/tags/sources
4. 不带中文路径(避免编码)
5. 文件不超过 50K(超了 archive 到 `tasks/_archive/`)

## 7 步生命周期

1. **announce** — 创建 `<task-id>/announce.md` 描述任务
2. **claim** — agent 写自己的 `<agent>.md` + `meta.json` lock=true
3. **work** — agent 改 scratchpad 文件(其他 agent 看到)
4. **update** — 改 `meta.json` status=in_progress
5. **hand-off** — 完成后改 status=done, lock=false
6. **release** — 删除 `<agent>.md` 或保留
7. **archive** — 任务完结后移到 `tasks/_archive/`

## 4 实战模板

### 模板 1: 临时分析(A 写,B 读)
```bash
mkdir scratchpad/analysis-2026-06-04
echo "..."
```

### 模板 2: 异步任务(A 委派,B 异步做)
A 写 announce.md,B 监听,B 写 done.md。

### 模板 3: 协调白板(多 agent 共享状态)
所有 agent 读 `state.md`,自己更新。

### 模板 4: 跨 session 上下文传递
完结后留 `handoff.md`,下次 session 读。

## 3 防坑

- ❌ 放敏感信息(可能被 push 到云端)
- ❌ 忘 frontmatter(协议不识别)
- ❌ Lock 用完不 release(60s 超时阻塞)

## 关联

- [[protocols/multi-agent-detail]] — 协议详细
- [[methods/using-knowledge-base]] — wiki 入口
