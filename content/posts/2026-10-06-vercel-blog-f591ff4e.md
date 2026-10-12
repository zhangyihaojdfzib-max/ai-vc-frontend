---
title: Nano Banana 2.1 now available on AI Gateway - Vercel
title_original: Nano Banana 2.1 now available on AI Gateway - Vercel
date: '2026-10-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/nano-banana-2-1-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Nano Banana 2.1from Google is now available onAI Gatewayasgoogle/gemini-nano-banana-2.1.


  Compared with earlier Nano Banana models, it im...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:23:13.471637'
---

[翻译失败，原文如下]

Nano Banana 2.1from Google is now available onAI Gatewayasgoogle/gemini-nano-banana-2.1.

Compared with earlier Nano Banana models, it improves image generation and editing, including product recontextualization, mask- and ink-based editing, and factuality. In practice, that means placing products in new scenes, limiting edits to masked or marked regions, and depicting real-world subjects more accurately.

It also renders photorealistic skin tones, detailed materials, sharp lighting, and coherent backgrounds while maintaining Flash-tier latency and cost.

SetAI_GATEWAY_API_KEY, then use the model through theAI SDK, the OpenAI-compatibleChat Completions API, orAI CLI:

```
1import { generateText } from 'ai';2
3const result = await generateText({4  model: 'google/gemini-nano-banana-2.1',5  prompt: 'A studio photo of a ceramic coffee mug on a white background.',6});
```

Try Nano Banana 2.1 inimagen.shor themodel playground. See theimage generation documentationfor additional configuration and editing examples.

Browse allimage modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Nano Banana 2.1 now available on AI Gateway - Vercel](https://vercel.com/changelog/nano-banana-2-1-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-12 08:23
