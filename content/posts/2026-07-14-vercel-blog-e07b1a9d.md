---
title: Vercel将于2026年10月弃用Node.js 20
title_original: Node.js 20 is being deprecated on October 1, 2026 - Vercel
date: '2026-07-14'
source: Vercel Blog
source_url: https://vercel.com/changelog/node-js-20-is-being-deprecated
author: ''
summary: Vercel宣布将于2026年10月1日弃用Node.js 20，原因是Node.js 20已于2026年4月30日终止生命周期。现有部署不受影响，但新部署将无法使用该版本。用户可通过命令行检查受影响项目，并建议升级至Node.js
  24。若无法及时升级，可使用容器镜像部署以规避弃用限制。文章提供了升级步骤和容器化方案。
categories:
- 技术趋势
tags:
- Node.js
- Vercel
- 版本弃用
- 技术升级
- 容器化部署
draft: false
translated_at: '2026-07-15T04:54:28.154829'
---

根据 Node.js 20 于 2026 年 4 月 30 日终止生命周期，我们将在 2026 年 10 月 1 日弃用用于构建和函数的 Node.js 20。

如何查看哪些项目受到影响？

您可以通过以下方式查看受此弃用影响的项目：

```
npm i -g vercel@latest
vercel project ls --update-required
```

列出仍使用已弃用 Node.js 版本的项目。

现有部署会受影响吗？

不会，现有包含无服务器函数的部署不会受到影响。已部署函数的调用将继续正常运行。只有新部署会受到影响。

何时将无法再使用 Node.js 20？

2026 年 10 月 1 日，Node.js 20 将在项目设置中被禁用。使用 Node.js 20 作为函数版本的现有项目在创建新部署时将显示错误。

如何升级 Node.js 版本？

您可以在项目设置中或通过 `package.json` 中的 `engines` 字段配置 Node.js 版本。

您也可以将升级任务交给您的编码 Agent（智能体）：

```
将此 Vercel 项目从 Node.js 20 升级到 24。在 package.json 中设置 engines 字段为 { "node": "24.x" }，该设置将在下次部署时覆盖项目设置中的版本。更新 .nvmrc、.node-version 或 CI 配置中的 Node 20 固定版本。将本地运行时切换到 Node 24，重新安装依赖，运行构建和测试，并修复任何破坏性变更。部署后，通过记录 process.version 确认版本。
```

交给您的编码 Agent（智能体）为您处理项目升级。

如果在 10 月 1 日前无法完成升级怎么办？

如果您无法在不中断应用的情况下及时完成升级，可以将其部署为容器镜像。在项目根目录添加 `Dockerfile.vercel`，镜像将在每次提交时构建并部署：

```
1FROM node:20-alpine
2WORKDIR /app
3COPY . .
4RUN npm ci
5
6CMD ["node", "server.js"]
```

将 Node.js 20 固定为基础镜像。项目设置中的 Node.js 版本不适用于容器，因此弃用不会阻止这些部署。

我们仍建议您在条件允许时进行升级。使用容器时，您需要自行管理 Node.js 版本及其安全更新。

请在 2026 年 10 月 1 日前升级。了解更多关于受支持的 Node.js 版本的信息。

---

> 本文由AI自动翻译，原文链接：[Node.js 20 is being deprecated on October 1, 2026 - Vercel](https://vercel.com/changelog/node-js-20-is-being-deprecated)
> 
> 翻译时间：2026-07-15 04:54
