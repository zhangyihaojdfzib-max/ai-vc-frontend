---
title: GPT Image 2图像模型正式登陆Vercel AI Gateway
title_original: GPT Image 2 on AI Gateway - Vercel – Vercel
date: '2026-04-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/gpt-image-2-on-ai-gateway
author: ''
summary: OpenAI最新图像生成模型GPT Image 2现已在Vercel AI Gateway平台上线。该模型能够根据详细指令生成高分辨率图像，支持精确物体布局、多种宽高比及密集文本渲染，包括非英语文本。其应用场景涵盖照片、电影剧照、像素艺术、漫画等多种视觉风格，适用于游戏原型、故事板、营销创意等专业工作流。开发者可通过AI
  SDK或模型游乐场直接调用，同时AI Gateway提供统一的API管理、成本跟踪、性能优化及智能路由等功能。
categories:
- AI产品
tags:
- GPT Image 2
- Vercel AI Gateway
- 图像生成
- AI模型
- OpenAI
draft: false
translated_at: '2026-04-22T05:05:19.079420'
---

GPT Image 2 现已在 Vercel AI Gateway 上可用。

OpenAI 最新的图像模型支持遵循详细指令、精确放置物体及其相互关系，并能在多种宽高比下渲染密集文本。

该模型能以高达 2K 的分辨率渲染精细元素，包括小号文本、图标、UI 元素、密集构图以及微妙的风格约束。同时支持非英语文本，并能确保其连贯可读。

GPT Image 2 能够生成照片、电影剧照、像素艺术、漫画及其他独特的视觉风格，并在纹理、光照、构图和细节上保持一致性。这适用于游戏原型设计、故事板绘制、营销创意以及特定媒介资产生成等工作流程。

要使用 GPT Image 2，请在 AI SDK 中将模型设置为 `openai/gpt-image-2`，或直接在我们的模型游乐场中试用。

```
1import { generateImage } from 'ai';2
3const result = await generateImage({4  model: 'openai/gpt-image-2',5  prompt: 'Poster of Vercel AI products, Bauhaus style.',6});
```

![](/images/posts/4a4d90002a6c.jpg)

![](/images/posts/34ba64dd1b70.jpg)

AI Gateway 提供了一个统一的 API 来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它内置了自定义报告、可观测性、自带密钥支持以及具备自动重试功能的智能供应商路由。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[GPT Image 2 on AI Gateway - Vercel – Vercel](https://vercel.com/changelog/gpt-image-2-on-ai-gateway)
> 
> 翻译时间：2026-04-22 05:05
