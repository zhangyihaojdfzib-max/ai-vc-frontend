---
title: Decision-1.1 now available on AI Gateway - Vercel
title_original: Decision-1.1 now available on AI Gateway - Vercel
date: '2026-11-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/decision-1-1-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Decision-1.1from Microsoft AI is now available on AI Gateway.It is more accurate,
  better calibrated, and faster than Decision-1.


  The dec...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-22T09:09:52.955720'
---

[翻译失败，原文如下]

Decision-1.1from Microsoft AI is now available on AI Gateway.It is more accurate, better calibrated, and faster than Decision-1.

The decision model returns structured answers instead of free-form text for tasks such as routing support requests, choosing which model should handle a request, selecting the next step in a workflow, or grading AI responses.

- Boolean: the probability that a condition is true
- Choice: a selected category and probabilities for each option
- Score: a numerical rating on a scale you define

Boolean: the probability that a condition is true

Choice: a selected category and probabilities for each option

Score: a numerical rating on a scale you define

Multiple questions can share the same input in one request. Better calibration means the model's probabilities track how often it is right, so your application can set thresholds for when to act, flag a case for review, or escalate.

Decision-1.1 accepts the same request format as Decision-1. To switch, change the model ID tomicrosoft/decision-1.1.

Call it through theAI SDK, theOpenAI-compatible Decisions API, or theAI CLI. The examples below requireai7.0.128 or later for TypeScript, or the OpenAI Python SDK 3.26.0 or later for Python.

```
1import { experimental_decide as decide } from 'ai';2
3const { answers } = await decide({4  model: 'microsoft/decision-1.1',5  state: 'I was charged twice for one order.',6  questions: {7    department: {8      type: 'choice',9      instructions: 'Which team should handle this?',10      criteria: {11        billing: 'Charges and refunds',12        technical: 'Bugs and outages',13      },14    },15  },16});17
18console.log(answers.department.choice);
```

Decision requests appear inrequest logs, count towardbudgets, and supportdecision fallbacks.

Try Decision-1.1 in themodel playground, or see thedecision models documentationfor request formats and question types.

---

> 本文由AI自动翻译，原文链接：[Decision-1.1 now available on AI Gateway - Vercel](https://vercel.com/changelog/decision-1-1-now-available-on-ai-gateway)
> 
> 翻译时间：2026-11-22 09:09
