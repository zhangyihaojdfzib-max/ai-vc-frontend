---
title: Vercel微前端支持进入公开测试，助力大型应用拆分与并行开发
title_original: Microfrontends support is now in Public Beta - Vercel
date: '2025-08-06'
source: Vercel Blog
source_url: https://vercel.com/changelog/microfrontends-support-is-now-in-public-beta
author: ''
summary: Vercel宣布其微前端支持功能现已进入公开测试阶段。该功能允许开发团队将大型单体应用拆分为多个独立的小型应用，从而实现并行构建、测试与部署，显著缩短构建时间并提升开发效率。通过Vercel平台，这些独立应用可被自动组装并路由为统一的用户体验，同时支持预获取与预渲染机制以实现应用间的快速导航。文章提供了从创建微前端群组、添加专用包到配置路由文件的快速入门指南，适用于希望实现渐进式迁移或提升大型应用开发流程的团队。
categories:
- AI基础设施
tags:
- 微前端
- Vercel
- 前端架构
- 开发工具
- 应用部署
draft: false
translated_at: '2026-04-09T04:38:32.664537'
---

微前端支持现已进入公开测试阶段。微前端允许您将大型应用程序拆分为多个小型应用，使开发团队能够更快速地推进工作。

这项功能支持团队和大型应用独立构建与测试，同时由Vercel将这些应用组装并路由为统一的用户体验。这能有效缩短构建时间，支持并行开发，并实现渐进式的遗留系统迁移。

开发者可使用Vercel工具栏独立迭代和测试应用，而微前端间的导航将受益于预获取与预渲染机制，实现应用间的快速切换。

要开始使用微前端，请克隆我们的示例项目或按照快速入门指南操作：

1. 在Vercel控制面板中，进入设置页面的微前端标签页
2. 创建包含所有微前端项目的微前端群组
3. 为每个微前端应用添加@vercel/microfrontends包
4. 在主应用中添加microfrontends.json配置文件，在预览环境测试后即可部署至生产环境

在Vercel控制面板中，进入设置页面的微前端标签页

创建包含所有微前端项目的微前端群组

为每个微前端应用添加@vercel/microfrontends包

在主应用中添加microfrontends.json配置文件，在预览环境测试后即可部署至生产环境

```
1{2  "dashboard": {},3  "docs": {4    "routing": [{5      "paths": ["/docs", "/docs/:path*"]6    }]7  }],8  "marketing": {9    "routing": [{10      "paths": ["/home", "/pricing"]11    }]12  }13}
```

微前端配置文件将路由路径指向三个不同应用

如需了解更多微前端相关信息，请查阅我们的文档，或直接联系Vercel及您的客户团队。

---

> 本文由AI自动翻译，原文链接：[Microfrontends support is now in Public Beta - Vercel](https://vercel.com/changelog/microfrontends-support-is-now-in-public-beta)
> 
> 翻译时间：2026-04-09 04:38
