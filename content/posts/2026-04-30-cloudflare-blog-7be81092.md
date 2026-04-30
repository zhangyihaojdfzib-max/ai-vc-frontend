---
title: Agent可自主创建Cloudflare账户并部署应用
title_original: Agents can now create Cloudflare accounts, buy domains, and deploy
date: '2026-04-30'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/agents-stripe-projects/
author: ''
summary: Cloudflare宣布Agent现在可以代表用户自动完成账户创建、域名购买、支付订阅和API Token获取等全流程操作，无需人工干预。通过与Stripe合作的新协议，Agent能从零开始部署生产应用，包括发现可用服务、授权身份验证和支付处理。这一突破消除了传统手动配置步骤，使AI
  Agent能独立完成从零到生产的完整部署流程。
categories:
- AI产品
tags:
- Cloudflare
- AI Agent
- 自动化部署
- Stripe
- MCP协议
draft: false
translated_at: '2026-04-30T05:32:40.664342'
---

# Agent 现在可以创建 Cloudflare 账户、购买域名并部署

2026-04-30

- Sid Chatterjee
- Brendan Irvine-Broque

![](/images/posts/d8b3322f3d9f.png)

编程 Agent 非常擅长构建软件。但要部署到生产环境，它们需要从托管应用的云平台获得三样东西——一个账户、一种支付方式和一个 API Token。到目前为止，这些任务都需要人类直接处理。如今，Agent 越来越多地代表用户处理这些事务。Agent 需要执行人类客户所能完成的所有任务。它们被赋予更高层次的问题来解决，并选择使用 Cloudflare 和调用 Cloudflare API。

从今天开始，Agent 可以代表用户配置 Cloudflare。它们可以创建 Cloudflare 账户、开通付费订阅、注册域名，并获取 API Token 以便立即部署代码。人类可以参与授权流程，并且必须接受 Cloudflare 的服务条款，但除此之外，从头到尾无需人工操作。无需访问控制面板、复制粘贴 API Token 或输入信用卡信息。无需任何额外设置，Agent 就能一次性获得部署新生产应用所需的一切。借助 Cloudflare 的 Code Mode MCP 服务器和 Agent Skills，它们在这方面表现更佳。

这一切都通过我们与 Stripe 共同设计的新协议实现，该协议是 Stripe Projects 发布的一部分。

我们很高兴宣布与 Stripe 建立这一新的合作伙伴关系，并向所有使用 Stripe Atlas 注册的新创企业提供 10 万美元的 Cloudflare 信用额度。但这一新协议也使得任何拥有登录用户的平台都能像 Stripe 一样与 Cloudflare 集成，对最终用户实现零摩擦。

## 工作原理：从零到生产，无需任何设置或手动步骤

安装带有 Stripe Projects 插件的 Stripe CLI，登录 Stripe，然后启动一个新项目：

```JavaScript
stripe projects init
```

然后提示你的 Agent 构建新内容并将其部署到新域名。你可以在下方观看整个流程的浓缩两分钟视频：

如果你登录 Stripe 所用的邮箱已有 Cloudflare 账户，系统会提示你通过标准的 OAuth 流程授予 Agent 访问权限。如果该邮箱没有现有 Cloudflare 账户，Cloudflare 将自动为你和你的 Agent 配置一个账户：

你会看到 Agent 构建一个网站并将其部署到新的 Cloudflare 账户，然后使用 Stripe Projects CLI 注册域名：

Agent 会在必要时提示输入和审批。例如，如果你的 Stripe 账户尚未关联支付方式，Agent 会提示你添加一个：

最后，Agent 已部署到生产环境，应用在新注册的域名上运行：

Agent 从字面意义上的零开始——没有 Cloudflare 账户，没有任何预配置的 Agent Skills 或 MCP 服务器——到最终拥有：

- 配置了一个新的 Cloudflare 账户
- 获取了一个 API Token
- 购买了一个域名
- 将一个应用部署到生产环境

配置了一个新的 Cloudflare 账户

获取了一个 API Token

购买了一个域名

将一个应用部署到生产环境

但等等——Agent 是如何发现它可以完成所有这些操作的？它如何知道可以配置哪些服务，以及如何购买域名？它如何获得理解如何部署到 Cloudflare 所需的上下文？让我们深入探讨。

## 协议与集成的工作原理

上述 Agent、Stripe 和 Cloudflare 之间的交互包含三个组件：

- 发现——Agent 可以调用命令查询可用服务目录。
- 授权——平台证明用户身份，允许服务提供商配置账户或关联现有账户，并安全地将凭证返回给 Agent。
- 支付——平台提供支付 Token，服务提供商可用其向客户收费，允许 Agent 启动订阅、进行购买并按使用量计费。

发现——Agent 可以调用命令查询可用服务目录。

授权——平台证明用户身份，允许服务提供商配置账户或关联现有账户，并安全地将凭证返回给 Agent。

支付——平台提供支付 Token，服务提供商可用其向客户收费，允许 Agent 启动订阅、进行购买并按使用量计费。

这些建立在现有技术和标准（如 OAuth、OIDC 和支付 Token 化）之上——但将它们结合使用，消除了许多原本需要人工参与的步骤。

## 发现：Agent 如何找到可以自行配置的服务

在上述 Agent 会话中，在 Agent 运行 CLI 命令 `stripe projects add cloudflare/registrar:domain` 之前，它首先需要发现 Cloudflare Registrar 服务。它通过调用 `stripe projects catalog` 命令来实现，该命令返回可用服务：

Cloudflare 产品的完整集合以及其他提供商的服务既庞大且不断增长——对人类来说可能令人不知所措。但对于 Agent 来说，这个服务目录正是它们所需的上下文。Agent 根据用户要求它们做的事情以及用户的偏好，从该目录中选择要使用的服务——但用户无需事先了解哪些提供商提供哪些服务，也无需提供任何输入。像 Cloudflare 这样的提供商通过一个简单的返回 JSON 的 REST API 提供此目录，为 Agent 提供所需的一切。

## 授权：为新用户即时创建账户

当 Agent 选择一项服务并进行配置时（例如：`stripe projects add cloudflare/registrar:domain`），它会在 Cloudflare 账户内配置资源。但它是如何能够按需创建账户，而无需将用户引导至注册页面的呢？

还记得开始时用户登录了他们的 Stripe 账户吗？Stripe 充当身份提供商，证明用户身份。如果用户尚未拥有账户，Cloudflare 会自动为用户配置一个新账户，并将凭证返回给 Stripe Projects CLI，这些凭证被安全存储，但可供 Agent 用于向 Cloudflare 发起经过身份验证的请求。这意味着，即使某人从未使用过 Cloudflare 或其他服务，他们也可以立即与 Agent 一起开始构建，无需额外步骤。

如果用户已有 Cloudflare 账户，他们将通过标准的 OAuth 流程授予 Stripe Projects CLI 访问权限，从而允许其在现有 Cloudflare 账户上配置资源。

## 支付：给你的 Agent 一个可支配的预算，无需提供信用卡信息

你可能会担心："如果我的 Agent 有点过头，开始购买几十个域名怎么办？我最终会不会面临巨额账单？我真的能把信用卡交给我的 Agent 吗？"

该协议通过两种方式解决了这个问题。当 Agent 配置付费服务时，Stripe 会在向提供商（Cloudflare）发出的请求中包含一个支付 Token。信用卡号等原始支付信息永远不会与 Agent 共享。Stripe 随后设置默认限额为每月 100.00 美元，作为 Agent 在任何单个提供商上的最大支出。当你准备提高此限额时，可以在 Cloudflare 账户上设置预算提醒。

## 任何拥有登录用户的平台都可以像 Stripe 一样与 Cloudflare 集成

任何拥有登录用户的平台都可以充当"编排器"，扮演 Stripe 在 Stripe Projects 中的角色，并与 Cloudflare 集成。

假设你的产品是一个编程Agent（智能体）。你希望用户能够将他们构建的内容部署到生产环境，使用Cloudflare和其他服务。但你最不想做的就是让用户陷入授权流程和部署位置及方式的决策树迷宫中。你只想让人们顺利发布产品。

你的平台作为编排器，用户已登录。当你的用户需要一个域名、一个存储桶、一个沙箱来提供给他们的Agent（智能体），或任何其他资源时，你只需向Cloudflare发起一次API调用，为其预配一个新的Cloudflare账户，并取回一个令牌，以便代表他们进行经过身份验证的请求。

或者，假设你希望Cloudflare客户能够轻松预配你的服务，类似于Cloudflare与Planetscale合作，使得可以直接从Cloudflare创建Planetscale Postgres数据库。我们早在该新协议启动之前就与Planetscale开始了这方面的合作，但这里的流程非常相似。Cloudflare作为编排器，让你能够连接到你的Planetscale账户、创建数据库，并使用用户现有的支付方式进行计费。

这一新协议开始标准化许多平台多年来一直在进行的跨产品集成类型，而这些集成往往是以一次性或特定于某个平台的方式完成的。没有标准，每次集成都需要工程投入，且通常无法为未来的集成所复用。类似于OAuth标准使得将账户访问权限委托给其他平台成为可能，该协议使用了OAuth，并进一步扩展到支付和账户创建，同时将Agent（智能体）作为首要关注点。

我们很高兴能继续发展这一标准，并很快与Stripe合作分享更正式的规范。我们也期待与更多平台集成——请发送邮件至[email protected]，告诉我们你希望你的平台如何与Cloudflare集成。

## 赋予你的Agent（智能体）预配和支付能力

Stripe Projects现已公开测试，即使你还没有Cloudflare账户，也可以开始使用。只需安装Stripe CLI，登录Stripe，然后启动一个新项目：

```JavaScript
stripe projects init
```

提示你的Agent（智能体）在Cloudflare上构建新内容，并向我们展示你的成果！

---

> 本文由AI自动翻译，原文链接：[Agents can now create Cloudflare accounts, buy domains, and deploy](https://blog.cloudflare.com/agents-stripe-projects/)
> 
> 翻译时间：2026-04-30 05:32
