---
title: Vercel新功能：通过标签使CDN缓存失效
title_original: Invalidate the CDN cache by tag - Vercel
date: '2025-10-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/invalidate-the-cdn-cache-by-tag
author: ''
summary: 本文介绍了Vercel推出的新功能——通过标签使CDN缓存内容失效。该功能允许用户将特定标签关联的所有缓存内容标记为陈旧，下次请求时系统会立即提供旧内容并在后台重新验证，从而实现对用户无感知的缓存更新。文章详细说明了四种失效方法：仪表板设置、Vercel
  CLI、函数API和REST API，并提醒用户谨慎使用删除缓存功能，以避免可能导致的延迟或服务中断。所有套餐用户均可使用此功能。
categories:
- AI基础设施
tags:
- CDN缓存
- Vercel
- 缓存失效
- 前端部署
- 性能优化
draft: false
translated_at: '2026-02-22T04:34:22.198151'
---

![](/images/posts/868cc4cea936.jpg)

![](/images/posts/305267611ede.jpg)

您现在可以通过标签使CDN缓存内容失效。

此操作会将与该标签关联的所有缓存内容标记为陈旧。下一次请求会立即提供陈旧内容，同时后台进行重新验证，对用户无延迟影响。

有几种使内容失效的方法：

- 仪表板设置
- Vercel CLI
- 函数API
- REST API

仪表板设置

Vercel CLI

函数API

REST API

除了在原始内容更改时通过标签使其失效外，如果原始内容已删除，您也可以通过标签删除缓存。但请注意，删除缓存可能会在新内容生成期间增加延迟，或在您的源站无响应时导致服务中断，请谨慎使用。

所有套餐均可用。了解更多关于缓存失效的信息。

---

> 本文由AI自动翻译，原文链接：[Invalidate the CDN cache by tag - Vercel](https://vercel.com/changelog/invalidate-the-cdn-cache-by-tag)
> 
> 翻译时间：2026-02-22 04:34
