---
title: Vercel推出ISR请求合并机制，防止缓存雪崩
title_original: Request collapsing for ISR cache misses - Vercel
date: '2025-09-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/request-collapsing-for-isr-cache-misses
author: ''
summary: Vercel在其CDN中引入了请求合并机制，以解决增量静态再生（ISR）页面过期时可能引发的缓存雪崩问题。当多个请求同时访问一个过期的ISR页面时，该机制确保仅触发一次页面再生函数调用，其余请求则等待并共享结果。这有效避免了因大量并发再生请求导致的计算资源浪费和后端过载，提升了系统可靠性和资源效率。该功能可自动应用于可缓存路由，无需额外配置。
categories:
- AI基础设施
tags:
- Vercel
- CDN
- ISR
- 请求合并
- 缓存优化
draft: false
translated_at: '2026-02-26T04:32:55.645006'
---

Vercel CDN 现通过**请求合并**机制防止缓存雪崩——当某个**增量静态再生（ISR）**页面过期时，每个区域仅触发一次函数调用。若无合并机制，同时到达的多个请求会各自触发重新生成，既浪费计算资源又导致后端过载。启用合并后，仅一个请求执行页面再生，其余请求则等待并返回缓存结果。

此举提升了系统可靠性，减轻了后端负载，并在大规模场景下显著节省计算资源。

该功能可自动应用于可缓存路由。系统通过框架元数据推断路由的可缓存性，无需额外配置。

具体实现细节可参阅博客文章《防止雪崩：Vercel CDN 中的请求合并机制》。

---

> 本文由AI自动翻译，原文链接：[Request collapsing for ISR cache misses - Vercel](https://vercel.com/changelog/request-collapsing-for-isr-cache-misses)
> 
> 翻译时间：2026-02-26 04:32
