---
title: gh CLI 命令速查
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [github, cli, cheatsheet, reference]
sources:
  - https://cli.github.com/manual/
  - https://dev.to/github/top-10-tips-for-using-github-from-the-command-line-1me6
  - https://www.trainwithshubham.com/blog/github-cli-comprehensive-guide
confidence: high
source: gh-cli-tooling-2026
---

# gh CLI 命令速查

> **L1-L2 用法**。所有 list/view 命令支持 `--json` + `--jq` + `--limit`。

## 安装(本机 L0)

```bash
# Windows
winget install --id GitHub.cli
# 或 scoop
scoop install gh

# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

## 认证 (L0 必走)

```bash
gh auth login                     # 浏览器流程(推荐)
gh auth login --with-token < token.txt   # CI 用
gh auth status                    # 看当前
gh auth refresh --scopes repo,workflow    # 加 scope
```

## PR 工作流(L1 必会)

```bash
# 查
gh pr list --state open --json number,title,author,headRefName,url --limit 20
gh pr list --search "review:required" --json number,title
gh pr view 123 --json number,title,state,additions,deletions,changedFiles
gh pr view 123 --comments

# 本地 checkout
gh pr checkout 123
gh pr diff 123

# 创建 PR
gh pr create --base main --head feature --title "feat: X" --body "..."
gh pr create --fill          # 用 commit message 自动填 title/body
gh pr create --draft         # 草稿

# 维护
gh pr review 123 --approve
gh pr review 123 --request-changes -b "..."
gh pr review 123 --comment -b "LGTM"
gh pr merge 123 --squash --delete-branch
gh pr close 123
gh pr ready 123          # draft → ready
```

## Issue 工作流

```bash
gh issue list --state open --label bug --assignee @me
gh issue list --search "is:open author:@me"
gh issue view 456
gh issue create --title "bug: X" --body "..." --label bug
gh issue close 456 --reason "not planned"
gh issue reopen 456
gh issue comment 456 -b "我有同样的问题"
```

## Repo

```bash
gh repo clone owner/repo          # = git clone 但更省
gh repo create my-repo --public --source=. --push   # 本地 → 远程
gh repo fork owner/repo --clone   # fork + clone
gh repo view owner/repo --json name,description,stargazerCount
gh repo sync                      # fork 同步 upstream
gh repo archive owner/repo
```

## Release

```bash
gh release list --limit 20
gh release view v1.0.0
gh release create v1.0.0 ./dist/*.tar.gz --title "v1.0.0" --notes "..."
gh release download v1.0.0 --pattern "*.tar.gz"
gh release delete v1.0.0
```

## Actions / Workflows

```bash
gh workflow list
gh workflow view ci.yml
gh workflow run ci.yml --ref feature-branch
gh workflow enable ci.yml

gh run list --limit 20
gh run view 12345
gh run view 12345 --log
gh run watch 12345
gh run rerun 12345
gh run cancel 12345
```

## Search(陷阱高发区)

```bash
# ⭐ 一定用 -- 分隔符,否则 -label 被当 flag
gh search issues -- "is:open -label:wontfix label:bug"
gh search prs -- "is:open author:@me"
gh search repos -- "language:go stars:>1000"
gh search code -- "TODO repo:owner/myrepo"
gh search commits -- "fix typo"
```

## API(直接调 REST/GraphQL)

```bash
# REST
gh api /user
gh api /repos/owner/repo --jq '.stargazers_count'
gh api /repos/owner/repo/issues --paginate

# POST
gh api -X POST /repos/owner/repo/issues \
  -f title="bug" -f body="..." -f labels[]=bug

# GraphQL
gh api graphql -F query='
  query { 
    viewer { login }
    repository(owner:"AK47ZZQ", name:"agent-wiki") { 
      stargazerCount 
    }
  }
'
```

## Auth Token(给子进程用)

```bash
# 拿当前 token(不打印,只设 env)
export GITHUB_TOKEN=$(gh auth token)
export GH_TOKEN=$GITHUB_TOKEN

# 临时换 token(多账号)
GH_TOKEN=$(gh auth token --hostname github.com-myother) gh api /user
```

## Secret / Variable(L1.5)

```bash
gh secret set MY_SECRET --body "value"            # 写到 repo secrets
gh secret set MY_SECRET < secret.txt              # 从文件
gh secret list
gh secret delete MY_SECRET

gh variable set MY_VAR --body "value"             # 写到 repo variables
gh variable list
```

## Gist

```bash
gh gist list
gh gist create ./script.sh --public --desc "my script"
gh gist view <id>
gh gist clone <id>
```

## Status / Misc

```bash
gh status                  # 当前 repo 的 PR + issue 概览
gh config set pager cat    # 关掉 less(避免 pager 卡住脚本)
gh config list
gh alias set pv "pr view"  # 自定义 alias
```

## Extension

```bash
gh extension list
gh extension install owner/gh-mytool
gh extension install .                # 本地路径(开发用)
gh extension upgrade mytool
gh extension remove mytool
gh extension create mytool            # 脚手架
```

## 关键 flag(全局)

| Flag | 作用 | 注意 |
|---|---|---|
| `--repo owner/name` | 显式 repo(不在 git 目录时) | 多 repo 操作必加 |
| `--json <fields>` | JSON 输出 | 字段名小写严格 |
| `--jq '.expr'` | jq 过滤 | 配合 --json |
| `--limit N` | 限制行数 | list 类命令 |
| `--paginate` | 翻所有页 | API 命令 |
| `--` | 分隔符 | search 必加 |

## 5 个最常见 footgun

1. **search 缺 `--`**:`gh search issues "is:open -label:bug"` → shell 吃 flag。**必须** `gh search issues -- "is:open -label:bug"`
2. **pager 卡脚本**:`gh issue list` → 进 `less`。设 `gh config set pager cat`
3. **JSON 字段大小写**:`--json Number` 错,`--json number` 对
4. **多账号**:`GH_TOKEN` 跟 host 绑。`GH_HOST=other-host` + `gh auth token --hostname other-host`
5. **rate limit**:`gh api` 触达 → 等 1h 或换 token

## 关联

- [[github-cli-overview]] — 概览
- [[github-cli-architecture]] — 内部架构
- [[gh-extension-development]] — 写 extension
- [[tools-gh-cli]] — 本机部署
