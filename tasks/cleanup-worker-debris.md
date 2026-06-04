---
id: cleanup-worker-debris
created: 2026-06-04
updated: 2026-06-04
status: pending
owner: agents/main-claude
assignees: [agents/main-claude]
depends_on: [tasks/wiki-multi-agent-refactor]
priority: medium
tags: [cleanup, post-refactor]
---

# cleanup-worker-debris

## 目标

清理 7 worker profile 删除后的残留:
- `AGENTS.md.bak-pre-flatten`(3.6KB) — 旧 AGENTS.md 备份
- `references/hermes-commands-full.md.bak-pre-flatten` — 平铺冲突备份
- Obsidian workspace.json 里的 .bak/.tmp 引用
- 2 个空 canvas
- 2 个未命名 canvas

## 范围

**包含**:
- 对比 .bak 文件和当前版本,确认无价值后删
- Obsidian workspace.json 自动清(下次打开 Obsidian 时)

**不包含**:
- 不动 hermes/ 任何文件
- 不动 git 仓库

## 验收标准

- [ ] 2 个 .bak 文件已删(对比后确认无差异)
- [ ] scratchpad 演示完成后归档

## 进度日志

- 2026-06-04 12:00 — created
