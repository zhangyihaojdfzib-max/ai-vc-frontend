---
title: Vercel微前端路由更新：别名与分支域名全面支持
title_original: Microfrontends routing now applies to vc alias and branch domains
  - Vercel
date: '2026-05-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/microfrontends-routing-now-applies-to-vc-alias-and-branch-domains
author: ''
summary: Vercel本周逐步推出微前端路由更新，涉及别名和分支分配域名。新版本中，使用`vc alias`创建的别名将继承源部署的完整微前端路由配置，而不再仅继承`deploymentId`。同时，分配给git分支的项目域名现在会跨所有共享该分支名称的项目路由到对应分支，而不仅限于拥有该域名的项目。用户需更新至最新版Vercel
  CLI以获取这些变更。
categories:
- AI基础设施
tags:
- Vercel
- 微前端
- 路由更新
- 别名
- 分支域名
draft: false
translated_at: '2026-05-27T06:18:42.231304'
---

本周，我们正在逐步推出对 Vercel 微前端路由的更新，涉及别名和分支分配域名。

别名继承微前端路由  
使用 `vc alias` 为微前端 URL 创建别名时，现在会保留源部署的完整微前端路由配置。此前，新别名仅继承 `deploymentId`。请更新至最新版 Vercel CLI 以获取此变更。

分支域名跨所有项目路由  
分配给 git 分支的项目域名现在会路由到微前端中所有共享该分支名称的项目中的对应分支。此前，该域名仅路由到拥有该域名的项目内的对应分支。

有关路由、别名和域名分配的详细信息，请参阅微前端文档。

---

> 本文由AI自动翻译，原文链接：[Microfrontends routing now applies to vc alias and branch domains - Vercel](https://vercel.com/changelog/microfrontends-routing-now-applies-to-vc-alias-and-branch-domains)
> 
> 翻译时间：2026-05-27 06:18
