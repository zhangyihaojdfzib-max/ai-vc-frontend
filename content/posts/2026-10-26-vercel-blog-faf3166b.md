---
title: GPT-6.1 Terra now available on AI Gateway - Vercel
title_original: GPT-6.1 Terra now available on AI Gateway - Vercel
date: '2026-10-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/gpt-6-1-terra-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  GPT-6.1 TerrafromOpenAIis now available onAI Gateway.


  GPT-6.1 Terra is a fast model for visual reasoning, computer use, and writing, and...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:32:57.548282'
---

[翻译失败，原文如下]

GPT-6.1 TerrafromOpenAIis now available onAI Gateway.

GPT-6.1 Terra is a fast model for visual reasoning, computer use, and writing, and it improves on the previous Terra model in visual reasoning, factual accuracy, and coding. It suits high-volume work in documents and desktop apps, such as filling out forms, interpreting technical drawings, or entering invoice details into accounting software. OpenAI still recommends its larger GPT-6 models for the most complex coding tasks.

The model accepts text and images and returns text, with a context window of more than 1M tokens. It supports configurablereasoning effort,structured outputs, tool calling, and implicit and explicitprompt caching. For latency-sensitive work,fast modeis available asopenai/gpt-6.1-terra-fast.

GPT-6.1 Terra works with theAI SDK, theOpenAI-compatible Chat Completions API, theResponses API, andcoding agentsconnected to AI Gateway. Useopenai/gpt-6.1-terraas the model name:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'openai/gpt-6.1-terra',5  prompt: 'Draft a one-page proposal for migrating our docs site to Next.js.',6});
```

To use it in Codex, Cursor, and more, install the latest Vercel CLI and run setup:

```
npx vercel ai-gateway setup
```

Then selectopenai/gpt-6.1-terrain the agent. See thecoding agents guidefor details.

Try GPT-6.1 Terra in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[GPT-6.1 Terra now available on AI Gateway - Vercel](https://vercel.com/changelog/gpt-6-1-terra-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-27 07:32
