---
title: TypeSafe AI's Jev now available on AI Gateway - Vercel
title_original: TypeSafe AI's Jev now available on AI Gateway - Vercel
date: '2026-09-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Jev from TypeSafe AIis now available on AI Gateway.


  Jev is a probabilistic decision model for software: state goes in, typed Choice,
  Sco...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T07:00:24.966440'
---

[翻译失败，原文如下]

Jev from TypeSafe AIis now available on AI Gateway.

Jev is a probabilistic decision model for software: state goes in, typed Choice, Score, and Boolean answers come out.

Regular language models generate text one token at a time, which the application then parses and validates. Jev evaluates all declared questions in parallel and returns typed answers plus probabilities directly. That removes unnecessary text generation and makes it straightforward to automate clear cases while routing uncertain ones to review.

TypeSafe reports Jev was up to 193.6x faster and 444.6x cheaper than LLMs on its workflow evaluations. Example use cases include:

- Choosing the next tool or subagent in an agent loop
- Deciding whether to continue, retry, ask the user, or stop
- Scoring urgency or risk before an action
- Verifying model outputs and enforcing guardrails.

Choosing the next tool or subagent in an agent loop

Deciding whether to continue, retry, ask the user, or stop

Scoring urgency or risk before an action

Verifying model outputs and enforcing guardrails.

AI SDK 7 exposes Jev through the experimentalevaluateAPI. Choice selects an option, Score grades an ordered rubric, and Boolean estimates the probability oftrue. Install the current AI SDK (AI SDK 7.0.105 onwards supports theevaluateAPI):

```
pnpm add ai@latest
```

Each evaluation specifies:

- model: the evaluation model to call,
- state: the shared string, object, or array to evaluate, and
- questions: a map of named decisions to make about that state.

model: the evaluation model to call,

state: the shared string, object, or array to evaluate, and

questions: a map of named decisions to make about that state.

Call the model withtypesafe-ai/jev. This example turns one support case into a queue, priority, and refund-review decision, with uncertain routing sent for manual review:

```
1import { experimental_evaluate as evaluate } from 'ai';2
3const result = await evaluate({4  model: 'typesafe-ai/jev',5  state: 'The support agent issued a full refund to the customer.',6  questions: {7    refunded: {8      type: 'boolean',9      instructions: 'Was a refund issued?',10    },11  },12  providerOptions: {13    gateway: { zeroDataRetention: true },14  },15});16
17console.log(result.answers.refunded);
```

The result preserves question IDs and Choice keys. TypeSafe reports separate Choice and Score confidence inresult.providerMetadata.typesafe.confidence. Calibrate probabilities and confidence against labeled examples from your workflow.

Jev supportsZero Data RetentionandNo Training, enabled per request in the example. Evaluation calls also appear inlogsandcustom reporting, count towardbudgets, and accept other Gateway provider options in the sameproviderOptions.gatewayobject.

Read the documentation onevaluation modelson AI Gateway for more details.

---

> 本文由AI自动翻译，原文链接：[TypeSafe AI's Jev now available on AI Gateway - Vercel](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)
> 
> 翻译时间：2026-09-17 07:00
