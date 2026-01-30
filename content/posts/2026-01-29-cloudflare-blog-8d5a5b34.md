---
title: Moltworker：无需专用硬件，在Cloudflare上自托管个人AI助手
title_original: 'Introducing Moltworker: a self-hosted personal AI agent, minus the
  minis'
date: '2026-01-29'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/
author: ''
summary: 本文介绍了Moltworker，一个基于Cloudflare Workers平台的自托管个人AI智能体解决方案。它通过利用Cloudflare日益完善的Node.js兼容性、Sandbox隔离环境、Browser
  Rendering和R2存储等服务，将原本需要本地硬件（如Mac mini）运行的Moltbot智能体迁移到云端。文章阐述了其架构原理，包括如何通过入口点Worker、AI
  Gateway和容器化环境来安全、高效地运行个人助手应用，从而使用户无需购买专用硬件即可享受私有化AI助手服务。
categories:
- AI产品
tags:
- 自托管AI
- Cloudflare Workers
- 个人智能体
- Node.js兼容性
- 无服务器架构
draft: false
translated_at: '2026-01-30T04:07:39.137235'
---

# 介绍 Moltworker：一款自托管的个人AI智能体，无需迷你主机

2026-01-29

- Celso Martinho
- Brian Brunner
- Sid Chatterjee
- Andreas Jansson

![](/images/posts/29ecca899441.png)

本周，互联网上涌现了大量购买Mac mini来运行Moltbot（原名Clawdbot）的用户。Moltbot是一款开源、自托管的AI智能体，旨在充当个人助手。它在用户自己的硬件后台运行，拥有庞大且不断增长的聊天应用、AI模型及其他流行工具的集成列表，并支持远程控制。Moltbot可以帮助您管理财务、社交媒体、安排日程——所有这些都通过您喜爱的即时通讯应用完成。

但如果您不想购买新的专用硬件呢？如果您仍能在线上高效安全地运行Moltbot呢？请见Moltworker，这是一个中间件Worker及适配脚本，允许您在Cloudflare的Sandbox SDK和我们的开发者平台API上运行Moltbot。

## 在Cloudflare上运行个人助手——这是如何实现的？

Cloudflare Workers的Node.js兼容性比以往任何时候都要好。过去我们必须模拟API才能运行某些软件包，而现在这些API已由Workers Runtime原生支持。

这改变了我们在Cloudflare Workers上构建工具的方式。当我们首次实现Playwright（一个在浏览器渲染上运行的流行Web测试与自动化框架）时，我们不得不依赖memfs。这很糟糕，因为memfs不仅是一种临时方案和外部依赖，还迫使我们偏离了官方的Playwright代码库。值得庆幸的是，随着Node.js兼容性的提升，我们能够开始原生使用node:fs，降低了复杂性和维护难度，使得升级到最新版本的Playwright变得轻而易举。

我们原生支持的Node.js API列表持续增长。博客文章《Cloudflare Workers中提升Node.js兼容性的一年》概述了我们当前的进展和正在开展的工作。

我们也衡量这一进展。最近我们进行了一项实验：选取1000个最流行的NPM软件包，安装后让AI自由尝试在Cloudflare Workers中运行它们（采用“Ralph Wiggum式‘软件工程师’”风格），结果出奇地好。排除那些属于构建工具、CLI工具或仅限浏览器使用且不适用的情况，只有15个软件包确实无法运行。**这仅占1.5%。**

以下是我们Node.js API支持情况随时间变化的图表：

我们整理了一个页面，展示了我们关于NPM软件包支持的内部实验结果，您可以在此自行查看。

Moltbot并不一定需要Workers具备大量的Node.js兼容性，因为大部分代码无论如何都在容器中运行，但我们认为强调我们通过原生API支持了如此多软件包所取得的进展非常重要。这是因为，当从头开始构建一个新的AI智能体应用时，我们实际上可以在Workers中运行大量逻辑，更贴近用户。

故事的另一个重要部分是，我们开发者平台的产品和API列表已增长到足以让任何人在Cloudflare上构建和运行任何类型的应用——即使是最复杂、要求最高的应用。而且，一旦启动，在我们开发者平台上运行的每个应用都能立即受益于我们安全、可扩展的全球网络。

这些产品和服务为我们提供了起步所需的要素。首先，我们现在拥有Sandboxes，您可以在隔离环境中安全地运行不受信任的代码，为运行服务提供了场所。其次，我们现在拥有Browser Rendering，您可以以编程方式控制无头浏览器实例并与之交互。最后，还有R2，您可以持久存储对象。有了这些可用的构建模块，我们就可以开始着手适配Moltbot。

## 我们如何将Moltbot适配到我们的平台上运行

Workers上的Moltbot，即Moltworker，是一个入口点Worker的组合体，它充当API路由器以及我们API与隔离环境之间的代理，两者均受Cloudflare Access保护。它还提供了一个管理界面，并连接到运行标准Moltbot Gateway运行时及其集成的Sandbox容器，同时使用R2进行持久存储。

Moltworker的高层架构图。

让我们深入探讨。

### AI Gateway

Cloudflare AI Gateway充当您的AI应用与任何流行AI提供商之间的代理，并为我们的客户提供对通过请求的集中可见性和控制。

最近我们宣布支持自带密钥（BYOK），即我们为您集中管理密钥，并可在您的网关配置中使用它们，而无需在每次请求中以明文传递您的提供商密钥。

一个更优的选择是使用统一计费，这样您完全无需端到端地管理AI提供商的密钥。在这种情况下，您为账户充值积分，直接通过AI Gateway使用任何受支持的提供商，Cloudflare负责计费，我们将从您的账户中扣除积分。

要让Moltbot使用AI Gateway，首先我们创建一个新的网关实例，然后为其启用Anthropic提供商，接着要么添加我们的Claude密钥，要么购买积分以使用统一计费，最后我们只需设置ANTHROPIC_BASE_URL环境变量，使Moltbot使用AI Gateway端点即可。就这样，无需更改代码。

一旦Moltbot开始使用AI Gateway，您将完全掌握成本情况，并能访问日志和分析，帮助您了解您的AI智能体如何使用AI提供商。

请注意，Anthropic只是其中一个选项；Moltbot支持其他AI提供商，AI Gateway也是如此。使用AI Gateway的优势在于，如果任何提供商推出了更好的模型，您无需在AI智能体配置中更换密钥并重新部署——您只需在网关配置中切换模型。此外，您还可以指定模型或提供商的回退方案，以处理请求失败并确保可靠性。

### Sandboxes

去年，我们预见到AI智能体在隔离环境中安全运行不受信任代码的需求日益增长，并宣布了Sandbox SDK。该SDK构建于Cloudflare Containers之上，但它提供了一个简单的API，用于执行命令、管理文件、运行后台进程以及暴露服务——所有这些都从您的Workers应用中完成。

简而言之，Sandbox SDK为您提供了开发者友好的API用于安全代码执行，并处理了容器生命周期、网络、文件系统和进程管理的复杂性，让您只需几行TypeScript代码就能专注于构建应用逻辑，而无需处理底层的Container API。以下是一个示例：

```TypeScript
import { getSandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const sandbox = getSandbox(env.Sandbox, 'user-123');

    // 创建项目结构
    await sandbox.mkdir('/workspace/project/src', { recursive: true });

    // 检查node版本
    const version = await sandbox.exec('node -v');

    // 运行一些python代码
    const ctx = await sandbox.createCodeContext({ language: 'python' });
    await sandbox.runCode('import math; radius = 5', { context: ctx });
    const result = await sandbox.runCode('math.pi * radius ** 2', { context: ctx });

    return Response.json({ version, result });
  }
};
```

这对Moltbot来说再合适不过。我们不是在您本地的Mac mini上运行Docker，而是在Containers上运行Docker，使用Sandbox SDK向隔离环境发出命令，并通过回调到我们的入口点Worker，从而有效地在两个系统之间建立了双向通信通道。

### 用于持久存储的R2

在本地计算机或VPS上运行程序的一个好处是，您可以免费获得持久存储。然而，容器本质上是**临时的**，这意味着其中生成的数据在容器删除时会丢失。不过别担心——Sandbox SDK 提供了 `sandbox.mountBucket()` 方法，您可以在容器启动时使用它来自动将您的 R2 存储桶挂载为文件系统分区。

一旦我们拥有了一个保证能在容器生命周期之外持续存在的本地目录，我们就可以用它来让 Moltbot 存储会话记忆文件、对话记录以及其他需要持久化的资源。

### 用于浏览器自动化的浏览器渲染

AI Agent（智能体）在很大程度上依赖于浏览有时结构并不严谨的网页。Moltbot 利用专用的 Chromium 实例来执行操作、浏览网页、填写表单、截取快照以及处理需要网络浏览器的任务。当然，我们也可以在沙箱中运行 Chromium，但如果我们能简化操作并使用 API 来代替呢？

借助 Cloudflare 的**浏览器渲染**功能，您可以通过编程方式控制和交互在我们边缘网络中大规模运行的无头浏览器实例。我们支持 **Puppeteer**、**Stagehand**、**Playwright** 以及其他流行的软件包，以便开发者只需最少的代码改动即可上手。我们甚至为 AI 支持 **MCP**。

为了让浏览器渲染与 Moltbot 协同工作，我们做了两件事：

*   首先，我们创建一个**轻量级 CDP 代理**（**CDP** 是允许对基于 Chromium 的浏览器进行检测的协议），从沙箱容器连接到 Moltbot Worker，再使用 Puppeteer API 连接回浏览器渲染服务。
*   然后，在沙箱启动时，我们向运行时注入一个**浏览器渲染技能**。

首先，我们创建一个**轻量级 CDP 代理**（**CDP** 是允许对基于 Chromium 的浏览器进行检测的协议），从沙箱容器连接到 Moltbot Worker，再使用 Puppeteer API 连接回浏览器渲染服务。

然后，在沙箱启动时，我们向运行时注入一个**浏览器渲染技能**。

从 Moltbot 运行时的角度来看，它有一个可以连接的本地 CDP 端口，并可以执行浏览器任务。

### 用于认证策略的零信任访问

接下来，我们希望保护我们的 API 和管理界面免受未经授权的访问。从头开始做身份验证很困难，而且通常是您不想重新发明或不得不处理的轮子。零信任访问通过为端点定义特定的策略和登录方法，使得保护您的应用程序变得异常简单。

为 Moltworker 应用程序配置的零信任访问登录方法。

一旦端点受到保护，Cloudflare 将为您处理身份验证，并自动在发送到您源端点的每个请求中包含一个 **JWT 令牌**。然后，您可以**验证**该 JWT 以提供额外保护，确保请求来自 Access 服务，而非恶意的第三方。

与 AI 网关类似，一旦您的所有 API 都置于 Access 之后，您就能很好地了解用户是谁以及他们如何使用您的 Moltbot 实例。

## Moltworker 实战演示

演示时间到了。我们搭建了一个 Slack 实例，可以在其中使用我们部署在 Workers 上的 Moltbot 实例。以下是我们用它完成的一些有趣的事情。

我们讨厌坏消息。

这是一个聊天会话，我们要求 Moltbot 使用谷歌地图查找伦敦 Cloudflare 办公室到里斯本 Cloudflare 办公室之间的最短路线，并在 Slack 频道中截取屏幕截图。它通过一系列步骤，使用浏览器渲染功能来导航谷歌地图，并且完成得相当不错。另外，请注意当我们第二次询问时，Moltbot 的记忆是如何发挥作用的。

我们今天想吃点亚洲菜，让 Moltbot 来帮忙找找。

我们也用眼睛"品尝"美食。

让我们更有创意一点，要求 Moltbot 创建一个浏览我们开发者文档的视频。如您所见，它会下载并运行 ffmpeg，根据它在浏览器中捕获的帧来生成视频。

## 运行您自己的 Moltworker

我们已经将我们的实现开源，并发布在 https://github.com/cloudflare/moltworker，因此您今天就可以在 Workers 上部署和运行您自己的 Moltbot。

`README` 文件会指导您完成所有必要的设置步骤。您需要一个 Cloudflare 账户，并且至少订阅 **5 美元/月的 Workers 付费计划** 才能使用沙箱容器，但所有其他产品要么可以免费使用（如 **AI 网关**），要么提供**慷慨的免费额度**，您可以在合理的限制内免费开始使用并长期运行。

请注意，Moltworker 是一个概念验证项目，并非 Cloudflare 的正式产品。我们的目标是展示我们**开发者平台**中一些最令人兴奋的功能，这些功能可用于高效、安全地运行 AI Agent（智能体）和无监督代码，并在利用我们全球网络的同时获得出色的可观测性。

欢迎为我们的 **GitHub** 仓库贡献代码或进行分支；我们会在一段时间内关注并提供支持。同时，我们也考虑向上游的官方项目贡献 Cloudflare 相关的技能。

## 结论

我们希望您喜欢这个实验，并且我们能够说服您，Cloudflare 是运行您的 AI 应用程序和 Agent（智能体）的绝佳平台。我们一直在不懈努力，试图预见未来并发布新功能，例如 **Agent SDK**，您可以用它在**几分钟内**构建您的第一个 Agent（智能体）；**沙箱**，您可以在隔离环境中运行任意代码，而无需处理容器的生命周期复杂性；以及 **AI Search**，Cloudflare 托管的基于向量的搜索服务，等等。

Cloudflare 现在提供了一套完整的 AI 开发工具包：推理、存储 API、数据库、用于有状态工作流的持久执行，以及内置的 AI 功能。这些构建模块结合在一起，使得在我们全球边缘网络上构建和运行即使是最苛刻的 AI 应用程序也成为可能。

如果您对 AI 感到兴奋，并希望帮助我们构建下一代产品和 API，我们正在**招聘**。

---

> 本文由AI自动翻译，原文链接：[Introducing Moltworker: a self-hosted personal AI agent, minus the minis](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/)
> 
> 翻译时间：2026-01-30 04:07
