---
title: Vercel Fluid计算全面支持ISR后台与按需更新
title_original: Fluid compute now supports ISR background and on-demand revalidation
  - Vercel
date: '2025-05-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/fluid-compute-now-supports-isr-background-and-on-demand-revalidation
author: ''
summary: Vercel宣布其Fluid compute现已支持所有项目中的后台与按需增量静态再生（ISR），无需更改配置即可享受性能提升。Fluid通过复用现有资源，为高并发工作负载降低高达85%的成本，兼具无服务器灵活性与服务器级效率。核心特性包括优化并发、零到无限扩展、低冷启动、按用量计费，并完整支持Node.js和Python，通过waitUntil支持后台任务。
categories:
- AI基础设施
tags:
- Vercel
- Fluid compute
- ISR
- 无服务器
- 性能优化
draft: false
translated_at: '2026-05-07T05:38:25.000154'
---

Fluid compute 现已在所有 Vercel 项目中支持后台与按需增量静态再生（ISR）。

这意味着 ISR 函数现在无需更改任何配置即可受益于 Fluid 的性能与并发效率。如果您近期重新部署过项目，您已经在使用该功能。

Fluid compute 在创建新资源之前会复用现有资源，从而为高并发工作负载降低高达 85% 的成本。它以无服务器灵活性提供服务器级效率，具体包括：

- 优化的并发能力
- 从零到无限扩展
- 极低的冷启动
- 按用量计费
- 完整支持 Node.js 和 Python
- 无需基础设施管理
- 通过 `waitUntil` 支持后台任务

优化的并发能力

从零到无限扩展

极低的冷启动

按用量计费

完整支持 Node.js 和 Python

无需基础设施管理

通过 `waitUntil` 支持后台任务

为您的现有项目启用 Fluid，并在我们的博客和文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Fluid compute now supports ISR background and on-demand revalidation - Vercel](https://vercel.com/changelog/fluid-compute-now-supports-isr-background-and-on-demand-revalidation)
> 
> 翻译时间：2026-05-07 05:38
