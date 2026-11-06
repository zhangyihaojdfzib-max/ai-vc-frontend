---
title: Gemini Omni 1.2 Flash now available on AI Gateway - Vercel
title_original: Gemini Omni 1.2 Flash now available on AI Gateway - Vercel
date: '2026-11-05'
source: Vercel Blog
source_url: https://vercel.com/changelog/gemini-omni-1-2-flash-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Gemini Omni 1.2 Flashfrom Google is now available on AI Gateway. Generate videos
  from text prompts with one API key and no separate Googl...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-06T09:06:20.454957'
---

[翻译失败，原文如下]

Gemini Omni 1.2 Flashfrom Google is now available on AI Gateway. Generate videos from text prompts with one API key and no separate Google account.

Gemini Omni 1.2 Flash generates 3–15 second videos with native audio and edits 3–15 second source clips with up to six reference images. Extend videos by 3–10 seconds per call, up to 30 seconds total, or refine generated clips in follow-up calls usingpreviousInteractionId. Output supports 360p, 720p, 1080p, and 4K in 16:9 or 9:16. UsegenerateTextorstreamTextinAI SDKto receive the generated video as a file.

## Copy link to headingGenerate a video

Usegoogle/gemini-omni-1.2-flashas the model name. This example generates a three-second, 360p clip and saves it asvideo.mp4:

```
1import { writeFile } from 'node:fs/promises';2import { generateText } from 'ai';3
4const { files } = await generateText({5  model: 'google/gemini-omni-1.2-flash',6  prompt: 'A red ball rolls across a white table.',7  providerOptions: {8    google: {9      responseModalities: ['text', 'video'],10      responseFormat: [11        { type: 'video', resolution: '360p', duration: '3s' },12      ],13    },14  },15});16
17const video = files.find(file => file.mediaType === 'video/mp4');18if (!video) throw new Error('No MP4 video returned');19
20await writeFile('video.mp4', video.uint8Array);
```

## Copy link to headingReceive video in a streaming response

WithstreamText, readfullStreamto handle generated files as they arrive. The video is delivered as a completed file:

```
1import { writeFile } from 'node:fs/promises';2import { streamText } from 'ai';3
4const result = streamText({5  model: 'google/gemini-omni-1.2-flash',6  prompt: 'A red ball rolls across a white table.',7  providerOptions: {8    google: {9      responseModalities: ['text', 'video'],10      responseFormat: [11        { type: 'video', resolution: '360p', duration: '3s' },12      ],13    },14  },15});16
17for await (const part of result.fullStream) {18  if (part.type === 'file' && part.file.mediaType === 'video/mp4') {19    await writeFile('video.mp4', part.file.uint8Array);20  } else if (part.type === 'error') {21    throw part.error;22  }23}
```

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

Explore more models in theAI Gateway model catalog.

---

> 本文由AI自动翻译，原文链接：[Gemini Omni 1.2 Flash now available on AI Gateway - Vercel](https://vercel.com/changelog/gemini-omni-1-2-flash-now-available-on-ai-gateway)
> 
> 翻译时间：2026-11-06 09:06
