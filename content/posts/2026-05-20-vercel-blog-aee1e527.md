---
title: Grok Build 0.1 登陆 Vercel AI Gateway
title_original: Grok Build 0.1 now available on Vercel AI Gateway - Vercel
date: '2026-05-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/grok-build-0-1-now-available-on-vercel-ai-gateway
author: ''
summary: Vercel 宣布 Grok Build 0.1 模型现已在 AI Gateway 上可用。该模型是专为智能体编码训练的测试版编码模型，目前处于早期访问阶段，并为
  Grok Build CLI 应用提供支持。用户可通过 AI SDK 将模型设置为 `xai/grok-build-0.1` 来使用。AI Gateway 提供统一
  API 用于调用模型、跟踪使用情况和成本，并支持重试、故障转移和性能优化，确保高于提供商正常运行时间的可用性。
categories:
- AI基础设施
tags:
- Grok Build
- Vercel
- AI Gateway
- 编码模型
- AI基础设施
draft: false
translated_at: '2026-05-21T06:22:52.471007'
---

Grok Build 0.1 现已在 Vercel AI Gateway 上可用。

这是一个为智能体编码训练的测试版编码模型，目前处于早期访问阶段，并为 Grok Build CLI 应用提供支持。推理努力不可配置，且没有非推理模式。

要使用 Grok Build 0.1，请在 AI SDK 中将模型设置为 `xai/grok-build-0.1`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'xai/grok-build-0.1',5  prompt: '重构此模块以使用 async/await 并添加测试。',6});
```

AI Gateway 提供统一的 API 用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于提供商正常运行时间的可用性。它包含内置的自定义报告、可观测性、自带密钥支持，以及带有自动重试的智能提供商路由。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中尝试。

---

> 本文由AI自动翻译，原文链接：[Grok Build 0.1 now available on Vercel AI Gateway - Vercel](https://vercel.com/changelog/grok-build-0-1-now-available-on-vercel-ai-gateway)
> 
> 翻译时间：2026-05-21 06:22
