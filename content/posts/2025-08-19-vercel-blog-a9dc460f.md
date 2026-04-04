---
title: Vercel Functions 现已支持 fetch web handlers，提升Node.js互操作性
title_original: Node.js Vercel Functions now support fetch web handlers - Vercel
date: '2025-08-19'
source: Vercel Blog
source_url: https://vercel.com/changelog/node-js-vercel-functions-now-support-fetch-web-handlers
author: ''
summary: Vercel宣布其Node.js环境中的Functions现已支持fetch web handlers，允许开发者使用与Web标准兼容的fetch
  API来处理HTTP请求。这一更新增强了不同JavaScript运行时和框架之间的互操作性，简化了开发流程。开发者现在可以导出fetch函数来处理请求，并返回Response对象，同时仍支持按需导出独立的HTTP方法。此举旨在为开发者提供更灵活、更符合现代Web标准的无服务器函数开发体验。
categories:
- 技术趋势
tags:
- Vercel
- Node.js
- 无服务器
- Web标准
- 开发工具
draft: false
translated_at: '2026-04-04T04:29:33.566466'
---

博客/更新日志

# Node.js Vercel Functions 现已支持 fetch web handlers

## 作者

运行在 Node.js 环境中的 Vercel Functions 现已支持 `fetch` web handlers，这提升了跨 JavaScript 运行时和框架的互操作性。

```
1export default {2  fetch(request: Request) { 3    return new Response('Hello from Vercel!');4  }5};
```

您仍然可以按需导出独立的 HTTP 方法。

在文档中了解更多关于 `fetch` web handlers 的信息。

---

> 本文由AI自动翻译，原文链接：[Node.js Vercel Functions now support fetch web handlers - Vercel](https://vercel.com/changelog/node-js-vercel-functions-now-support-fetch-web-handlers)
> 
> 翻译时间：2026-04-04 04:29
