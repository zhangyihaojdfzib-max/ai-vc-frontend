---
title: Vercel AI Gateway现已支持月之暗面Kimi K2 0905模型
title_original: Moonshot AI's Kimi K2 0905 model is now supported in Vercel AI Gateway
  - Vercel
date: '2025-09-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/moonshot-ais-kimi-k2-0905-model-is-now-supported-in-vercel-ai-gateway
author: ''
summary: Vercel AI Gateway正式集成月之暗面（Moonshot AI）最新推出的Kimi K2 0905模型。该模型专注于智能体编码，拥有256K上下文窗口，开发者无需单独供应商账户即可通过统一的API直接调用。AI
  Gateway提供使用追踪、成本管理、性能优化及故障转移等功能，并利用多个底层供应商（包括Moonshot AI、Groq和Fireworks AI）确保高性能服务。通过AI
  SDK v5，开发者仅需更新模型标识字符串即可快速接入，同时享受内置可观测性、自带密钥支持和智能路由等特性。
categories:
- AI基础设施
tags:
- Vercel
- Moonshot AI
- AI Gateway
- 大模型
- 开发者工具
draft: false
translated_at: '2026-03-29T05:03:14.689700'
---

您现在可以通过Vercel AI Gateway直接访问月之暗面（Moonshot AI）推出的新模型**Kimi K2 0905**，该模型专注于智能体编码，并拥有256K的上下文窗口，无需其他供应商账户即可使用。

AI Gateway允许您通过统一且一致的API调用模型，只需更新一个字符串即可。您可以跟踪使用情况和成本，并配置性能优化、重试和故障转移策略，以实现高于供应商平均水平的运行时间。

要在**AI SDK v5**中使用它，请先安装软件包：

然后，将模型设置为 `moonshotai/kimi-k2-0905`：

```
1import { streamText } from 'ai'2
3const result = streamText({4  model: 'moonshotai/kimi-k2-0905',5  prompt: 'How is a trillion parameter oss model possible?'6})
```

该服务包含内置的**可观测性**、**自带密钥（BYOK）支持**以及具备自动重试功能的智能**供应商路由**。

为了向Kimi K2提供高性能服务，AI Gateway在底层利用了多个模型供应商，包括直接连接月之暗面（Moonshot AI）、Groq和Fireworks AI。

了解更多关于**AI Gateway**的信息。

---

> 本文由AI自动翻译，原文链接：[Moonshot AI's Kimi K2 0905 model is now supported in Vercel AI Gateway - Vercel](https://vercel.com/changelog/moonshot-ais-kimi-k2-0905-model-is-now-supported-in-vercel-ai-gateway)
> 
> 翻译时间：2026-03-29 05:03
