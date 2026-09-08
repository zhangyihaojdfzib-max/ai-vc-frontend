---
title: Microfrontends previews now link across repositories - Vercel
title_original: Microfrontends previews now link across repositories - Vercel
date: '2026-08-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/microfrontends-previews-now-link-across-repositories
author: ''
summary: '[翻译失败，原文如下]


  Microfrontends can now link Preview Deployments across repositories when their Git
  branch names match exactly.


  In a monorepo, projects s...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-08T06:49:27.996244'
---

[翻译失败，原文如下]

Microfrontends can now link Preview Deployments across repositories when their Git branch names match exactly.

In a monorepo, projects share the same Git repository, commits, and branches, so Vercel can automatically link their previews. Cross-repository projects have separate commit histories and branches in separate repositories. With this update, Vercel matchesGit-connected projects by branch name and links their corresponding previews.

For example, when you preview thenew-checkoutbranch of one project, requests to other projects in the Microfrontends group will use theirnew-checkoutpreviews when available. This makes it easier to review coordinated changes across repositories in one preview experience.

This feature is enabled by default for new Microfrontends groups. You can manage it in your Microfrontends settings. Learn more abouthow deployment routing worksfor Microfrontends.

---

> 本文由AI自动翻译，原文链接：[Microfrontends previews now link across repositories - Vercel](https://vercel.com/changelog/microfrontends-previews-now-link-across-repositories)
> 
> 翻译时间：2026-09-08 06:49
