---
title: Vercel团队项目间重写数据传输免费
title_original: Fast Data Transfer for rewrites between your team's projects is now
  free - Vercel
date: '2025-02-27'
source: Vercel Blog
source_url: https://vercel.com/changelog/fast-data-transfer-for-rewrites-between-a-teams-projects-is-now-free
author: ''
summary: Vercel宣布，同一团队内项目间的外部重写现在对原始请求的快速数据传输免费。该功能常用于反向代理或微前端架构，可在vercel.json、中间件或next.config.js中配置。优化后，原始与目标请求的数据流合并，减少总体传输量，同时每次重写仍触发完整请求生命周期和安全检查。用户可监控使用情况与可观测性。
categories:
- AI基础设施
tags:
- Vercel
- 快速数据传输
- 重写
- 微前端
- 反向代理
draft: false
translated_at: '2026-06-06T05:52:37.892430'
---

同一团队内项目间的外部重写现在仅对目标请求使用快速数据传输。此项变更使得原始请求的快速数据传输变为免费。

作为反向代理或微前端架构的常见用法，重写可在 `vercel.json`、中间件或 `next.config.js` 中配置，用于在同一或不同 Vercel 项目之间路由请求，同时保持用户看到的 URL 不变。

同一团队的外部重写使用说明：

- 原始请求和目标请求的快速数据传输已优化并合并为单一数据流，从而减少总体传输量。
- 每次外部重写都会触发完整的请求生命周期，包括路由和 Web 应用程序防火墙检查，确保每个项目都执行安全策略，并计为一次独立的边缘请求。

原始请求和目标请求的快速数据传输已优化并合并为单一数据流，从而减少总体传输量。

每次外部重写都会触发完整的请求生命周期，包括路由和 Web 应用程序防火墙检查，确保每个项目都执行安全策略，并计为一次独立的边缘请求。

了解重写，并监控您的快速数据传输使用情况和可观测性。

---

> 本文由AI自动翻译，原文链接：[Fast Data Transfer for rewrites between your team's projects is now free - Vercel](https://vercel.com/changelog/fast-data-transfer-for-rewrites-between-a-teams-projects-is-now-free)
> 
> 翻译时间：2026-06-06 05:52
