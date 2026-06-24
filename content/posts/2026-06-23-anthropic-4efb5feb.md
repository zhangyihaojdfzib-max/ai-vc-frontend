---
title: 推出Claude Tag：团队协作的AI新方式
title_original: Introducing Claude Tag
date: '2026-06-23'
source: Anthropic
source_url: https://www.anthropic.com/news/introducing-claude-tag
author: ''
summary: Anthropic推出Claude Tag，一种让Claude以团队成员身份加入Slack频道的新协作方式。用户可通过@Claude委派任务，Claude能访问工具、数据和代码库，并随时间学习上下文、主动更新信息、异步工作。该功能面向Claude
  Enterprise和Team客户提供Beta版本，已在Anthropic内部广泛使用，产品团队65%的代码由Claude Tag创建。
categories:
- AI产品
tags:
- Claude Tag
- 团队协作
- Slack集成
- AI代理
- Anthropic
draft: false
translated_at: '2026-06-24T06:08:19.841629'
---

# 推出 Claude Tag

![推出 Claude Tag](/images/posts/53d82823e182.jpg)

Claude Tag 是团队与 Claude 协作的全新方式。

我们从 Slack 开始，Claude 可以以团队成员的身份加入其中。授予 Claude 对选定频道的访问权限，并将其连接到您选择的任何工具、数据甚至代码库。然后，频道中的任何人都可以@Claude 并委派任务给它，同时专注于其他工作。Claude 通过记住所在频道的相关信息来构建上下文，并可以规划未来要完成的任务。

我们将 Claude Tag 视为 Claude Code 演进的开端：它使模型更加主动，并且能更好地与整个团队协作。@Claude 现在已成为 Anthropic 内部完成任务的主要方式之一。如今，我们产品团队 65% 的代码是由内部版本的 Claude Tag 创建的。同样的模式现已远远超出工程领域——我们正在@Claude 来追踪产品指标和数据、处理支持工单，甚至帮助查找棘手 Bug 的根本原因。

我们在 Slack 上推出 Claude Tag，因为它是团队与 AI 之间协作工作的天然场所，也是 Anthropic 大部分日常工作已经发生的地方。今天，它面向 Claude Enterprise 和 Team 客户提供 Beta 版本。我们的目标是更广泛地扩展其可用范围，以便团队可以在他们工作的许多其他场所@Claude。

## 与 @Claude 协作

如果您之前使用过 Claude Code 或 Cowork，那么 Claude Tag 会让您感到熟悉。用简单的语言@Claude 提出请求，它会将任务分解为多个阶段，然后使用其可访问的工具依次完成。完成后，它会在 Slack 线程中回复所创建的内容。

但@Claude 带来了一些新的优势：

**@Claude 是多玩家模式。** 在给定的 Slack 频道中，只有一个 Claude 与所有人互动。这意味着任何人都可以看到它在做什么，并且可以从前一个人离开的地方继续对话。这使得@Claude 与在单个聊天或单个任务中工作截然不同——它更像是与队友协作互动。

**@Claude 会随时间学习。** 随着 Claude 跟随其频道，它会构建更多关于工作的上下文。这意味着用户无需一遍又一遍地从零开始向它解释事情。如果获得许可，Claude 甚至可以自动从其他 Slack 频道和数据源学习。（它不会从私密频道获取信息。）这赋予了它提供最佳工作成果所需的隐性知识。

**@Claude 会主动行动。** 如果启用了"环境"行为，Claude 会主动向您更新它认为您可能需要了解的任何信息。它会标记来自其所在频道和所连接工具的相关信息，并跟进那些已沉寂但尚未解决的线程或任务。

**@Claude 可异步工作。** 给 Claude 设定一个任务，您可以在它工作时专注于其他优先事项。它还可以为自己安排任务，自主地花费数小时或数天推进项目。我们发现这在 Anthropic 内部特别有用：现在我们将更多时间用于并行地向多个 Claude 委派任务。

您也可以向 Claude 发送直接消息：它会使用您设置的个人工具和连接器私下回复。

## 开始使用

我们为团队和组织设计了 Claude Tag：@Claude 对敏感数据和任务特定工具的访问权限可以得到非常严格的控制。

要开始使用，系统管理员需要指定模型应在哪些频道中访问哪些工具和信息。可以将其视为为不同用途创建独立的 Claude 身份：包括其记忆在内的一切都将限定在管理员定义的频道范围内。例如，为销售工作设置的模型不会将记忆传递给为工程工作设置的模型；也不会让工程师访问任何销售数据或工具。有关配置访问权限的更多信息，请参见此处。

权限设置完成后，每个人都可以立即开始@。管理员可以设置 Token 消耗限制（针对组织和个人频道），并且可以查看 @Claude 所做的一切日志，以及每个任务的请求者。

如果您是 Claude Enterprise 或 Team 客户，从今天起您可以访问 Claude Tag 的 Beta 版本。要开始使用，请访问此处并按照以下四个步骤操作：

1. 将 Claude Tag 与您的 Slack 工作区配对
2. 授予 Claude 对您工具的访问权限
3. 设置您组织的月度消耗限制
4. 在私密频道中测试 Claude 以确认其正常工作。

Claude Tag 取代了现有的 Slack 中的 Claude 应用。要迁移，管理员可以在 30 天内选择加入。我们正在向符合条件的 Enterprise 和 Team 组织发放启动信用额度，以便整个公司都可以试用。

Claude Tag 与 Opus 4.8 配合使用。您可以阅读我们的文档和产品页面。

## 相关内容

### Anthropic 开设首尔办事处并宣布在韩国 AI 生态系统中的新合作伙伴关系

### 关于美国政府指令暂停访问 Fable 5 和 Mythos 5 的声明

美国政府已发布出口管制指令，暂停对 Fable 5 和 Mythos 5 的所有访问。

### 首次 Anthropic 公开记录的结果

---

> 本文由AI自动翻译，原文链接：[Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag)
> 
> 翻译时间：2026-06-24 06:08
