---
title: GLM 5.3 FlashX now available on AI Gateway - Vercel
title_original: GLM 5.3 FlashX now available on AI Gateway - Vercel
date: '2026-09-18'
source: Vercel Blog
source_url: https://vercel.com/changelog/glm-5-3-flashx-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  GLM 5.3 FlashXis now available on AI Gateway.


  GLM 5.3 FlashX is a high-speed serving option for Z.ai''s multimodal coding model,
  deliveri...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-20T07:20:56.967686'
---

[翻译失败，原文如下]

GLM 5.3 FlashXis now available on AI Gateway.

GLM 5.3 FlashX is a high-speed serving option for Z.ai's multimodal coding model, delivering inference at ~200 tokens per second for faster streamed responses.

The higher serving speed is useful for coding agents, tool loops, and interactive applications where users wait on generated output.

Usezai/glm-5.3-flashxacross API formats and in coding agents:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'zai/glm-5.3-flashx',5  prompt: 'Name three checks to run after deploying a latency-sensitive API',6});7
8for await (const text of result.textStream) {9  process.stdout.write(text);10}
```

To use it in a coding agent, see thecoding agents guide, then runvercel ai-gateway setupto create a key and configure your supported agents. Selectzai/glm-5.3-flashxinside the agent.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

TryGLM-5.3-FlashX in the model playground, orview all language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[GLM 5.3 FlashX now available on AI Gateway - Vercel](https://vercel.com/changelog/glm-5-3-flashx-now-available-on-ai-gateway)
> 
> 翻译时间：2026-09-20 07:20
