---
title: 为整个Cloudflare构建下一代CLI：面向智能体与开发者的统一接口
title_original: Building a CLI for all of Cloudflare
date: '2026-04-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cf-cli-local-explorer/
author: ''
summary: 本文介绍了Cloudflare正在重建其CLI工具Wrangler，旨在为旗下超过100种产品、近3000个API操作提供统一的命令行接口。新系统基于全新的TypeScript模式，能够自动生成CLI命令、配置、SDK、文档等多种接口，以解决当前产品支持分散、更新手动且易出错的问题。技术预览版`cf`已发布，未来将整合现有Wrangler功能，并着重优化对AI智能体及开发者的使用体验。
categories:
- AI基础设施
tags:
- Cloudflare
- CLI
- API
- 开发者工具
- 代码生成
draft: false
translated_at: '2026-04-14T04:42:57.755729'
---

# 为整个 Cloudflare 构建 CLI

2026-04-13

- Matt "TK" Taylor
- Dimitri Mitropoulos
- Dan Carter

![](/images/posts/31abf1d949d4.png)

Cloudflare 拥有庞大的 API 接口。我们拥有超过 100 种产品，以及近 3,000 个 HTTP API 操作。

如今，智能体正日益成为我们 API 的主要客户。开发者们带着他们的编码智能体来 Cloudflare 构建和部署应用程序、智能体和平台，配置他们的账户，并查询我们的 API 以获取分析和日志。

我们希望让每一种 Cloudflare 产品都能以智能体所需的所有方式提供。例如，我们现在将 Cloudflare 的整个 API 集成在一个单一的 Code Mode MCP 服务器中，该服务器使用的 Token 数量少于 1,000 个。然而，还有更多的接口需要覆盖：CLI 命令、Workers 绑定（包括用于本地开发和测试的 API）、跨多种语言的 SDK、我们的配置文件、Terraform、开发者文档、API 文档和 OpenAPI 模式，以及智能体技能。

目前，我们的许多产品并未在所有上述接口中提供支持。这一点在我们的 CLI——Wrangler 上尤为明显。许多 Cloudflare 产品在 Wrangler 中没有 CLI 命令。而智能体们非常喜欢 CLI。

因此，我们一直在重建 Wrangler CLI，旨在使其成为适用于整个 Cloudflare 的 CLI。它将为所有 Cloudflare 产品提供命令，并允许您使用基础设施即代码的方式一起配置它们。

今天，我们分享一个早期版本，展示下一代 Wrangler 作为技术预览版的样子。它非常早期，但公开协作能让我们获得最好的反馈。

您今天就可以通过运行 `npx cf` 来尝试这个技术预览版。或者，您也可以通过运行 `npm install -g cf` 来全局安装它。

目前，`cf` 仅为 Cloudflare 产品的一小部分子集提供命令。我们已经在测试一个支持整个 Cloudflare API 接口的 `cf` 版本——并且我们将有意地审查和调整每个产品的命令，以产生对智能体和人类都符合人体工程学的输出。需要明确的是，这个技术预览版只是未来 Wrangler CLI 的一小部分。在接下来的几个月里，我们将把它与您熟悉和喜爱的 Wrangler 部分整合起来。

为了以一种能与 Cloudflare 产品开发的快速步伐保持同步的方式来构建这个系统，我们必须创建一个新的系统，使我们能够生成命令、配置、绑定 API 等。

## 从第一性原理重新思考模式与代码生成流水线

我们已经基于 Cloudflare API 的 OpenAPI 模式生成了 Cloudflare API SDK、Terraform provider 和 Code Mode MCP 服务器。但是，更新我们的 CLI、Workers 绑定、wrangler.jsonc 配置、智能体技能、仪表板和文档仍然是一个手动过程。这本身就容易出错，需要太多的来回沟通，并且无法扩展到在我们的 CLI 下一个版本中支持整个 Cloudflare API。

要做到这一点，我们需要比 OpenAPI 模式所能表达的更多内容。OpenAPI 模式描述 REST API，但我们有交互式 CLI 命令，这些命令涉及结合本地开发和 API 请求的多个操作，有表达为 RPC API 的 Workers 绑定，以及将所有这一切联系在一起的智能体技能和文档。

我们在 Cloudflare 编写了大量的 TypeScript。它是软件工程的通用语言。我们不断发现，用 TypeScript 表达 API 效果更好——正如我们在 Cap'n' Web、Code Mode 以及内置于 Workers 平台的 RPC 系统中所做的那样。

因此，我们引入了一种新的 TypeScript 模式，它可以定义 API、CLI 命令和参数以及生成任何接口所需的上下文的完整范围。该模式格式“仅仅”是一组带有约定、代码检查和防护措施的 TypeScript 类型，以确保一致性。但因为它是我们自己的格式，所以可以轻松调整以支持我们今天或未来需要的任何接口，同时仍然能够生成 OpenAPI 模式：

迄今为止，我们的大部分精力都集中在这一层——构建我们需要的机器，以便我们现在可以开始构建我们多年来一直希望能够提供的 CLI 和其他接口。这让我们开始梦想，我们可以在 Cloudflare 内部标准化什么，并为智能体做得更好——尤其是在 CLI 的上下文工程方面。

## 智能体与 CLI——一致性与上下文工程

智能体期望 CLI 保持一致。如果一个命令使用 `<command> info` 作为获取资源信息的语法，而另一个使用 `<command> get`，智能体会期望一种语法，并为另一种调用不存在的命令。在一个拥有数百或数千人、众多产品的大型工程组织中，通过审查手动强制执行一致性就像瑞士奶酪一样漏洞百出。你可以在 CLI 层强制执行，但那样 CLI、REST API 和 SDK 之间的命名就会不同，使问题可能变得更糟。

我们首先做的事情之一就是开始在模式层创建规则和防护措施。总是 `get`，从不 `info`。总是 `--force`，从不 `--skip-confirmations`。总是 `--json`，从不 `--format`，并且始终在所有命令中支持。

Wrangler CLI 也相当独特——它提供的命令和配置既可以与模拟的本地资源一起工作，也可以与远程资源一起工作，例如 D1 数据库、R2 存储桶和 KV 命名空间。这意味着一致的默认值甚至更重要。如果一个智能体认为它正在修改远程数据库，但实际上是在向本地数据库添加记录，而开发者正在使用远程绑定来针对远程数据库进行本地开发，那么当智能体向本地开发服务器发出请求时，它将无法理解为什么新添加的记录没有显示出来。一致的默认值，以及明确指示命令是应用于远程还是本地资源的输出，确保智能体获得明确的指导。

## Local Explorer——您能在远程做的，现在也能在本地做

今天，我们还发布了 Local Explorer，这是 Wrangler 和 Cloudflare Vite 插件中都提供的一个处于公开测试阶段的新功能。

Local Explorer 允许您在本地开发时，检查您的 Worker 所使用的模拟资源，包括 KV、R2、D1、Durable Objects 和 Workflows。您可以通过 Cloudflare API 和仪表板对每种资源执行的操作，现在也可以完全在本地执行，由相同的底层 API 结构提供支持。

多年来，我们一直押注于完全本地开发——不仅针对 Cloudflare Workers，而且针对整个平台。当您使用 D1 时，即使 D1 是一个托管的、无服务器的数据库产品，您也可以完全在本地运行您的数据库并通过绑定与其通信，无需任何额外的设置或工具。通过 Miniflare（我们的本地开发平台模拟器），Workers 运行时在本地开发和生产环境中提供完全相同的 API，并使用本地 SQLite 数据库来提供相同的功能。这使得编写和运行快速、无需网络访问且可离线工作的测试变得容易。

但在此之前，要弄清楚本地存储了什么数据，您需要进行逆向工程、检查 `.wrangler/state` 目录的内容，或者安装第三方工具。

现在，每当您使用 Wrangler CLI 或 Cloudflare Vite 插件运行应用程序时，系统都会提示您打开本地浏览器（键盘快捷键 `e`）。这为您提供了一个简单的本地界面，用于查看您的 Worker 当前附加了哪些绑定，以及存储了哪些数据。

当您使用智能体进行构建时，Local Explorer 是理解智能体如何处理数据的好方法，使本地开发周期更具交互性。您可以在需要验证模式、填充一些测试记录，或者只是重新开始并 `DROP TABLE` 时随时打开 Local Explorer。

我们的目标是为Cloudflare API提供一个仅修改本地数据的镜像，这样您所有的本地资源都能通过您远程使用的相同API进行访问。通过使本地和远程的API形态保持一致，当您在即将发布的CLI版本中运行CLI命令并传递`--local`标志时，命令可以直接运行。唯一的区别是，命令会向这个本地的Cloudflare API镜像发起请求，而非远程API。

从今天起，此API可在任何由Wrangler或Vite插件驱动的应用程序中通过`/cdn-cgi/explorer/api`访问。通过将您的Agent指向此地址，它将找到一个OpenAPI规范，从而能够通过与该Agent通信来管理您的本地资源。

## 告诉我们您对Cloudflare全局CLI的期望与愿景

既然我们已经构建了这台机器，现在是时候将Wrangler当前的最佳部分与现在可能实现的功能结合起来，使Wrangler成为使用整个Cloudflare的最佳CLI工具。

您今天就可以通过运行`npx cf`来尝试技术预览版。或者，您可以通过运行`npm install -g cf`将其全局安装。

通过这个非常早期的版本，我们希望得到您的反馈——不仅仅是关于技术预览版目前的功能，还包括您希望从Cloudflare整个平台的CLI中获得什么。告诉我们您希望哪些操作能通过简单的一行CLI命令完成，但目前在我们的仪表板中却需要多次点击。您希望在`wrangler.jsonc`中配置什么——比如DNS记录或缓存规则。以及您在哪些地方遇到过Agent卡住的情况，您希望我们的CLI为您的Agent提供哪些命令。

请加入[Cloudflare Developers Discord](https://discord.com/invite/cloudflaredev)，告诉我们您希望我们首先在CLI中添加什么功能，并请继续关注更多即将到来的更新。

感谢Emily Shen为启动Local Explorer项目做出的宝贵贡献。

---

> 本文由AI自动翻译，原文链接：[Building a CLI for all of Cloudflare](https://blog.cloudflare.com/cf-cli-local-explorer/)
> 
> 翻译时间：2026-04-14 04:42
