---
title: 阿里通义千问Qwen 3 Max Thinking模型现已登陆Vercel AI Gateway
title_original: Qwen 3 Max Thinking now available on AI Gateway - Vercel
date: '2026-01-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/qwen-3-max-thinking-now-available-on-ai-gateway
author: ''
summary: 阿里云的通义千问Qwen 3 Max Thinking模型现已在Vercel的AI Gateway上提供。该模型集成了思考与非思考模式，能够自主调用内置的搜索、记忆和代码解释器工具，以提升复杂推理任务的性能并减少幻觉。开发者可通过AI
  SDK直接调用该模型，而AI Gateway则提供了统一的API接口，支持使用情况跟踪、成本管理、故障转移和性能优化等功能，简化了模型集成与运维流程。
categories:
- AI产品
tags:
- 通义千问
- AI Gateway
- Vercel
- 大语言模型
- AI开发工具
draft: false
translated_at: '2026-01-30T04:07:57.973252'
---

您现在可以通过AI Gateway直接访问Qwen 3 Max Thinking，无需其他提供商账户。

Qwen 3 Max Thinking集成了思考与非思考模式，以提升复杂推理任务的性能。该模型能在对话中自主选择并使用其内置的搜索、记忆和代码解释器工具，无需手动选择工具。这些工具有助于减少幻觉并提供实时信息。

要使用此模型，请在AI SDK中将模型设置为`alibaba/qwen3-max-thinking`：

```
1import { streamText } from 'ai'2
3const { textStream } = await streamText({4  model: 'alibaba/qwen3-max-thinking',5  prompt:6   `Research a current topic, verify facts, remember a user preference,7    and include a short code snippet to support the explanation.`,8})
```

AI Gateway提供了一个统一的API，用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于提供商水平的运行时间。它包含内置的可观测性、自带密钥支持以及具备自动重试功能的智能提供商路由。

了解更多关于AI Gateway的信息，查看AI Gateway模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Qwen 3 Max Thinking now available on AI Gateway - Vercel](https://vercel.com/changelog/qwen-3-max-thinking-now-available-on-ai-gateway)
> 
> 翻译时间：2026-01-30 04:07
