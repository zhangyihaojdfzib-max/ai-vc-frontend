---
title: Vercel推出Slack自定义运行时模块
title_original: Build custom Slack runtimes - Vercel
date: '2026-06-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/build-custom-slack-runtimes
author: ''
summary: Vercel的Chat SDK现已将Slack适配器的原生模块作为独立导入项提供，适用于已自行处理路由、状态或工作流执行的应用程序。开发者可按需使用请求验证与负载解析、Markdown格式化、基于Fetch的Web
  API调用以及Block Kit转换等功能。每个子路径均跳过完整的Chat运行时，保持导入简洁。文章提供了代码示例和完整指南链接，帮助开发者快速构建和部署Slack机器人。
categories:
- AI基础设施
tags:
- Vercel
- Slack
- Chat SDK
- 自定义运行时
- Webhook
draft: false
translated_at: '2026-06-12T06:37:02.377099'
---

![](/images/posts/c4964168d47f.jpg)

Chat SDK 现已将 Slack 适配器的原生模块作为独立导入项提供，适用于已自行处理路由、状态或工作流执行的应用程序。

按需使用所需功能：

- 请求验证与负载解析（@chat-adapter/slack/webhook）
- Markdown 格式化（@chat-adapter/slack/format）
- 基于 Fetch 的 Web API 调用（@chat-adapter/slack/api）
- Block Kit 转换（@chat-adapter/slack/blocks）

请求验证与负载解析（@chat-adapter/slack/webhook）

Markdown 格式化（@chat-adapter/slack/format）

基于 Fetch 的 Web API 调用（@chat-adapter/slack/api）

Block Kit 转换（@chat-adapter/slack/blocks）

每个子路径均跳过完整的 Chat 运行时，因此您的导入保持简洁。

```
1import { readSlackWebhook } from "@chat-adapter/slack/webhook";2import { postSlackMessage } from "@chat-adapter/slack/api";3
4export async function POST(request: Request) {5  const payload = await readSlackWebhook(request, {6    signingSecret: process.env.SLACK_SIGNING_SECRET!,7  });8
9  if (payload.kind === "app_mention") {10    await postSlackMessage({11      channel: payload.continuation.channelId,12      markdownText: `received: ${payload.text}`,13      token: process.env.SLACK_BOT_TOKEN!,14    });15  }16
17  return new Response(null, { status: 200 });18}
```

使用底层子路径验证 Webhook 并回复消息。

如需开始使用，请阅读 Slack 原生模块文档。

Chat SDK 完整指南

了解 Chat SDK 的端到端工作原理：从核心概念到构建您的第一个机器人，再到将其部署到 Slack、Teams 等平台。

阅读指南

---

> 本文由AI自动翻译，原文链接：[Build custom Slack runtimes - Vercel](https://vercel.com/changelog/build-custom-slack-runtimes)
> 
> 翻译时间：2026-06-12 06:37
