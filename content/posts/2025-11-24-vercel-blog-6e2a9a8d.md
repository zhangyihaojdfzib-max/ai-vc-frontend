---
title: Vercel AI Gateway 现已支持 Claude Opus 4.5 模型
title_original: Claude Opus 4.5 now available in Vercel AI Gateway - Vercel
date: '2025-11-24'
source: Vercel Blog
source_url: https://vercel.com/changelog/claude-opus-4-5-now-available-in-vercel-ai-gateway
author: ''
summary: Vercel 宣布其 AI Gateway 现已直接集成 Anthropic 最新模型 Claude Opus 4.5，开发者无需额外供应商账户即可使用。该模型专为高要求推理任务和复杂问题解决设计，在通用智能、视觉能力及编码任务方面表现优异，特别适用于前端开发与智能体工作流。AI
  Gateway 提供统一 API 接口，支持使用量追踪、成本管理、故障转移和性能优化，并内置可观测性工具与供应商路由功能。开发者可通过 AI SDK 指定模型参数并配置新的
  effort 参数来控制 Token 使用级别。
categories:
- AI基础设施
tags:
- Vercel
- Claude Opus
- AI Gateway
- 模型集成
- 开发工具
draft: false
translated_at: '2026-01-26T05:04:33.460345'
---

您现在可以通过 Vercel 的 **AI Gateway** 直接访问 Anthropic 的最新模型 Claude Opus 4.5，无需其他供应商账户。

Claude Opus 4.5 适用于高要求的推理任务和复杂问题解决。与之前的版本相比，该模型在通用智能和视觉能力方面有所提升。它擅长处理困难的编码任务和智能体工作流，尤其是涉及计算机使用和工具使用的场景，并能有效处理上下文使用和外部记忆文件。前端编码和设计是其公认的优势领域，特别是在开发现实世界的 Web 应用程序方面。

要使用 Claude Opus 4.5，请在 AI SDK 中将 `model` 设置为 `anthropic/claude-opus-4.5`。该模型有一个新的 `effort` 参数。此参数会影响所有类型的 Token，并控制响应请求时的 Token 使用级别。默认情况下，`effort` 设置为高，且独立于思考预算。要在 AI Gateway 中通过 AI SDK 使用它，请在 `providerOptions` 中为供应商设置 `effort`，如下例所示。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'anthropic/claude-opus-4.5',5  prompt:6  `Design and build a production-ready SaaS web app with7   real-time analytics, feature flags, dashboards, alerts, RBAC,8   integrations, accessibility, and performance optimization.`,9  providerOptions: {10    anthropic: {11      effort: 'high',12  },13});
```

AI Gateway 提供了一个统一的 API 来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它包括内置的**可观测性**、**自带密钥支持**以及具有自动重试功能的智能**供应商路由**。

阅读**文档**，查看 **AI Gateway 模型排行榜**，或直接在我们的**模型游乐场**中使用 Claude Opus 4.5。

AI Gateway：按使用量追踪顶级 AI 模型

AI Gateway 模型排行榜根据通过网关的所有流量的总 Token 量，对一段时间内使用最多的模型进行排名。定期更新。

---

> 本文由AI自动翻译，原文链接：[Claude Opus 4.5 now available in Vercel AI Gateway - Vercel](https://vercel.com/changelog/claude-opus-4-5-now-available-in-vercel-ai-gateway)
> 
> 翻译时间：2026-01-26 05:04
