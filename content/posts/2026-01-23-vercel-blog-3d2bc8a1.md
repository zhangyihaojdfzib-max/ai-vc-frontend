---
title: Vercel优化函数缓存，部署速度提升高达5秒
title_original: Faster deploys with improved function caching - Vercel
date: '2026-01-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/faster-deploys-with-improved-function-caching
author: ''
summary: Vercel通过改进函数缓存机制，显著提升了部署速度。新方案将部署特定的环境变量（如VERCEL_DEPLOYMENT_ID）从函数载荷移至运行时注入，使得当代码未变更时，系统能够识别并跳过冗余的函数上传过程。这一优化平均可减少构建时间400-600毫秒，在大型构建中最多可节省5秒。该功能目前自动适用于无框架的Vercel
  Functions以及使用Python、Go、Ruby和Rust的项目，Next.js项目也将很快获得支持，且无需任何配置即可生效。
categories:
- AI基础设施
tags:
- Vercel
- 部署优化
- 函数计算
- 云原生
- 开发工具
draft: false
translated_at: '2026-01-24T04:30:43.447566'
---

当代码未发生更改时，函数上传现将被跳过，平均可减少构建时间400-600毫秒，对于大型构建最多可节省5秒。

此前，诸如`VERCEL_DEPLOYMENT_ID`这类部署特定的环境变量被包含在函数载荷中，导致即使代码完全相同，每次部署也被视为唯一。现在这些变量在运行时注入，使得Vercel能够识别未变更的函数并跳过冗余上传。

此项优化适用于不使用框架的`Vercel Functions`，以及使用Python、Go、Ruby和Rust的项目。Next.js项目也将很快获得同样的改进。

该优化会自动应用于所有部署，无需任何配置。

在我们的文档中了解更多关于`functions`和`builds`的信息。

---

> 本文由AI自动翻译，原文链接：[Faster deploys with improved function caching - Vercel](https://vercel.com/changelog/faster-deploys-with-improved-function-caching)
> 
> 翻译时间：2026-01-24 04:30
