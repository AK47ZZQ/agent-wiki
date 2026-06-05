---
title: "Agent Evaluation — 如何度量 Agent 的质量"
created: 2026-06-05
updated: 2026-06-05
type: method
tags: [method, evaluation, benchmark, quality, swe-bench, humaneval]
sources:
  - swebench.com (SWE-bench Verified, 2026)
  - Anthropic "Building Effective Agents" § evaluation
  - LangSmith / LangFuse observability platforms
confidence: medium
---

# Agent Evaluation — 如何度量 Agent 的质量

> **为什么需要**: 你花了 2 周搭建 Harness、写 AGENTS.md、调 Skills——但怎么知道 Agent 真的变好了？没有度量的优化是盲目的优化。Evaluation 是 Harness Engineering 的反馈回路。

---

## TL;DR

| 评估维度 | 工具/方法 | 测绘什么 |
|:---------|:---------|:--------|
| **代码生成** | SWE-bench, HumanEval | Agent 能正确解决真实 GitHub issue 吗？ |
| **终端任务** | Terminal Bench | Agent 能完成 CLI 工作流吗？ |
| **端到端** | 自建 E2E 测试套件 | Agent 在你的代码库上的表现 |
| **回归** | Eval Harness（固定测试集） | 改动 Harness 后 Agent 有没有退步？ |

---

## 1. 核心基准 (Benchmarks)

### 1.1 SWE-bench (swebench.com)

**什么**: 从真实 Python GitHub 仓库中提取的 bug 修复任务。Agent 拿到 issue 描述 + 代码库 → 生成 patch → 跑真实测试验证。

**为什么重要**: 这是目前**最接近真实工作的 Agent 基准**：
- 不是合成问题，是真 issue
- 不是单文件修改，是跨文件 patch
- 不是 mock 测试，是真 CI pass/fail

**关键指标**:
| 指标 | 含义 |
|:-----|:-----|
| Resolved Rate | 生成的 patch 通过了仓库的真实测试 |
| Coverage | 参与评估的总 issue 数 |
| Cost per Resolution | 解决一个问题花了多少 token/$ |

**当前领先者 (2026)**:
- Claude 4.5 Opus + mini-SWE-agent v2
- DeepSeek V3.2 Reasoner
- Codex 系列

### 1.2 HumanEval

**什么**: 164 个人工编写的 Python 编程题。Agent 生成函数 → 对隐藏测试用例验证。

**为什么重要**: 纯代码生成能力基线。简单、快、可复现。

### 1.3 自建 E2E (最重要!)

基准测试通用但不针对你的代码库。**必须建自己的 E2E 评估**:

```
你的 E2E 评估套件应该包含:
├── tasks/                      # 真实任务
│   ├── add-api-endpoint.md     # "加一个 GET /users 端点"
│   ├── fix-bug-42.md           # "修复 issue 42"
│   ├── refactor-module.md      # "重构 payment 模块"
│   └── ...
├── expected/                   # 预期结果
│   ├── add-api-endpoint.patch  # gold standard patch (可选)
│   └── ...
├── tests/                      # 验证脚本
│   ├── check_lint.sh
│   ├── check_tests.sh
│   └── check_arch.sh
└── eval.py                     # 运行评估的脚本
```

**最少 5 个任务、覆盖 3 种任务类型**（新增功能 / 修 bug / 重构）。

---

## 2. Eval-Driven Development for Agents

类比 TDD（测试驱动开发），但对象是 Agent:

```
Eval-Driven Agent Development 循环:

1. 写 Eval 任务: "Agent 必须能修这种 bug"
2. 跑基线: 当前 Agent 能解决吗？（记录基线分）
3. 改 Harness: 调整 AGENTS.md / Skills / linter 规则
4. 再跑 Eval: 分数有没有提高？
5. 没提高 → 回滚改动，尝试别的
   有提高 → 保留改动，继续下一个
```

**关键**: 每次改 Harness 后**必须重跑 Eval**，否则不知道改动是优化还是退化。

---

## 3. Agent 质量的多维仪表盘

不应只看单一分数。建议追踪这 6 个维度:

| 维度 | 指标 | 如何测量 |
|:-----|:-----|:--------|
| **正确性** | E2E 任务通过率 | Eval suite pass % |
| **效率** | Token / 时间 per task | API 日志统计 |
| **可维护性** | 生成代码的质量分 | linter / typecheck / complexity |
| **鲁棒性** | 失败后的自我修复率 | 从 Sensor 告警到修复成功的 % |
| **安全性** | 危险操作拦截率 | Guardrail 触发次数 / 应触发次数 |
| **回归** | 已修复 bug 的复现率 | 历史 Eval 任务是否仍然通过 |

---

## 4. 可观测性 (Observability)

评估需要数据。需要**能看到 Agent 每步做了什么**:

| 工具 | 定位 | 产出 |
|:-----|:-----|:-----|
| **LangSmith** | Agent 追踪 + 评估平台 | 每次 tool call 的 trace + 自动评分 |
| **LangFuse** | 开源替代 | 同上，self-hosted |
| **自建 log** | 最小可行 | 结构化 JSON 日志 (task_id, steps, result, tokens) |
| **Hermes LCM** | 会话压缩引擎 | 压缩后的对话摘要 + 历史检索 |

---

## 5. 最小可行评估流程 (今天就能建)

```python
# eval.py — 5 分钟建好的基线评估
import subprocess, json, time

tasks = [
    {"id": "T1", "desc": "添加 GET /health 端点，返回 {'status': 'ok'}", "check": "curl -s localhost:3000/health | grep ok"},
    {"id": "T2", "desc": "修复: 用户名为空时返回 500 而非 400", "check": "curl -s -X POST localhost:3000/users -d '{}' | grep 400"},
    {"id": "T3", "desc": "添加单元测试覆盖 payment.calculate()", "check": "npm test -- --coverage | grep 'payment'"},
]

results = []
for task in tasks:
    start = time.time()
    # 调用 Agent (根据你的 Agent 框架调整)
    subprocess.run(["hermes", "run", task["desc"]])
    passed = subprocess.run(task["check"], shell=True).returncode == 0
    results.append({"id": task["id"], "passed": passed, "time": time.time() - start})

pass_rate = sum(1 for r in results if r["passed"]) / len(results)
print(f"Eval Pass Rate: {pass_rate:.0%} ({sum(1 for r in results if r['passed'])}/{len(results)})")
# 保存基线: echo '{"date":"2026-06-05","pass_rate":0.67}' >> eval_history.json
```

**每周跑一次** → 看趋势 → 发现 Harness 改动的影响。

---

## 6. 关联 Wiki 页面

- [[concepts/harness-engineering-deep-study]] — Harness 的 Sensors 反馈 = Evaluation 的一种形式
- [[concepts/agent-reasoning-patterns]] — ReAct / Reflexion 的评估方法不同
- [[concepts/context-engineering]] — 上下文设计好坏 → 通过 Eval 验证
- [[comparisons/multi-agent-architecture-patterns]] — 不同架构的评估维度不同
- [[methods/agent-writing-standard]] — AGENTS.md 的好坏 → 通过 Eval 验证

---

## 7. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：SWE-bench + HumanEval + 自建 E2E + Eval-Driven + 6 维仪表盘 + 最小可行脚本 |

---

> **核心领悟**: 没有评估的 Agent 优化就像没有测试的重构——你不知道是在变好还是变坏。Eval 不是点缀，是 Harness Engineering 的**反馈回路**（Sensors 中最关键的一个）。
