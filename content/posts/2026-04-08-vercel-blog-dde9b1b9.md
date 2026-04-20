---
title: Vercel AI Gateway推出团队级零数据保留功能，简化AI合规管理
title_original: Zero Data Retention on AI Gateway - Vercel – Vercel
date: '2026-04-08'
source: Vercel Blog
source_url: https://vercel.com/blog/zdr-on-ai-gateway
author: ''
summary: 本文介绍了Vercel AI Gateway新推出的团队级零数据保留功能，旨在解决开发者使用多个AI模型时面临的数据政策碎片化问题。该功能允许团队在仪表盘中一键启用，确保所有请求自动路由至已签订零数据保留协议的提供商，无需修改代码。文章还详细说明了请求级ZDR控制、禁止提示词训练等配套功能，以及它们如何协同工作，为处理敏感数据的工作流提供灵活且严格的合规保障，帮助开发者从繁琐的政策管理中解放出来，专注于应用开发。
categories:
- AI基础设施
tags:
- Vercel
- AI Gateway
- 数据合规
- 零数据保留
- AI开发工具
draft: false
translated_at: '2026-04-20T05:00:07.400709'
---

使用多个AI模型进行构建，意味着需要应对碎片化的数据政策。面对众多不同的模型提供商，这不仅仅是碎片化的问题，更是将大量时间耗费在了错误的事情上。

你必须通读不同的服务条款，追踪哪些提供商符合你的安全要求，并希望开发人员记得在每个请求上都正确配置退出选项。本该是清晰直接的政策，却因为许多提供商默认不提供零数据保留（ZDR）功能，而变成了一个手动、易出错的过程。

AI Gateway通过为你处理协商和执行，改变了这一现状。你无需再逐个提供商地管理政策，而是可以自由地专注于构建。AI Gateway通过仅将请求路由至我们已协商好零数据保留协议的提供商，自动确保你的数据要求得到满足。来自OpenAI、Anthropic、Google等公司的模型都有支持ZDR的提供商可选。

今天，我们正在扩展AI Gateway的合规能力，推出团队级的零数据保留（ZDR）功能，让你无需触碰任何代码，就能在整个团队范围内执行严格的数据政策。Gateway的合规功能现在包括：仪表盘中的团队级ZDR、针对特定敏感工作流的请求级ZDR，以及禁止提示词训练的明确控制。

在AI Gateway仪表盘设置中开启此功能，随后所有通过AI Gateway的请求将仅通过符合ZDR要求的提供商进行路由。

![](/images/posts/859ac839d603.jpg)

![](/images/posts/ddcb765a07a2.jpg)

### 团队级零数据保留

团队级ZDR适用于专业版和企业版团队。它适用于你团队发出的每一个请求，无需更改代码。这对于希望获得完全控制、确保无人能修改或误用限制的团队来说是理想选择。

### 请求级控制

请求级ZDR让你可以在特定请求上强制执行数据删除，特别是当只有某些工作流处理敏感数据时。这在你的应用程序中某些查询包含专有信息而其他请求无需同等保护时非常有用。你可以在AI Gateway支持的所有API格式中，通过`provider options`启用请求级ZDR。

```
1import type { GatewayProviderOptions } from '@ai-sdk/gateway';2import { streamText } from 'ai';3
4const result = streamText({5  model: 'anthropic/claude-sonnet-4.6',6  prompt: 'Analyze this sensitive business data and provide insights.',7  providerOptions: {8    gateway: {9      zeroDataRetention: true,10    } satisfies GatewayProviderOptions,11  },12});
```

团队级和请求级设置协同工作。只要其中任一设置被启用，ZDR就会被强制执行。

### 禁止提示词训练

禁止提示词训练可防止提供商使用你的提示词数据来训练他们的模型。对于任何通过LLM发送专有代码、内部文档或商业策略的团队来说，这都是一个很好的默认设置。此过滤器可在请求级别使用。

ZDR是此控制的超集。如果你启用了ZDR，则已包含退出训练的控制。

```
1import type { GatewayProviderOptions } from '@ai-sdk/gateway';2import { streamText } from 'ai';3
4const result = streamText({5  model: 'anthropic/claude-sonnet-4.6',6  prompt: 'Analyze this proprietary business strategy.',7  providerOptions: {8    gateway: {9      disallowPromptTraining: true,10    } satisfies GatewayProviderOptions,11  },12});
```

每个响应都包含元数据，显示考虑了哪些提供商以及过滤掉了哪些提供商。这为你提供了数据政策如何执行的审计追踪记录。

```
1{2  "gateway": {3    "routing": {4      "planningReasoning": "ZDR requested: 5 attempts → 2 ZDR attempts. ZDR execution order: anthropic(system) → bedrock(system)"5    }6  }7}
```

所有这些过滤器都与AI SDK、Chat Completions API、Responses API、Anthropic Messages API以及OpenResponses API兼容。

保护数据不再需要在每个路由中编写自定义逻辑。通过将这些规则移至网关，合规性变成了基础设施的一部分，而非应用程序的繁琐工作。你重新获得了控制权，而你的团队则可以继续交付成果。

有关定价详情，请参阅零数据保留定价。在模型子页面上查看支持零数据保留和禁止提示词训练的模型和提供商。立即在你的仪表盘设置中启用零数据保留，或阅读文档以获取完整的设置详情。

---

> 本文由AI自动翻译，原文链接：[Zero Data Retention on AI Gateway - Vercel – Vercel](https://vercel.com/blog/zdr-on-ai-gateway)
> 
> 翻译时间：2026-04-20 05:00
