---
title: Vercel更新部署保留策略，活跃分支部署不再被自动清理
title_original: Deployment retention policies now preserve active branch deployments
  - Vercel – Vercel
date: '2026-04-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/deployment-retention-policies-now-preserve-active-branch-deployments
author: ''
summary: Vercel宣布更新其部署保留策略，现在针对存在未合并或未关闭拉取请求的活跃分支，其最新的预览部署将不再受配置的保留窗口期限制而被自动移除。这意味着用户可以设置更短的保留窗口以节省资源，同时确保重要的活跃预览部署不会丢失。该变更适用于所有套餐，并且最近的10个生产部署及所有别名部署将继续被永久保留。这项改进旨在优化开发工作流程，提升预览环境的稳定性。
categories:
- AI基础设施
tags:
- Vercel
- 部署管理
- DevOps
- 云服务
- 版本控制
draft: false
translated_at: '2026-04-18T04:42:00.355507'
---

保留策略不再删除针对存在未合并或未关闭拉取请求分支的最新预览部署。此前，若活跃分支的部署超过配置的保留窗口期，可能会被移除。

这意味着您可以安全地设置更短的保留窗口，而无需担心丢失活跃的预览部署。此项变更适用于所有套餐。

无论保留设置如何，您最近的10个生产部署以及所有已设置别名的部署将继续被保留。

了解更多关于[部署保留](Deployment Retention)的信息。

---

> 本文由AI自动翻译，原文链接：[Deployment retention policies now preserve active branch deployments - Vercel – Vercel](https://vercel.com/changelog/deployment-retention-policies-now-preserve-active-branch-deployments)
> 
> 翻译时间：2026-04-18 04:42
