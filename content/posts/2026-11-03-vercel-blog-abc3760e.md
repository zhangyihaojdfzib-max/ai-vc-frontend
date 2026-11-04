---
title: Vercel CI no longer requires a linked Vercel project - Vercel
title_original: Vercel CI no longer requires a linked Vercel project - Vercel
date: '2026-11-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-ci-no-longer-requires-a-linked-vercel-project
author: ''
summary: '[翻译失败，原文如下]


  Vercel CI can now run on a GitHub repository that has no Vercel project. Until now
  you had to create an empty project just to connect the...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-04T08:50:42.655631'
---

[翻译失败，原文如下]

Vercel CI can now run on a GitHub repository that has no Vercel project. Until now you had to create an empty project just to connect the repository.

To enable it, you need:

- The Vercel GitHub App installed with access to the repository
- Your GitHub account connected to your Vercel account
- Write or admin permission on the repository

The Vercel GitHub App installed with access to the repository

Your GitHub account connected to your Vercel account

Write or admin permission on the repository

Then, from a clone of the repository, run:

```
1vercel ci enable
```

CI is enabled for the team your CLI is set to. Pass--scope <team>to use a different one. From the next push, tasks run as configured in your repository.

Private GitHub repositories only. Public repositories and other Git providers are not yet supported.

Read theVercel CI documentationto configure tasks.

---

> 本文由AI自动翻译，原文链接：[Vercel CI no longer requires a linked Vercel project - Vercel](https://vercel.com/changelog/vercel-ci-no-longer-requires-a-linked-vercel-project)
> 
> 翻译时间：2026-11-04 08:50
