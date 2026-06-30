---
title: Vercel CLI 新增 Speed Insights 查询功能
title_original: Query Speed Insights from the Vercel CLI - Vercel
date: '2026-06-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/query-speed-insights-from-the-vercel-cli
author: ''
summary: Vercel 在其 CLI 中新增了 `vercel metrics` 命令，允许开发者直接查询基于真实用户流量的核心 Web 指标（LCP、INP、CLS）及其他性能数据（FCP、TTFB）。该功能支持按页面、地区、设备等维度筛选数据，并可结合编码
  Agent 自动回答性能回退、地域感知速度等复杂问题，极大提升了性能监控与调试的效率。
categories:
- 技术趋势
tags:
- Vercel
- Speed Insights
- CLI
- Web性能
- 核心Web指标
draft: false
translated_at: '2026-06-30T06:15:04.819699'
---

您现在可以直接通过 Vercel CLI 查询 Speed Insights 数据点。

使用 `vercel metrics` 命令，您可以基于真实用户流量的客户端测量数据，提取核心 Web 指标（LCP、INP、CLS）以及其他页面性能指标（FCP、TTFB）。

![](/images/posts/86fc2b0da4e8.jpg)

![](/images/posts/21ba9436e9c4.jpg)

通过为编码 Agent（智能体）提供 CLI 访问权限，Agent（智能体）可以回答诸如以下问题：

- 自上周以来，哪些页面的 INP 出现了回退？
- 我的首页在亚洲地区的感知速度如何？
- 比较仪表盘页面在移动端和桌面端的 CLS。

自上周以来，哪些页面的 INP 出现了回退？

我的首页在亚洲地区的感知速度如何？

比较仪表盘页面在移动端和桌面端的 CLS。

有关如何使用 CLI 命令的更多详细信息，以及支持的指标、维度、筛选条件和查询选项的完整列表，请查阅文档。

---

> 本文由AI自动翻译，原文链接：[Query Speed Insights from the Vercel CLI - Vercel](https://vercel.com/changelog/query-speed-insights-from-the-vercel-cli)
> 
> 翻译时间：2026-06-30 06:15
