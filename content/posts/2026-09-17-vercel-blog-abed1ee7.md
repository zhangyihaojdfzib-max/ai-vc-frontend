---
title: Turbo build machines can now be enabled per deployment - Vercel
title_original: Turbo build machines can now be enabled per deployment - Vercel
date: '2026-09-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/turbo-build-machines-can-now-be-enabled-per-deployment
author: ''
summary: '[翻译失败，原文如下]


  You can now opt into Turbo build machines on any individual deployment. This is
  useful when you need to increase resources temporarily wi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:56:45.177146'
---

[翻译失败，原文如下]

You can now opt into Turbo build machines on any individual deployment. This is useful when you need to increase resources temporarily without changing project settings. You can do this in three ways:

1. Include#VERCEL_BUILD_MACHINE=TURBOin your Git commit message before pushing to GitHub
2. Usevc deploy --turbo(Vercel CLI 59.20.0 or later)
3. SetbuildMachinetoturbowhen creating a deployment withthe REST API

Include#VERCEL_BUILD_MACHINE=TURBOin your Git commit message before pushing to GitHub

Usevc deploy --turbo(Vercel CLI 59.20.0 or later)

SetbuildMachinetoturbowhen creating a deployment withthe REST API

Learn more in themanaging builds documentation.

Loading status…

---

> 本文由AI自动翻译，原文链接：[Turbo build machines can now be enabled per deployment - Vercel](https://vercel.com/changelog/turbo-build-machines-can-now-be-enabled-per-deployment)
> 
> 翻译时间：2026-09-18 06:56
