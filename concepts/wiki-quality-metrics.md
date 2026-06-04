---
title: 9 维质量指标仪表盘
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [wiki, metrics, quality, dashboard, health]
sources: [methods/wiki-curation-guide, methods/using-knowledge-base]
---

# 9 维质量指标仪表盘

> wiki 健康度的客观度量 — 跑 `check-wiki-quality.py` 自动算,周一/周五 cron 出报告。

## TL;DR

- **9 指标** = 3 健康度 + 3 完整性 + 3 链接性
- **每周** cron 自动跑
- **FAIL** 阈值 = 死链 ≥ 1 / 缺 frontmatter ≥ 1 / 缺索引 ≥ 1

## 3 健康度指标

| 指标 | 计算 | 健康阈值 |
|---|---|---|
| **死链数** | `grep` wikilink 但目标文件不存在 | **0** |
| **缺 frontmatter** | .md 文件但 6 字段缺 | **0** |
| **缺索引** | 文件不在 index.md / 多件套首页 | 0(孤立页允许短存) |

## 3 完整性指标

| 指标 | 计算 | 健康阈值 |
|---|---|---|
| **wikilink 度** | 平均每个文件 wikilink 数 | ≥ 3 |
| **frontmatter 覆盖率** | 有 6 字段文件 / 总数 | ≥ 95% |
| **索引覆盖率** | index.md 引文件 / 总数 | ≥ 80% |

## 3 链接性指标

| 指标 | 计算 | 健康阈值 |
|---|---|---|
| **孤立页面数** | 0 wikilink 引用 | ≤ 5 |
| **双向引用率** | 互相 wikilink 的 pair 数 | ≥ 30% |
| **跨分类链接** | 链接到不同类目(concepts↔methods 等) | ≥ 50% |

## 9 指标判定

- **3/3 健康度 PASS** = 总体 PASS
- **2/3 健康度 PASS** = 警告
- **≤ 1/3 健康度 PASS** = FAIL

## 跑法

```bash
python3 scripts/check-wiki-quality.py
# 输出:
# 死链:0 / 缺 frontmatter:0 / 缺索引:1 / wikilink 度:5.2
# 孤立页:3 / 双向引用率:45% / 跨分类链接:62%
# 总判定:PASS
```

## 关联

- [[methods/wiki-curation-guide|wiki 策展指南]] — 怎么用指标判断质量
- [[methods/using-knowledge-base|知识库使用指南]] — wiki 整体入口
- [[methods/curation-checklist|新知识入库检查清单]] — 5 问检查
