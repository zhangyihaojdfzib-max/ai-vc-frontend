---
title: Vercel CDN全面支持stale-if-error指令，提升源站故障时缓存韧性
title_original: Stale-if-error cache-control directive now supported for all responses
  - Vercel
date: '2026-02-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/stale-if-error-cache-control-header-is-now-supported
author: ''
summary: Vercel宣布其CDN现已全面支持Cache-Control头部中的`stale-if-error`指令。该指令允许开发者为缓存响应设置一个时间窗口（以秒为单位），当向源站请求失败（如遇到500错误、网络或DNS故障）时，CDN可在此窗口内继续提供已过期的缓存响应，而非直接向客户端返回错误。这一功能显著增强了应用程序的弹性，确保在上游服务暂时不可用时，终端用户仍能获得响应，从而提升了系统的可用性与用户体验。
categories:
- AI基础设施
tags:
- Vercel
- CDN
- 缓存策略
- Web性能
- 高可用性
draft: false
translated_at: '2026-02-14T04:16:34.803245'
---

Vercel CDN 现已支持在 Cache-Control 头部中使用 `stale-if-error` 指令，从而在源站故障时实现更具弹性的缓存行为。

您现在可以使用 `stale-if-error` 指令来指定，当向源站的请求失败时，一个过期的缓存响应仍可被提供服务的时长（以秒为单位）。当存在此指令且源站返回错误时，CDN 可能会提供先前缓存的响应，而不是将错误返回给客户端。对于诸如 500 内部服务器错误、网络故障或 DNS 错误等情况，都可能提供过期的响应。

这允许应用程序在上游服务暂时不可用时保持可用并优雅地响应。

阅读 `stale-if-error` 文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Stale-if-error cache-control directive now supported for all responses - Vercel](https://vercel.com/changelog/stale-if-error-cache-control-header-is-now-supported)
> 
> 翻译时间：2026-02-14 04:16
