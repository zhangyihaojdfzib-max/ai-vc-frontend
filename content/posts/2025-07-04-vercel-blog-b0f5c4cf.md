---
title: Vercel 通过 OpenTelemetry 自动关联日志与追踪
title_original: Correlate logs and traces with OpenTelemetry in Vercel Log Drains
  - Vercel – Vercel
date: '2025-07-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/correlate-logs-and-traces-with-opentelemetry-in-vercel-log-drains
author: ''
summary: Vercel 宣布为使用 OpenTelemetry 进行应用插桩的客户，自动实现日志与分布式追踪的关联。该功能利用追踪和跨度标识符来丰富相关日志，使用户能够将特定日志精准关联到具体的请求追踪或操作跨度，从而更高效地定位性能问题和错误根源。目前，此功能已面向使用
  Datadog 和 Dash0 日志导出集成的客户自动生效，无需额外配置。这有助于开发者提升应用可观测性和故障排查效率。
categories:
- 技术趋势
tags:
- Vercel
- OpenTelemetry
- 可观测性
- 日志管理
- 分布式追踪
draft: false
translated_at: '2026-04-15T04:48:22.182849'
---

Vercel 现已为使用 OpenTelemetry 对应用程序进行插桩的客户，自动将日志与分布式追踪关联起来。

追踪是一种收集应用程序性能和行为数据的方式，有助于定位性能问题、错误及其他问题的根源。OpenTelemetry（OTel）是一个开源项目，可让您对应用程序进行插桩以收集追踪数据。

当使用 OTel 追踪请求时，Vercel 将使用追踪标识符和跨度标识符来丰富相关日志。这使您能够将单个日志关联到具体的追踪或跨度。

此功能适用于通过我们与 Datadog 和 Dash0 的集成使用日志导出的客户。无需任何操作，对于使用 OTel 并启用这些集成的客户，日志与追踪的关联将自动生效。

详细了解如何通过日志导出将日志与追踪关联。

---

> 本文由AI自动翻译，原文链接：[Correlate logs and traces with OpenTelemetry in Vercel Log Drains - Vercel – Vercel](https://vercel.com/changelog/correlate-logs-and-traces-with-opentelemetry-in-vercel-log-drains)
> 
> 翻译时间：2026-04-15 04:48
