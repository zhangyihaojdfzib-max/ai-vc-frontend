---
title: Vercel开源Chat SDK：一套代码，部署所有主流聊天平台
title_original: Introducing npm i chat – One codebase, every chat platform - Vercel
date: '2026-02-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk
author: ''
summary: Vercel开源了处于公测阶段的Chat SDK，这是一个统一的TypeScript库，旨在解决多平台聊天机器人开发中代码库分散的痛点。开发者只需编写一次机器人逻辑，即可通过模块化适配器部署到Slack、Microsoft
  Teams、Discord、GitHub等主流平台。该SDK采用事件驱动架构，提供类型安全的处理器来处理消息、反应、按钮点击等交互，并支持使用JSX构建跨平台原生渲染的卡片界面。同时，它集成了可插拔的状态管理适配器（如Redis），并支持与AI
  SDK结合，实现AI响应的实时流式传输，显著提升了聊天机器人开发的效率与一致性。
categories:
- AI基础设施
tags:
- Vercel
- 聊天机器人
- TypeScript
- 开源
- 跨平台开发
draft: false
translated_at: '2026-02-25T04:35:28.166458'
---

传统上，在多平台构建聊天机器人需要维护独立的代码库并处理各个平台的API。

今天，我们开源了处于公测阶段的**新Chat SDK**。这是一个统一的TypeScript库，允许团队编写一次机器人逻辑，并将其部署到Slack、Microsoft Teams、Google Chat、Discord、GitHub和Linear。

其事件驱动架构包含针对提及、消息、反应、按钮点击和斜杠命令的类型安全处理器。团队可以使用JSX卡片和模态框构建用户界面，这些界面会在每个平台上原生渲染。

该SDK使用可插拔适配器（支持Redis、ioredis和内存存储）来处理分布式状态管理。

```
1import { Chat } from "chat";2import { createSlackAdapter } from "@chat-adapter/slack";3import { createRedisState } from "@chat-adapter/state-redis";4
5const bot = new Chat({6  userName: "mybot",7  adapters: {8    slack: createSlackAdapter(),9  },10  state: createRedisState(),11});12
13bot.onNewMention(async (thread) => {14  await thread.subscribe();15  await thread.post("Hello! I am listening to this thread.");16});
```

一个使用Slack适配器和Redis状态、用于响应新提及的Chat实例的简单示例。

您可以使用字符串、对象、AST甚至JSX向任何提供商发送消息！

```
1import { Card, CardText, Actions, Button } from "chat";2
3await thread.post(4  <Card title="Order #1234">5    <CardText>Your order has been received!</CardText>6    <Actions>7      <Button id="approve" style="primary">Approve</Button>8      <Button id="reject" style="danger">Reject</Button>9    </Actions>10  </Card>11);
```

Chat SDK的`post()`函数接受AI SDK文本流，从而能够将AI响应和其他增量内容实时流式传输到聊天平台。

```
1import { ToolLoopAgent } from "ai";2
3const agent = new ToolLoopAgent({4  model: "anthropic/claude-4.6-sonnet",5  instructions: "You are a helpful assistant.",6});7
8bot.onNewMention(async (thread, message) => {9  const result = await agent.stream({ prompt: message.text });10  await thread.post(result.textStream);11});
```

该框架从核心的`chat`包开始，并通过模块化平台适配器进行扩展。我们提供了使用Next.js和Redis构建Slack机器人、使用Nuxt构建Discord支持机器人、使用Hono构建GitHub机器人以及构建自动化代码审查机器人的指南。

请查阅**文档**以了解更多信息。

在寻找聊天机器人模板吗？它无处可寻。

---

> 本文由AI自动翻译，原文链接：[Introducing npm i chat – One codebase, every chat platform - Vercel](https://vercel.com/changelog/chat-sdk)
> 
> 翻译时间：2026-02-25 04:35
