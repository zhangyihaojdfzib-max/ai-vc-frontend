---
title: Strix now supports Vercel AI Gateway - Vercel
title_original: Strix now supports Vercel AI Gateway - Vercel
date: '2026-10-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/strix-now-supports-vercel-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Strix, the open-source AI penetration testing tool, can now run on any of the 400+
  models on VercelAI Gateway.


  Strix can reach models fr...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:56.901106'
---

[翻译失败，原文如下]

Strix, the open-source AI penetration testing tool, can now run on any of the 400+ models on VercelAI Gateway.

Strix can reach models from Anthropic, OpenAI, Kimi, GLM, Deepseek, and others through a single API with no markup, removing the need to sign up for multiple providers. Usage and cost are tracked across all models in AI Gateway.

Strix selects the Gateway throughSTRIX_LLM, where the model is the standard AI Gateway<provider>/<model>ID behind avercel_ai_gateway/prefix:

```
1export STRIX_LLM="vercel_ai_gateway/zai/glm-5.3"2export LLM_API_KEY="your-ai-gateway-api-key"
```

SeeStrix's AI Gateway setup guideto configure it and get started today.

## Contributors

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[Strix now supports Vercel AI Gateway - Vercel](https://vercel.com/changelog/strix-now-supports-vercel-ai-gateway)
> 
> 翻译时间：2026-10-30 08:47
