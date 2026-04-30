---
title: Grok 4.20登陆Vercel AI Gateway，三种变体齐发
title_original: Try Grok 4.20 on AI Gateway - Vercel – Vercel
date: '2026-03-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/grok-4-20-on-ai-gateway
author: ''
summary: xAI最新旗舰模型Grok 4.20现已通过Vercel AI Gateway提供三种变体：非推理型（优化速度与直接响应）、推理型（针对复杂问题扩展思考）和多Agent型（专为多智能体编排与协作构建）。该模型具备低幻觉率、严格的提示词遵循能力和行业领先的速度，支持工具调用。开发者可通过AI
  SDK设置模型标识符进行调用。AI Gateway还提供统一API、使用追踪、成本管理、重试与故障转移等基础设施能力。
categories:
- AI基础设施
tags:
- Grok 4.20
- Vercel AI Gateway
- xAI
- AI模型
- 多智能体
draft: false
translated_at: '2026-04-30T05:32:54.167529'
---

Grok 4.20 现已在 Vercel AI Gateway 上以三种变体提供：推理型、非推理型和多 Agent（智能体）型。作为 xAI 最新的旗舰模型，Grok 4.20 提供了行业领先的速度和 Agent（智能体）工具调用能力。它具有低幻觉率和严格的提示词遵循能力，能够生成精确的响应。

- Grok 4.20 非推理型：针对速度和直接响应优化的非推理变体
- Grok 4.20 推理型：针对复杂问题解决任务的扩展思考
- Grok 4.20 多 Agent（智能体）型：专为多 Agent（智能体）编排与协作而构建

Grok 4.20 非推理型：针对速度和直接响应优化的非推理变体

Grok 4.20 推理型：针对复杂问题解决任务的扩展思考

Grok 4.20 多 Agent（智能体）型：专为多 Agent（智能体）编排与协作而构建

要使用 Grok 4.20，请在 AI SDK 中将模型设置为 `xai/grok-4.20-non-reasoning-beta`、`xai/grok-4.20-reasoning-beta` 或 `xai/grok-4.20-multi-agent-beta`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'xai/grok-4.20-reasoning-beta',5  prompt:6    `Analyze this dataset for anomalies, cross-reference7     against our historical baselines, and generate8     a summary report with recommended actions.`,9});
```

AI Gateway 提供了一个统一的 API，用于调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商正常运行时间的可用性。它内置了可观测性、自带密钥支持，以及带有自动重试的智能提供商路由。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Try Grok 4.20 on AI Gateway - Vercel – Vercel](https://vercel.com/changelog/grok-4-20-on-ai-gateway)
> 
> 翻译时间：2026-04-30 05:32
