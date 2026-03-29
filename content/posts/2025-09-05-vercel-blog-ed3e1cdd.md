---
title: Vercel 支持零配置部署 Express 后端应用
title_original: Zero-configuration Express backends - Vercel
date: '2025-09-05'
source: Vercel Blog
source_url: https://vercel.com/changelog/zero-configuration-express-backends
author: ''
summary: Vercel 宣布其框架定义基础设施现已能够自动识别并深度理解 Express.js 应用程序，实现了真正的零配置部署。这意味着开发者无需在 vercel.json
  中手动配置重定向规则，也无需将应用代码放入特定的 /api 文件夹，即可将 Express 应用直接部署到 Vercel 平台。这一更新简化了 Node.js
  后端服务的部署流程，提升了开发效率，使得像输出“Hello World”这样的简单 Express 应用能够更快速、更便捷地上线。
categories:
- AI基础设施
tags:
- Vercel
- Express.js
- 无服务器部署
- Node.js
- 后端开发
draft: false
translated_at: '2026-03-29T05:03:11.817410'
---

![](/images/posts/bbb903c48a90.jpg)

![](/images/posts/4814e0209379.jpg)

Express，一个快速、灵活、极简的 Node.js Web 框架，现已支持零配置部署。

```
1import express from 'express'2const app = express()3
4app.get('/', (req, res) => {5  res.send('Hello World!')6})7
8export default app
```

一个在 Vercel 上运行的 "Hello World" Express.js 应用

Vercel 的框架定义基础设施现已能够识别并深度理解 Express 应用程序。此更新消除了在 `vercel.json` 中配置重定向或使用 `/api` 文件夹的需要。

在 Vercel 上部署 Express 或访问 Express on Vercel 文档。

---

> 本文由AI自动翻译，原文链接：[Zero-configuration Express backends - Vercel](https://vercel.com/changelog/zero-configuration-express-backends)
> 
> 翻译时间：2026-03-29 05:03
