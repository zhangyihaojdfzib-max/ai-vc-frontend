---
title: Mistral Large 4 now available on AI Gateway - Vercel
title_original: Mistral Large 4 now available on AI Gateway - Vercel
date: '2026-10-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/mistral-large-4-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Mistral Large 4is now available on AI Gateway. The open-weight, natively multimodal
  model combines reasoning with text and image understa...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:53:28.321707'
---

[翻译失败，原文如下]

Mistral Large 4is now available on AI Gateway. The open-weight, natively multimodal model combines reasoning with text and image understanding. It is useful for cyber defense, manufacturing, and finance workflows.

You can access the model through AI Gateway with one API key, without creating a separate Mistral account.

Use Mistral Large 4 (mistral/mistral-large-4) with theAI SDK,OpenAI-compatible Chat Completions API,Responses API, orAnthropic Messages API. You can also select it in acoding agentconnected to AI Gateway.

```
1import { streamText } from 'ai';2const result = streamText({3  model: 'mistral/mistral-large-4',4  prompt: 'Fix the failing test and verify the change.',5});
```

For coding agents, runnpx vercel ai-gateway setupand selectmistral/mistral-large-4in your agent's model settings.

Try Mistral Large 4 in themodel playground, or explore themodel catalog.

AI Gateway provides one API for calling models, tracking usage and cost, and configuring routing, retries, and failover. You can use anAI Gateway API keyorbring your own provider key.

---

> 本文由AI自动翻译，原文链接：[Mistral Large 4 now available on AI Gateway - Vercel](https://vercel.com/changelog/mistral-large-4-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-12 08:53
