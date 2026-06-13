---
title: Workflow SDK原生集成Nitro v3，性能与开发体验双提升
title_original: Workflow SDK now runs natively in Nitro v3 - Vercel
date: '2026-06-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/workflow-sdk-now-runs-natively-in-nitro-v3
author: ''
summary: Vercel宣布Workflow SDK现已原生集成到Nitro v3中，进入Beta阶段。步骤函数在应用相同的捆绑运行时内执行，无需独立捆绑包，并可直接使用Nitro的useStorage()等API。Nitro开发服务器提供/_workflow
  Web UI用于监控和调试。Workflow路由作为应用构建的一部分打包，依赖追踪和摇树优化使构建更快、包体积更小。
categories:
- AI基础设施
tags:
- Workflow SDK
- Nitro v3
- Vercel
- 开发工具
- 性能优化
draft: false
translated_at: '2026-06-13T06:20:18.809177'
---

Workflow SDK 原生的 Nitro v3 集成现已进入 Beta 阶段。步骤在应用其余部分相同的捆绑运行时内执行，而非独立的捆绑包。Nitro 的 `useStorage()` 及其他服务端 API 可直接在 `"use step"` 函数内部使用。

```
1import { useStorage } from "nitro/storage";2
3export async function getUserPreferences(userId: string) {4  "use step";5
6  const storage = useStorage("cache");7  return await storage.getItem(`preferences:${userId}`);8}
```

在步骤函数内从 Nitro 存储读取数据

Nitro 开发服务器还在 `/_workflow` 提供 Workflow Web UI。在浏览器中打开它，即可检查、监控和调试 Workflow 运行。

Workflow 路由现在由 Nitro 作为应用构建的一部分进行打包。依赖项会被追踪，未使用的代码会被摇树优化，因此输出仅包含实际运行的部分，从而实现更快的构建和更小的包体积。

立即开始使用 Nitro 上的 Workflow SDK。

---

> 本文由AI自动翻译，原文链接：[Workflow SDK now runs natively in Nitro v3 - Vercel](https://vercel.com/changelog/workflow-sdk-now-runs-natively-in-nitro-v3)
> 
> 翻译时间：2026-06-13 06:20
