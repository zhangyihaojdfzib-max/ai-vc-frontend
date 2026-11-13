---
title: Inkling 2 Small now available on AI Gateway - Vercel
title_original: Inkling 2 Small now available on AI Gateway - Vercel
date: '2026-11-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/inkling-2-small-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Inkling 2 Small from Thinking Machinesis now available on AI Gateway. The multimodal
  reasoning model supports coding agents, visual under...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:33.311363'
---

[翻译失败，原文如下]

Inkling 2 Small from Thinking Machinesis now available on AI Gateway. The multimodal reasoning model supports coding agents, visual understanding, and professional knowledge work, with text and image inputs and text output.

Inkling 2 Small can work through extended coding tasks, use tools to gather information, and turn that information into documents, spreadsheets, and other deliverables. Its visual capabilities include reading text in images, interpreting charts and infographics, and inspecting interfaces. For visual development, it can use screenshots to check the output of the code it writes and guide the next revision.

Usethinkingmachines/inkling-2-smallas the model name:

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'thinkingmachines/inkling-2-small',5  prompt: 'Write a TypeScript function that groups tasks by status.',6});7
8for await (const text of result.textStream) {9  process.stdout.write(text);10}
```

To use it in Claude Code, Codex, Cursor, and more, install the latest Vercel CLI and run setup:

```
npx vercel ai-gateway setup
```

Then selectthinkingmachines/inkling-2-smallin the agent. See thecoding agents guidefor details.

Try Inkling 2 Small in themodel playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime. It includes built-incustom reporting,Zero Data Retention support,budgets for API keys,routing rules, and more.

AI Gateway reflects provider pricing with no markup and does not charge a platform fee on inference, including onBring Your Own Key(BYOK) requests.

You can viewall language modelsavailable on AI Gateway.

---

> 本文由AI自动翻译，原文链接：[Inkling 2 Small now available on AI Gateway - Vercel](https://vercel.com/changelog/inkling-2-small-now-available-on-ai-gateway)
> 
> 翻译时间：2026-11-13 09:19
