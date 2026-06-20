---
title: Vercel监控新增Edge Function三大指标
title_original: Edge Function metrics now available in Monitoring - Vercel
date: '2025-01-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/edge-function-metrics-now-available-in-monitoring
author: ''
summary: Vercel的监控功能为Edge Functions新增三个关键指标：调用次数、执行单元（以50ms为增量衡量CPU时间）以及快速源站传输速率（入站和出站）。这些指标适用于Observability
  Plus和Monitoring客户，旨在提供Edge Functions活动与性能的全面视图。注意，Edge Functions已弃用，新项目应使用Node.js运行时的Vercel
  Functions和Fluid compute。
categories:
- 技术趋势
tags:
- Vercel
- Edge Functions
- 监控指标
- 性能分析
- 云基础设施
draft: false
translated_at: '2026-06-20T06:20:47.404511'
---

![](/images/posts/8e40cf072f13.jpg)

![](/images/posts/5689b799a1ab.jpg)

注意：此更新日志条目为历史记录。Edge Functions 已弃用，不适用于新项目。请使用带有 Node.js 运行时的 Vercel Functions 和 Fluid compute。在响应完成前，使用路由中间件进行请求时路由。

监控功能现在为 Edge Functions 新增了三个指标，以提供 Edge Functions 活动和性能的全面视图：

- **Edge Function 调用次数**：追踪 Edge Functions 被调用的总次数，包括成功和错误的调用
- **Edge Function 执行单元**：衡量 Edge Functions 使用的 CPU 时间，以 50ms 为增量计算
- **快速源站传输（入站和出站）**：追踪与源站服务器之间的数据传输速率

**Edge Function 调用次数**：追踪 Edge Functions 被调用的总次数，包括成功和错误的调用

**Edge Function 执行单元**：衡量 Edge Functions 使用的 CPU 时间，以 50ms 为增量计算

**快速源站传输（入站和出站）**：追踪与源站服务器之间的数据传输速率

这些指标适用于所有 Observability Plus 和 Monitoring 客户。

Monitoring 最近已纳入 Observability Plus。

---

> 本文由AI自动翻译，原文链接：[Edge Function metrics now available in Monitoring - Vercel](https://vercel.com/changelog/edge-function-metrics-now-available-in-monitoring)
> 
> 翻译时间：2026-06-20 06:20
