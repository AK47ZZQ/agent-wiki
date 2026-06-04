# Writing Your Own gh Extension

gh extensions are just Go binaries named `gh-<name>`. Auth, HTTP, and repo context come from `go-gh`.

## Step 0: Do I Really Need an Extension?

| Trigger | Tool |
|---|---|
| 1 command, simple output | Shell script |
| 1 command, API call, parse JSON | Python + `gh api` |
| 1 command, Cobra-style subcommands | **gh extension** |
| Tool for the team, easy install | **gh extension** |
| > 5 subcommands | Standalone Go CLI (overkill for extension) |

## Step 1: Init

```bash
mkdir gh-mytool && cd gh-mytool
go mod init github.com/<you>/gh-mytool
go get github.com/cli/go-gh/v2
go get github.com/spf13/cobra   # for subcommands
```

## Step 2: Minimal Working Extension (10 lines)

```go
// main.go
package main

import (
    "fmt"
    "github.com/cli/go-gh/v2/pkg/api"
    "github.com/cli/go-gh/v2/pkg/repository"
)

func main() {
    base, err := repository.Current()
    if err != nil { fmt.Println(err); return }
    client, err := api.DefaultRESTClient()
    if err != nil { fmt.Println(err); return }
    var resp struct{ Login string `json:"login"` }
    client.Get("user", &resp)
    fmt.Printf("hello, %s (repo: %s/%s)\n",
        resp.Login, base.RepoOwner(), base.Name())
}
```

```bash
go build -o gh-mytool
gh mytool   # Output: hello, octocat (repo: cli/cli)
```

## Step 3: With Cobra Subcommands

```go
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
            if err := client.Get(path, &prs); err != nil { return err }

            if jsonOut {
                return json.NewEncoder(os.Stdout).Encode(prs)
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

## Step 4: Publish

1. Create GitHub repo named `gh-mytool` (must start with `gh-`)
2. Push code
3. Create a release tag (e.g. `v0.1.0`)
4. Add topic `gh-extension` (so it appears in https://github.com/topics/gh-extension)

```bash
gh repo create gh-mytool --public --source=. --push
gh release create v0.1.0 --title "v0.1.0" --notes "initial"
```

Users install:

```bash
gh extension install <owner>/gh-mytool
gh mytool --help
```

## Local Development Loop

```bash
go build -o gh-mytool && gh mytool --help
# or
gh extension install .    # install from current dir
# edit code
go build -o gh-mytool     # rebuild
gh mytool                 # gh picks up the new binary
```

## go-gh API Cheat Sheet

```go
import (
    ghapi "github.com/cli/go-gh/v2/pkg/api"
    ghrepo "github.com/cli/go-gh/v2/pkg/repository"
    ghos "github.com/cli/go-gh/v2/pkg/iostreams"
    "github.com/cli/go-gh/v2/pkg/auth"
)

// Auth-aware HTTP client
client, _ := ghapi.DefaultRESTClient()
client, _ := ghapi.DefaultGraphQLClient()

// Current repo (from git remote)
base, _ := ghrepo.Current()
base.RepoOwner()  // "octocat"
base.Name()       // "hello-world"
base.IsEmpty()    // false

// Hostname detection
host, _ := ghauth.DefaultHost()
host.IsEnterprise()  // false

// IO streams (stdout/stderr that respect pager)
ios := ghos.System()
ios.ErrOut  // *os.File for stderr
ios.CanPrompt()  // interactive check
```

## Debugging

```bash
# Verbose output (HTTP trace)
GH_DEBUG=1 gh mytool

# Force a specific host (for multi-account)
GH_HOST=github.com-work gh mytool

# Test API access directly
gh api /user
```

## 6 Worthwhile Extensions (2026)

| Extension | Purpose | Install |
|---|---|---|
| `gh-dash` | TUI PR/issue dashboard | `gh extension install dlvhdr/gh-dash` |
| `gh-copilot` | Copilot integration | `gh extension install github/gh-copilot` |
| `gh-ai` | AI to generate extensions | `gh extension install gh-cli-for-education/gh-ai` |
| `gh-actions-cache` | Manage Actions caches | `gh extension install actions/gh-actions-cache` |
| `poi` | Clean local branches | `gh extension install kpbird/poi` |
| `bump` | Semantic version bump | `gh extension install valeriobelli/gh-bump` |

Full list: https://github.com/topics/gh-extension
