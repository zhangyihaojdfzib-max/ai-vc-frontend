---
title: Laguna S 2.1登陆Vercel AI Gateway
title_original: Laguna S 2.1 is now available on AI Gateway - Vercel
date: '2026-07-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/laguna-s-2-1-is-now-available-on-ai-gateway
author: ''
summary: Poolside的Laguna S 2.1模型现已通过Vercel AI Gateway提供，包含免费版（256K上下文）和付费版（1M上下文）。该开放权重混合专家模型专注于智能体编程与长时间运行任务，如代码编写、调试、测试、MLOps及AI研究。在思考模式下，其在Terminal-Bench
  2.1、SWE-bench Multilingual和SWE-Bench Pro上分别达到70.2%、78.5%和59.4%的得分。AI Gateway提供统一API、使用量追踪、成本控制及高可用性，且不收取加价费用。
categories:
- AI基础设施
tags:
- Laguna S 2.1
- AI Gateway
- Vercel
- 混合专家模型
- 智能体编程
draft: false
translated_at: '2026-07-27T05:49:00.721073'
---

来自Poolside的Laguna S 2.1现已登陆AI Gateway。该模型提供两个版本：

- 免费版（256K上下文窗口）：poolside/laguna-s-2.1-free
- 付费版（1M上下文窗口）：poolside/laguna-s-2.1

免费版（256K上下文窗口）：poolside/laguna-s-2.1-free

付费版（1M上下文窗口）：poolside/laguna-s-2.1

Laguna S 2.1是一个开放权重的混合专家模型，支持高达1M Token的上下文窗口，并可在思考模式与非思考模式下运行。

该模型专注于Agent（智能体）编程和长时间运行任务，包括编写和调试代码、运行测试、构建基于浏览器的工具、处理MLOps流水线以及AI研究。在思考模式下，Laguna S 2.1在Terminal-Bench 2.1上达到70.2%，在SWE-bench Multilingual上达到78.5%，在SWE-Bench Pro上达到59.4%。

要使用Laguna S 2.1，请在AI SDK中将model设置为poolside/laguna-s-2.1-free或poolside/laguna-s-2.1：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'poolside/laguna-s-2.1',5  prompt: '修复支付套件中的不稳定测试。',6});
```

AI Gateway提供统一的API来调用模型、跟踪使用量和成本，并配置重试、故障转移和性能优化，以实现高于提供商正常运行时间的可用性。它包含内置的自定义报告、零数据保留支持、API密钥预算、路由规则等功能。

AI Gateway反映提供商的定价，不收取任何加价费用，也不对推理收取平台费，包括自带密钥（BYOK）请求。

在模型游乐场中试用Laguna S 2.1。

AI Gateway：按使用量追踪顶级AI模型

AI Gateway模型排行榜会持续追踪最受欢迎的模型，根据所有网关流量中处理的Token总量进行排名。

查看排行榜

---

> 本文由AI自动翻译，原文链接：[Laguna S 2.1 is now available on AI Gateway - Vercel](https://vercel.com/changelog/laguna-s-2-1-is-now-available-on-ai-gateway)
> 
> 翻译时间：2026-07-27 05:49
