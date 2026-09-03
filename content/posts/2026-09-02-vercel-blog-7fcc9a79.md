---
title: GLM-5.3 is 50% off through DigitalOcean on AI Gateway - Vercel
title_original: GLM-5.3 is 50% off through DigitalOcean on AI Gateway - Vercel
date: '2026-09-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/glm-5-3-is-50-off-through-digitalocean-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  GLM-5.3is 50% off on AI Gateway through Tuesday, September 8, in partnership with
  DigitalOcean.


  ## Copy link to headingHow to use the mo...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-03T07:04:14.328897'
---

[翻译失败，原文如下]

GLM-5.3is 50% off on AI Gateway through Tuesday, September 8, in partnership with DigitalOcean.

## Copy link to headingHow to use the model during the offer period

- Using the promo name (zai/glm-5.3-promo-50) gets the discounted rate. It routes only to DigitalOcean, with no fallback to another provider, and it stops serving when the offer ends.
- Using the standard name (i.e.,zai/glm-5.3) with provider options to sort DigitalOcean as the preferred provider keeps working after September 8 and routes across every provider that serves the model, at their usual rates.

Using the promo name (zai/glm-5.3-promo-50) gets the discounted rate. It routes only to DigitalOcean, with no fallback to another provider, and it stops serving when the offer ends.

Using the standard name (i.e.,zai/glm-5.3) with provider options to sort DigitalOcean as the preferred provider keeps working after September 8 and routes across every provider that serves the model, at their usual rates.

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'zai/glm-5.3-promo-50',5  prompt: 'Add error recovery to the data ingestion pipeline.',6});
```

Because the promo name goes away when the offer ends, treat it as something you switch on for the window rather than hardcode. To keep the standard name in your code instead, pin the provider withorder: ['digitalocean']underproviderOptions.gateway, which prefers DigitalOcean and falls back to the others if it cannot serve the request.

GLM-5.3 takes text input, with a 1M token context window and a maximum output of 128K tokens. Discounted requests appear in your spend dashboard and carry a trace like any other request.

TryGLM-5.3in the model playground.

To use it in a coding agent, see thecoding agents guide, then runvercel ai-gateway coding-agents setupto connect agents like Claude Code, Codex, OpenCode, Cursor, Pi, and more and selectzai/glm-5.3-promo-50inside the agent.

You can viewall language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[GLM-5.3 is 50% off through DigitalOcean on AI Gateway - Vercel](https://vercel.com/changelog/glm-5-3-is-50-off-through-digitalocean-on-ai-gateway)
> 
> 翻译时间：2026-09-03 07:04
