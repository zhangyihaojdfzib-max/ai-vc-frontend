---
title: Chat SDK新增Sendblue支持，构建跨平台消息机器人
title_original: Chat SDK adds Sendblue support - Vercel
date: '2026-06-22'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-sendblue-support
author: ''
summary: Vercel的Chat SDK通过新的vendor-official适配器支持Sendblue，使开发者能够构建通过Sendblue托管网关发送和接收iMessage、SMS及RCS的机器人。该适配器将每个Sendblue对话映射到Chat
  SDK线程，支持消息优先通过iMessage投递，并自动回退至SMS和RCS，同时提供轻点回应、输入状态指示器和投递状态回调等功能。文章提供了代码示例和配置说明，帮助开发者快速集成并响应移动对话中的@-提及。
categories:
- AI产品
tags:
- Chat SDK
- Sendblue
- 消息机器人
- 跨平台通信
- Vercel
draft: false
translated_at: '2026-06-25T06:08:00.213102'
---

Chat SDK 现在通过新的 `vendor-official` 适配器支持 Sendblue。

构建能够通过 Sendblue 托管网关发送和接收 iMessage、SMS 及 RCS 的机器人，触达用户已在使用的消息应用。消息优先通过 iMessage 投递，并支持自动回退至 SMS 和 RCS、轻点回应、输入状态指示器以及投递状态回调。

```
1import { Chat } from "chat";2import { createSendblueAdapter } from "chat-adapter-sendblue";3import { createMemoryState } from "@chat-adapter/state-memory";4
5const chat = new Chat({6  userName: "imessage-bot",7  adapters: {8    sendblue: createSendblueAdapter(),9  },10  state: createMemoryState(),11});12
13chat.onDirectMessage(async (thread, message) => {14  await thread.post(`Got it: ${message.text}`);15});
```

配置适配器以响应移动对话中的 @-提及

该适配器将每个 Sendblue 对话映射到一个 Chat SDK 线程（关联特定电话号码和联系人/群组），并将每条入站 iMessage、SMS 或 RCS 消息映射为一条 Chat SDK 消息。

阅读 Sendblue 文档以开始使用。

Chat SDK 完整指南

了解 Chat SDK 的端到端工作原理：从核心概念到构建第一个机器人，再到将其部署到 Slack、Teams 等平台。

阅读指南

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds Sendblue support - Vercel](https://vercel.com/changelog/chat-sdk-adds-sendblue-support)
> 
> 翻译时间：2026-06-25 06:08
