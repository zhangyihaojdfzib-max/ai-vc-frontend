---
title: LangSmith Fleet发布：两种Agent授权模式详解
title_original: Two different types of agent authorization
date: '2026-03-23'
source: LangChain Blog
source_url: https://blog.langchain.com/two-different-types-of-agent-authorization/
author: ''
summary: 本文介绍了LangSmith Fleet推出的两种Agent授权机制：代表用户模式和OpenClaw模式。代表用户模式下，Agent使用最终用户的凭证进行操作，确保数据隔离与隐私安全；而OpenClaw模式下，Agent拥有固定的专用凭证，适用于公开共享场景。文章还阐述了两种模式对应的产品形态（助手与Claw）、支持的渠道以及人工介入的必要性，并通过实际案例说明了不同授权模式的应用场景。
categories:
- AI产品
tags:
- 智能体
- LangSmith
- Agent授权
- AI安全
- 人机协作
draft: false
translated_at: '2026-03-24T04:50:00.352844'
---

我们上周推出了 **LangSmith Fleet**，作为构建、使用和管理Agent（智能体）的一种方式。本次发布的一个关键部分是引入了两种不同类型的Agent授权机制。

Agent授权指的是Agent被允许执行哪些操作。当Agent调用Slack工具时——在拉取数据之前，它以谁的身份进行**身份验证**？

## 代表用户模式

直到最近，大多数人设想的Agent标准运作方式是“代表”某个用户行事。

假设有一个拥有Notion和Rippling访问权限的入职Agent。当Alice与之交互时，它应该能够在Rippling中查找关于Alice的信息，并查看Alice有权访问的所有Notion页面。Alice不应该能够使用这个入职Agent在Rippling中查找关于Bob的任何私人信息，或者查看Bob可能拥有的任何私人Notion页面。当Bob使用这个入职Agent时，他应该能够访问自己在Rippling中的所有信息以及Notion中的所有私人页面，但不能访问Alice的。

为了实现这一点，你需要几样东西。你需要一种方法来知道谁在使用Agent——是Alice还是Bob？然后，你需要将这些用户ID映射到一些在运行时传递给工具的认证凭证。

## 随后出现了OpenClaw模式

在OpenClaw出现之前，“代表用户”是人们设想Agent的主要方式。有了OpenClaw，Alice可以创建一个Agent。可能只有她自己会使用这个Agent（在这种情况下，这种授权区别就不太重要）。但也可能她通过不同的渠道（如短信、电子邮件或Twitter）将其开放给其他人使用。

当其他人与该Agent交互时，它使用的不是最终用户的凭证——而是使用Alice赋予它的授权。

有时这可能是Alice自己的凭证，但这可能并不理想。如果Agent拥有Alice的凭证，它就可以查看Alice有权访问的Notion中的所有内容。这可能包括她不想让别人通过Agent询问的私人文档。

这导致人们专门为Agent在Notion、Rippling等工具中创建专用账户，以便控制Agent能访问什么。每个与该Agent交互的人实际上都将使用同一套凭证。

## LangSmith Fleet

在推出LangSmith Fleet时，我们发现人们需要这两种类型的Agent。有时他们想创建一个Agent并让他人使用自己的凭证来使用它；有时他们希望该Agent拥有自己固定的一套凭证。我们添加了两种不同类型的Agent，分别对应这两种授权类型：

*   **助手**：以“代表”其最终用户的身份行事
*   **Claw**：拥有自己固定的凭证

![Agent identity](/images/posts/8d35662d67bb.png)

我们还引入了**渠道**（初始支持Slack、Gmail、Outlook和Teams）和Agent**共享**的概念。助手和Claw支持不同的渠道。为了让助手能够被共享，我们必须建立该渠道中最终用户（例如他们的Slack用户ID）与其LangSmith ID之间的映射关系。因此，目前助手仅在我们支持这种映射的部分渠道中可用。

渠道和这些不同的授权类型也凸显了**人工介入**的必要性。如果你正在创建一个拥有固定凭证集的Agent，并通过某个渠道将其公开，你就是在开放它以各种方式被使用。如果该Agent可以执行可能具有潜在危险或敏感性的操作，你可能需要使用一些“人工介入”的防护措施来确保这些操作受到控制。

## 示例

为了具体说明，让我们看看我们创建的几个真实Agent及其授权类型。

**入职Agent**：助手。拥有Slack和Notion的访问权限，并在Slack中公开。使用最终用户的Slack和Notion凭证。

**邮件Agent**：Claw。该Agent响应收到的电子邮件。无论谁发送邮件，该Agent都会查看我的日历以确定会议可用性，并尝试代表我进行回复。发送电子邮件和日历邀请的操作受到人工介入防护措施的控制。

**产品Agent**：Claw。该Agent监控竞争对手并协助处理产品问题和路线图。它拥有自己的Notion账户，并通过一个自定义的Slack机器人公开。

## 未来工作

我们很高兴能在LangSmith Fleet中推出这两种不同的Agent类型。然而，我们认为这只是Agent授权的开始。请阅读WorkOS的这篇博客，了解一些潜在的未来方向。

我们也期待在后续工作中引入更细粒度的**记忆权限**。根据Agent类型（助手或Claw）的不同，你可能希望以不同的方式处理记忆。例如，你可能不希望一个助手记住关于Alice的敏感信息，并在与Bob的聊天中使用这些信息。目前，我们通过访问权限来管理这一点。当你共享一个Agent时，你可以选择其他用户是否可以编辑它，包括其记忆。未来，我们将引入用户特定的记忆。

立即试用LangSmith Fleet。

### 加入我们的通讯

来自LangChain团队和社区的更新

正在处理您的申请...

成功！请检查您的收件箱并点击链接确认订阅。

抱歉，出错了。请重试。

---

> 本文由AI自动翻译，原文链接：[Two different types of agent authorization](https://blog.langchain.com/two-different-types-of-agent-authorization/)
> 
> 翻译时间：2026-03-24 04:50
