---
title: 在Vercel防火墙中管理Next.js Server Actions
title_original: Manage Next.js Server Actions in the Vercel Firewall - Vercel
date: '2025-10-24'
source: Vercel Blog
source_url: https://vercel.com/changelog/manage-next-js-server-actions-in-the-vercel-firewall
author: ''
summary: 本文介绍了Vercel防火墙与可观测性插件对Next.js Server Actions的一流支持。自Next.js 15.5起，用户可以为特定的服务器操作名称配置自定义规则，例如对某个操作（如`app/auth/actions.ts#getUser`）设置每分钟每IP
  100次请求的速率限制。该功能已面向所有Vercel计划免费提供，旨在帮助开发者更好地管理和保护其服务器端操作，防止滥用并提升应用安全性。
categories:
- AI基础设施
tags:
- Vercel
- Next.js
- Server Actions
- 防火墙
- 速率限制
draft: false
translated_at: '2026-02-09T04:27:07.976626'
---

Vercel防火墙与可观测性插件为Server Actions提供了一流的支持。

从Next.js 15.5开始，客户现在可以针对特定的服务器操作名称配置自定义规则。在下面的示例中，您可以将`app/auth/actions.ts#getUser`操作的速率限制为每个IP地址每分钟100个请求。

![](/images/posts/1c700acdedcf.jpg)

![](/images/posts/3524a69c7ca8.jpg)

```
12'use server' 3
4export async function getUser(userId: string) { 5  6}
```

Server Action Name功能已在防火墙中面向所有计划提供，无需额外费用。请阅读相关文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Manage Next.js Server Actions in the Vercel Firewall - Vercel](https://vercel.com/changelog/manage-next-js-server-actions-in-the-vercel-firewall)
> 
> 翻译时间：2026-02-09 04:27
