---
title: Wan 3.0 now available on AI Gateway - Vercel
title_original: Wan 3.0 now available on AI Gateway - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/wan-3-0-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Wan 3.0 from Alibabais now available on AI Gateway asalibaba/wan-v3.0-video.


  Wan 3.0 combines text-to-video, image-to-video, first- and ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:11:35.099377'
---

[翻译失败，原文如下]

Wan 3.0 from Alibabais now available on AI Gateway asalibaba/wan-v3.0-video.

Wan 3.0 combines text-to-video, image-to-video, first- and last-frame conditioning, and reference-based generation in one model. References can include images, video, and audio. It generates clips up to 30 seconds at 30 fps in 480p, 720p, or 1080p, with synchronized audio.

Previously, Wan 2.7 required separate-t2vand-r2vmodel IDs and was limited to 15-second clips at 24 fps.

## Copy link to headingGenerate a video

Wan 3.0 supportsasynchronous generation, so no HTTP request needs to remain open for the entire render.

Pass awebhookto receive an event when the generation finishes:

```
1import { experimental_generateVideo as generateVideo } from 'ai'; 2
3const { videos } = await generateVideo({4  model: 'alibaba/wan-v3.0-video',5  prompt: 'A paper lantern drifting over a harbor at night',6  webhook: async () => ({ 7    url: callbackUrl, 8    received: waitForDelivery(token) 9  }),10});
```

Generate a Wan 3.0 video and receive its completion event through a webhook.

Learn about asynchronous generation options in the docs, including how toverify webhook deliveries.

## Copy link to headingAdd references

Pass image, video, or audio references throughinputReferences, including the source and media type for each one. Images accept hosted URLs or base64. Video and audio references require hosted URLs.

First- and last-frame conditioning accepts one image for each frame and can't be combined with other references.

Try Wan 3.0 in themodel playground, orbrowse all video models.

---

> 本文由AI自动翻译，原文链接：[Wan 3.0 now available on AI Gateway - Vercel](https://vercel.com/changelog/wan-3-0-now-available-on-ai-gateway)
> 
> 翻译时间：2026-08-26 03:11
