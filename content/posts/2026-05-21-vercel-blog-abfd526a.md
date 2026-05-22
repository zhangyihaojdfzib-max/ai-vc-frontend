---
title: 通义千问3.7 Max上线Vercel AI Gateway
title_original: Qwen 3.7 Max now available on Vercel AI Gateway - Vercel
date: '2026-05-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/qwen-3-7-max-now-available-on-vercel-ai-gateway
author: ''
summary: 阿里通义千问3.7 Max模型现已在Vercel AI Gateway上线，该模型定位为Agent基础模型，具备编程、办公自动化及长期自主执行能力。在前端原型设计和复杂多文件工程方面表现提升，支持多Agent编排的办公与生产力任务，并在长期工具调用中保持连贯推理。用户可通过AI
  SDK设置模型标识符进行调用。AI Gateway提供统一API、使用追踪、成本管理、重试与故障转移等功能，并支持自定义报告与可观测性。
categories:
- AI产品
tags:
- 通义千问
- Vercel
- AI Gateway
- Agent
- 模型部署
draft: false
translated_at: '2026-05-22T06:06:15.701625'
---

阿里通义千问3.7 Max现已在Vercel AI Gateway上线。该模型被设计为Agent（智能体）基础模型，具备涵盖编程、办公流程自动化和长期自主执行的能力。

通义千问3.7 Max在前端原型设计和复杂多文件工程方面表现出改进。该模型通过多Agent（智能体）编排支持办公和生产力任务，并在长期工具调用会话中维持连贯推理。

要使用通义千问3.7 Max，请在AI SDK中将模型设置为`alibaba/qwen-3.7-max`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'alibaba/qwen3.7-max',5  prompt: `将此服务重构为更小的模块，并更新整个仓库中的调用方。`,6});
```

AI Gateway提供统一的API用于调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商正常运行时间的可用性。它包含内置的自定义报告、可观测性、自带密钥支持，以及具有自动重试功能的智能提供商路由。

了解更多关于AI Gateway的信息，查看AI Gateway模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Qwen 3.7 Max now available on Vercel AI Gateway - Vercel](https://vercel.com/changelog/qwen-3-7-max-now-available-on-vercel-ai-gateway)
> 
> 翻译时间：2026-05-22 06:06
