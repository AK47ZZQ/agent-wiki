---
title: Hermes Dojo Improve — Yonkoo11/hermes-dojo 5 阶段闭环 + 5 大可借鉴设计点
created: 2026-06-06
updated: 2026-06-06
type: note
tags: [dojo, self-evolution, hermes-dojo, yonkoo11, metrics-tracker, learning-curve, failure-patterns, 3rd-notebook]
source: dojo-improve-2026-06
---

# Hermes Dojo Improve — Yonkoo11/hermes-dojo 5 阶段闭环 + 5 大可借鉴设计点

> 3rd 笔记本实战 (2026-06-06, "dojo improve" 任务). 静态读 + 5 脚本分析 + 5 大可借鉴设计点 + Z3rd 集成方案.

## TL;DR

- **项目**: `https://github.com/Yonkoo11/hermes-dojo` (Yonkoo11, beta, Hermes Agent Hackathon March 2026 产物). 13 commits, master 分支. 13 个核心文件: `SKILL.md` orchestrator + `install.sh` + 5 个 .py 脚本 (monitor / analyzer / fixer / reporter / tracker) + `references/failure_patterns.md` + `data/metrics.json` + `seed_demo_data.py` + `demo.py`
- **5 阶段闭环**: `measure (monitor) → identify weakness (analyzer) → evolve (fixer) → measure again (reporter) → report (tracker learning curve)`. 对应 5 个 `/dojo` 命令: `analyze / improve / report / history / auto`
- **5 大可借鉴设计点** (vs Z3rd 现状 `hermes-self-evolution` mental_model v0.3):
  1. **metrics.json 90 天 rolling 窗口** — tracker.py 用 atomic write (tmp + rename) 防 corruption
  2. **priority_score 算法** — `error_rate × total × 10`, 排序 + 去重
  3. **root-cause 5 类 not-fixable** — infra / auth / rate_limit / context_unavailable / security_policy (5 类直接报"不是 skill 问题")
  4. **sparkline trend 趋势** — `▁▂▃▄▅▆▇█` Unicode blocks 8 段, 30 天窗口
  5. **failure_patterns.md 决策表** — 5+5+4+5 错误模式 + 可执行 fix 模板
- **Z3rd 集成方案**: 不直接装 hermes-dojo (sandbox 无 state.db + Nous hermes-agent fork 冲突), 把 5 大设计点**写进 hermes-self-evolution mental_model v0.4** (4 反模式 + 5 大 dojo 改进 → 总 9 节)

## 1. 背景: 为什么 explore hermes-dojo

**触发**: 用户原话 "dojo improve". 已知线索:
- L3 wiki `concepts/awesome-hermes-agent-ecosystem-2026.md` L55: `hermes-dojo | Yonkoo11 | 自我改进系统, 性能监控+自动迭代 | beta`
- L3 wiki `agents/main-claude.md` L137: `hermes-dojo — 持续自改进(分析过去 session 自动创建 skill)`
- L3 wiki `agents/ai-harness-exploration-SKILL.md` L2134: `SkillClaw 和 hermes-dojo 的互补关系 (dojo 识别问题 → self-evolution 解决)`

**Z3rd 现状 (mental_model `hermes-self-evolution` v0.3, 4903 chars)**:
- 5 sections: 反模式/待办/工作流/自检/沉淀规则
- DSPy-Hindsight-gbrain 三层验证 (笔记 `dspy-self-evolution-2026-06-06.md` 详述)
- **缺**: metrics 历史 (无 tracker.py 等价), priority 排序算法, root-cause 分类, trend 趋势图, failure_patterns 决策表

→ hermes-dojo 正好补这 5 块, **借鉴 > 直接装** (避免 hermes-agent fork 冲突)

## 2. 项目架构 (静态读,无 git clone)

> 直连 GitHub 不通 (`Recv failure: Connection was reset`), 改用 `web_extract` + `tavily_extract` 读 master 分支 (注意: 是 master, 不是 main)

### 2.1 目录结构 (13 文件)

```
hermes-dojo/
├── SKILL.md                      # orchestrator (Hermes skill format)
├── install.sh                    # 自动装到 ~/.hermes/skills/hermes-dojo/
├── scripts/
│   ├── monitor.py                # 读 state.db, 算 metrics
│   ├── analyzer.py               # 分类 + 推荐
│   ├── fixer.py                  # patch + create + evolve (404 on master, 可能在别的分支)
│   ├── reporter.py               # CLI / Telegram 双格式
│   ├── tracker.py                # metrics.json 持久化 + learning curve
│   ├── seed_demo_data.py         # 造 demo 数据
│   └── demo.py                   # 端到端 demo
├── references/
│   └── failure_patterns.md       # 19 类错误模式 + fix 模板
└── data/
    └── metrics.json              # 历史 metrics (90 天 rolling)
```

### 2.2 5 阶段闭环 (核心)

| # | 阶段 | 脚本 | 输入 | 输出 |
|---|---|---|---|---|
| 1 | **Measure** | `monitor.py` | `state.db` (Hermes session SQLite) | `monitor_data: { sessions_analyzed, total_tool_calls, overall_success_rate, user_corrections, weakest_tools, skill_gaps, retry_patterns }` |
| 2 | **Identify** | `analyzer.py` | monitor_data | `recs[]: { action: patch/create/evolve/investigate, target, priority, suggested_fix }` |
| 3 | **Fix** | `fixer.py` | recs[] | 调用 `skill_manage` 自动 patch / create / evolve skill |
| 4 | **Report** | `reporter.py` | monitor_data + improvements + history | CLI 60-char 表格 / Telegram Markdown (含 sparkline) |
| 5 | **Track** | `tracker.py` | monitor_data + improvements | `data/metrics.json` (90 天 rolling) + `print_history` 含 sparkline ▁▂▃▄▅▆▇█ |

### 2.3 5 个 /dojo 命令

| Command | What | 触发脚本链 |
|---|---|---|
| `/dojo analyze` | 分析最近 session 找失败 | monitor → analyzer |
| `/dojo improve` | 修最弱 skill + 跑 self-evolution | monitor → analyzer → fixer |
| `/dojo report` | 生成改进报告 | monitor → reporter (+ tracker history) |
| `/dojo history` | 看 learning curve | tracker |
| `/dojo auto` | 设 cron 夜间跑 | 全链 + 早 Telegram 报告 |

## 3. 5 大可借鉴设计点 (核心)

### 3.1 metrics.json 90 天 rolling + atomic write

**dojo 设计** (`tracker.py`):
```python
history = load_metrics()  # 读 data/metrics.json
history.append(snapshot)  # 加新 snapshot
# 90 天 cutoff
cutoff = time.time() - (90 * 86400)
history = [h for h in history if h.get("timestamp", 0) > cutoff]
# atomic write: tmp + rename 防 corruption
tmp_file = METRICS_FILE.with_suffix(".tmp")
with open(tmp_file, "w") as f:
    json.dump(history, f, indent=2)
tmp_file.replace(METRICS_FILE)
```

**Z3rd 现状**: 无 metrics 历史, mental_model 是 in-memory sub-table (重启后从 source_query 重生成, 但无时间序列 trend)

**Z3rd 实施建议**:
- 新建 `E:\hermes\hermes\logs\hermes-self-evolution-metrics.json` (放 logs 而非 ~/.hermes/, 跟 watchdog.log 同目录, 易守护)
- mental_model refresh 时同步写 metrics (date, source_query, content_len, sections_count, refresh_latency_s)
- cron 90 天 cutoff 脚本 (`purge_old_metrics.py`)

### 3.2 priority_score 算法

**dojo 设计** (`analyzer.py _priority_score`):
```python
def _priority_score(tool: dict) -> float:
    error_rate = 1 - (tool["success_rate"] / 100)
    return error_rate * tool["total"] * 10
```

排序 + 去重:
```python
seen = set()
unique = []
for rec in sorted(recommendations, key=lambda x: x["priority"], reverse=True):
    if rec["target"] not in seen:
        seen.add(rec["target"])
        unique.append(rec)
```

**Z3rd 现状**: 反模式触发后, 全靠人工 5 步核验判定严重度, 无算法

**Z3rd 实施建议**:
- DSPy `Predict(priority_score, input_fields=[error_count, success_rate, total, target_type], output_field=priority)` 跑一次
- 落地 mental_model v0.4 加 "priority 算法" 章节

### 3.3 root-cause 5 类 not-fixable 分类

**dojo 设计** (`analyzer.py _classify_error_root_cause`):

| Category | fixable_by_skill | 关键词 |
|---|---|---|
| `infra` | False | "cannot connect", "connection refused", "ECONNREFUSED", "no such host", "DNS", "unreachable" |
| `auth` | False | "unauthorized", "invalid key", "invalid credentials", "auth", "authentication failed", "forbidden", "403" |
| `rate_limit` | False | "rate limit", "429", "throttled", "too many requests" |
| `context_unavailable` | False | "not available in this execution context" |
| `security_policy` | False | "security scan" |
| `missing_parameter` | True | "missing required", "field required", "X is required" (需参数前缀) |
| `unknown` | True | 默认 |

**Z3rd 现状**: AP-1/2/3/5 4 个反模式有"反模式库", 但**没有"什么不是反模式"的白名单**。**L1 铁律 #3** "工具调用效果不符预期, 怀疑顺序固定" 已经暗含这 5 类的判别, 但**没写成 actionable 决策表**

**Z3rd 实施建议**:
- L1 铁律 #3 扩成 8 行决策表 (5 类 not-fixable + 3 类 fixable)
- 反模式库每条加 `root_cause` 字段, 触发时**先分类, 再决定是 skill 改还是用户告知**

### 3.4 sparkline trend + delta%

**dojo 设计** (`tracker.py print_history`):
```python
rates = [h.get("overall_success_rate", 0) for h in history[-10:]]
blocks = " ▁▂▃▄▅▆▇█"
min_r, max_r = min(rates), max(rates)
span = max_r - min_r
if span == 0:
    sparkline = "█" * len(rates)
else:
    sparkline = "".join(
        blocks[min(8, int((r - min_r) / span * 8))] for r in rates
    )
print(f" Sparkline: [{sparkline}]")
```

trend emoji: `📈 delta>0 / 📉 delta<0 / ➡️ delta=0`

**Z3rd 现状**: mental_model content_len 4903 (单点值, 无 trend)

**Z3rd 实施建议**:
- mental_model v0.4 注入时同步输出 sparkline (从 metrics.json 读最近 10 次)
- 每日 cron (`hermes-self-evolution-metrics-cron`) 跑一次 refresh + sparkline 输出
- 跟 4 层数字 heartbeat 同款 (v6.0.1 bat `:tick_log` 已有)

### 3.5 failure_patterns.md 决策表 (5+5+4+5 = 19 类)

**dojo 设计** (`references/failure_patterns.md`):

| Error Pattern | Root Cause | Fix |
|---|---|---|
| **Terminal/Command** (5 类) |||
| "command not found" | Tool/binary not in PATH | Add `which` check before execution, suggest install |
| "permission denied" | File/dir not writable | Check permissions first, suggest `chmod` or `sudo` |
| "no such file or directory" | Path doesn't exist | Validate path exists before operations |
| "syntax error" | Bad shell syntax | Use proper quoting and escaping |
| "killed" / exit code 137 | OOM or timeout | Add memory/time limits, suggest smaller scope |
| **Web/Network** (5 类) |||
| "timeout" / "ETIMEDOUT" | Slow server or network | Add retry with backoff, increase timeout |
| "connection refused" | Service not running | Check if service is up before connecting |
| "rate limit" / 429 | API throttling | Add rate limiting, exponential backoff |
| "404 not found" | Wrong URL | Validate URL format, check for typos |
| "SSL certificate" | Cert issues | Flag to user, don't auto-skip verification |
| **File Operations** (4 类) |||
| "ENOENT" | File not found | Check existence first |
| "EACCES" | Permission denied | Check read/write permissions |
| "EISDIR" | Expected file, got dir | Validate file type before operation |
| "disk full" / "ENOSPC" | No space | Check available space, suggest cleanup |
| **User Correction Signals** (5 类) |||
| "no, I meant..." | Misunderstood intent | Improve skill instructions for disambiguation |
| "wrong file/path" | Path resolution error | Add more context-aware path resolution |
| "try again" | Non-specific failure | Need more error details in skill |
| "that broke" | Side effect caused damage | Add safety checks and dry-run options |
| "undo" / "revert" | Want to roll back | Add undo capability to skill |

**Z3rd 现状**: AP-1/2/3/5 4 个反模式 (5 月以来沉淀) 在 L1 MEMORY.md, 但**没有 fix 模板**。每次触发靠 mental_model 注入 + skill_manage 手动

**Z3rd 实施建议**:
- mental_model v0.4 加 "19 类错误模式 + 决策表" 章节 (复制 dojo 表格 + 加 Z3rd 实战注释)
- 跟 L1 铁律 #3 串起来: 触发反模式 → 查 19 类决策表 → 用 fix 模板 skill_manage

## 4. Z3rd 集成方案 (mental_model v0.4 升级)

### 4.1 为什么 "借鉴 > 直接装"

| 维度 | 直接装 hermes-dojo | 借鉴 5 大设计点 |
|---|---|---|
| **state.db 依赖** | 必须 Nous hermes-agent, 我们用 hermes-agent fork | 无依赖, mental_model 自带 |
| **DSPy GEPA** | 必须装 dspy + 配置 (3 landmines) | 已装, mental_model refresh 已用 ChainOfThought |
| **skill_manage 自动 patch** | 自动改 ~/.hermes/skills/\*\* | 改 E:\hermes\hermes\skills\*\* (hermes-agent fork) |
| **Telegram 报告** | 需配置多平台 channel | 飞书, 已配 |
| **5 PATCH bank config** | 跟 Hindsight 0.7.2 无关, 各自独立 | mental_model refresh 自动对齐 5 PATCH |
| **风险** | 跟 hermes-agent fork 冲突 + 5 PATCH 被覆盖 | 0 风险, mental_model 是 sub-table |

### 4.2 mental_model v0.3 → v0.4 增量

**v0.3 现状** (5 sections, 4903 chars):
1. 反模式
2. 待办
3. 工作流 (DSPy-Hindsight-gbrain)
4. 自检 (5 步核验)
5. 沉淀规则

**v0.4 增量** (新增 4 sections, 预计 7000-8000 chars):
6. **dojo-improvements** — 5 大可借鉴设计点 (本笔记第 3 节精要)
7. **priority-algorithm** — `error_rate × total × 10` + 排序去重
8. **failure-patterns-table** — 19 类错误模式 + fix 模板 (dojo 第 3.5 节复制)
9. **metrics-tracker-spec** — `E:\hermes\hermes\logs\hermes-self-evolution-metrics.json` 90 天 rolling + atomic write

### 4.3 实施步骤 (含 5 步核验)

1. **DSPy 草稿** — ChainOfThought 生成 v0.4 markdown (5000-7000 chars)
2. **POST mental_model** — `POST /v1/default/banks/hermes/mental-models` 含 4 新 section
3. **POST refresh** — 200, 30s 后 verify content_len > 7000
4. **/reflect 验证** — 5 步核验注入 (r.text[:200] 兜底, 不信 r.json())
5. **L1 铁律更新** — MEMORY.md 铁律 #3 扩成 8 行决策表

## 5. 5 步核验 (mental_model v0.4 实施时)

> 参考 `git-push-v16-pitfalls-2026-06-05.md` 5 步核验金标准

| 步 | 验证项 | 期望 |
|---|---|---|
| 1 | GET `mentals?include_content=false` | list 含 `hermes-self-evolution` v0.4 |
| 2 | POST `/refresh` | 200, status="queued" |
| 3 | 30s 后 GET `content` | content_len ≥ 7000 chars |
| 4 | 5 步核验 (新 mental_model 注入 /reflect 上下文) | r.text[:200] 含 "dojo-improvements" / "failure-patterns-table" 关键词 |
| 5 | daemon log: `REFRESH_MENTAL_MODEL_TASK Completed` | 事件存在, 30s 内 |

## 6. 关键学习

1. **借鉴 > 直接装** — 当外部项目跟我们的 fork 冲突时, 读 5 个核心脚本拿设计点, 比装整个 project 安全
2. **metrics.json 是自我进化的基石** — 没有历史数据, mental_model 是单点值; 加 tracker 才有 trend
3. **5 类 not-fixable 分类价值** — 把"什么不是反模式"显式化, 触发时直接告诉用户"基础设施问题, 不是 skill 问题", 减少误诊
4. **sparkline 趋势 > 单点 KPI** — 30 天 success rate trend 比"今天 95%" 更能反映真实成长
5. **decision table 沉淀模式** — 19 类错误 + fix 模板 = 反模式库的可执行版本, 比"靠 mental_model 注入凭感觉"更稳

## 7. 关联笔记

- `notes/dspy-self-evolution-2026-06-06.md` — 5 步核验金标准 + DSPy 实战 3 landmines
- `notes/hindsight-v072-upgrade-3rd-notebook-2026-06-05.md` — 5 PATCH bank config 来源
- `notes/hermes-self-evolution-mental-model-v0.3` (mental_model) — 当前基线
- `notes/agent-governance-framework.md` — 反模式库 4 反模式来源
- L3 wiki `concepts/awesome-hermes-agent-ecosystem-2026.md` L55 — hermes-dojo 来源引用
- L3 wiki `agents/main-claude.md` L137 — in-repo 5 套技能之 hermes-dojo

## 8. 待办 (dojo 实施时)

- [ ] mental_model `hermes-self-evolution` v0.3 → v0.4 (本笔记方案)
- [ ] L1 MEMORY.md 铁律 #3 扩成 8 行决策表
- [ ] 新建 `E:\hermes\hermes\logs\hermes-self-evolution-metrics.json` + atomic write helper
- [ ] cron `hermes-self-evolution-metrics-cron` (每日 03:00 跑 refresh + 写 metrics)
- [ ] cron `purge_old_metrics` (每周日 04:00 跑 90 天 cutoff)
- [ ] failure_patterns.md 复制到 L3 wiki `concepts/hermes-failure-patterns.md` 并加 Z3rd 实战注释
- [ ] 7-天后 复盘 v0.4 效果, sparkline 趋势是否真的显示
