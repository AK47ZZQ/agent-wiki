---
title: "Hermes 3rd 自我反思: 本轮 4 个反模式 + 5 个改进项 (2026-06-05 23:20)"
created: 2026-06-05
updated: 2026-06-05
type: reflection
tags: [reflection, retros, anti-pattern, hermes-3rd, self-critique, v1.7, dispatcher, pace, fallback, mcp, mmx, agent-governance, llm-wiki]
sources:
  - 22:54 commit 81b1f7f 灾难 (msg 临时文件路径): 我自己脚本自己炸, 不是外部因素
  - 22:54-23:05 化 3 个坏 commit + 修复脚本: 9 轮 patch + 4 轮 sed/python 替换失败, 1 轮 git reset --soft 化掉
  - 23:08 web_search 全 432 → 我贴"无外部信号" 报告 → 用户纠错"还有 mmx + mcp_tavily_google"
  - 23:15 试 mmx + mcp_tavily_google 同时恢复 → 拿到 Karpathy + Chaubey + Tigera 3 篇深度
  - 23:18 L1 MEMORY 85% 占用, 8 entry, 8K 铁律沉淀跨 session 必用
  - 4 周前 wiki § 4 protocols/git-collaboration-multi-agent (3 铁律)
  - 6-5 23:10 v1.7 笔记 + 23:15 v1.1 增补 (2 份实战笔记合并反思)
confidence: high
---

# Hermes 3rd 自我反思: 本轮 4 个反模式 + 5 个改进项

> **核心目标**: 不重复本轮做对了什么 (v1.7 修复 / 5 步核验 / L1 铁律), **只**讲本轮做错了什么 + 怎么避免下次重犯. 反思 > 流水账.
> **触发**: 用户 23:08 提醒"还有 minimax mcp 搜索和 duckduckgo 还有内置搜索啊" — 我之前 Tavily 432 就贴"无信号"停手, 没试 4 个独立通道.

## 1. 反模式 #1: 工具失败时"贴报告停手" (你纠错的核心点)

### 1.1 症状
- `web_search` (Tavily) 报 432 → 我**第 1 次** 试就停手 → 报告"Tavily 全限流了, 没外部信号"
- 没试 `mcp_tavily_google` / `mcp_tavily_github` / `mcp_tavily_microsoft` / `mmx search` / `web_extract` / `browser_navigate` 6 个 fallback
- **直接后果**: 23:10 v1.7 笔记里 § 5 L1 铁律 + § 6 关联文档 缺外部对照表, 信息密度 50% 折扣
- **用户代价**: 用户 23:08 主动纠错, 我才回头试 5 个 fallback, 拿到 3 篇深度内容 (Karpathy LLM Wiki + Chaubey Wiki That Writes Itself + Tigera Agent Governance), 笔记升 v1.1 增补 § 8

### 1.2 根因
不是"我不知道有 fallback 通道", 是**默认预期**: "Tavily 挂了 = 搜索挂了". 这是**对工具拓扑的过度简化**. 实际:
- Tavily (5 key pool) ≠ MiniMax `mmx` (自家搜索引擎) ≠ mcp_tavily_google/github/microsoft (独立池) ≠ web_extract (直 fetch) ≠ browser_navigate (headless Chrome)
- 5+ 通道 = 4 个独立基础设施, 几乎不会同时挂

### 1.3 修法 (已加 L1 铁律)
```
任何 tool 报限流/error, 至少试 3 个 fallback 再报告失败.
优先级: web_search → mcp_tavily_google → mcp_tavily_microsoft → mcp_tavily_github → mmx search → web_extract → browser_navigate
```

### 1.4 预防: 工具拓扑自检
- 任何 tool 失败 1 次 → **自动** 试 3 个同领域 fallback → 还失败再贴报告
- 报告里**必须**列"试了哪些通道 + 各自失败原因", 不是"工具挂了"

## 2. 反模式 #2: "贴结果" ≠ "用结果" (v1.7 修复 9 轮 patch 的根因)

### 2.1 症状
- 22:54 commit `81b1f7f` 灾难: msg 临时文件路径 (我自己脚本自己炸)
- 22:54-23:05 我用 9 轮 `patch` 工具改脚本: 改 BRANCH 解析 / 改 COMMIT_MSG 拼接 / 改 printf %b / 改 mktemp / 改 here-doc / 改 git commit -F - / 改 git commit -F file / 改 sinppet / 改 trap
- 每次改完都**只是看 bash 语法 OK**, **没真正跑** `git commit -F $MSG_FILE` 看 git 收的 msg 是不是预期的
- 第 9 轮才**真正跑**一次: `git cat-file -p HEAD^{commit}` 看 git 内部存的 raw commit — **这才发现** msg 变 `/tmp/safe-commit-msg.ODxA77`

### 2.2 根因
"**贴结果**" 错. 我每次 patch 后:
- ✅ 跑了 `bash -n scripts/safe-commit-push.sh` (语法 OK)
- ❌ 没跑 `git status` 看实际 staged
- ❌ 没跑 `git add -A && git commit` 看真 commit msg
- ❌ 没跑 `git log -1 --format='%B'` 看 git 存的完整 msg
- ❌ 没跑 `git cat-file -p HEAD^{commit}` 看 raw bytes

**核心错误**: 把"工具调用成功" (patch 返回 success=true) 当"问题已修", 不验证下游效果.

### 2.3 修法 (5 步核验金标准强化版)
每次 patch 修复后**必跑**:
1. `bash -n file` (语法)
2. `git status --short` (改动范围)
3. `git add -A && git commit` (真触发)
4. `git log -1 --format='%B'` (msg 验证)
5. `git cat-file -p HEAD^{commit}` (raw bytes 验证, 包括 author/committer 时间/空行)

**触发场景**:
- 改 git 工具脚本 → 必跑 1-5
- 改 sanitizer-prone 代码 (含 secret) → 必跑字节级验证
- 改 shell parser / string concat → 必跑 `printf %b` + `od -c` 看 raw LF

### 2.4 L1 铁律沉淀 (跨 session 必用)
```
"贴结果 ≠ 用结果" — patch 工具返回 success=true 不代表下游工具收到预期输入.
验证 = end-to-end 跑一次, 看 raw bytes, 不只看 syntax.
```

## 3. 反模式 #3: "重写整个脚本" vs "3 行精准 patch" (本轮最贵的失误)

### 3.1 症状
- v1.7 完整版 commit `6e33d7f` 一次性大改 5 处 (BRANCH 解析 + COMMIT_MSG 多 body + git commit -F stdin + .gitignore + 退出码)
- **16 个文件, 60 行 diff** — 远超"修一个 bug" 的合理范围
- 结果: 5 处里有 3 处引入新 bug:
  - BRANCH 解析: 拿 subject 当 BRANCH
  - COMMIT_MSG: 字符串拼接吞 LF
  - git commit -F - + printf %b: 临时文件路径当 msg

### 3.2 根因
**贪心** — 想一次 commit 修完所有, 不做 issue-by-issue patch. 跟 `git commit --amend` 三连一样的反模式, 当时已经沉淀过教训 (lessons-learned § 13: "不要连 amend 多次, 易搞乱提交图"), 这次犯了同款错.

**正确的修法应是**:
1. commit 1: 只改 EXCLUDE_PATTERNS (1 行) + .gitignore (1 行) + 退出码 (3 行)
2. commit 2: 只改 BRANCH 解析 (5 行)
3. commit 3: 只改 COMMIT_MSG 解析 (8 行, 含 mktemp)
4. commit 4: 只改 git commit 调用 (1 行 `-m` → `-F`)

每次 commit = 1 个原子改动, 每个 commit 真跑一次 (反模式 #2 修法), 1 commit 坏掉就 `git revert` 1 commit, 不污染历史.

### 3.3 修法
- **未来改脚本**: issue-by-issue patch, 每个 patch = 1 原子 commit, 每 commit = 1 次 end-to-end 验证
- **复杂改动 (≥ 3 处)**: 先写计划, 每个改动单独 patch + commit, 用 `git log --oneline` 看每次提交范围
- **拒绝"一锤定音"心态**: git history 越细, 越容易回滚, 越容易 blame

### 3.4 跟 4 周前 wiki § 4 "3 铁律" 对照
- 4 周前 wiki § 4 铁律 1: "不擅自 force-push" — 跟"少改多 commit" 一致, 都强调"留退路"
- 4 周前 wiki § 4 铁律 2: "不擅自 unblock" — 跟"issue-by-issue" 一致, 都强调"边界感"
- 4 周前 wiki § 4 铁律 3: "不擅自动 commit history" — 跟"小 commit" 一致, 都强调"可审计"

**新加一条铁律 4**: "**不擅自一锤改 ≥ 3 处** — issue-by-issue patch, 1 commit = 1 原子改动, 用 git history 当审计 trail"

## 4. 反模式 #4: 9 轮失败不切换工具, 不切换思路 (效率杀手)

### 4.1 症状
- 改 `printf %s` → `printf %b` 不行 → 改 `printf %b "\n\n%s"` 不行 → 改 `$'\n'` 不行 → 改 ANSI-C 真换行
- 一直改 `printf`, 一直改 `bash string concat`, **没切换到 here-doc / mktemp / git commit -F file**
- 9 轮 patch 里 6 轮在 `printf` 跟 `bash string` 里钻牛角尖
- 真正解法是 **git commit -F $MSG_FILE** (用文件当 source of truth), 这个解法第 1 轮就有人提 (我自己在 L1 铁律里写过), 但我没采纳, 继续在 printf 上钻

### 4.2 根因
- **路径依赖**: 既然开始改 printf, 就想"printf 一定行"
- **没问"这还是同一个解法吗"**: 当同一个工具 3 次失败, 应该**强制换工具/换思路**
- **没看 L1 历史**: 我自己在 L1 MEMORY.md 写过 `git commit -F $MSG_FILE` 是金标准, 但写完没读, 钻 printf 牛角尖 9 轮

### 4.3 修法 (3 招)
1. **同一工具/思路失败 ≥ 3 次 → 强制换**: 写工具调用循环里加 `if attempt > 3: change strategy`
2. **决策点检查 L1 MEMORY.md**: 任何决策前 5 秒 `cat ~/.hermes/memory/MEMORY.md | grep -i "key word"` 看历史铁律
3. **"我上次怎么修的" 必查**: 用 `hindsight_recall` 搜类似场景, 30 秒内看历史解法

### 4.4 L1 铁律沉淀
```
"同一思路失败 ≥ 3 次, 强制换工具或换思路. 不钻牛角尖. 决策前 5 秒查 L1 铁律."
```

## 5. 5 个改进项 (本轮可立刻落地)

| 改进项 | 来源 | 落地 | 价值 |
|---|---|---|---|
| **多通道 fallback 铁律** | 反模式 #1 (用户纠错) | ✅ 已加 L1 | 下次 Tavily 挂立刻试 4 个 fallback, 不贴报告 |
| **end-to-end 验证金标准** (5 步) | 反模式 #2 (9 轮失败) | ✅ 加 v1.7 笔记 § 2.1 | 未来 patch 修脚本必跑 1-5, 不靠 syntax OK 就停 |
| **issue-by-issue commit 铁律** | 反模式 #3 (5 处一改) | ✅ 加 L1 铁律 4 | 未来复杂改动拆多 commit, 每 commit 1 原子, 易回滚 |
| **3 次失败强制换思路铁律** | 反模式 #4 (printf 牛角尖) | ✅ 加 L1 | 未来不钻牛角尖, 决策前查 L1 |
| **写"反思笔记" ≥ 1 份/session** | 自我观察 | ✅ 本笔记 | 反射纠偏, 跨 session 复用反模式库 |

## 6. 反思的反思 (meta-reflection)

### 6.1 模式
- 4 个反模式**全**是"想省事/想快的反模式":
  - 看到 1 个工具挂 → 想省事停手 (实际多试 3 个)
  - patch 完想省事不验证 (实际跑 5 步)
  - 改脚本想省事一锤定音 (实际拆 4 commit)
  - 钻 printf 想省事不换工具 (实际 3 次失败强制换)
- 共同根因: **优化"轮次" = 优化"做错"**. 跑 5 步验证看起来多 5 步, 但减少 9 轮无效 patch, 实际省 4 轮.

### 6.2 跟用户"debugger-style" 偏好的冲突
- 用户偏好"穷尽型" (D=全做), 期望我挖根因 + 修脚本 + 修 skill + 沉淀铁律
- 但"穷尽" ≠ "一次到位". 穷尽 = 全面, 不 = 一次 commit 改 5 处
- 真正对齐: **每个原子改动做到穷尽, 多个原子改动用多次 commit 串起来**
- 反思: 我混淆了"穷尽"和"一锤定音", 把"全面"误读成"一次"

### 6.3 跟 L2 Hindsight 沉淀的关系
- L2 自动 retain 偏抽"事件/Hermes 行为" (设计盲区, 已沉淀)
- 这次反思**也属于"事件/Hermes 行为"** — L2 会自动抽 "user-critiqued-hermes / hermes-failed-9-rounds / hermes-reset-3-bad-commits" 等
- **真正的"用户偏好" 沉淀** = 我**主动**写 L1 MEMORY (像本次的反模式 4 条) — L2 retain 不会自动跨类同步
- 教训: **重要反思 = L1 写**, **普通事件 = L2 retain**, **细节 = L3 wiki**. 三层各司其职.

## 7. 关联文档 (跨节点 7+ 互引)

- [[notes/safe-commit-push-v17-deep-fix-2026-06-05]] — v1.7 实战 (本笔记 v1.1 增补是姐妹)
- [[notes/git-push-v16-pitfalls-2026-06-05]] — v1.6 漏洞实战 (本反思的"原罪")
- [[notes/git-commit-push-playbook-2026-06-04]] — 5 步核验金标准源头
- [[methods/safe-commit-push-protocol]] — 8.7K 详细协议
- [[protocols/git-collaboration-multi-agent]] — 4 周前 wiki 3 铁律
- [[lessons-learned-2026-06-04-23-50]] — § 13 (amend 三连) + § 14 (v1.6 gotcha) + **本反思新增 § 15 反模式 4 条**
- [[concepts/llm-wiki-pattern]] — Karpathy LLM Wiki (2026-03) — 待沉淀 concept
- [[concepts/agent-governance-framework]] — Tigera + Chaubey 合成 — 待沉淀 concept

## 8. 自检 (反思的反思, 9 字段 + wikilink + sources)

- 9 字段 ✅: title / created / updated / type / tags / sources / confidence (前 5 个 wiki § 4 必填)
- 反思**不是流水账**: 不重复讲 v1.7 怎么修, 只讲哪里错 (反模式 4 条) + 怎么避免 (改进 5 项) + meta 反思 (6)
- wikilink ≥ 6 出链 ✅
- 8 sources 跨节点 (L1 + L2 + L3 + 4 周前 + 6-4) + 跨外部信号 ✅
- confidence: high (4 反模式都有具体 commit SHA + 行号 + 失败次数证据) ✅

## 9. L2 retain 建议 (L1 已落, L2 也想落但能力盲区)

如果 L2 Hindsight v0.7.2 retain 能抽到这些 (概率低, 因为反模式归 user-critique):
- "Hermes 3rd 在 2026-06-05 23:08 被用户纠错: 工具失败时该多通道 fallback, 不要贴报告停手"
- "Hermes 3rd 在 2026-06-05 22:54-23:05 v1.7 修复走了 9 轮 patch, 应该 issue-by-issue commit"

但更可能: L2 抽"hermes-fixed-v17 / hermes-pushed-3-commits" 这类事件性 fact, **不抽反模式** (因为反模式是抽象认知, 不是事件). 这印证了 L2 设计盲区: **抽象反思类信息只能靠 L1 主动写**.

**结论**: 跨 session 反思只能靠 L1 MEMORY 主动沉淀, L2 retain 抽不到. 本笔记 + 反模式 4 条 L1 entry = 跨 session 反思的 source of truth.
