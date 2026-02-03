---
title: Vercel 可观测性功能升级：全面支持重定向与外部重写监控
title_original: Redirects and rewrites now available in Observability - Vercel
date: '2025-11-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/redirects-and-rewrites-now-available-in-observability
author: ''
summary: Vercel 宣布其可观测性功能现已面向所有客户开放对重定向和外部重写的监控支持。外部重写允许 Vercel 作为反向代理或独立 CDN，将请求转发至外部
  API 或网站。所有计划客户均可查看外部重写总数及按主机名统计的指标，而 Pro 和 Enterprise 计划客户升级至可观测性增强版后，还能获取连接延迟、按路径统计的重写详情及重定向位置等深度数据。此外，Drains
  功能也已更新，支持记录重定向、外部重写及缓存的外部重写日志，帮助开发者更好地诊断和优化网络请求性能。
categories:
- AI基础设施
tags:
- Vercel
- 可观测性
- 重定向
- CDN
- 性能监控
draft: false
translated_at: '2026-02-03T04:16:53.959130'
---

![显示选择加入重定向请求日志的编辑Drain模态窗口的图片](/images/posts/3c47cb20625a.jpg)

![显示选择加入重定向请求日志的编辑Drain模态窗口的图片](/images/posts/eb64334f1158.jpg)

针对**重定向**和**外部重写**的改进可观测性现已面向所有 Vercel 客户开放。

外部重写将请求转发到您 Vercel 项目之外的 API 或网站，这实际上允许 Vercel 充当反向代理或独立的 CDN。

![按主机名或路径查看外部重写、连接延迟和错误](/images/posts/609aab072e0b.jpg)

![按主机名或路径查看外部重写、连接延迟和错误](/images/posts/8df6e6b27a49.jpg)

所有计划的客户都将获得新的视图，以查看关键重写指标：

-   外部重写总数
-   按主机名统计的外部重写

外部重写总数

按主机名统计的外部重写

Pro 和 Enterprise 计划的客户可以升级到**可观测性增强版**以获得：

-   到外部主机的连接延迟
-   按源/目标路径统计的重写
-   重定向位置的路径和路由

到外部主机的连接延迟

按源/目标路径统计的重写

重定向位置的路径和路由

**Drains** 也已更新，以支持以下内容：

-   重定向
-   外部重写
-   缓存的外部重写

重定向

外部重写

缓存的外部重写

[查看外部重写](https://vercel.com/docs/observability/external-rewrites)或[了解更多关于可观测性的信息](https://vercel.com/docs/observability)。

---

> 本文由AI自动翻译，原文链接：[Redirects and rewrites now available in Observability - Vercel](https://vercel.com/changelog/redirects-and-rewrites-now-available-in-observability)
> 
> 翻译时间：2026-02-03 04:16
