---
title: LangSmith Fetch发布：在终端中调试Agent的新工具
title_original: 'Introducing LangSmith Fetch: Debug agents from your terminal'
date: '2025-12-10'
source: LangChain Blog
source_url: https://blog.langchain.com/introducing-langsmith-fetch/
author: LangChain Accounts
summary: 本文介绍了新发布的CLI工具LangSmith Fetch，它将LangSmith的追踪功能直接引入终端和IDE。该工具解决了开发者在调试Agent时需要切换到Web界面的不便，支持通过命令行直接获取追踪记录和会话线程数据。文章重点说明了两个核心工作流：即时调试最新运行记录和批量导出数据用于评估分析，并展示了如何与Claude
  Code等编码Agent配合，使其能够直接分析完整的Agent执行数据，从而提升调试效率。
categories:
- AI产品
tags:
- LangSmith
- Agent调试
- 开发者工具
- 命令行工具
- 可观测性
draft: false
translated_at: '2026-01-06T01:09:14.285Z'
---

今天我们发布 LangSmith Fetch，这是一款 CLI 工具，它将 LangSmith 追踪的全部功能直接带入了您的终端和 IDE。

如果您正在使用 Claude Code 或 Cursor 等编码工具构建 Agent（智能体），或者您只是单纯更喜欢在命令行中工作，您可能都遇到过这种不便：您的 Agent 运行了，但出了问题，现在您不得不切换上下文到 LangSmith 的 Web 界面去查找原因。您需要找到正确的追踪记录，点击界面，并想办法将这些数据带回您的工作流中。

LangSmith Fetch 彻底消除了这种不便。只需一条命令，您就可以将任何追踪记录或会话线程直接拉取到您的终端，将其提供给您的编码 Agent，或者通过管道传输到您的分析脚本中。请在此处查看代码仓库。

**适配各种工作流的可观测性**

LangSmith 是帮助您快速交付可靠 Agent 的 Agent 工程平台。它能捕获您 Agent 所做的一切：每一次 LLM（大语言模型）调用、每一次工具执行、每一个决策点。成千上万的开发者依赖它来调试生产环境中的 Agent。

然而，并非每个人都想在 Web 界面中进行调试。如果您是终端优先的开发者，切换到浏览器会打断您的工作流。如果您正在使用 Claude Code 或其他编码 Agent 来协助调试，您需要的是您的 Agent 能够消费的追踪数据格式。如果您正在根据生产环境的追踪记录构建评估数据集，您需要批量导出的能力。

LangSmith 的 Web 界面功能强大，但对于这些工作流，您需要的是不同的东西：从命令行直接以编程方式访问您的追踪数据。

**LangSmith Fetch 的功能**

LangSmith Fetch 围绕两个核心开发者工作流设计：

**“我刚运行了某个东西”工作流**

您在本地执行您的 Agent。发生了奇怪的事情。您立即运行：
```
langsmith-fetch traces --project-uuid <your-uuid> --format json
```
搞定。您项目中最新的追踪记录，就在您的终端里。无需打开浏览器，无需寻找追踪 ID，无需复制粘贴。即时访问刚刚发生的情况。

您可以进一步缩小范围：
```
# 获取过去 30 分钟的追踪记录
langsmith-fetch traces --project-uuid <your-uuid> --last-n-minutes 30
# 获取最后 5 条追踪记录
langsmith-fetch traces --project-uuid <your-uuid> --limit 5
```

**批量导出工作流**

当您需要用于评估、分析或构建测试套件的数据集时：
```
# 将 50 个会话线程导出为单独的 JSON 文件
langsmith-fetch threads ./my-data --limit 50
# 使用时间过滤器导出追踪记录
langsmith-fetch traces ./traces --project-uuid <your-uuid> --after 2025-12-01
```
每个会话线程或追踪记录都会保存为单独的文件，非常适合批处理、提供给 LLM 进行分析，或构建回归测试套件。

**专为编码 Agent 打造**

这才是它真正强大的地方：LangSmith Fetch 让您的编码 Agent 成为专家级的 Agent 调试器。

当您使用 Claude Code、Cursor 或其他 AI 编码助手时，它们现在可以直接访问您完整的 Agent 执行数据。只需运行 `langsmith-fetch` 并将输出通过管道传输给您的编码 Agent。突然间，您的编码 Agent 就能：
- 分析您的 Agent 为何做出特定决策
- 识别跨多个追踪记录的低效模式
- 根据实际执行数据建议提示词改进
- 从生产环境故障中构建测试用例

**与 Claude Code 配合使用的示例工作流：**
```
claude-code "use langsmith-fetch to analyze the traces in <project-uuid> and tell me why the agent failed"
```
现在，您的编码 Agent 无需您手动解释或复制数据，就能获得关于所发生情况的完整上下文。

**与您现有的 LangSmith 设置协同工作**

无需新的配置。如果您已经在向 LangSmith 发送追踪记录，LangSmith Fetch 可以立即使用。只需通过 pip 安装：
```
pip install langsmith-fetch
```
设置您的 API 密钥（如果尚未设置）：
```
export LANGSMITH_API_KEY=your_api_key
```
然后您就可以开始了。LangSmith Fetch 使用与您其他 LangSmith 设置相同的身份验证和项目。

**CLI，而非 MCP**

您可能想知道：为什么要构建 CLI 工具而不是 MCP 服务器？MCP 是一种优秀的协议，用于让 LLM 结构化地访问外部数据源，许多开发者直接在他们的调试工作流中使用它，尤其是在 Cursor 或 Claude Code 等工具内部。

但 MCP 和 CLI 解决的是不同的需求。当您调试 Agent 时，您需要灵活性：
- 有时您想在终端中快速检查一条追踪记录
- 有时您想将数据通过管道传输到 `jq` 或其他 Unix 工具
- 有时您想将追踪记录保存到文件以供后续分析
- 有时您想将数据提供给编码 Agent
- 有时您想构建处理数百条追踪记录的脚本

CLI 工具为您提供了所有这些可能。您可以独立使用它，将其输出传输到任何地方，将其集成到任何工作流中，并与您生态系统中的任何工具结合使用。它是一个基础的构建模块。

相比之下，MCP 会将您锁定在兼容 MCP 的工具和实时请求/响应模式中。它非常适合其设计目标（让 Claude 或其他 MCP 客户端访问您的数据），但对于开发者所需的各种工作流来说，它限制性太强。

CLI 更灵活、更具组合性，也更符合 Unix 哲学。您仍然可以将 LangSmith Fetch 的输出提供给您的编码 Agent（无论是否兼容 MCP），但您还可以用它做上百件其他事情。

我们并不反对 MCP。我们只是认为并非每个开发者工具都需要是 MCP。有时，一个精心设计的 CLI 正是您所需要的。

**立即开始使用**

LangSmith Fetch 现已可在 PyPI 上获取。安装它，运行您的第一次获取，体验无需离开终端的 Agent 调试。

```
# 安装
pip install langsmith-fetch
# 获取您最近的追踪记录
langsmith-fetch threads --project-uuid <your-uuid>
```

有关完整文档、示例和高级用法，请查看 GitHub 仓库。

如需动手教程，请在此处观看我们的视频演示。

无论您是终端优先的开发者、使用编码 Agent 进行构建，还是只想更快地访问您的追踪数据，LangSmith Fetch 都将 LangSmith 可观测性的强大功能直接带入了您的工作流。

---

> 本文由AI自动翻译，原文链接：[Introducing LangSmith Fetch: Debug agents from your terminal](https://blog.langchain.com/introducing-langsmith-fetch/)
> 
> 翻译时间：2026-01-06 01:09
