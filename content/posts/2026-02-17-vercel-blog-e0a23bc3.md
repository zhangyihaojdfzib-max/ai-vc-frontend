---
title: Vercel 改进运行时日志导出：支持流式下载与精准筛选
title_original: Improved streaming runtime logs exports - Vercel
date: '2026-02-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/improved-streaming-runtime-logs-exports
author: ''
summary: Vercel 宣布改进其运行时日志导出功能，新增流式传输至浏览器的下载方式，用户无需等待文件缓冲即可在后台执行导出并继续使用仪表板。同时增加了两个导出选项：可精确导出屏幕上显示的内容，或导出所有符合当前搜索条件的请求。所有套餐用户最多可导出
  10,000 条请求，而可观测性增强版订阅用户最多可导出 100,000 条。导出的日志数据现已按请求建立索引，确保与仪表板界面的一致性，导出限制也按请求应用，以匹配筛选后的请求数据。
categories:
- AI基础设施
tags:
- Vercel
- 日志导出
- 流式传输
- 可观测性
- 开发工具
draft: false
translated_at: '2026-02-19T04:43:40.696491'
---

借助运行时日志，您可以查看并导出日志记录。现在导出功能可直接流式传输至浏览器——下载立即开始，您可以在后台执行导出的同时继续使用 Vercel 仪表板。这消除了等待大文件缓冲的需要。

此外，我们新增了两个选项：您现在可以精确导出屏幕上显示的内容，或导出所有符合当前搜索条件的请求。

![](/images/posts/f906eebf3c0d.jpg)

![](/images/posts/2fd5d911f28e.jpg)

所有套餐每次最多可导出 10,000 条请求，而**可观测性增强版**订阅用户最多可导出 100,000 条请求。

导出的日志数据现已按请求建立索引，以确保与**运行时日志**仪表板界面的一致性。导出限制现按请求应用，以确保导出的数据与仪表板上显示的筛选请求相匹配。

了解更多关于运行时日志的信息。

---

> 本文由AI自动翻译，原文链接：[Improved streaming runtime logs exports - Vercel](https://vercel.com/changelog/improved-streaming-runtime-logs-exports)
> 
> 翻译时间：2026-02-19 04:43
