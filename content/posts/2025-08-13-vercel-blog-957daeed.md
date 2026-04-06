---
title: Vercel推出运行时缓存API，实现跨函数数据共享与精准失效
title_original: Introducing the Runtime Cache API - Vercel
date: '2025-08-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/introducing-the-runtime-cache-api
author: ''
summary: Vercel正式推出运行时缓存API，允许开发者在同一区域内跨函数、路由中间件和构建过程中临时存储和检索数据。该API支持基于标签的失效机制，便于对缓存进行精确控制与高效管理。用户可通过代码示例快速上手，在可观测性仪表板中监控缓存命中率、失效模式及存储使用情况。读写操作将根据运行时区域计费，而Next.js
  13中相关的数据缓存功能目前仍处于测试阶段，暂不计费。此举旨在提升边缘计算场景下的数据共享效率与开发体验。
categories:
- AI基础设施
tags:
- Vercel
- 边缘计算
- 缓存API
- Serverless
- Web开发
draft: false
translated_at: '2026-04-06T04:44:53.939431'
---

您现在可以通过API访问Vercel的运行时缓存。

运行时缓存是一种临时缓存，用于在同一区域内跨函数、路由中间件和构建存储和检索数据。它支持基于标签的失效机制，以实现精确高效的缓存控制。

您可以像这样开始使用该API：

```
1import { getCache } from "@vercel/functions";2
3export async function GET(request) {4  const cache = getCache();5  const cacheKey = 'blog';6
7  const value = await cache.get(cacheKey);8
9  if (value) {10    return value;11  }12
13  const res = await fetch("https://api.vercel.app/blog");14  const originValue = await res.json();15
16  await cache.set(cacheKey, originValue, {17    ttl: 3600,18    tags: ['blogs'],19  });20
21  return originValue;22}
```

您可以在可观测性仪表板的“运行时缓存”选项卡中，监控所有应用程序的缓存命中率、失效模式和存储使用情况。

运行时缓存的读写操作将根据运行时区域进行计费。

由Next.js 13中的`unstable_cache()`和`fetch()`缓存使用的Vercel数据缓存仍处于测试阶段，在此期间不计费。

您仍可通过页面顶部的切换开关，在运行时缓存选项卡下查看Vercel数据缓存的使用情况。

在文档中了解更多关于运行时缓存的信息。

---

> 本文由AI自动翻译，原文链接：[Introducing the Runtime Cache API - Vercel](https://vercel.com/changelog/introducing-the-runtime-cache-api)
> 
> 翻译时间：2026-04-06 04:44
