---
title: Vercel容器仓库现已支持公开访问
title_original: Vercel Container Registry repositories can now be made public - Vercel
date: '2026-08-07'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-container-registry-repositories-can-now-be-made-public
author: ''
summary: Vercel宣布其容器注册表仓库现可设为公开，任何拥有Vercel账户的用户均可拉取镜像，但仅限只读操作，无法修改或删除。此前共享功能仅限最多100个团队，现在公开访问面向所有团队开放。用户可通过仪表盘、CLI或REST
  API设置仓库可见性，默认保持私有。公开镜像可用于Vercel Sandbox，支持团队级镜像引用。此举简化了镜像分发流程，提升了协作效率。
categories:
- 技术趋势
tags:
- Vercel
- 容器注册表
- 公开访问
- 镜像共享
- 开发者工具
draft: false
translated_at: '2026-08-11T03:56:27.327247'
---

Vercel 容器注册表现在允许你将仓库设为公开，这样任何拥有 Vercel 账户的人都可以拉取并使用其中的镜像。

共享功能此前已支持向最多 100 个团队授予读取权限，而将仓库设为公开后，访问权限将开放给所有 Vercel 团队，而非仅限于指定的团队列表。公开访问为只读模式，因此任何人都可以拉取和使用镜像，但无法推送、删除或以其他方式修改仓库。仓库默认保持私有。

你可以通过项目仪表盘中的 镜像 → 仓库 → 设置 → 公开访问 路径将仓库设为公开，确认时需要输入仓库名称。你也可以通过 Vercel CLI 设置可见性：

```
1vercel vcr config <repository> --public true2vercel vcr config <repository> --public false
```

公开镜像的使用方式与 Vercel Sandbox 中的共享镜像相同，后者接受在 `Sandbox.create()` 中传入团队级镜像引用：

```
1import { Sandbox } from '@vercel/sandbox';2const sandbox = await Sandbox.create({3  image: 'their-team/their-project/their-repository:latest',4});
```

你可以通过仪表盘、CLI 或 REST API 更新仓库可见性，并参阅 Vercel 容器注册表文档了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Container Registry repositories can now be made public - Vercel](https://vercel.com/changelog/vercel-container-registry-repositories-can-now-be-made-public)
> 
> 翻译时间：2026-08-11 03:56
