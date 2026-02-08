---
title: OpenAI开源模型GPT-OSS-Safeguard-20B现已登陆Vercel AI网关
title_original: OpenAI's GPT-OSS-Safeguard-20B now available in Vercel AI Gateway
  - Vercel
date: '2025-10-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/openai-gpt-oss-safeguard-20b-now-available-in-vercel-ai-gateway
author: ''
summary: Vercel宣布其AI网关现已支持OpenAI最新的开源模型GPT-OSS-Safeguard-20B。该模型是通用GPT-OSS的微调版本，专为开发者设计，用于实现策略驱动的内容审核。通过Vercel
  AI网关，开发者可以使用统一的API调用该模型，并享受使用量追踪、成本管理、性能优化、自动重试和故障转移等功能，从而获得更高的服务可用性。文章还介绍了如何在AI
  SDK中集成该模型，并提及了AI网关提供的模型排行榜和游乐场等辅助功能。
categories:
- AI基础设施
tags:
- OpenAI
- Vercel
- AI网关
- 开源模型
- 内容审核
draft: false
translated_at: '2026-02-08T04:36:32.341796'
---

您现在可以通过Vercel的AI网关访问OpenAI最新的开源模型GPT-OSS-Safeguard-20B，无需其他供应商账户。

GPT-OSS-Safeguard-20B是其通用GPT-OSS模型的微调版本，专为开发者设计，用于实现自定义的、策略驱动的内容审核。

AI网关允许您通过统一且一致的API调用模型，只需更新单个字符串即可跟踪使用情况和成本，并配置性能优化、重试和故障转移，以实现高于供应商平均水平的正常运行时间。

若要在AI SDK中使用，请将模型设置为openai/gpt-oss-safeguard-20b：

```
1import { streamText } from 'ai'2
3const result = streamText({4  model: "openai/gpt-oss-safeguard-20b",5  prompt: "Why are safety classification models important?"6})
```

内置可观测性、支持自带密钥以及具备自动重试功能的智能供应商路由。

了解更多关于AI网关的信息，查看AI网关模型排行榜，或在我们的模型游乐场中试用。

AI网关：按使用量追踪顶级AI模型

AI网关模型排行榜根据通过网关的所有流量总Token量，对长期使用最多的模型进行排名。定期更新。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[OpenAI's GPT-OSS-Safeguard-20B now available in Vercel AI Gateway - Vercel](https://vercel.com/changelog/openai-gpt-oss-safeguard-20b-now-available-in-vercel-ai-gateway)
> 
> 翻译时间：2026-02-08 04:36
