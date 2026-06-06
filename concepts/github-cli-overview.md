---
title: GitHub CLI (gh) 概览
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [github, cli, tool, terminal, devtools]
sources:
  - https://github.com/cli/cli
  - https://www.augmentcode.com/open-source/cli/cli
  - https://cli.github.com/manual/
confidence: high
source: gh-cli-tooling-2026
---

# GitHub CLI (gh) 概览

## 一句话定义

`gh` 是 GitHub 官方出品的 **standalone** 命令行工具,把 Pull Request / Issue / Release / Repo / Action 等 GitHub 概念带到终端,**不**是 `git` 的代理(对比 `hub`)。

## 核心价值

- ✅ 浏览器/终端切换成本消失 — **所有 GitHub 操作在 terminal**
- ✅ 脚本化 + JSON 输出 + `--jq` 过滤(可被 `delegate_task` worker 用)
- ✅ **extension API** — 任何 Go binary 命名为 `gh-xxx` 放 PATH = 子命令(140+ 社区 extension)
- ✅ 官方维护,GitHub API 升级即跟

## 关键设计: vs `hub`

| 维度 | `hub` (老) | `gh` (新) |
|---|---|---|
| 定位 | git 的 wrapper | **standalone** 工具 |
| 命令 | `hub` 前缀或 alias `git` | `gh` 自有命令空间 |
| 设计 | 透明代理 git | Cobra 命令树 + Factory DI |
| 安装 | `alias git=hub` | 独立 binary |
| 状态 | 弃用(2025) | **官方** |

## 命令集结构

```
gh <command> <subcommand> [flags]

issue    list / view / create / close / reopen / comment
pr       list / view / create / checkout / review / merge / close
repo     create / clone / fork / view / archive / sync
release  list / view / create / delete / download
workflow list / view / run / disable / enable
run      list / view / watch / rerun / cancel
search   issues / prs / repos / code / commits
auth     login / logout / status / refresh / token
extension list / install / remove / create / upgrade
api      <endpoint>   (REST + GraphQL)
config   get / set / list
gist     list / create / clone / delete
secret   list / set / delete
status   (本仓库 PR+issue 概览)
```

**所有 list/view 命令**都支持 `--json <fields>` + `--jq '.expr'` + `--limit N` → **脚本友好**。

## 何时用 gh,何时用 GitHub web

| 场景 | 工具 |
|---|---|
| 查 PR 列表 / status / 简单 review | `gh pr list --json` |
| 写 review 评论 / 行级 comment | `gh pr review --request-changes` |
| 创建 issue / PR | `gh issue create` / `gh pr create` |
| 看 issue/PR 完整页面 (含 diff) | GitHub web |
| 看 Actions log + retry | `gh run view` (看) / `gh run rerun` (重跑) |
| 看 multi-file diff / 大 PR | GitHub web |
| 自动化脚本 / cron / worker | `gh api` + `gh` 命令 + `--json` |
| **批处理 50+ PR/issues** | `gh api --paginate` |

## 学习曲线(从日常用户到 workflow 自动化)

```
L0: 安装 + auth login(1 分钟)
L1: 日常命令 pr/issue/repo(5 个命令,3 分钟)
L2: 脚本化 --json --jq --limit(8 个场景,30 分钟)
L3: gh api 直接调 REST/GraphQL(15 分钟)
L4: 写 gh extension(1-2 小时,Go)
```

**本机 L0 现状**:`gh` 未安装(`gh: command not found`)。建议先 L0-L2。

## 已知陷阱

1. **`--` 分隔符**:`gh search issues "is:open -label:bug"` shell 会把 `-label` 当 flag → 必须 `gh search issues -- "is:open -label:bug"`。**这是 gh 最常见的 footgun**。
2. **pager 配置**: `gh` 默认用 `$PAGER` 而不读 `git config core.pager`(issue #1733,未修)。设 `PAGER=cat` 或 `gh config set pager cat`。
3. **rate limit**: 未认证 60 req/h,认证 5000 req/h。`gh api` 触达超限。
4. **enterprise server**:`gh auth login --hostname` 必须显式指(hostname 不同 cookie 隔离)。
5. **JSON 字段大小写**:`gh pr list --json Number` 错,`--json number` 对。

## 关联

- [[github-cli-architecture]] — 仓库内部结构(Go/Cobra/Factory/api)
- [[gh-extension-development]] — 写自己的 extension
- [[gh-command-cheatsheet]] — L1-L2 速查
- [[tools-gh-cli]] — 本机安装+认证流程
- [[main-claude]] — Hermes 主对话 agent(常用 gh 做 PR/repo)
