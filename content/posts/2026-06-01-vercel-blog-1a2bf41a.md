---
title: Vercel Blob 支持 OIDC 认证，提升安全性
title_original: Vercel Blob now supports OIDC authentication - Vercel
date: '2026-06-01'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-blob-now-supports-oidc-authentication
author: ''
summary: Vercel Blob 现已支持 OIDC 认证，并在新项目中默认启用。该认证使用短期自动轮换的 Token，取代了长期有效的 BLOB_READ_WRITE_TOKEN，从而增强了安全性。用户可通过更新
  @vercel/blob 库并升级存储来启用此功能。Vercel 函数会自动接收 Token 进行认证，CLI 工具也支持自动获取环境变量，方便终端操作。此举简化了开发流程，降低了密钥泄露风险。
categories:
- AI基础设施
tags:
- Vercel
- OIDC认证
- 云存储
- 安全
- 开发者工具
draft: false
translated_at: '2026-06-02T06:35:33.347950'
---

Vercel Blob 现已支持 OIDC 认证，并且在连接新项目时默认启用该设置。

Vercel 签发的 OIDC Token 有效期短且会自动轮换，因此您不再需要长期有效的 `BLOB_READ_WRITE_TOKEN`。

要升级现有存储，请先将项目更新为使用最新的 `@vercel/blob`，然后导航至 Blob 存储下的 **Projects** 选项卡，并从项目的上下文菜单中选择 **Upgrade to OIDC**。

在 Vercel 上运行的函数会自动接收 Token 并使用它来认证请求：

```
1import { put } from '@vercel/blob';2const { url } = await put('hello.txt', 'Hello, world!', {3  access: 'public',4});
```

使用 OIDC 认证将文件上传至 Blob，无需长期有效的 Token。

一旦您更新了 Vercel CLI，它会自动获取相同的环境变量，因此您和您的 Agent（智能体）可以在终端中读写私有存储，而无需长期有效的 Token：

```
vercel linkvercel env pullvercel blob put hello.txt --from-file ./hello.txtvercel blob listvercel blob del hello.txt
```

关联项目、拉取环境变量，然后在终端中读写 Blob。

阅读[文档](documentation)以开始使用。

---

> 本文由AI自动翻译，原文链接：[Vercel Blob now supports OIDC authentication - Vercel](https://vercel.com/changelog/vercel-blob-now-supports-oidc-authentication)
> 
> 翻译时间：2026-06-02 06:35
