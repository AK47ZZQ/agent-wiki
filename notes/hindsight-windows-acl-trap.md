---
title: Hindsight Windows ACL 陷阱 — daemon log access denied 排查
created: 2026-06-06
updated: 2026-06-06
type: note
tags: [hindsight, windows, acl, pitfall, 3rd-notebook]
source: hindsight-deployment-2026-06
---

# Hindsight Windows ACL 陷阱 — daemon log access denied 排查

> 3rd 笔记本实战 (2026-06-05 期间). 从 lessons-learned 引用反推.
> 症状: Hindsight daemon 跑着, 但 `/tmp/hindsight.log` 报 "Access Denied", 看不到启动事件

## TL;DR

- **触发**: Windows 下 daemon 用 Python `open(log_path, 'a')` 默认沿用父进程 token, 但 log 目录 ACL 限制写入
- **根因**: 父进程 (hermes gateway) 在 `Users\ZZQ` 下启动, daemon fork 后 token 降级或目录只允许 `Users` 组写
- **症状**: daemon log 一行不写, 看似 daemon 跑着实际只读 stdin/stdout
- **临时修法**: `icacls <log_dir> /grant Users:(OI)(CI)F` 显式 grant
- **长期修法**: 改用 `%LOCALAPPDATA%\hindsight\logs\` (默认 User 写权限)

## 1. 现象

- `tasklist | grep hindsight` → 进程存在, RSS 正常
- `curl :9177/health` → 200
- **但 `tail /c/Users/ZZQ/.hindsight/profiles/hermes.log` → 文件不存在 或 "Access Denied"**

## 2. 排查

1. 看 daemon 父进程 PID
2. `tasklist /v` 看 daemon 的 token user
3. `icacls <log_file>` 看 ACL
4. 多数情况: ACL 只有 SYSTEM + Administrators 写权限, daemon 进程是 Users 组成员 → 写失败

## 3. 修法 (3 选 1)

| 方案 | 命令 | 风险 |
|---|---|---|
| A. 显式 grant | `icacls C:\Users\ZZQ\.hindsight /grant Users:(OI)(CI)F /T` | 低 |
| B. 改 log 路径 | `set HINDSIGHT_LOG_DIR=%LOCALAPPDATA%\hindsight\logs` | 低 |
| C. 跑 daemon 提权 | 启动 bat 加 `runas /user:Administrator` | 中 |

## 4. 关联文档

- [[notes/hindsight-gbrain-source-code-learning-2026-06-05]] — 源仓库学实战
- [[notes/safe-commit-push-v17-deep-fix-2026-06-05]] — 同期 v1.7 实战
- [[notes/lessons-learned-index]] — 引用本笔记的索引页

## 5. 自检

- [x] 6 字段齐
- [x] 至少 2 wikilink 出链
- [x] tag: hindsight + windows + acl + pitfall + 3rd-notebook
- [x] source: hindsight-deployment-2026-06
