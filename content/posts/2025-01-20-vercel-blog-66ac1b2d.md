---
title: Vercel推出Claim Deployments，实现快速安全部署转移
title_original: Claim Deployments now available for fast and secure deployment transfers
  - Vercel
date: '2025-01-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/claim-deployments
author: ''
summary: Vercel宣布推出Claim Deployments功能，允许多租户平台（如AI Agent和可视化构建应用）将部署所有权直接转移给用户或团队。该流程通过Vercel
  CLI或API创建部署，生成claim-deployment URL，用户确认团队后即可完成转移。这一更新简化了部署管理，提升了安全性和效率，尤其适用于需要跨用户或团队协作的场景。
categories:
- AI基础设施
tags:
- Vercel
- 部署转移
- 多租户平台
- API
- AI基础设施
draft: false
translated_at: '2026-06-21T07:01:22.873238'
---

![Claim Deployment - Dark](/images/posts/3175dd3b2e2f.jpg)

![Claim Deployment - Dark](/images/posts/267b372d1779.jpg)

多租户平台（如AI Agent（智能体）和可视化构建应用）现在可以轻松地将部署所有权直接转移给用户或团队。

工作原理如下：

- 创建部署：任何第三方均可通过Vercel CLI或Vercel API（POST /files和POST /deployments）创建新部署。
- 发起转移：随后使用Vercel API端点生成该部署的claim-deployment URL。
- 用户确认团队：用户选择其Vercel团队并完成转移。

创建部署：任何第三方均可通过Vercel CLI或Vercel API（POST /files和POST /deployments）创建新部署。

发起转移：随后使用Vercel API端点生成该部署的claim-deployment URL。

用户确认团队：用户选择其Vercel团队并完成转移。

查阅我们的文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Claim Deployments now available for fast and secure deployment transfers - Vercel](https://vercel.com/changelog/claim-deployments)
> 
> 翻译时间：2026-06-21 07:01
