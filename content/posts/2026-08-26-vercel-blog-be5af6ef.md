---
title: Muse Image now available on AI Gateway - Vercel
title_original: Muse Image now available on AI Gateway - Vercel
date: '2026-08-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/muse-image-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Muse Imagefrom Meta Superintelligence Labs is now available on AI Gateway. It is
  their first image model and a separate family from Muse ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-31T07:59:46.953744'
---

[翻译失败，原文如下]

Muse Imagefrom Meta Superintelligence Labs is now available on AI Gateway. It is their first image model and a separate family from Muse Spark, returning images rather than text. Send a prompt and get an image back, or send an image with an instruction and get it changed. One model does both, so you don't switch models to move from generating to editing.

To use Muse Image, setmodeltometa/muse-image-1.0and callgenerateImagefrom theAI SDK:

```
1import { generateImage } from 'ai';2
3const { images } = await generateImage({4  model: 'meta/muse-image-1.0',5  prompt: 'A conference poster for a talk on database indexes.',6});
```

To steer the result toward art you already have, pass reference images inprompt.imagesalongside the text, and the model blends them into what it draws.

## Copy link to headingEditing

Pass the image you want changed inprompt.imageswith an instruction, and the model changes what you asked for and leaves the rest:

```
1import { readFileSync } from 'node:fs';2import { generateImage } from 'ai';3
4const { images } = await generateImage({5  model: 'meta/muse-image-1.0',6  prompt: {7    text: 'Move the date to the bottom right and make it larger.',8    images: [readFileSync('./poster.png')],9  },10});
```

Try Muse Image in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall image modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Muse Image now available on AI Gateway - Vercel](https://vercel.com/changelog/muse-image-now-available-on-ai-gateway)
> 
> 翻译时间：2026-08-31 07:59
