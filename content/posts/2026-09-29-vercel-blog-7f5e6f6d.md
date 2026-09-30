---
title: GPT-6.1 Sol now available on AI Gateway - Vercel
title_original: GPT-6.1 Sol now available on AI Gateway - Vercel
date: '2026-09-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/gpt-6-1-sol-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  GPT-6.1 Solfrom OpenAI is now available on AI Gateway. It improves on GPT-6 Sol
  for coding, computer use, and professional work, includin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-30T08:14:46.513838'
---

[翻译失败，原文如下]

GPT-6.1 Solfrom OpenAI is now available on AI Gateway. It improves on GPT-6 Sol for coding, computer use, and professional work, including reading complex documents and carrying out multi-step workflows.

The model is suited to agents that need to debug code, work through business tasks, or extract answers from PDFs with tables and charts. It also improves factual accuracy on difficult questions. Its standard input and output pricing is lower than GPT-6 Astra's, while cheaper cached input makes it useful for requests that reuse a long shared context.

Useopenai/gpt-6.1-solas the model name with theAI SDK,OpenAI-compatible Chat Completions API, orResponses API. You can also select it incoding agentsconnected to AI Gateway:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'openai/gpt-6.1-sol',5  prompt: 'Investigate the failing tests, fix the issue, and summarize the changes.',6});
```

To use the model in coding agents like Codex, Cursor, and more, install the latest Vercel CLI and run setup:

```
1npm i -g vercel@latest2vercel ai-gateway setup
```

Then selectopenai/gpt-6.1-solin the agent. See thecoding agents guidefor details.

Try GPT-6.1 Sol in theplaygroundandlearnmore about theGPT-6 model family.

---

> 本文由AI自动翻译，原文链接：[GPT-6.1 Sol now available on AI Gateway - Vercel](https://vercel.com/changelog/gpt-6-1-sol-now-available-on-ai-gateway)
> 
> 翻译时间：2026-09-30 08:14
