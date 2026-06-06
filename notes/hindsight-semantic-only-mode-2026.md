---
title: Hindsight semantic-only mode (2026-06-04 新装)
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [hindsight, memory, mode, semantic-only, hermes, note]
sources:
  - user statement (2026-06-04)
  - concepts/hindsight-memory-modes-guide
confidence: medium
source: hindsight-deployment-2026-06
---

# Hindsight semantic-only mode (2026-06-04 新装)

> 2026-06-04 刚在 Hermes 里给 Hindsight 装的一个新 mode。**单源记录**(用户口头声明),细节待补。

## 是什么

- **名称**:`semantic-only mode`
- **类别**:Hindsight 自身的 mode(与 [[methods/install-hindsight-native-hermes-method|Hermes memory_mode 字段]] 的 3 选 1 `hybrid`/`context`/`tools` **正交**,不是同一层概念)
- **关键特性**(用户口径):
  - ❌ **不是** `hybrid`
  - ❌ **不是** `context`
  - ❌ **不是** `tools`
  - ❌ **不**与现有 4 mode(默认 `world` / `agent` / `user` / TBD)重合
  - ✅ 名字暗示:**只做语义检索**,不绑定 auto-recall / 显式工具

## 为什么单独记录

`concepts/hindsight-memory-modes-guide` 的 stub 一直把"第 4 个 mode"标为"待调研"。
这次 `semantic-only` 落地后,等于补上了**一个**新维度,但**没有**完全填上 TBD
(因为语义上它是"只检索不绑定策略",跟 `world`/`agent`/`user` 的"按内容分类"不是同一轴)。

→ 现状:**5 个 mode**,3 个"内容维度" + 1 个"只检索"新维度 + 1 个 TBD。

## 已知 vs 待补

| 维度 | 状态 |
|---|---|
| 模式名 | ✅ 已知 `semantic-only` |
| 与 hybrid 关系 | ✅ 明确"不是 hybrid" |
| 与 4 现有 mode 关系 | ✅ 全部不同 |
| 配置字段 | ⚠️ 待补(在 `~/.hermes/hindsight/config.json` 哪个 key?) |
| 与 `prefetch_method` 互斥 | ⚠️ 待测(`recall` / `reflect` 是否可用?) |
| 与 3 种 Hermes memory_mode 组合 | ⚠️ 待测(可叠加?互斥?) |
| 适用场景 | ⚠️ 待写(何时用最合适?) |
| 实测 token 成本 | ⚠️ 待测(标"只语义"应比 hybrid 省 token?) |

## 配置猜测(待验证)

```jsonc
// ~/.hermes/hindsight/config.json
{
  "mode": "semantic-only"  // 推测字段;也可能是新顶层 key
}
```

**验证步骤**(用户后续):
1. `cat ~/.hermes/hindsight/config.json` 确认实际写入字段
2. `hermes memory status` 看 status 输出是否识别新 mode
3. 重启 Hermes + 发 1 turn 测试 recall 行为

## 风险与决策点

| 风险 | 描述 |
|---|---|
| **可能与官方 mode 冲突** | 官方文档只列 `hybrid`/`context`/`tools`,`semantic-only` 可能是用户自定义 / fork 出来的 |
| **可能没有 prefetch** | "只语义"暗示 0 auto-recall,但需实测确认 |
| **与 handoff v1 关系** | [[notes/hindsight-risks-and-optimizations-2026|现有 handoff v1]] 是基于 `hybrid` 设计的,semantic-only 模式下 retain/recall 行为可能不同 |

## 行动项

- [ ] 用户跑一次 `hermes memory status` 确认新 mode 生效
- [ ] 把 `config.json` 实际内容贴回来(填空"配置猜测"段)
- [ ] 跑一轮 retain + recall 实测 token 成本
- [ ] 验证 prefetch_method 在 semantic-only 下是否被忽略
- [ ] 如果"4 现有 mode"具体是哪些与用户口径不符,**回头修** `concepts/hindsight-memory-modes-guide` 表格

## 关联文档

- [[concepts/hindsight-memory-modes-guide]] — 5 mode 总览(本条触发了它从 stub 升到 medium-confidence)
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 在 Hermes 生态定位
- [[methods/install-hindsight-native-hermes-method]] — Hermes 3 种 memory_mode(注意:与 semantic-only 正交)
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索(语义/关键词/图/时间)中的"语义"那一维可能就是 semantic-only 的底层
- [[notes/hindsight-risks-and-optimizations-2026]] — 已有风险点(在 hybrid 下测的)
