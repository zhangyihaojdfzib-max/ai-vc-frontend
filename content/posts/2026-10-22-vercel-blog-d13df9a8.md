---
title: Deploy without an account using Vercel CLI - Vercel
title_original: Deploy without an account using Vercel CLI - Vercel
date: '2026-10-22'
source: Vercel Blog
source_url: https://vercel.com/changelog/deploy-without-an-account-using-vercel-cli
author: ''
summary: '[翻译失败，原文如下]


  You can now deploy apps to Vercel without an account usingVercel CLI. Share prototypes
  faster with a live URL before signing in to claim ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-25T07:27:16.296377'
---

[翻译失败，原文如下]

You can now deploy apps to Vercel without an account usingVercel CLI. Share prototypes faster with a live URL before signing in to claim your project.

From a project directory that isn't linked to Vercel, run:

```
vercel deploy --temporary
vercel deploy --temporary prototype.html
```

Deploying a project or single file without a Vercel account

The CLI builds your project locally when needed and returns a deployment URL you can share.

Temporary deployments use the dedicatedtmp.nowdomain, separate fromvercel.app, and expire after one hour unless claimed.

To keep your project live, open the claim link in the CLI output and sign in or create an account. Keep this link private.

Read theVercel CLI documentationto get started.

---

> 本文由AI自动翻译，原文链接：[Deploy without an account using Vercel CLI - Vercel](https://vercel.com/changelog/deploy-without-an-account-using-vercel-cli)
> 
> 翻译时间：2026-10-25 07:27
