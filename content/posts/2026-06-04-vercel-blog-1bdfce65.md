---
title: Vercel AI Gateway上线英伟达Nemotron 3 Ultra模型
title_original: Nemotron 3 Ultra now available on AI Gateway - Vercel
date: '2026-06-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/nemotron-3-ultra-now-available-on-ai-gateway
author: ''
summary: Vercel AI Gateway正式上线Nvidia的Nemotron 3 Ultra开源混合专家推理模型。该模型专为长时间运行的Agent工作流设计，拥有100万Token上下文窗口，支持规划、工具使用、子Agent委派和错误恢复等功能。其吞吐量达每秒350
  Token，在Agent任务上成本可降低30%。用户可通过AI SDK直接调用，AI Gateway还提供统一API、使用追踪、成本管理及性能优化等能力，且不加价、不收取平台推理费用。
categories:
- AI产品
tags:
- Nemotron 3 Ultra
- Vercel AI Gateway
- 开源模型
- Agent工作流
- Nvidia
draft: false
translated_at: '2026-06-05T06:22:29.547957'
---

Nvidia 的 Nemotron 3 Ultra 现已在 Vercel AI Gateway 上线。

Nemotron 3 Ultra 是一款开源的混合专家推理模型，专为编排长时间运行的 Agent（智能体）工作流而构建，拥有 100 万 Token 的上下文窗口。该模型针对多轮 Agent（智能体）工作流：规划、工具使用、子 Agent（智能体）委派和错误恢复。吞吐量可达每秒 350 Token，在 Agent（智能体）任务上成本降低高达 30%。

要使用 Nemotron 3 Ultra，请在 AI SDK 中将模型设置为 `nvidia/nemotron-3-ultra-550b-a55b`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'nvidia/nemotron-3-ultra-550b-a55b',5  prompt: '规划并执行一项多步骤研究任务，然后综合生成一份报告。',6});
```

AI Gateway 提供统一的 API 来调用模型、跟踪使用情况和成本，并配置重试、故障转移和性能优化，以实现高于提供商的服务可用性。它包含内置的自定义报告、零数据保留支持、按延迟和成本动态排序提供商等功能。AI Gateway 反映提供商定价，无加价，并且不对推理收取平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Nemotron 3 Ultra now available on AI Gateway - Vercel](https://vercel.com/changelog/nemotron-3-ultra-now-available-on-ai-gateway)
> 
> 翻译时间：2026-06-05 06:22
