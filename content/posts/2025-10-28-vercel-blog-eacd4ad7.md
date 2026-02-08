---
title: MiniMax M2开源模型现可通过Vercel AI网关免费使用
title_original: MiniMax M2 now available for free in Vercel AI Gateway - Vercel
date: '2025-10-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/minimax-m2-now-available-in-vercel-ai-gateway
author: ''
summary: Vercel宣布其AI网关现已集成MiniMax最新开源模型MiniMax M2，用户无需其他供应商账户即可通过统一API调用。该模型专注于智能体应用，每次推理仅激活100亿参数，效率极高，并可免费使用至2025年11月7日。AI网关提供使用追踪、成本管理、性能优化及故障转移等功能，同时支持在AI
  SDK中直接调用。此外，Vercel还提供了模型排行榜和游乐场，方便开发者评估与试用。
categories:
- AI基础设施
tags:
- Vercel
- MiniMax
- 开源模型
- AI网关
- API集成
draft: false
translated_at: '2026-02-08T04:36:47.893631'
---

您现在可以通过Vercel的AI网关访问MiniMax最新的开源模型MiniMax M2，无需其他供应商账户。该模型可免费使用至2025年11月7日。MiniMax M2专注于智能体应用，服务效率极高，每次前向传播仅激活100亿参数。

AI网关允许您通过统一且一致的API调用模型，只需更新一个字符串即可。您可以跟踪使用情况和成本，并配置性能优化、重试和故障转移，以获得高于供应商平均水平的运行时间。

若要在AI SDK中使用它，请将模型设置为`minimax/minimax-m2`：

```
1import { streamText } from 'ai'2
3const result = streamText({4  model: "minimax/minimax-m2",5  prompt: "What is the future of open source LLM models?"6})
```

包含内置可观测性、自带密钥支持以及具备自动重试功能的智能供应商路由。

了解更多关于AI网关的信息，查看AI网关模型排行榜，或在我们的模型游乐场中试用。

AI网关：按使用量追踪顶级AI模型

AI网关模型排行榜根据通过网关的所有流量总Token量，对长期使用最多的模型进行排名。定期更新。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[MiniMax M2 now available for free in Vercel AI Gateway - Vercel](https://vercel.com/changelog/minimax-m2-now-available-in-vercel-ai-gateway)
> 
> 翻译时间：2026-02-08 04:36
