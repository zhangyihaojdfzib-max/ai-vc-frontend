---
title: Native Marketplace integrations now support custom environments - Vercel
title_original: Native Marketplace integrations now support custom environments -
  Vercel
date: '2026-09-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/custom-environments-support-for-marketplace-integrations
author: ''
summary: '[翻译失败，原文如下]


  You can now connect native Marketplace resources tocustom environments. Previously,
  resource connections could only target production, pr...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T07:15:19.211941'
---

[翻译失败，原文如下]

You can now connect native Marketplace resources tocustom environments. Previously, resource connections could only target production, preview, and development environments.

Choose custom environments when connecting a resource from the Vercel dashboard, Vercel CLI, or REST API. Vercel scopes the environment variables created by the connection to the selected environments.

For example, from the CLI:

```
vercel integration add neon --environment staging
```

Existing deployments do not change. Create a new deployment after connecting a resource or changing its environment scope.

Custom environments are available on Pro and Enterprise plans.

Read thedocsfor connecting from thedashboard, theCLI--environmentflag, and theREST APIenvVarEnvironmentsfield.

## Contributors

Hedi Zandi,Dima Voytenko

---

> 本文由AI自动翻译，原文链接：[Native Marketplace integrations now support custom environments - Vercel](https://vercel.com/changelog/custom-environments-support-for-marketplace-integrations)
> 
> 翻译时间：2026-09-18 07:15
