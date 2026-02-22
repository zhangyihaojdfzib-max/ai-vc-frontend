---
title: 我们如何构建Agent Builder的记忆系统
title_original: How we built Agent Builder’s memory system
date: '2026-02-22'
source: LangChain Blog
source_url: https://blog.langchain.com/how-we-built-agent-builders-memory-system/
author: ''
summary: 本文介绍了LangSmith Agent Builder如何构建其记忆系统。文章阐述了优先考虑记忆系统的原因，即Agent需要重复执行特定任务，记忆能避免用户在不同会话中重复指令。系统将记忆表示为文件集合，利用模型擅长处理文件系统的特点，通过虚拟文件系统存储在数据库中。记忆类型参考了COALA论文的分类，包括程序性、语义和情景记忆，并采用行业标准文件格式进行管理。
categories:
- AI产品
tags:
- 智能体
- 记忆系统
- 无代码开发
- LangSmith
- AI基础设施
draft: false
translated_at: '2026-02-22T04:32:47.427272'
---

我们上个月推出了**LangSmith Agent Builder**，作为构建Agent（智能体）的无代码方式。Agent Builder的一个关键组成部分是其记忆系统。在本文中，我们将阐述我们优先考虑记忆系统的理由、构建该系统的技术细节、构建记忆系统过程中的经验教训、记忆系统带来的可能性，并讨论未来的工作。

## 什么是 LangSmith Agent Builder

**LangSmith Agent Builder** 是一个无代码的Agent构建器。它建立在 **Deep Agents** 框架之上。它是一个托管式网络解决方案，主要面向**技术门槛较低**的公民开发者。在 LangSmith Agent Builder 中，构建者将创建一个Agent来自动化特定的工作流程或日常工作中的一部分。例如，可以构建一个**电子邮件助手**、一个**文档助手**等。

![使用自然语言创建Agent](/images/posts/4462eda3e2f3.png)

早期，我们就有意识地选择将记忆作为平台的一个优先组成部分。这并非一个显而易见的选择——大多数AI产品最初发布时没有任何形式的记忆，甚至添加记忆功能也**尚未像某些人预期的那样彻底改变产品**。我们优先考虑它的原因在于我们用户的使用模式。

与 ChatGPT、Claude 或 Cursor 不同，LangSmith Agent Builder 不是一个通用目的的Agent。相反，它专门设计用于让构建者为特定任务定制Agent。在通用Agent中，用户执行的任务多种多样且可能完全无关，因此从一次与Agent的会话中学到的东西可能与下一次无关。而当 LangSmith Agent 执行任务时，它是在一遍又一遍地执行相同的任务。从一次会话中获得的经验教训，在下次会话中适用的比例要高得多。事实上，如果没有记忆功能，用户体验会很糟糕——那将意味着你必须在不同的会话中向Agent一遍又一遍地重复自己。

在思考记忆对 LangSmith Agent 究竟意味着什么时，我们参考了一个第三方对Agent记忆的定义。**COALA 论文**将Agent的记忆分为三类：

- **程序性记忆**：可应用于工作记忆以决定Agent行为的一套规则
- **语义记忆**：关于世界的事实
- **情景记忆**：Agent过去行为的序列

![COALA 记忆示意图](/images/posts/6e029143670f.png)

## 我们如何构建记忆系统

我们在 Agent Builder 中将记忆表示为一组文件。这是一个有意的选择，旨在利用**模型擅长使用文件系统**这一事实。通过这种方式，我们可以轻松地让Agent读取和修改其记忆，而无需为其提供专门的工具——我们只需授予它访问文件系统的权限！

在可能的情况下，我们尽量使用行业标准。我们使用 **AGENTS.md** 来定义Agent的核心指令集。我们使用 **agent skills** 来为Agent提供针对特定任务的专门指令。目前没有子Agent的标准，但我们采用了**类似于 Claude Code 的格式**。对于 **MCP** 访问，我们使用自定义的 **tools.json** 文件。我们使用自定义的 tools.json 文件而非标准的 mcp.json 的原因是，我们希望允许用户只向Agent提供 MCP 服务器中工具的一个子集，以避免上下文溢出。

![记忆 = 文件系统](/images/posts/2e201d2d2105.png)

实际上，我们并没有使用真实的文件系统来存储这些文件。相反，我们将它们存储在 Postgres 数据库中，并以文件系统的形式暴露给Agent。这样做是因为LLM（大语言模型）非常擅长处理文件系统，但从基础设施的角度来看，使用数据库更简单、更高效。这个“虚拟文件系统”**由 DeepAgents 原生支持**——并且是完全可插拔的，因此你可以使用任何你想要的存储层（S3、MySQL 等）。

我们还允许用户（以及Agent自身）向Agent的记忆文件夹写入其他文件。这些文件也可以包含任意知识，Agent在运行时可以参考。Agent会在工作过程中，在“热路径”上编辑这些文件。

之所以能够在不编写任何代码或任何领域特定语言的情况下构建复杂的Agent，是因为我们在底层使用了像 Deep Agents 这样的通用Agent框架。Deep Agents 抽象掉了许多复杂的上下文工程（如**摘要**、**工具调用卸载**和**规划**），让你可以通过相对简单的配置来引导你的Agent。

这些文件很好地映射到了 COALA 论文中定义的记忆类型。程序性记忆——驱动核心Agent指令的部分——是 **AGENTS.md** 和 **tools.json**。语义记忆是 agent skills 和其他知识文件。唯一缺失的记忆类型是情景记忆，我们认为对于这类Agent来说，它不如其他两种类型重要。

### 文件系统中Agent记忆的样貌

我们可以看看我们内部一直在使用的一个真实Agent——一个基于 LangSmith Agent Builder 构建的 LinkedIn 招聘人员。

- **AGENTS.md**：定义了核心Agent指令
- **subagents/**：只定义了一个子Agent `linkedin_search_worker`：在主Agent校准搜索后，它将启动这个子Agent来寻找约 50 名候选人。
- **tools.json**：定义了一个可以访问 LinkedIn 搜索工具的 MCP 服务器
- 目前记忆中还有另外 3 个文件，代表不同候选人的职位描述。随着我们与Agent一起进行这些搜索，它已经更新并维护了这些职位描述。

![Agent Builder 记忆文件系统](/images/posts/3e76e24de7a9.png)

### 记忆编辑如何工作：一个具体例子

为了让记忆的工作原理更具体，我们可以通过一个示例来逐步说明。

**开始：**

你从一个简单的 **AGENTS.md** 开始：

```
Summarize meeting notes.
```

**第一周：**

Agent生成了段落摘要。你纠正它："使用项目符号列表代替。" Agent将 **AGENTS.md** 编辑为：

```
# Formatting Preferences
User prefers bullet points for summaries, not paragraphs.
```

**第二周：**

你要求Agent总结另一个会议。它读取其记忆并自动使用项目符号列表。无需提醒。在此会话期间，你要求它："在末尾单独提取行动项。" 记忆更新为：

```
# Formatting Preferences
User prefers bullet points for summaries, not paragraphs.
Extract action items in separate section at end.
```

**第四周：**

两种模式都自动应用。随着新的边缘情况出现，你继续添加改进。

**第三个月：**

Agent的记忆包括：

- 针对不同文档类型的格式偏好
- 领域特定术语
- "行动项"、"决策"和"讨论要点"之间的区别
- 频繁参会者的姓名和角色
- 会议类型处理（工程会议 vs. 规划会议 vs. 客户会议）
- 使用过程中积累的边缘情况修正

记忆文件可能看起来像这样：

```
# Meeting Summary Preferences

## Format
- Use bullet points, not paragraphs
- Extract action items in separate section at end
- Use past tense for decisions
- Include timestamp at top

## Meeting Types
- Engineering meetings: highlight technical decisions and rationale
- Planning meetings: emphasize priorities and timelines
- Customer meetings: redact sensitive information
- Short meetings (<10 min): just key points

## People
- Sarah Chen (Engineering Lead) - focus on technical details
- Mike Rodriguez (PM) - focus on business impact
...
```

这个 **AGENTS.md** 是通过修正而非预先编写文档的方式自我构建起来的。我们迭代地达成了一个详细程度恰当的Agent规范，而用户从未手动更改过 **AGENTS.md**。

## 构建此记忆系统的经验教训

在此过程中，我们学到了几个经验教训。

**最困难的部分是提示词设计**

构建一个能记住事情的Agent，最困难的部分是提示词设计。在几乎所有Agent表现不佳的情况下，解决方案都是改进提示词。通过这种方式解决的问题示例包括：

- Agent（智能体）在该记住的时候没有记住
- Agent（智能体）在不该记住的时候却记住了
- Agent（智能体）向 `AGENTS.md` 文件写入过多内容，而非写入技能文件
- Agent（智能体）不知道技能文件的正确格式
- … 以及更多问题

我们曾安排一名成员全职负责针对记忆的提示词优化（这在团队中占了相当大的比例）。

**验证文件类型**

部分文件需要遵循特定的模式（例如 `tools.json` 需要包含有效的 MCP 服务器信息，技能文件需要包含正确的前置元数据等）。我们发现 Agent Builder 有时会忘记这些要求，从而生成无效文件。为此，我们增加了一个步骤来显式验证这些自定义结构，如果验证失败，则将错误信息反馈给 LLM（大语言模型），而不是直接提交文件。

**Agent（智能体）擅长向文件添加内容，但不擅长压缩整理**

Agent（智能体）在工作时会编辑自己的记忆。它们很擅长向文件添加具体内容。然而，它们不擅长的一点是，不知道何时应该压缩整理已学到的内容。例如：我的电子邮件助手一度开始列出所有应忽略其冷推广邮件的具体供应商名单，而不是更新自身以忽略所有冷推广邮件。

**作为终端用户，显式提示有时仍然有用**

即使 Agent（智能体）能够在工作中更新其记忆，我们（作为终端用户）发现，在某些情况下，显式提示 Agent（智能体）管理其记忆仍然很有用。一种情况是在其工作结束时，让它回顾对话并更新记忆，以补充可能遗漏的内容。另一种情况是提示它压缩记忆，以解决它记住了具体案例但未能进行归纳概括的问题。

**人在回路**

我们对记忆的所有编辑都采用“人在回路”机制——即在更新前需要获得明确的人工批准。这主要是为了尽量减少提示词注入的潜在攻击风险。我们也为用户提供了关闭此功能（“yolo 模式”）的选项，适用于那些不担心此类风险的情况。

## **这带来了什么**

除了更好的产品体验，以这种方式表示记忆还实现了许多可能性。

**无代码体验**

无代码构建器的一个问题是，它们要求你学习一种不熟悉的 DSL（领域特定语言），而这种语言在处理复杂问题时扩展性不佳。通过将 Agent（智能体）表示为 Markdown 和 JSON 文件，Agent（智能体）现在以一种（a）大多数技术背景较浅的人所熟悉，（b）更具扩展性的格式存在。

**更好的 Agent（智能体）构建**

记忆实际上能带来更好的 Agent（智能体）构建体验。构建 Agent（智能体）是一个高度迭代的过程——很大程度上是因为在尝试之前，你无法预知 Agent（智能体）会做什么。记忆让迭代变得更容易，因为你不必每次都手动更新 Agent（智能体）配置，只需用自然语言给出反馈，它就会自行更新。

**可移植的 Agent（智能体）**

文件非常易于移植！这使你能够轻松地将 Agent Builder 中构建的 Agent（智能体）移植到其他框架中（只要它们使用相同的文件约定）。为此，我们尽可能多地采用了标准约定。例如，我们希望让在 Deep Agents CLI 中使用 Agent Builder 构建的 Agent（智能体）变得容易。或者完全移植到其他 Agent（智能体）框架，如 Claude Code 或 OpenCode。

## **未来方向**

我们希望在发布前实现许多记忆方面的改进，但由于时间或信心不足而未能完成。

**情景记忆**

Agent Builder 目前缺少的 COALA 记忆类型是情景记忆：即 Agent（智能体）过去行为的序列。我们计划通过将之前的对话作为文件暴露在文件系统中，供 Agent（智能体）交互来实现这一点。

**后台记忆处理**

目前，所有记忆更新都发生在“热路径”上；也就是说，在 Agent（智能体）运行时进行。我们希望增加一个在后台运行的进程（可能是一个定时任务，每天运行一次左右），来反思所有对话并更新记忆。我们认为这将捕捉到 Agent（智能体）在当下未能识别的项目，并且对于将具体学习内容归纳概括特别有用。

![在热路径中](/images/posts/f31eba089986.png)

**`/remember` 命令**

我们希望提供一个显式的 `/remember` 命令，以便你可以提示 Agent（智能体）回顾对话并更新其记忆。我们发现偶尔这样做会带来很大好处，因此希望使其更容易操作并更受鼓励。

**语义搜索**

虽然能够使用 `glob` 和 `grep` 搜索记忆是一个很好的起点，但在某些情况下，允许 Agent（智能体）对其记忆进行语义搜索会带来一些收益。

**不同层级的记忆**

目前，所有记忆都是针对特定 Agent（智能体）的。我们没有用户级或组织级记忆的概念。我们计划通过向 Agent（智能体）暴露代表这些记忆类型的特定目录，并提示 Agent（智能体）相应地使用和更新这些记忆来实现这一点。

## **结论**

如果构建具有记忆的 Agent（智能体）听起来很有趣，请尝试 [LangSmith Agent Builder](https://smith.langchain.com/agent_builder)。如果你想帮助我们构建这个记忆系统，[我们正在招聘](https://boards.greenhouse.io/langchain)。

### **加入我们的通讯**

获取来自 LangChain 团队和社区的更新

正在处理您的申请...

成功！请检查您的收件箱并点击链接确认订阅。

抱歉，出错了。请重试。

---

> 本文由AI自动翻译，原文链接：[How we built Agent Builder’s memory system](https://blog.langchain.com/how-we-built-agent-builders-memory-system/)
> 
> 翻译时间：2026-02-22 04:32
