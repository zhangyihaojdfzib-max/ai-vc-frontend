---
title: Vercel AI Gateway 推出追踪导出功能
title_original: Export AI Gateway traces with Vercel Drains - Vercel
date: '2026-08-05'
source: Vercel Blog
source_url: https://vercel.com/changelog/export-ai-gateway-traces-with-vercel-drains
author: ''
summary: Vercel 的 AI Gateway 现在为每个请求生成 OpenTelemetry 追踪，Pro 和 Enterprise 团队可通过 Vercel
  Drains 将追踪发送至兼容 OTLP/HTTP 的端点，如 Braintrust、Sentry 等。追踪包含模型路由、回退重试、Token 使用量、成本、延迟等关键信息，但不含提示词和补全内容。采样控制可调节导出流量，费用为每千条追踪
  $0.05 加数据传输费。该功能旨在提升 AI 应用的可观测性和调试效率。
categories:
- AI基础设施
tags:
- AI Gateway
- 可观测性
- OpenTelemetry
- Vercel
- 追踪
draft: false
translated_at: '2026-08-06T05:11:19.104533'
---

AI Gateway 现在会为每个请求生成一条 OpenTelemetry 追踪。Pro 和 Enterprise 团队可以通过 Vercel Drains 将这些追踪发送到任何兼容 OTLP/HTTP 的端点，包括 Braintrust、Dash0、Kubiks、Sentry 和 Statsig 的原生集成。

![配置 AI Gateway Trace Drain，选择项目并设置采样率。](/images/posts/227bde7af812.jpg)

![配置 AI Gateway Trace Drain，选择项目并设置采样率。](/images/posts/0e985d92955b.jpg)

每条追踪都展示了完整的请求生命周期，包括：

- 模型和提供商路由
- 回退和重试尝试
- Token 使用量和成本
- 首个 Token 时间、请求持续时间和响应状态
- 项目、部署、API 密钥、环境和自定义标签归属

模型和提供商路由

回退和重试尝试

Token 使用量和成本

首个 Token 时间、请求持续时间和响应状态

项目、部署、API 密钥、环境和自定义标签归属

Trace Drains 不包含提示词或补全内容。采样控制允许您选择导出到每个 drain 的流量大小。

AI Gateway 追踪的费用为每个 drain 每 1,000 条追踪 $0.05，另加标准 Drains 费率每 GB 数据传输 $0.50。每次成功投递到 drain 计为一次请求，即使 AI Gateway 进行了多次提供商尝试也是如此。失败的投递不产生追踪费用。

![按数量、项目、drain 或来源查看已投递的 AI Gateway 追踪事件。](/images/posts/517bcbe8d7e8.jpg)

![按数量、项目、drain 或来源查看已投递的 AI Gateway 追踪事件。](/images/posts/41dc3e83b3dc.jpg)

从您团队的 Drains 设置中设置 Trace Drain，或在 AI Gateway 文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Export AI Gateway traces with Vercel Drains - Vercel](https://vercel.com/changelog/export-ai-gateway-traces-with-vercel-drains)
> 
> 翻译时间：2026-08-06 05:11
