---
title: Vercel 集成 GitHub Actions，部署数据更丰富
title_original: Trigger GitHub Actions with enriched deployment data from Vercel -
  Vercel
date: '2025-04-07'
source: Vercel Blog
source_url: https://vercel.com/changelog/trigger-github-actions-with-enriched-deployment-data-from-vercel
author: ''
summary: Vercel 宣布支持通过 `repository_dispatch` 事件在部署时触发 GitHub Actions 工作流，并携带完整的自定义
  JSON 负载，包含部署上下文和变更详情。相比此前使用的 `deployment_status` 事件，新方式减少了额外解析开销，能实现更灵活、高效的 CI 流水线和端到端测试。Vercel
  建议用户迁移至 `repository_dispatch`，同时保持对旧事件的向后兼容。
categories:
- 技术趋势
tags:
- Vercel
- GitHub Actions
- CI/CD
- 部署事件
- 工作流自动化
draft: false
translated_at: '2026-05-28T06:10:51.796639'
---

您现在可以通过 `repository_dispatch` 事件，在 Vercel 部署事件发生时触发 GitHub Actions 工作流，并携带丰富的数据。这些事件由 Vercel 发送至 GitHub，能够实现更灵活、更具成本效益的 CI 工作流，并简化 Vercel 部署的端到端测试。

此前，我们推荐使用 `deployment_status` 事件，但这些事件负载内容有限，需要额外的解析或调查才能了解具体变更内容。

借助 `repository_dispatch`，Vercel 会发送包含完整部署上下文的自定义 JSON 负载，从而帮助您减少 GitHub Actions 的开销，并优化 CI 流水线。

我们建议迁移至 `repository_dispatch` 以获得更佳体验。`deployment_status` 事件将继续保持向后兼容。

---

> 本文由AI自动翻译，原文链接：[Trigger GitHub Actions with enriched deployment data from Vercel - Vercel](https://vercel.com/changelog/trigger-github-actions-with-enriched-deployment-data-from-vercel)
> 
> 翻译时间：2026-05-28 06:10
