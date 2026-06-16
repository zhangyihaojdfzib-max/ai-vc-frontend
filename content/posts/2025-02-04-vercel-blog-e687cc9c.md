---
title: Vercel Functions 上线 Fluid 计算：效率与成本双提升
title_original: Vercel Functions can now run on Fluid compute - Vercel
date: '2025-02-04'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-functions-can-now-run-on-fluid-compute
author: ''
summary: Vercel 宣布其 Functions 现可在 Fluid 计算上运行，带来多项关键改进：优化并发使每个实例可处理多个请求，高并发下计算成本最高降低85%；冷启动保护通过智能扩缩容和预预热减少冷启动次数；优化扩缩容打破传统1:1模型；支持
  waitUntil 扩展函数生命周期；内置失控成本保护；多区域执行提升性能；并全面支持 Node.js 和 Python。Fluid 现已面向所有套餐开放。
categories:
- AI基础设施
tags:
- Vercel
- Fluid计算
- 无服务器函数
- 成本优化
- 性能提升
draft: false
translated_at: '2026-06-16T07:39:35.896439'
---

![](/images/posts/c6d993f9f422.jpg)

![](/images/posts/77fdf105d1fd.jpg)

Vercel Functions 现可在 Fluid 计算上运行，在效率、可扩展性和成本效益方面均有提升。Fluid 现已面向所有套餐开放。

### 链接到标题 新增功能

- **优化并发**：每个实例可处理多个请求，减少空闲时间，对于高并发工作负载，计算成本最高可降低 85%
- **冷启动保护**：通过更智能的扩缩容和预预热实例，减少冷启动次数
- **优化扩缩容**：函数在实例之前进行扩缩，超越传统的 1:1 调用与实例对应模型
- **扩展函数生命周期**：使用 `waitUntil` 在响应客户端后运行后台任务
- **失控成本保护**：检测并阻止无限循环和过度调用
- **多区域执行**：请求路由至所选计算区域中最近的位置，以获得更佳性能
- **支持 Node.js 和 Python**：对原生模块或标准库无限制

**优化并发**：每个实例可处理多个请求，减少空闲时间，对于高并发工作负载，计算成本最高可降低 85%

**冷启动保护**：通过更智能的扩缩容和预预热实例，减少冷启动次数

**优化扩缩容**：函数在实例之前进行扩缩，超越传统的 1:1 调用与实例对应模型

**扩展函数生命周期**：使用 `waitUntil` 在响应客户端后运行后台任务

**失控成本保护**：检测并阻止无限循环和过度调用

**多区域执行**：请求路由至所选计算区域中最近的位置，以获得更佳性能

**支持 Node.js 和 Python**：对原生模块或标准库无限制

立即启用 Fluid，或前往我们的博客和文档了解更多。

---

> 本文由AI自动翻译，原文链接：[Vercel Functions can now run on Fluid compute - Vercel](https://vercel.com/changelog/vercel-functions-can-now-run-on-fluid-compute)
> 
> 翻译时间：2026-06-16 07:39
