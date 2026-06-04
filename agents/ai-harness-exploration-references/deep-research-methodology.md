# Deep Research 3-Layer Methodology

> 来源：deusyu/harness-engineering 实际实践
> 该仓库维护了一份 19 篇文章的深度研究数据库，横跨三条知识脉络

## 3-Layer 追踪框架

### 第一层：每日自动监控

- 工具：ChatGPT Deep Research / Manus / openclaw
- 7 个固定来源：arXiv / GitHub Trending / Twitter / 5 个专业博客
- 5 个搜索域：新概念 / 新工具 / 实践案例 / 批判分析 / 对比
- 3 级优先级：official papers > well-known authors > community posts
- 去重：对照已知文章清单和已跟踪项目

### 第二层：双周深度搜索

- 检索范围：上一轮之后的所有新内容
- 深度分析：逐篇阅读摘要→判断是否值得全量读
- 趋势信号：同一概念出现在多个来源 = 值得关注

### 第三层：按需深入

- 触发条件：出现新范式、新工具、显著批判
- 使用 ai-harness-exploration 的完整探勘法

## Article Database 结构

```
每篇文章包含：
  标题 + 作者 + 日期
  核心论点（1-2 句）
  关键数据
  跨文章关联（引用了谁？被谁引用？与谁冲突？）
  脉络归属（脉络一/二/三/延伸）
```

## 实际效果（deusyu 案例）

| 投入 | 产出 |
|:----|:----|
| 3 层追踪（每日+双周+按需） | 19 篇深度摘要 + 8 篇概念笔记 + 8 篇独立思考 |
| 一致性检查脚本（C1-C7） | 7 层机器校验保证计数和引用准确 |
| 翻译 pipeline | 12 篇中文翻译 |
| Ralph Demo | 321s / $0.31 实证 |

## 已验证的 3 个子代理并行深研模式（2026-05-31）

针对大型复杂主题（如 GitHub 仓库全量分析），实测最佳的并行模式：

```python
# 3 路并行子代理，每路独立搜索+分析+产出
delegate_task(tasks=[
    {"goal": "深入分析: {topic} 架构原理/API/协议", "toolsets": ["web","terminal","file"]},
    {"goal": "深挖: {topic} 对比分析/落地可行性/社区评价", "toolsets": ["web","terminal","file"]},
    {"goal": "分析: {topic} 安全模型/PWA/版本演进", "toolsets": ["web","terminal","file"]},
])
```

**实测结果（Hermes Workspace 探勘 2026-05-31）：**
| 指标 | 值 |
|:-----|:---|
| 子代理完成数 | 2/3（第3路 600s 超时） |
| 产出 | ~15KB 对比分析 + ~21KB 架构分析 |
| 墙钟 | ~10min |
| 串行等价 | ~30min+ |
| 加速比 | ~3× |
| 超时处理 | 2 路已完成所有内容，超时路损失安全分析视角 |

**模式总结：**
- 3 路是最优并行度（token 成本上限可控，覆盖度够广）
- 其中 1 路超时（600s limit）是正常现象 — 2/3 已完成足够交付
- 超时路损失单一视角，不影响主体交付
- 产出分析文件落地为 wiki pages：编排器验收后移入 `~/hermes-all/wiki/wiki/entities/`
- 工具调用：每路子代理约 16-55 次，合计 ~120 次工具调用
- 适用于：GitHub 仓库探勘、工具对比、框架深研
