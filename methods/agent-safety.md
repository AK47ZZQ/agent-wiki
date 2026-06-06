---
title: "Agent Safety — Guardrails, 沙箱, and 权限模型"
created: 2026-06-05
updated: 2026-06-05
type: method
tags: [method, safety, guardrails, sandbox, approval, security]
sources:
  - Anthropic RSP (Responsible Scaling Policy)
  - Claude Code permission modes: /approve, /deny, /yolo
  - Claude Code Harness guardrail engine (Chachamaru127, v4.14.0)
  - Hermes CLI security commands
confidence: medium
source: hermes-3rd-context-2026-06
---

# Agent Safety — Guardrails, 沙箱, 权限模型

> **为什么需要**: Agent 越自主，破坏力越大。一个没有安全模型的 Agent 就像一个没有 sudo 密码提示的 root shell——一次误操作就是灾难。

---

## TL;DR — 安全分层模型

```
Layer 1: 模型层安全    "模型本身不产生有害输出"
Layer 2: 工具层安全    "Agent 不能调用危险工具"
Layer 3: 权限层安全    "Agent 调用工具时需审批"
Layer 4: 环境层安全    "Agent 在隔离环境中运行"
Layer 5: 监控层安全    "Agent 的行为被持续审计"
```

---

## 1. 工具层安全 — Guardrails

### 1.1 13 条基础规则 (来自 Claude Code Harness v4.14.0)

| 规则 ID | 规则 | 动作 |
|:--------|:-----|:-----|
| R01 | `sudo` 调用 | ❌ 拒绝 |
| R02 | 修改系统文件 (`/etc/`, `/boot/`) | ❌ 拒绝 |
| R03 | 受保护路径写入 | ❌ 拒绝 |
| R04 | 删除 `.git/` 目录 | ❌ 拒绝 |
| R05 | `rm -rf /` 或 `rm -rf ~` | ⚠️ 需确认 |
| R06 | `git push --force` to main | ❌ 拒绝 |
| R07 | 修改 `.git/config` | ❌ 拒绝 |
| R08 | 安装系统级包 (`apt install`, `brew install`) | ⚠️ 需确认 |
| R09 | 修改环境变量文件 (`.env`, `.bashrc`) | ⚠️ 需确认 |
| R10 | 读取密钥文件 (`.env`, `credentials.json`) | ⚠️ 告警 |
| T01-T12 | 测试篡改检测 | ❌ 拒绝 + 告警 |
| S01 | 密钥泄露检测 (API key / PAT 在输出中) | ❌ 阻断 |

### 1.2 实现要求

```
Guardrail 引擎的性能要求:
- 热路径 < 5ms (不能拖慢 Agent 响应)
- 零文件 I/O (避免竞争条件)
- 零网络调用 (避免延迟不可控)
- 编译型语言实现 (Go/Rust, 非 shell 脚本)

反模式:
- ❌ bash if-else 守卫 (40-60ms, 不可测试)
- ❌ 每次调用都读配置文件
- ❌ 规则写在人类文档里 (Agent 可以忽略)
```

---

## 2. 权限模型 — Approval Gates

### 2.1 三级权限模型

| 级别 | 操作 | 需要审批？ | 示例 |
|:-----|:-----|:---------|:-----|
| **🟢 安全** | 读文件、写临时文件、运行测试 | 否 | `cat file.txt`, `npm test` |
| **🟡 敏感** | 修改代码、安装依赖、网络请求 | 本次 session 内首次需审批 | `git commit`, `npm install` |
| **🔴 危险** | 删除文件、修改系统配置、force push | 每次都需审批 | `rm -rf`, `git push --force` |

### 2.2 Claude Code 模式 vs Hermes 模式

| 操作 | Claude Code | Hermes |
|:-----|:-----------|:------|
| 批准本次 session | `/approve session` | `/approve session` |
| 永久信任 | `/approve always` | `/approve always` |
| 拒绝 | `/deny` | `/deny` |
| 跳过所有审批 (危险!) | `/yolo` | `/yolo` |

### 2.3 审批设计原则

> **不应让人类成为安全瓶颈**——如果每个操作都要审批，人类会变成"审批疲劳"然后无脑点通过。

正确做法:
- 安全操作自动放行（零审批）
- 同类型操作 session 内只问一次
- 审批历史可视化（"你今天批了 47 次 rm -rf"）

---

## 3. 沙箱 — 环境隔离

### 3.1 沙箱层级

| 级别 | 隔离程度 | 性能开销 | 适用场景 |
|:-----|:---------|:--------|:--------|
| **None** | 直接在当前环境执行 | 零 | 信任的代码库 + 人类监督 |
| **Read-only FS** | Agent 只能读文件系统 | 低 | 代码审查 Agent |
| **Workspace** | 只能读写指定目录 | 低 | 常规编码 Agent |
| **Docker Sandbox** | 容器隔离 | 中 | 运行不可信代码 |
| **VM Sandbox** | 虚拟机隔离 | 高 | 安全研究 / 恶意代码分析 |

### 3.2 实用配置

```yaml
# 推荐: 大多数 Agent 使用 Workspace 级别
sandbox:
  mode: workspace
  allowed_paths:
    - ./src/
    - ./tests/
    - ./docs/
  denied_paths:
    - ./.git/
    - ./.env
    - ./secrets/
  network: allow_outbound  # 允许 API 调用
  commands:
    allow: [git, npm, python, node]  # 白名单
    deny: [sudo, su, chmod 777]
```

---

## 4. 监控与审计

### 4.1 必须记录的信息

每次 Agent 操作都应该记录:

```json
{
  "timestamp": "2026-06-05T12:00:00Z",
  "agent_id": "main-claude",
  "tool": "bash",
  "command": "rm -rf ./temp/",
  "risk_level": "medium",
  "approval": "session",
  "result": "success",
  "files_affected": ["./temp/*"]
}
```

### 4.2 异常检测信号

| 信号 | 阈值 | 动作 |
|:-----|:-----|:-----|
| 单位时间危险操作数 | > 10 / 分钟 | 暂停 Agent + 告警 |
| 修改文件数 | > 50 / session | 人类确认 |
| 网络请求到新 IP | 首次 | 告警 |
| 连续审批拒绝 | > 3 次 | 停止 Agent |
| 密钥出现在输出中 | 任何 | 立即阻断 + 轮换密钥 |

---

## 5. Anthropic RSP (Responsible Scaling Policy) 参考

> Anthropic 的安全分级框架，适用于评估 Agent 系统的整体安全水平。

| ASL 级别 | 描述 | 典型安全措施 |
|:---------|:-----|:-----------|
| **ASL-1** | 无显著风险 | 基础测试 |
| **ASL-2** | 可能造成中等伤害 | 红队测试 + 外部审计 |
| **ASL-3** | 可能造成重大伤害 | 严格安全控制 + 部署前审批 |
| **ASL-4+** | 极端风险 | 不部署 / 极其严格的访问控制 |

**对你的 Agent 的问**: 你的 Agent 能删除生产数据库吗？能 force push 到 main 吗？能发送任意 HTTP 请求吗？答案如果是 "能" 且无审批——你需要安全模型。

---

## 6. 最小可行安全清单

```
[ ] Guardrail 引擎已部署（至少 R01-R07 + S01）
[ ] 危险命令白名单已配置
[ ] 审批模型已启用（禁止 /yolo 作默认）
[ ] Agent 运行在 workspace 级别沙箱
[ ] 操作日志已结构化记录
[ ] 异常检测规则已配置
[ ] 密钥扫描已启用（pre-commit + Agent 输出）
[ ] 审批疲劳指标已监控
```

---

## 7. 关联 Wiki 页面

- [[concepts/harness-engineering-deep-study]] — Harness 的机械化执行 = Guardrails 的理论基础
- [[methods/safe-commit-push-protocol]] — Git 安全推送（安全模型的子集）
- [[methods/agent-writing-standard]] — 不把密钥写进 wiki
- [[concepts/agent-4-tier-memory-architecture]] — 记忆系统的安全隔离
- [[notes/lessons-learned-index]] — 踩过的安全坑

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版: 5 层安全模型 + 13 规则表 + 三级权限 + 沙箱 + 监控 |

---

> **核心领悟**: 安全不是功能，是架构属性。加在后面的安全 = 没有安全。Agent 的安全性必须在设计 Harness 的第一天就 baked in，就像你不会先盖房子再加地基。
