---
title: Cloudflare CASB集成Claude合规API，强化AI安全监控
title_original: Announcing Claude Compliance API support with Cloudflare CASB
date: '2026-05-21'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/casb-anthropic-integration/
author: ''
summary: Cloudflare宣布将其云访问安全代理（CASB）扩展至支持Anthropic的Claude合规API，使安全和合规团队无需端点代理即可在Cloudflare仪表板中直接监控Claude的使用情况。该集成解决了AI工具快速普及带来的安全治理滞后问题，覆盖项目共享、文件上传、聊天消息等场景的敏感数据检测与错误配置扫描。结合AI
  Gateway、Gateway/数据丢失防护及Access等工具，Cloudflare为AI应用提供从API调用到静态数据的全生命周期安全保护。
categories:
- AI基础设施
tags:
- Cloudflare
- Claude合规API
- AI安全
- CASB
- 企业治理
draft: false
translated_at: '2026-05-22T06:06:06.750128'
---

# 宣布通过 Cloudflare CASB 支持 Claude 合规 API

2026-05-21

- Abe Carryl

![](/images/posts/a3450dd1e11a.png)

今天，我们将 Cloudflare 的云访问安全代理（CASB）扩展以支持 Claude 合规 API。安全和合规团队现在可以直接在 Cloudflare 仪表板中监控 Claude 的使用情况。无需端点代理。

企业安全团队长期以来一直难以了解用户如何与已批准和未批准的应用程序交互。AI 应用的快速普及使这一问题更加困难。员工在这些新的交互面上花费了大量时间，并且他们的交互方式与传统 SaaS 不同：用户上传文件、分享自由格式的提示词，而提供商生成的内容可能包含敏感数据。

Cloudflare CASB 有助于解决这一问题。一次 API 集成即可让您获得对组织使用的应用程序的带外可见性和控制。此集成建立在我们现有的 AI 治理支持之上，将覆盖范围扩展到安全团队现在管理的最常见工具。

## 安全采用 AI 的快速路径

AI 的采用已经超越了安全治理。虽然 IT 和安全团队竞相启用 AI 工具以提高生产力，但控制措施却滞后了。如今，大多数组织都在部分可见性的情况下运作：他们可能在网络层阻止未经授权的 AI 工具，但无法看到已批准工具内部发生了什么。

这一点很重要，因为 AI 工具不像传统的 SaaS 应用程序。它们是对话式的、持久性的，并通过 API 和 Agent 框架深度集成到工作流程中。员工可能会将客户数据粘贴到提示词中。开发者可能会意外共享 API 密钥并数月不轮换。AI 应用程序可能会生成包含公司机密的内容。这些行为中的每一个都会产生传统安全工具无法检测到的合规风险。

组织正在快速采用 AI，但这些工具需要不同的安全模型。它们不仅读取数据；它们还生成数据、对数据采取行动，并在单个工作流程中连接到多个记录系统。安全需要覆盖完整的生命周期：从应用程序如何调用 API，到它处理哪些数据，再到这些数据在静态时存储在哪里。Cloudflare 为组织提供了在工作流程的每个节点执行此操作的工具：

- Cloudflare AI Gateway 位于您的应用程序和 Anthropic 等 AI 提供商之间，为您提供对请求、Token 消耗和模型性能的可观测性。这允许管理员实施速率限制、缓存响应并做出细粒度的路由决策。
- Cloudflare Gateway 和数据丢失防护检查 AI 流量中的敏感数据，在包含客户个人身份信息或机密材料的提示词到达模型之前将其阻止。
- Cloudflare Access 与 MCP 服务器门户将 Agent 与企业工具之间的连接集中到单个受保护端点之后。管理员控制哪些用户和 Agent 可以访问哪些系统，并且每个请求都会被记录以进行审计。
- Cloudflare CASB 现在将这种统一的方法扩展到 Claude 内部的静态数据，无需端点代理即可扫描错误配置和敏感数据。

这些功能在同一硬件上并行运行，使每项服务既可组合又可编程。更重要的是，这意味着流量永远不会通过多个供应商或云进行回程以进行安全保护。

## 通过 Cloudflare CASB 获得更好的洞察和控制

Cloudflare CASB 帮助组织通过轻量级 API 集成连接、扫描和监控第三方 SaaS 应用程序，以发现错误配置、不当数据共享和其他安全风险。组织可以重新获得对其不断增长的 SaaS 应用投资的可见性和控制。

随着企业大规模部署 Claude，安全和合规团队需要像对待其技术栈中每个其他企业应用程序一样，对 Claude 的使用情况拥有相同的可见性。Anthropic 认识到了这一差距，并构建了 Claude 合规 API，使企业能够以编程方式访问有关其 Claude 组织、工作区和使用的安全相关数据。

Cloudflare CASB 现在使用此端点来呈现可操作的安全发现，而无需内联流量检查或端点代理。

### Claude 合规 API 呈现的内容

通过此集成，Cloudflare One 客户可以使用他们已经依赖的检测和修复工作流程来监控 Claude Enterprise 活动。Cloudflare CASB 通过合规 API 连接到 Claude 并扫描安全发现。

从今天开始，Cloudflare 支持以下资产的安全发现：

- 项目：检测跨组织或部分用户和组共享的项目
- 项目附件：添加到项目中违反 DLP 策略的文件和文档
- 聊天文件：用户上传和提供商生成的文件，违反 DLP 策略
- 聊天消息：用户提示词和提供商响应，违反 DLP 策略
- 工件：提供商生成的文档和文件，违反 DLP 策略

这些发现直接出现在 Cloudflare 仪表板中，与来自其他 SaaS 应用程序的态势和内容发现一起显示。发现按类别分组并按严重级别排序。安全团队可以使用与 Microsoft 365、Google Workspace 或 Salesforce 相同的工作流程来分类、分配和修复 Claude 特定的风险。

### 支持 Claude Enterprise 和 Claude Platform

对于 Claude Enterprise，CASB 呈现合规数据，例如组织、项目、聊天和角色。它还通过专用的只读端点检索对话内容，包括消息和上传的文件，以防止数据丢失。

对于 Claude Platform，CASB 将继续呈现成员和工作区变更、API 密钥创建以及文件创建或下载事件。在不久的将来，我们将添加对活动源的支持。

CASB 将发现转化为行动。在 Claude 中检测到的安全发现，例如用户上传包含敏感数据的文件，可以在几分钟内成为 Gateway 策略。您可以使用 Gateway 阻止特定用户向 Claude 上传内容，完全限制对应用程序的访问，或在问题解决之前限制功能。这通过将 CASB 发现与 Cloudflare 现有的内联策略引擎相结合，使安全团队从可见性转向行动。

### 开始使用

要启用 Claude 合规 API 集成：

1. 确保您拥有Claude企业版账户。
2. 向Claude申请您组织的Compliance API访问权限。
3. 在Cloudflare控制面板中，进入Zero Trust > Integrations > Cloud & SaaS。
4. 选择Add Integration > Anthropic，并输入您的Compliance API密钥。
5. 如果您希望扫描上传文件中的敏感数据，请配置DLP策略。

确保您拥有Claude企业版账户。

向Claude申请您组织的Compliance API访问权限。

在Cloudflare控制面板中，进入Zero Trust > Integrations > Cloud & SaaS。

选择Add Integration > Anthropic，并输入您的Compliance API密钥。

如果您希望扫描上传文件中的敏感数据，请配置DLP策略。

集成将立即开始扫描，并在几分钟内在控制面板中显示结果。

对于新Cloudflare客户，您可以注册并免费使用前两个集成。现有客户可以直接在控制面板中启用集成。

## 后续计划

我们正在持续扩展针对AI工具的CASB覆盖范围，随着各提供商发布新的企业安全API。同时，我们也在深化CASB内部的集成，使客户能够创建自定义发现结果并构建自动修复安全发现的工作流程。

向Agent（智能体）化AI的转变已经到来，我们相信帮助组织安全采用这一技术的最佳方式是提供一个统一的平台来构建、部署和管理Agent（智能体）。要获取最新信息，请查看我们的开发者文档或订阅以自动接收更新。

---

> 本文由AI自动翻译，原文链接：[Announcing Claude Compliance API support with Cloudflare CASB](https://blog.cloudflare.com/casb-anthropic-integration/)
> 
> 翻译时间：2026-05-22 06:06
