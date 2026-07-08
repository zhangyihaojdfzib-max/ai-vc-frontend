---
title: Chat SDK新增Photon支持，构建iMessage机器人
title_original: Chat SDK adds Photon support - Vercel
date: '2026-07-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-photon-support
author: ''
summary: Chat SDK通过新的vendor-official适配器支持Photon，使开发者能够构建直接发送和接收iMessage的机器人，包括个人和群组聊天、媒体分享及原生Tapback反应。适配器可运行于Spectrum
  Cloud、自有服务器或Mac上。每个Photon对话成为Chat SDK线程，Tapback作为反应传入，Webhook经HMAC验证，支持直接回复私信而无需实时连接。文章还提供了配置示例和完整指南链接。
categories:
- AI产品
tags:
- Chat SDK
- Photon
- iMessage机器人
- 适配器
- Vercel
draft: false
translated_at: '2026-07-08T05:26:26.697170'
---

Chat SDK 现通过新的 `vendor-official` 适配器支持 Photon。

构建能够直接发送和接收 iMessage（包括个人聊天和群组聊天）、分享媒体以及使用原生 Tapback 进行反应的机器人。该适配器可针对 Spectrum Cloud、你自己的服务器或直接在 Mac 上运行。

```
1import { Chat } from "chat";2import { createMemoryState } from "@chat-adapter/state-memory";3import { createiMessageAdapter } from "@photon-ai/chat-adapter-imessage";4
5export const bot = new Chat({6  userName: "Photon Bot",7  adapters: {8    imessage: createiMessageAdapter({9      local: false,10      projectId: process.env.IMESSAGE_PROJECT_ID,11      projectSecret: process.env.IMESSAGE_PROJECT_SECRET,12    }),13  },14  state: createMemoryState(),15});16
17bot.onNewMention(async (thread, message) => {18  await thread.post(`You said: ${message.text}`);19});
```

配置 Photon 适配器以响应 @-提及

每个 Photon 对话都会成为 Chat SDK 中的一个线程，而 Tapback 则会作为反应传入。处理程序、消息发布和订阅的工作方式与其他适配器相同。Webhook 经过 HMAC 验证，你的机器人可以直接通过 Webhook 投递回复私信，无需保持实时连接。

阅读 Photon 文档以开始使用。

Chat SDK 完全指南

了解 Chat SDK 的端到端工作原理：从核心概念到构建你的第一个机器人，再到跨平台部署。

阅读指南

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds Photon support - Vercel](https://vercel.com/changelog/chat-sdk-adds-photon-support)
> 
> 翻译时间：2026-07-08 05:26
