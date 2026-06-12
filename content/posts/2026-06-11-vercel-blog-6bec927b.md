---
title: DeepSeek模型现可通过Azure在Vercel AI Gateway使用
title_original: DeepSeek models now available via Azure on AI Gateway - Vercel
date: '2026-06-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/deepseek-models-now-available-via-azure-on-ai-gateway
author: ''
summary: Vercel宣布其AI Gateway新增Azure作为DeepSeek V4 Pro和V4 Flash模型的提供商，用户无需修改代码即可实现自动故障转移和路由优化。通过设置order参数可优先使用Azure，并支持自带密钥（BYOK）以利用现有凭证。AI
  Gateway提供统一API、使用量追踪、成本监控、重试与性能优化等功能，且无平台加价。此举进一步扩展了DeepSeek模型的部署选项，提升了可用性和灵活性。
categories:
- AI基础设施
tags:
- DeepSeek
- Azure
- AI Gateway
- Vercel
- 模型部署
draft: false
translated_at: '2026-06-12T06:36:55.331886'
---

Azure 现已成为 AI Gateway 上 DeepSeek V4 Pro 和 V4 Flash 的提供商。

对任一模型的请求均可通过 Azure 路由，与现有提供商共同构成另一条故障转移路径。无需修改代码：默认路由会自动考虑 Azure，若某个提供商发生故障，网关将回退至剩余列表中的其他提供商。

若希望请求优先尝试 Azure，可在 AI SDK 中为 `deepseek/deepseek-v4-pro` 或 `deepseek/deepseek-v4-flash` 的网关提供商选项使用 `order` 参数，将 Azure 设为优先，同时保留其他提供商作为回退：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'deepseek/deepseek-v4-pro',5  prompt: 'Refactor this function to use async/await.',6  providerOptions: {7    gateway: {8      order: ['azure'],9    },10  },11});
```

若您已有 Azure 凭证，可自带密钥，AI Gateway 将使用该密钥处理路由至 Azure 的请求。详见 API 密钥认证与 BYOK 设置。

AI Gateway 提供统一 API 用于调用模型、跟踪使用量与成本，并配置重试、故障转移及性能优化，以实现高于单一提供商的正常运行时间。它内置自定义报告、零数据留存支持、API 密钥预算等功能。AI Gateway 反映提供商定价，无加价，且不对推理收取平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[DeepSeek models now available via Azure on AI Gateway - Vercel](https://vercel.com/changelog/deepseek-models-now-available-via-azure-on-ai-gateway)
> 
> 翻译时间：2026-06-12 06:36
