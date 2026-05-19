---
title: Vercel 现可禁用 GitHub 部署状态事件
title_original: Optionally disable deployment_status webhook events for GitHub Actions
  - Vercel
date: '2025-05-01'
source: Vercel Blog
source_url: https://vercel.com/changelog/optionally-disable-deployment_status-webhook-events-for-github-actions
author: ''
summary: Vercel 新增功能，允许用户禁用向 GitHub 发送的 deployment_status webhook 事件，以减少大型仓库（尤其是单体仓库）中因频繁部署产生的嘈杂事件日志。禁用后，GitHub
  PR 事件历史将更清晰，但预览部署链接的评论功能不受影响。Vercel 建议用户迁移至 repository_dispatch 事件以获取更丰富的部署信息。
categories:
- 技术趋势
tags:
- Vercel
- GitHub Actions
- Webhook
- 部署管理
- 单体仓库
draft: false
translated_at: '2026-05-19T06:14:15.967892'
---

![](/images/posts/f8b664782937.jpg)

![](/images/posts/01561bd5fc5b.jpg)

你现在可以禁用 Vercel 连接到 GitHub 仓库时向 GitHub 发送的 `deployment_status` webhook 事件。

当 `deployment_status` 事件启用时，GitHub 的拉取请求活动会为每次部署创建一个包含状态事件的日志。虽然这可以让你的团队更好地了解情况，但对于拥有大量部署事件的仓库（尤其是包含多个项目的单体仓库）来说，也会产生嘈杂的事件日志。

![](/images/posts/05a3405d69b9.jpg)

![](/images/posts/806dd9441cca.jpg)

禁用这些事件可以防止重复消息扰乱你的 GitHub PR 事件历史，让你更清晰、更专注地查看拉取请求活动。Vercel 在 GitHub 评论中包含预览部署链接的功能将继续像以前一样发布。

![](/images/posts/3ffa86958e80.jpg)

![](/images/posts/22907afaee54.jpg)

`deployment_status` 事件最常被用作 GitHub Actions 的触发器。我们建议迁移到 `repository_dispatch` 事件，以简化工作流并获取更丰富的 Vercel 部署信息。

更多信息请参阅文档。

---

> 本文由AI自动翻译，原文链接：[Optionally disable deployment_status webhook events for GitHub Actions - Vercel](https://vercel.com/changelog/optionally-disable-deployment_status-webhook-events-for-github-actions)
> 
> 翻译时间：2026-05-19 06:14
