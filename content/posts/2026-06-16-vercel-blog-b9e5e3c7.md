---
title: Vercel推出企业级AI应用与Agent安全平台
title_original: Vercel for Enterprise Apps and Agents
date: '2026-06-16'
source: Vercel Blog
source_url: https://vercel.com/blog/vercel-for-enterprise-apps-and-agents
author: ''
summary: Vercel正式发布面向企业应用与Agent的平台，旨在解决AI Agent在企业内部大规模使用后的安全与权限管理问题。该平台包含Vercel Passport（默认将内部应用置于身份提供商之后）、Vercel
  Connect（为Agent提供短期、作用域受限的系统凭证）以及Enterprise Managed Users（通过目录实现用户生命周期管理）等核心组件，帮助企业安全交付AI能力。
categories:
- AI产品
tags:
- Vercel
- 企业AI
- Agent安全
- 身份管理
- AI基础设施
draft: false
translated_at: '2026-06-19T07:09:14.046661'
---

今天我们正式推出 **Vercel for Enterprise Apps and Agents（面向企业应用与Agent的平台）**，让整个公司都能在自身访问与安全边界内，安全地交付AI能力。

过去一年里，Vercel 的员工交付了数百个 Agent 和内部应用。上线到生产环境是容易的部分，因为我们基于 **Agent Stack（Agent技术栈）** 在 **v0** 上构建了它们，并部署在 Vercel 上。

真正棘手的问题出现在这些 Agent 被公司员工广泛使用之后：

- 谁有权使用每个 Agent？
- 如何确保内部 Agent 不对外泄露？
- Agent 可以接触哪些数据和系统？
- Agent 使用了哪些模型，成本是多少？

谁有权使用每个 Agent？

如何确保内部 Agent 不对外泄露？

Agent 可以接触哪些数据和系统？

Agent 使用了哪些模型，成本是多少？

### Vercel for Enterprise Apps and Agents

我们构建 Enterprise Apps and Agents 正是为了回答这些问题。它让所有权、访问权限和安全性成为构建者默认继承的特性，而不是平台团队需要排队处理的项目。

**平台组件**

**安全实现**

**Vercel Passport**  
默认将每个内部应用和 Agent 置于你的身份提供商之后

**Vercel Connect**  
为 Agent 提供对其所用系统（如 Slack、GitHub、Snowflake、Salesforce 和 Linear）的短期、作用域受限的凭证

**Enterprise Managed Users**  
通过你现有的目录，对每个 Vercel 和 **v0** 用户进行完整的生命周期控制

**在 AWS 上使用自有云**  
在你的 AWS 账户内运行应用和 Agent（目前处于 Private Beta 阶段）

## Vercel Passport：保持内部应用和 Agent 的内部性

我们构建的第一批 Agent 是供员工使用的内部工具，而非最终用户，这也是许多客户的常见起点。

Vercel 是将软件发布到网络的最快方式，但此前这意味着“内部”是每个项目上需要有人手动配置的设置。一旦有员工忘记将某个部署设为私有，就可能暴露对公司敏感系统和数据的访问权限。

**Vercel Passport** 默认将每个内部应用和 Agent 置于你的身份提供商之后，因此你可以通过 Okta、Microsoft Entra、Auth0 或任何其他兼容 OpenID Connect 的提供商来控制访问权限。

![配置一次 IdP 连接，Passport 便会自动将其应用于所有部署。](/images/posts/c2348f709c2b.jpg)

![配置一次 IdP 连接，Passport 便会自动将其应用于所有部署。](/images/posts/797c59deccbb.jpg)

应用和 Agent 的部署从创建那一刻起就是私有的，访问需通过员工身份进行身份验证，每项操作都可审计，管理员可集中设置策略，而无需依赖每个构建者自行正确配置。

## Vercel Connect：为 Agent 提供对系统的安全访问

Passport 管理谁能访问内部 Agent，但正如使用它们的员工一样，这些 Agent 也需要访问你的数据和系统。这种业务上下文使它们既有用又危险，因为大多数 Agent 被授予长期有效的凭证，存储在环境变量中，为 Agent 可能需要执行的所有操作而预配置。

![Vercel Connect 为应用和 Agent 提供对系统的安全、短期访问。](/images/posts/ca633375ebca.jpg)

![Vercel Connect 为应用和 Agent 提供对系统的安全、短期访问。](/images/posts/f9f3034b949e.jpg)

**Vercel Connect** 将 OAuth、OIDC 和密钥注入整合为一个产品，取代了那些静态密钥。Agent 不再存储密钥，而是在工作时请求短期凭证。Token 按任务授予，而非一次性永久有效，并在任务完成时过期。Connect 为 Agent 提供对 Slack、GitHub、Snowflake、Salesforce 和 Linear 的安全访问，以及可通过 OAuth 或 API 访问的其他系统。

## Enterprise Managed Users：从身份提供商管理每个构建者

当公司里的每个人都是构建者时，账户泛滥是一种无声的故障模式。席位似乎无人配置，访问权限在员工换组或离职后依然存在，整个平台上谁做了什么没有单一记录。

Enterprise Managed Users 为管理员提供对使用 Vercel 的每个构建者的完整生命周期控制。它基于 SAML SSO 和 Directory Sync 构建，通过你现有的目录自动配置席位，因此当你的身份提供商表示应该存在账户时，账户便立即创建；当目录移除用户时，访问权限也随之撤销。

基于组的访问控制、部署保护和 Vercel 上的 MFA 强制执行适用于整个组织，每项操作都会记录在单一的审计追踪中。你公司已运行的身份系统，无论是 Okta 还是其他 SAML 或 OIDC 提供商，现在也可以管理 Vercel 和 **v0**。

Enterprise Managed Users 目前处于 Private Beta 阶段。

### 通过 **v0** 和 Snowflake 实现数据民主化

**v0** 是 Vercel 的 AI 应用构建器。你描述需求，它便生成一个可运行的应用。**v0** 现已连接 Snowflake，因此你可以让任何人安全地构建基于数据仓库的数据应用，而无需提交工单。对 **v0** 和 Snowflake 的访问通过你的 IDP 控制，因此数据保持内部性。你决定谁获得席位，应用可直接部署到你的 Snowflake 账户。

![借助 v0 和 Snowflake，任何人都能安全地直接在数据仓库之上构建数据应用。](/images/posts/47f16a17f28d.jpg)

## 在 AWS 上使用自有云

对于大型企业来说，边界问题不仅限于私有部署。工作负载本身必须在他们控制的基础设施上运行，在安全团队拥有并审计的账户内。

通过 AWS 上的自有云（BYOC），你的计算资源、构建产物和数据都在你自己的 AWS 账户和 VPC 内运行，Vercel 在其上运行控制平面。你的应用和 Agent 访问私有后端和内部系统的方式，与 AWS 账户中的其他资源相同，你的源代码永远不会离开你的 CI。

AWS 上的 BYOC 意味着你的工程师保留 Vercel 的开发者体验，你的安全团队保留其已拥有的网络控制、审计证据和账户。自有云目前在 AWS 上处于 Private Beta 阶段。

## 以AI的速度安全交付

传统上，想法在安全审查中夭折是有充分理由的：数据泄露的风险不值得创新的潜在收益。Vercel Enterprise Apps and Agents 将安全控制内置于平台和工具本身，这意味着公司中的每个人都能以想法的速度交付应用和 Agent，而无需你的 CISO 夜不能寐。

当安全路径成为默认选项时，构建便是这样的：

- **大规模安全原型设计**：公司中的任何人都可以在受管控的轨道上使用 **v0** 进行原型设计，因此实验不再是安全例外，而成为探索工作的默认方式。
- **领域专家构建自己的工具**：最接近问题的人构建解决问题的方案，而不是提交工单并等待一个季度让别人来做。
- **直接通往生产环境的升级路径**：当原型证明其价值时，工程团队在同一平台上将其投入生产，而不是从头重建或直接禁止。

**大规模安全原型设计**：公司中的任何人都可以在受管控的轨道上使用 **v0** 进行原型设计，因此实验不再是安全例外，而成为探索工作的默认方式。

**领域专家构建自己的工具**：最接近问题的人构建解决问题的方案，而不是提交工单并等待一个季度让别人来做。

从原型到生产的直接路径：当原型证明其价值后，工程团队会在同一平台上将其投入生产，而不是从头重建或直接禁止。

## Link to heading常见问题

什么是面向企业应用和Agent（智能体）的Vercel？  
它是用于部署、治理和连接员工构建的应用和Agent（智能体）的平台，覆盖整个组织。它为贵公司发布的所有内容提供所有权、访问控制、身份和安全保障，无论是有人在v0中构建的原型，还是工程团队从零开始搭建的系统。该平台包括Vercel Passport、Vercel Connect、Enterprise Managed Users，以及在自己的AWS账户内运行的选项。

使用Passport、Connect和Enterprise Managed Users是否需要特定的框架？  
不需要。Passport、Connect和Enterprise Managed Users可治理部署到Vercel的任何内容，无论其构建方式如何。它们对现有项目的适用方式与对新项目相同。

支持哪些身份提供商和外部服务？  
Enterprise Managed Users支持Okta以及任何SAML或OIDC身份提供商。Vercel Connect为Agent（智能体）提供对Slack、GitHub、Snowflake、Salesforce和Linear的安全访问，以及通过OAuth或API可访问的任何其他服务。

目前有哪些功能可用？  
Vercel Passport和Vercel Connect处于Beta阶段。Enterprise Managed Users和AWS上的BYOC处于Private Beta阶段。

---

> 本文由AI自动翻译，原文链接：[Vercel for Enterprise Apps and Agents](https://vercel.com/blog/vercel-for-enterprise-apps-and-agents)
> 
> 翻译时间：2026-06-19 07:09
