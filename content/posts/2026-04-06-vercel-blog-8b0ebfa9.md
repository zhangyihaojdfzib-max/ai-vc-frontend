---
title: Vercel AI Gateway推出团队级零数据保留与提示训练控制
title_original: Team-wide Zero Data Retention and prompt training controls now on
  AI Gateway - Vercel – Vercel
date: '2026-04-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/zero-data-retention-no-prompt-training-on-ai-gateway
author: ''
summary: Vercel宣布其AI Gateway新增团队级别的零数据保留功能，用户无需再为每个AI提供商单独配置数据保留退出选项。该功能可自动将请求路由至已签订零数据保留协议的提供商，支持Anthropic、OpenAI、Google等主流模型。用户可在仪表板中为整个团队启用此策略，或在单个请求中通过参数配置零数据保留和禁止提示词训练。团队级功能按请求量收费，而请求级控制对所有用户免费开放，为AI应用的数据隐私管理提供了更便捷的解决方案。
categories:
- AI基础设施
tags:
- Vercel
- AI Gateway
- 数据隐私
- 零数据保留
- AI开发工具
draft: false
translated_at: '2026-04-22T05:05:22.393131'
---

AI Gateway 现支持团队级别的零数据保留（ZDR），无需再单独为每个提供商配置退出选项或达成协议。它会将请求仅路由至已签订 ZDR 协议的提供商，支持 Anthropic、OpenAI、Google 及众多其他模型。

### 团队级 ZDR

在 **AI Gateway 仪表板设置** 中启用团队级 ZDR，即可对团队发出的每个请求强制执行零数据保留，无需更改任何代码。

### 请求级 ZDR 与禁止提示词训练

您也可以在请求级别配置 ZDR 和/或禁止提示词训练，只需在每个请求中设置 `zeroDataRetention: true` 或 `disallowPromptTraining: true`。启用零数据保留会自动包含训练退出选项，因此无需单独配置两者。

```
1import type { GatewayProviderOptions } from '@ai-sdk/gateway';2import { streamText } from 'ai';3
4const result = streamText({5  model: 'anthropic/claude-sonnet-4.6',6  prompt: 'Summarize this internal document.',7  providerOptions: {8    gateway: {9      disallowPromptTraining: true,10      zeroDataRetention: true,11    } satisfies GatewayProviderOptions,12  },13});
```

**定价**

| 选项 | 可用性 |
| :--- | :--- |
| 团队级 ZDR | 每 1,000 次请求 0.10 美元 | Pro 和 Enterprise |
| 请求级 ZDR | 免费 | 所有用户 |
| 禁止提示词训练（请求级） | 免费 | 所有用户 |

每个响应都包含元数据，显示哪些提供商被考虑、哪些被过滤掉，为您提供策略执行的审计追踪。

这些控制功能适用于 AI SDK、Chat Completions API、Responses API、Anthropic Messages API 和 OpenResponses API。

阅读 **[零数据保留文档](https://example.com)** 和 **[禁止提示词训练文档](https://example.com)** 了解更多详情。

---

> 本文由AI自动翻译，原文链接：[Team-wide Zero Data Retention and prompt training controls now on AI Gateway - Vercel – Vercel](https://vercel.com/changelog/zero-data-retention-no-prompt-training-on-ai-gateway)
> 
> 翻译时间：2026-04-22 05:05
