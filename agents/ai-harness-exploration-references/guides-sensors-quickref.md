# Guides × Sensors 参考卡

> Fowler/Böckeler 控制论框架速查。用于分析任何 AI 编码工具/系统。

## 2×2 矩阵

| | 计算性（确定性，CPU） | 推理性（语义，LLM） |
|---|---|---|
| **前馈/Guides**（行动前） | bootstrap、模板、LSP、脚手架 | AGENTS.md、Spec、Workflow、Constraints |
| **反馈/Sensors**（行动后） | linter、测试、类型检查、CI | AI review、LLM judge、行为验证 |

## 三类 Harness

| 类型 | 成熟度 | 说明 |
|:----|:------|:------|
| 可维护性 | ✅ 最成熟 | 代码质量，工具丰富 |
| 架构适配性 | 🟡 中等 | Fitness Functions |
| 行为正确性 | 🚩 最弱 | 房间里的大象 |

## 分析问题模板

```
前馈分析：
  □ 有 AGENTS.md / CLAUDE.md 吗？
  □ 有 SPEC / ARCHITECTURE 文档吗？
  □ 有启动模板/脚手架吗？
  □ 有 Workflow 定义吗？

反馈分析：
  □ 有 linter/type checker 吗？
  □ 有 CI/CD pipeline 吗？
  □ 有 AI code review 循环吗？
  □ 有自动化测试吗？

平衡检查：
  □ 前馈 > 反馈？→ 规则多但无法验证
  □ 反馈 > 前馈？→ 总是事后修补
  □ 平衡？→ 最健康
```
