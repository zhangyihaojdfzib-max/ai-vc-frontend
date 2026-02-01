---
title: Vercel AI网关现已支持谷歌Nano Banana Pro图像模型
title_original: Nano Banana Pro (Gemini 3 Pro Image) now available in the AI Gateway
  - Vercel
date: '2025-11-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/nano-banana-pro-gemini-3-pro-image-now-available-in-the-ai-gateway
author: ''
summary: Vercel AI网关正式集成了谷歌的尖端图像生成模型Nano Banana Pro（Gemini 3 Pro Image），用户无需其他供应商账户即可直接调用。该模型专为高级专业和创意工作流设计，支持生成带精确标注的图表、集成网络搜索信息以获取最新内容、更高分辨率的图像生成以及更多的多图像输入。通过AI
  SDK，开发者可将模型设置为`google/gemini-3-pro-image`，使用`generateText`方法进行多模态图像生成。AI网关提供了统一的API，集成了使用追踪、成本管理、重试与故障转移机制，以及性能优化和可观测性工具，旨在提升服务可靠性和开发效率。
categories:
- AI基础设施
tags:
- Vercel
- AI网关
- Gemini
- 图像生成
- 多模态AI
draft: false
translated_at: '2026-02-01T04:24:21.831494'
---

您现在可以通过Vercel的AI网关访问谷歌尖端图像模型Nano Banana Pro（Gemini 3 Pro Image），无需其他供应商账户。

Nano Banana Pro（Gemini 3 Pro Image）专为比Nano Banana更高级的用例设计。该模型针对专业和创意工作流程进行了特别改进，例如生成带精确标注的图表，以及为图像集成包含最新信息的网络搜索信息。Nano Banana Pro还支持更高分辨率的生成和更高的多图像输入限制，以实现更好的合成效果。

要在AI网关中使用AI SDK调用Nano Banana Pro，请将模型设置为`google/gemini-3-pro-image`。请注意，这是一个多模态模型，因此使用`generateText`进行实际的图像生成。

```
1import { generateText } from 'ai';2
3const result = await generateText({4  model: 'google/gemini-3-pro-image',5  prompt:6    `Generate a labeled data pipeline diagram,7     from data ingestion through transformation,8     storage, and analytics layers.`,9});10if (result.text) {11  process.stdout.write(`\nAssistant: ${result.text}`);12}13for (const file of result.files) {14  if (file.mediaType.startsWith('image/')) {15    await presentImages([file]);16  }17}
```

AI网关提供了一个统一的API，用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它包含内置的可观测性、自带密钥支持以及具有自动重试功能的智能供应商路由。

请阅读AI网关文档，了解如何使用Nano Banana Pro生成图像的示例，查看AI网关模型排行榜，或在我们的模型游乐场中尝试生成图像。

AI网关：按使用量追踪顶级AI模型

AI网关模型排行榜根据通过网关的所有流量的总Token量，对一段时间内使用最多的模型进行排名。定期更新。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[Nano Banana Pro (Gemini 3 Pro Image) now available in the AI Gateway - Vercel](https://vercel.com/changelog/nano-banana-pro-gemini-3-pro-image-now-available-in-the-ai-gateway)
> 
> 翻译时间：2026-02-01 04:24
