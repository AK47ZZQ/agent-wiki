---
title: gh Extension 开发实战
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [github, cli, extension, go, development]
sources:
  - https://github.com/cli/go-gh
  - https://github.com/t-dedah/gh-cli-extension-demo
  - https://github.com/gh-cli-for-education/awesome-gh-cli-extensions
  - https://docs.github.com/en/github-cli/github-cli/creating-github-cli-extensions
confidence: high
---

# gh Extension 开发实战

## 一句话

**写 1 个 Go binary,命名为 `gh-<name>`,放 PATH,就完成 extension**。Auth/HTTP/Repo 元数据全从 `go-gh` library 拿。

## Step 0: 决策 — 真要写 extension 吗

| 触发 | 工具 |
|---|---|
| 1 个命令 + 简单输出 | **shell script**(gh 不需要) |
| 1 个命令 + API call + parse JSON | **Python + `gh api`**(更轻) |
| 1 个命令 + Cobra 风格子命令 | **gh extension**(值得 Go) |
| 1 个 subtool 给团队用 | **gh extension**(安装简单) |
| > 5 个 subcommand | **独立 Go CLI**(gh extension 太杂) |

**反模式**:用 Go 写 1 个 10 行 extension → 用 shell 写 `gh api /foo | jq` 就够了。

## Step 1: 准备环境

```bash
# 前提: gh 已装
gh --version   # ≥ 2.0.0

# 创建目录
mkdir gh-mytool && cd gh-mytool
go mod init github.com/<you>/gh-mytool

# 添加 go-gh 依赖
go get github.com/cli/go-gh/v2
```

## Step 2: 最小可运行 extension (10 行 Go)

```go
// main.go
package main

import (
    "fmt"
    "github.com/cli/go-gh/v2/pkg/api"
)

func main() {
    client, err := api.DefaultRESTClient()
    if err != nil { fmt.Println(err); return }

    resp := struct{ Login string `json:"login"` }{}
    err = client.Get("user", &resp)
    if err != nil { fmt.Println(err); return }

    fmt.Println("hello,", resp.Login)
}
```

```bash
go build -o gh-mytool

# 临时测试
gh mytool   # 输出: hello, <your-username>

# 安装(可选)
gh extension install .
# 或: gh extension install <owner>/gh-mytool
```

## Step 3: 进阶 — 加 Cobra 风格子命令

```go
// main.go
package main

import (
    "github.com/spf13/cobra"
)

func main() {
    rootCmd := &cobra.Command{
        Use:   "mytool",
        Short: "My gh extension",
    }
    rootCmd.AddCommand(newListCmd(), newShowCmd())
    rootCmd.Execute()
}

func newListCmd() *cobra.Command { ... }
func newShowCmd() *cobra.Command { ... }
```

**为什么用 Cobra**:子命令/flag/help 自动一致,跟 gh 主命令一样。

## Step 4: 拿当前 repo 信息

```go
import "github.com/cli/go-gh/v2/pkg/repository"

baseRepo, err := repository.Current()
fmt.Println("repo:", baseRepo.Name())          // e.g. "agent-wiki"
fmt.Println("owner:", baseRepo.RepoOwner())    // e.g. "AK47ZZQ"
```

## Step 5: 拿认证 client

```go
import "github.com/cli/go-gh/v2/pkg/api"

client, _ := api.DefaultRESTClient()
// 自动用 `gh auth token` 拿的 token
resp := struct{ Name string `json:"name"` }{}
client.Get("repos/{owner}/{repo}", &resp)
```

## Step 6: 拿 IO streams(避免 print 阻塞 pager)

```go
import "github.com/cli/go-gh/v2/pkg/iostreams"

// iostreams.System() 拿 system stdout/stderr
// iostreams.Test() 拿测试用 buffer
```

## Step 7: 发布到 GitHub

1. **Repo 命名** = `gh-<name>`(GitHub 协议要求,见 docs)
2. **README** 写明安装方法 + 截图
3. **Release** 至少 1 个 tag
4. **topic 标签**:`gh-extension`(让 awesome list 收录)

```bash
git init && git add . && git commit -m "init"
gh repo create gh-mytool --public --source=. --push
gh release create v0.1.0
# 用户安装:
# gh extension install <owner>/gh-mytool
```

## 完整样板(可复制)

```go
// go.mod
module github.com/<you>/gh-mytool
go 1.22
require (
    github.com/cli/go-gh/v2 v2.0.0
    github.com/spf13/cobra v1.8.0
)

// main.go
package main

import (
    "encoding/json"
    "fmt"
    "os"

    "github.com/cli/go-gh/v2/pkg/api"
    "github.com/cli/go-gh/v2/pkg/repository"
    "github.com/spf13/cobra"
)

type prItem struct {
    Number int    `json:"number"`
    Title  string `json:"title"`
    State  string `json:"state"`
    URL    string `json:"url"`
}

func main() {
    var state string
    var limit int
    var jsonOut bool

    rootCmd := &cobra.Command{
        Use:   "mytool",
        Short: "List PRs with extended info",
        RunE: func(cmd *cobra.Command, args []string) error {
            base, err := repository.Current()
            if err != nil { return err }

            client, err := api.DefaultRESTClient()
            if err != nil { return err }

            path := fmt.Sprintf("repos/%s/%s/pulls?state=%s&per_page=%d",
                base.RepoOwner(), base.Name(), state, limit)
            var prs []prItem
            err = client.Get(path, &prs)
            if err != nil { return err }

            if jsonOut {
                enc := json.NewEncoder(os.Stdout)
                enc.SetIndent("", "  ")
                return enc.Encode(prs)
            }
            for _, p := range prs {
                fmt.Printf("#%-4d %-9s %s\n", p.Number, p.State, p.Title)
            }
            return nil
        },
    }

    rootCmd.Flags().StringVarP(&state, "state", "s", "open", "PR state filter")
    rootCmd.Flags().IntVarP(&limit, "limit", "L", 30, "Max results")
    rootCmd.Flags().BoolVar(&jsonOut, "json", false, "Output JSON")

    if err := rootCmd.Execute(); err != nil { os.Exit(1) }
}
```

## 调试技巧

```bash
# 1. 临时测试(不安装)
go build -o gh-mytool && gh mytool --help

# 2. 看 gh 怎么调你
GH_DEBUG=1 gh mytool

# 3. 看认证状态
gh auth status

# 4. 用其他用户身份(测试)
GH_HOST=github.com gh mytool  # 默认
# 多账号:
GH_HOST=my-other-account gh mytool
```

## 经典踩坑

1. **Cobra import 重复** — 多个 `cobra.Command` 共享 root,但每个 `newCmdXxx` 自己 `&cobra.Command{}` 别复用指针
2. **错误吞掉** — `if err != nil { return err }` 优于 `panic`
3. **--json 字段大小写** — `cobra.Command` 解析严格小写,大写字段名无法 unmarshal
4. **多账号** — 用 `GH_HOST=<hostname>` env 切,不是 `GH_TOKEN`(token 跟 host 绑)
5. **binary 大小** — `go build` 静态链接 = 8-12MB,可加 `-ldflags="-s -w"` 缩 30%

## 6 个值得装的 extension(2026 活跃)

| Extension | 用途 | 装 |
|---|---|---|
| `gh-dash` | TUI PR/issue 看板 | `gh extension install dlvhdr/gh-dash` |
| `gh-copilot` | Copilot 集成 | `gh extension install github/gh-copilot` |
| `gh-ai` | AI 写 extension | `gh extension install gh-cli-for-education/gh-ai` |
| `gh-actions-cache` | Actions 缓存管理 | `gh extension install actions/gh-actions-cache` |
| `poi` | 干净删本地分支 | `gh extension install kpbird/poi` |
| `bump` | semver 自动化 | `gh extension install valeriobelli/gh-bump` |

## 关联

- [[github-cli-overview]] — 何时用 gh
- [[github-cli-architecture]] — 内部 Factory / go-gh / Cobra
- [[gh-command-cheatsheet]] — 用 gh 命令
