---
title: Vercel Sandbox 新增动态延长超时功能，支持长时间运行任务
title_original: Dynamically extend timeout of an active Sandbox - Vercel
date: '2025-10-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/dynamically-extend-timeout-of-an-active-sandbox
author: ''
summary: Vercel 为其 Sandbox 环境引入了新的 `extendTimeout` 方法，允许用户动态延长正在运行的沙盒的超时时间。这一功能解决了长时间运行流程（如链式智能体任务或多步骤代码生成）可能超出初始超时限制的问题。用户可以通过调用该方法多次延长沙盒的存活时间，直至达到订阅计划规定的最大运行时长上限。其中，Pro
  和 Enterprise 计划最多支持 5 小时，Hobby 计划最多支持 45 分钟。这为开发者处理耗时较长的异步任务提供了更大的灵活性和便利性。
categories:
- AI基础设施
tags:
- Vercel
- 开发工具
- 云计算
- 沙盒环境
- 超时管理
draft: false
translated_at: '2026-02-14T04:16:34.253360'
---

您现在可以使用新的 `extendTimeout` 方法来延长正在运行的 Vercel Sandbox 的持续时间。

这使得长时间运行的沙盒能够在其初始超时后保持活动状态，从而更容易支持那些耗时超出预期的流程，例如链式智能体任务或多步骤代码生成。

```
1const sandbox = await Sandbox.create({2  3  timeout: 15 * 60 * 1000,4});5
67await sandbox.extendTimeout(10 * 60 * 1000);
```

您可以多次延长超时时间，直至达到您订阅计划所允许的**最大运行时间**。

Pro 和 Enterprise 计划最多支持 5 小时，Hobby 计划最多支持 45 分钟。

立即开始使用 Sandbox，并在文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Dynamically extend timeout of an active Sandbox - Vercel](https://vercel.com/changelog/dynamically-extend-timeout-of-an-active-sandbox)
> 
> 翻译时间：2026-02-14 04:16
