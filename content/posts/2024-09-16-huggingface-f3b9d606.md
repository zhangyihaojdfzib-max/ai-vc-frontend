---
title: HuggingChat推出社区工具功能
title_original: Introducing Community Tools on HuggingChat
date: '2024-09-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/community-tools
author: ''
summary: HuggingChat发布社区工具功能，允许用户将HuggingFace上的任何Space转化为工具，供模型在对话中使用。该功能扩展了可用模态，支持图像理解、视频生成、文本转语音等。文章详细介绍了四种用例：将社区Space转化为工具、自行创建自定义工具、使用社区工具增强助手、以及基于文档创建RAG工具。通过简单的配置和Python编程，用户可轻松集成现有模型或自定义功能，极大提升了HuggingChat的扩展性和实用性。
categories:
- AI产品
tags:
- HuggingChat
- 社区工具
- AI产品
- 工具集成
- Gradio
draft: false
translated_at: '2026-06-30T06:14:02.183856'
---

# HuggingChat 社区工具发布

今天，我们在 HuggingChat 上发布了最新功能：社区工具！这让你可以将 HuggingFace 上你喜爱的任何 Space 转化为一个工具，供模型直接在 HuggingChat 中使用。

借助这一功能，我们还在 HuggingChat 中扩展了可用的模态。你现在可以使用社区工具来理解图像、生成视频，或通过文本转语音模型进行回答。可能性是无限的，任何人都可以使用 Hugging Face 上的 Space 创建工具！在此处探索现有工具。

在这篇文章中，我们将探讨创建社区工具的几个用例：

1. 将社区 Space 转化为工具
2. 自行创建自定义工具
3. 使用社区工具增强你的助手
4. 基于自己的文档创建 RAG 工具

## 将社区 Space 转化为工具

你可以将任何人的公开 Space 转化为工具。这对于直接在 HuggingChat 中使用最新模型非常方便。我们以 DamarJati/FLUX.1-RealismLora 为例。

首先，创建一个新工具并填写各个字段。当你将 Space URL 输入到 Hugging Face Space URL 字段时，可用的函数和参数会自动填充。

![](/images/posts/9596022de924.png)

有一些字段需要正确填写，以确保工具的最佳性能。

- 工具描述：该描述会传递给 LLM，用于说明工具的功能。请保持简短，并描述工具的用途。
- AI 函数名称：工具以代码函数的形式呈现。这是你的工具的函数名称。请保持简短、唯一且不言自明。
- 参数：这些是 LLM 可以填写的工具参数。它们可以是：
  - 必填：模型必须填写一个值才能使用此工具。这要求参数被正确描述。
  - 可选：提供了默认值，但模型可以在需要时覆盖它。
  - 固定：创建工具时值被固定，模型无法更改。

你可以随时查看其他工具的定义，以更好地理解如何创建工具。（示例）

![](/images/posts/abd52c1d44ed.png)

现在我们的工具已创建完成，我们可以启用它，并开始与支持工具的模型一起使用！

![](/images/posts/7779d111abd3.png)

## 自行创建自定义工具

使用现有的 Space 可以覆盖许多用例，但如果你能编写基本的 Python，那么你也可以轻松地为自己创建自定义工具。我们以掷骰子工具为例，因为 LLM 在自行选择随机数方面表现不佳。

首先，在 Hugging Face 上创建一个新的 Gradio Space。CPU Basic 免费套餐对此完全够用。你的 Space 必须是公开的，才能在 HuggingChat 中使用。

在你的 Space 仓库中创建一个简单的 app.py 文件，以我们的掷骰子示例为例，可以是：

```python
import gradio as gr
import random

def roll_dice(sides=6):
    return random.randint(1, sides)

demo = gr.Interface(
    fn=roll_dice,
    inputs=gr.Number(value=6, label="Number of Sides"),
    outputs="text",
    title="Dice Roller",
    description="Enter the number of sides for the dice and get the roll result."
)

demo.launch()
```

如果你不熟悉 Gradio，入门创建界面非常简单，你可以在此处找到文档。

你可以在一个 Space 中包含多个函数，以便更轻松地管理你的工具。

完成后，推送更改，当你的 Space 部署完成后，你就可以像之前一样在 HuggingChat 中为其创建一个社区工具。

![](/images/posts/ecdd44ecad54.png)

## 使用社区工具增强你的助手

你可以直接前往工具页面激活工具，选择你喜欢的工具，或者你也可以将工具打包到助手中。

在创建助手时，如果使用支持工具调用的模型，你现在可以选择工具。搜索工具名称，最多可添加 3 个不同的工具。在我们的例子中，让我们创建一个游戏大师助手，它可以访问图像生成和掷骰子工具。

你可以使用系统指令字段告诉模型何时使用这些工具。

![](/images/posts/e8fb7a8d765c.png)

## 基于自己的文档创建 RAG 工具

配合此次发布，我们创建了一个简单的 RAG 工具，你可以轻松复制它，以便直接从 HuggingChat 询问关于你文档的问题。首先，将此 Space 复制到你的账户中。然后，你可以将想要解析的文件放入该 Space 的 sources/ 文件夹中。

![](/images/posts/0b39d35ea7f8.png)

一旦 Space 启动，你就可以像我们之前介绍的那样，在 HuggingChat 上轻松地为其创建一个工具。

![](/images/posts/34bc4428528e.png)

### 与我们分享你的反馈

随着社区工具的发布，我们希望你能通过多模态内容和自定义工具来增强你的聊天体验。该功能仍处于实验阶段，因此如果你发现不支持的 Space 或无法正常工作的工具，请在此反馈帖中与我们分享！

---

> 本文由AI自动翻译，原文链接：[Introducing Community Tools on HuggingChat](https://huggingface.co/blog/community-tools)
> 
> 翻译时间：2026-06-30 06:14
