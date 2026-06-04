---
title: 新知识入库检查清单
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, curation, checklist, knowledge-base, 4-tier]
sources: [methods/wiki-curation-guide, methods/using-knowledge-base]
---

# 新知识入库检查清单

> 10 步标准化流程 — 写 wiki 内容前必走一遍,避免低质量条目。

## TL;DR

- **核心**:5 问检查 + 8 步写入 + 4 步去重
- **不写**:百科条目 / 通用知识 / LCM 摘要复制
- **必写**:源链 + frontmatter + 至少 1 个 wikilink

## 5 问检查(开写之前)

1. **能复用吗?** — 是否已存在于 wiki? `grep -r "关键词" methods/ notes/ concepts/`
2. **能链接吗?** — 至少 1 个 wikilink 指向相关页面
3. **有源吗?** — 至少 1 个 sources 字段引用(内部链接或外部 URL)
4. **位置对吗?** — concepts/ methods/ notes/ entities/ tasks/ 哪个?
5. **frontmatter 齐吗?** — 6 字段(title/created/updated/type/tags/sources)

## 8 步写入流程

1. `git pull origin main` — 拉最新(避免冲突)
2. 决定位置(concept/method/note/entity/task)
3. 写文件(`write_file` 或 editor)
4. 跑 5 问检查
5. `check-wiki-quality.py` 验证
6. `git add -A && git commit -m "..."
7. `git push origin main` — 5 步核验后
8. log.md 追加 1 段(标记事件)

## 4 步去重

1. `grep -r "关键词"` 搜已有内容
2. 找到重复 → 决定:删除旧的 / 合并 / 交叉链接
3. 找引用 → 修所有引用旧文件的位置
4. `git add -A && git commit -m "去重:..."

## 5 反模式

- ❌ 复制 LCM 摘要(二次损失)
- ❌ 写百科条目(只写"我们学到的")
- ❌ 改 frontmatter schema(破坏 Obsidian)
- ❌ 用 `\u2014` 等 unicode escape 替代真字符(渲染失败)
- ❌ 不跑 `check-wiki-quality.py` 就 push

## 关联

- [[methods/wiki-curation-guide|wiki 策展指南]] — 详细判断框架
- [[methods/using-knowledge-base|知识库使用指南]] — 上手 3 步
- [[concepts/wiki-quality-metrics|9 维质量指标]] — 验收标准
- [[tasks/daily-knowledge-curation|每日新知识推送任务]] — 节奏流程
