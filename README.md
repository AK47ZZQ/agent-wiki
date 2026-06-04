# Hermes + Obsidian 知识图谱 Wiki

基于 gusibi/obsidian-llm-wiki 架构 + Karpathy LLM Wiki 模式。

## 快速开始
1. 在 Obsidian 中打开 `C:\Users\Administrator\hermes-all\wiki` 作为 vault
2. Graph View 可视化知识网络
3. 运行 `hermes-workflow-archiver.py` 归档 session
4. 用 `/ingest` 摄入新资料

## 目录结构（2026-06-04 整理后）
- `raw/work/` — 源文件（只读）
  - 1 份 `hermes命令大全v2-...-1780136199.md`
- `wiki/` — Agent 维护的知识库
  - `concepts/` — 16 个概念/主题页
  - `entities/` — 14 个实体/技能/工具
  - `methods/` — 6 个方法论
  - `notes/` — 4 个部署/实战记录
  - `comparisons/` — 2 个对比分析
  - `references/` — Hermes 命令大全提炼版
  - `indexes/` — 主题子索引
  - `AGENTS.md` — Hermes 4-Tier 架构
  - `_archive/sessions/` — 25 个归档会话日志
- `index.md` — 主索引（25 个有效页面）
- `log.md` — 操作日志（含历史）
- `CLAUDE.md` — Wiki Schema 规范

## 2026-06-04 整理要点
- 删除 26 个 skill 自动生成存根
- 合并 14 个薄 concept → `[[concepts/full-stack-ecosystem]]`
- 归档 25 个 session 日志
- 清理 raw/work/ 重复 + 测试文件
- 补建/更新 index.md、log.md、README.md

详见 [[log|log.md]] 2026-06-04 记录。