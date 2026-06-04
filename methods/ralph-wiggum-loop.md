---
title: Ralph Wiggum Loop 实战方法
created: 2026-06-02
updated: 2026-06-02
type: method
tags: [harness-engineering, agent-loop, backpressure]
confidence: high
source: https://github.com/deusyu/harness-engineering
---

# Ralph Wiggum Loop — Harness Engineering 的核心实现模式

> 让智能体在循环中自主工作直到任务完成。来自 snarktank/ralph (13.6k★) + ralph-orchestrator (2.3k★)。

## 六条信条（与 Harness Engineering 映射）

| Ralph 信条 | Harness Engineering 对应 |
|:----------|:------------------------|
| **Fresh Context Is Reliability** | 智能体可读性 — 每次迭代重新读取整个上下文 |
| **Backpressure Over Prescription** | 机械化执行 — 不规定怎么做，但门控拒绝坏结果 |
| **The Plan Is Disposable** | 熵管理 — 重新生成成本只是一个 planning loop |
| **Disk Is State, Git Is Memory** | 仓库即记录系统 — 文件是交接机制 |
| **Steer With Signals, Not Scripts** | 人类掌舵 — 加路标，不加脚本 |
| **Let Ralph Ralph** | 智能体执行 — 坐在循环上，不坐在循环里 |

## 实践案例（来自 deusyu 的 Ralph Demo）

321 秒，$0.31，4 次迭代构建了一个 CLI 单词计数器（`wc.py` + 7 个 pytest 测试）。

**Hat 系统：** Planner→Builder→Critic→Finalizer 角色分离
**背压门控：** 测试必须在继续之前通过
**持久记忆：** `scratchpad.md` 跨迭代
**循环终止：** `LOOP_COMPLETE` 信号
**自愈：** Builder 在测试失败后自动修复字符计数 bug

## 在 Hermes 中的应用

等价于 `delegate_task` 的背压版本：

```
每个子代理 = 一个 Ralph 迭代
背压 = 测试/验证失败导致循环重来
终止条件 = 所有检查通过
```

区别在于 Ralph 是 bash 脚本驱动，Hermes 是工具调用驱动。

## 相关概念

- [[concepts/harness-engineering-deep-study]] — 框架全景
- [[concepts/harness-engineering]] — 基础概念
