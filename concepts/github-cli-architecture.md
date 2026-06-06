---
title: GitHub CLI 内部架构 (cli/cli)
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [github, cli, architecture, go, cobra, di]
sources:
  - https://github.com/cli/cli
  - https://www.augmentcode.com/open-source/cli/cli
  - https://github.com/cli/cli/tree/trunk/pkg/cmd
confidence: high
source: gh-cli-tooling-2026
---

# GitHub CLI 内部架构 (cli/cli)

## 一句话架构

**Cobra 命令树 + Factory DI 容器 + `internal/gh` API 客户端**,Go 1.22+,1 个 binary 200+ 子命令。

## 仓库目录结构

```
cli/cli/
├── cmd/gh/main.go              # 入口(只 6 行,调用 internal/ghcmd)
├── internal/
│   ├── ghcmd/cmd.go            # 主命令调度
│   ├── ghrepo/                 # repo 解析(从任意 URL 提 owner/name)
│   ├── ghinstance/             # hostname 检测
│   ├── browser/                # 浏览器打开
│   ├── config/                 # config file 读写
│   └── ...
├── pkg/
│   ├── cmdutil/factory.go      # ⭐ DI 容器(cmdutil.Factory)
│   ├── cmd/                    # ⭐ 所有命令实现(分层 cmd/<name>/<sub>/<sub>.go)
│   │   ├── pr/list/list.go
│   │   ├── pr/view/view.go
│   │   ├── issue/list/list.go
│   │   └── ... 200+ 子命令
│   ├── api/                    # ⭐ REST + GraphQL 客户端(query constructors)
│   ├── commands/               # 共享 command helpers
│   ├── extensions/             # ⭐ extension 加载器(go binary discovery)
│   ├── search/                 # gh search 客户端
│   └── ...
├── api/
│   ├── queries/                # GraphQL query strings + Go struct
│   ├── client.go
│   └── ...
├── go-gh/                      # ⭐ 独立可 import 的 library
│   ├── pkg/                    # (其他工具可以 import)
│   └── ...
└── docs/                       # 用户文档(.md → cli.github.com/manual)
```

## 3 个核心设计

### 1. cmdutil.Factory (DI 容器)

```go
// pkg/cmdutil/factory.go
type Factory struct {
    IOStreams          *iostreams.IOStreams
    HttpClient         func() (*http.Client, error)
    BaseRepo           func() (ghrepo.Interface, error)
    Executable         string  // gh binary 自身路径
    Browser            browser.Browser
    ExtensionManager   extensions.ExtensionManager
    Config             config.Config
    Prompter           iprompter
    // ...
}
```

**作用**:所有命令函数 `func newCmdList(f *cmdutil.Factory) *cobra.Command`,通过 `f` 拿到 IO/HTTP/Config/Extension,**不**自己 new。

**好处**:
- 测试容易(mock factory)
- extension 可复用同一套(f 通过 env 传递)
- 命令无全局状态(可并发)

### 2. Cobra 命令树(分层)

```
gh                      # 根 (cobra.Command)
gh pr                   # 1 级 (prCommand)
gh pr list              # 2 级 (listCommand)
gh pr list --state open # leaf
```

每个命令 1 个文件 = `pkg/cmd/<name>/<sub>/<sub>.go`:
```go
func NewCmdList(f *cmdutil.Factory, runF func(...) error) *cobra.Command { ... }
```

**约定**:`runF` 是 `func(...) error` 类型,可在测试中 mock;**所有 IO 经 `f.IOStreams`**,**所有 HTTP 经 `f.HttpClient`**。

### 3. go-gh 独立 library

`go-gh/` 子目录是 **可被其他 Go 项目 import** 的子集:
- `pkg/auth` — OAuth token 解析
- `pkg/repository` — git repo 元数据
- `pkg/instance` — hostname detection
- `pkg/api` — REST 客户端(可独立用)

**价值**:extension 作者 / 第三方工具可以 import 同一套 IO/Auth 逻辑,不用 fork gh。

## 命令实现模式(典型 list.go)

```go
type listOptions struct {
    BaseRepo   func() (ghrepo.Interface, error)
    IO         *iostreams.IOStreams
    HttpClient func() (*http.Client, error)

    State      string  // --state flag
    Limit      int     // --limit flag
    JSONFields []string // --json flag
}

func NewCmdList(f *cmdutil.Factory, runF func(*listOptions) error) *cobra.Command {
    opts := &listOptions{...}
    cmd := &cobra.Command{
        Use:   "list",
        Short: "List pull requests in a repository",
        Args:  cobra.NoArgs,
        RunE:  func(cmd *cobra.Command, args []string) error {
            if runF != nil { return runF(opts) }
            return listRun(opts)
        },
    }
    cmd.Flags().StringVarP(&opts.State, "state", "s", "open", "Filter by state")
    cmd.Flags().IntVarP(&opts.Limit, "limit", "L", 30, "Maximum number of items")
    cmdutil.AddJSONFlags(cmd, &opts.JSONFields, prFields)
    return cmd
}

func listRun(opts *listOptions) error {
    httpClient, err := opts.HttpClient()
    // ... fetch PRs via api
    // ... print via opts.IO or JSON
}
```

**关键点**:
- `runF` = test hook
- 所有 IO 走 `opts.IO`
- 所有 HTTP 走 `opts.HttpClient`
- `addJSONFlags` = 一致 `--json` + `--jq` 行为

## API 层(双协议: REST + GraphQL)

`pkg/api/` + `api/` 两个目录:

| 目录 | 协议 | 用途 |
|---|---|---|
| `api/queries/` | GraphQL | 复杂查询(PR detail, issue + comments + reviews) |
| `pkg/api/` | REST | 简单 CRUD(repo/issue/PR create) + extension API |

**GraphQL 优势**:
- 1 个 query 拿 5 个 entity + 关系(避免 REST 5 次 roundtrip)
- 强类型(query string + Go struct 配对)
- GitHub 推荐 2020+ 的新查询方式

**REST 用途**:
- 创建/更新/删除(POST/PUT/PATCH/DELETE)
- GitHub Actions 触发(`gh workflow run`)
- Raw API access(`gh api /repos/...`)

## Extension 加载机制(`pkg/extensions/`)

```
gh extension install owner/gh-<name>   # 走 gh-eco/gh-extension 协议
# 安装位置:
#   Linux:  ~/.local/share/gh/extensions/gh-<name>
#   macOS:  ~/Library/Application Support/gh/extensions/gh-<name>
#   Win:    %LOCALAPPDATA%\gh\extensions\gh-<name>
# 加载: gh <name> → PATH 查 gh-<name> binary → exec(...)
```

**关键设计**:
- extension 是**独立 Go binary**(`gh-foo`),**不**是 gh plugin
- 协议极简:放 PATH,叫 `gh-xxx`,**完事**
- 可用 `go-gh` library 拿到 auth/HTTP/repo
- GitHub 维护 `gh-extension` topic,140+ 公开 extension

## 关键 takeaway(给想写 gh extension 的人)

1. **不必懂 Cobra** — extension 是个独立 Go binary,自己管 CLI
2. **import `github.com/cli/go-gh/v2/pkg/api`** 拿认证 + HTTP client
3. **import `github.com/cli/go-gh/v2/pkg/repository`** 拿当前 repo 元数据
4. **命名规则**:`gh-<your-tool>`,release tag = version
5. **发布**:`gh extension install owner/gh-<your-tool>`

## 关联

- [[github-cli-overview]] — 概览 / 何时用
- [[gh-extension-development]] — 写 extension 实战
- [[gh-command-cheatsheet]] — 速查(看命令结构)
- [[tools-gh-cli]] — 本机安装

## 资料源

- cli/cli 仓库 trunk 目录结构(2026-06-04)
- augmentcode wiki(2025-2026,go-gh/cobra/Factory 描述)
- cli/cli docs/working-with-us.md
- go-gh repo: https://github.com/cli/go-gh
