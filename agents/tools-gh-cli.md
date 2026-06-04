---
title: gh CLI 本机部署
created: 2026-06-04
updated: 2026-06-04
type: agent
tags: [github, cli, deploy, setup, hermes-main]
sources:
  - https://github.com/aaddrick/gh-cli-search/blob/main/skills/gh-cli-setup/SKILL.md
  - https://cli.github.com/manual/
sources_local: []
deploy_status: pending
confidence: high
---

# gh CLI 本机部署 (main-claude 节点)

> 本机状态: ❌ **未安装** (`gh: command not found`,2026-06-04 23:35 实测)

## 1. 安装 (本机 Windows 11)

```bash
# 方案 A: winget (推荐,已预装)
winget install --id GitHub.cli

# 方案 B: scoop (如已装 scoop)
scoop install gh

# 方案 C: MSI (如 winget 不通)
# https://cli.github.com/ 下载 GitHub CLI Windows MSI
```

**验证**:
```bash
gh --version
# 期望: gh version 2.x.x (2026-06-04 已发 v2.62.0+)
```

## 2. 认证

**方式 1: 浏览器流程(交互,推荐开发机)**
```bash
gh auth login
# 选 GitHub.com
# 选 HTTPS
# 选 Login with a web browser  ← 复制一次性 code → 浏览器授权
```

**方式 2: Token(本机已有 PAT,推荐)**

本机已有 `~/.netrc` 存 9dfc PAT(`machine github.com login ghp_...9dfc password x-oauth-basic`)。**有两种接法**:

```bash
# A) 让 gh 直接读 netrc (默认 config 就在那)
gh auth login --with-token < ~/.netrc   # 不行 — netrc 不是 token 文件
# 实际应该是:
gh auth login --with-token < <(grep "password" ~/.netrc | awk '{print $2}')

# B) 用 gh api 测认证(更直接)
export GITHUB_TOKEN=$(awk '/machine github.com/ {found=1} found && /password/ {print $2; exit}' ~/.netrc)
gh auth status   # 应显示: Logged in to github.com as <user>
```

**期望输出**:
```
github.com
  ✓ Logged in to github.com as AK47ZZQ (~/.config/gh/hosts.yml)
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: *******************
```

## 3. 验证(跑通 L1 命令)

```bash
# 查自己
gh api /user --jq '.login'
# 期望: "AK47ZZQ"

# 查一个 PR
gh pr list --repo AK47ZZQ/agent-wiki --state open --json number,title --limit 5

# 创建 issue 测试(用 dry-run / 不真发)
gh issue create --repo AK47ZZQ/agent-wiki --title "[test] gh setup verify" --body "ignore"
# 拿到 URL 后立即 close
gh issue close <N> --comment "test only"

# 看 actions
gh run list --repo AK47ZZQ/agent-wiki --limit 3
```

## 4. 配置优化

```bash
# 关掉 pager(避免卡脚本)
gh config set pager cat

# 默认 editor
gh config set editor "code -w"   # VS Code wait 模式

# 默认 protocol
gh config set git_protocol https

# 启用 beta features
gh config set experimental_extensions true   # 旧版本;v2.0+ 不需要
```

**配置文件位置** (Windows):
```
%AppData%\GitHub CLI\config.yml
%AppData%\GitHub CLI\hosts.yml    # 认证 token
```

## 5. 已知陷阱(本机特别)

1. **PATH 不全**:`winget install` 完后**关掉重开** terminal,否则 `gh` 找不到
2. **netrc vs gh hosts.yml**:这是**两个独立**认证源
   - `gh` 用 `%AppData%\GitHub CLI\hosts.yml`
   - `git` 用 `~/.netrc`(你的 _netrc 配置)
   - 改一个不影响另一个
3. **MSYS bash 路径转换**:Cygwin-style path 在 gh 输出里可能变形,建议用 `cmd` / PowerShell 跑 gh 验证
4. **PAT scope 不足**:9dfc 是 fine-grained,确认 `Contents: Read and write` 已勾
5. **proxy**:本机不需 proxy,但 **curl gh API** 调试时可能被 MSYS argv rewriter 破坏(已知)

## 6. 跟现有工具的关系

| 工具 | 用 gh 替代? | 何时用 gh |
|---|---|---|
| `curl https://api.github.com/...` | ✅ 替代 | `gh api` 帮你管 auth + rate limit + JSON |
| `git push ...` | ❌ | 推代码还是 `git`(gh 不管 git) |
| 浏览器开 GitHub | 部分 | 看 diff / 长 log / 复杂 review 仍用 web |
| `gh-pr-*` skill 名 | ❌ 误 | 我之前误以为装了 gh,实际**没装**,skill 名是巧合 |
| `terminal` 工具调 `gh` | ✅ | 跑 gh 命令的首选方式 |

## 7. 卸载(退出成本 0)

```bash
# winget
winget uninstall --id GitHub.cli

# scoop
scoop uninstall gh
```

**确认干净**:
```bash
where gh     # 应报 "INFO: Could not find files"
gh --version # 应报 "command not found"
```

**认证数据清空** (可选):
```bash
gh auth logout
# 或手动:
rm -rf "$APPDATA/GitHub CLI"     # Windows
```

## 8. 部署 checklist

```
[ ] gh --version 输出 v2.x
[ ] gh auth status 显示 Logged in
[ ] gh api /user --jq '.login' 返回 "AK47ZZQ"
[ ] gh pr list --repo AK47ZZQ/agent-wiki 能查
[ ] gh config set pager cat 已设
[ ] winget 升级源已启用(后续 gh 升级走 winget upgrade)
```

## 关联

- [[github-cli-overview]] — gh 是什么
- [[github-cli-architecture]] — 内部
- [[gh-command-cheatsheet]] — L1 命令
- [[main-claude]] — 本机节点身份
