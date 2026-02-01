---
title: Elysia框架现可自动部署于Vercel平台
title_original: Elysia can now be automatically deployed on Vercel - Vercel
date: '2025-11-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/support-for-elysia
author: ''
summary: 本文宣布Elysia——一款注重端到端类型安全且符合人体工程学的TypeScript框架，现已支持在Vercel平台上实现自动部署。Vercel能够自动识别Elysia应用，并为其配置最优资源以确保高效运行。文章提供了使用Node.js或通过配置选择Bun运行时的示例代码，并指出Vercel的后端默认采用Fluid
  compute和Active CPU pricing计费模式，用户只需为代码实际消耗的CPU时间付费。最后，文章引导读者访问相关文档以获取更多部署细节。
categories:
- 技术趋势
tags:
- Elysia
- Vercel
- TypeScript
- Bun
- Serverless
draft: false
translated_at: '2026-02-01T04:31:52.863984'
---

![](/images/posts/157d917927a0.jpg)

![](/images/posts/d33047b8a2a2.jpg)

Elysia，一款广受欢迎的、具有端到端类型安全的符合人体工程学的 TypeScript 框架，现在可以即时部署在 Vercel 上。

部署时，Vercel 现在会自动识别您的应用正在运行 Elysia，并调配最优资源以使其高效运行。

```
1import { Elysia } from "elysia";2
3const app = new Elysia()4  .get("/", () => `Hello from Elysia, running on Vercel!`);5
6export default app;7

```

默认情况下，Elysia 将使用 Node。您可以通过在 `vercel.json` 中添加如下所示的 `bunVersion` 行来选择使用 Bun 运行时。

```
1{2  "$schema": "https://openapi.vercel.sh/vercel.json",3  "bunVersion": "1.x"4}
```

Vercel 上的后端默认使用 **Fluid compute** 和 **Active CPU pricing**，因此您只需为代码主动使用 CPU 的时间付费。

在 Vercel 上部署 Elysia，或访问 Vercel 上的 [Elysia](https://vercel.com/docs/frameworks/elysia) 或 [Bun Runtime](https://vercel.com/docs/runtimes/bun) 文档。

---

> 本文由AI自动翻译，原文链接：[Elysia can now be automatically deployed on Vercel - Vercel](https://vercel.com/changelog/support-for-elysia)
> 
> 翻译时间：2026-02-01 04:31
