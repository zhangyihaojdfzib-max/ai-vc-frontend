---
title: Cloudflare与Anthropic合作推出Claude托管Agent集成
title_original: Announcing Claude Managed Agents on Cloudflare
date: '2026-05-19'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/claude-managed-agents/
author: ''
summary: Cloudflare与Anthropic合作，将Claude Managed Agents集成到Cloudflare平台，为开发者提供更安全、可编程的Agent云环境。该集成允许Agent在Anthropic运行核心循环（大脑），而在Cloudflare执行代码和工具调用（双手），实现安全连接、沙箱控制、可观测性、私有服务连接等功能。开发者可通过默认模板快速部署，获得增强安全性、轻量级沙箱、浏览器控制等开箱即用能力。
categories:
- AI基础设施
tags:
- Claude
- Cloudflare
- 托管Agent
- AI基础设施
- 沙箱
draft: false
translated_at: '2026-05-20T06:12:00.727450'
---

# 在Cloudflare上发布Claude Managed Agents（托管Agent）

2026-05-19

- Mike Nomitch

![](/images/posts/2d123887580c.png)

Cloudflare和Anthropic合作，将Claude Managed Agents（托管Agent）与Cloudflare Sandboxes（沙箱）集成。我们的新集成让您对Agent沙箱拥有更多控制权，保障与私有服务的连接安全，并提升可观测性。

过去一年中，Cloudflare的开发者平台不断扩展，为更多开发者提供了大规模运行Agent所需的工具。其中包括：

- Sandboxes（沙箱）——用于大规模运行全状态Linux微型虚拟机
- Agents SDK——提供简单且可定制的Agent框架
- Browser Run——为Agent提供完全可编程且可观测的浏览器
- Dynamic Workers——支持大规模动态沙箱化代码执行

我们的目标是让Cloudflare成为最简洁、最安全、最可编程的Agent云平台。

与Claude Managed Agents（托管Agent）的集成是朝着这一方向迈出的又一步。您可以在Claude平台上运行Agent循环，同时使用Cloudflare执行代码、保障连接安全以及运行自定义工具调用。

为了帮助您在几分钟内快速上手，我们创建了一个默认部署模板，为您提供以下功能：

- 增强安全性——通过可自定义的代理路由所有Agent流量。这使您能够安全地注入凭证、防止数据泄露，并更好地观察Agent与外部世界的交互方式。
- 沙箱控制与可观测性——获取详细的沙箱指标和日志。通过SSH进入正在运行的机器。自定义沙箱镜像。
- 轻量级沙箱——编写和执行不受信任的代码可以在传统微型虚拟机或轻量级隔离环境中完成。这使您能够达到大规模水平，在毫秒内启动沙箱，并最大限度地减少基础设施支出。
- 私有服务连接——将Agent连接到私有内部服务，而无需将其暴露在互联网上。
- 浏览器控制与可观测性——获取每个Agent浏览器会话的审计追踪，包括会话录制和人机协同流程。
- 电子邮件——为每个Agent分配独立的电子邮件地址和发送邮件的能力。
- 自定义工具——无需额外基础设施即可为Agent扩展工具。只需编写函数并部署即可。

部署集成后，您即可开箱即用地获得所有这些功能，如果需要更多功能，还可以轻松自定义。

让我们简要了解一下Claude Managed Agents（托管Agent），看看如何集成基于Cloudflare的环境，然后探索如何在Cloudflare上充分利用Claude。

## Claude Managed Agents（托管Agent）概述

Claude Managed Agents（托管Agent）使开发者能够轻松地在Anthropic平台上定义和运行Agent。在这些托管环境中，Claude可以读取文件、运行命令、浏览网页和执行代码。该框架支持内置的提示词缓存、压缩以及各种Agent优先的性能优化。

到目前为止，使用Claude Managed Agents（托管Agent）意味着要在Anthropic提供的基础设施上运行整个堆栈。虽然这对某些开发者来说很好，但其他开发者可能出于安全、合规或性能原因，需要对其基础设施选择拥有更多控制权。Claude Agent的自管理环境正好提供了这一点。

Anthropic将此描述为"将大脑与双手解耦"。核心Agent循环在Anthropic中运行（"大脑"），但运行和执行代码的基础设施（"双手"）可以在任何地方运行，包括Cloudflare。

## Cloudflare环境

我们的新集成使您的Agent能够在几分钟内获得基于Cloudflare的运行和执行代码的环境。

按照入门指南开始使用。然后复刻仓库并根据需要自定义集成。

设置完成后，当Claude Agent启动会话时，它会向您新的基于Cloudflare的控制平面发送消息。基于Workers的控制平面为每个Agent会话提供一个沙箱化环境，用于执行代码、开发应用程序、运行CLI工具等。状态会在会话休眠期间自动持久化。

沙箱响应基于Claude的Agent循环来写入文件和执行代码

您可以选择配置沙箱实例大小，或自定义在基于VM的沙箱内运行的容器镜像。每个沙箱都可以在Cloudflare仪表板中观察，沙箱日志可以查询或发送到Datadog或Splunk等外部提供商，控制平面附带内置UI，便于跟踪沙箱状态或通过SSH进入特定机器。

获取Agent沙箱的交互式Shell会话

## 在互联网规模上启用Agent

如果您的Agent后端能在几毫秒内启动，并且运行Agent时无需为完整VM的资源付费，那会怎样？

随着我们大规模采用Agent，行业需要一种轻量级的沙箱原语，而我们正在构建这样的解决方案。

但随着模型不断改进，我们预计越来越多的工作流将由Agent管理。您的每个客户应该能够同时运行多个Agent；您的每位员工应该能够同时运行数十个Agent。如果我们为每个Agent持续运行一个完整的微型虚拟机，我们将不必要地消耗大量资源和资金来实现这种规模。

这就是为什么我们为您的Claude Agent提供更快、更便宜的沙箱。该沙箱基于Agents SDK构建。您可以使用Codemode在Dynamic Workers中执行任意代码，并且仍然拥有文件系统，但您的Agent是在V8隔离环境而非微型虚拟机中完成所有这些操作。

如果您需要Agent像开发者一样行动，构建完整的应用程序并运行基于Linux的工具，您仍然可以使用基于微型虚拟机的沙箱。为此，我们提供Cloudflare Containers，Claude Managed Agents（托管Agent）也可以使用它。

但如果您想要更快、更便宜、更具可扩展性的替代方案，您可以轻松使用隔离环境而非微型虚拟机。只需在设置Agent时为后端类型选择"isolate"即可。

设置"isolate"后端会为您提供轻量级的V8隔离沙箱，而非微型虚拟机

如果您需要处理数万个或更多并发Agent的突发流量，使用隔离环境将使您能够以任何基于VM的解决方案都无法实现的方式进行扩展。

## 保障您的Agent工作负载安全

当Agent连接到您组织的上下文时，它们会变得更加强大。这通常意味着访问私有服务和数据。

正如我们之前所写，Cloudflare 上的沙盒工作负载可以使用出站代理，在沙盒与外部服务之间实现完全动态、可定制且零信任的身份验证。这让你可以在沙盒外部将机密信息注入请求，因此 Agent（智能体）永远无法访问它们。这可以防范数据泄露攻击。

有时内部服务根本不应该暴露在开放互联网上。我们最近推出了 Cloudflare Mesh 和 Cloudflare Workers VPC，以便更好地连接这些私有服务，无论它们是在 AWS 等云提供商上运行，还是在本地运行。这让你无需 VPN 或堡垒机，即可使用后量子加密网络连接到内部服务。

Claude Managed Agents 可以通过标头注入或私有 VPC/Mesh 隧道轻松连接到私有服务。这是通过可定制的出站代理实现的。你可以定义出口策略，仅将你选择的服务暴露给你选择的 Agent（智能体）沙盒。你可以将特定端点加入白名单，执行加密凭据的零信任注入，通过 Cloudflare Mesh 访问私有服务，甚至编写自定义代理中间件。

该集成使用出站 Workers 以你认为合适的方式处理出口流量。

你可以按租户、按 Agent（智能体）或基于任何有用的元数据来应用策略。这让你可以完全控制你的 Agent（智能体）如何连接到外部服务。

## 利用 Cloudflare 开发者平台做更多事

Agent（智能体）需要的不仅仅是代码执行环境。Cloudflare 的开发者平台默认提供了你所需的工具，让你的 Agent（智能体）能做更多事情。

沙盒可以在 Cloudflare 上进行工具调用，并安全地访问外部服务。

以下是在 Cloudflare 上部署 Agent（智能体）时，你会发现最有用的几个工具：

### 通过 Claude 使用 Browser Run

Agent（智能体）最常用的工具之一是浏览器。虽然 `curl` 可以帮你完成很多工作，但当你希望 Agent（智能体）像人类一样行动时，这通常意味着要像人类一样与网络交互：渲染重度 JS 应用、截取 QA 验证截图、填写表单等。Browser Run 是 Cloudflare 为 Agent（智能体）提供浏览器的工具。

Browser Run 会话记录让你可以观察 Agent（智能体）如何使用浏览器。这是众多内置工具之一。

Claude Managed Agents 集成附带多个与浏览器相关的工具，可以立即启用。这些工具包括 `browser_search`、`browser_execute`、`screenshot`、`browse`、`fetch_to_markdown`，以及一个 Cloudflare 特有的 `web_fetch` 实现，它允许你的 Agent（智能体）控制一个在 Cloudflare 基础设施上运行的浏览器。这不仅让你的 Agent（智能体）能做更多事情，还让你可以轻松审计 Agent（智能体）的浏览器在网络上执行的每一个操作，为浏览器会话应用白名单和黑名单，并保存浏览器会话记录以供将来调试。

### Agent（智能体）收件箱

该集成还内置了对电子邮件的支持，提供了 `send_email`、`email_read` 和 `email_list` 工具。

你还可以通过电子邮件启动新的会话，或配置 Agent（智能体）使用通过 Cloudflare Email Service 配置的任何域名和地址发送电子邮件。这使得 Agent（智能体）可以在需要时代表你行事，回复转发邮件中的上下文，并通过电子邮件自主与他人互动。

### 自定义工具及更多

其他内置工具包括 `call_service`，它使用 Cloudflare Mesh 或 Workers VPC 连接到私有服务，以及 `image_generate`，它使用 Workers AI 在 Cloudflare 上生成图像。这与 Claude 提供基于文本的推理配合得很好。

此外，我们鼓励 Fork 仓库以轻松添加自定义工具。例如，你可以添加一个自定义工具，在 Cloudflare 的 R2 对象存储上托管公共文件。只需在 wrangler 配置中添加相关绑定，编写一个 zod 定义，以及在 `custom-tools.js` 中编写一个简短函数：

```JavaScript
defineTool({
  name: "r2_host_file",
  description: "从沙盒上传到 R2 并获取公共 URL。",
  inputSchema: z.object({
    key: z.string().describe("对象键"),
    content: z.string().describe("UTF-8 文件内容"),
    contentType: z.string().describe("MIME 类型"),
  }),
  run: async ({ key, content, contentType }, { env }) => {
    await env.PUBLIC_BUCKET.put(
      key, content, { httpMetadata: { contentType }}
    );
    return `${env.PUB_R2_URL.replace(/\/$/, "")}/${encodeURI(key)}`;
  }
}),
```

Cloudflare 开发者平台为扩展你的 Agent（智能体）提供了各种可能性：通过 Artifacts 为每个 Agent（智能体）会话提供一个 Git 支持的仓库，使用 Workers AI 运行边缘推理，通过 Dynamic Workers 托管即时编写的应用程序，等等。

你无需担心基础设施或扩展问题——只需编写几行代码，然后点击部署即可。

## Claude + Cloudflare

我们很高兴能与 Anthropic 合作，将 Cloudflare 的灵活性、可扩展性和安全性带给更多用户。无论你是想使用隔离技术运行数千万个 Agent（智能体），通过 Workers VPC 安全连接到私有服务，还是编写利用 Cloudflare 全部功能的自定义工具，我们的新集成都让这一切变得简单。

请参阅 Managed Agents 入门指南，在几分钟内将 Claude Managed Agents 与 Cloudflare 集成。

---

> 本文由AI自动翻译，原文链接：[Announcing Claude Managed Agents on Cloudflare](https://blog.cloudflare.com/claude-managed-agents/)
> 
> 翻译时间：2026-05-20 06:12
