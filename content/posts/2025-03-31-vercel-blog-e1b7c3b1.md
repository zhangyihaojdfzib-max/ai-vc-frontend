---
title: Flags SDK 3.2：SvelteKit预计算标志提升页面性能
title_original: Flags SDK 3.2 - Vercel
date: '2025-03-31'
source: Vercel Blog
source_url: https://vercel.com/changelog/flags-sdk-3-2
author: ''
summary: Flags SDK 3.2版本新增了对SvelteKit中预计算特性标志的支持，通过在Edge Middleware中评估标志来决定页面变体，使营销页面保持静态并快速加载，避免布局偏移。该版本还解决了静态使用多个标志时的组合爆炸问题，支持构建时生成不同变体及增量静态再生成。同时，文档按框架拆分并明确列出适配器供应商。
categories:
- 技术趋势
tags:
- Flags SDK
- SvelteKit
- 预计算标志
- Edge Middleware
- 性能优化
draft: false
translated_at: '2026-05-31T06:30:50.808666'
---

![](/images/posts/34f4315b07ca.jpg)

![](/images/posts/10e9ee46eaca.jpg)

TheFlags SDK 3.2版本新增了对SvelteKit中预计算特性标志的支持，使营销页面的实验更便捷，同时保持页面快速加载并避免布局偏移。

![Edge Middleware决定展示页面的哪个变体](/images/posts/8330a5547948.jpg)

![Edge Middleware决定展示页面的哪个变体](/images/posts/2e878735c90e.jpg)

预计算标志在Edge Middleware中进行评估，以决定展示页面的哪个变体。这使页面保持静态，从而通过边缘网络提供静态变体，实现低全局延迟。

预计算处理了静态使用多个特性标志时的组合爆炸问题。在构建时生成页面的不同变体，依赖增量静态再生成仅按需构建特定组合，以及更多功能。

我们还改进了Flags SDK文档，将其按不同框架拆分，并明确列出了所有为Flags SDK提供适配器的供应商。

了解更多关于SvelteKit的Flags SDK以及预计算模式的信息。

---

> 本文由AI自动翻译，原文链接：[Flags SDK 3.2 - Vercel](https://vercel.com/changelog/flags-sdk-3-2)
> 
> 翻译时间：2026-05-31 06:30
