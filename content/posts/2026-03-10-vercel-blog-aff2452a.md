---
title: Vercel如何将CDN部署在Discourse前端
title_original: How we run Vercel's CDN in front of Discourse - Vercel
date: '2026-03-10'
source: Vercel Blog
source_url: https://vercel.com/blog/how-we-run-vercels-cdn-in-front-of-discourse
author: ''
summary: 本文介绍了Vercel如何利用其CDN为外部托管的应用（如Discourse）提供代理服务，实现防火墙保护、DDoS缓解和可观测性，而无需迁移整个应用。文章详细说明了通过Vercel的CDN设置、微前端技术将Next.js应用与Discourse整合在同一域名下的方法，以及如何通过路由重写和微前端配置实现灵活的功能扩展和安全防护。
categories:
- AI基础设施
tags:
- CDN
- Vercel
- 微前端
- Discourse
- Next.js
draft: false
translated_at: '2026-03-14T04:51:23.222608'
---

Vercel的CDN可以为任何应用提供前端服务，而不仅仅是那些原生部署在该平台上的应用，且设置简单。这使您能为Discourse或WordPress等平台添加防火墙保护、DDoS缓解和可观测性，而无需完全迁移它们。

**Vercel社区**就是这种架构的一个例子。它是一个托管在其他地方的Discourse应用，但我们通过Vercel的CDN自行代理它，这既保护了应用，又让我们能够使用Vercel网站技术栈中的有用功能：

- **网站分析**为我们提供匿名的、无需Cookie的人口统计数据和来源数据，因此我们可以看到用户来自哪里以及他们在寻找什么。
- **防火墙**为我们提供DDoS保护，并在去年自动阻止了多次攻击。
- **机器人管理**让我们能够阻止恶意爬虫，同时允许受信任的爬虫索引论坛，并使社区帖子能够出现在ChatGPT的搜索结果中。

社区平台的某些部分，例如**Vercel社区直播会话**，是直接使用Next.js在Vercel上运行的。我们使用**Vercel微前端**将Next.js应用挂载到与Discourse应用相同的域名下，原因有三：

- 创建那些作为CMS插件实现起来不切实际的新页面。
- 覆盖我们无法完全自定义的现有Discourse页面。
- 通过**使用Vercel登录**来保持用户身份验证。

当新页面准备就绪可以发布时，我们将其路径添加到微前端配置中，用户将在下一次部署时被无缝重定向。

![](/images/posts/7fdb09b3a1dc.jpg)

![](/images/posts/9658a7daa18c.jpg)

![](/images/posts/7590dab893fc.jpg)

![](/images/posts/d0bb9a8b2fb6.jpg)

## 将Vercel用作CDN

要像这样将Vercel设置为CDN代理，您需要两个域名：

1.  **内部主机**：网站实际托管的源服务器。可能类似于 `your-site.discourse.com`。
2.  **外部主机**：用户与之交互的Vercel项目域名，例如 `community.vercel.com`。

确保网站上的所有链接及其规范URL都使用外部域名。

一旦这些设置完成，在Vercel上创建一个新项目，并将其部署到外部主机。然后，您可以使用 `vercel.ts`（原 `vercel.json`）将流量重写到内部域名。

```
1import { type VercelConfig, routes, deploymentEnv } from '@vercel/config/v1'2
3export const config: VercelConfig = {4  rewrites: [5    routes.rewrite('/(.*)', deploymentEnv('INNER_HOST'), {6      requestHeaders: {7        'x-proxy-secret': deploymentEnv('PROXY_HEADER')8      }9    }),10  ],11}
```

内部主机会读取 `x-proxy-secret` 请求头来验证流量，确保没有任何东西可以直接访问内部主机。

## 使用微前端在单个域名上运行多个应用

为了突破Discourse的限制来扩展社区论坛，我们使用**垂直微前端**方法配置了外部主机域名。

Vercel的微前端允许您将不同的Vercel项目挂载到不同的路由路径。我们添加了一个 `microfrontends.json` 文件，将特定路由的流量定向到单独的Vercel项目。

可以按路由逐步添加更多页面。我们还添加了 `.well-known/workflow` 路由，以便使用**工作流开发套件**进行事件创建和视频处理。

```
1{2  "$schema": "https://openapi.vercel.sh/microfrontends.json",3  "applications": {4    "community-proxy": {5      "development": {6        "fallback": "community.vercel.com"7      }8    },9    "community-nextjs": {10      "routing": [11        {12          "paths": [13            "/.well-known/workflow/:path*",14            "/live/:path*"15          ]16        }17      ]18    }19  }20}
```

虽然您可以通过在代理正则表达式中使用反向匹配来避免代理某些路由，从而完成其中部分工作，但拆分项目能提供更好的隔离性。这种方法允许独立的环境变量和组织权限，从而锁定与第三方主机通信的项目。

## 无需大规模迁移的现代化CDN

至此，Vercel的CDN已位于您的用户和源服务器之间。所有流量都流经Vercel的全球网络，让您在无需触及现有应用的情况下获得企业级安全性。

当您将此与微前端结合使用时，您将获得更大的灵活性。您现在拥有了一条逐步实现应用现代化的路径。您无需进行"大爆炸"式的重构，而是可以创建一个Next.js应用，并逐一开启特定路由，同时您的核心应用继续在Discourse、WordPress或任何其他构建平台上运行。

这种架构开启了一条务实的道路：今天使用Vercel的CDN保护您现有的投资，明天再在此基础上叠加现代功能，所有这些都无需承担完整平台迁移的风险。

通过阅读**Vercel微前端文档**了解更多信息，或访问 `community.vercel.com/live` 查看实际效果。

---

> 本文由AI自动翻译，原文链接：[How we run Vercel's CDN in front of Discourse - Vercel](https://vercel.com/blog/how-we-run-vercels-cdn-in-front-of-discourse)
> 
> 翻译时间：2026-03-14 04:51
