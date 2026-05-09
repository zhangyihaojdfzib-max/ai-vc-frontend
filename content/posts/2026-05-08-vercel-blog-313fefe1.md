---
title: Chat SDK新增Web适配器，轻松构建浏览器聊天界面
title_original: Chat SDK adds web adapter support - Vercel
date: '2026-05-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-web-adapter-support
author: ''
summary: Chat SDK 推出了新的 Web 适配器，允许开发者通过简单的代码在服务器上定义机器人，并利用预配置的 React 钩子将聊天实时流式传输到浏览器。该适配器支持构建产品内助手、客服系统等基于浏览器的聊天体验，降低了开发门槛。文章提供了代码示例，展示了如何创建机器人、处理私聊消息以及集成到
  React 组件中，并鼓励用户查阅文档或构建自定义适配器。
categories:
- AI基础设施
tags:
- Chat SDK
- Web适配器
- 实时聊天
- React
- 浏览器集成
draft: false
translated_at: '2026-05-09T05:23:21.414610'
---

你现在可以通过新的Web适配器，构建连接到Chat SDK的聊天用户界面。打造产品内助手、支持客服或任何其他基于浏览器的聊天体验。

在你的服务器上定义机器人：

```
1import { Chat } from "chat";2import { createWebAdapter } from "@chat-adapter/web";3
4const bot = new Chat({5  userName: "mybot",6  adapters: {7    web: createWebAdapter({8      userName: "mybot",9      getUser: (req) => ({ id: getUserIdFromCookie(req) }),10    }),11  },12});13
14bot.onDirectMessage(async (thread, message) => {15  await thread.post(`You said: ${message.text}`);16});
```

将每条私聊消息原样回复给发送者

然后通过预配置的 `@ai-sdk/react` 的 `useChat` 钩子，将回复实时流式传输到浏览器：

```
1import { useChat } from "@chat-adapter/web/react";2
3const { messages, sendMessage, status } = useChat();
```

将机器人接入React组件

阅读Chat SDK文档以开始使用，浏览支持的适配器，或了解如何构建你自己的适配器。

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds web adapter support - Vercel](https://vercel.com/changelog/chat-sdk-adds-web-adapter-support)
> 
> 翻译时间：2026-05-09 05:23
