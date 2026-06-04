---
title: 飞书群聊配置教程
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, feishu, lark, group, bot, configuration]
sources: [methods/feishu-rich-messages, methods/using-knowledge-base]
---

# 飞书群聊配置教程

> 给 Hermes Agent:配置飞书群聊机器人的 8 步 + 权限清单 + 6 测试场景 + 5 踩坑。

## TL;DR

- **8 步配置** = 开发者后台 → 添加能力 → 权限 → 发布 → 群里加机器人 → 启用 → 事件订阅 → 验证
- **3 关键权限** = `im:message` / `im:chat` / `contact:user`
- **回调 URL** 必须是公网 HTTPS

## 8 步配置

1. **开发者后台** — 飞书开放平台 https://open.feishu.cn
2. **创建应用** — 企业自建应用,记 App ID + App Secret
3. **添加机器人能力** — 应用能力 → 机器人
4. **权限配置** — 权限管理 → 开通 20 个 im scope(见下)
5. **版本发布** — 版本管理 → 创建版本 → 提交审核
6. **群里添加机器人** — 群设置 → 群机器人 → 添加 → 搜索 App
7. **启用机器人** — 应用后台 → 启用机器人
8. **事件订阅** — 事件订阅 → 填回调 URL → 选事件(im.message.receive_v1 等)

## 20 个 im scope 含义

| 权限 | 用途 |
|---|---|
| `im:message` | 发送消息 |
| `im:message.group_at_msg` | 群 @ 消息 |
| `im:message.p2p_msg` | 单聊消息 |
| `im:message:send_as_bot` | 以机器人身份发 |
| `im:chat` | 群聊操作 |
| `im:chat:read` | 读群信息 |
| `im:chat.member` | 群成员 |
| `im:chat.member:read` | 读群成员 |
| `im:contact` | 通讯录 |
| `contact:user.id` | 读 user_id |
| ... 共 20 个 | |

## 6 测试场景

1. **发消息** — 验证机器人能发到群
2. **收消息** — 验证事件订阅能收 @ 机器人
3. **@机器人** — 测 mention
4. **拉群成员** — 测 `im:chat.member:read`
5. **发富文本** — 测 Post / Interactive Card
6. **发图片** — 测 image upload

## 5 踩坑

- ❌ 回调 URL 是 `http://`(必须 https)
- ❌ 回调 URL 是内网 IP(必须公网穿透 — `frp` / `cloudflare tunnel`)
- ❌ 权限漏给(消息发不出)
- ❌ 群 ID 跟 chat_id 混用(必须 `oc_` 前缀)
- ❌ 消息 ID 不唯一(必须用 `om_` 开头的 message_id)

## 2 进阶

- **多群路由** — 一个机器人接多群,按 `chat_id` 路由不同任务
- **静默消息** — 用 webhook 主动发,不通过事件

## 关联

- [[methods/feishu-rich-messages]] — 消息发送
- [[methods/using-knowledge-base]] — wiki 入口
