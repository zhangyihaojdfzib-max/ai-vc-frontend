---
title: Ling 3.0 Flash is now available on AI Gateway - Vercel
title_original: Ling 3.0 Flash is now available on AI Gateway - Vercel
date: '2026-07-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/ling-3-0-flash-is-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Ling 3.0 Flashfrom Ant Group is now available on AI Gateway.


  The model is free to use for the next three weeks, through August 3rd.


  Lin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:48.399765'
---

[翻译失败，原文如下]

Ling 3.0 Flashfrom Ant Group is now available on AI Gateway.

The model is free to use for the next three weeks, through August 3rd.

Ling 3.0 Flash is a Mixture-of-Experts model with 124B total parameters and about 5.1B active per token. It has a 256K token context window and runs in thinking and non-thinking modes.

Ling 3.0 Flash is built for token-efficient agentic inference at production scale, doing more work within tighter token, latency, and cost budgets across multi-step agent runs. The model targets high-frequency agentic workflows, coding agents, document work, and long-context multi-turn interactions.

To use Ling 3.0 Flash, set model toinclusionai/ling-3.0-flash-freein theAI SDK:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'inclusionai/ling-3.0-flash-free',5  prompt: 'Triage the open issues in this repo and group them by theme.',6});7

```

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

Try Ling 3.0 Flash in themodel playground.

---

> 本文由AI自动翻译，原文链接：[Ling 3.0 Flash is now available on AI Gateway - Vercel](https://vercel.com/changelog/ling-3-0-flash-is-now-available-on-ai-gateway)
> 
> 翻译时间：2026-07-25 05:00
