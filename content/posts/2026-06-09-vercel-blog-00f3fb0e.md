---
title: Claude Fable 5上线Vercel AI Gateway
title_original: Claude Fable 5 now available on AI Gateway - Vercel
date: '2026-06-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/claude-fable-5-now-available-on-ai-gateway
author: ''
summary: Anthropic的Claude Fable 5模型现已在Vercel AI Gateway上线。作为Mythos级模型，Fable 5在长期运行、多步骤任务上显著提升，能端到端执行此前需人工介入的工作，并支持并行子智能体调度。模型内置阻断分类器以防范滥用风险，提示词保留30天但不用于训练。AI
  Gateway提供统一API、使用量跟踪、成本优化等功能，且不加价收费。
categories:
- AI产品
tags:
- Claude Fable 5
- AI Gateway
- Vercel
- Anthropic
- 模型部署
draft: false
translated_at: '2026-06-10T06:26:48.592901'
---

Anthropic 的 Claude Fable 5 现已在 AI Gateway 上线。作为 Mythos 级模型，Fable 5 在长期运行、模糊不清、多步骤任务上相比之前的 Claude 模型有显著提升，能够端到端执行此前需要频繁人工介入的工作。

该模型在持续数天的运行中保持高效输出，并能可靠地调度并行子 Agent（智能体），且较低努力设置下的表现往往能匹敌之前 Claude 模型在最高努力设置下的产出。代码审查、漏洞发现和代码库调研能力更强，复杂问题的首次正确率也明显提高。

Fable 5 内置了阻断分类器，可拒绝攻击性网络安全、生物学及思维链摘要提取等请求，因为该模型在这些领域的能力带来了实际滥用风险。Anthropic 也不支持零数据保留，因为某些滥用模式只有在累积请求中才会显现。提示词和补全内容将保留 30 天，且不会用于训练 Claude。

要使用 Fable 5，请在 AI SDK 中将模型设置为 `anthropic/claude-fable-5`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'anthropic/claude-fable-5',5  prompt: '调查 p99 延迟为何退化并提出修复方案。',6  providerOptions: {7    anthropic: {8      thinking: { type: 'adaptive' },9      effort: 'high',10    },11  },12});
```

AI Gateway 提供统一 API 用于调用模型、跟踪使用量和成本，并配置重试、故障转移和性能优化，以实现高于提供商自身的正常运行时间。它包含内置的自定义报告、零数据保留支持、按延迟和成本动态排序提供商等功能。AI Gateway 反映提供商定价，不收取加价，也不对推理收取平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Claude Fable 5 now available on AI Gateway - Vercel](https://vercel.com/changelog/claude-fable-5-now-available-on-ai-gateway)
> 
> 翻译时间：2026-06-10 06:26
