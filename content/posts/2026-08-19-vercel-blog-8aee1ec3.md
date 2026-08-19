---
title: Chat SDK adds Instagram adapter - Vercel
title_original: Chat SDK adds Instagram adapter - Vercel
date: '2026-08-19'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-adds-instagram-adapter
author: ''
summary: '[翻译失败，原文如下]


  ![](/images/posts/a320fdd853fa.jpg)


  You can now build bots for Instagram with the newInstagram adapterfor Chat SDK.


  Bots can send and r...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:56.407265'
---

[翻译失败，原文如下]

![](/images/posts/a320fdd853fa.jpg)

You can now build bots for Instagram with the newInstagram adapterfor Chat SDK.

Bots can send and receive DMs and media, render cards as quick replies and link buttons, show typing indicators, receive reactions, and handle story replies.

```
1import { Chat } from "chat";2import { createInstagramAdapter } from "@chat-adapter/instagram";3
4export const bot = new Chat({5  userName: "mybot",6  adapters: {7    instagram: createInstagramAdapter(),8  },9});10
11bot.onDirectMessage(async (thread, message) => {12  await thread.post("Hello from Instagram!");13});
```

Reply to a direct message on Instagram

The adapter connects through Meta's Instagram Messaging API and requires a professional Business or Creator account.

Messages are buffered, so streamed responses send as one message when the stream completes. Meta enforces a 24-hour messaging window, so bots can only reply within a day of the user's last message.

Read thedocumentationto get started or browse theadapter directory.

---

> 本文由AI自动翻译，原文链接：[Chat SDK adds Instagram adapter - Vercel](https://vercel.com/changelog/chat-sdk-adds-instagram-adapter)
> 
> 翻译时间：2026-08-19 03:07
