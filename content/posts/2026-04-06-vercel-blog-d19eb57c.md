---
title: Vercel仪表板新增数据库管理功能：支持SQL查询与可视化编辑
title_original: Query and manage Marketplace databases from the dashboard - Vercel
  – Vercel
date: '2026-04-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/query-and-manage-marketplace-databases-from-the-dashboard
author: ''
summary: Vercel宣布其仪表板现已集成数据库管理功能，用户无需依赖外部工具即可直接操作受支持的市场数据库（如AWS Aurora Postgres、Neon、Prisma、Supabase等）。新功能提供三个核心模块：查询标签页允许运行任意SQL查询并导出CSV、JSON或Markdown格式结果；数据编辑器提供类电子表格界面，支持行数据的排序、复制、编辑、插入和删除；架构标签页则以可视化图形展示表结构关系。该功能目前面向拥有所有者权限的用户开放，旨在简化团队在Vercel平台内的数据库管理工作流程。
categories:
- AI基础设施
tags:
- Vercel
- 数据库管理
- PostgreSQL
- 开发者工具
- 云平台
draft: false
translated_at: '2026-04-22T05:05:34.277404'
---

![](/images/posts/7ab7cfd5227e.jpg)

![](/images/posts/1e2c80867a74.jpg)

您现在可以直接从 Vercel 仪表板运行 SQL 查询、查看和编辑数据，以及检查数据库架构。此功能适用于受支持的市场数据库集成，包括 AWS Aurora Postgres、Neon、Prisma 和 Supabase，更多服务即将推出。

团队无需依赖 `psql` 或外部数据库 UI 工具，可以直接在 Vercel 内管理数据。

受支持的 Postgres 数据库集成资源页面现在包含三个新标签页：

- **查询**：运行任何 SQL 查询、查看结果，并将其复制为 CSV、JSON 或 Markdown 格式。
- **数据编辑器**：在类似电子表格的界面中查看表数据。您可以对行进行排序、复制、编辑、插入和删除，然后以原子操作方式将更改应用到数据库。
- **架构**：在可视化图形布局中查看表和关系。

**查询**：运行任何 SQL 查询、查看结果，并将其复制为 CSV、JSON 或 Markdown 格式。

**数据编辑器**：在类似电子表格的界面中查看表数据。您可以对行进行排序、复制、编辑、插入和删除，然后以原子操作方式将更改应用到数据库。

**架构**：在可视化图形布局中查看表和关系。

此功能目前对拥有所有者权限的用户开放。您可以通过导航至仪表板中数据库页面的“浏览器”部分来管理您的数据库。

---

> 本文由AI自动翻译，原文链接：[Query and manage Marketplace databases from the dashboard - Vercel – Vercel](https://vercel.com/changelog/query-and-manage-marketplace-databases-from-the-dashboard)
> 
> 翻译时间：2026-04-22 05:05
