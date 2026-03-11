---
title: Chat SDK推出适配器目录，集成Vercel与社区平台
title_original: Chat SDK now has an adapter directory - Vercel
date: '2026-03-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adapter-directory
author: ''
summary: Chat SDK 最新推出了适配器目录，允许开发者从 Vercel 和社区中搜索并使用各类平台与状态适配器。适配器分为三类：由核心团队维护的官方适配器、由平台公司（如
  Resend 和 Beeper）构建维护的供应商官方适配器，以及由第三方开发者构建的社区适配器。文章鼓励团队构建并提交适配器，并提供了使用 Resend 适配器连接电子邮件服务的代码示例，展示了如何利用与
  Slack 机器人相同的处理机制来创建处理邮件的工作流。开发者可通过浏览目录或阅读贡献指南来了解如何构建、测试和发布自己的适配器。
categories:
- AI基础设施
tags:
- Chat SDK
- 适配器
- Vercel
- 开发者工具
- 开源社区
draft: false
translated_at: '2026-03-11T04:31:44.478328'
---

Chat SDK 现已拥有 `adapter` 目录，因此你可以从 Vercel 和社区中搜索平台与状态适配器。

这些包括：

- **官方适配器**：由核心 Chat SDK 团队维护，以 `@chat-adapter/*` 名义发布。
- **供应商官方适配器**：由平台公司（如 Resend 和 Beeper）构建和维护。它们位于其 GitHub 组织中，并在其文档中有说明。
- **社区适配器**：由第三方开发者构建，并可遵循与 AI SDK 社区提供者相同的模式进行发布。

**官方适配器**：由核心 Chat SDK 团队维护，以 `@chat-adapter/*` 名义发布。

**供应商官方适配器**：由平台公司（如 Resend 和 Beeper）构建和维护。它们位于其 GitHub 组织中，并在其文档中有说明。

**社区适配器**：由第三方开发者构建，并可遵循与 AI SDK 社区提供者相同的模式进行发布。

我们鼓励团队构建并提交适配器以纳入此新目录，例如 Resend 的将电子邮件连接到 Chat SDK 的适配器：

```
1import { Chat } from "chat";
2import { MemoryStateAdapter } from "@chat-adapter/state-memory";
3import { createResendAdapter } from "@resend/chat-sdk-adapter";
4
5const resend = createResendAdapter({
6  fromAddress: "bot@yourdomain.com",
7});
8
9const chat = new Chat({
10  userName: "email-bot",
11  adapters: { resend },
12  state: new MemoryStateAdapter(),
13});
14
15
16chat.onNewMention(async (thread, message) => {
17  await thread.subscribe();
18  await thread.post(`Got your email: ${message.text}`);
19});
```

一个用于分拣支持邮件或发送后续邮件的 Agent（智能体）工作流，使用与 Slack 机器人相同的处理程序和卡片基元。

浏览 `adapter` 目录或阅读贡献指南，了解如何构建、测试、记录和发布你自己的适配器。

---

> 本文由AI自动翻译，原文链接：[Chat SDK now has an adapter directory - Vercel](https://vercel.com/changelog/chat-sdk-adapter-directory)
> 
> 翻译时间：2026-03-11 04:31
