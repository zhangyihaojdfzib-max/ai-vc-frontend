---
title: Grok Imagine Image 2.0登陆Vercel AI Gateway
title_original: Grok Imagine Image 2.0 now available on Vercel AI Gateway - Vercel
date: '2026-08-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/grok-imagine-image-2-0-preview-now-available-on-vercel-ai-gateway
author: ''
summary: xAI的Grok Imagine Image 2.0 Preview现已集成至Vercel AI Gateway，支持高精度指令遵循、排版布局协同规划，确保信息图、海报等复杂视觉内容结构完整且小字清晰。该模型还支持图像编辑，保持主体一致性。开发者可通过AI
  SDK设置模型为'xai/grok-imagine-image-2.0-preview'，调用generateImage生成或编辑图像，并可调整分辨率（1k/2k）及批量生成。Vercel提供了即时试用入口，并列出所有支持的图像模型。
categories:
- AI产品
tags:
- Grok Imagine
- Vercel AI Gateway
- 图像生成
- AI模型
- 开发者工具
draft: false
translated_at: '2026-08-11T03:38:09.078630'
---

xAI 的 Grok Imagine Image 2.0 Preview 现已登陆 AI Gateway。

该模型能够紧密遵循详细指令，并协同规划排版与布局，因此信息图、海报、标题画面等密集的多部分视觉内容能保持其结构，小号文字也清晰可读。Grok Imagine Image 2.0 Preview 还支持图像编辑，在多次生成中保持主体和细节的一致性。

现在即可在 imagine.vercel.sh 上试用该模型，它运行于 AI Gateway。

要使用 Grok Imagine Image 2.0 Preview，请将模型设置为 `xai/grok-imagine-image-2.0-preview`，并通过 AI SDK 调用 `generateImage`。

```
1import { generateImage } from 'ai';2
3const { images } = await generateImage({4  model: 'xai/grok-imagine-image-2.0-preview',5  prompt: 'An infographic tracing letterforms from movable type to digital fonts.',6});
```

在 `providerOptions.xai` 下设置 `resolution` 为 `1k` 或 `2k` 以选择输出档位，设置 `n` 以在单次调用中生成多张图像。

对于图像编辑，在 `prompt.images` 中传入图像及指令，模型将只修改你要求的部分，其余保持不变：

```
1import { readFileSync } from 'node:fs';2import { generateImage } from 'ai';3
4const { images } = await generateImage({5  model: 'xai/grok-imagine-image-2.0-preview',6  prompt: {7    text: 'Change the title to a monospace font.',8    images: [readFileSync('./letterforms.png')],9  },10});
```

要查看 AI Gateway 支持的所有图像模型，请参阅完整列表。

---

> 本文由AI自动翻译，原文链接：[Grok Imagine Image 2.0 now available on Vercel AI Gateway - Vercel](https://vercel.com/changelog/grok-imagine-image-2-0-preview-now-available-on-vercel-ai-gateway)
> 
> 翻译时间：2026-08-11 03:38
