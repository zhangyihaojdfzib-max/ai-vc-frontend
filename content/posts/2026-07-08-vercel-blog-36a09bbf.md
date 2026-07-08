---
title: Chat SDK新增Dial电话适配器
title_original: Chat SDK adds Dial support - Vercel
date: '2026-07-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-dial-support
author: ''
summary: Vercel的Chat SDK通过新的vendor-official适配器支持Dial，使开发者能够构建通过真实电话号码收发SMS、MMS、iMessage及语音通话的机器人。该适配器支持双向媒体传输和入站语音通话转录，每次通话自动创建Chat
  SDK线程，文本、媒体和转录均以消息形式呈现。开发者可使用标准API进行回复，并享受HMAC验证的webhook和稳定的每会话线程。文章提供了配置示例和完整指南链接。
categories:
- AI产品
tags:
- Chat SDK
- Dial适配器
- 电话机器人
- Vercel
- 消息API
draft: false
translated_at: '2026-07-08T05:26:22.602627'
---

Chat SDK 现在通过新的 `vendor-official` 适配器支持 Dial。

构建能够通过真实电话号码发送和接收 SMS、MMS 和 iMessage 的机器人，支持双向媒体和入站语音通话转录。回复使用标准的 Chat SDK 线程和消息 API，并配备 HMAC 验证的 webhook 和稳定的每会话线程。

```
1import { Chat } from "chat";2import { createMemoryState } from "@chat-adapter/state-memory";3import { createDialAdapter } from "@getdial/chat-sdk-adapter";4
5export const bot = new Chat({6  userName: "Dial Bot",7  adapters: {8    dial: createDialAdapter({9      apiKey: process.env.DIAL_API_KEY,10      fromNumberId: process.env.DIAL_FROM_NUMBER_ID,11      webhookSecret: process.env.DIAL_WEBHOOK_SECRET,12    }),13  },14  state: createMemoryState(),15});16
17bot.onNewMention(async (thread, message) => {18  await thread.post(`听到你说: ${message.text}`);19});
```

配置 Dial 适配器以响应 @-提及

每次电话通话都会成为一个 Chat SDK 线程。文本和媒体作为消息到达该线程，当语音通话结束时，其转录也会出现在那里。订阅、处理程序、帖子以及每线程状态的工作方式与任何其他 Chat SDK 适配器相同。

阅读 Dial 文档以开始使用。

Chat SDK 完整指南

了解 Chat SDK 的端到端工作原理：从核心概念到构建第一个机器人，再到跨平台部署。

阅读指南

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds Dial support - Vercel](https://vercel.com/changelog/chat-sdk-adds-dial-support)
> 
> 翻译时间：2026-07-08 05:26
