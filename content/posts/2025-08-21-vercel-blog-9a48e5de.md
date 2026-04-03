---
title: Vercel AI Gateway全面开放：统一API访问数百AI模型，零加价透明定价
title_original: AI Gateway is now generally available - Vercel
date: '2025-08-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/ai-gateway-is-now-generally-available
author: ''
summary: Vercel宣布AI Gateway现已全面开放，该服务提供了一个统一的API接口，允许开发者访问数百个AI模型。其核心优势包括：透明的定价策略（对Token不加价，支持自带密钥）、低于20毫秒的低延迟路由、自动故障转移以提高可用性、高频次限制以及详细的成本与使用情况分析。用户可通过AI
  SDK或OpenAI兼容端点轻松集成，仅需切换模型字符串即可开始使用。该服务旨在简化AI模型调用，提升开发效率与系统可靠性。
categories:
- AI基础设施
tags:
- Vercel
- AI Gateway
- API网关
- AI模型部署
- 开发者工具
draft: false
translated_at: '2026-04-03T05:03:55.713559'
---

![](/images/posts/c985887c0f5c.jpg)

![](/images/posts/63910bfa7243.jpg)

AI Gateway现已全面开放，它提供了一个统一的API，用于访问数百个AI模型，并具备透明的定价和内置的可观测性。

凭借跨多个推理提供商低于20毫秒的延迟路由，AI Gateway提供：

-   透明的定价，Token无加价（包括自带密钥）
-   自动故障转移以实现更高的可用性
-   高频率限制
-   详细的成本和使用情况分析

透明的定价，Token无加价（包括自带密钥）

自动故障转移以实现更高的可用性

高频率限制

详细的成本和使用情况分析

您可以通过AI SDK或通过OpenAI兼容的端点使用AI Gateway。使用AI SDK时，只需简单地切换模型字符串即可。

通过一次API调用即可开始使用：

```
1import { streamText } from 'ai'2
3const result = streamText({4  model: 'openai/gpt-5',5  prompt: 'How can AI Gateway not have a markup on tokens?'6})
```

阅读更多关于此[公告](https://example.com/announcement)的信息，了解更多关于[AI Gateway](https://example.com/ai-gateway)的详情，或[立即开始使用](https://example.com/get-started)。

---

> 本文由AI自动翻译，原文链接：[AI Gateway is now generally available - Vercel](https://vercel.com/changelog/ai-gateway-is-now-generally-available)
> 
> 翻译时间：2026-04-03 05:03
