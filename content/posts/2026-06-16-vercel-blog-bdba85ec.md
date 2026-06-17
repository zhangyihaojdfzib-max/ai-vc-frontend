---
title: Vercel Sandbox会话时长延长至24小时
title_original: Vercel Sandbox can now run for up to 24 hours - Vercel
date: '2026-06-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-can-now-run-for-up-to-24-hours
author: ''
summary: Vercel宣布其Sandbox产品支持最长24小时的不间断会话，较此前的5小时大幅提升。这一更新使开发者能够处理大规模数据处理、端到端测试流水线以及长期运行的Agent工作流等耗时任务。结合持久化Sandbox功能，可在长时间运行中维持持久状态。新时长适用于所有Pro和Enterprise套餐用户，为需要更长运行时间的云开发工作负载提供了更灵活的基础设施支持。
categories:
- AI基础设施
tags:
- Vercel
- Sandbox
- 云开发
- 工作负载
- 基础设施
draft: false
translated_at: '2026-06-17T07:09:15.921941'
---

Vercel Sandbox 现在可以运行长达 24 小时（此前为 5 小时）的不间断会话。这一新的最长持续时间解锁了需要更长运行时间的工作负载，例如大规模数据处理、端到端测试流水线以及长期运行的 Agent（智能体）工作流。

```
1import { Sandbox } from '@vercel/sandbox';2
3const sandbox = await Sandbox.create({4  
5  timeout: 24 * 60 * 60 * 1000,6});
```

配合持久化 Sandbox 使用，可在长时间运行中维持持久状态。

24 小时最长持续时间适用于所有 Pro 和 Enterprise 套餐。了解更多限制信息，请参阅文档。

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox can now run for up to 24 hours - Vercel](https://vercel.com/changelog/vercel-sandbox-can-now-run-for-up-to-24-hours)
> 
> 翻译时间：2026-06-17 07:09
