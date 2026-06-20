---
title: Fern在Vercel上实现多租户文档的快速迁移与性能提升
title_original: How Fern runs multi-tenant docs for Webflow and ElevenLabs on Vercel
date: '2026-06-09'
source: Vercel Blog
source_url: https://vercel.com/blog/how-fern-runs-multi-tenant-docs-for-webflow-and-elevenlabs-on-vercel
author: ''
summary: Fern通过Vercel平台为Webflow、ElevenLabs等客户提供多租户文档服务，在单个Next.js应用中跨自定义域名运行。团队在七天内将65%的内容从Pages
  Router迁移到App Router，避免了长达数月的工程项目。迁移后，首字节时间提升3倍，页面加载时间减少80%，部署时间缩短至五分钟，每月服务超过100万独立访客和600万页面浏览量。
categories:
- 技术趋势
tags:
- Vercel
- Next.js
- 多租户
- 性能优化
- 文档管理
draft: false
translated_at: '2026-06-20T06:20:42.993543'
---

## 链接到标题Fern on Vercel

- 首字节时间提升3倍
- 页面加载时间减少80%
- 每月来自100万+独立访客的600万+页面浏览量
- 平台65%的内容在7天内从Pages Router迁移到App Router

首字节时间提升3倍

页面加载时间减少80%

每月来自100万+独立访客的600万+页面浏览量

平台65%的内容在7天内从Pages Router迁移到App Router

Fern帮助公司发布开发者文档和SDK，为Webflow、ElevenLabs等客户在Vercel上的单个Next.js应用中跨自定义域名运行客户文档。在从Pages Router向App Router迁移的过程中，团队在七天内完成了平台65%的迁移，而非启动一个长达数月的工程项目。如今Fern每天多次部署，部署时间缩短至五分钟，页面加载时间最多减少80%。

---

> 本文由AI自动翻译，原文链接：[How Fern runs multi-tenant docs for Webflow and ElevenLabs on Vercel](https://vercel.com/blog/how-fern-runs-multi-tenant-docs-for-webflow-and-elevenlabs-on-vercel)
> 
> 翻译时间：2026-06-20 06:20
