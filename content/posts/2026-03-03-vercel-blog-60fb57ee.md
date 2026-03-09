---
title: Gemini 3.1 Flash Lite模型登陆Vercel AI Gateway
title_original: Gemini 3.1 Flash Lite is now on AI Gateway - Vercel
date: '2026-03-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/gemini-3-1-flash-lite-is-now-on-ai-gateway
author: ''
summary: 谷歌最新轻量级模型Gemini 3.1 Flash Lite现已集成至Vercel的AI Gateway平台。该模型在翻译、数据提取和代码补全等任务上表现优于前代2.5
  Flash Lite，特别适合高吞吐量的智能体任务及对预算和延迟敏感的应用场景。AI Gateway为用户提供了统一的API接口，支持模型调用、成本跟踪、性能优化及智能路由等功能，并内置了可观测性和自动重试机制，提升了服务的可靠性与易用性。
categories:
- AI基础设施
tags:
- Gemini
- AI Gateway
- Vercel
- 大模型
- AI开发工具
draft: false
translated_at: '2026-03-09T04:49:47.671651'
---

谷歌的 Gemini 3.1 Flash Lite 现已登陆 AI Gateway。

该模型在整体质量上超越了 2.5 Flash Lite，在翻译、数据提取和代码补全方面有显著提升。Gemini 3.1 Flash Lite 最适合高吞吐量的 Agent（智能体）任务、数据提取，以及预算和延迟为主要评估约束的应用场景。

要使用此模型，请在 AI SDK 中设置 `model: 'google/gemini-3.1-flash-lite-preview'`。该模型支持四种思维级别：`minimal`、`low`、`medium` 和 `high`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'google/gemini-3.1-flash-lite-preview',5  prompt:6    `Translate this customer support article from English to Japanese,7     preserving formatting and technical terms.`,8  providerOptions: {9    google: {10      thinkingConfig: {11        thinkingLevel: 'medium',12        includeThoughts: true,13      },14    },15  },16});
```

AI Gateway 提供了一个统一的 API，用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它内置了可观测性、支持自带密钥，并具备带自动重试的智能供应商路由功能。

了解更多关于 [AI Gateway](https://s.ai-gateway) 的信息，查看 [AI Gateway 模型排行榜](https://s.ai-leaderboard) 或在我们的 [模型游乐场](https://s.ai-playground) 中试用。

---

> 本文由AI自动翻译，原文链接：[Gemini 3.1 Flash Lite is now on AI Gateway - Vercel](https://vercel.com/changelog/gemini-3-1-flash-lite-is-now-on-ai-gateway)
> 
> 翻译时间：2026-03-09 04:49
