---
title: Vercel AI网关正式接入Arcee AI开源模型Trinity Mini
title_original: Trinity Mini model now available in Vercel AI Gateway - Vercel
date: '2025-12-01'
source: Vercel Blog
source_url: https://vercel.com/changelog/trinity-mini-model-now-available-in-vercel-ai-gateway
author: ''
summary: Vercel宣布其AI网关现已集成Arcee AI的最新开源模型Trinity Mini。该模型是一个拥有260亿参数（活跃参数30亿）的MoE推理模型，在美国完成端到端训练。开发者无需额外供应商账户，即可通过Vercel
  AI SDK直接调用。AI网关提供统一的API接口，支持使用量追踪、成本管理、故障转移、性能优化及智能路由等功能，并内置可观测性工具。用户可通过文档、模型排行榜或在线游乐场体验该模型。
categories:
- AI基础设施
tags:
- Vercel
- AI网关
- 开源模型
- MoE
- 推理服务
draft: false
translated_at: '2026-01-07T03:12:32.188Z'
---

您现在可以通过Vercel的AI网关访问Arcee AI的最新模型Trinity Mini，无需其他供应商账户。Trinity Mini是一个开源权重的MoE推理模型，拥有260亿参数（活跃参数30亿），在美国进行端到端训练。

要使用Trinity Mini，请在AI SDK中将模型设置为`arcee-ai/trinity-mini`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'arcee-ai/trinity-mini',5  prompt:6  `Generate a full reasoning chain that reconstructs how an unknown machine7   operates solely from its final outputs, inferring internal mechanisms,8   intermediate states, and causal links step by step.`,9});
```

AI网关提供了一个统一的API来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它内置了可观测性、支持自带密钥以及智能供应商路由与自动重试功能。

阅读文档，查看AI网关模型排行榜，或直接在我们的模型游乐场中使用该模型。

AI网关：按使用量追踪顶级AI模型

AI网关模型排行榜根据通过网关的所有流量的总Token量，对一段时间内使用最多的模型进行排名。榜单定期更新。

---

> 本文由AI自动翻译，原文链接：[Trinity Mini model now available in Vercel AI Gateway - Vercel](https://vercel.com/changelog/trinity-mini-model-now-available-in-vercel-ai-gateway)
> 
> 翻译时间：2026-01-07 02:46
