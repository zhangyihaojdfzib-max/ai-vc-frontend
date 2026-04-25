---
title: Vercel CDN默认遵循外部源站缓存头
title_original: Vercel CDN now respects Cache-Control headers from external origins
  by default - Vercel – Vercel
date: '2026-03-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercels-cdn-now-respects-cache-control-headers-from-external-origins-by-default
author: ''
summary: Vercel宣布自4月6日起，新建项目在代理请求至外部源站时，将默认遵循上游的Cache-Control、CDN-Cache-Control和Vercel-CDN-Cache-Control头部进行缓存。此前默认不缓存，需手动配置。现有项目可通过仪表盘启用新行为，并支持通过缓存标签清除缓存。用户也可为特定路径禁用缓存。
categories:
- AI基础设施
tags:
- Vercel
- CDN
- 缓存策略
- Cache-Control
- 基础设施更新
draft: false
translated_at: '2026-04-25T04:36:56.419427'
---

自4月6日起，新建Vercel项目在代理请求至外部源站时，将默认遵循`cache-control`头部。

此前，通过重写至外部源站所响应的内容默认不缓存，如需启用缓存需在`vercel.json`中添加`x-vercel-enable-rewrite-caching`头部。现在，Vercel的CDN将自动遵循您源站的缓存头部。

变更内容：

- 对于新建项目，Vercel将根据上游`Cache-Control`、`CDN-Cache-Control`和`Vercel-CDN-Cache-Control`头部，默认缓存来自外部源站的响应。
- 您可以使用源站的缓存标签（`Vercel-Cache-Tag`头部）来清除缓存内容。
- 现有项目可通过项目仪表盘选择启用新的缓存行为。
- 您可以通过将`x-vercel-enable-rewrite-caching`头部设置为`0`，为特定请求路径禁用缓存。

对于新建项目，Vercel将根据上游`Cache-Control`、`CDN-Cache-Control`和`Vercel-CDN-Cache-Control`头部，默认缓存来自外部源站的响应。

您可以使用源站的缓存标签（`Vercel-Cache-Tag`头部）来清除缓存内容。

现有项目可通过项目仪表盘选择启用新的缓存行为。

您可以通过将`x-vercel-enable-rewrite-caching`头部设置为`0`，为特定请求路径禁用缓存。

在4月6日之前，请检查您的上游缓存头部——当创建代理至外部源站且未启用缓存的新项目时，确保这些头部能反映您预期的缓存策略。

了解更多关于重写至外部源站的信息，并在项目设置的CDN标签页中配置路由。

---

> 本文由AI自动翻译，原文链接：[Vercel CDN now respects Cache-Control headers from external origins by default - Vercel – Vercel](https://vercel.com/changelog/vercels-cdn-now-respects-cache-control-headers-from-external-origins-by-default)
> 
> 翻译时间：2026-04-25 04:36
