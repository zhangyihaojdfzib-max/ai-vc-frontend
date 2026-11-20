---
title: GPT-Live 1.1 now available on AI Gateway - Vercel
title_original: GPT-Live 1.1 now available on AI Gateway - Vercel
date: '2026-11-19'
source: Vercel Blog
source_url: https://vercel.com/changelog/gpt-live-1-1-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  GPT-Live 1.1 from OpenAIis now available on AI Gateway.


  GPT-Live 1.1 is a full-duplex voice model, so it listens while it speaks and a c...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:23.294060'
---

[翻译失败，原文如下]

GPT-Live 1.1 from OpenAIis now available on AI Gateway.

GPT-Live 1.1 is a full-duplex voice model, so it listens while it speaks and a caller can pause, interrupt, or add detail mid-reply. Compared with the previous GPT-Live model, it transcribes speech more accurately and keeps a more consistent accent and voice across languages. It uses the same Live endpoint and client delegation, so an existing GPT-Live integration only needs the new model ID.

### Copy link to headingSimple example without delegation

Runopenai/gpt-live-1.1by itself:

```
1import { createOpenAI } from '@ai-sdk/openai';2
3const live = createOpenAI({4  apiKey: process.env.AI_GATEWAY_API_KEY,5  baseURL: 'https://ai-gateway.vercel.sh/v1',6}).experimental_realtime('openai/gpt-live-1.1', { api: 'live' });7
8const { url, headers } = await live.getServerWebSocketConfig();9
10send(live.serializeClientEvent({11  type: 'session-start',12  config: { instructions: 'You are a helpful voice assistant.' },13}));
```

### Copy link to headingDelegate work and keep talking

Turn on client delegation, and use the session instructions to tell GPT-Live 1.1 when to ask for help. It asks by sending delegation-created. Answer with any text model on AI Gateway and return the result on the commentary channel for GPT-Live to speak. This example uses openai/gpt-6.2-sol and builds on the session above:

```
1send(live.serializeClientEvent({2  type: 'session-start',3  config: {4    instructions: 'Ask the application for help with order questions.',5    providerOptions: { openai: { delegation: { type: 'client' } } },6  },7}));8
9async function handleDelegation({ delegationId }) {10  const { text } = await generateText({11    model: 'openai/gpt-6.2-sol', 12    prompt: conversationContext,13  });14
15  send(live.serializeClientEvent({16    type: 'context-append',17    delegationId,18    content: text,19    providerOptions: { openai: { channel: 'commentary' } },20  }));21}
```

Your application controls delegated work and its permissions, confirmations, and cancellation. Delegated model requests are billed separately through AI Gateway, and voice-session usage continues while they run. These snippets omit the WebSocket connection, event parsing, transcript assembly, audio streaming, and shutdown. See theGPT-Live guidefor connection setup, audio streaming, and complete examples.

Try GPT-Live 1.1 in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[GPT-Live 1.1 now available on AI Gateway - Vercel](https://vercel.com/changelog/gpt-live-1-1-now-available-on-ai-gateway)
> 
> 翻译时间：2026-11-20 09:31
