---
title: Vercel GitHub应用新增Actions与Workflows权限
title_original: New GitHub App permissions for Actions and Workflows - Vercel – Vercel
date: '2026-03-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-github-app-updated-permissions
author: ''
summary: Vercel GitHub应用更新，新增两项仓库权限：Actions（读取）和Workflows（读取与写入）。这些权限使Vercel Agent能读取工作流运行日志以诊断CI失败，并代表用户配置CI工作流文件。同时，v0工具可创建包含CI/CD管道的完整生产仓库。用户需在GitHub设置中接受更新权限以使用新功能。
categories:
- AI产品
tags:
- Vercel
- GitHub应用
- CI/CD
- 权限更新
- 工作流
draft: false
translated_at: '2026-04-29T05:27:43.736104'
---

Vercel GitHub 应用现在在安装时会请求两项额外的仓库权限：Actions（读取）和 Workflows（读取与写入）。

这些权限使 Vercel Agent（智能体）能够读取工作流运行日志，以帮助诊断 CI 失败，并代表您配置 CI 工作流文件。这也使得 v0 能够创建包含已配置 CI/CD 管道的完整、可用于生产环境的仓库。要使用这些功能，请在您的 GitHub 组织或账户设置中接受更新后的权限。

有关 Vercel GitHub 应用请求的所有权限的完整详情，请参阅文档。

---

> 本文由AI自动翻译，原文链接：[New GitHub App permissions for Actions and Workflows - Vercel – Vercel](https://vercel.com/changelog/vercel-github-app-updated-permissions)
> 
> 翻译时间：2026-04-29 05:27
