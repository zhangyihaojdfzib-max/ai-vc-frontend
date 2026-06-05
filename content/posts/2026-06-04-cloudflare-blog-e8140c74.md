---
title: VoidZero加入Cloudflare，Vite生态获百万美元基金支持
title_original: VoidZero is joining Cloudflare
date: '2026-06-04'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/voidzero-joins-cloudflare/
author: ''
summary: VoidZero（Vite、Vitest、Rolldown、Oxc等开源工具背后的公司）正式加入Cloudflare，所有团队成员也将加入。Cloudflare承诺保持这些项目的开源、供应商中立和社区驱动特性，并投入工程资源支持其发展。同时，Cloudflare宣布设立100万美元的Vite生态系统基金，由Vite核心团队管理，用于支持维护者和贡献者。此举旨在巩固Vite作为JavaScript生态系统共享基础的地位。
categories:
- 技术趋势
tags:
- Vite
- Cloudflare
- 开源
- JavaScript生态
- 开发者工具
draft: false
translated_at: '2026-06-05T06:22:20.161431'
---

# VoidZero 加入 Cloudflare

2026-06-04

- 尤雨溪
- Steve Faulkner

![](/images/posts/182cd8c261ba.png)

VoidZero，即 Vite、Vitest、Rolldown、Oxc 和 Vite+ 背后的公司，正式加入 Cloudflare。作为此次变更的一部分，VoidZero 的所有团队成员也将加入 Cloudflare。

在说其他事情之前，我们首先要明确最重要的一点：Vite、Vitest、Rolldown、Oxc 和 Vite+ 将继续保持开源、供应商无关和社区驱动。这一点不会改变。

Cloudflare 的使命是帮助构建更美好的互联网。而更美好的互联网是一个开放的互联网。开发者需要选择，框架需要中立的基础，应用程序需要可移植。期望整个 Web 生态系统围绕单一供应商构建是不合理的。最重要的工具和框架在设计上就应该是可移植的。

Vite 是整个 JavaScript 生态系统都认同的少数基础工具之一。它凭借快速、卓越、可移植和供应商中立的特点赢得了这一地位。Cloudflare 帮助构建更美好互联网的最佳方式之一，就是投资于这一基础性的开源工具链。一个能让互联网对所有人（而不仅仅是使用 Cloudflare 或选择在我们这里托管的用户）都变得更好的工具链。

在过去几年中，我们投入了大量资源，使 Cloudflare 成为在开发者平台上构建和运行网站、应用程序和 Agent（智能体）的最佳场所。但最终，这个选择始终在您手中。您可以在任何地方运行您的 Vite 应用程序。

### 这对 Vite 意味着什么

今天的消息为 Vite 提供了更多资源以持续发展，而成就 Vite 的那些特质将保持不变：

- Vite 保持 MIT 许可并开源。
- Vite 保持供应商无关。使用 Vite 构建的应用程序可以在任何地方运行，并且将继续如此。
- Vite 的路线图继续由更广泛的 Vite 团队和社区驱动，并继续在开放环境中开发。
- 尤雨溪和 VoidZero 团队的其他成员继续领导 Vite、Vitest、Rolldown、Oxc 和 Vite+。
- Cloudflare 正在为这些项目投入工程和资源，而非将其转移。

Vite 保持 MIT 许可并开源。

Vite 保持供应商无关。使用 Vite 构建的应用程序可以在任何地方运行，并且将继续如此。

Vite 的路线图继续由更广泛的 Vite 团队和社区驱动，并继续在开放环境中开发。

尤雨溪和 VoidZero 团队的其他成员继续领导 Vite、Vitest、Rolldown、Oxc 和 Vite+。

Cloudflare 正在为这些项目投入工程和资源，而非将其转移。

今年早些时候 Astro 加入 Cloudflare 时，我们做出了同样的承诺。Astro 仍然是开源的，并且仍然可以部署到任何地方。该团队仍在推进他们原本就在推进的路线图。

这一承诺对 Vite 更为重要，因为 Vite 不仅仅是一个框架。Vite 是众多框架的基础：Vue、SvelteKit、Nuxt、Astro、Solid、Qwik、Angular、React Router、TanStack Start。甚至 Next.js 现在也在 vinext 中有了基于 Vite 的实现。Vite 已成为 JavaScript 生态系统的共享基础。

我们的首要目标是维护让 Vite 获得如此广泛采用的信任。不是通过我们在这里的言辞，而是通过每天在支持和开发这些项目中的实际行动来证明。

在支持开源和共享生态系统基础方面，我们也希望言行一致。作为此次公告的一部分，Cloudflare 承诺向一个 Vite 生态系统基金投入 100 万美元，以支持维护者和贡献者，该基金由 Vite 核心团队管理。Vite 比 VoidZero 或 Cloudflare 更宏大，那些帮助构建它的人应该成为未来的一部分。

### Vite 作为基础

Vite 和 Cloudflare 团队在此公告之前就已开始合作，始于 2024 年的 Vite Environment API。Environment API 允许 Vite 在开发期间在 Node.js 之外的环境中运行服务器代码。我们与 Vite 团队密切合作设计了该 API，然后在此基础上构建了 Cloudflare Vite 插件。

当您使用 Cloudflare 插件运行 `vite dev` 时，您的服务器代码在 workerd 中运行，这是与生产环境中驱动 Workers 相同的开源运行时。Durable Objects、D1、KV、R2、Workflows、Workers AI、Agent（智能体）、Service Bindings、Workers RPC——所有这些都在与生产环境相同的运行时模型中本地运行。

长期以来，在非 Node 运行时上开发的代价是本地开发感觉像是生产环境的劣化版本。Environment API 消除了这一代价，而无需强迫任何人采用 Cloudflare 特定的开发服务器。任何想要接入 Vite 的运行时都可以做同样的事情。这种设计——Vite 中的通用机制配合特定供应商的实现——已被证明行之有效，也是我们希望继续发展的方向。

当我们看到 Cloudflare Vite 插件的采用率飙升时，我们就知道我们做对了：

Vite 的采用曲线目前是生态系统中值得关注的最显著现象之一。截至本文撰写时，Vite 的周下载量约为 1.29 亿次。Cloudflare Vite 插件（@cloudflare/vite-plugin）的周下载量接近 1400 万次。

如果一年前有人告诉我们，Cloudflare Vite 插件的下载量将达到 Vite 本身的 10% 以上，我们不会相信。发生了什么？AI 发生了。正在创建的软件比以往任何时候都多，其中很多始于 AI 生成的代码。这些应用程序需要一个默认的技术栈和一个运行场所。Agent（智能体）编写的应用程序正在选择 Vite，并且越来越多地选择在 Cloudflare 上运行的 Vite。

### AI 正在改变我们编写软件的方式

过去，开发者是开发服务器、打包工具、代码检查工具、格式化工具和 CLI 的唯一用户。这已不再成立：Agent（智能体）也在持续使用它们。它们搭建项目、运行开发服务器、读取错误、编写测试、检查并格式化代码、部署预览并进行迭代。

许多 AI 生成的应用程序已经以 Vite 应用起步，因为 Vite 快速、易于理解，并且与 Agent（智能体）在其训练数据中看到的内容广泛兼容。快速反馈循环一直很重要。当使用 Agent（智能体）编写软件时，这变得更加关键：

- 快速构建，因为它们比人类迭代更多。
- 快速测试，因为它们不断重新运行测试套件以验证自己的工作。
- 快速的代码检查和格式化，因为这些工具成为护栏。
- 清晰、结构化的错误信息，因为 Agent（智能体）需要读取并据此采取行动。
- 一致的 CLI，因为小的不一致会导致大的弯路。

快速构建，因为它们比人类迭代更多。

快速测试，因为它们不断重新运行测试套件以验证自己的工作。

快速的代码检查和格式化，因为这些工具成为护栏。

清晰、结构化的错误信息，因为 Agent（智能体）需要读取并据此采取行动。

一致的 CLI，因为小的不一致会导致大的弯路。

整个 VoidZero 工具链就是为此类循环而构建的。Vitest、Rolldown、Oxc、Oxlint 和 Oxfmt 各自都是其类别中最快的工具之一，并且当被 Agent（智能体）反复运行时也能良好工作。Vite+ 将这些组件整合到一个工具链中，拥有一个 CLI、一个配置模型和更少的活动部件。这使得开发循环对人类来说更容易理解，对 Agent（智能体）来说更易于可靠驱动。

我们自己在实践这一点。Cloudflare 仪表盘构建在 Vite 之上。Oxlint 已经为 Cloudflare 代码库节省了数天的工程时间。来自 Astro 团队的 Agent（智能体）框架 Flue 也正在迁移到 Vite 作为其基础。Flue 可以在 Node.js、Cloudflare Workers、GitHub Actions、GitLab CI/CD 等环境中运行 Agent（智能体），并且 Cloudflare 目标现在使用官方的 Cloudflare Vite 插件和 workerd 集成。Vite 正在成为 Cloudflare 内部的默认应用程序基础。

### Vite 正在成为全栈

几年前，构建工具的工作很简单：获取源文件，生成打包文件，然后交付。但对于现代应用来说，这已经不够了，尤其是在某些应用本身就是Agent（智能体）的世界里。

一个现代应用包含服务端渲染路由、API、后台任务、队列、数据库、对象存储、实时功能、认证，以及越来越多的Agent（智能体）和AI能力。“构建”不再是终点，而是部署的起点，部署必须理解所有这些组成部分。

这意味着Vite必须超越构建工具的范畴。它需要更深入地理解应用，同时保持Vite最初成功的核心：速度、简洁性和可移植性。

Void，一个专为Vite设计的部署平台，一直是这些理念的试验场。它帮助我们探索了现代应用框架应该拥有什么、部署应该是什么感觉，以及整个应用生命周期中有多少可以围绕一个工具链统一起来。我们从这项工作中收获良多。

现在，我们要将这些经验应用到正确的地方。有些经验属于Vite本身，作为与提供商无关的基元：为后端、API、Agent（智能体）和部署提供一流的抽象和钩子，任何提供商都可以实现。其他经验则属于Cloudflare内部。Cloudflare将在Workers及其开发者平台的其他部分上，提供这些钩子的一流实现。

尽管一些Vite维护者加入了Cloudflare，但Vite本身的变更将继续遵循与其他Vite贡献相同的开放贡献流程。添加到Vite本身的功能不应是Cloudflare特有的。它们应该在Vite能运行的任何地方都能工作。

### 让Cloudflare向Vite靠拢

同样的原则也塑造了我们如何看待Cloudflare自身工具的未来。我们不是让Vite向Cloudflare的方向发展。恰恰相反：我们将Cloudflare的应用工具迁移到Vite上，使其构建在开发者已经熟悉的工作流程之上。

我们最近发布了`cf`的技术预览版，这是一个面向整个Cloudflare平台的统一CLI。Vite将成为我们应用CLI体验的基础。最终目标是为整个Cloudflare提供一个一致的CLI，无论你是在处理Workers、R2、D1、Agent（智能体）还是其他任何东西，都能获得相同的操作体验。

如果我们做对了，Cloudflare CLI应该感觉像Vite，而不是一个附加在Vite旁边的独立工具。

- `cf dev` 应该是 `vite dev` 的超集。同样的速度，同样的热模块替换，同样的插件模型，外加在你需要时的Cloudflare运行时和绑定。
- `cf build` 应该原生理解Vite项目，无需适配器的繁琐步骤。
- `cf deploy` 应该让将Vite应用部署到Cloudflare变得简单。

`cf dev` 应该是 `vite dev` 的超集。同样的速度，同样的热模块替换，同样的插件模型，外加在你需要时的Cloudflare运行时和绑定。

`cf build` 应该原生理解Vite项目，无需适配器的繁琐步骤。

`cf deploy` 应该让将Vite应用部署到Cloudflare变得简单。

如果你现在正在使用Vite，通往Cloudflare的路径将感觉像是替换为你已经熟悉的命令的超集。相同的项目结构。相同的Vite工作流程。当你需要时，整个Cloudflare开发者平台都触手可及。

### 接下来会发生什么

短期内，对于Vite用户或基于Vite构建的框架来说，没有任何变化：

- Vite、Vitest、Rolldown、Oxc和Vite+将继续发布。VoidZero团队将继续贡献并领导它们。
- Cloudflare Vite插件将持续改进。
- Environment API以及“在本地正确的运行时中运行你的服务端代码”这一更广泛的故事将持续变得更好，包括针对非Cloudflare运行时。

Vite、Vitest、Rolldown、Oxc和Vite+将继续发布。VoidZero团队将继续贡献并领导它们。

Cloudflare Vite插件将持续改进。

Environment API以及“在本地正确的运行时中运行你的服务端代码”这一更广泛的故事将持续变得更好，包括针对非Cloudflare运行时。

长期来看：

- 我们将开始将Cloudflare CLI迁移到直接构建在Vite之上的体验。
- Vite将获得新的、简洁的、与提供商无关的基元，用于全栈应用和Agent（智能体），这些基元适用于任何平台上的所有人。
- 随着时间的推移，我们打算将Void平台开源，以便其他人可以从中学习，并在Vite和Cloudflare之上构建自己的平台。

我们将开始将Cloudflare CLI迁移到直接构建在Vite之上的体验。

Vite将获得新的、简洁的、与提供商无关的基元，用于全栈应用和Agent（智能体），这些基元适用于任何平台上的所有人。

随着时间的推移，我们打算将Void平台开源，以便其他人可以从中学习，并在Vite和Cloudflare之上构建自己的平台。

我们将公开地、与社区一起完成所有这些工作。就像Vite一直以来的构建方式一样。

### 欢迎VoidZero

Vite、Vitest、Rolldown、Oxc和Vite+的存在，是因为一个由开源贡献者组成的深厚生态系统投入了多年的努力。这些项目已经成为构建Web的基础，我们感谢每一位帮助它们走到今天的人。感谢每一位在此过程中贡献代码、评审、问题、文档、插件、集成和支持的人。

我们很高兴欢迎VoidZero团队加入Cloudflare，也很高兴为这些项目投入更多资源。我们现在的任务是帮助它们成长，保持开放，并为所有人赋能JavaScript生态系统。

Vite继续做Vite。Cloudflare提供帮助。

如果你想今天就在Cloudflare上尝试Vite，请运行：

npm create vite@latest

npx wrangler deploy

---

> 本文由AI自动翻译，原文链接：[VoidZero is joining Cloudflare](https://blog.cloudflare.com/voidzero-joins-cloudflare/)
> 
> 翻译时间：2026-06-05 06:22
