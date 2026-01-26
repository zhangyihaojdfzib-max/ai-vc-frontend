---
title: Vercel AI Gateway 现已支持谷歌 Gemini 3 Flash 模型
title_original: Gemini 3 Flash is now available on the Vercel AI Gateway - Vercel
date: '2025-12-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/gemini-3-flash-is-now-available-on-the-vercel-ai-gateway
author: Authors
summary: 本文宣布谷歌最新的 Gemini 3 Flash 模型现已通过 Vercel AI Gateway 提供。该模型是谷歌最智能的模型之一，专为速度优化，在保持
  Gemini 3 专业级推理能力的同时，实现了闪电级的响应速度、更高的效率以及更低的成本。文章指出，Gemini 3 Flash 在多数基准测试中超越了前代 Gemini
  2.5 Pro 模型，不仅速度快3倍、使用的 Token 数量减少30%，成本也仅为几分之一。用户可通过 AI SDK 轻松调用该模型。Vercel AI Gateway
  提供了一个统一的 API 接口，用于调用各类模型、跟踪使用情况和成本，并集成了可观测性、智能路由、自动重试等运维功能，旨在提供高于单一供应商水平的服务可用性。
categories:
- AI基础设施
tags:
- Vercel
- Gemini
- AI Gateway
- 模型部署
- API网关
draft: false
translated_at: '2026-01-06T01:18:27.899Z'
---

1 分钟阅读
您现在可以通过 Vercel 的 AI Gateway 访问谷歌最新的 Gemini 模型 Gemini 3 Flash，无需其他提供商账户。
这是谷歌最智能的模型，专为速度优化，兼具 Gemini 3 的专业级推理能力和闪电级的延迟、效率与成本。Gemini 3 Flash 性能显著超越之前的 Gemini 2.5 模型，在大多数基准测试中击败了 Gemini 2.5 Pro，同时使用的 Token 数量减少 30%，速度快 3 倍，而成本仅为几分之一。
要在 AI SDK 中使用 Gemini 3 Flash，请将模型设置为 `google/gemini-3-flash`：
```javascript
import { streamText } from 'ai';
const result = streamText({ model: 'google/gemini-3-flash', prompt: `Produce a step-by-step analysis that solves a novel problem, exposes intermediate logic, and delivers a final answer using minimal tokens and maximal inference density.` providerOptions: { google: { thinkingLevel: 'high', includeThoughts: true }, },});
```
AI Gateway 提供了一个统一的 API 来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商水平的正常运行时间。它包含内置的可观测性、自带密钥支持以及具有自动重试功能的智能提供商路由。
了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。
AI Gateway：按使用量追踪顶级 AI 模型
AI Gateway 模型排行榜根据通过网关的所有流量的总 Token 量，对一段时间内使用最多的模型进行排名。定期更新。
查看排行榜


> 本文由AI自动翻译，原文链接：[Gemini 3 Flash is now available on the Vercel AI Gateway - Vercel](https://vercel.com/changelog/gemini-3-flash-is-now-available-on-the-vercel-ai-gateway)
> 
> 翻译时间：2026-01-06 01:18
