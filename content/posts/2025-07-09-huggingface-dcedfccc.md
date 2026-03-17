---
title: 使用Gradio MCP服务器为LLM扩展图像编辑等新能力
title_original: Upskill your LLMs With Gradio MCP Servers
date: '2025-07-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gradio-mcp-servers
author: ''
summary: 本文介绍了模型上下文协议（MCP）如何像智能手机应用商店一样，为大型语言模型（LLM）添加新功能。文章重点展示了如何通过Hugging Face
  Spaces这一“MCP应用商店”，寻找并集成数千个基于Gradio的MCP服务器，从而赋予LLM图像编辑、网页浏览等原本不具备的能力。文中以Flux.1 Kontext[dev]图像编辑模型为例，详细演示了将其作为MCP服务器接入Cursor等LLM客户端的操作步骤，让LLM能够根据文本指令直接编辑图像。
categories:
- AI产品
tags:
- MCP协议
- Gradio
- LLM工具扩展
- Hugging Face Spaces
- AI应用开发
draft: false
translated_at: '2026-03-17T04:34:06.292119'
---

# 使用 Gradio MCP 服务器提升你的 LLM 能力

你是否曾希望自己喜爱的大语言模型（LLM）不仅能回答问题，还能做更多事情？如果它能为你编辑图片、浏览网页或整理电子邮件收件箱呢？

现在，它可以做到了！在这篇博客文章中，我将向你展示：

- MCP 协议是什么，以及它如何与我们熟悉的智能手机应用类似地工作，但这是针对 LLM 的。
- 如何通过“MCP 应用商店”找到数千个 MCP 服务器。
- 如何将其中一个服务器添加到你选择的 LLM 上，赋予它新的能力。我们将通过一个使用 `Flux.1 Kontext[dev]` 的例子来实践，该模型可以根据纯文本指令编辑图像。

## MCP 简介

**模型上下文协议（Model Context Protocol, MCP）** 是一个开放标准，使开发者能够在 LLM 与一组工具之间建立安全的双向连接。例如，如果你创建了一个 MCP 服务器，它公开了一个能够转录视频的工具，那么你就可以将一个 LLM 客户端（如 Cursor、Claude Code 或 Cline）连接到该服务器。然后，LLM 将知道如何转录视频，并根据你的请求为你使用这个工具。

简而言之，MCP 服务器是一种通过赋予新能力来提升 LLM 技能的标准方式。可以把它想象成你智能手机上的应用。智能手机本身无法编辑图片，但你可以从应用商店下载一个应用来实现这个功能。现在，要是有一个 MCP 服务器的应用商店就好了？🤔

## Hugging Face Spaces：MCP 应用商店

Hugging Face **Spaces** 是世界上最大的 AI 应用集合。这些空间中的大多数都使用 AI 模型执行专门的任务。例如：

- 图像背景移除
- OCR（光学字符识别）
- 文本转语音合成

这些空间是使用 **Gradio** 实现的，Gradio 是一个用于创建 AI 驱动的 Web 服务器的开源 Python 包。从 5.28.0 版本开始，**Gradio 应用支持 MCP 协议**。

这意味着 Hugging Face Spaces 是你可以为你的 LLM 找到数千种 AI 驱动能力的唯一地方，也就是 **MCP 应用商店**！

想浏览应用商店吗？访问此[链接](https://hf.co/spaces)。你也可以在 https://hf.co/spaces 手动筛选 **MCP Compatible** 选项。

![](/images/posts/bd0b3f43aa60.png)

## 示例：一个可以编辑图像的 LLM

`Flux.1 Kontext[dev]` 是一个令人印象深刻的模型，它可以根据纯文本提示词编辑图像。例如，如果你要求它“把我的头发染成蓝色”并上传一张你自己的照片，模型将返回照片，但你的头发会变成蓝色！

让我们将这个模型作为一个 MCP 服务器接入一个 LLM，并让它为我们编辑图像。请按照以下步骤操作：

1.  前往 [Hugging Face](https://huggingface.co/) 并创建一个免费账户。
2.  在你的**设置**中，点击左侧的 **MCP**。你可能需要向下滚动页面才能看到它。
3.  现在，滚动到页面底部。你应该会看到一个名为 **Spaces Tools** 的部分。在搜索栏中，输入 `Flux.1-Kontext-Dev` 并选择名为 `black-forest-labs/Flux.1-Kontext-Dev` 的空间。点击后页面应如下所示：

![](/images/posts/7542c5bcab40.png)

4.  对于这个演示，我们将使用 Cursor，但任何 **MCP 客户端** 都应遵循类似的步骤。滚动回 **MCP 设置** 页面的顶部，点击 **Setup with your AI assistant** 部分的 **Cursor** 图标。现在，复制该代码片段并将其粘贴到你的 Cursor 设置文件中。

![](/images/posts/39c14014c241.png)

5.  现在，当你在 Cursor 中开始一个新的聊天会话时，你可以要求它编辑图像了！请注意，目前图像必须通过公共 URL 访问。你可以创建一个 **Hugging Face Dataset** 来在线存储你的图像。

![](/images/posts/4d6201c89b77.png)

使用流行的公共空间作为工具可能意味着你需要等待更长时间才能收到结果。如果你访问该空间，可以点击“Duplicate This Space”为自己创建一个私有版本的空间。如果该空间使用的是“ZeroGPU”，你可能需要升级到 **PRO** 账户才能复制它。

6.  额外提示：你也可以使用 Hugging Face MCP 服务器搜索兼容 MCP 的空间！完成第 4 步后，你还可以要求你的 LLM 查找能完成特定任务的空间：

![](/images/posts/b8309d531bdc.png)

## 结论

这篇博客文章向你介绍了模型上下文协议（MCP）为大语言模型（LLM）带来的激动人心的新功能。我们已经看到，Gradio 应用，特别是那些托管在 Hugging Face Spaces 上的应用，现在完全兼容 MCP，这有效地将 Spaces 变成了一个充满活力的 LLM 工具“应用商店”。通过连接这些专门的 MCP 服务器，你的 LLM 可以超越基本的问答功能，获得强大的新能力，从图像编辑到转录，再到任何你能想象到的事情！

---

> 本文由AI自动翻译，原文链接：[Upskill your LLMs With Gradio MCP Servers](https://huggingface.co/blog/gradio-mcp-servers)
> 
> 翻译时间：2026-03-17 04:34
