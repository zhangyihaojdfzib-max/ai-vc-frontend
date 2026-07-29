---
title: Vercel Sandbox 新增分支创建功能
title_original: Vercel Sandbox supports forking - Vercel
date: '2026-07-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-supports-forking
author: ''
summary: Vercel Sandbox 推出分支创建功能，允许用户通过 `Sandbox.fork()` 从现有沙盒快照创建独立副本，继承配置和环境变量。该功能可用于派生智能体、为租户提供模板副本或并行运行不同配置变体。分支创建时间与新建沙盒相当，支持通过
  SDK 和 CLI 操作，需升级至最新版本。
categories:
- AI基础设施
tags:
- Vercel
- Sandbox
- 分支创建
- 云沙盒
- 开发工具
draft: false
translated_at: '2026-07-29T05:33:29.914314'
---

Vercel Sandbox 现在支持通过 `Sandbox.fork()` 进行分支创建。

分支从源的当前快照开始，并继承其配置和环境变量。如果源正在运行，则分支会基于最近保存的状态，而非实时的内存状态。如果源没有快照，则会回退到全新创建，使用源的运行时和配置。你传入的任何参数都会覆盖继承的值。

分支创建所需的时间与创建沙盒大致相同，并遵循相同的限制。你可以用它从一个共享基础派生出 Agent（智能体），为每个租户提供模板的独立副本，或并行运行同一配置的不同变体。

使用 SDK 分支创建沙盒：

```
1import { Sandbox } from '@vercel/sandbox';23const fork = await Sandbox.fork({4  sourceSandbox: 'prod-agent',5});67const customized = await Sandbox.fork({8  sourceSandbox: 'prod-agent',9  name: 'forked-prod-agent',10  resources: {11    vcpus: 4,12  }13});
```

使用 CLI 分支创建沙盒：

```
sandbox fork prod-agent --name forked-prod-agent --vcpus 4
```

要开始使用，请升级到最新版本：

- pnpm install @vercel/sandbox@latest # SDK
- pnpm install -g sandbox@latest # CLI

pnpm install @vercel/sandbox@latest # SDK

pnpm install -g sandbox@latest # CLI

更多信息请参阅 Sandbox 文档。

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox supports forking - Vercel](https://vercel.com/changelog/vercel-sandbox-supports-forking)
> 
> 翻译时间：2026-07-29 05:33
