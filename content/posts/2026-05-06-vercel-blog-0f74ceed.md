---
title: Vercel推出仅生产环境凭证保护功能
title_original: Secure Marketplace credentials with Production-only access - Vercel
date: '2026-05-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/secure-marketplace-credentials-with-production-only-access
author: ''
summary: Vercel新增安全功能，允许用户将原生集成资源设置为“仅生产环境”，从而移除非生产环境的访问权限，并将凭证作为敏感环境变量保护。应用后，开发与预览环境连接将被移除，新非生产连接被阻止，无生产目标的连接断开，且凭证无法从仪表盘或CLI读取。恢复设置需所有者权限并可能要求MFA验证。
categories:
- AI基础设施
tags:
- Vercel
- 安全
- 环境变量
- 生产环境
- 凭证保护
draft: false
translated_at: '2026-05-06T05:30:14.096776'
---

![](/images/posts/d79c31f69300.jpg)

![](/images/posts/32c7ae7902cb.jpg)

现在，您可以通过限制原生集成资源的使用位置来保护它们。将资源设置为**仅生产环境**可移除非生产环境的访问权限，并将凭证作为**敏感环境变量**进行保护，因此密钥值将无法再从仪表盘或 CLI 中读取。

在集成资源的**设置**中，选择**允许的环境 → 仅生产环境**并保存。我们建议您在保存后轮换集成资源的密钥。

应用后：

- 开发环境和预览环境的连接将被移除
- 新的非生产环境连接将被阻止
- 没有生产环境目标的连接将被断开
- 凭证将受到保护且无法再读取

开发环境和预览环境的连接将被移除

新的非生产环境连接将被阻止

没有生产环境目标的连接将被断开

凭证将受到保护且无法再读取

恢复此设置需要**所有者**权限。所有者可以从**设置**中重新启用开发环境和预览环境的访问权限，并在需要时重新连接项目。您可能会被要求通过 MFA 验证进行重新认证。要了解更多信息，请阅读**文档**。

---

> 本文由AI自动翻译，原文链接：[Secure Marketplace credentials with Production-only access - Vercel](https://vercel.com/changelog/secure-marketplace-credentials-with-production-only-access)
> 
> 翻译时间：2026-05-06 05:30
