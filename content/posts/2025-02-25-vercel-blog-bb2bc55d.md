---
title: Vercel支持glob模式，精准控制分支部署
title_original: Granular branch matching for Git configuration in vercel.json - Vercel
date: '2025-02-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/granular-branch-matching-for-git-configuration-in-vercel-json
author: ''
summary: Vercel在vercel.json的git.deploymentEnabled字段中新增了glob模式支持，允许开发者使用通配符（如internal-*）一次性匹配多个分支，从而更灵活地控制哪些分支可以部署。此前只能通过显式命名单个分支来禁用部署，现在通过模式匹配可以批量管理，例如阻止所有以internal-开头的分支部署。这一更新简化了多分支项目的部署配置，提升了开发效率。
categories:
- 技术趋势
tags:
- Vercel
- Git配置
- 分支部署
- glob模式
- 前端部署
draft: false
translated_at: '2026-06-06T06:00:33.579430'
---

Vercel 现在在 `git.deploymentEnabled` 字段中支持 glob 模式（如 `testing-*`），让您对分支部署拥有更多控制权。

此前，您可以通过显式命名特定分支来禁用其部署。现在，您可以使用模式一次性匹配多个分支。

例如，以下配置会在分支名称以 `internal-` 开头时阻止其在 Vercel 上的部署。

```
1{2  "git": {3    "deploymentEnabled": {4      "internal-*": false 5    } 6  }7}
```

了解更多关于 Git 配置的信息。

---

> 本文由AI自动翻译，原文链接：[Granular branch matching for Git configuration in vercel.json - Vercel](https://vercel.com/changelog/granular-branch-matching-for-git-configuration-in-vercel-json)
> 
> 翻译时间：2026-06-06 06:00
