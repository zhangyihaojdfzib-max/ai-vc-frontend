---
title: Nano Banana 2（Gemini 3.1 Flash Image Preview）在AI Gateway正式上线
title_original: Nano Banana 2 is live on AI Gateway - Vercel
date: '2026-02-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/nano-banana-2-is-live-on-ai-gateway
author: ''
summary: Vercel宣布其AI Gateway正式上线Nano Banana 2（即Gemini 3.1 Flash Image Preview模型）。该多模态模型在保持闪存级生成速度和成本优势的同时，显著提升了视觉输出质量。新功能包括利用谷歌图片搜索关联实时图像数据以渲染地标和物体、引入可配置的“思考级别”（最小/高级）供模型处理复杂提示前进行推理，并新增了512p分辨率及1:4、1:8等宽高比选项，扩展了创意素材的支持范围。用户可通过AI
  SDK调用模型，并利用AI Gateway的统一API进行成本跟踪、性能优化及智能路由。
categories:
- AI产品
tags:
- Vercel
- AI Gateway
- Gemini
- 多模态模型
- 图像生成
draft: false
translated_at: '2026-02-27T04:40:04.398867'
---

Gemini 3.1 Flash Image Preview（Nano Banana 2）现已在 AI Gateway 上可用。

此版本在保持闪存级模型的生成速度和成本的同时，提升了视觉质量。

Nano Banana 2 可以利用谷歌图片搜索，将输出结果与现实世界图像相关联。这通过检索实时视觉数据，有助于渲染不太知名的地标和物体。该模型还引入了可配置的思考级别（最小和高级），让模型在渲染前能够对复杂的提示词进行推理。除了现有选项外，还新增了新的分辨率和新的宽高比（512p、1:4 和 1:8），以扩展支持更多类型的创意素材。

要使用此模型，请在 AI SDK 中将模型设置为 `google/gemini-3.1-flash-image-preview`。Nano Banana 2 是一个多模态模型。使用 `streamText` 或 `generateText` 可以生成图像和文本响应。此示例展示了模型如何使用网络搜索来查找实时数据。

![](/images/posts/c33ef8c58d63.jpg)

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'google/gemini-3.1-flash-image-preview',5  providerOptions: {6    google: { responseModalities: ['TEXT', 'IMAGE'] },7  },8  prompt: 'Generate an image of the 2026 Super Bowl at golden hour',9});
```

您也可以更改思考级别：在此示例中，思考级别被设置为 `high` 以获得更详尽的响应。

![](/images/posts/2e3631f12c8f.jpg)

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'google/gemini-3.1-flash-image-preview',5  providerOptions: {6    google: {7      responseModalities: ['TEXT', 'IMAGE'],8      thinkingConfig: {9        includeThoughts: true,10        thinkingLevel: 'high',11      },12    },13  },14  prompt:15   `An exploded view diagram of a modern GPU, showing the die, HBM stacks, interposer,16    and cooling solution as separate floating layers with labeled callouts.`,17});
```

AI Gateway 提供了一个统一的 API，用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它包括内置的可观测性、自带密钥支持以及具有自动重试功能的智能供应商路由。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Nano Banana 2 is live on AI Gateway - Vercel](https://vercel.com/changelog/nano-banana-2-is-live-on-ai-gateway)
> 
> 翻译时间：2026-02-27 04:40
