---
title: Liquid AI's d1-ultra now available on AI Gateway - Vercel
title_original: Liquid AI's d1-ultra now available on AI Gateway - Vercel
date: '2026-10-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/liquid-ais-d1-ultra-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  d1-ultra from Liquid AIis now available on AI Gateway. It is a multimodal decision
  model for classification, routing, and scoring across ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-25T07:27:16.302328'
---

[翻译失败，原文如下]

d1-ultra from Liquid AIis now available on AI Gateway. It is a multimodal decision model for classification, routing, and scoring across text and images, including visual defect inspection and checking damage claims against customer photos.

Rather than generating text, d1-ultra returns structured answers with probabilities. Ask a Boolean question to get the probability of a yes/no answer, use Choice to select among named categories, or use Score to rate an ordered scale. You can ask multiple questions about the same input in one request and use the probabilities to decide when to automate an action or request human review.

d1-ultra is designed for harder real-world decisions, with an emphasis on calibrated probabilities. It supports a 32,768-token context window and is billed on input tokens only, including image input, with no output-token charges.

Useliquid/d1-ultraas the model name. The examples below ask the same question through the AI SDK, OpenAI-compatible Decisions API, and TypeSafe-compatible API:

```
1import { experimental_decide as decide } from 'ai';2
3const result = await decide({4  model: 'liquid/d1-ultra',5  state: 'The customer reports that the delivered laptop has a cracked screen.',6  questions: {7    damaged: {8      type: 'boolean',9      instructions: 'Does the customer report that the item arrived damaged?',10    },11  },12});13
14console.log(result.answers.damaged);
```

See thedecision models documentationfor question types and additional usage details.

Try d1-ultra in themodel playground.

AI Gateway provides a unified API for accessing models and tracking usage and cost. Decision calls appear inlogsand count towardbudgetsalongside other model requests.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Keyrequests.

Browseall decision modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Liquid AI's d1-ultra now available on AI Gateway - Vercel](https://vercel.com/changelog/liquid-ais-d1-ultra-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-25 07:27
