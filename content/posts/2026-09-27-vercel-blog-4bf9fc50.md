---
title: Ember-1 from Fireworks now available on AI Gateway - Vercel
title_original: Ember-1 from Fireworks now available on AI Gateway - Vercel
date: '2026-09-27'
source: Vercel Blog
source_url: https://vercel.com/changelog/ember-1-from-fireworks-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Ember-1from Fireworks is now available onAI Gateway.


  Ember-1 is a research preview reasoning model built onKimi K3for coding and agentic...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-13T08:48:26.677860'
---

[翻译失败，原文如下]

Ember-1from Fireworks is now available onAI Gateway.

Ember-1 is a research preview reasoning model built onKimi K3for coding and agentic workflows.

Fireworks reports approximately 40% fewer generated tokens than Kimi K3 at comparable quality across its evaluations. For coding agents that make repeated model calls, shorter reasoning traces can reduce output costs and the amount of context carried into later steps.

Ember-1 supports a 1M-token context window, text and image input, tool calling, andimplicit prompt caching. The Fireworks endpoint supportsZero Data RetentionandNo Prompt Training.

This model is available as a research preview with an initial two-week window.

To get started, usefireworks/ember-1for the model name across APIs and coding agents:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'fireworks/ember-1',5  prompt: 'Write a retry helper with exponential backoff.',6});
```

To use Ember-1 in yourcoding agent, run the setup command with theVercel CLI:

```
1npm i -g vercel@latest2vercel ai-gateway setup
```

The command detects installed agents, provisions or reuses an AI Gateway API key, and configures their connection to the gateway. Then selectfireworks/ember-1in your agent's model configuration.

AI Gateway provides a unified API for calling models, with built-inusage and cost tracking,budgets for API keys, androuting rules.

Try Ember-1 in themodel playground.

---

> 本文由AI自动翻译，原文链接：[Ember-1 from Fireworks now available on AI Gateway - Vercel](https://vercel.com/changelog/ember-1-from-fireworks-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-13 08:48
