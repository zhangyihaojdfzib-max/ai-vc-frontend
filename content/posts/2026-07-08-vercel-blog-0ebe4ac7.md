---
title: eve Chat SDK通道：一键连接多平台Agent
title_original: Use any Chat SDK adapter with eve - Vercel
date: '2026-07-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/eve-chat-sdk-channel
author: ''
summary: Vercel的eve平台推出新的Chat SDK通道，允许开发者通过单一通道将Agent连接到Facebook Messenger、WhatsApp、Resend、Liveblocks等多个平台。开发者只需编写标准的Chat
  SDK处理程序，调用send函数即可传递消息。该通道自动挂载webhook路由、显示输入状态指示器、渲染人工介入卡片、持久化线程并报告失败情况，极大简化了多平台Agent的部署与交互流程。
categories:
- AI基础设施
tags:
- eve
- Chat SDK
- 多平台集成
- Agent开发
- Vercel
draft: false
translated_at: '2026-07-08T05:26:23.578285'
---

evenow 支持通过新的 Chat SDK 通道使用 Chat SDK 适配器。

一个通道即可将您的 eve Agent 连接到 Facebook Messenger、WhatsApp、Resend、Liveblocks 以及任何其他带有适配器的平台。您只需编写标准的 Chat SDK 处理程序代码，在处理程序内部调用 `send` 即可将消息传递给您的 Agent。

```
1import { createMemoryState } from "@chat-adapter/state-memory";
2import { createResendAdapter } from "@resend/chat-sdk-adapter";
3import type { Message, Thread } from "chat";
4import { chatSdkChannel } from "eve/channels/chat-sdk";
5
6export const { bot, channel, send } = chatSdkChannel({
7  userName: "Resend Agent",
8  adapters: {
9    resend: createResendAdapter({
10      fromAddress: "hello@example.com",
11      fromName: "Resend Agent",
12    }),
13  },
14  state: createMemoryState(),
15  streaming: false,
16});
17
18bot.onNewMention(async (thread: Thread, message: Message) => {
19  await thread.subscribe();
20  await send(message.text, { thread });
21});
22
23export default channel;
```

使用 eve Resend Agent 回复邮件

在 `bot` 上注册处理程序的方式与在独立 Chat SDK 应用中完全相同。

该通道开箱即用，具备以下功能：

- 为每个适配器挂载一个 webhook 路由（例如 `/eve/v1/chat/slack`）
- 在轮次运行期间显示输入状态指示器，随后发布 Agent 的回复
- 将人工介入的输入请求渲染为带按钮的卡片，点击按钮后恢复会话
- 持久化线程，使得后续事件（包括来自定时任务的主动发送）能够到达同一对话
- 在线程中以可读消息报告失败情况

为每个适配器挂载一个 webhook 路由（例如 `/eve/v1/chat/slack`）

在轮次运行期间显示输入状态指示器，随后发布 Agent 的回复

将人工介入的输入请求渲染为带按钮的卡片，点击按钮后恢复会话

持久化线程，使得后续事件（包括来自定时任务的主动发送）能够到达同一对话

在线程中以可读消息报告失败情况

您可以提供自己的事件处理程序来覆盖这些默认行为。

阅读 Chat SDK 通道文档以开始使用，或了解如何使用 Resend 构建您自己的 eve Agent。

---

> 本文由AI自动翻译，原文链接：[Use any Chat SDK adapter with eve - Vercel](https://vercel.com/changelog/eve-chat-sdk-channel)
> 
> 翻译时间：2026-07-08 05:26
