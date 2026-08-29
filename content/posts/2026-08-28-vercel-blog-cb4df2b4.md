---
title: Hy4 Preview now available on AI Gateway - Vercel
title_original: Hy4 Preview now available on AI Gateway - Vercel
date: '2026-08-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/hy4-preview-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Hy4 Preview from Tencentis now available on AI Gateway.


  Hy4 Preview is an open-source Mixture-of-Experts model with 770B total parameter...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-29T08:49:24.458447'
---

[翻译失败，原文如下]

Hy4 Preview from Tencentis now available on AI Gateway.

Hy4 Preview is an open-source Mixture-of-Experts model with 770B total parameters  and 49B active per token, aimed at long-horizon coding, document analysis, game development, and scientific reasoning. It serves a context window of 1M tokens.

To use Hy4 Preview, setmodeltotencent/hy4-previewin theAI SDK:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'tencent/hy4-preview',5  prompt: 'Add pagination to the results endpoint.',6});
```

To use it in a coding agent, see thecoding agents guide, then runvercel ai-gateway coding-agents setupto connect agents like Claude Code, Codex, OpenCode, Cursor, Pi, and more and selecttencent/hy4-previewinside the agent.

Try Hy4 Preview in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Hy4 Preview now available on AI Gateway - Vercel](https://vercel.com/changelog/hy4-preview-now-available-on-ai-gateway)
> 
> 翻译时间：2026-08-29 08:49
