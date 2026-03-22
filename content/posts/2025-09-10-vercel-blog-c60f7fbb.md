---
title: MongoDB Atlas正式登陆Vercel应用市场，实现无缝集成
title_original: MongoDB Atlas is now available on the Vercel Marketplace  - Vercel
date: '2025-09-10'
source: Vercel Blog
source_url: https://vercel.com/blog/mongodb-atlas-is-now-available-on-the-vercel-marketplace
author: ''
summary: MongoDB Atlas现已正式入驻Vercel应用市场，开发者可直接在Vercel仪表板中配置完全托管的MongoDB数据库并连接到项目，无需切换平台。该集成提供一键设置、统一计费管理、自动环境变量配置等功能，支持从免费到无服务器的多种部署选项，并内置全文搜索、向量搜索等AI就绪能力。此举旨在简化开发流程，让开发者更专注于应用构建，为Vercel上的Web和AI应用提供快速、现代的数据层支持。
categories:
- AI基础设施
tags:
- MongoDB Atlas
- Vercel
- 云数据库
- 开发者工具
- AI集成
draft: false
translated_at: '2026-03-22T04:42:08.504398'
---

MongoDB Atlas 现已登陆 Vercel 应用市场。开发者现在可以直接从 Vercel 仪表板配置一个完全托管的 MongoDB 数据库，并将其连接到您的项目，无需离开平台。

为项目添加数据库通常意味着需要管理另一个账户、进行连接设置，并协调跨服务的计费。Vercel 应用市场将这些工具融入您现有的工作流程中，让您可以专注于构建而非配置。

![](/images/posts/eb31023efd40.jpg)

![](/images/posts/fbc1f40bf85e.jpg)

## 通过统一工作流程加速交付

通过 Vercel 配置 Atlas 会自动配置您项目的环境变量，并将计费集成到您的 Vercel 账户中。数据库的设置和管理由 MongoDB Atlas 处理，而您可以在 Vercel 上继续使用现有的工作流程。

其他主要优势包括：

*   **一键设置**：无需单独注册 MongoDB Atlas。如果您还没有 Atlas 账户，系统会自动创建并关联一个。
*   **集成管理**：Atlas 可通过您的 Vercel 仪表板进行管理，集成了计费和配置功能。在一个地方监控您的应用和数据库。
*   **灵活、可扩展的数据**：MongoDB Atlas 提供适用于结构化和非结构化数据的文档数据模型，以及通过副本集和分片实现的水平扩展。您可以选择免费、预配置或无服务器的部署选项。
*   **内置搜索与 AI 就绪**：Atlas 包含全文搜索、向量搜索和面向 AI 应用的语义搜索，为您的 Vercel 应用提供开箱即用的高级查询和 AI/ML 能力。
*   **高性能与安全性**：通过全球副本实现低延迟数据访问，以及加密和访问控制等内置安全功能。

此集成为 Vercel 上的 Web 和 AI 应用提供了一个快速、现代的数据层。一旦您通过应用市场配置了 Atlas，连接到数据库就变得非常简单：

```
1import { MongoClient, MongoClientOptions } from 'mongodb';2import { attachDatabasePool } from '@vercel/functions';3
4const options: MongoClientOptions = {5  appName: "devrel.vercel.integration",6  maxIdleTimeMS: 50007};8const client = new MongoClient(process.env.MONGODB_URI, options);9   1011attachDatabasePool(client);12
1314export default client; 
```

当您通过 Vercel 配置 Atlas 时，`MONGODB_URI` 环境变量会自动配置，因此您可以立即开始构建。

### 在 Vercel 上开始使用 MongoDB Atlas

MongoDB Atlas 已在 Vercel 应用市场上架，适用于所有套餐的客户。

在 Vercel 上部署 [MongoDB Atlas 论坛模板](https://vercel.com/templates/mongodb/forum)。

---

> 本文由AI自动翻译，原文链接：[MongoDB Atlas is now available on the Vercel Marketplace  - Vercel](https://vercel.com/blog/mongodb-atlas-is-now-available-on-the-vercel-marketplace)
> 
> 翻译时间：2026-03-22 04:42
