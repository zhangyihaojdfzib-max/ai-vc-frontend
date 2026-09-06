---
title: Bring your agent to Notion with Chat SDK - Vercel
title_original: Bring your agent to Notion with Chat SDK - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/notion-chat-sdk
author: ''
summary: '[翻译失败，原文如下]


  ![](/images/posts/0fda6d29dde6.jpg)


  Your team already works in Notion. Now your agent can too.


  With the newNotion adapterfor Chat SDK, ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-06T06:45:00.431686'
---

[翻译失败，原文如下]

![](/images/posts/0fda6d29dde6.jpg)

Your team already works in Notion. Now your agent can too.

With the newNotion adapterfor Chat SDK, the same agent you run on Slack, Discord, GitHub, Teams, or WhatsApp can join comment discussions on your Notion pages, no separate codebase required.

```
1import { Chat } from "chat";2import { createNotionAdapter } from "@chat-adapter/notion";3import { createRedisState } from "@chat-adapter/state-redis";4
5const bot = new Chat({6  userName: "my-bot",7  adapters: {8    notion: createNotionAdapter(),9  },10  state: createRedisState(),11});12
13bot.onNewMention(async (thread, message) => {14  await thread.post("Hello from Notion!");15});
```

Respond to a comment on Notion with your agent

Each Notion page maps to a channel and each comment thread to a thread, so replies stay threaded automatically.

The adapter supports mentions, message editing, conversation history, and up to three file attachments. By default, your bot replies when @-mentioned and where mentions aren't available in a workspace, it can trigger on a keyword or on all comments instead.

Notion doesn't support buttons, modals, or reactions, and cards render as markdown. Discussions can start at the page or block level, but not on inline text ranges. History fetches return only open comments.

Read thedocumentationto get started, browse thedirectory, orbuild your own.

---

> 本文由AI自动翻译，原文链接：[Bring your agent to Notion with Chat SDK - Vercel](https://vercel.com/changelog/notion-chat-sdk)
> 
> 翻译时间：2026-09-06 06:45
