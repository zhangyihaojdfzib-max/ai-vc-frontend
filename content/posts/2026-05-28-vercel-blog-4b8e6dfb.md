---
title: Claude Opus 4.8上线Vercel AI Gateway
title_original: Opus 4.8 on AI Gateway - Vercel
date: '2026-05-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/opus-4-8-on-ai-gateway
author: ''
summary: Claude Opus 4.8现已登陆Vercel AI Gateway，专为长周期Agent执行设计，能处理复杂多步编码任务如重构，减少人工修正需求。该模型在知识工作如文档起草、数据分析和演示制作中生成更清晰、更少含糊的文本。AI
  Gateway提供统一API调用、使用与成本追踪、重试与故障转移等功能，支持零数据保留和动态提供商排序，不加价且不收取推理平台费用。
categories:
- AI产品
tags:
- Claude Opus 4.8
- Vercel AI Gateway
- AI Agent
- 模型部署
- 开发者工具
draft: false
translated_at: '2026-05-29T06:13:16.384031'
---

Claude Opus 4.8 现已在 Vercel AI Gateway 上线。

Claude Opus 4.8 专为长周期 Agent（智能体）执行而构建，能够处理复杂的多步编码任务（如重构），这些任务此前需要在过程中进行人工修正。该模型在知识工作（如起草文档、分析数据和制作演示文稿）中也能生成更清晰、更少含糊的文本。

要使用 Opus 4.8，请在 AI SDK 中将模型设置为 `anthropic/claude-opus-4.8`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'anthropic/claude-opus-4.8',5  prompt: '查找并修复这些间歇性测试失败的根本原因。',6  providerOptions: {7    anthropic: {8      thinking: { type: 'adaptive' },9      effort: 'high',10    },11  },12});
```

AI Gateway 提供统一的 API 用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于提供商自身的正常运行时间。它包含内置的自定义报告、零数据保留支持、基于延迟和成本的动态提供商排序等功能。AI Gateway 反映提供商定价，不加价，并且不收取推理平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Opus 4.8 on AI Gateway - Vercel](https://vercel.com/changelog/opus-4-8-on-ai-gateway)
> 
> 翻译时间：2026-05-29 06:13
