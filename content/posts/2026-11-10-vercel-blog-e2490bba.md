---
title: Speed Insights and Web Analytics now support custom environments - Vercel
title_original: Speed Insights and Web Analytics now support custom environments -
  Vercel
date: '2026-11-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/speed-insights-and-web-analytics-now-support-custom-environments
author: ''
summary: '[翻译失败，原文如下]


  Speed InsightsandWeb Analyticsnow fully supportcustom environments.


  Previously, data captured on deployments to a custom environment was...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-11T09:04:26.292458'
---

[翻译失败，原文如下]

Speed InsightsandWeb Analyticsnow fully supportcustom environments.

Previously, data captured on deployments to a custom environment was attributed to the Preview environment. That data is now attributed to the custom environment it came from, so you can track performance and traffic for staging, QA, or canary environments separately from Production and Preview.

![Speed Insights Environment dropdown showing All Environments, Production, Preview, and the custom environments staging and pre-production.](/images/posts/8adec3441d55.jpg)

![Speed Insights Environment dropdown showing All Environments, Production, Preview, and the custom environments staging and pre-production.](/images/posts/2cd5ada99437.jpg)

You can view this data in several places:

- Dashboard:use the Environment dropdown in Speed Insights and Web Analytics to pick a custom environment
- CLI:query it with thevc metricscommand
- Query builder:filter and break down by environment
- Aggregation API:query it programmatically (Web Analytics only)

Dashboard:use the Environment dropdown in Speed Insights and Web Analytics to pick a custom environment

CLI:query it with thevc metricscommand

Query builder:filter and break down by environment

Aggregation API:query it programmatically (Web Analytics only)

This change only affects how data is attributed. No new data points are collected, and no configuration changes are needed.

Custom environments are available on Pro and Enterprise plans. Learn more in theenvironments documentation.

---

> 本文由AI自动翻译，原文链接：[Speed Insights and Web Analytics now support custom environments - Vercel](https://vercel.com/changelog/speed-insights-and-web-analytics-now-support-custom-environments)
> 
> 翻译时间：2026-11-11 09:04
