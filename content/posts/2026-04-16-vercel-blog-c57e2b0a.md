---
title: Vercel Flags功能开关服务全面开放，内置平台支持多框架
title_original: Vercel Flags is now generally available - Vercel – Vercel
date: '2026-04-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-flags-ga
author: ''
summary: Vercel宣布其内置功能开关服务Vercel Flags现已全面开放使用。该服务允许开发者直接在Vercel仪表板中通过目标规则、用户细分和环境控制来创建和管理功能开关。Flags
  SDK为Next.js和SvelteKit应用程序提供了框架原生的集成方式，开发者只需几行代码即可在应用中使用功能开关进行功能发布或回滚。此外，通过支持OpenFeature标准，使用其他框架或自定义后端的团队也能将Vercel
  Flags接入其提供商无关的SDK，实现了灵活的部署控制与渐进式发布能力。
categories:
- AI基础设施
tags:
- Vercel
- 功能开关
- DevOps
- 前端开发
- 云平台
draft: false
translated_at: '2026-04-18T04:42:06.166962'
---

![](/images/posts/e0a42a142652.jpg)

![](/images/posts/e0d129eb313e.jpg)

Vercel Flags现已全面开放使用。

Vercel Flags是内置于Vercel平台的功能开关服务提供商。您可以直接在Vercel仪表板中，通过目标规则、用户细分和环境控制来创建和管理功能开关。

Flags SDK提供了一种框架原生的方式，可在Next.js和SvelteKit应用程序中定义和使用这些功能开关，并直接与您现有的代码库集成：

```
1import { vercelAdapter } from "@flags-sdk/vercel"2import { flag } from "flags/next"3
4export const showNewFeature = flag({5  key: "show-new-feature",6  adapter: vercelAdapter()7})
```

定义功能开关后，您只需几行代码即可在应用程序中使用它们：

```
1import { showNewFeature } from "~/flags"2
3export default async function Page() {  4  const isEnabled = await showNewFeature()5
6  return isEnabled ? <NewDashboard /> : <OldDashboard />7}
```

对于使用其他框架或自定义后端的团队，Vercel Flags适配器支持OpenFeature标准，允许您将Vercel Flags接入其提供商无关的SDK。

立即试用或了解更多关于Vercel Flags的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Flags is now generally available - Vercel – Vercel](https://vercel.com/changelog/vercel-flags-ga)
> 
> 翻译时间：2026-04-18 04:42
