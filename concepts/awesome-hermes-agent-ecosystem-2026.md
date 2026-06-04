---
title: Awesome Hermes Agent 生态全景
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [tech, hermes, ecosystem, awesome-list, skills, plugins, agents]
source: raw/tech/awesome-hermes-agent-zh.md
confidence: high
contested: false
---

# Awesome Hermes Agent 生态全景

> 基于 [jefferyjob/awesome-hermes-agent-zh](https://github.com/jefferyjob/awesome-hermes-agent-zh) 精选清单的二次整理。源文件见 [[raw/tech/awesome-hermes-agent-zh]]。
> 原文翻译自 [0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)，持续同步。

## 总览

Awesome Hermes Agent 是 Hermes 生态系统的**社区精选清单**，涵盖 14 个类别、~65 个条目（截至 2026-04-03 审查）。Hermes Agent 版本 v0.6.0 (v2026.3.30)，核心仓库 23k+ stars。

### 成熟度标签体系

| 标签 | 含义 | 数量估算 |
|-----|------|---------|
| **production** | 稳定、文档完善、持续维护——可放心在生产环境构建 | ~12 |
| **beta** | 可用，但仍在持续演进——预计有粗糙边角 | ~35 |
| **experimental** | 概念验证或早期阶段——可借鉴学习，不建议依赖 | ~18 |

## 14 类别结构化索引

### 1. 官方资源（9 条目）

| 项目 | 作者 | 描述 | 成熟度 |
|------|------|------|--------|
| [hermes-agent](https://github.com/NousResearch/hermes-agent) (23k★) | Nous Research | 核心项目，自我改进 AI agent | production |
| [autonovel](https://github.com/NousResearch/autonovel) | Nous Research | 自主小说写作流水线 (100k+字) | — |
| [hermes-paperclip-adapter](https://github.com/NousResearch/hermes-paperclip-adapter) | Nous Research | Paperclip 公司托管员工适配器 | — |
| [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) | Nous Research | DSPy + GEPA 进化式自我改进 | — |
| [tinker-atropos](https://github.com/NousResearch/tinker-atropos) | Nous Research | Thinking Machines Tinker API + RL 训练 | — |
| [Skills Hub](https://agentskills.io) | — | agent 技能开放标准，跨平台兼容 | production |
| [Official Docs](https://hermes-agent.nousresearch.com/docs/) | Nous Research | 全面官方文档 | production |
| [Release Notes](https://github.com/NousResearch/hermes-agent/releases) | Nous Research | 版本更新日志 | production |
| [Discord](https://discord.gg/NousResearch) | Nous Research | 社区讨论 | — |

### 2. 社区技能（9 条目）

| 项目 | 作者 | 亮点 | 成熟度 |
|------|------|------|--------|
| [hermes-plugins](https://github.com/42-evey/hermes-plugins) | 42-evey | 目标管理、agent 间桥接、模型选择、成本控制 | beta |
| [hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory) | Romanescu11 | 自动从工作流生成可复用技能的**元技能** | beta |
| [litprog-skill](https://github.com/tlehman/litprog-skill) (75★) | tlehman | Claude Code/OpenCode/Hermes 文学化编程 | beta |
| [super-hermes](https://github.com/Cranot/super-hermes) | Cranot | 教 Hermes 为自己写更优提示词（元推理） | experimental |
| [hermes-life-os](https://github.com/Lethe044/hermes-life-os) | Lethe044 | 个人 OS agent，日常模式学习 | experimental |
| [hermes-incident-commander](https://github.com/Lethe044/hermes-incident-commander) | Lethe044 | 自主 SRE agent，故障检测+自愈 | beta |
| [hermes-dojo](https://github.com/Yonkoo11/hermes-dojo) | Yonkoo11 | 自我改进系统，性能监控+自动迭代 | beta |
| [hermes-skill-marketplace](https://github.com/Lethe044/hermes-skill-marketplace) | Lethe044 | 自主编写/测试/发布技能的 agent | experimental |
| [Wizards-of-the-Ghosts](https://github.com/Hmbown/Wizards-of-the-Ghosts) | Hmbown | RPG 风格重构/lint/测试工具包 | experimental |

### 3. agentskills.io 生态（12 条目）

基于 [agentskills.io](https://agentskills.io) 开放标准——可跨 Hermes、Claude Code、Cursor、Codex 使用。

| 项目 | 作者 | 亮点 | 成熟度 |
|------|------|------|--------|
| [wondelai/skills](https://github.com/wondelai/skills) (380★) | wondelai | **跨平台 agent 技能库**，社区最推荐的第一步 | production |
| [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) (4k★) | mukul975 | 753+ 网络安全技能，MITRE ATT&CK 映射 | production |
| [chainlink-agent-skills](https://github.com/smartcontractkit/chainlink-agent-skills) | Chainlink | 官方预言机/CCIP/智能合约技能 | production |
| [black-forest-labs/skills](https://github.com/black-forest-labs/skills) | Black Forest Labs | 官方 FLUX 图像生成技能 | production |
| [pydantic-ai-skills](https://github.com/DougTrajano/pydantic-ai-skills) | DougTrajano | Pydantic AI + agentskills.io schema 校验 | production |
| [cognify-skills](https://github.com/Yarmoluk/cognify-skills) | Yarmoluk | 19 个业务运营技能（CRM/开票/项目管理） | beta |
| [execplan-skill](https://github.com/tiann/execplan-skill) | tiann | 长任务生命周期管理（进度/检查点/恢复） | beta |
| [maestro](https://github.com/ReinaMacCredy/maestro) | ReinaMacCredy | Conductor+Beads 技能编排流水线 | beta |
| [bmad-module-skill-forge](https://github.com/armelhbobdad/bmad-module-skill-forge) | armelhbobdad | 仓库→agentskills.io 技能转换 | beta |
| [Agentic-MCP-Skill](https://github.com/cablate/Agentic-MCP-Skill) | cablate | MCP 客户端 + agentskills.io 校验 | beta |
| [skillsdotnet](https://github.com/PederHP/skillsdotnet) | PederHP | C# 实现，.NET 替代方案 | beta |

### 4. 插件（8 条目）

| 项目 | 作者 | 功能 | 成熟度 |
|------|------|------|--------|
| [plur](https://github.com/plur-ai/plur) | plur-ai | 开放 engram 格式 (YAML) 共享记忆层 | beta |
| [hermes-web-search-plus](https://github.com/robbyczgw-cla/hermes-web-search-plus) | robbyczgw-cla | 多提供商网页搜索（Serper/Tavily/Exa 智能路由） | beta |
| [hermes-weather-plugin](https://github.com/FahrenheitResearch/hermes-weather-plugin) | FahrenheitResearch | 专业天气（NWS/NEXRAD 雷达/气象计算） | beta |
| [evey-bridge-plugin](https://github.com/42-evey/evey-bridge-plugin) | 42-evey | Claude Code ↔ Hermes 双向桥接 | beta |
| [hermes-payguard](https://github.com/nativ3ai/hermes-payguard) | nativ3ai | USDC/x402 安全支付（消费上限+审批流） | experimental |
| [hermes-plugin-chrome-profiles](https://github.com/anpicasso/hermes-plugin-chrome-profiles) | anpicasso | CDP Chrome profile 多账号切换 | experimental |
| [hermes-wxtrain-plugin](https://github.com/FahrenheitResearch/hermes-wxtrain-plugin) | FahrenheitResearch | 气象 ML 训练数据集构建 (HRRR/GFS/ERA5) | experimental |
| [hermes-cloudflare](https://github.com/raulvidis/hermes-cloudflare) | raulvidis | Cloudflare 无头浏览器渲染 | experimental |

### 5. 技能注册表与发现（2 条目）

| 项目 | 作者 | 描述 | 成熟度 |
|------|------|------|--------|
| [skilldock.io](https://github.com/chigwell/skilldock.io) | chigwell | 跨平台 AI 技能注册表（OpenClaw/Claude/Hermes） | production |
| [hermeshub](https://github.com/amanning3390/hermeshub) | amanning3390 | Hermes 社区技能中心（浏览/分享/安装） | beta |

### 6. 工具与实用程序（11 条目）

| 项目 | 作者 | 亮点 | 成熟度 |
|------|------|------|--------|
| [hermes-workspace](https://github.com/outsourc-e/hermes-workspace) (500★) | outsourc-e | **最完整 Hermes GUI**，Web 工作区 | production |
| [mission-control](https://github.com/builderz-labs/mission-control) (3.7k★) | builderz-labs | **agent 编排仪表盘**，fleet 管理/任务分发/成本跟踪 | production |
| [hermes-webui](https://github.com/sanchomuzax/hermes-webui) | sanchomuzax | 轻量级进程监控与配置仪表盘 | beta |
| [portable-hermes-agent](https://github.com/rookiemann/portable-hermes-agent) | rookiemann | Windows 桌面应用，100 工具+GUI+本地模型 | beta |
| [evey-setup](https://github.com/42-evey/evey-setup) | 42-evey | 一条命令搭建完整技术栈（29 插件+免费模型） | beta |
| [vessel-browser](https://github.com/unmodeled-tyler/vessel-browser) | unmodeled-tyler | AI 原生 Linux 浏览器，MCP 控制 | experimental |
| [flowstate-qmd](https://github.com/amanning3390/flowstate-qmd) | amanning3390 | 预期式记忆系统（RAG+向量搜索，预取上下文） | beta |
| [lintlang](https://github.com/roli-lpci/lintlang) | roli-lpci | agent 配置/提示词静态 linter (HERM v1.1) | beta |
| [nix-hermes-agent](https://github.com/0xrsydn/nix-hermes-agent) | 0xrsydn | Nix flakes 可复现部署 | beta |
| [openclaw-to-hermes](https://github.com/jefferyjob/awesome-hermes-agent-zh) | jefferyjob | OpenClaw→Hermes 迁移工具（v0.3.0+ 推荐原生命令） | beta |
| [hermes-neurovision](https://github.com/Tranquil-Flow/hermes-neurovision) | Tranquil-Flow | 42 种动画主题终端神经可视化器 | experimental |

### 7. 部署（4 条目）

| 项目 | 作者 | 方式 | 成熟度 |
|------|------|------|--------|
| [hermes-agent-docker](https://github.com/xmbshwll/hermes-agent-docker) | xmbshwll | 最小化 Docker 沙箱 | beta |
| [hermes-agent-template](https://github.com/Crustocean/hermes-agent-template) | Crustocean | Crustocean 云端生产就绪 Docker | beta |
| [hermes-autonomous-server](https://github.com/JackTheGit/hermes-autonomous-server) | JackTheGit | systemd+cron 无头部署 | experimental |
| [portainer-stack-hermes](https://github.com/ellickjohnson/portainer-stack-hermes) | ellickjohnson | Docker Compose + Portainer + Web 终端 | experimental |

### 8. 集成与桥接（10 条目）

| 项目 | 作者 | 连接目标 | 成熟度 |
|------|------|---------|--------|
| [hindsight](https://github.com/vectorize-io/hindsight) | Vectorize | **长期记忆层** (retain/recall/reflect) | production |
| [hermes-android](https://github.com/raulvidis/hermes-android) | raulvidis | Android 设备控制 | beta |
| [hermes-miniverse](https://github.com/teknium1/hermes-miniverse) | teknium1¹ | Miniverse 像素世界 | beta |
| [honcho-self-hosted](https://github.com/elkimek/honcho-self-hosted) | elkimek | 自托管 Honcho 记忆后端 | beta |
| [hermes-agent-acp-skill](https://github.com/Rainhoole/hermes-agent-acp-skill) | Rainhoole | Hermes/Codex/Claude 多 agent 委派 | beta |
| [reina](https://github.com/Crustocean/reina) | Crustocean | Crustocean 平台集成 | beta |
| [zouroboros-swarm-executors](https://github.com/marlandoj/zouroboros-swarm-executors) | marlandoj | Claude Code + Hermes 任务移交 | experimental |
| [hermes-blockchain-oracle](https://github.com/gizdusum/hermes-blockchain-oracle) | gizdusum | Solana 链上数据 MCP | experimental |
| [hermes-council](https://github.com/Ridwannurudeen/hermes-council) | Ridwannurudeen | 对抗式多视角 council | experimental |
| [NemoHermes](https://github.com/Hmbown/NemoHermes) | Hmbown | NVIDIA 能力注册表+GPU 路由 | experimental |

> ¹ teknium1 是 Nous Research 联合创始人之一。

### 9. 检测与媒体取证（1 条目）

| 项目 | 作者 | 功能 | 成熟度 |
|------|------|------|--------|
| [detect-skill](https://github.com/resemble-ai/detect-skill) | Resemble AI | 语音与媒体真伪检测 | beta |

### 10. 多 Agent 与 Swarm（4 条目）

| 项目 | 作者 | 模式 | 成熟度 |
|------|------|------|--------|
| [bigiron](https://github.com/supermodeltools/bigiron) | supermodeltools | Hermes + Supermodel 代码图谱 → AI 原生 SDLC | beta |
| [opencode-hermes-multiagent](https://github.com/1ilkhamov/opencode-hermes-multiagent) | 1ilkhamov | 17 个专用 agent，结构化接口通信 | beta |
| [Ankh.md](https://github.com/Abruptive/Ankh.md) | Abruptive | TAW Agent x Hermes 多 agent swarm | experimental |
| [gladiator](https://github.com/runtimenoteslabs/gladiator) | runtimesnoteslabs | 两家 AI 公司争夺 GitHub stars（黑客松） | experimental |

### 11. 领域应用（11 条目）

| 项目 | 作者 | 领域 | 成熟度 |
|------|------|------|--------|
| [hermescraft](https://github.com/bigph00t/hermescraft) | bigph00t | Minecraft AI 伙伴，持久记忆 | beta |
| [anihermes](https://github.com/rodmarkun/anihermes) | rodmarkun | 动漫追踪器，自然语言界面 | beta |
| [job-scout-agent](https://github.com/Christabel337/job-scout-agent) | Christabel337 | 自主求职 agent | beta |
| [hermes-ai-infrastructure-monitoring-toolkit](https://github.com/JackTheGit/hermes-ai-infrastructure-monitoring-toolkit) | JackTheGit | 基础设施监控 (Telegram+cron) | beta |
| [hermes-startup-architect](https://github.com/dlkakbs/hermes-startup-architect) | dlkakbs | 创业资料包生成（市场分析/deck/财务预测） | beta |
| [mercury](https://github.com/hxsteric/mercury) | hxsteric | 多链区块链现金流分析 (WebGL 仪表盘) | beta |
| [hermes-embodied](https://github.com/bryercowan/hermes-embodied) | bryercowan | 机器人 VLA 微调（Nous Hackathon） | experimental |
| [Hermes-mars-rover](https://github.com/Snehal707/Hermes-mars-rover) | Snehal707 | ROS2+Gazebo 火星车模拟 | experimental |
| [hermes-genesis](https://github.com/Ridwannurudeen/hermes-genesis) | Ridwannurudeen | 程序化"活世界"引擎 | experimental |
| [hermes-legal](https://github.com/Lethe044/hermes-legal) | Lethe044 | 合同风险分析（英/土） | experimental |
| [hermes-research-agent](https://github.com/Aum08Desai/hermes-research-agent) | Aum08Desai | 自主 LLM 研究（文献综述/假设/实验设计） | experimental |

### 12. 分叉与衍生（4 条目）

| 项目 | 作者 | 方向 | 成熟度 |
|------|------|------|--------|
| [hermes-agent-camel](https://github.com/nativ3ai/hermes-agent-camel) | nativ3ai | CaMeL 信任边界 + 正式验证 | beta |
| [hermes-alpha](https://github.com/kaminocorp/hermes-alpha) | kaminocorp | 云端部署版 + 预配基础设施模板 | beta |
| [orahermes-agent](https://github.com/jasperan/orahermes-agent) | jasperan | Oracle OCI GenAI + 26ai 企业入口 | experimental |
| [hermes-skill-distillation](https://github.com/beardthelion/hermes-skill-distillation) | beardthelion | agentic 训练轨迹生成（黑客松） | experimental |

### 13. 指南与文档（3 条目）

| 项目 | 作者 | 内容 | 成熟度 |
|------|------|------|--------|
| [hermes-wsl-ubuntu](https://github.com/metantonio/hermes-wsl-ubuntu) | metantonio | Windows WSL2 分步搭建 | production |
| [hermes-agent-docs](https://github.com/mudrii/hermes-agent-docs) | mudrii | 社区文档（详细覆盖 v0.2.0 部署模式） | beta |
| [HermesWiki](https://github.com/martymcenroe/HermesWiki) | martymcenroe | 社区 wiki，实用模式+部署建议 | beta |

### 14. 运维作战手册 & 进阶蓝图

**5 条运维最佳实践**：
1. 夜间自我进化 + 护栏评估（self-evolution + 验证 cron）
2. 用 Honcho/Hindsight 处理记忆压力 → 参见本知识库 [[concepts/hindsight-in-hermes-ecosystem-2026]]
3. 尽早调整 session timeout/expiry
4. OpenClaw 并行迁移（双系统运行至行为一致后切换）
5. 有意识地维护 USER.md 和 MEMORY.md（简洁/持久/聚焦偏好）

**2 条进阶蓝图**：
- **工作区优先**：hermes-workspace (GUI) + wondelai/skills (技能底座) → 见 [[entities/hermes-workspace]]
- **编排运维**：mission-control (调度) + hindsight (记忆) → 见 [[concepts/hindsight-in-hermes-ecosystem-2026]]

## 与已有知识库的交叉引用

本 wiki 已深度覆盖以下条目，awesome list 提供补充视角：

| Awesome 条目 | Wiki 已有页面 | 覆盖程度 |
|-------------|-------------|---------|
| Hindsight | [[concepts/hindsight-in-hermes-ecosystem-2026\|concept]] + [[methods/install-hindsight-native-hermes-method\|method]] + [[methods/hindsight-4d-retrieval-complete\|4D检索]] + [[notes/hindsight-local-deployment-windows-2026\|部署]] + [[notes/hindsight-risks-and-optimizations-2026\|风险]] + [[comparisons/hindsight-automation-patterns-2026\|4模式]] + [[concepts/hindsight-memory-modes-guide\|4模式指南]] | ⭐⭐⭐ 全覆盖 |
| hermes-workspace | [[entities/hermes-workspace\|实体]] + [[entities/hermes-workspace-architecture\|架构]] + [[entities/hermes-workspace-deployment-guide\|部署]] | ⭐⭐⭐ 全覆盖 |
| Hermes Skills 系统 | 10 个 [[entities/hermes-skill-*\|skill 实体页]] | ⭐⭐ 部分覆盖 |
| LCM 记忆 | [[notes/lcm-upgrade-v0.12-to-v0.15\|升级记录]] + [[concepts/agent-memory-state-2026\|记忆状态]] | ⭐⭐ 部分覆盖 |
| MCP 生态 | [[concepts/mcp-ecosystem-2026\|MCP 全景]] + [[concepts/mcpb-bundle-format\|Bundle 格式]] | ⭐⭐ 部分覆盖 |
| Kanban/Swarm | [[concepts/hermes-kanban\|Kanban]] + [[entities/hermes-skill-kanban-orchestrator\|编排]] + [[entities/hermes-skill-kanban-worker\|Worker]] | ⭐⭐ 部分覆盖 |

**Wiki 未覆盖但值得关注的条目**（按优先级）：
1. `wondelai/skills` — agentskills.io 核心技能库，推荐作为 Hermes 第一步
2. `mission-control` — agent fleet 编排仪表盘，3.7k stars
3. `hermes-agent-self-evolution` — 官方进化式自我改进管线
4. `hermes-plugins` — 四插件运维套件
5. `hermes-dojo` — 自我改进系统

## 关键洞察

1. **Hermes 的核心差异化**：唯一内置学习闭环的 agent——能从经验中创建技能，跨会话建立用户深层模型
2. **agentskills.io 是技能互操作性的核心标准**：12 个条目，从安全到区块链到 CRM，跨 Hermes/Claude/Cursor/Codex
3. **记忆层双雄**：Hindsight（生产级，已落地）+ Honcho（自托管备选）
4. **GUI 之争**：hermes-workspace（完整工作区，500★）vs mission-control（编排仪表盘，3.7k★）vs hermes-webui（轻量监控）
5. **部署生态分层**：Docker（主流）→ Nix（可复现）→ systemd（无头服务器）→ Portainer（Web 管理）

## 关联页面

- [[raw/tech/awesome-hermes-agent-zh]] — 完整源文件（30KB）
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 在本生态中的定位
- [[entities/hermes-workspace]] — Hermes Workspace 实体
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider 对比（含 Hindsight vs Honcho）
- [[concepts/mcp-ecosystem-2026]] — MCP 生态全景（交叉覆盖多个集成条目）
- [[concepts/full-stack-ecosystem]] — 14 节点全栈地图（补充视角）
