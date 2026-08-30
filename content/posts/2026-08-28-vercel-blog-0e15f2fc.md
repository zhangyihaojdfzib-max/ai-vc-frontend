---
title: Run Claude Managed Agents with Chat SDK - Vercel
title_original: Run Claude Managed Agents with Chat SDK - Vercel
date: '2026-08-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/claude-managed-agents-with-chat-sdk
author: ''
summary: '[翻译失败，原文如下]


  ![](/images/posts/7ad017880ffe.jpg)


  You can now runClaude Managed AgentswithChat SDK.


  Claude Managed Agents handles the agent loop serv...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-30T07:44:54.038093'
---

[翻译失败，原文如下]

![](/images/posts/7ad017880ffe.jpg)

You can now runClaude Managed AgentswithChat SDK.

Claude Managed Agents handles the agent loop server-side, including the model, tools, session state, and sandboxed web research. That means you can ship a Slack research bot built on Claude Managed Agents and Chat SDK, with one persistent session per thread and streamed briefs with sources.

### Copy link to headingWhat you get

- Token-by-token streaming: Replies render as the model writes them, over a single streamed response.
- Live activity feed: Tool calls and model requests are available during the turn, so you can surface a trace in the chat.
- No database to run:The Managed Agents session stores the conversation, so the sidebar, transcript, and replay read from it, no server-side state of your own.
- Portability by design: Swapping a few lines in the handler moves your agent to Teams, Google Chat, Discord, WhatsApp, and 30+ other platforms.

Token-by-token streaming: Replies render as the model writes them, over a single streamed response.

Live activity feed: Tool calls and model requests are available during the turn, so you can surface a trace in the chat.

No database to run:The Managed Agents session stores the conversation, so the sidebar, transcript, and replay read from it, no server-side state of your own.

Portability by design: Swapping a few lines in the handler moves your agent to Teams, Google Chat, Discord, WhatsApp, and 30+ other platforms.

### Copy link to headingGet started

To try Claude Managed Agents with Chat SDK:

- Deploy aSlack research agent on Vercelin one click
- Follow thestep-by-step guideor view thetemplate source

Deploy aSlack research agent on Vercelin one click

Follow thestep-by-step guideor view thetemplate source

## Contributors

Amelia Charles

---

> 本文由AI自动翻译，原文链接：[Run Claude Managed Agents with Chat SDK - Vercel](https://vercel.com/changelog/claude-managed-agents-with-chat-sdk)
> 
> 翻译时间：2026-08-30 07:44
