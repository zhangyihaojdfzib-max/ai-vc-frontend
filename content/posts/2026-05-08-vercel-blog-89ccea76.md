---
title: Vercel Chat SDK新增Messenger适配器支持
title_original: Chat SDK adds Messenger adapter support - Vercel
date: '2026-05-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-messenger-adapter
author: ''
summary: 'Vercel的Chat SDK现已支持将Messenger作为聊天适配器，开发者可以构建支持消息、反应、多媒体下载、回传按钮和直接对话的智能体。用户显示名称会自动从资料中获取。文章提供了简单的代码示例，展示如何创建适配器并处理直接消息。此外，还感谢了社区贡献者@mitkodkn在PR
  #461中的工作。开发者可查阅文档开始使用或构建自定义适配器。'
categories:
- AI基础设施
tags:
- Chat SDK
- Messenger
- Vercel
- 聊天适配器
- 智能体
draft: false
translated_at: '2026-05-09T05:23:20.630190'
---

![](/images/posts/a226eea1b1e6.jpg)

Chat SDK 现已支持将 Messenger 作为聊天适配器。

构建支持消息、反应、多媒体下载、回传按钮和直接对话的 Agent（智能体），显示名称会自动从用户资料中获取。

```
1import { Chat } from "chat";2import { createMessengerAdapter } from "@chat-adapter/messenger";3
4const bot = new Chat({5  userName: "mybot",6  adapters: {7    messenger: createMessengerAdapter(),8  },9});10
11bot.onDirectMessage(async (thread, message) => {12  await thread.post(`You said: ${message.text}`);13});
```

将每条新提及的消息回复给发送者

阅读 Chat SDK 文档以开始使用，浏览支持的适配器，或学习如何构建自己的适配器。

特别感谢 @mitkodkn，其在 PR #461 中的社区贡献为该适配器奠定了基础。

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds Messenger adapter support - Vercel](https://vercel.com/changelog/chat-sdk-adds-messenger-adapter)
> 
> 翻译时间：2026-05-09 05:23
