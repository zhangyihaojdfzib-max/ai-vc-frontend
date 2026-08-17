---
title: Vercel Connect 新增可观测性支持
title_original: Vercel Connect adds observability support - Vercel
date: '2026-08-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-connect-adds-observability-support
author: ''
summary: Vercel Connect 推出可观测性功能，为团队提供令牌生命周期的行级可见性，包括查看令牌创建者、使用应用、使用时间及有效性。新增的“可观测性”标签页包含运行时事件、关联ID和活动筛选功能，支持按类型筛选令牌请求、授权、刷新等事件。该功能适用于所有套餐，事件保留时间因套餐而异，Pro和Enterprise可添加Drain延长保留。此更新旨在提升连接器的透明度和调试效率。
categories:
- AI基础设施
tags:
- Vercel Connect
- 可观测性
- 令牌管理
- 开发者工具
- 云基础设施
draft: false
translated_at: '2026-08-17T02:58:19.413456'
---

![](/images/posts/1ed007bb8ddd.jpg)

Vercel Connect 现在为团队提供令牌生命周期的行级可见性。您可以查看谁创建了令牌、哪个应用或项目使用了它、使用时间以及它是否仍然有效。

每个连接器的详情页面都包含一个新的“可观测性”标签页：

- **运行时事件**：每个令牌请求、授权、刷新、撤销和触发器投递，均可按类型筛选。
- **关联 ID**：稳定的 `tokenId` 和 `authorizationId` 值将每个令牌的事件关联起来，因此您可以将 Connect 事件与您自己的系统进行匹配。
- **活动**：“活动筛选”按钮会打开活动页面，并预先筛选出该连接器的配置事件，以便您查看其变更时间和方式。

运行时事件：每个令牌请求、授权、刷新、撤销和触发器投递，均可按类型筛选。

关联 ID：稳定的 `tokenId` 和 `authorizationId` 值将每个令牌的事件关联起来，因此您可以将 Connect 事件与您自己的系统进行匹配。

活动：“活动筛选”按钮会打开活动页面，并预先筛选出该连接器的配置事件，以便您查看其变更时间和方式。

Connect 可观测性在所有套餐中均可用。事件保留时间：Hobby 套餐为 12 小时，Pro 套餐为 3 天，Enterprise 套餐为 30 天。如需更长时间保留事件，可在 Pro 和 Enterprise 套餐中添加 Drain，将事件转发到自定义 webhook 端点。Enterprise 团队还可使用基于角色的访问控制和审计日志。

请在连接器的“可观测性”标签页中开始使用，或阅读文档。

Vercel Connect 目前处于测试阶段，适用于所有套餐。在正式发布之前，功能和行为（包括可用的连接器和触发器转发）可能会发生变化。使用需遵守 Beta 协议和 Vercel Connect 条款。

## 贡献者

Hedi Zandi、Dima Voytenko、Ben Sabic

---

> 本文由AI自动翻译，原文链接：[Vercel Connect adds observability support - Vercel](https://vercel.com/changelog/vercel-connect-adds-observability-support)
> 
> 翻译时间：2026-08-17 02:58
