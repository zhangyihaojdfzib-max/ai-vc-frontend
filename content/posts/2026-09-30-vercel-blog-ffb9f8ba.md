---
title: Ling 3.1 Flash is now available on AI Gateway - Vercel
title_original: Ling 3.1 Flash is now available on AI Gateway - Vercel
date: '2026-09-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/ling-3-1-flash-is-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Ling 3.1 Flashfrom InclusionAI is now available on AI Gateway. The model is free
  to use through October 13, 2026.


  Ling 3.1 Flash is a hy...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:35.272270'
---

[翻译失败，原文如下]

Ling 3.1 Flashfrom InclusionAI is now available on AI Gateway. The model is free to use through October 13, 2026.

Ling 3.1 Flash is a hybrid reasoning language model with 560B total parameters and 25B active per token. It has a 262K-token context window on AI Gateway.

The model is designed for coding, multi-step analysis, and agents that use tools, including workflows involving long documents, code, and extended task histories.

To try Ling 3.1 Flash, useinclusionai/ling-3.1-flashorinclusionai/ling-3.1-flash-freeas the model name:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'inclusionai/ling-3.1-flash-free',5  prompt: 'Triage the open issues in this repo and group them by theme.',6});
```

The standard model ID is free during the promotion and begins billing when it ends. The-freemodel ID stops serving instead of billing when the free promotion ends.

To use Ling 3.1 Flash in a coding agent, follow theAI Gateway coding agents guideand selectinclusionai/ling-3.1-flashas the model.

Try Ling 3.1 Flash in theAI Gateway model playground, or explore themodel catalog.

AI Gateway provides one API for calling models, tracking usage and cost, and configuring routing, retries, and failover. You can use anAI Gateway API keyorbring your own provider key.

---

> 本文由AI自动翻译，原文链接：[Ling 3.1 Flash is now available on AI Gateway - Vercel](https://vercel.com/changelog/ling-3-1-flash-is-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-05 08:02
