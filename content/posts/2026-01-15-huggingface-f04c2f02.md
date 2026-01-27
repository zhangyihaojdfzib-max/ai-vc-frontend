---
title: 开放响应：新一代AI推理标准解析
title_original: 'Open Responses: What you need to know'
date: '2026-01-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/open-responses
author: ''
summary: 本文介绍了开放响应（Open Responses）这一新兴的开放推理标准。它由OpenAI发起、开源社区构建，并获Hugging Face生态系统支持，旨在解决传统Chat
  Completion格式在智能体工作流中的局限性。文章阐述了开放响应的核心特性，包括无状态设计、标准化参数、事件流式传输等，并对比了客户端与提供商所需的变更，为开发者迁移和构建下一代自主智能体系统提供了关键指引。
categories:
- AI基础设施
tags:
- 开放响应
- 推理标准
- AI智能体
- API设计
- 开源生态
draft: false
translated_at: '2026-01-16T04:39:01.486745'
---

# 开放响应：你需要了解的内容

- +14

什么是开放响应？使用开放响应进行构建需要了解什么？向开放响应发起的客户端请求推理客户端与提供商的变更用于路由的开放响应工具子智能体循环后续步骤开放响应是一种全新且开放的推理标准。它由 OpenAI 发起，由开源 AI 社区构建，并得到 Hugging Face 生态系统的支持。开放响应基于 Responses API，专为智能体的未来而设计。在这篇博客文章中，我们将探讨开放响应的工作原理以及开源社区为何应该使用开放响应。

- 什么是开放响应？
- 使用开放响应进行构建需要了解什么？向开放响应发起的客户端请求推理客户端与提供商的变更用于路由的开放响应工具子智能体循环
- 后续步骤

- 向开放响应发起的客户端请求
- 推理客户端与提供商的变更
- 用于路由的开放响应
- 工具
- 子智能体循环

聊天机器人的时代早已过去，智能体主导着推理工作负载。开发者正转向能够在长时间范围内进行推理、规划和行动的自主系统。尽管发生了这种转变，但生态系统的大部分仍在使用为回合制对话设计的`Chat Completion`格式，这无法满足智能体用例的需求。`Responses`格式旨在解决这些限制，但它是封闭的，并未被广泛采用。尽管存在替代方案，`Chat Completion`格式仍然是事实上的标准。

智能体工作流需求与根深蒂固的接口之间的这种不匹配，催生了对开放推理标准的需求。在接下来的几个月里，我们将与社区和推理提供商合作，实现并调整开放响应，使其成为一种共享格式，实际上能够替代聊天补全。

开放响应建立在 OpenAI 于 2025 年 3 月推出的`Responses API`所设定的方向上，该 API 以一致的方式取代了现有的 Completion 和 Assistants API，能够：

- 生成文本、图像和 JSON 结构化输出
- 通过独立的任务型端点创建视频内容
- 在提供商端运行智能体循环，自主执行工具调用并返回最终结果。

## 什么是开放响应？

开放响应扩展并开源了 Responses API，使构建者和路由提供商更容易在共同利益上进行互操作和协作。

一些关键点包括：

- 默认无状态，支持需要加密推理的提供商。
- 标准化的模型配置参数。
- 流式传输被建模为一系列语义事件，而非原始文本或对象增量。
- 可通过特定于某些模型提供商的可配置参数进行扩展。

## 使用开放响应进行构建需要了解什么？

我们将简要探讨影响大多数社区成员的核心变更。如果你想深入了解规范，请查看`开放响应文档`。

### 向开放响应发起的客户端请求

向开放响应发起的客户端请求与现有的 Responses API 类似。下面我们演示使用 curl 向开放响应 API 发起请求。我们调用一个代理端点，该端点使用开放响应 API 模式路由到推理提供商。

```
 curl https://evalstate-openresponses.hf.space/v1/responses \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer $HF_TOKEN" \
+  -H "OpenResponses-Version: latest" \
   -N \
   -d '{
         "model": "moonshotai/Kimi-K2-Thinking:nebius",
         "input": "explain the theory of life"
       }'

```

### 推理客户端与提供商的变更

已经支持 Responses API 的客户端可以相对轻松地迁移到开放响应。主要变更包括：

- 将推理流迁移为使用可扩展的“reasoning”块，而非“reasoning_text”。
- 实现更丰富的状态变更和有效载荷 - 例如，托管的代码解释器可以发送特定的`interpreting`状态以提高智能体/用户的可观测性。

对于模型提供商而言，如果他们已遵循 Responses API 规范，那么为开放响应实施变更应该是直接的。对于路由器而言，现在有机会在一致的端点上实现标准化，并在需要时支持自定义的配置选项。

随着时间的推移，随着提供商不断创新，某些功能将在基础规范中实现标准化。

总之，迁移到开放响应将使推理体验更加一致，并提高质量，因为旧版 Completions API 中未记录的扩展、解释和变通方法将在开放响应中得到规范化。

你可以在下面看到如何流式传输推理块。

```
 {
  "model": "moonshotai/Kimi-K2-Thinking:together",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": "explain photosynthesis."
    }
  ],
  "stream": true
}

```

以下是开放响应与 Responses 在推理增量上的区别：

```
{
  "delta": " heres what i'm thinking",
  "sequence_number": 12,
+ "type": "response.reasoning.delta",
- "type": "response.reasoning_text.delta",
  "item_id": "msg_cbfb8a361f26c0ed0cb133b3c2387279b3d54149a262f3a7",
  "output_index": 0,
  "obfuscation": "0HG8OhAdaLQBg",
  "content_index": 0
}

```

### 用于路由的开放响应

开放响应区分了“模型提供商”（提供推理服务）和“路由器”（在多个提供商之间进行编排的中介）。

客户端现在可以在发起请求时指定一个提供商以及特定于该提供商的 API 选项，从而允许中介路由器在上游提供商之间编排请求。

开放响应原生支持两类工具：内部工具和外部工具。外部托管的工具在模型提供商的系统之外实现。例如，需要在客户端执行的函数，或 MCP 服务器。内部托管的工具则在模型提供商的系统内部。例如，OpenAI 的文件搜索或 Google Drive 集成。模型调用、执行和检索结果完全在提供商的基础设施内进行，无需开发者干预。

开放响应形式化了智能体循环，该循环通常由推理、工具调用和响应生成的重复周期组成，使模型能够自主完成多步骤任务。

图片来源：openresponses.org

循环操作如下：

1.  API 接收用户请求并从模型中进行采样
2.  如果模型发出工具调用，API 则执行它（内部或外部）
3.  工具结果被反馈给模型以继续推理
4.  循环重复，直到模型发出完成信号

对于内部托管的工具，提供商管理整个循环；执行工具，将结果返回给模型，并流式传输输出。这意味着像“搜索文档、总结发现、然后起草电子邮件”这样的多步骤工作流只需一个请求。

客户端通过`max_tool_calls`来限制迭代次数，并通过`tool_choice`来约束可调用的工具，从而控制循环行为：

```
{
  "model": "zai-org/GLM-4.7",
  "input": "Find Q3 sales data and email a summary to the team",
  "tools": [...],
  "max_tool_calls": 5,
  "tool_choice": "auto"
}

```

响应包含所有中间项：工具调用、结果、推理。

Open Responses 扩展并改进了 Responses API，提供了更丰富、更详细的内容定义、兼容性和部署选项。它还提供了一种标准方式，在主推理调用期间执行子智能体循环，为 AI 应用开启了强大的能力。我们期待与 Open Responses 团队及整个社区合作，共同推进该规范的未来发展。

您现在就可以通过 Hugging Face 推理提供商 试用 Open Responses。我们在 Hugging Face Spaces 上提供了早期访问版本，今天就使用您的客户端和 Open Responses 合规工具来试试吧！

## ScreenEnv：部署您的全栈桌面智能体

## Codex 正在开源 AI 模型

这是否意味着本地 LLM 端点提供商（如 vLLM）的下一步是支持托管工具？

是的——我认为我们将看到更多这种模式，特别是对于通过 Open Responses 将工作卸载给子智能体工具循环的智能体。

> 本文由AI自动翻译，原文链接：[Open Responses: What you need to know](https://huggingface.co/blog/open-responses)
> 
> 翻译时间：2026-01-16 04:39
