---
title: Vercel Queues 消息队列服务开启有限测试
title_original: Vercel Queues is now in Limited Beta - Vercel – Vercel
date: '2025-06-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-queues-is-now-in-limited-beta
author: ''
summary: Vercel 宣布其专为 Vercel 应用程序设计的消息队列服务 Vercel Queues 现已进入有限测试阶段。该服务允许开发者将耗时任务（如
  AI 视频处理、发送邮件等）发送到队列进行后台异步处理，从而提升应用响应速度与可靠性。其核心特性包括基于主题的发布/订阅模式、流式处理支持、通过 OIDC Token
  的简化身份验证，以及提供完全类型安全的 TypeScript SDK。此举旨在帮助开发者更轻松地构建可扩展、 resilient 的后台任务处理系统。
categories:
- AI基础设施
tags:
- Vercel
- 消息队列
- Serverless
- 云计算
- 开发者工具
draft: false
translated_at: '2026-04-17T04:53:20.705347'
---

Vercel Queues 是为 Vercel 应用程序构建的消息队列服务，目前处于有限测试阶段。

Vercel Queues 允许您通过将任务发送到队列来卸载工作，这些任务将在后台进行处理。这意味着用户无需在请求期间等待耗时操作完成，并且您的应用程序可以更可靠地处理重试和失败。

在底层，Vercel Queues 使用仅追加日志来存储消息，并确保诸如 AI 视频处理、发送电子邮件或更新外部服务等任务被持久化且永不丢失。

Vercel Queues 的主要特性：

- 发布/订阅模式：基于主题的消息传递，允许多个消费者组
- 流式支持：处理有效负载而无需将其完全加载到内存中
- 简化的身份验证：通过 OIDC Token 自动认证
- SDK：具有完全类型安全性的 TypeScript SDK

发布/订阅模式：基于主题的消息传递，允许多个消费者组

流式支持：处理有效负载而无需将其完全加载到内存中

简化的身份验证：通过 OIDC Token 自动认证

SDK：具有完全类型安全性的 TypeScript SDK

```
1import { send, receive } from "@vercel/queue";2
3await send("topic", { message: "Hello World!" });4
5await receive("topic", "consumer", (m) => {6  console.log(m.message); 7});
```

使用队列发送和接收消息的示例。

如果您有任何问题，请在 Vercel 社区中告诉我们。

---

> 本文由AI自动翻译，原文链接：[Vercel Queues is now in Limited Beta - Vercel – Vercel](https://vercel.com/changelog/vercel-queues-is-now-in-limited-beta)
> 
> 翻译时间：2026-04-17 04:53
