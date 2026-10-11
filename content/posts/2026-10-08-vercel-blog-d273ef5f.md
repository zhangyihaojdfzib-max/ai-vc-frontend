---
title: Step 5 Preview now available on AI Gateway - Vercel
title_original: Step 5 Preview now available on AI Gateway - Vercel
date: '2026-10-08'
source: Vercel Blog
source_url: https://vercel.com/changelog/step-5-preview-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Step 5 Preview, StepFun''s flagship model, is now available onAI Gateway. It''s
  built for agentic coding, professional knowledge work, and ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:32:18.416581'
---

[翻译失败，原文如下]

Step 5 Preview, StepFun's flagship model, is now available onAI Gateway. It's built for agentic coding, professional knowledge work, and financial analysis, from building apps and debugging code to research and analytical reports.

Step 5 Preview supports text and image input with a 1M-token context window, allowing you to work with large codebases, a stack of documents, or screenshots and charts in a single request.

Usestepfun/step-5-previewas the model name:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'stepfun/step-5-preview',5  prompt: 'Plan a dashboard for analyzing quarterly financial results.',6});7
8for await (const text of result.textStream) {9  process.stdout.write(text);10}
```

For other coding agents such as Claude Code, Codex, Cursor, and more, install the latest Vercel CLI and run setup:

```
1npm i -g vercel@latest2vercel ai-gateway setup
```

Then selectstepfun/step-5-previewin the agent. See thecoding agents guidefor details.

Try Step 5 Preview in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Step 5 Preview now available on AI Gateway - Vercel](https://vercel.com/changelog/step-5-preview-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-11 08:32
