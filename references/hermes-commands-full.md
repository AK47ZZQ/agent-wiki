Hermes命令大全V2
Hermes命令大全
📖 Hermes Agent 命令大全
Hermes Agent 完整命令手册 — 共 126 个命令

⚡ 基本命令

/new [name]
开始一个新会话。创建一个全新的会话 ID，清空当前对话历史记录。可选的 \[name\] 参数可以为新会话命名，方便后续通过 /resume 恢复。
别名：/reset
参数：\[name\] — 可选，新会话的名称
示例：/new、/new feature\-auth

/retry
重试最后一条消息。将上一次用户输入重新发送给代理，用于代理响应不符合预期时重新生成。不会改变你的输入内容，但代理将重新处理。
无参数

/undo
撤销最后一次交互。删除最近一次用户/助手消息对，回退到之前的状态。适合在代理给出了错误响应时使用。
无参数
可连续使用多次

/stop
终止所有正在运行的后台进程。立即杀死所有由 /background 启动的后台任务以及任何运行中的子代理。
无参数

/help
显示帮助信息。列出所有可用的命令和基本用法。
无参数

/commands [page]
浏览所有命令和技能。分页显示完整的命令列表（内置命令 + 技能命令），每页约 18 个条目。
参数：\[page\] — 页码，从 1 开始
示例：/commands 3
🗂️ 会话管理

/title [name]
为当前会话设置标题。给当前对话一个有意义的名称，方便后续通过 /sessions 或 /resume 查找和恢复。
参数：\[name\] — 会话标题
示例：/title Debug auth bug

/branch [name]
分支当前会话。基于当前会话的历史创建一个新分支，用于探索不同的解决路径而不影响原始对话。
别名：/fork
参数：\[name\] — 分支名称
示例：/branch try\-different\-approach

/compress [focus topic]
压缩对话上下文。手动触发上下文压缩，将之前的对话内容总结提炼，减少 token 占用。可选 focus topic 指定压缩重点保留的主题。
参数：\[focus topic\] — 可选，需要保留的重点话题
示例：/compress authentication flow

/rollback [number]
文件系统回滚。列出或恢复到文件系统检查点。Hermes 会自动在关键操作前创建文件系统快照。
参数：\[number\] — 可选，回滚到的检查点编号；不传则列出所有可用检查点
示例：/rollback、/rollback 3

/resume [name]
恢复之前的会话。根据会话名称跳转到之前保存的会话，继续之前的对话。
参数：\[name\] — 要恢复的会话名称
示例：/resume feature\-auth

/sessions
浏览历史会话。列出所有之前命名的会话，支持浏览和选择恢复。
无参数

/topic [off|help|session-id]
主题会话管理。启用或检查 Telegram DM 中的主题会话功能。用于在 Telegram 私聊中创建子主题。
参数：off 关闭 | help 查看帮助 | session\-id 检查当前会话 ID
示例：/topic help

/status
显示会话信息。查看当前会话的元数据：会话 ID、模型、配置文件、上下文大小等。
无参数

/whoami
查看权限。显示你当前的斜杠命令访问级别——是管理员（admin）还是普通用户（user）。
无参数

/profile
查看活动配置。显示当前正在使用的配置文件名称和 Hermes 主目录路径。
无参数

/sethome
设置主频道。将当前聊天窗口设为 Hermes 的主频道，所有例行通知和自动消息将发送到这里。
别名：/set\-home
无参数

/footer [on|off|status]
页脚开关。切换最终回复中是否显示网关运行时元数据页脚（包含模型、延迟、token 用量等信息）。
参数：on 开启 | off 关闭 | status 查看当前状态
示例：/footer off
🎯 任务与目标

/background <prompt>
后台运行任务。将提示作为独立任务在后台执行，你可以在前台继续聊天。后台任务完成后会通知你。
别名：/bg、/btw（by the way）
参数：\&lt;prompt\&gt; — 必需，后台任务描述
示例：/background 搜索最近的 AI 新闻

/agents
查看活动代理。显示当前所有活动的代理会话和正在运行的后台任务列表。
别名：/tasks
无参数

/queue <prompt>
排队提示。将一条提示排入等待队列，在当前回合完成后自动执行。不会中断当前对话。
别名：/q
参数：\&lt;prompt\&gt; — 要排队的提示内容
示例：/queue 帮我翻译这段话

/steer <prompt>
引导注入。在下次工具调用完成后注入一条消息，不影响当前正在进行的操作流程。
参数：\&lt;prompt\&gt; — 要注入的消息内容
示例：/steer 改用中文回复

/goal [text | pause | resume | clear | status]
设置长期目标。设置一个跨回合持续执行的目标，Hermes 会在每次响应时记住并推进这个目标，直到完成为止。
参数：text 设置新目标 | pause 暂停 | resume 恢复 | clear 清除 | status 查看状态
示例：/goal 帮我调研并实现用户认证功能

/subgoal [text | remove N | clear]
管理子目标。在已有的长期目标上添加或管理额外的子标准/里程碑。
参数：text 添加子目标 | remove N 移除第 N 条 | clear 清除所有
示例：/subgoal 先完成数据库模型设计
🛡️ 安全与审批

/approve [session|always]
批准危险命令。批准待处理的高风险操作（如文件删除、系统修改等）。
参数：session 本次会话内自动批准 | always 永久信任
示例：/approve session

/deny
拒绝危险命令。拒绝当前待处理的危险命令审批请求。
无参数

/yolo
YOLO 模式。切换&#34;你只活一次&#34;模式——开启后跳过所有危险命令审批，直接执行。慎用！
无参数（切换开关）
🤖 模型与配置

/model [model] [--provider name] [--global]
切换模型。切换当前会话使用的大语言模型，也可以指定不同的提供商（如 OpenAI、Anthropic 等）。
别名：/provider
参数：\[model\] 模型名 | \-\-provider name 指定提供商 | \-\-global 全局生效
示例：/model gpt\-4o、/model claude\-sonnet\-4 \-\-provider anthropic

/codex-runtime [auto|codex_app_server]
Codex 运行时。切换 OpenAI/Codex 模型的 Codex 应用服务器运行时模式。
参数：auto 自动 | codex\_app\_server 指定使用应用服务器
示例：/codex\-runtime auto

/personality [name]
切换个性。设置预定义的代理个性，改变回复风格（如简洁、详细、幽默等）。
参数：\[name\] — 个性名称
示例：/personality concise

/reasoning [level|show|hide]
推理管理。控制代理展示思考过程的方式。可设置推理工作量级别，或显示/隐藏推理过程。
参数：level 设置级别 | show 显示 | hide 隐藏
示例：/reasoning hide

/fast [normal|fast|status]
快速模式。切换 OpenAI 优先处理或 Anthropic 快速响应模式，以牺牲一定质量为代价换取更快的响应速度。
参数：normal 正常 | fast 快速 | status 状态
示例：/fast fast

/voice [on|off|tts|status]
语音模式。切换语音交互模式。开启后代理的回复将转为语音播报。
参数：on 开启 | off 关闭 | tts 文本转语音 | status 状态
示例：/voice on
📦 技能与扩展

/bundles
列出技能包。显示所有可用的技能包及其别名。技能包是多技能的快捷组合，通过 /\&lt;name\&gt; 快速调用。
别名：/\&lt;name\&gt; — 直接用包名作为命令
无参数

/curator [subcommand]
技能管理员。后台技能维护工具，支持查看状态、运行/停止、固定/取消固定、存档/恢复技能。
参数：status 状态 | run 运行 | pin 固定 | archive 存档 | list\-archived 列出存档
示例：/curator status

/kanban [subcommand]
看板面板。多配置文件协作看板，用于管理跨 session 的任务、链接和评论。
参数：tasks 任务管理 | links 链接 | comments 评论
示例：/kanban tasks

/reload-mcp
重载 MCP。从配置文件中重新加载所有 MCP（模型上下文协议）服务器，用于在新增或修改 MCP 配置后生效。
无参数

/reload-skills
重载技能。重新扫描 \~/\.hermes/skills/ 目录，识别新增或移除的技能，更新可用命令列表。
无参数
🔧 调试与管理

/restart
重启网关。等待所有正在运行的任务完成后，优雅地重启 Hermes 网关服务。
无参数

/usage
用量统计。显示当前会话的 token 使用量、速率限制和成本估算（如果已配置）。
无参数

/insights [days]
使用洞察。显示 Hermes 的使用情况分析和统计，包括对话次数、token 消耗趋势等。
参数：\[days\] — 可选，回溯天数，默认 7 天
示例：/insights 30

/platform <pause|resume|list> [name]
平台管理。暂停、恢复或列出故障的网关平台连接（如 Telegram、Discord 等）。
参数：pause 暂停 | resume 恢复 | list 列出
示例：/platform list

/update
更新 Hermes。将 Hermes Agent 更新到最新版本。
无参数

/debug
调试报告。收集系统信息 + 日志，上传并生成可共享的调试链接，便于排查问题。
无参数

🧩 技能命令
🎨 设计与创意

/architecture-diagram
架构图。以 HTML 格式生成暗色主题的 SVG 架构图/云架构/基础设施图，适合技术文档和演示文稿。

/ascii-art
ASCII 艺术。使用 pyfiglet、cowsay、boxes 等工具生成 ASCII 艺术字，或将图片转换为 ASCII 字符画。

/ascii-video
ASCII 视频。将视频或音频文件转换为彩色 ASCII 艺术风格的 MP4/GIF 动画。

/baoyu-article-illustrator
文章插图。根据文章内容自动配图，支持类型 × 风格 × 调色板一致性，适合博客和出版物。

/baoyu-comic
知识漫画。生成教育、传记、教程类的知识漫画，将文字内容转化为漫画分镜。

/baoyu-infographic
信息图。21 种布局 × 21 种风格的信息图生成器，将数据可视化呈现。

/claude-design
设计原型。设计一次性 HTML 作品——着陆页、演示文稿、原型。注重设计过程和审美。

/design-md
DESIGN.md 规范。编写/验证/导出 Google 风格的 DESIGN.md 令牌规范文件，用于设计系统文档化。

/excalidraw
手绘风格图。生成手绘风格的 Excalidraw JSON 图表，支持架构图、流程图、时序图。

/gif-search
GIF 搜索。通过 curl + jq 从 Tenor（GIF 搜索引擎）搜索和下载 GIF 动图。

/heartmula
音乐生成。HeartMuLa：类似 Suno AI 的歌曲生成工具，从歌词和标签生成音乐。

/manim-video
数学动画。使用 Manim CE（3Blue1Brown 使用的引擎）生成数学/算法解说动画视频。

/p5js
创意编程。p5.js 草图：生成艺术、着色器、交互式作品和 3D 可视化。

/pixel-art
像素艺术。像素画生成器，支持 NES、Game Boy、PICO-8 等经典游戏机调色板。

/popular-web-designs
流行设计系统。54 个真实世界的设计系统（Stripe、Linear、Vercel、Apple 等）以 HTML/CSS 形式呈现，可直接使用。

/sketch
设计草图。快速生成一次性 HTML 线框图/高保真原型，支持 2-3 个设计变体并行比较。

/songsee
音频可视化。通过 CLI 生成音频频谱图和特征图（mel、chroma、MFCC）。

/songwriting-and-ai-music
歌曲创作。结合歌曲创作技巧和 Suno AI 音乐提示生成，可以帮写歌词和优化提示词。

/pretext
创意浏览器演示。使用 @chenglou/pretext 构建无 DOM 的文本布局演示，支持 ASCII 艺术排版、文字绕障碍物、文字几何游戏、动态排版。
🤖 AI 与 ML

/arxiv
论文搜索。按关键词、作者、类别或 ID 搜索 arXiv 学术论文，获取摘要和下载链接。

/blogwatcher
博客监控。通过 blogwatcher-cli 工具监控博客和 RSS/Atom 源，及时发现新内容。

/comfyui
ComfyUI 图像生成。安装、启动、管理 ComfyUI 节点和模型，运行工作流并注入参数，支持图像、视频和音频生成。

/dspy
声明式 AI 编程。DSPy 框架：声明式 LM 程序，自动优化提示词，支持 RAG（检索增强生成）等高级模式。

/godmode
LLM 越狱。高级提示注入技术：Parseltongue、GODMODE、ULTRAPLINIAN 等，用于红队测试和安全评估。

/huggingface-hub
HuggingFace Hub。通过 hf CLI 搜索、下载和上传模型与数据集。

/ideation
创意生成。通过创造性约束条件生成项目创意，适合头脑风暴和灵感探索。

/jupyter-live-kernel
Jupyter 内核。通过实时 Jupyter 内核（hamelnb）进行迭代式 Python 编程，适合数据分析和原型开发。

/llama-cpp
本地 LLM 推理。在本地运行 GGUF 格式的模型推理，支持从 HuggingFace Hub 发现和下载模型。

/llm-wiki
LLM 知识库。构建和查询交叉链接的 Markdown 格式知识库（Karpathy 风格），用于知识管理。

/segment-anything-model
图像分割。使用 SAM（Segment Anything Model）进行零样本图像分割，支持点选、框选和掩码方式。

/weights-and-biases
W&amp;B 实验跟踪。记录 ML 实验、超参数搜索、模型注册表和可视化仪表板。

/youtube-content
YouTube 内容处理。将 YouTube 视频的转录文本转换为摘要、推文文章、博客等格式。
💻 编码与开发

/claude-code
Claude Code 委托。将编码任务委托给 Claude Code CLI，用于实现功能和 PR。

/codebase-inspection
代码库检查。通过 pygount 分析代码库：代码行数、编程语言分布、代码比例。

/codex
Codex CLI 委托。将编码任务委托给 OpenAI Codex CLI，用于实现功能和 PR。

/debugging-hermes-tui-commands
调试 Hermes TUI。调试 Hermes TUI 斜杠命令系统：Python 代码、网关通信、Ink UI 渲染。

/hermes-agent
配置 Hermes Agent。配置、扩展或贡献 Hermes Agent 自身——模型、提供商、工具、技能、插件等。

/hermes-agent-skill-authoring
技能创作。在 Hermes 仓库中编写 SKILL.md：前置元数据、验证器、目录结构规范。

/hermes-s6-container-supervision
容器监督。修改、调试或扩展 s6-overlay 监督树（Hermes Docker 镜像中的进程管理），添加新服务或调试网关。

/humanizer
人性化文本。去除 AI 生成文本的特征，添加真实的人类口吻和个性化表达。

/node-inspect-debugger
Node.js 调试。通过 --inspect 标志和 Chrome DevTools 协议 CLI 调试 Node.js 应用程序。

/opencode
OpenCode 委托。将编码任务委托给 OpenCode CLI，用于实现功能和 PR 审查。

/plan
计划模式。以&#34;只计划不执行&#34;模式编写 Markdown 计划，保存到 \.hermes/plans/ 目录。

/requesting-code-review
代码审查。提交前自动审查流水线：安全扫描、质量门禁、独立审查者子代理、自动修复循环。

/spike
技术探针。快速一次性实验，在正式实现前验证想法的可行性，完成后丢弃。

/subagent-driven-development
子代理驱动开发。通过 delegate_task 子代理按计划执行任务，2 阶段审查（规范审查 + 代码质量）。

/systematic-debugging
系统化调试。4 阶段根因调试流程：根因调查 → 模式分析 → 假设验证 → 修复。找到根源再修。

/test-driven-development
测试驱动开发。强制 RED-GREEN-REFACTOR 循环：先写失败测试，再写最小代码让它通过，最后重构。

/touchdesigner-mcp
TouchDesigner 控制。通过 twozero MCP 控制运行中的 TouchDesigner 实例——创建节点、设置参数、连线、执行 Python、构建实时视觉。36 个原生工具。

/writing-plans
编写实现计划。写完整的实现计划：小块任务（2-5 分钟）、精确文件路径、完整代码、验证步骤。DRY、YAGNI、TDD。

/webhook-subscriptions
Webhook 订阅。事件驱动的代理自动运行——配置 Webhook 使 Hermes 在外部事件发生时自动执行任务。
🐱 GitHub 与项目管理

/github-auth
GitHub 认证。设置 GitHub 认证：HTTPS 令牌、SSH 密钥、gh CLI 登录配置。

/github-code-review
GitHub PR 审查。审查其他人的 Pull Request：查看差异、通过 gh CLI 或 REST API 添加内联评论。

/github-issues
GitHub Issues。创建、分类、标记、分配 GitHub Issue，通过 gh CLI 或 REST API 管理。

/github-pr-workflow
GitHub PR 流程。完整的 PR 生命周期管理：创建分支、提交代码、打开 PR、等待 CI、合并代码。

/github-repo-management
仓库管理。克隆/创建/分叉仓库，管理远程仓库、发布版本。

/linear
Linear 项目管理。通过 GraphQL + curl 管理 Linear 项目：问题、项目、团队。

/kanban-codex-lane
Kanban Codex 通道。当 Hermes Kanban 工作者使用 Codex CLI 作为隔离实现通道时的专用模式——Hermes 保留任务生命周期、协调、测试和交接。

/kanban-orchestrator
Kanban 编排者。编排者角色的分解手册和反诱惑规则——通过 Kanban 路由工作，管理多工作者并行。

/kanban-worker
Kanban 工作者。Hermes Kanban 工作者的陷阱、示例和边界情况处理指南。
📮 飞书与协作

/feishu-cli
飞书 CLI。安装、配置和认证飞书/Lark CLI，包括 Hermes 绑定、二维码登录和身份策略配置。

/feishu-integration
飞书集成。将飞书/Lark 完整集成到 Hermes：安装 CLI、绑定应用、OAuth 登录、管理权限、发送富消息、构建机器人。

/feishu-rich-message
飞书富消息。通过 lark-cli 发送飞书富文本消息（Post 格式）和互动卡片（Interactive Card），适合结构化数据和表格。

/notion
Notion 集成。通过 Notion API + ntn CLI 管理页面、数据库、Markdown 导入导出、Workers。

/obsidian
Obsidian 笔记。读取、搜索、创建和编辑 Obsidian 保管库中的笔记文件。

/yuanbao
元宝群组。在元宝（企业微信群）中 @提及用户，查询群组信息和成员。
📧 邮箱与通信

/google-workspace
Google Workspace。通过 gws CLI 或 Python 使用 Gmail、日历、云端硬盘、文档和表格。

/himalaya
终端邮件。通过 Himalaya CLI 在终端中收发邮件（IMAP/SMTP），支持多账户。
📄 文档与办公

/airtable
Airtable API。通过 curl 调用 Airtable REST API：记录增删改查、过滤器、批量插入更新。

/nano-pdf
PDF 编辑。通过 nano-pdf CLI 用自然语言编辑 PDF——修改文本、修正错字、更改标题。

/ocr-and-documents
OCR 与文档提取。从 PDF/扫描件中提取文字（使用 pymupdf、marker-pdf）。

/powerpoint
PPT 操作。创建、读取和编辑 .pptx 演示文稿：幻灯片、备注、模板、内容编辑。

/teams-meeting-pipeline
Teams 会议流水线。操作 Microsoft Teams 会议摘要流水线：总结会议、检查流水线状态、重放作业、管理订阅。
🏠 智能家居

/openhue
飞利浦 Hue。通过 OpenHue CLI 控制飞利浦 Hue 智能灯：开关灯、调整亮度/颜色、场景切换、房间管理。
🎵 社交与娱乐

/spotify
Spotify 控制。播放、搜索、排队，管理播放列表和设备。

/pokemon-player
宝可梦游戏。通过无头模拟器 + RAM 读取数据玩宝可梦游戏。

/maps
地图服务。通过 OpenStreetMap/OSRM 进行地理编码、兴趣点查询、路线规划和时区查询。
📊 预测与金融

/polymarket
Polymarket 预测市场。查询预测市场数据：市场列表、价格、订单簿、历史数据。
🔌 MCP 与集成

/native-mcp
原生 MCP 客户端。连接 MCP 服务器、注册工具，支持 stdio 和 HTTP 传输方式。

/dogfood
内部质量测试。对 Web 应用进行探索性 QA 测试：发现 Bug、收集证据、生成测试报告。


Hermes Agent — nousresearch.com
🆕 新增技能 (2026-05-27)
软件工程
/agency\-agents\-sync — 🔄 代理仓库同步。从 msitarzewski/agency-agents（106k ⭐，147+ 代理）批量导入代理作为 Hermes 技能。支持单代理导入、分类过滤、全部批量下载，自动转换 frontmatter 格式。
/hermes\-skills\-roster — 📋 技能目录。生成所有已安装 Hermes 技能的完整目录/名册——按分类排序，含 emoji、描述和使用建议。支持终端输出、Python 表格、Markdown 文件导出。
/hermes\-skills\-export — 📤 技能导出。将 Hermes 技能导出为其他 AI 编码工具格式——Cursor (.mdc)、Claude Code (.md)、Aider (CONVENTIONS.md)、Windsurf (.windsurfrules)、OpenCode (.md)、GitHub Copilot。一次编写，到处运行。
MCP &amp; 集成
/openclaw\-integration — 🏗️ OpenClaw 集成。桥接 Hermes Agent 与 OpenClaw 多代理生态系统。支持双向格式转换（Hermes SKILL.md ↔ OpenClaw SOUL.md/IDENTITY.md/AGENTS.md），以及 MCP 网关桥接。

(注：内容由 AI 生成，请谨慎参考）
🆕 新增技能（2026-05-28）
wiki-archive
描述： 归档 Hermes session 到 Obsidian wiki，自动生成 wikilinks 和 Graph View 节点
路径：~/.hermes/skills/hermes/wiki-archive/
命令：

python3 archiver.py              # 归档最新 session
python3 archiver.py --all        # 归档全部历史
python3 archiver.py --stats      # 统计知识库规模
cron： 每日 23:00 自动归档，推送到飞书
wiki-ingest
描述： 摄入 URL/文件/文本到 wiki，提取摘要、概念、实体页
wiki-methods
描述： 从 session 中提取可复用工作流，保存到 wiki/methods/
🆕 wiki 知识库命令（2026-05-28）


操作

命令

自然语言触发

归档 session 到知识库

`/wiki-archive`

保存到 wiki / 归档这个 session / 存档

灌资料（URL/文件/文本）

`/wiki-ingest`

灌资料 / 摄入文档 / 把这篇文章加入知识库

查知识库

`/wiki-query`

查知识库 / 问 wiki 里关于

提取可复用工作流

`/wiki-methods`

沉淀方法 / 提取工作流 / 记录最佳实践

健康检查

`/wiki-lint`

扫描 wiki / lint 检查
Wiki 知识库： 42 页面 · 201 wikilinks · gusibi/Karpathy 风格 · Obsidian Graph View 可可视化


🆕 更新 (2026-05-28)
系统优化与新增组件
🧠 记忆系统升级 — Mnemosyne v3.1.0
内存引擎升级：从旧版 FTS5 关键词搜索升级为 Mnemosyne 三层记忆系统。
存储格式：向量语义 (50%) + FTS5 全文 (30%) + 重要性 (20%) 混合检索
记忆层级：工作记忆 → 情景记忆（三层 BEAM 架构）
时间知识图谱：TripleStore 版本化事实，支持 query_time 回溯
数据库：~/.hermes/mnemosyne/data/mnemosyne.db
配置：memory.provider=mnemosyne
🔄 进化循环
P0-P3 优先级项目全部完成，形成完整闭环：

P0 ✅ rtk-rewrite     → 终端命令 RTK 重写（降低 token 用量）
P1 🟢 Mnemosyne       → 向量记忆引擎
P2 ✅ SkillClaw       → 旁路注入 + 技能自动进化（运行中 :30000）
P3 ✅ self-evolution  → GEPA 进化引擎（evolution 模块）
P3 ✅ hermes-dojo     → 技能缺陷检测 + 自动修复（/dojo 命令）
⚡ rtk-rewrite 插件
终端命令优化。通过 rtk rewrite 自动将长命令缩短为等效短命令，减少工具输出 token 消耗。
安装：pip install rtk-hermes（需在 Hermes venv 中）
配置：plugins.enabled 添加 rtk-rewrite
验证：日志出现 [rtk] Hermes plugin registered
二进制：rtk v0.40.0
状态：entry-point 插件，不在 hermes plugins list 显示
🧩 新增技能
hermes-windows — Windows 专属指南
Windows 系统下 Hermes 的已知问题和解决方法——配置文件路径、CLI 标志冲突、路径转换、终端后端差异。

/hermes-windows
context-engine-plugins — 上下文引擎管理
安装、启用、配置和排错上下文引擎插件（如 LCM 替换内置 ContextCompressor）。

/context-engine-plugins
memory-maintenance — 记忆维护
管理、合并、扩展 Hermes 持久内存——清理过期条目、合并相关事实、优化容量。

/memory-maintenance
hermes-dojo — 技能训练场
持续自我改进系统。分析历史会话发现失败模式和技能缺口，自动创建或优化技能，运行自进化修复。

/dojo           # 分析失败模式
/dojo improve   # 修复最弱技能 + 运行进化
路径：~/.hermes/skills/hermes-dojo/
hermes-agent-self-evolution — GEPA 进化引擎
Hermes Agent 的进化式自我改进系统。使用 DSPy + GEPA 优化技能、提示词、工具描述和代码。
安装：git clone → pip install -e .（Hermes venv 中）
模块：evolution/
🧰 wiki 知识库补充命令
以下 wiki 命令也已集成到系统中：


操作

命令

自然语言触发

查询知识库

/wiki-query

问 wiki / 查知识库 / 关于...

健康检查

/wiki-lint

扫描 wiki / lint 检查 / 完整性检查
❌ 已移除
W&B（Weights & Biases） — 已从系统中卸载
master-skill — 仓库 404，已放弃
camofox-browser — 无 Windows 二进制，已放弃
📊 系统当前状态


组件

版本/状态

Hermes Agent

v0.14.0

Provider

deepseek-v4-flash

Context Engine

LCM (hermes-lcm v0.12.0)

Memory

Mnemosyne v3.1.0

MCP Servers

3/3 在线（minimax, minimax-multimodal, twozero_td）

Cron Jobs

2 活跃（每日 01:00 归档, 08:00 知识库整理）

Total Skills

91

GPU

GTX 1060 3GB

磁盘

C: 239G (96G 剩余)
🆕 更新 (2026-05-29)
💬 LCM 斜杠命令 — /lcm
LCM 上下文引擎现在支持手动控制：
启用方法：

hermes config set LCM_ENABLE_SLASH_COMMAND 1
# 或在 ~/.hermes/.env 中添加：
# LCM_ENABLE_SLASH_COMMAND=1
# 修改后重启生效
可用命令：


命令

作用

/lcm 或 /lcm status

查看当前 LCM 运行时/会话状态

/lcm doctor

运行只读 LCM 健康检查

/lcm rotate apply

手动触发压缩（备份先行，推进 lifecycle frontier）

/lcm backup

手动备份 LCM 数据库

/lcm help

查看所有命令
压缩机制：
LCM 的压缩是全自动的，背后的工作原理：
leaf_chunk_tokens (默认 24K) — tail 外的 backlog 超过此值时自动创建摘要 DAG node
context_threshold (默认 50%) — 上下文达到总容量 50% 时强制压缩
/lcm rotate apply 手动推进 current_frontier_store_id，标记旧消息不再重播到上下文
当前 session 示例：310 条消息约 50K tokens，远小于 50 万阈值，因此自动判定为 noop。等待 backlog 积累到 24K tokens 后自动触发压缩。
🧠 记忆整理 — memory-organizer
新增技能 /memory-organizer，每日定时整理持久记忆：
流程：
扫描 Mnemosyne 工作记忆
合并重复条目（FTS5 相似度匹配）
删除过期/冲突信息
补充遗漏的关键事实
调整重要性权重
cron： 每日 08:30
⏰ 定时任务全景更新
系统现在运行 3 个活跃 cron 定时任务：

01:00  每日归档       → archiver.py → 删>30天session页 → prune 14d state
08:00  知识库整理     → wiki-lint + archive
08:30  记忆整理       → memory-organizer（合并重复、删过期、精简条目）
归档清理规则：
wiki/entities/hermes-session-*.md > 30 天 → 自动删除（但 session 中提炼的知识已在 concepts/methods/comparisons 中永久保留）
Hermes SQLite state > 14 天 → hermes sessions prune --older-than 14 自动清理
📊 系统状态（2026-05-29 更新）


组件

状态

Hermes Agent

v0.14.0 ✓

Provider

deepseek-v4-flash ✓

Context Engine

LCM (hermes-lcm v0.12.0) ✓

Memory

Mnemosyne v3.1.0（6 working, 26 memoria facts）

MCP

3/3 在线 ✓

Skills

92 个 ✓

Cron

3 活跃（01:00, 08:00, 08:30）✓

GPU

GTX 1060 3GB ✓

磁盘

C: 239G（96G 剩余）✓

rtk-rewrite

已激活（entry-point plugin）✓

SkillClaw

:30000 运行中（PID 18108） ✓

self-evolution

GEPA 模块 ✓

hermes-dojo

已安装 ✓

memory-organizer

已安装 ✓（新增）
系统状态更新（2026-05-29）
self-evolution 已重装：hermes-agent-self-evolution v0.1.0，GEPA 进化引擎就绪（Hermes venv 中 pip install -e）。
每日定时任务全景更新

01:00  每日归档       → archiver.py → 删>30天session页 → prune 14d state
08:00  知识库整理     → wiki-lint + archive
08:15  Dojo 自我改进  → monitor.py → 修复弱点 → tracker → reporter
08:30  记忆整理       → memory-maintenance → 合并重复、删过期
新增 Dojo 每日自我改进（08:15）：


阶段

操作

1. Analyze

monitor.py --json 扫描近 7 天会话

2. Improve

对 top 3 弱点 patch skill / create skill

3. Track

tracker.py save 记录指标历史

4. Report

reporter.py 生成改进报告并推送
🤖 编码与工作流

/hermes-workflow
Hermes 执行工作流。v4.4.0。P0-P4 工作流 + Agent 实际行为模式 — 工具决策树（22 行速查表）、C1-C6 一致性验证、13 个固定工作流模式、Harness Engineering 深度融合（Harnessability/5 张力/CDLA/Spec-as-Product/3 监管维度/Ralph Loop/Builder-Validator/Agent 5模式）。18 个实际陷阱。姐妹技能：/ai-harness-exploration。

/ai-harness-exploration
AI 工具/文章探勘方法论。v6.0.0。6 步探勘法（Analyze→Extract→Formalize→Deliver→Verify→Debrief）+ 四路并发搜索引擎（DuckDuckGo + tavily-search1 + tavily-search2 + mcp_minimax 同时开火）。6 种入口模式（快速/全量/延续/Meta/自测试/默认）。50+ 次迭代优化，10 条陷阱。姐妹技能：/hermes-workflow。

🆕 更新 (2026-05-29)
核心技能更新：hermes-workflow + ai-harness-exploration


技能

版本

更新内容

hermes-workflow

v3.0.0 → v4.4.0

Harness Engineering 深度融合（11 概念）、Agent 5 模式映射、C1-C6 一致性矩阵、Ralph Loop Exit Code 2、Builder-Validator 双代理、Agentic MCP 工作流、OpenClaw 集成、13 个工作流模式、18 个陷阱

ai-harness-exploration

v3.0.0 → v6.0.0

回退链→四路并发（major bump）、3 层并行搜索策略、3 种入口模式变成 6 种、10 条陷阱、50+ 次迭代优化
版本演化：两个技能从独立开发到深度融合，hermes-workflow 吸收 Harness Engineering 全部核心概念，ai-harness-exploration 从 7 引擎回退链升级为四路并发同时开火。
wiki 知识库更新


操作

内容

方法页更新

methods/hermes-workflow-and-exploration.md — 从 v3.0.0 同步到 v4.4.0/v6.0.0，增到 100+ 行

概念页新建

concepts/harness-engineering-deep-study.md — 11 核心概念全景

索引更新

index.md — 新增 2 条索引条目
🆕 更新 (2026-05-30)
Kanban 全面优化 — 5 路并发 + 上下文治理
核心变更


旧

新

自定义 deepseek-m2.7-orchestrator skill + 6 个手工维护 profile

Hermes 内置 Kanban 原生调度

Worker 角色分工（搜索/编码/写作/分析/审查）

5 个 Worker 全能通用型（搜编写析审全能）

load_all: true（加载 90+ 技能）

skills.load: [ai-harness-exploration, hermes-workflow]（精确 2 个）

Worker 443 认证失败

Worker .env 同步 + Gateway 重启 = 全部正常

sessions.auto_prune=false, retention=90 天

auto_prune=true, retention=30 天

无 LCM → 上下文膨胀

Worker 全部启用 LCM stateless 模式

34 个空工作区 + 57 个日志积压

每日 Kanban GC (02:00) 自动清理
Worker 配置

# 5 个 minimax-worker1~5
# MiniMax M2.7（会员无限 token），全能通用型
# Round-Robin 轮转分配
# 默认加载: ai-harness-exploration + hermes-workflow
# 记忆只读（Session scope，不污染编排器）
定时任务全景（7 个活跃）


时间

任务

说明

01:00

每日归档

wiki-archive → 删 >30 天 session 页 → prune 14d state

02:00

Kanban GC 🆕

清理 workspace + 事件 + 日志

07:30

飞书文档流水线

lark-cli → wiki-ingest → wiki-archive

08:00

知识库整理

wiki-lint + wiki-archive

08:15

Dojo 分析+改进+报告

技能缺陷检测 + 自动修复

08:30

记忆整理

memory-maintenance

08:45

LCM 碎片整理 🆕

每天运行 (old: 周三+周日)
Kanban 使用示例

# 5 路并行搜索
kanban create "🔍 搜索A" --assignee worker1 --workspace "dir:持久路径"
kanban create "🔍 搜索B" --assignee worker2
kanban create "💻 编码C" --assignee worker3
kanban create "📊 分析D" --assignee worker4 --parent <A_id> --parent <B_id>
kanban create "📝 报告E" --assignee worker5 --parent <C_id> --parent <D_id>
已知陷阱
标题不要用冒号（swarm 解析为 skill 分隔符）
不用 auto_decompose: true（与 decompose CLI 冲突）
使用 dir: 持久 workspace 传文件，scratch 会被 GC 清空
Worker 401 → 重启 Gateway
相关技能


技能

版本

kanban-orchestrator

v5.2.0（编排指挥）

kanban-worker

v3.1.0（Worker 执行）
🆕 更新 (2026-05-30)
🦶 Footer 系统重建
运行时页脚（runtime_footer）从 3 字段扩展到 6 字段自动适配：

deepseek-v4-flash · 14% · 136K/1M · 27.7s · 5次


字段

说明

model

模型名（自动适配 flash/pro/minimax）

context_pct

上下文占比

context_k

K数/1M

turn_time

响应耗时

api_calls

调用次数

total_tokens

总 token（有数据才显示）
修复陷阱： Python .pyc 缓存导致 patch 不生效——必须清理 gateway/__pycache__/ 再重启。
🧠 记忆上限提升


存储

旧上限

新上限

优化后

记忆 (Memory)

8,000

15,000

63% 5,049 (15条)

画像 (User)

5,000

10,000

42% 2,117 (12条)
🧰 CLI-Anything — 深度集成
cli-anything-methodology v1.6.0 — 基于 HKUDS/CLI-Anything (40.6K⭐) 的深度方法论技能。
已实测验证：
minimax CLI ✅ 全链跑通（pip install -> --help -> --json -> REPL）
browser CLI ✅ CLI 安装成功（需 DOMShell 扩展）
obsidian CLI ✅ 完整集成（见下文）
📝 Obsidian CLI 集成（本机已验证）
状态： 已安装并测试通过

cli-anything-obsidian vault list              # 列出文件
cli-anything-obsidian vault read index.md     # 读笔记
cli-anything-obsidian --json server status    # 服务状态


组件

版本

Obsidian

1.12.7

Local REST API 插件

4.1.2

cli-anything-obsidian

1.1.0

Vault

C:\Users\Administrator\wiki (80+ pages)
修复： search query 在 API v4.x 中 DQL 已废弃，已修复为降级到 /search/simple/。
📊 系统状态更新


组件

状态

Hermes Agent

v0.14.0

Provider

deepseek-v4-flash (编) + minimax M2.7 (Worker)

Context Engine

LCM v0.12.0

Memory

Mnemosyne v3.1.0 (15K限制)

MCP

4/4 在线: minimax, minimax-multimodal, twozero_td, tavily-search

Skills

112个

Kanban Workers

5个 minimax-worker1~5 (通用型, Round-Robin)

Cron

7活跃

Wiki 知识库

84页面

Disk C:

96G 剩余
🔧 已知陷阱补充
config.yaml 写 list 用 yaml.dump - hermes config set 会把数组写成字符串而非 YAML 列表
pyc 缓存 - 改 gateway 代码后必须清 pycache/ 再重启
Kanban dispatcher 重启丢失 - 设 kanban.default_assignee=minimax-worker1 自动恢复
Worker .env 不同步 - 不能继承主 env，必须 cp 复制到每个 profile
