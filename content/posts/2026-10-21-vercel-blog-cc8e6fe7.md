---
title: Baseten's Mammoth-1 and Elephant-1 now available on AI Gateway for free - Vercel
title_original: Baseten's Mammoth-1 and Elephant-1 now available on AI Gateway for
  free - Vercel
date: '2026-10-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/basetens-mammoth-1-and-elephant-1-now-available-on-ai-gateway-for-free
author: ''
summary: '[翻译失败，原文如下]


  Mammoth-1andElephant-1from Baseten are now available for free on AI Gateway for
  one week. Free access is available through October 27. Th...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:55:58.038954'
---

[翻译失败，原文如下]

Mammoth-1andElephant-1from Baseten are now available for free on AI Gateway for one week. Free access is available through October 27. These decision models classify text, route requests, and score content against criteria you define.

Mammoth-1 is the larger, 27B model, while Elephant-1 is a smaller, 9B option.Mammoth-1 is #1 on the Jev Decision Index and Elephant-1 is tied for #1 on the Artificial Analysis Decision Index.

Both support a 16k-token context window and return choices, probabilities, and scores. Ask several questions about the same input in one request: select a support team with a Choice question, check for a refund request with a Boolean question, or rate urgency with a Score question. Your application chooses the probability threshold for acting automatically or sending a result for review.

Usebaseten/mammoth-1orbaseten/elephant-1as the model name:

```
1import { experimental_decide as decide } from 'ai';2
3const result = await decide({4  model: 'baseten/mammoth-1',5  state: 'I was charged twice. Please refund the duplicate.',6  questions: {7    refund: {8      type: 'boolean',9      instructions: 'Is the customer asking for a refund?',10    },11  },12});13
14console.log(result.answers.refund);
```

See thedecision models documentationfor question types and additional usage details.

AI Gateway provides a unified API for accessing models and tracking usage and cost. Decision calls appear inlogsand count towardbudgetsalongside other model requests.

Browseall decision modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Baseten's Mammoth-1 and Elephant-1 now available on AI Gateway for free - Vercel](https://vercel.com/changelog/basetens-mammoth-1-and-elephant-1-now-available-on-ai-gateway-for-free)
> 
> 翻译时间：2026-10-22 06:55
