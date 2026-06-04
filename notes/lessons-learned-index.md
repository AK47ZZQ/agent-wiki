---
title: 经验与教训索引 (Lessons Learned Index)
created: 2026-06-05
updated: 2026-06-05
type: index
tags: [index, lessons, retrospective, hermes, multi-agent, auto-summarize]
source: |
  2026-06-04 19:30-2026-06-05 00:55 main-claude 长期会话沉淀 + 3rd 端 Hindsight 笔记 + ai-harness-exploration v6.17 决策树 + v1.6 re-enable guard rails
confidence: high
---

# 经验与教训索引

> 跨 session 沉淀的踩坑、决策、流程改进。**这是索引页**,不重复细节;每条经验 1 个 wikilink 跳到细节源页。
> 目的:未来 agent (3rd / future) 启动时拉这一页,获得"前人踩过什么坑"全景。

## 1. 工具与平台坑(Windows + MSYS + Git)

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **MSYS bash curl POST JSON 不可靠** — `{}` `[]` 双引号被 MSYS argv rewriter 破坏,server 报 "error parsing body" | 修法: Python `urllib.request` + `json.dumps().encode()` | 2026-06-04 23:35 |
| **MSYS bash + `safe-commit-push.sh` CRLF 静默失败** — `set -euo pipefail` + 嵌套 `bash -c` 在 Windows MSYS 上有 CRLF 问题 | workaround: 用 `subprocess.run(['git', ...])` 跑 5 步核验 | 2026-06-04 19:30+ |
| **GitHub push protection blocks PAT redaction** — 本地已删 PAT,commit "Redact PATs" push 仍被 GH013 阻断 | 唯一解: 撤销 PAT → 等 5min → 再 commit/push | 2026-06-04 v1.9 |
| **Git 5 步核验** — `cat-file -t HEAD` + `fetch` + `rev-parse` 对比 + `git show --stat` + `git ls-remote` | 实战真成功: `805ae1a` (5 files), `aa0bcb0` (1148 lines) | 2026-06-04 19:30+ |

## 2. Hermes / LCM / Hindsight 架构坑

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **LCM `lcm_lifecycle_state` PK 是 `conversation_id`** — 不是 `session_id`,无 `last_compress_at` / `last_rotate_at` 字段 | 4 字段 (current_bound_at / last_finalized_at / last_maintenance_attempt_at) 全 NEVER = maintenance dead code | 2026-06-04 21:48 |
| **"current" 标签是骗人的** — `current_session_id` 字段被覆写覆盖,旧 row 不清,41 个 "current" 标签 90% 是死 session | 永远先 `PRAGMA table_info()` 再写 LCM audit query | 2026-06-04 21:48 |
| **12 个 orphan session 永远不被 LCM 跟踪** — 5372 条消息 (~21% 总盘) 5.4 天跨度,无 lifecycle row | 包含在 retention candidates | 2026-06-04 21:48 |
| **LCM 无 time-based archive** — 仅 message-count 触发压缩; `/lcm rotate apply` 手动 + active-session-only | 5 步核验的 24k-msg / 67MB 验证 | 2026-06-04 21:48 |
| **Hindsight `hermes memory status` 误报 "not available"** — 本地模式不需要 HINDSIGHT_API_KEY,status 工具不知道 env var | 4 步真验证法: `curl /health` + `list` + `retain/recall` | 2026-06-05 00:11 |
| **Hindsight daemon 死循环** — healthcheck 拉活但 daemon 持续 exit,需要 `lsof -i:8888` 查 PID | `pkill -9` + 重启 + 5min 间隔 | 2026-06-04 14:25-15:13 |
| **provider 切换不会 reset MemoryStore** — limit 改要重启进程 | 见 [[AGENTS]] § 0 协议 | 2026-06-04 |

## 3. Memory / Wiki 写作坑

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **`memory(action='add')` 是追加不是 replace** — 想整合必须 `remove` 旧条,或用 `replace` + `old_text` | `memory()` 工具跨次字符计数累加 | 2026-06-05 00:30 |
| **`execute_code` sandbox 写虚文件** — 不动真 MEMORY.md / USER.md | 真改写用 `terminal("python -c ...")` 或 `write_file` 工具 | 2026-06-05 00:30 |
| **Markdown `\u2014` / `\u00a0` unicode escape 污染** — 4 个文件 4 次踩坑,根因是 Python 脚本走非 f-string 路径 | 强制规则: 写完 1 个新 markdown 立刻 `grep -F '\u' file.md` | 2026-06-04 23:35+ |
| **LCM "**Expand for details about**:" 标记泄露** — LCM 摘要节点被 sibling agent 读到时,copy 到 wiki file 当作"wikilink style" | 4 个 wiki 文件污染,scrubbing 修了;Rule: 写 wiki 永不写这短语 | 2026-06-04 |
| **wiki-keeper v1.5 → v1.6 误 add `未命名.canvas`** — 3rd 反馈驱动,Obsidian 本地垃圾文件被误 commit | v1.6 加 `.canvas`/`.bak`/`.obsidian/*` 排除 | 2026-06-04 |
| **4 wikilink dead link 来自 `using-knowledge-base.md` 自引用** — line 7 `using-knowledge-base-draft` + 3 个 wikilink | 今天 ABC 修了 (5 stub + 3 rename + wikilink 修正) | 2026-06-04 |

## 4. 流程与协作坑

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **用户"0 自动化"原则演化** — 2026-06-04 0 cron → 2026-06-05 0 script-cron + agent-cron OK | `auto-apply mode` 取代 `staging file review` | 2026-06-05 00:50 |
| **cron `memory-maintenance` only-add bias** — 之前 teardown 原因:MEMORY 3500→5000 chars,1 周膨胀 43% | v1.6 re-enable 5 guard rails 防御 (staging→backup, delta report→apply direct, equal removals, no self-ref, token monitor) | 2026-06-04 evening teardown |
| **3rd 端冲突报告 BEGIN/END merge block** — 3rd 看到冲突用 BEGIN/END 标记友好处理,main-claude 整合时保留 | 跨 agent 协作最佳实践 | 2026-06-04 c030a77 / 42268e4 / 5bb84e2 / cb0c11e |
| **hermes-all 远端被删,skill 镜像到 agent-wiki** — 唯一 cross-agent 共享路径 | `skill mirror pattern` + 加 SKIP_PREFIXES + index.md 链 | 2026-06-04 |
| **3rd 端 "误判沉默" 是错的** — 3rd 一直活跃,本机 `git fetch` 超时让我以为没推 | 3rd 真实推 5+ commit / day | 2026-06-04 19:30+ |

## 5. 用户偏好与交互

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **§ 0c pushback 必给 lettered choice** — raise pushback 但不 silently 降级 | D1/D2/D3/D4 模式 1 round 解决 | 2026-06-05 00:47 |
| **"算了" = 真不再劝,不再二次 push** | 已被 USER.md § 5 沉淀 | 2026-06-04 22:30+ |
| **"ABCD" = 1 轮回 auto-decide + 报 commit hash 证据** | 已被 USER.md § 5 沉淀 | 2026-06-04 |
| **极简命令 + 3 步 verify 报告** | 单字母 "A"/"ABC"/"修 bug" + `git status/复验/ls-remote` | 持续 |
| **destructive-ops binary clarify** | "delete?/keep?" not 4-choice,4-choice 给真 trade-off | 2026-06-04 |
| **meta-methodology 问题必带 web 搜索** — "如何/为什么/更好/最佳" 触发 | 见 [[AGENTS]] § 4 5 反模式 | 2026-06-04 |
| **fs view > git status** — "自检/审视 folder" 不要 git diff | 默认 fs view,只有用户明示"git status"才展示 | 2026-06-04 |

## 6. wiki 第二大脑写作规约

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **5 问检查(开写之前)** — 能复用? 能链接? 有源? 位置对? frontmatter 齐? | AGENTS.md § 4.1 | 2026-06-04 |
| **§ 4.0 申请(本 skill)** — 写新内容必申请,维护不需 | 5 min 默认 = auto-execute | 持续 |
| **5 反模式** — 复制 LCM 摘要 / 写百科 / 改 frontmatter schema / 用 unicode escape / 跳 check | AGENTS.md § 4.3 | 2026-06-04 |
| **PARA + Zettelkasten 融合** — 5 知识类目 (concepts / methods / notes / entities / tasks) + wikilink | 见 [[AGENTS]] § 4.1 | 2026-06-04 |

## 7. Auto-Apply 模式(2026-06-05 新规)

| 经验 | 细节页 | 沉淀日期 |
|---|---|---|
| **v1.6 re-enable guard rails (auto-apply 适配版)** | 1) backup .bak.<ts> 2) 直接改 live (不用 memory() action) 3) adds ≤ removes 4) no self-ref 5) token monitor | 2026-06-05 00:50 |
| **staging file review 模式 → auto-apply 直改** | 用户硬偏好: "全自动整理,不需要过问我,我只看飞书最后的结果" | 2026-06-05 00:50 |
| **agent-cron 优先于 script-cron** | LLM 跑 = 产生 delta report;script 跑 = 仅 stdout | 2026-06-05 00:50 |

## 8. 2026-06-04 重大决策记录

| 决策 | 原因 | 日期 |
|---|---|---|
| **hermes user.name = "Hermes"** | 替代 wiki-keeper@hermes.local / main-claude / Hermes 3rd 三个 author | 2026-06-04 17:00 |
| **唯一远端 = agent-wiki** | 用户硬偏好 "我的仓库是 agent-wiki" | 2026-06-04 18:00 |
| **hermes-all 远端删,本地留 backup** | 用户硬偏好 "hermes all 仓库已经被我彻底删除了" | 2026-06-04 18:00 |
| **agent-wiki 公开(2026-06-04 22:15)** → **改回私有** → **保持公开** (3 次反复) | 3rd 端推 / 接受 PAT 泄露风险 | 2026-06-04 22:15-22:30 |
| **公开 wiki 中含 8 处已知敏感字符串** | log.md L248/L274 + README.md L18 + 5 散落,未 revoke | 2026-06-04 |
| **memory limit 激进扩: 24000→40000 / 5000→10000** | 用户硬偏好 "激进提高" | 2026-06-05 00:30 |
| **2 cron memory-maintenance 9:00 + 18:00 auto-apply** | 用户硬偏好 "全自动整理,只看飞书" | 2026-06-05 00:50 |

## 9. 未来踩坑预警

| 待办 | 优先级 | 何时处理 |
|---|---|---|
| **3rd 端推的 Hindsight 笔记索引** | 🟡 中 | 3rd 推过来后做 dead-link-check + wikilink |
| **`hermes-all` 本地 backup** 的 1c2ef6324 commit 历史保留 | 🟢 长期 | 永久 |
| **公开 wiki 8 处敏感字符串** | 🟡 中 | 改回私有 = 根除;但当前选择保持公开 |
| **cron 9:00 第一次跑观察** | 🔴 高 | 2026-06-05 09:00 跑后看飞书,确认 agent 是否越界用 memory() action |

## 10. 关联文档

- [[AGENTS]] — v2 工作环境规约
- [[methods/git-push-cheatsheet]] — 5 步核验详细
- [[methods/safe-commit-push-protocol]] — v1.6 协议详细
- [[methods/using-knowledge-base]] — wiki 入口
- [[concepts/agent-4-tier-memory-architecture]] — 4 层记忆设计
- [[concepts/github-cli-architecture]] — gh CLI 工具
- [[agents/skills-markitdown-converter/SKILL|markitdown 工具]]
- [[agents/skills-github-gh-cli/SKILL|gh CLI skill]]
- [[notes/auto-apply-mode-best-practices]] — auto-apply 详细

## 11. 元教训

> **Linus 原则**: 经验 = 让未来 agent 不再踩同一坑; 教训 = 知道坑有多大 + 多频。
> **不要重复 wiki**: 每条经验 wikilink 到原始细节页,本索引只列 "什么坑 → 跳去细节" 1 行表格,避免成为第二份 wiki 副本。
