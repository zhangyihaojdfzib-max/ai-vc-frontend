---
title: Elorian AI's Glimpse now available on AI Gateway - Vercel
title_original: Elorian AI's Glimpse now available on AI Gateway - Vercel
date: '2026-10-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/elorian-ai-glimpse-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Glimpse from Elorianis now available on AI Gateway. The visual reasoning model accepts
  images and video to follow objects through motion,...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T07:19:54.834006'
---

[翻译失败，原文如下]

Glimpse from Elorianis now available on AI Gateway. The visual reasoning model accepts images and video to follow objects through motion, interpret spatial relationships, and connect an action to its physical consequences.

Glimpse can return to visual evidence as it works: zooming into a detail, revisiting a short interval of video, or tracking the same feature across frames. This allows the model to support use cases like scientific chart analysis, video captioning, visual counting, and robotics data annotation.

Some examples include checking a train's motion to determine whether it is slowing down, keeping objects distinct through camera movement, and labeling completed actions in robot footage.

Useelorian/glimpseas the model name:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'elorian/glimpse',5  messages: [{6    role: 'user',7    content: [8      { type: 'text', text: 'Describe this image in one sentence.' },9      {10        type: 'file',11        mediaType: 'image/jpeg',12        data: new URL('https://elorian.ai/assets/blog/glimpse/open-pliers.jpg'),13      },14    ],15  }],16  maxOutputTokens: 4096,17  reasoning: 'low'18});19
20for await (const text of result.textStream) {21  process.stdout.write(text);22}
```

With AI SDK 7, you can send a video as a file part. Replace the placeholder URL with a public or signed HTTPS URL for your video:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'elorian/glimpse',5  maxOutputTokens: 4096,6  messages: [{7    role: 'user',8    content: [9      { type: 'text', text: 'Describe the visible scene in at most five words. Do not use code or search.' },10      {11        type: 'file',12        data: new URL('https://example.com/your-video.mp4'),13        mediaType: 'video/mp4',14      },15    ],16  }],17  reasoning: 'low',18  providerOptions: { elorian: { video_fps: 1 } }19});20
21for await (const text of result.textStream) {22  process.stdout.write(text);23}
```

To configure AI Gateway in Claude Code, Codex, Cursor, and more, install the latest Vercel CLI and run setup:

```
npx vercel ai-gateway setup
```

Try Glimpse in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

---

> 本文由AI自动翻译，原文链接：[Elorian AI's Glimpse now available on AI Gateway - Vercel](https://vercel.com/changelog/elorian-ai-glimpse-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-21 07:19
