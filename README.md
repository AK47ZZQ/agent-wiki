# Hermes + Obsidian 知识图谱 Wiki

> 2026-06-04 flatten + 多 Agent 第二大脑升级版 + 公开仓库
> 维护状态:**5 项自检全过**(0 死链 / 106 索引 / 0 缺字段 / log 0.2h 前 / 0.59M)

基于 gusibi/obsidian-llm-wiki 架构 + Karpathy LLM Wiki 模式 + Tiago Forte CODE 工作流 + Hindsight 4 维检索 + Hermes 多 Agent 协议。

## 快速开始

1. 在 Obsidian 中打开 `C:\Users\Administrator\hermes-all\wiki` 作为 vault
2. Graph View 可视化知识网络
3. 运行 `wiki-keeper` skill 做定期维护(自检 / 同步 / 回滚)
4. 用 `ai-harness-exploration` skill 探勘新主题

## 仓库

- **本地**: `C:\Users\Administrator\hermes-all\wiki`
- **云端**: https://github.com/AK47ZZQ/agent-wiki (branch: main, 公开)
- **同步**: 通过 `_netrc` 鉴权(具体 PAT 不在仓库内)
- **维护**: `wiki-keeper` skill(`autonomous-ai-agents/wiki-keeper/`)

## 目录结构(2026-06-04)

```
wiki/
├── README.md                ← 本文件
├── AGENTS.md                ← Hermes Agent 工作环境与协作规约(v2, 8K)
├── CLAUDE.md                ← Wiki Schema 规范
├── index.md                 ← 主索引(106 个有效页面)
├── log.md                   ← 操作日志(含历史)
│
├── agents/                  ← Agent 实例档案
│   ├── main-claude.md
│   ├── hermes-3rd.md
│   └── ...
│
├── concepts/                ← 概念/范式(主题页)
│   ├── full-stack-ecosystem.md
│   ├── hindsight-in-hermes-ecosystem-2026.md
│   ├── mcp-ecosystem-2026.md
│   ├── wiki-as-second-brain.md
│   └── ...
│
├── methods/                 ← 方法论(可执行流程,20 个)
│   ├── install-hindsight-native-hermes-method.md
│   ├── hindsight-4d-retrieval-complete.md
│   ├── wiki-code-workflow.md
│   ├── wiki-as-second-brain.md
│   ├── safe-commit-push-protocol.md
│   ├── git-push-cheatsheet.md       ← 1 页速查(2026-06-04 新)
│   ├── git-tutorial.md
│   ├── feishu-rich-messages.md
│   ├── lcm-memory-guide.md
│   ├── scratchpad-coordination.md
│   └── ...
│
├── protocols/               ← 多 Agent 协议(5 个)
│   ├── agent-coordination.md
│   ├── git-collaboration-multi-agent.md
│   ├── goal-alignment.md
│   ├── multi-agent-detail.md
│   ├── per-project-claude-md-template.md
│   ├── scratchpad-protocol.md
│   └── ...
│
├── tasks/                   ← 任务档案
│   └── _archive/
│
├── scratchpad/              ← Agent 临时工作区
│   ├── 2026-06-04-agent-stack-test/
│   ├── wiki-multi-agent-refactor/
│   ├── 3rd-notebook-sync-test/
│   └── _drafts/             ← 拒绝的边界写入
│
├── raw/                     ← 源材料(只读, 探勘第一站)
│
├── comparisons/             ← 对比分析
│
├── notes/                   ← 部署/实战记录(9 个)
│
├── entities/                ← 实体/技能/工具(14 个)
│
├── references/              ← Hermes 命令大全
│
└── indexes/                 ← 主题子索引
```

## 关键计数(2026-06-04)

| 指标 | 数值 |
|---|---|
| .md 文件总数 | 121 |
| content 页(已索引) | 106 / 0 缺 |
| 真死链 | 0 |
| frontmatter 缺字段 | 0 |
| protocols/ | 5 个(多 Agent) |
| methods/ | 20 个 |
| concepts/ | 16+ 个 |
| agents/ | 4+ 实例 |
| notes/ | 9 个 |
| scratchpad namespace | 3+ task 隔离 |
| wiki 总大小 | ~11 MB(content 0.59 MB) |
| log.md 更新 | 0.2h 前 |

## 2026-06-04 大事记

| 时间 | 事件 |
|---|---|
| 09:00 | 自检启动,清 268 MB SQLite WAL |
| 10:00 | 删除 14 个 worker profiles,清理 7 段文件 |
| 11:00 | flatten wiki/wiki/* → wiki/*, 修 222 真死链 |
| 12:00 | 重构为多 Agent 第二大脑,加 6 原语 + 9 字段 schema |
| 13:00 | 加 4 个 P0/P1 改进(Progressive Disclosure / Schema / Namespace / A2A) |
| 14:00 | 实测 4 MCP 搜索通道 + 8 步 Wiki 集成模式 |
| 14:25 | E2E 多 Agent 协议栈测试(3 Agent / 6 原语 / lock / archive) |
| 14:30 | git init + push 到 AK47ZZQ/agent-wiki,rename master→main |
| 14:45 | 写 README + check 脚本 |
| 17:00 | git user.name 改为 "Hermes" |
| 18:00 | 用户删 AK47ZZQ/hermes 远端仓库(本机仍保留) |
| 18:30 | AGENTS.md v2(5 步核验协议) |
| 18:55 | safe-commit-push.sh v1.5 + 5 步核验协议发布 |
| 19:00 | v1.6(排除 .canvas/.bak/.obsidian 等) + ABC 修 4 死链 |
| 20:00 | Hindsight healthcheck cron 部署 |
| 20:30 | Hindsight wiki 更新(cron 验证证据) |
| 21:45 | git-push-cheatsheet.md 1 页速查 |
| 22:00 | 用户改 wiki 为公开仓库(116 处敏感字符串扫描发现) |
| 22:15 | 本 README 维护(更新计数 + 加公开安全提醒) |

## 关键 Skill

- `wiki-keeper` v1.8 — 维护 / 同步 / 回滚 / 25 个 pitfall
- `ai-harness-exploration` v6.x — 探勘 + Wiki 集成模式
- `hermes-workflow` — P0-P4 AI 编码工作流
- `file-based-agent-coordination` v1.1 — 多 Agent 文件协议
- `wiki-archive` — Session 自动归档到 wiki
- `hermes-self-check` — 本机健康度自检

## 5 步核验协议(必走)

**任何 wiki 写入**:永远走 `scripts/safe-commit-push.sh` v1.6,**不**裸 `git commit` + `git push`。
详细 1 页速查见 [[methods/git-push-cheatsheet]]。

## 写入协议(ai-harness-exploration § 4.0)

**任何 wiki 写入 = 必须申请**:

1. 列出候选清单(文件/类型/大小/来源/是否用户要求)
2. 每个文件 1 段内容摘要
3. 标注"用户显式" vs "边界"
4. 询问"写哪些/全部/不写"
5. 用户决定后才执行
6. 拒绝内容 → `scratchpad/_drafts/`

**例外**: 用户显式说"写 X 到 wiki/Y...";任务必然副作用(任务页、scratchpad ns);自测试临时文件

## 维护脚本

`scripts/check-wiki-quality.py` — Python 3 自检 5 项(2026-06-04 当前版本):
1. 死链(0 真)
2. 索引同步(106 content / 106 已索引)
3. frontmatter 9 字段(0 缺)
4. log.md 24h 内更新
5. 总大小(content < 10 MB)

跑法: `python scripts/check-wiki-quality.py` 或 `--strict` 模式(CI)

## 2026-06-04 整理要点(累计)

- ✅ 删除 14 个 worker profiles(7 段配置 + 7 段记忆)
- ✅ flatten wiki/wiki/* → wiki/*
- ✅ 修 222 真死链(从 222 降到 0)
- ✅ 加 5 个 protocols/(多 Agent)
- ✅ 加 20 个 methods/(含 git-push-cheatsheet)
- ✅ 加 4+ agents/ 实例
- ✅ scratchpad namespace 隔离
- ✅ git init + push 到云端 + rename master→main
- ✅ 加 README + check 脚本
- ✅ safe-commit-push.sh v1.5/v1.6 + 5 步核验协议
- ✅ wiki-keeper v1.6/v1.7/v1.8(25 个 pitfall)
- ✅ AGENTS.md v2(8K)
- ✅ Hindsight 部署 + healthcheck cron
- ⏳ 待办: cron 自动同步 / 公开仓库安全策略(用户决定)

详见 [[log|log.md]] 2026-06-04 记录。

## ⚠️ 公开仓库安全提醒

**本仓库 2026-06-04 22:00 改为 Public**。已知泄露内容(在 git 历史里):
- 🔴 2 个完整 82 字符 GitHub PAT(`ghp_11A6WPGLQ...`)
- 🟡 多个 4 字符 PAT 残片
- 🟡 26 处 Windows 路径(`C:\Users\Administrator\...`)
- 🟡 66 处 localhost 端口号

**强烈建议**:
- 如果想恢复私有: https://github.com/AK47ZZQ/agent-wiki/settings → Change repository visibility → Private
- 轮换当前 `_netrc` 里的 PAT: https://github.com/settings/tokens

## 关联文档

- [[AGENTS]] — Hermes Agent 工作环境与协作规约
- [[index]] — 主索引(106 个有效页面)
- [[log]] — 操作日志
- [[methods/git-push-cheatsheet]] — 5 步核验速查
- [[methods/safe-commit-push-protocol]] — 5 步核验详细
- [[protocols/git-collaboration-multi-agent]] — 多 Agent 协作
