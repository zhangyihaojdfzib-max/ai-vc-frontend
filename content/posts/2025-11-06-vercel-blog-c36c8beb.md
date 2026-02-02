---
title: 月之暗面Kimi K2思维模型现可通过Vercel AI Gateway调用
title_original: Moonshot AI's Kimi K2 Thinking models are now available on Vercel
  AI Gateway - Vercel
date: '2025-11-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/moonshot-ai-kimi-k2-thinking-and-kimi-k2-thinking-turbo-are-now-available
author: ''
summary: 月之暗面（Moonshot AI）最新推出的深度推理模型Kimi K2 Thinking及其高速版Kimi K2 Thinking Turbo，现已集成至Vercel
  AI Gateway。开发者可通过统一的API直接调用这些模型，无需单独供应商账户。Kimi K2 Thinking作为开源模型，擅长处理复杂推理任务，支持多达200-300个连续工具调用，在基准测试中表现优异。AI
  Gateway提供了使用追踪、成本管理、性能优化及故障转移等功能，简化了模型集成与管理流程。
categories:
- AI基础设施
tags:
- Moonshot AI
- Vercel
- AI Gateway
- 推理模型
- API集成
draft: false
translated_at: '2026-02-02T04:23:10.719008'
---

您现在可以通过 Vercel 的 AI Gateway 访问月之暗面（Moonshot AI）最新、最强大的思维模型——Kimi K2 Thinking 和 Kimi K2 Thinking Turbo，无需其他供应商账户。

Kimi K2 Thinking 是开源的，擅长深度推理，能处理多达 200-300 个连续的工具调用，并在推理和编码基准测试中取得了顶尖成绩。Kimi K2 Thinking Turbo 是 Kimi K2 Thinking 的高速版本，最适合需要深度推理和低延迟的场景。

AI Gateway 允许您通过统一且一致的 API 调用模型，只需更新一个字符串即可，同时还能跟踪使用情况和成本，并配置性能优化、重试和故障转移，以实现高于供应商平均水平的正常运行时间。

要在 AI SDK 中使用它，请将模型设置为 `moonshotai/kimi-k2-thinking` 或 `moonshotai/kimi-k2-thinking-turbo`：

```
1import { streamText } from 'ai'2
3const result = streamText({4  model: "moonshotai/kimi-k2-thinking",5  prompt: "Please help me generate a technology and economic news report"6})
```

包含内置的可观测性、自带密钥支持以及具有自动重试功能的智能供应商路由。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

AI Gateway：按使用量追踪顶级 AI 模型

AI Gateway 模型排行榜根据通过网关的所有流量的总 Token 量，对一段时间内使用最多的模型进行排名。定期更新。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[Moonshot AI's Kimi K2 Thinking models are now available on Vercel AI Gateway - Vercel](https://vercel.com/changelog/moonshot-ai-kimi-k2-thinking-and-kimi-k2-thinking-turbo-are-now-available)
> 
> 翻译时间：2026-02-02 04:23
