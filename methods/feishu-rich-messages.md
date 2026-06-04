---
title: 飞书富文本消息教程
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, feishu, lark, rich-message, post, card]
sources: [methods/feishu-group-setup, methods/using-knowledge-base]
---

# 飞书富文本消息教程

> 写给 Hermes Agent — 飞书 Post / Interactive Card / 富文本消息发送的 4 类方法 + 7 字段构造 + 6 实战模板。

## TL;DR

- **4 消息类型** = text / post / interactive / image
- **Post 消息** = 7 字段 JSON 构造
- **Interactive Card** = JSON 2.x 模板
- **feishu-rich-message skill** 封装 API

## 4 消息类型对比

| 类型 | 用途 | 复杂度 | 富文本 |
|---|---|---|---|
| **text** | 纯文本 | ⭐ | ❌ |
| **post** | 富文本(标题 + 多语言 + 链接) | ⭐⭐⭐ | ✅ |
| **interactive** | 卡片(按钮 + 表单 + 回调) | ⭐⭐⭐⭐ | ✅ |
| **image** | 图片消息 | ⭐ | ❌ |

## Post 消息构造(7 字段)

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "标题",
        "content": [
          [{"tag": "text", "text": "第一段"}],
          [{"tag": "a", "text": "链接", "href": "https://..."}],
          [{"tag": "at", "user_id": "ou_xxx"}]
        ]
      }
    }
  }
}
```

## Interactive Card(JSON 2.x)

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {"title": {"tag": "plain_text", "content": "标题"}},
    "elements": [
      {"tag": "div", "text": {"tag": "lark_md", "content": "**Markdown** 内容"}},
      {"tag": "hr"},
      {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "按钮"}, "type": "primary"}]}
    ]
  }
}
```

## 6 实战模板

1. **日报** — 标题 + 3 段(今日完成/问题/明日计划)
2. **报警** — header(red) + 关键指标 + @oncall
3. **审批** — 卡片 + 2 按钮(同意/拒绝)
4. **投票** — 表单 + 多选项
5. **code review 通知** — 文件链接 + diff 摘要
6. **GitHub commit 同步** — 标题 + commit 列表 + 链接

## 4 防坑

- ❌ Card 1.x 模板(已废弃,必须用 2.x)
- ❌ text 字段超 4096 字符
- ❌ @user_id 拼错(必须 `ou_` 前缀)
- ❌ webhook URL 用 IP(必须域名)

## 关联

- [[methods/feishu-group-setup]] — 群聊配置
- [[methods/using-knowledge-base]] — wiki 入口
