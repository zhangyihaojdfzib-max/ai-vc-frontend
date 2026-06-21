---
title: Vercel将于2025年9月1日弃用Node.js 18
title_original: Node.js 18 is being deprecated on September 1, 2025 - Vercel
date: '2025-01-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/node-js-18-is-being-deprecated
author: ''
summary: Vercel宣布，由于Node.js 18已于2025年4月30日终止生命周期，平台将于2025年9月1日起停止对Builds和Functions中Node.js
  18的支持。现有Serverless Functions部署不受影响，但新部署将无法使用Node.js 18。用户可通过项目设置或package.json的engines字段升级Node.js版本，并可使用Vercel
  CLI命令查看受影响的项目。
categories:
- 技术趋势
tags:
- Node.js
- Vercel
- 弃用通知
- 版本升级
- Serverless
draft: false
translated_at: '2026-06-21T07:01:22.212324'
---

根据 Node.js 18 于 2025 年 4 月 30 日终止生命周期，我们将在 2025 年 9 月 1 日停止对 Builds 和 Functions 中 Node.js 18 的支持。

我现有的部署会受影响吗？

不会，现有的 Serverless Functions 部署不会受到影响。

我何时将无法再使用 Node.js 18？

2025 年 9 月 1 日，Node.js 18 将在项目设置中被禁用。当创建新部署时，使用 18 作为 Functions 版本的现有项目将显示错误。

如何升级我的 Node.js 版本？

您可以在项目设置中或通过 package.json 中的 engines 字段配置 Node.js 版本。

如何查看哪些项目受到影响？

您可以通过以下命令查看受此弃用影响的项目：

```
1npm i -g vercel@latest2vercel project ls --update-required
```

查看需要更新的项目。

---

> 本文由AI自动翻译，原文链接：[Node.js 18 is being deprecated on September 1, 2025 - Vercel](https://vercel.com/changelog/node-js-18-is-being-deprecated)
> 
> 翻译时间：2026-06-21 07:01
