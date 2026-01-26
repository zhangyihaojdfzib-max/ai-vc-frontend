---
title: 使用LangSmith与Polly调试深度智能体
title_original: Debugging Deep Agents with LangSmith
date: '2025-12-10'
source: LangChain Blog
source_url: https://www.blog.langchain.com/debugging-deep-agents-with-langsmith/
author: ''
summary: 本文探讨了调试深度智能体与简单LLM应用程序的区别，指出深度智能体因提示词长、追踪记录复杂、多轮交互等特点而更难调试。文章介绍了LangSmith的追踪功能如何捕获智能体执行的运行、追踪和线程数据，并重点推出了Polly——一个内置于LangSmith的AI助手，可通过聊天方式分析智能体轨迹，帮助开发者快速定位问题、优化提示词。此外，还发布了命令行工具langsmith-fetch，为编码智能体提供调试支持。
categories:
- AI产品
tags:
- LangSmith
- 智能体调试
- AI助手
- LLM追踪
- 深度智能体
draft: false
translated_at: '2026-01-15T04:40:27.497207'
---

![Debugging Deep Agents with LangSmith](/images/posts/f482dea708f9.webp)

![Debugging Deep Agents with LangSmith](/images/posts/f482dea708f9.webp)

# 使用 LangSmith 调试深度智能体

调试是发现并修复错误的过程。这是软件工程中的关键步骤，在智能体工程中则更为关键。LangSmith 的一项核心能力就是提供调试 LLM（大语言模型）应用程序的工具。

今天，我们将加倍努力，为正在开发的新一波“深度智能体”解决这个问题。

- 解释为什么调试深度智能体与调试简单的 LLM 应用程序不同
- 介绍 **Polly**（一个用于智能体工程的 AI 助手），以帮助在 LangSmith 中调试深度智能体
- 发布 **langsmith-fetch**，一个为 Claude Code 或 DeepAgents CLI 等编码智能体配备调试能力的命令行工具

## 深度智能体与简单 LLM 应用程序有何不同

与简单的 LLM 调用或简短工作流不同，深度智能体运行时间长达数分钟，跨越数十甚至数百个步骤，并且通常涉及与用户的多次来回交互。

![](/images/posts/f4ca4dd9043c.png)

![](/images/posts/f4ca4dd9043c.png)

因此，一次深度智能体执行所产生的追踪记录可能包含海量信息，远超出人类能够轻松扫描或理解的范围。当出现问题时，可能很难确定是哪个决策、提示词指令或工具调用导致了您所看到的行为。

这正是使用 LangSmith 进行追踪——并利用 AI 分析这些追踪记录——变得重要的地方。那么，具体是什么让深度智能体更加复杂呢？

- **更长的提示词**：深度智能体的提示词通常长达数百甚至数千行——通常包含一个通用角色设定、调用工具的说明、重要指导原则以及少量示例。当行为表现下降时，很难知道是提示词的哪一部分出了问题。
- **更长的追踪记录**：深度智能体可以运行数十甚至数百个步骤（需要数分钟才能完成）。面对如此庞大的追踪记录，人类需要解析的内容更多，才能找到有意义的片段。
- **多轮交互**：深度智能体默认支持人机协作工作流。一次有意义的深度智能体对话示例通常涉及多次来回交互。为了理解智能体的行为并查看其完整轨迹，您需要查看多次交互。

## 追踪捕获相关信息

为了调试智能体，您需要能够洞察其内部正在发生什么。这就是追踪的作用。

我们使用“追踪”这个总称来描述将您的智能体执行数据记录到 LangSmith。数据格式由**运行**、**追踪**和**线程**组成。

![](/images/posts/e8637c1f5175.png)

![](/images/posts/e8637c1f5175.png)

- **运行**：您的智能体执行的一个步骤。例如包括 LLM 模型调用和工具调用。运行以树形结构嵌套。
- **追踪**：您的智能体的一次执行。一个追踪由一棵运行树构成。
- **线程**：追踪记录的集合。一个线程是用户与应用程序之间的完整对话。

追踪的设置非常简单——您可以按照此[指南](https://docs.smith.langchain.com/tracing)在几分钟内完成设置。

一旦您的应用程序数据进入 LangSmith，您就可以利用 AI 分析完整的智能体轨迹，以了解发生了什么，然后建议更新提示词。主要有两种方法可以实现这一点。

## Polly - 智能体工程的 AI 助手

Polly 是一项**新的应用内功能**，允许您通过与一个智能体聊天来分析您的线程和追踪数据。请在此处查看我们的[视频概述](https://youtu.be/8h2X4i1Q7qI)。

以下是几种与 Polly 聊天的方式！

![](/images/posts/f3351767664c.png)

![](/images/posts/f3351767664c.png)

您可以使用 Polly 来调试、分析和理解追踪记录中发生的事情。无需手动扫描数十或数百个步骤，您可以向 Polly 提出诸如以下问题：

- “智能体有没有做什么可以更高效的事情？”
- “智能体有没有犯任何错误？”

这对于深度智能体尤其有帮助，因为它们往往有更长的追踪记录，故障模式可能分布在许多步骤中。

![](/images/posts/120a861b27b2.png)

![](/images/posts/120a861b27b2.png)

这与单个追踪类似，但在这里，Polly 可以访问整个线程的信息。线程跨越多次对话轮次，并且通常也可能跨越数小时或数天。一个人很难掌握所有这些上下文。

**在提示词游乐场中**

![](/images/posts/800f0138befc.png)

![](/images/posts/800f0138befc.png)

深度智能体最重要的部分之一是系统提示词。Polly 经过调优，成为了一名出色的提示词工程师！只需用自然语言描述您想要的行为，Polly 就会相应地更新您的提示词。Polly 还可以帮助您定义结构化输出或在模型调用上模拟工具。

## LangSmith Fetch CLI - 让您的编码智能体成为专家智能体工程师的工具

如果您更喜欢在 IDE 或代码智能体（例如 DeepAgents、Claude Code 等）中工作，我们提供了一个 CLI 工具 **LangSmith Fetch**，可以轻松连接到 LangSmith 的追踪记录或线程。无论您是在调试智能体、分析对话流，还是从生产追踪记录中构建数据集，这个 **CLI** 都能为您提供快速、灵活地访问 LangSmith 追踪记录和线程的方式。

它弥合了 LangSmith UI 与您本地工作流程之间的差距，让您可以在确切知道需要什么时通过 ID 获取追踪记录或线程，或者在需要获取刚刚发生的事情时通过时间获取。该工具支持多种输出格式（人类可读的面板、美观的 JSON 或紧凑的原始 JSON），以适应您的用例——无论您是在终端检查数据、通过管道传输到 `jq`，还是将结果提供给 LLM 进行分析。

它支持两个关键工作流程。首先，是“我刚运行了某个东西”的工作流程，用于获取最近的线程：您执行您的智能体，然后立即运行 `langsmith-fetch threads ./my_data` 来获取项目中最近的追踪记录，而无需在 UI 中寻找 ID。添加时间过滤器，如 `--last-n-minutes 30` 来缩小搜索范围，或使用 `--project-uuid` 来定位特定项目。

```
# 刚运行了您的智能体？立即获取最近的追踪记录
langsmith-fetch traces --project-uuid <your-uuid> --format json

# 或者获取最后 5 条追踪记录
langsmith-fetch traces --project-uuid <your-uuid> --limit 5

```

其次，是批量导出工作流程：当您需要用于评估或分析的数据集时，像 `langsmith-fetch threads ./my-data --limit 50` 这样的命令可以获取多个线程并将每个线程保存为单独的 JSON 文件，非常适合批处理或构建测试集。

```
# 或者从特定项目获取最后 5 条追踪记录
langsmith-fetch traces --project-uuid <your-uuid> --limit 5

```

当然，您也可以提供所需的线程或追踪 ID。输出格式可根据您的需求调整：`--format pretty` 用于通过 Rich 面板在终端查看，`--format json` 用于可读的结构化数据，或 `--format raw` 用于通过管道传输到其他工具。

## LangSmith 让调试和改进您的深度智能体变得简单

深度智能体功能强大，但与简单的 LLM 工作流相比，运行时间更长且更复杂。为了理解和改进它们，您需要能够洞察您的深度智能体实际在做什么。

借助 LangSmith，您可以追踪您的深度智能体并查看发生了什么——然后，与 **Polly** 聊天以分析您深度智能体的行为，并使用 AI 帮助您改进提示词。如果您更愿意使用 Claude Code 或其他编码智能体进行分析，您可以使用 **LangSmith Fetch** 为您的编码智能体配备所有必要的调试工具。

只需几分钟即可设置追踪，今天就尝试在 LangSmith 上与 Polly 聊天，以调试和改进您的深度智能体！

来自 LangChain 团队和社区的更新

正在处理您的申请...

成功！请检查您的收件箱并点击链接确认订阅。

抱歉，出错了。请重试。

---

> 本文由AI自动翻译，原文链接：[Debugging Deep Agents with LangSmith](https://www.blog.langchain.com/debugging-deep-agents-with-langsmith/)
> 
> 翻译时间：2026-01-15 04:40
