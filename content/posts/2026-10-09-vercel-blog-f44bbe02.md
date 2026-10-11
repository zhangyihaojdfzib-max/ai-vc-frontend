---
title: Liquid AI's d1 is available on AI Gateway - Vercel
title_original: Liquid AI's d1 is available on AI Gateway - Vercel
date: '2026-10-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/liquid-ai-d1-is-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Liquid d1is now available onAI Gateway.


  d1 is adecision modelthat evaluates shared state against typed questions for classification,
  rou...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:06:30.190551'
---

[翻译失败，原文如下]

Liquid d1is now available onAI Gateway.

d1 is adecision modelthat evaluates shared state against typed questions for classification, routing, and scoring. It returns structured answers with probabilities without generating text tokens.

d1 also has vision support: the model can answer typed questions about images for visual classification, inspection, and scoring.

Useliquid/d1through theAI SDK decision API, theOpenAI-compatible Decisions API, or theTypeSafe-compatible API. These examples ask whether a support agent issued a refund:

```
1import { experimental_decide as decide } from 'ai';2
3const result = await decide({4  model: 'liquid/d1',5  state: 'The support agent issued a full refund to the customer.',6  questions: {7    refunded: {8      type: 'boolean',9      instructions: 'Was a refund issued?',10    },11  },12});13
14console.log(result.answers.refunded);
```

## Copy link to headingImage input

This example reads a local PNG namedsquare.pngand asks which color it shows:

```
1import { readFileSync } from 'node:fs';2import { experimental_decide as decide } from 'ai';3
4const image = readFileSync('./square.png').toString('base64');5
6const result = await decide({7  model: 'liquid/d1',8  state: [9    {10      type: 'json',11      value: [12        'Which color is the square?',13        {14          type: 'image_url',15          image_url: { url: `data:image/png;base64,${image}` },16        },17      ],18    },19  ],20  questions: {21    color: {22      type: 'choice',23      instructions: 'What color is the square?',24      criteria: { red: null, blue: null, green: null },25    },26  },27});28
29console.log(result.answers.color);
```

AI Gateway provides a unified way to access models and track usage and cost. Decision calls appear inlogsand count towardbudgetsalongside other model requests.

See thedecision documentationfor Choice, Score, and Boolean questions. To pick a decision model, browse theavailable modelsor read ourdecision model guides.

---

> 本文由AI自动翻译，原文链接：[Liquid AI's d1 is available on AI Gateway - Vercel](https://vercel.com/changelog/liquid-ai-d1-is-available-on-ai-gateway)
> 
> 翻译时间：2026-10-11 08:06
