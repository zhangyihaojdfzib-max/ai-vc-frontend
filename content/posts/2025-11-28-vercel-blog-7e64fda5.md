---
title: Vercel AI网关新增纯图像模型，简化图像生成访问
title_original: Image-only models available in Vercel AI Gateway - Vercel
date: '2025-11-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/image-only-models-available-in-vercel-ai-gateway
author: ''
summary: Vercel宣布其AI网关现已支持纯图像生成模型，用户无需依赖其他提供商账户即可直接调用。本次新增的模型包括Black Forest Labs的FLUX系列（如FLUX.2
  Flex、FLUX.2 Pro等）和Google的Imagen 4.0系列（如Imagen 4.0 Generate 001）。用户可通过AI SDK统一API进行调用，支持`generateImage`方法。AI网关还提供使用情况跟踪、成本管理、故障转移、性能优化及内置可观测性等功能，旨在简化开发流程并提升服务可靠性。
categories:
- AI基础设施
tags:
- Vercel
- AI网关
- 图像生成
- AI模型
- 开发者工具
draft: false
translated_at: '2026-01-07T04:29:13.472881'
---

您现在可以通过 Vercel 的 AI 网关访问纯图像模型，无需其他提供商账户。除了 AI 网关中当前可用的具备图像生成能力的多模态模型（例如 GPT-5.1、Nano Banana Pro 等）外，这些纯图像模型专门用于图像生成。这些模型包括：

**Black Forest Labs：**
- FLUX.2 Flex：bfl/flux-2-flex
- FLUX.2 Pro：bfl/flux-2-pro
- FLUX.1 Kontext Max：bfl/flux-kontext-max
- FLUX.1 Kontext Pro：bfl/flux-kontext-pro
- FLUX 1.1 Pro Ultra：bfl/flux-pro-1.1-ultra
- FLUX 1.1 Pro：bfl/flux-pro-1.1
- FLUX.1 Fill Pro：bfl/flux-pro-1.0-fill

**Google：**
- Imagen 4.0 Generate 001：google/imagen-4.0-generate
- Imagen 4.0 Fast Generate 001：google/imagen-4.0-fast-generate
- Imagen 4.0 Ultra Generate 001：google/imagen-4.0-ultra-generate

要使用这些模型，请在 AI SDK 中将 `model` 设置为上述对应的标识符。这些模型支持 `generateImage`。

```
1import { experimental_generateImage as generateImage } from 'ai';2
3const result = await generateImage({4  model: 'bfl/flux-2-flex',5  prompt:6    'A snow leopard poised on a neon-lit rooftop at midnight rendered in vivid pop-art style.',7});
```

AI 网关提供了一个统一的 API 来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商水平的正常运行时间。它包含内置的可观测性、自带密钥支持以及具有自动重试功能的智能提供商路由。

请阅读关于图像生成的文档，查看 AI 网关模型排行榜，或直接在模型游乐场中试用这些模型。

**AI 网关：按使用量追踪顶级 AI 模型**

AI 网关模型排行榜根据通过网关的所有流量的总 Token 量，对一段时间内使用最多的模型进行排名。榜单定期更新。

---

> 本文由AI自动翻译，原文链接：[Image-only models available in Vercel AI Gateway - Vercel](https://vercel.com/changelog/image-only-models-available-in-vercel-ai-gateway)
> 
> 翻译时间：2026-01-07 04:29
