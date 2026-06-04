# _drafts — 3rd Notebook Sync Test (2026-06-04 18:42)

> **状态**: _drafts (按 README § 写入协议"拒绝内容 → scratchpad/_drafts/")
> **原因**: 3rd 写了一份"笔记本用户偏好深度分析"草稿, 内容**边界** (混合 session 记录 + 用户偏好 + 内部吐槽) — 按 CLAUDE.md § 2.5 反模式"纯 session 日志" + 4.0 申请协议, 3rd **不发布**, 暂存到 _drafts, 等用户裁决.

## 草稿内容 (暂不发布)

### 笔记本用户偏好 (草稿)

(以下内容**不发布**, 仅做 3rd 内部"边界判定"演示)

- 用户偏好 VSCode + MSYS bash, 不用 PowerShell
- 飞书是主对话界面
- 写代码优先 TDD, 但不僵化
- 中文为主, 英文术语保留
- 喜欢结构化报告 + 表格 + 真实证据
- 喜欢"动手" 不喜欢"我猜"
- 被打断时耐心等, 不连续追问
- 自检类任务要给"状态表 + 风险清单 + 一次性修复建议"

### Session 吐槽 (不发布)

- 飞书 thinking 块渲染 bug 经常出现, 用户得用 [Replying to: ...] 提示
- 飞书消息"AB" 可能是我 thinking 尾巴被错误渲染
- 用户多次 push "继续" 信号, 实际是"继续深挖", 不是"确认完成"
- 用户说"ABCD 全做", 实际是 "按顺序, 全做, 不要跳", 不是 "做 ABC 不做 D"

### 内部笔记 (不发布)

- 笔记本路径 E:\hermes\wiki\ 跟 main-claude 的 C:\Users\Administrator\hermes-all\wiki\ 不同, 别混
- 3rd 的 git user 是 [email protected], 不跟 wiki-keeper 冲突
- 3rd 的 Co-authored-by 头必须, 否则没标识

## 为什么 _drafts (不正式发布)

按 CLAUDE.md § 2.5 反模式:
- ❌ 纯 session 日志 → 归档到 `wiki/_archive/sessions/`
- ❌ 重复内容 → 先 Grep 查重
- ❌ 没有 wikilink 的孤岛 → 至少 2 出链

本草稿**有 3 段混合内容** (用户偏好 / 吐槽 / 笔记), 不属于任何单一 category. 强发会:
1. 把 session 记录 (3rd 跟用户的对话) 混入 wiki → 污染
2. 把"内部吐槽" (3rd 视角) 当作 wiki 知识 → 错位
3. 跟 `notes/hermes-selfcheck-2026-06-04.md` 内容重复

## 建议处置

- **方案 A**: 删掉本文件, 不留 (3rd 内部)
- **方案 B**: 写一份精炼的 `notes/hermes-3rd-user-preferences-2026-06-04.md`, 只含"笔记本用户偏好"那段, 加 frontmatter + wikilink
- **方案 C**: 等用户说"把草稿变成 wiki 页" 才动

**3rd 默认选 C** (等用户裁决).

## TTL

`scratchpad/_drafts/` 按 README 默认 1 周 (7 天). 本草稿 2026-06-11 自动过期. 到期未升级到正式 wiki → 删除.

## 关联 (不发布, 仅 3rd 内部参考)

- 笔记本协作者: [[agents/hermes-3rd]]
- 写入协议: README § 写入协议
- 反模式: CLAUDE.md § 2.5
- 申请协议: ai-harness-exploration § 4.0
