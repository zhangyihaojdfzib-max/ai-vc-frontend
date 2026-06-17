---
title: GLM 5.2登陆Vercel AI Gateway，支持百万Token上下文
title_original: GLM 5.2 now available on AI Gateway - Vercel
date: '2026-06-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/glm-5-2-now-available-on-ai-gateway
author: ''
summary: Vercel宣布GLM 5.2模型已在AI Gateway上线。该模型专为长周期任务设计，支持项目级工程上下文，上下文窗口从200K Token升级至1M
  Token，能更可靠地运行长时间任务并遵循工程标准。开发者可通过AI SDK设置模型ID为'zai/glm-5.2'直接调用。AI Gateway提供统一API、使用追踪、成本管理、重试与故障转移等功能，不额外收费，支持自带密钥。
categories:
- AI基础设施
tags:
- GLM 5.2
- Vercel
- AI Gateway
- 长上下文
- 模型部署
draft: false
translated_at: '2026-06-17T07:09:16.562496'
---

GLM 5.2 现已在 AI Gateway 上可用。

GLM 5.2 专为长周期任务而设计，可在单个任务中承载项目级工程上下文，更可靠地运行长时间任务，并更一致地遵循工程标准。

该模型的上下文窗口已从 GLM 5.1 的 200K Token 升级至 1M Token。

要使用 GLM 5.2，请在 AI SDK 中将模型设置为 `zai/glm-5.2`：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'zai/glm-5.2',5  prompt: '为数据摄入管道添加错误恢复功能。',6});
```

AI Gateway 提供统一的 API 用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于提供商自身的正常运行时间。它包含内置的自定义报告、零数据保留支持、API 密钥预算等功能。AI Gateway 反映提供商定价，不收取额外费用，且不对推理收取平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[GLM 5.2 now available on AI Gateway - Vercel](https://vercel.com/changelog/glm-5-2-now-available-on-ai-gateway)
> 
> 翻译时间：2026-06-17 07:09
