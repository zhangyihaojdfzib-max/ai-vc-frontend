---
title: MiniMax M3 and M2.7 are free on AI Gateway - Vercel
title_original: MiniMax M3 and M2.7 are free on AI Gateway - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/minimax-m3-and-m2-7-are-free-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  MiniMax M3andM2.7are free on AI Gateway via GMI Cloud through Sunday, September
  6.


  Useminimax/minimax-m3-freeorminimax/minimax-m2.7-free...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:33.838669'
---

[翻译失败，原文如下]

MiniMax M3andM2.7are free on AI Gateway via GMI Cloud through Sunday, September 6.

Useminimax/minimax-m3-freeorminimax/minimax-m2.7-freeto route requests to GMI Cloud. These model IDs will return an error after the free period ends.

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'minimax/minimax-m3-free',5  prompt: 'Summarize the incident report.',6});7

```

Stream a response from MiniMax M3 through the free GMI Cloud route.

To keep requests working after the free period, use the standard model ID without the-freesuffix and place GMI Cloud first in the provider order:

```
1const result = streamText({2  model: 'minimax/minimax-m3',3  prompt: 'Summarize the incident report.',4  providerOptions: {5    gateway: {6      order: ['gmicloud'],7    },8  },9});
```

Prefer GMI Cloud for MiniMax M3 while allowing provider fallback.

AI Gateway tries GMI Cloud first and can fall back to another provider if GMI Cloud can't serve the request. This lets the same code continue working after the free period. Outside the free GMI Cloud route, requests are billed at the serving provider's rate. Both routing options work across all AI Gateway APIs.

To use a free MiniMax model with acoding agent, runvercel ai-gateway coding-agents setup, then select one of the-freemodel IDs in your agent.

Try MiniMaxM3andM2.7in the gateway playground.

---

> 本文由AI自动翻译，原文链接：[MiniMax M3 and M2.7 are free on AI Gateway - Vercel](https://vercel.com/changelog/minimax-m3-and-m2-7-are-free-on-ai-gateway)
> 
> 翻译时间：2026-08-26 03:00
