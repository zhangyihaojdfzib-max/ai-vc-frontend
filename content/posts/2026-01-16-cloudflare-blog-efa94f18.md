---
title: Astro框架正式加入Cloudflare，加速内容驱动型网站开发
title_original: Astro is joining Cloudflare
date: '2026-01-16'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/astro-joins-cloudflare/
author: ''
summary: Astro Technology Company宣布正式加入Cloudflare，标志着这款专注于构建快速、内容驱动型网站的开源网络框架进入新发展阶段。Astro将保持MIT开源许可和开放治理模式，其团队全员加入Cloudflare并继续推进框架开发。文章阐述了Astro凭借内容驱动、服务器优先、默认快速、易于使用和以开发者为中心的五项设计原则获得市场认可，其独特的岛屿架构允许在静态HTML页面中嵌入动态客户端组件。此次合作将强化Astro在内容网站领域的领先地位，Astro
  6版本即将发布，Cloudflare承诺通过生态系统基金持续支持开源贡献。
categories:
- 技术趋势
tags:
- Astro
- Cloudflare
- Web开发
- 开源框架
- 前端技术
draft: false
translated_at: '2026-01-17T04:15:56.041240'
---

# Astro 正式加入 Cloudflare

- Fred Schott
- Brendan Irvine-Broque

![Fred Schott](/images/posts/7def320d3603.jpg)

![Brendan Irvine-Broque](/images/posts/54fb95dc051a.jpg)

![](/images/posts/31a536cb911a.png)

Astro 网络框架的创建者 Astro Technology Company 正式加入 Cloudflare。

Astro 是用于构建快速、内容驱动型网站的网络框架。过去几年，我们见证了极其多样化的开发者和公司使用 Astro 进行网络开发。这涵盖了从保时捷、宜家等知名品牌，到 Opencode 和 OpenAI 等快速发展的 AI 公司。基于 Cloudflare 构建的平台，如 Webflow Cloud 和 Wix Vibe，已选择 Astro 来驱动其客户构建并部署到各自平台上的网站。在 Cloudflare，我们也使用 Astro——用于我们的开发者文档、网站、落地页等。几乎互联网上所有存在内容的地方，都能看到 Astro 的身影。

通过与 Astro 团队联手，我们将加倍努力，使 Astro 在未来多年内成为内容驱动型网站的最佳框架。Astro 的最佳版本——Astro 6——即将发布，它将带来由 Vite 驱动的全新开发服务器。Astro 6 的首个公开测试版现已发布，正式版将在未来几周内推出。

我们很高兴分享这个消息，更令人兴奋的是这对使用 Astro 进行开发的开发者意味着什么。如果您尚未尝试过 Astro——不妨一试，运行 `npm create astro@latest`。

### 这对 Astro 意味着什么

Astro 将保持开源、MIT 许可，并继续开放贡献，拥有公开的路线图和开放的治理模式。Astro Technology Company 的所有全职员工现已成为 Cloudflare 的员工，并将继续致力于 Astro 的开发。我们致力于 Astro 的长期成功，并渴望持续构建。

如果没有极其强大的开源贡献者社区，Astro 不会有今天的成就。Cloudflare 也致力于通过 Astro 生态系统基金，与包括 Webflow、Netlify、Wix、Sentry、Stainless 等在内的行业伙伴一起，继续支持开源贡献。

从一开始，Astro 就是对网络和可移植性的押注：Astro 旨在能够在任何地方运行，跨越云和平台。这一点不会改变。您可以将 Astro 部署到任何平台或云上，我们致力于为各地的 Astro 开发者提供支持。

### 市面上有许多网络框架——为什么开发者选择 Astro？

Astro 一直在快速增长：

为什么？许多网络框架试图满足所有人的所有需求，旨在同时服务于内容驱动型网站和网络应用，但它们来了又去。

Astro 成功的关键在于：它没有试图服务于所有用例，而是始终坚持五项设计原则。Astro 是……

- **内容驱动**：Astro 旨在展示您的内容。
- **服务器优先**：网站在服务器上渲染 HTML 时运行更快。
- **默认快速**：在 Astro 中构建一个缓慢的网站应该是不可能的。
- **易于使用**：您无需成为专家即可用 Astro 构建东西。
- **以开发者为中心**：您应该拥有成功所需的资源。

**内容驱动**：Astro 旨在展示您的内容。

**服务器优先**：网站在服务器上渲染 HTML 时运行更快。

**默认快速**：在 Astro 中构建一个缓慢的网站应该是不可能的。

**易于使用**：您无需成为专家即可用 Astro 构建东西。

**以开发者为中心**：您应该拥有成功所需的资源。

Astro 的**岛屿架构**是实现这一切的核心部分。每个页面的绝大部分可以是快速、静态的 HTML——默认情况下构建快速且简单，专注于渲染内容。当您需要时，您可以将页面的特定部分渲染为客户端岛屿，使用任何客户端 UI 框架。您甚至可以在同一页面上混合搭配多个框架，无论是 React.js、Vue、Svelte、Solid 还是其他任何框架：

### 重拾构建网站的乐趣

Astro 和 Cloudflare 交流得越多，我们就越清楚地发现彼此有多少共同点。Cloudflare 的使命是帮助构建一个更好的互联网——其中一部分是帮助构建一个更快的互联网。我们几乎所有人都是伴随着构建网站长大的，我们希望看到一个人们乐于在互联网上构建东西的世界，一个任何人都可以发布真正属于自己的网站的世界。

当 Astro 在 2021 年首次推出时，构建出色的网站已经变得非常痛苦——感觉像是在与构建工具和框架作斗争。说起来可能有些奇怪，在拥有编码智能体和强大 LLM（大语言模型）的 2026 年，但在 2021 年，如果不成为 JavaScript 构建工具领域的专家，就很难构建一个优秀且快速的网站。如今，情况已经大为改善，这既得益于 Astro，也得益于更广泛的前端生态系统，以至于我们今天几乎认为这是理所当然的。

Astro 项目在过去五年里一直致力于简化网络开发。因此，当 LLM（大语言模型）、氛围编码，以及如今真正的编码智能体相继出现，使得任何人都能够真正进行构建时——Astro 提供了一个默认简单快速的基础。我们都看到，当在一个结构良好的代码库上基于正确的基础进行构建时，智能体变得多么出色和快速。越来越多的构建者和平台选择 Astro 作为这个基础。

我们通过 Cloudflare 和 Astro 共同服务的平台最清楚地看到了这一点，这些平台使用 Cloudflare for Platforms 以创造性的方式将 Cloudflare 扩展到他们自己的客户，并选择 Astro 作为其客户构建的框架。

当您部署到 Webflow Cloud 时，您的 Astro 站点可以直接运行，并部署在 Cloudflare 的网络上。当您使用 Wix Vibe 开始一个新项目时，实际上您正在创建一个运行在 Cloudflare 上的 Astro 站点。当您使用 Stainless 生成一个开发者文档站点时，它会生成一个运行在 Cloudflare 上的 Astro 项目，由 Starlight（一个基于 Astro 构建的框架）驱动。

这些平台中的每一个都是为不同的受众构建的。但它们的共同点——除了使用 Cloudflare 和 Astro 之外——是它们让创建内容并将其发布到互联网变得有趣。在一个每个人都可以既是构建者又是内容创作者的世界里，我们认为还有更多的平台需要构建，更多的人需要触达。

### Astro 6 —— 由 Vite 驱动的新本地开发服务器

Astro 6 即将到来，首个公开测试版现已发布。要成为首批试用者之一，请运行：

```
npm create astro@latest -- --ref next
```

或者要升级您现有的 Astro 应用，请运行：

```
npx @astrojs/upgrade beta
```

Astro 6 带来了一个全新的开发服务器，它基于 Vite Environments API 构建，使用与您部署时相同的运行时在本地运行您的代码。这意味着，当您使用 Cloudflare Vite 插件运行 `astro dev` 时，您的代码将在 workerd（开源的 Cloudflare Workers 运行时）中运行，并且可以使用 Durable Objects、D1、KV、Agent（智能体）等。这不仅仅是 Cloudflare 的功能：任何拥有使用 Vite Environments API 插件的 JavaScript 运行时都可以从这项新支持中受益，并确保本地开发在与生产环境相同的环境和运行时 API 下运行。

Astro 中的实时内容集合在 Astro 6 中也已稳定并退出测试版。这些内容集合允许您实时更新数据，而无需重新构建您的站点。这使得引入经常变化的内容（例如商店的当前库存）变得容易，同时仍然受益于 Astro 现有对内容集合支持所带来的内置验证和缓存功能。

Astro 6 还有更多内容，包括 Astro 获得最多投票的功能请求——对内容安全策略的一流支持——以及更简单的 API、升级到 Zod 4 等。

### 加倍投入 Astro

我们非常高兴地欢迎Astro团队加入Cloudflare。我们将持续构建、持续交付，致力于让Astro成为构建内容驱动型网站的最佳选择。我们已经在思考V6版本之后的规划，并期待听到您的想法。

请关注[Astro博客](https://astro.build/blog)并加入[Astro Discord](https://astro.build/chat)，以获取最新动态。告诉我们您正在构建什么吧！


> 本文由AI自动翻译，原文链接：[Astro is joining Cloudflare](https://blog.cloudflare.com/astro-joins-cloudflare/)
> 
> 翻译时间：2026-01-17 04:15
