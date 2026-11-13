---
title: Gemini Decision 1 now available on AI Gateway - Vercel
title_original: Gemini Decision 1 now available on AI Gateway - Vercel
date: '2026-11-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/gemini-decision-1-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Gemini Decision 1 from Googleis now available on AI Gateway. The multimodal decision
  model works with text, images, audio, video, and PDF...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:33.062921'
---

[翻译失败，原文如下]

Gemini Decision 1 from Googleis now available on AI Gateway. The multimodal decision model works with text, images, audio, video, and PDF documents, returning Boolean probabilities, choices, and scores. Use it to route requests, check policies, filter agent tools, or rank results without generating output tokens.

Usegoogle/gemini-decision-1with the AI SDK, TypeSafe-compatible API, or Decisions API.

PDF, audio, and video inputs are supported through AI SDK 7. The TypeSafe-compatible and Decisions APIs support text and image inputs.

```
1import { experimental_decide as decide } from 'ai';2
3const result = await decide({4  model: 'google/gemini-decision-1',5  state: 'I was charged twice. Please refund the duplicate charge.',6  questions: {7    requestsRefund: {8      type: 'boolean',9      instructions: 'Does the customer request a refund?',10    },11  },12});13
14console.log(result.answers.requestsRefund);
```

AI Gateway provides a unified way to access models and track usage and cost. Decision calls appear inlogsand count towardbudgetsalongside other model requests.

See thedecision documentationfor Choice, Score, and Boolean questions. To pick a decision model, browse theavailable modelsor read ourdecision model guides.

---

> 本文由AI自动翻译，原文链接：[Gemini Decision 1 now available on AI Gateway - Vercel](https://vercel.com/changelog/gemini-decision-1-now-available-on-ai-gateway)
> 
> 翻译时间：2026-11-13 09:19
