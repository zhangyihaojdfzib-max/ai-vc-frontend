---
title: FLUX 3 Image now available on AI Gateway - Vercel
title_original: FLUX 3 Image now available on AI Gateway - Vercel
date: '2026-10-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/flux-3-image-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  FLUX 3 Imagefrom Black Forest Labs is now available on AI Gateway. Generate images
  from text or edit existing images using the same model...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:23:11.811668'
---

[翻译失败，原文如下]

FLUX 3 Imagefrom Black Forest Labs is now available on AI Gateway. Generate images from text or edit existing images using the same model, with one API key and no Black Forest Labs account required.

FLUX 3 Image supports up to ten reference images for editing, combining subjects, or changing the composition. It supports five resolution tiers from 768 × 768 to 4K, with square, portrait, and landscape aspect ratios.

SetAI_GATEWAY_API_KEY, then usebfl/flux-3-imageas the model ID in AI SDK 7 or later. To generate an image, callgenerateImagewith a text prompt:

```
1import { generateImage } from 'ai';2
3const { image } = await generateImage({4  model: 'bfl/flux-3-image',5  prompt: 'A blue ceramic vase with wildflowers on a sunlit wooden table.',6  aspectRatio: '1:1',7  providerOptions: {8    blackForestLabs: { resolution: '1k' },9  },10});
```

Generate a square, 1K-resolution image with FLUX 3 Image and the AI SDK.

To edit an image, pass it inprompt.imageswith an instruction. This example edits the image generated above:

```
1const { image: editedImage } = await generateImage({2  model: 'bfl/flux-3-image',3  prompt: {4    text: 'Change the vase to terracotta and keep the flowers and setting.',5    images: [image.uint8Array],6  },7  aspectRatio: '1:1',8  providerOptions: {9    blackForestLabs: { resolution: '1k' },10  },11});
```

Edit the generated image while preserving the flowers and setting.

You can also use FLUX 3 Image from the terminal using the same AI Gateway API key and model ID withAI CLI.

```
npx ai-cli image 'A blue ceramic vase with wildflowers on a sunlit wooden table.' \  --model bfl/flux-3-image \  --output ./renders/
```

Try FLUX 3 Image in themodel playground, or see theimage generation guide.

---

> 本文由AI自动翻译，原文链接：[FLUX 3 Image now available on AI Gateway - Vercel](https://vercel.com/changelog/flux-3-image-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-12 08:23
