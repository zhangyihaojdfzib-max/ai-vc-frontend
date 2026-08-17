---
title: Grok 4.6登陆Vercel AI Gateway，支持多级推理
title_original: Grok 4.6 now available on AI Gateway - Vercel
date: '2026-08-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/grok-4-6-now-available-on-ai-gateway
author: ''
summary: Vercel宣布Grok 4.6现已在AI Gateway上可用，该模型来自SpaceXAI，拥有500K Token上下文窗口，支持文本和图像输入，并提供低、中、高、超高四种推理级别。开发者可通过AI
  SDK或编码Agent（如Claude Code、Codex等）集成使用。AI Gateway提供统一API、成本跟踪、重试与故障转移等功能，且不加价、不收取推理平台费用。文章还提及模型排行榜功能，帮助用户追踪热门模型。
categories:
- AI基础设施
tags:
- Grok 4.6
- AI Gateway
- Vercel
- 模型推理
- 开发者工具
draft: false
translated_at: '2026-08-17T02:58:12.810671'
---

Grok 4.6（来自SpaceXAI）现已在AI Gateway上可用。

该模型拥有500K Token的上下文窗口，支持文本和图像输入。Grok 4.6支持低、中、高和超高四种推理级别，默认设置为高。

要在AI SDK中使用Grok 4.6，请将模型设置为xai/grok-4.6：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'xai/grok-4.6',5  reasoning: 'xhigh',6  prompt: 'Analyze this dataset and summarize the key trends.',7});
```

要在编码Agent中使用它，请运行vercel ai-gateway coding-agents setup来连接Claude Code、Codex、OpenCode或Pi，然后在Agent中选择xai/grok-4.6。

如需无代码试用Grok 4.5，可在模型游乐场中体验。

AI Gateway提供统一的API，用于调用模型、跟踪使用量和成本，并配置重试、故障转移和性能优化，以实现高于提供商的服务可用性。它还内置了自定义报告、零数据保留支持、API密钥预算、路由规则等功能。

AI Gateway反映提供商定价，不加价，且不收取推理平台费用，包括自带密钥（BYOK）请求。

AI Gateway：按使用量追踪顶级AI模型

AI Gateway模型排行榜会随时间追踪最热门的模型，按所有Gateway流量中处理的Token总量进行排名。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[Grok 4.6 now available on AI Gateway - Vercel](https://vercel.com/changelog/grok-4-6-now-available-on-ai-gateway)
> 
> 翻译时间：2026-08-17 02:58
