---
title: Vercel Drop：拖拽即部署，无需Git或CLI
title_original: Introducing Vercel Drop - Vercel
date: '2026-05-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-drop
author: ''
summary: Vercel 推出 Drop 功能，用户只需将文件或文件夹拖入浏览器即可完成部署，无需使用 Git、CLI 或本地环境。该工具支持框架项目（如 Next.js）和静态站点，自动检测框架并进行构建，几秒内生成可分享的实时
  URL。每次拖放创建新项目，后续可连接 Git 仓库实现自动部署。
categories:
- AI基础设施
tags:
- Vercel
- 部署工具
- 无代码
- 静态站点
- 前端开发
draft: false
translated_at: '2026-06-12T06:54:40.073947'
---

![](/images/posts/fa2fc5dfa57c.jpg)

![](/images/posts/ca8a14be7120.jpg)

Vercel Drop 让你只需将文件或文件夹拖入浏览器即可完成部署。你无需使用 Git、Vercel CLI 或任何本地环境。

将项目拖放到 vercel.com/drop，选择团队和项目名称，然后点击部署。Vercel 会创建一个新项目，上传你的文件，并直接将其发布到生产环境，生成一个可分享的实时 URL。整个过程只需几秒钟。

Vercel Drop 不仅支持静态文件：

- 框架项目：Vercel 会检测你的框架（例如 Next.js）并进行构建。来自 Bolt.new 等工具的导出文件可通过此方式部署。
- 静态站点：无框架的文件会原样部署，无需构建步骤。这包括来自 Claude Design 和 Google Stitch 的导出文件。如果你的文件夹顶层没有 index.html，你可以选择在网站根目录加载哪个页面。

每次拖放都会创建一个新项目。如需在每次推送时自动部署，之后可将 Git 仓库连接到该项目。

请访问 vercel.com/drop 开始使用，或阅读相关文档。

---

> 本文由AI自动翻译，原文链接：[Introducing Vercel Drop - Vercel](https://vercel.com/changelog/vercel-drop)
> 
> 翻译时间：2026-06-12 06:54
