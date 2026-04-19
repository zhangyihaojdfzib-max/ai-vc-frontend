---
title: Cloudflare邮件服务公开测试版上线，为AI智能体提供电子邮件基础设施
title_original: Email for agents - Cloudflare Email Service now in public beta
date: '2026-04-16'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/email-for-agents/
author: ''
summary: Cloudflare宣布其邮件服务进入公开测试阶段，旨在为AI智能体提供原生电子邮件通信能力。该服务包含邮件发送和邮件路由功能，允许开发者的应用程序和智能体直接收发邮件，无需管理复杂的SPF、DKIM等配置。通过集成Workers绑定、智能体SDK钩子、MCP服务器及开源参考应用等工具，开发者可以轻松构建基于邮件的智能体工作流，如客户支持、发票处理等。电子邮件因其普遍性和易访问性，正成为智能体与用户交互的核心界面。
categories:
- AI基础设施
tags:
- Cloudflare
- 电子邮件服务
- AI智能体
- 开发者工具
- 公开测试版
draft: false
translated_at: '2026-04-19T04:49:02.207143'
---

# Cloudflare 邮件服务：现已进入公开测试版，为您的智能体做好准备

2026-04-16

- Thomas Gauvin
- Eric Falcão

![](/images/posts/553db426f1f2.png)

电子邮件是世界上最易访问的界面。它无处不在。无需定制聊天应用，也无需为每个渠道定制 SDK。每个人都已拥有电子邮件地址，这意味着每个人都已经可以与您的应用程序或智能体进行交互。而您的智能体也可以与任何人交互。

如果您正在构建应用程序，您可能已经依赖电子邮件来处理注册、通知和发票。越来越普遍的是，不仅您的应用程序逻辑需要这个渠道，您的智能体同样需要。在我们的内测期间，我们与正在构建此类应用的开发者进行了交流：客户支持智能体、发票处理流程、账户验证流程、多智能体工作流。所有这些都构建在电子邮件之上。模式很清晰：电子邮件正在成为智能体的核心界面，而开发者需要为其量身定制的基础设施。

Cloudflare 邮件服务正是为此而生。通过**邮件路由**，您的应用程序或智能体可以接收电子邮件。通过**邮件发送**，您的智能体可以回复邮件或发送外发邮件，在完成工作时通知您的用户。借助开发者平台的其他部分，您可以构建一个完整的电子邮件客户端，并将**智能体 SDK** 的 `onEmail` 钩子作为原生功能。

今天，作为“智能体周”的一部分，Cloudflare 邮件服务进入**公开测试版**，允许任何应用程序和任何智能体发送电子邮件。我们同时完善了构建原生邮件智能体的工具包：

- **邮件发送绑定**，可从您的 Workers 和智能体 SDK 使用
- **全新的 Email MCP 服务器**
- **Wrangler CLI 邮件命令**
- **用于编码智能体的技能**
- **一个开源的智能体收件箱参考应用**

邮件发送绑定，可从您的 Workers 和智能体 SDK 使用

全新的 Email MCP 服务器

Wrangler CLI 邮件命令

用于编码智能体的技能

一个开源的智能体收件箱参考应用

## 邮件发送：现已进入公开测试版

邮件发送功能今天从内测升级到**公开测试版**。您现在可以直接通过 Workers 的原生绑定发送事务性电子邮件——无需 API 密钥，无需管理密钥。

```javascript
export default {
  async fetch(request, env, ctx) {
    await env.EMAIL.send({
      to: "[email protected]",
      from: "[email protected]",
      subject: "Your order has shipped",
      text: "Your order #1234 has shipped and is on its way."
    });
    return new Response("Email sent");
  },
};

```

或者，使用 REST API 以及我们的 TypeScript、Python 和 Go SDK，从任何平台、任何语言发送：

```javascript
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/email-service/send" \
   --header "Authorization: Bearer <API_TOKEN>" \
   --header "Content-Type: application/json" \
   --data '{
     "to": "[email protected]",
     "from": "[email protected]",
     "subject": "Your order has shipped",
     "text": "Your order #1234 has shipped and is on its way."
   }'

```

发送能真正到达收件箱的邮件通常意味着要处理 SPF、DKIM 和 DMARC 记录。当您将域名添加到邮件服务时，我们会自动配置所有这些。您的邮件将经过身份验证并送达，不会被标记为垃圾邮件。并且，由于邮件服务是构建在 Cloudflare 网络上的全球性服务，您的邮件可以在世界任何地方以低延迟送达。

结合多年来一直免费可用的**邮件路由**功能，您现在可以在单一平台内实现完整的双向电子邮件通信。接收邮件，在 Worker 中处理，然后回复，全程无需离开 Cloudflare。

关于邮件发送功能的完整深度介绍，请**参阅我们的生日周公告**。本文的其余部分将介绍邮件服务为智能体解锁了哪些可能性。

## 智能体 SDK：您的智能体原生支持邮件

用于在 Cloudflare 上构建智能体的智能体 SDK 已经拥有一个一流的 `onEmail` 钩子，用于接收和处理入站邮件。但在此之前，您的智能体只能同步回复，或向您 Cloudflare 账户的成员发送邮件。

有了邮件发送功能，这个限制就消失了。这正是聊天机器人和智能体之间的区别。

邮件智能体接收消息，在平台内协调工作，并异步响应。

聊天机器人要么即时响应，要么完全不响应。而智能体则按照自己的时间线进行思考、行动和沟通。借助邮件发送功能，您的智能体可以接收一条消息，花一小时处理数据，检查其他三个系统，然后回复一个完整的答案。它可以安排后续跟进。当检测到边缘情况时，它可以升级处理。它可以独立运作。换句话说：它实际上可以**工作**，而不仅仅是回答问题。

以下是一个拥有完整流程（接收、持久化、回复）的支持智能体的示例：

```javascript
import { Agent, routeAgentEmail } from "agents";
import { createAddressBasedEmailResolver, type AgentEmail } from "agents/email";
import PostalMime from "postal-mime";

export class SupportAgent extends Agent {
  async onEmail(email: AgentEmail) {
    const raw = await email.getRaw();
    const parsed = await PostalMime.parse(raw);

   // 在智能体状态中持久化
    this.setState({
      ...this.state,
      ticket: { from: email.from, subject: parsed.subject, body: parsed.text, messageId: parsed.messageId },
    });

    // 启动长时间运行的后台智能体任务
    // 或者将消息放入队列，由另一个 Worker 处理

    // 在此处回复，或在其他 Worker 处理程序（如队列处理程序）中回复
    await this.sendEmail({
      binding: this.env.EMAIL,
      fromName: "Support Agent",
      from: "[email protected]",
      to: this.state.ticket.from,
      inReplyTo: this.state.ticket.messageId,
      subject: `Re: ${this.state.ticket.subject}`,
      text: `Thanks for reaching out. We received your message about "${this.state.ticket.subject}" and will follow up shortly.`
    });
  }
}

export default {
  async email(message, env) {
    await routeAgentEmail(message, env, {
      resolver: createAddressBasedEmailResolver("SupportAgent"),
    });
  },
} satisfies ExportedHandler<Env>;
```

如果您不熟悉智能体 SDK 的邮件功能，以下是其底层工作原理。

每个智能体都从单个域名获得自己的身份。**基于地址的解析器**将 `[email protected]` 路由到“支持”智能体实例，将 `[email protected]` 路由到“销售”实例，依此类推。您无需配置单独的收件箱——路由功能已内置在地址中。您甚至可以使用子地址（`[email protected]`）来路由到不同的智能体命名空间和实例。

**状态在邮件之间持久化**。因为智能体由 Durable Objects 支持，调用 `this.setState()` 意味着您的智能体会记住会话历史、联系信息和跨会话的上下文。收件箱成为智能体的记忆，无需单独的数据库或向量存储。

**内置安全的回复路由**。当您的智能体发送邮件并期待回复时，您可以使用 HMAC-SHA256 对路由头进行签名，以便回复能路由回发送原始消息的精确智能体实例。这可以防止攻击者伪造头部将邮件路由到任意的智能体实例——这是大多数“智能体邮件”解决方案尚未解决的安全问题。

这就是团队在其他地方从头开始构建的完整邮件智能体流程：接收邮件、解析、分类、持久化状态、启动异步工作流、回复或升级处理——所有这些都在一个智能体类中完成，并部署在 Cloudflare 的全球网络上。

## 为您的智能体准备的邮件工具：MCP 服务器、Wrangler CLI 和技能

邮件服务不仅适用于在Cloudflare上运行的Agent（智能体）。Agent（智能体）可以运行在任何地方，无论是像Claude Code、Cursor或Copilot这样在本地或远程环境中运行的编码Agent（智能体），还是在容器或外部云中运行的生产环境Agent（智能体）。它们都需要从这些环境中发送邮件。我们推出了三项集成，让任何Agent（智能体）都能使用邮件服务，无论其运行在何处。

现在，邮件功能可通过**Cloudflare MCP服务器**获取，这是同一个由Code Mode驱动的服务器，它让Agent（智能体）能够访问整个Cloudflare API。通过这个MCP服务器，您的Agent（智能体）可以发现并调用邮件端点来发送和配置邮件。您只需一个简单的提示词即可发送邮件：

```unset
"Send me a notification email at [email protected] from my staging domain when the build completes"
```

对于在计算机或具有bash访问权限的沙箱中运行的Agent（智能体），Wrangler CLI解决了我们在Code Mode博客文章中讨论过的MCP上下文窗口问题——工具定义可能会消耗数万个Token，然后您的Agent（智能体）甚至才开始处理一条消息。使用Wrangler，您的Agent（智能体）可以近乎零上下文开销地启动，并通过`--help`命令按需发现功能。以下是您的Agent（智能体）如何通过Wrangler发送邮件：

```javascript
wrangler email send \
  --to "[email protected]" \
  --from "[email protected]" \
  --subject "Build completed" \
  --text "The build passed. Deployed to staging."

```

无论您为Agent（智能体）提供的是Cloudflare MCP还是Wrangler CLI，您的Agent（智能体）现在都能仅凭一个提示词就代表您发送邮件。

### 技能

我们还发布了**Cloudflare邮件服务技能**。它为您的Agent（智能体）提供完整的指导：配置Workers绑定、通过REST API或SDK发送邮件、使用邮件路由配置处理入站邮件、使用Agents SDK构建应用，以及通过Wrangler CLI或MCP管理邮件。它还涵盖了送达率的最佳实践，以及如何撰写能进入收件箱而非垃圾邮件的事务性邮件。将其放入您的项目中，您的编码Agent（智能体）就拥有了在Cloudflare上构建可用于生产环境的邮件功能所需的一切。

## 为邮件Agent（智能体）开源工具

在非公开测试期间，我们也尝试了邮件Agent（智能体）。很明显，您通常希望保留人工参与环节来审核邮件并查看Agent（智能体）正在做什么。**实现这一点的最佳方式是拥有一个内置了Agent（智能体）自动化功能的、功能齐全的邮件客户端。**

这就是我们构建**Agentic Inbox**的原因：这是一个参考应用程序，具备完整的对话线程、邮件渲染、接收和存储邮件及其附件以及自动回复邮件的功能。它内置了一个专用的MCP服务器，因此外部Agent（智能体）可以在从您的Agentic Inbox发送之前，为您起草邮件以供审阅。

我们将**Agentic Inbox开源**，作为一个参考应用程序，展示如何使用邮件路由处理入站邮件、邮件发送处理出站邮件、Workers AI进行分类、R2存储附件，以及Agents SDK实现有状态的Agent（智能体）逻辑，来构建一个完整的邮件应用程序。您今天就可以一键部署它，获得一个完整的收件箱、邮件客户端和用于处理邮件的Agent（智能体）。

我们希望邮件Agent（智能体）工具是可组合和可重用的。与其让每个团队都重建相同的“接收-分类-回复”流程，不如从这个参考应用程序开始。复刻它、扩展它，将其作为构建适合您工作流程的自有邮件Agent（智能体）的起点。

## 立即试用

邮件是世界上最重要工作流程的承载地，但对于Agent（智能体）来说，它常常是一个难以触及的渠道。随着**邮件发送**功能进入公开测试阶段，Cloudflare邮件服务成为一个完整的双向通信平台，使收件箱成为您Agent（智能体）的一流界面。

无论您是在构建一个在客户收件箱中与客户会面的支持Agent（智能体），还是一个让您的团队实时了解进度的后台进程，您的Agent（智能体）现在都有了在全球范围内无缝通信的方式。收件箱不再是孤岛。现在，它是您的Agent（智能体）提供帮助的又一个场所。

- 在Cloudflare仪表板中试用**邮件发送**
- 阅读**邮件服务文档**
- 遵循**Agents SDK邮件文档**
- 查看**邮件服务MCP服务器**和**技能**
- 部署开源参考应用

在Cloudflare仪表板中试用**邮件发送**

阅读**邮件服务文档**

遵循**Agents SDK邮件文档**

查看**邮件服务MCP服务器**和**技能**

部署开源参考应用

## 在Cloudflare TV上观看

---

> 本文由AI自动翻译，原文链接：[Email for agents - Cloudflare Email Service now in public beta](https://blog.cloudflare.com/email-for-agents/)
> 
> 翻译时间：2026-04-19 04:49
