# Hermes + Obsidian 知识图谱 Wiki

> 2026-06-04 flatten + 多 Agent 第二大脑升级版

基于 gusibi/obsidian-llm-wiki 架构 + Karpathy LLM Wiki 模式 + Tiago Forte CODE 工作流 + Hindsight 4 维检索 + Hermes 多 Agent 协议。

## 快速开始

1. 在 Obsidian 中打开 `C:\Users\Administrator\hermes-all\wiki` 作为 vault
2. Graph View 可视化知识网络
3. 运行 `wiki-keeper` skill 做定期维护(自检 / 同步 / 回滚)
4. 用 `ai-harness-exploration` skill 探勘新主题

## 仓库

- **本地**: `C:\Users\Administrator\hermes-all\wiki`
- **云端**: https://github.com/AK47ZZQ/agent-wiki (branch: main)
- **同步**: 通过 `_netrc` 鉴权(github_pat_11AWPGLQ0noDjr6RjMOS9_w8957XOakzX9CssiAE5koaqLxIDFofOfLMXOUexbxexZM3N57IDDSlQ9dfc)
- **维护**: `wiki-keeper` skill(`autonomous-ai-agents/wiki-keeper/`)

## 目录结构(2026-06-04 整理 + flatten 后)

```
wiki/
├── README.md                ← 本文件
├── AGENTS.md                ← Hermes 4-Tier 架构(精简版)
├── CLAUDE.md                ← Wiki Schema 规范(11.5K,root 11.5K 接近 8K 目标)
├── index.md                 ← 主索引(76+ 个有效页面)
├── log.md                   ← 操作日志(含历史)
│
├── concepts/                ← 概念/范式(主题页)
│   ├── full-stack-ecosystem.md
│   ├── hindsight-in-hermes-ecosystem-2026.md
│   ├── mcp-ecosystem-2026.md
│   ├── wiki-as-second-brain.md         (新, 12.6K)
│   └── ...
│
├── methods/                 ← 方法论(可执行流程)
│   ├── install-hindsight-native-hermes-method.md
│   ├── hindsight-4d-retrieval-complete.md
│   ├── wiki-code-workflow.md           (新, 10K) - CODE 4 阶段
│   ├── wiki-as-second-brain.md         (新, 12.6K)
│   └── ...
│
├── protocols/               ← 多 Agent 协议(新模块, 2026-06-04)
│   ├── agent-coordination.md          (新, 5.2K, 含 A2A 兼容)
│   ├── goal-alignment.md               (新, 5.5K)
│   ├── multi-agent-detail.md           (新, 5.5K)
│   ├── per-project-claude-md-template.md (新, 6.8K)
│   ├── scratchpad-protocol.md
│   └── ...
│
├── agents/                  ← Agent 实例档案(新模块, 2026-06-04)
│   ├── main-claude.md                  (orchestrator)
│   ├── researcher-1.md                 (worker 实例)
│   ├── writer-1.md                     (worker 实例)
│   └── ...
│
├── tasks/                   ← 任务档案
│   ├── 2026-06-04-agent-stack-test.md
│   ├── 2026-06-04-wiki-multi-agent-refactor.md
│   └── _archive/                       ← 已完成任务
│
├── scratchpad/              ← Agent 临时工作区(new)
│   ├── 2026-06-04-agent-stack-test/    ← namespace 隔离
│   ├── wiki-multi-agent-refactor/
│   └── _drafts/                        ← 拒绝的边界写入
│
├── raw/                     ← 源材料(只读, 探勘第一站)
│   ├── work/
│   └── <category>/
│
├── comparisons/             ← 2 个对比分析
│   ├── hermes-memory-systems-comparison-2026.md
│   └── ...
│
├── notes/                   ← 4+ 个部署/实战记录
│   ├── hindsight-local-deployment-windows-2026.md
│   └── ...
│
├── entities/                ← 14 个实体/技能/工具
├── references/              ← Hermes 命令大全提炼版
└── indexes/                 ← 主题子索引
```

## 关键计数(2026-06-04 flatten 后)

| 指标 | 数值 |
|---|---|
| .md 文件总数 | 89+ (持续增长) |
| 真死链 | 0 (从 222 修复) |
| protocols/ | 4 个(多 Agent 协议) |
| methods/ | 8 个(含 wiki 工作流) |
| concepts/ | 16+ 个 |
| agents/ | 7 个实例 |
| scratchpad namespace | 2 个 task 隔离 |
| wiki 总大小 | ~8 MB |
| frontmatter 覆盖 | 100% content 页 |

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

## 关键 Skill

- `wiki-keeper` — 维护 / 同步 / 回滚
- `ai-harness-exploration` — 探勘 + Wiki 集成模式
- `hermes-workflow` — P0-P4 AI 编码工作流
- `file-based-agent-coordination` — 多 Agent 文件协议
- `wiki-archive` — Session 自动归档到 wiki

## 写入协议(2026-06-04 新增)

**任何 wiki 写入 = 必须申请(按 ai-harness-exploration § 4.0)**:

1. 列出候选清单(文件/类型/大小/来源/是否用户要求)
2. 每个文件 1 段内容摘要
3. 标注"用户显式" vs "边界"
4. 询问"写哪些/全部/不写"
5. 用户决定后才执行
6. 拒绝内容 → `scratchpad/_drafts/`

**例外**: 用户显式说"写 X 到 wiki/Y...";任务必然副作用(任务页、scratchpad ns);自测试临时文件

## 维护脚本

`scripts/check-wiki-quality.sh` — 自检 5 项:
1. 死链(0 真)
2. 索引同步(76+ content / 58 已索引)
3. frontmatter 9 字段
4. log.md 24h 内更新
5. 总大小 < 10 MB

跑法: `bash scripts/check-wiki-quality.sh` 或 `python3 scripts/check-wiki-quality.py`

## 2026-06-04 整理要点(累计)

- ✅ 删除 14 个 worker profiles(7 段配置 + 7 段记忆)
- ✅ flatten wiki/wiki/* → wiki/*
- ✅ 修 222 真死链(从 222 降到 0)
- ✅ 加 4 个 protocols/(多 Agent)
- ✅ 加 2 个 methods/(wiki 工作流)
- ✅ 加 6 个 agents/ 实例
- ✅ scratchpad namespace 隔离
- ✅ git init + push 到云端 + rename master→main
- ✅ 加 README + check 脚本
- ⏳ 待办: cron 自动同步 / README badge / 拉取协作

详见 [[log|log.md]] 2026-06-04 记录。
