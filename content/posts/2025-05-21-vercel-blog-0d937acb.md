---
title: Vercel Blob 正式上线：高性能对象存储服务
title_original: Vercel Blob is now generally available - Vercel
date: '2025-05-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-blob-is-now-generally-available
author: ''
summary: Vercel Blob 现已全面可用，为工作流和应用提供高性能、全球可扩展的对象存储。该服务基于 S3 基础设施，确保 99.999999999%
  的数据持久性，已存储超 4 亿文件，并支持 v0.dev 等生产级应用。定价按用量计算，存储每 GB 每月 0.023 美元，操作与数据传输费用透明，其中 Blob
  数据传输成本比快速数据传输低 3 倍。Hobby 用户每月可享 1 GB 免费存储和 10 GB 免费数据传输。
categories:
- AI基础设施
tags:
- Vercel Blob
- 对象存储
- 云基础设施
- S3兼容
- 开发者工具
draft: false
translated_at: '2026-05-10T05:39:08.829508'
---

![](/images/posts/883bc18d7a10.jpg)

![](/images/posts/29f9fd6933a0.jpg)

Vercel Blob 现已全面可用，将高性能、全球可扩展的对象存储引入您的工作流程和应用中。

Blob 存储底层基于 S3 基础设施，确保 99.999999999% 的数据持久性，目前已存储超过 4 亿个文件，并为 v0.dev 等生产级应用提供支持。

定价按用量计算：

- 存储：每月每 GB 0.023 美元
- 简单 API 操作（如读取）：每百万次 0.40 美元
- 高级操作（如上传）：每百万次 5.00 美元
- Blob 数据传输：每 GB 起价 0.050 美元

存储：每月每 GB 0.023 美元

简单 API 操作（如读取）：每百万次 0.40 美元

高级操作（如上传）：每百万次 5.00 美元

Blob 数据传输：每 GB 起价 0.050 美元

定价适用于：

- 即日起新建的 Blob 存储
- 2025 年 6 月 16 日起的现有存储

即日起新建的 Blob 存储

2025 年 6 月 16 日起的现有存储

存储和操作定价与 S3 一致，Blob 数据传输是一种新的直接对象访问机制，其成本比快速数据传输最多低 3 倍，并直接集成 Vercel 的全球缓存层。

Hobby 用户现在可获得更高的免费使用额度：每月 1 GB 存储和 10 GB Blob 数据传输。

立即开始使用 Vercel Blob，并在文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Blob is now generally available - Vercel](https://vercel.com/changelog/vercel-blob-is-now-generally-available)
> 
> 翻译时间：2026-05-10 05:39
