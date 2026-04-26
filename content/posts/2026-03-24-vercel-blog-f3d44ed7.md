---
title: Vercel Chat SDK新增并发消息处理功能
title_original: Chat SDK now supports concurrent message handling - Vercel – Vercel
date: '2026-03-24'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-now-supports-concurrent-message-handling
author: ''
summary: Vercel的Chat SDK新增了并发消息处理功能，通过Chat类的concurrency选项，开发者可以自定义消息到达时的处理策略。支持四种策略：drop（默认，丢弃新消息）、queue（排队处理最新消息）、debounce（等待对话暂停后处理最后一条）和concurrent（立即处理每条消息）。该功能允许控制当前消息处理完成前新消息的行为，并提供了maxQueueSize、onQueueFull、queueEntryTtlMs等配置选项，适用于需要精细管理消息流量的AI对话场景。
categories:
- AI产品
tags:
- Vercel
- Chat SDK
- 并发处理
- 消息队列
- AI对话
draft: false
translated_at: '2026-04-26T04:58:31.767204'
---

Chat SDKnow 允许你控制当前一条消息处理完成前新消息到达时的行为，通过 Chat 类新增的 `concurrency` 选项实现。

```
1const bot = new Chat({2  concurrency: {3    strategy: "queue",4    maxQueueSize: 20,5    onQueueFull: "drop-oldest",6    queueEntryTtlMs: 60_000,7  },8  9});
```

支持多种选项以自定义你的并发策略。

提供四种策略：

- drop（默认）：丢弃传入的消息
- queue：在处理器完成后处理最新消息
- debounce：等待对话暂停，仅处理最后一条消息
- concurrent：立即处理每条消息，无锁定

drop（默认）：丢弃传入的消息

queue：在处理器完成后处理最新消息

debounce：等待对话暂停，仅处理最后一条消息

concurrent：立即处理每条消息，无锁定

阅读文档以开始使用。

---

> 本文由AI自动翻译，原文链接：[Chat SDK now supports concurrent message handling - Vercel – Vercel](https://vercel.com/changelog/chat-sdk-now-supports-concurrent-message-handling)
> 
> 翻译时间：2026-04-26 04:58
