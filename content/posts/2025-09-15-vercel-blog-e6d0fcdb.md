---
title: Vercel更新部署保留默认策略，取消“无限制”选项
title_original: Updated defaults for deployment retention - Vercel
date: '2025-09-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/updated-defaults-for-deployment-retention
author: ''
summary: Vercel宣布自2025年10月15日起，将更新所有使用旧版“无限制”设置项目的默认部署保留策略。新策略为：已取消部署保留30天（最长1年），出错部署保留3个月（最长1年），预生产环境部署保留6个月（最长3年），生产环境部署保留1年（最长3年）。已设置自定义策略的项目不受影响，且团队所有者可为新项目配置默认策略。最近的10个生产部署及有别名的部署将永久保留。
categories:
- AI基础设施
tags:
- Vercel
- 部署管理
- 云服务
- DevOps
- 版本控制
draft: false
translated_at: '2026-03-20T04:51:14.589992'
---

自2025年10月15日起，Vercel将更新当前使用旧版“无限制”设置的所有项目的默认部署保留策略：

- 已取消的部署 - 30天，最长1年。
- 出错的部署 - 3个月，最长1年。
- 预生产环境部署 - 6个月，最长3年。
- 生产环境部署 - 1年，最长3年。

已取消的部署 - 30天，最长1年。

出错的部署 - 3个月，最长1年。

预生产环境部署 - 6个月，最长3年。

生产环境部署 - 1年，最长3年。

已设置**自定义部署保留策略**的项目将不受影响。此外，在10月15日之前，修改保留策略时“无限制”选项将不再可用。

团队所有者可以在 **团队 > 安全与隐私 > 部署保留策略** 中配置一个默认保留策略，该策略将应用于团队下创建的任何新项目。此策略也可以轻松应用于所有现有项目。

请注意，无论时间多久，您最近的10个生产环境部署以及任何当前已设置别名的部署都不会被删除。

了解更多关于**部署保留**的信息。

---

> 本文由AI自动翻译，原文链接：[Updated defaults for deployment retention - Vercel](https://vercel.com/changelog/updated-defaults-for-deployment-retention)
> 
> 翻译时间：2026-03-20 04:51
