---
title: Vercel AI Gateway上线GPT 5.6三款模型
title_original: GPT 5.6 Sol, Luna, and Terra now available on AI Gateway - Vercel
date: '2026-07-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/gpt-5-6-now-available-on-ai-gateway
author: ''
summary: Vercel宣布OpenAI的GPT 5.6现已在AI Gateway上以有限预览形式提供，包含Sol、Terra和Luna三种模型。Sol为旗舰模型，能力最强；Terra适合日常工作，性能与上一代相当但成本减半；Luna快速且经济实惠。这些模型在编程、生物学和网络安全领域的Agent工作中表现更强，且更具Token效率。AI
  Gateway提供统一API、使用跟踪、成本管理、重试与故障转移等功能，无加价，支持自带密钥。
categories:
- AI基础设施
tags:
- GPT 5.6
- AI Gateway
- Vercel
- 模型部署
- AI基础设施
draft: false
translated_at: '2026-07-12T05:27:27.876823'
---

GPT 5.6 现已在 AI Gateway 上以三种模型提供：Sol、Terra 和 Luna。

OpenAI 的 GPT 5.6 现已在 AI Gateway 上以有限预览形式提供，包含三种模型：Sol、Terra 和 Luna。这三款模型在编程、生物学和网络安全领域的 Agent（智能体）工作中表现更强，且相比上一代更具 Token 效率。

- Sol（openai/gpt-5.6-sol）：旗舰模型，是三款中能力最强的。
- Terra（openai/gpt-5.6-terra）：适合日常工作的均衡模型，性能与上一代相当，成本减半。
- Luna（openai/gpt-5.6-luna）：快速且经济实惠的模型，以系列中最低成本提供强大能力。

Sol（openai/gpt-5.6-sol）：旗舰模型，是三款中能力最强的。

Terra（openai/gpt-5.6-terra）：适合日常工作的均衡模型，性能与上一代相当，成本减半。

Luna（openai/gpt-5.6-luna）：快速且经济实惠的模型，以系列中最低成本提供强大能力。

要使用 GPT 5.6，请在 AI SDK 中将 `model` 设置为上述 slug 之一：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'openai/gpt-5.6-sol',5  prompt: 'Investigate the failing tests and open a PR with a fix.',6});
```

您还可以设置路由规则，在不修改代码的情况下从其他网关模型切换到 GPT 5.6。

```
vercel ai-gateway rules add \  --type rewrite \  --source openai/gpt-5.5 \  --destination openai/gpt-5.6-sol
```

AI Gateway 提供统一的 API 用于调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商级别的正常运行时间。它包含内置的自定义报告、零数据保留支持、API 密钥预算、路由规则等功能。

AI Gateway 反映提供商定价，无加价，且不对推理收取平台费用，包括自带密钥（BYOK）请求。

在模型游乐场中试用 GPT 5.6。

AI Gateway：按使用量跟踪顶级 AI 模型

AI Gateway 模型排行榜会随时间跟踪最受欢迎的模型，根据所有网关流量中处理的 Token 总量进行排名。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[GPT 5.6 Sol, Luna, and Terra now available on AI Gateway - Vercel](https://vercel.com/changelog/gpt-5-6-now-available-on-ai-gateway)
> 
> 翻译时间：2026-07-12 05:27
