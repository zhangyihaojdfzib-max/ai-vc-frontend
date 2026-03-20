---
title: Vercel Drains发布：统一导出全栈可观测性数据
title_original: 'Introducing Vercel Drains: Complete observability data, anywhere
  - Vercel'
date: '2025-09-15'
source: Vercel Blog
source_url: https://vercel.com/blog/introducing-vercel-drains
author: ''
summary: Vercel宣布将原有的Log Drains升级为Vercel Drains，功能从单一的日志导出扩展为统一的数据管道，支持导出OpenTelemetry追踪数据、Web
  Analytics事件和Speed Insights性能指标。该服务允许用户将完整的可观测性数据流式传输到Datadog、Honeycomb等现有工具或自定义HTTP端点，实现了日志、追踪、分析与指标的自动关联，为现代应用性能提供端到端的洞察。Drains现已面向Pro和企业用户开放，按量计费。
categories:
- AI基础设施
tags:
- 可观测性
- Vercel
- OpenTelemetry
- 无服务器
- DevOps
draft: false
translated_at: '2026-03-20T04:51:15.450799'
---

Vercel Log Drains 现已更名为 Vercel Drains。

为什么？因为它们不再仅用于日志，您现在还可以导出 OpenTelemetry 追踪数据、Web Analytics 事件以及 Speed Insights 指标。

Drains 为您提供了一种统一的方式，将可观测性数据从 Vercel 流式传输到您的团队已经依赖的系统中。

### 为什么 Drains 很重要

大多数团队已经拥有他们信赖的可观测性技术栈，例如 Datadog、Honeycomb、Grafana、Elastic 或他们自己的数据仓库。但这些系统的价值取决于它们接收到的数据。仅凭日志无法解释现代应用程序的行为。

要全面了解性能，您需要的不仅仅是日志行。追踪数据展示请求如何在无服务器函数中流转。分析数据捕获用户交互。真实用户指标揭示浏览器中发生的情况。

Vercel Drains 将这些信号统一到一个管道中，将完整的数据流式传输到您已使用的工具，包括：

- 日志：运行时、构建、静态资源、防火墙和函数日志。
- 追踪：Trace Drains 转发来自您部署的分布式追踪数据。
- Web Analytics：轻量级页面浏览和自定义事件数据。
- Speed Insights：真实用户性能指标和 Web Vitals。

由于 Vercel 运行整个请求路径，从浏览器到动态函数执行，这些信号是连贯且相互关联的。来自被追踪请求的日志会自动丰富 `traceId` 和 `spanId`，因此您可以从一条日志行直接跳转到其所属的分布式追踪。

![](/images/posts/7b92a4eb5053.jpg)

![](/images/posts/7e7956e1d5ee.jpg)

## 两种数据导出方式

Drains 可以以两种形式创建，具体取决于您希望如何连接：

1.  **自定义导出**：将数据导出到您控制的任何 HTTP 端点。您可以：
    - 选择数据类型（日志、追踪、分析或性能指标）
    - 配置采样率以管理流量
    - 选择 JSON、NDJSON 或 Protobuf 格式
    - 添加请求头或签名验证以增强安全性

    例如，您可以将追踪数据流式传输到 OTLP 收集器，将日志发送到自托管的 Elastic 集群，并将分析事件导入 Snowflake。

2.  **集成导出**：Vercel 与 Dash0、Statsig、Datadog、Logflare 等供应商提供开箱即用的集成。这些直接集成有助于自动处理配置，并开始将日志流式传输到您的账户。

## 端到端可观测性

Vercel Drains 的优势在于上下文关联。LCP 的激增可以追溯到某个缓慢 API 调用的追踪数据。一个 500 错误日志可以关联到触发它的特定请求。通过将日志、追踪、分析和性能指标一起导出，您可以获得应用程序在生产环境中行为的连续视图，并将其导入您已使用的任何工具。

由于追踪遵循 OpenTelemetry 协议，它们可以直接接入 Datadog APM、Honeycomb、Grafana Tempo、New Relic 或任何支持 OTel 的供应商，无需自定义插桩。日志和追踪会自动关联，分析数据可以流式传输到您用于业务报告的同一数据仓库。

Drains 现已适用于 Pro 和企业版计划。通过 Drains 导出的数据按每 GB 0.50 美元计费，与现有 Log Drains 费率相同。您可以为每个团队配置多个 Drains，覆盖任意数量的项目。

## 开始使用

您今天就可以从 Vercel 仪表板 → 团队设置 → Drains 来设置 Drains。选择一个自定义 HTTP 端点来流式传输任何数据类型，或者从市场安装一个集成以获得托管式设置。

阅读完整文档以获取配置详情、支持的格式和模式参考。

---

> 本文由AI自动翻译，原文链接：[Introducing Vercel Drains: Complete observability data, anywhere - Vercel](https://vercel.com/blog/introducing-vercel-drains)
> 
> 翻译时间：2026-03-20 04:51
