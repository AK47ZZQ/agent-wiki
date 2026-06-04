# gh Command Cheatsheet

> All list/view commands support `--json <fields>` + `--jq '<expr>'` + `--limit N`.
> Run `gh <command> --help` for full flag list on any subcommand.

## Setup

```bash
gh auth login                              # interactive
gh auth login --with-token < token.txt     # headless
gh auth status                             # show current
gh auth refresh --scopes repo,workflow     # add scopes
gh auth logout                             # clear
```

## PRs

```bash
# List
gh pr list --state open --json number,title,author,url --limit 50
gh pr list --search "review:required"
gh pr list --author @me --state all

# View
gh pr view 123
gh pr view 123 --json number,title,state,additions,deletions,changedFiles,url
gh pr view 123 --comments

# Local checkout
gh pr checkout 123
gh pr diff 123

# Create
gh pr create --base main --head feature --title "..." --body "..."
gh pr create --fill            # title/body from commit msgs
gh pr create --draft

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes -b "..."
gh pr review 123 --comment -b "..."

# Merge / close
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --rebase
gh pr merge 123 --auto --squash   # require CI
gh pr close 123
gh pr ready 123                  # draft → ready
gh pr edit 123 --title "..." --body "..."
```

## Issues

```bash
gh issue list --state open --label bug --assignee @me
gh issue list --search "is:open author:@me"
gh issue view 456
gh issue create --title "..." --body "..." --label bug
gh issue close 456 --reason "not planned"
gh issue reopen 456
gh issue comment 456 -b "..."
gh issue edit 456 --add-label "priority:high"
gh issue transfer 456 owner/other-repo
```

## Repos

```bash
gh repo clone owner/repo
gh repo create my-repo --public --source=. --push
gh repo fork owner/repo --clone
gh repo view owner/repo --json name,description,stargazerCount,url
gh repo sync            # fork → upstream
gh repo archive owner/repo
gh repo delete owner/repo
gh repo set-default owner/repo
gh repo rename new-name
```

## Releases

```bash
gh release list --limit 20
gh release view v1.0.0
gh release create v1.0.0 ./dist/*.tar.gz --title "v1.0.0" --notes "..."
gh release create v1.0.0 ./dist/*.tar.gz --generate-notes
gh release download v1.0.0 --pattern "*.tar.gz"
gh release delete v1.0.0
gh release upload v1.0.0 extra-file.zip
```

## Workflows / Actions

```bash
gh workflow list
gh workflow view ci.yml
gh workflow run ci.yml --ref feature-branch -f name=value
gh workflow enable ci.yml
gh workflow disable ci.yml

gh run list --limit 20
gh run list --workflow ci.yml --status failure
gh run view 12345
gh run view 12345 --log
gh run view 12345 --log-failed
gh run watch 12345 --exit-status
gh run rerun 12345
gh run rerun 12345 --failed
gh run cancel 12345
gh run download 12345
```

## Search

```bash
# ⭐ The -- separator is mandatory
gh search issues -- "is:open -label:wontfix label:bug"
gh search prs -- "is:open author:@me"
gh search repos -- "language:go stars:>1000"
gh search code -- "TODO repo:owner/myrepo"
gh search commits -- "fix typo"
```

## API

```bash
# REST
gh api /user
gh api /repos/owner/repo --jq '.stargazers_count'
gh api /repos/owner/repo/issues --paginate

# POST
gh api -X POST /repos/owner/repo/issues \
  -f title="bug" -f body="..." -f 'labels[]=bug'

# PATCH
gh api -X PATCH /repos/owner/repo \
  -f description="new desc" -f homepage="https://..."

# DELETE
gh api -X DELETE /repos/owner/repo/issues/123

# GraphQL
gh api graphql -F query='
  query {
    viewer { login }
    repository(owner:"AK47ZZQ", name:"agent-wiki") {
      stargazerCount
    }
  }
'

# Schema introspection
gh api graphql -F query='
  query { __schema { queryType { name } } }
'
```

## Secrets / Variables

```bash
gh secret set MY_SECRET --body "value"
gh secret set MY_SECRET < secret.txt
gh secret list
gh secret delete MY_SECRET

gh variable set MY_VAR --body "value"
gh variable list
gh variable delete MY_VAR
```

## Gist

```bash
gh gist list
gh gist create ./script.sh --public --desc "my script"
gh gist create ./script.sh --web                                   # open browser
gh gist view <id>
gh gist clone <id>
gh gist delete <id>
```

## Status / Misc

```bash
gh status                            # current repo PR + issue summary
gh config set pager cat              # disable pager (script-friendly)
gh config set editor "code -w"
gh config set git_protocol https
gh config list
gh alias set pv "pr view"            # custom alias
gh alias set iew "issue view --comments"

# Get current auth token (for sub-processes)
gh auth token | some-command

# Cache and config locations
gh config list --show-origin        # show where each setting lives
```

## Extensions

```bash
gh extension list
gh extension install owner/gh-<name>
gh extension install dlvhdr/gh-dash
gh extension install .               # from local dir
gh extension upgrade <name>
gh extension remove <name>
gh extension create <name>           # scaffold
gh browse                            # open current repo in browser
gh browse 123                        # open issue/PR 123
gh browse main:README.md             # open file at ref
```

## Global Flags

| Flag | Effect | Notes |
|---|---|---|
| `--repo owner/name` | Pin repo context | Use when not in git dir |
| `--json <fields>` | JSON output | Field names are **lowercase** |
| `--jq '<expr>'` | jq filter | Combine with `--json` |
| `--limit N` / `-L N` | Cap results | List commands |
| `--paginate` | All pages | `gh api` only |
| `--` | End of flags | **Required for `gh search`** |
| `--hostname <host>` | Multi-account | Or use `GH_HOST` env |
| `--template <tmpl>` | Go template | E.g. `gh pr list --template '{{range .}}#{{.number}} {{.title}}{{"\n"}}{{end}}'` |

## Field Names (Common)

| Resource | Field names (use in --json) |
|---|---|
| `pr list` | number, title, state, author, url, headRefName, baseRefName, isDraft, mergeable, reviewDecision, statusCheckRollup, additions, deletions, changedFiles, createdAt, updatedAt |
| `issue list` | number, title, state, author, url, labels, assignees, milestone, createdAt, updatedAt, closedAt |
| `repo view` | name, description, stargazerCount, watcherCount, forkCount, primaryLanguage, visibility, defaultBranch, url, isPrivate, isFork, isArchived |
| `run list` | databaseId, name, headBranch, headSha, status, conclusion, event, createdAt, updatedAt, url, workflowName |

Full field lists: `gh <cmd> --json help`.

## 5 Most Common Footguns

1. **Search missing `--`** → shell eats flag
2. **Pager blocks scripts** → `gh config set pager cat`
3. **JSON field case** → lowercase only
4. **Multi-account** → `GH_HOST`, not `GH_TOKEN`
5. **Rate limits** → 60/h unauth, 5000/h auth
