---
title: 本地部署OlympicCoder：开源编程助手实战指南
title_original: 'Open R1: How to use OlympicCoder locally for coding'
date: '2025-03-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/olympic-coder-lmstudio
author: ''
summary: 本文介绍了如何在本地环境中使用开源模型OlympicCoder 7B进行编程辅助。通过LM Studio下载并运行模型的GGUF量化版本，再借助Continue扩展将模型集成到VS
  Code中，即可获得媲美甚至超越Claude和GPT-4o的代码生成能力。文章详细演示了从安装LM Studio、获取模型到配置IDE的完整流程，为开发者提供了一条低成本、高隐私的本地AI编程助手搭建路径。
categories:
- AI产品
tags:
- OlympicCoder
- 本地部署
- 编程助手
- LM Studio
- 开源模型
draft: false
translated_at: '2026-05-07T05:30:58.357074'
---

# Open R1：如何在本地使用 OlympicCoder 进行编程

过去几年，大家都在使用 Claude 和 OpenAI 作为编程助手，但如果你关注一下 Open R1 等开源项目的最新进展，就会发现它们的吸引力有所下降。看看下面 LiveCodeBench 的评估结果，我们可以看到 7B 参数版本的表现优于 Claude 3.7 Sonnet 和 GPT-4o。这些模型是许多工程师在 Cursor 和 VSCode 等应用中的日常工具。

![评估结果](/images/posts/802737b728cc.png)

评估结果固然很好，但我想亲自动手，感受代码提交的乐趣！这篇博文将重点介绍如何现在就将这些模型集成到你的 IDE 中。我们将设置 OlympicCoder 7B，这是两个 OlympicCoder 变体中较小的一个，并且我们将使用量化版本以获得最佳的本地推理效果。以下是我们要使用的技术栈：

- OlympicCoder 7B：来自 LMStudio 社区的 4bit GGUF 版本
- LM Studio：一个简化 AI 模型运行的工具
- Visual Studio Code (VS Code)
- Continue：一个用于本地模型的 VS Code 扩展

需要说明的是，我们选择这个技术栈纯粹是为了简单。你可能想尝试更大的模型和/或不同的 GGUF 文件，甚至使用 llama.cpp 等替代推理引擎。

![生成过程](/images/posts/c479310333dc.gif)

# 1. 安装 LM Studio

LM Studio 就像一个 AI 模型的控制面板。它与 Hugging Face 中心集成，可以拉取模型，帮助你找到合适的 GGUF 文件，并提供一个 API 供其他应用程序与模型交互。

简而言之，它让你无需复杂设置就能下载和运行模型。

1. 访问 LM Studio 网站：打开你的网页浏览器，访问 https://lmstudio.ai/download。
2. 选择你的操作系统：点击适合你电脑的下载按钮（Windows、Mac 或 Linux）。
3. 安装 LM Studio：运行下载的文件并按照说明操作。就像安装其他任何程序一样。

# 2. 获取 OlympicCoder 7B

我们需要的 GGUF 文件托管在中心。我们可以使用“使用此模型”按钮，从中心在 LMStudio 中打开模型：

![模型页面](/images/posts/78209c35427f.png)

这将链接到 LMStudio 应用程序并在你的机器上打开它。你只需要选择量化方式。我选择了 Q4_K_M，因为它在大多数设备上都能表现良好。如果你有更强的算力，可以尝试 Q8_* 的选项。

如果你想跳过用户界面，也可以通过命令行使用 LMStudio 加载模型：

```
lms get lmstudio-community/OlympicCoder-7B-GGUF
lms load olympiccoder-7b
lms server start

```

# 3. 将 LM Studio 连接到 VS Code

这是重要的一步。我们现在需要将 VSCode 与 LMStudio 提供的模型集成。

1. 在 LM Studio 中，在“开发者”选项卡上激活服务器。这将暴露 http://localhost:1234/v1 的端点。

![lmstudio](/images/posts/88f6e32c4389.png)

1. 安装 VS Code 扩展以连接到我们的本地服务器。我选择了 Continue.dev，但也有其他选择。在 VSCode 中，转到扩展视图（点击左侧边栏的方形图标，或按 Ctrl+Shift+X / Cmd+Shift+X）。搜索“Continue”并安装来自“Continue Dev”的扩展。
2. 在 Continue.dev 中配置新模型。打开 Continue 选项卡，在模型下拉菜单中选择“添加新的聊天模型”。这将打开一个 json 配置文件。你需要指定模型名称，例如 olympiccoder-7b

- 在 VSCode 中，转到扩展视图（点击左侧边栏的方形图标，或按 Ctrl+Shift+X / Cmd+Shift+X）。
- 搜索“Continue”并安装来自“Continue Dev”的扩展。

- 打开 Continue 选项卡，在模型下拉菜单中选择“添加新的聊天模型”。
- 这将打开一个 json 配置文件。你需要指定模型名称，例如 olympiccoder-7b

![continue](/images/posts/67f647ab3683.png)

# 🚀 你拥有了一个本地编程助手！

通过此设置，vscode 中的大多数核心 AI 功能都可以使用，例如：

- 代码补全：开始输入，AI 会建议如何完成你的代码。
- 生成代码：要求它编写一个函数或整个代码块。例如，你可以输入（在注释或聊天窗口中，取决于扩展）：// 编写一个在 JavaScript 中反转字符串的函数
- 解释代码：选择一些代码，让 AI 解释它的作用。
- 重构代码：让 AI 使你的代码更简洁或更高效。
- 编写测试：让 AI 为你的代码创建单元测试。

# 🏋️‍♀️ OlympicCoder 的风格如何？

OlympicCoder 不是 Claude。它基于 CodeForces-CoTs 数据集进行了优化，该数据集基于竞赛编程挑战。这意味着你不应期望它非常友好和善于解释。相反，挽起袖子，准备迎接一个毫不留情的竞赛编程高手，随时准备处理棘手的问题。

你可能希望将 OlympicCoder 与其他模型混合使用，以获得全面的编程体验。例如，如果你想从二分查找中挤出毫秒级的性能提升，试试 OlympicCoder。如果你想设计面向用户的 API，选择 Claude-3.7-sonnet 或 Qwen-2.5-Coder。

# 后续步骤

- 在下方评论中分享你最喜欢的生成结果
- 从中心尝试 OlympicCoder 的另一个变体
- 根据你的硬件尝试不同的量化类型
- 在 LM Studio 中尝试多个模型以获得不同的编程风格！查看模型目录 https://lmstudio.ai/models
- 尝试其他 VS Code 扩展，如具有 Agent（智能体）功能的 Cline

---

> 本文由AI自动翻译，原文链接：[Open R1: How to use OlympicCoder locally for coding](https://huggingface.co/blog/olympic-coder-lmstudio)
> 
> 翻译时间：2026-05-07 05:30
