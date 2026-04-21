---
title: 5行Python代码构建MCP服务器：Gradio新功能详解
title_original: How to Build an MCP Server with Gradio
date: '2025-04-30'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gradio-mcp
author: ''
summary: 本文介绍了如何使用Gradio库快速构建MCP（模型上下文协议）服务器，使大语言模型能够调用自定义Python工具。文章以字母计数工具为例，展示了仅需5行核心代码即可将Gradio应用转换为MCP服务器，并详细说明了安装配置步骤、MCP服务器的工作原理以及如何与Claude
  Desktop、Cursor等客户端集成。2025年9月更新的版本还包含了资源管理、提示词优化和增强身份验证等新特性。
categories:
- AI基础设施
tags:
- Gradio
- MCP协议
- Python开发
- AI工具集成
- 大语言模型
draft: false
translated_at: '2026-04-21T05:06:21.759920'
---

# 如何用5行Python代码构建MCP服务器

已更新！（2025年9月）本文已更新，包含最新的Gradio MCP功能，包括资源、提示词、增强身份验证等多项特性。

Gradio是一个每月被超过100万开发者使用的Python库，用于为机器学习模型构建界面。除了创建用户界面外，Gradio还提供API功能，并且现在——Gradio应用可以作为大语言模型的模型上下文协议（MCP）服务器启动。这意味着你的Gradio应用，无论是图像生成器、税务计算器还是其他任何应用，都可以被大语言模型作为工具调用。

本指南将展示如何仅用几行Python代码，使用Gradio构建MCP服务器。

### 前提条件

如果尚未安装，请安装包含MCP扩展的Gradio：

```bash
pip install "gradio[mcp]"
```

这将安装必要的依赖项，包括`mcp`包。你还需要一个支持使用MCP协议进行工具调用的LLM应用，例如Claude Desktop、Cursor或Cline（这些被称为"MCP客户端"）。

## 为什么要构建MCP服务器？

MCP服务器是一种标准化的工具暴露方式，以便大语言模型可以使用它们。MCP服务器可以为大语言模型提供各种额外能力，例如生成或编辑图像、合成音频，或执行特定计算（如数字的质因数分解）。

Gradio使得构建这些MCP服务器变得简单，可以将任何Python函数转换为大语言模型可用的工具。

## 示例：计算单词中的字母数量

众所周知，大语言模型不太擅长计算单词中的字母数量（例如，"strawberry"中"r"的数量）。但如果我们为它们配备一个工具来帮助呢？让我们从编写一个简单的Gradio应用开始，该应用计算单词或短语中的字母数量：

```python
import gradio as gr

def letter_counter(word, letter):
    """Count the occurrences of a specific letter in a word.
    
    Args:
        word: The word or phrase to analyze
        letter: The letter to count occurrences of
        
    Returns:
        The number of times the letter appears in the word
    """
    return word.lower().count(letter.lower())

demo = gr.Interface(
    fn=letter_counter,
    inputs=["text", "text"],
    outputs="number",
    title="Letter Counter",
    description="Count how many times a letter appears in a word"
)

demo.launch(mcp_server=True)
```

请注意，我们在`.launch()`中设置了`mcp_server=True`。这就是让你的Gradio应用作为MCP服务器所需的全部！现在，当你运行此应用时，它将：

1. 启动常规的Gradio Web界面
2. 启动MCP服务器
3. 在控制台中打印MCP服务器URL

MCP服务器将在以下地址可访问：

```
http://your-server:port/gradio_api/mcp/sse
```

Gradio自动将`letter_counter`函数转换为大语言模型可用的MCP工具。函数的文档字符串用于生成工具及其参数的描述。

你只需要将此URL端点添加到你的MCP客户端（例如Cursor、Cline或Tiny Agents），这通常意味着在设置中粘贴此配置：

```
{
  "mcpServers": {
    "gradio": {
      "url": "http://your-server:port/gradio_api/mcp/sse"
    }
  }
}
```

一些MCP客户端，特别是Claude Desktop，尚不支持基于SSE的MCP服务器。在这些情况下，你可以使用诸如`mcp-remote`的工具。首先安装Node.js。然后，将以下内容添加到你的MCP客户端配置中：

```
{
  "mcpServers": {
    "gradio": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://your-server:port/gradio_api/mcp/sse"
      ]
    }
  }
}
```

（顺便说一下，你可以通过访问Gradio应用页脚中的"View API"链接，然后点击"MCP"来找到确切的复制粘贴配置。）

![](/images/posts/c01c1004be19.png)

## 近期重大改进

Gradio最近为MCP服务器添加了几个强大功能。关于五项主要改进的详细概述，包括无缝本地文件支持、实时进度通知、OpenAPI到MCP转换、增强身份验证和可自定义工具描述，请查看我们的专门博客文章：Gradio MCP服务器的五大改进。

## 高级MCP功能

### MCP资源和提示词

除了工具之外，MCP还支持资源（用于暴露数据）和提示词（用于定义可重用模板）。Gradio提供了装饰器，可以轻松创建具备所有三种功能的MCP服务器。你可以在我们的专门指南中阅读更多信息，此处：

```python
import gradio as gr

@gr.mcp.tool()  
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@gr.mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@gr.mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting", 
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

demo = gr.TabbedInterface(
    [
        gr.Interface(add, [gr.Number(value=1), gr.Number(value=2)], gr.Number()),
        gr.Interface(get_greeting, gr.Textbox("Abubakar"), gr.Textbox()),
        gr.Interface(greet_user, [gr.Textbox("Abubakar"), gr.Dropdown(choices=["friendly", "formal", "casual"])], gr.Textbox()),
    ],
    ["Add", "Get Greeting", "Greet User"]
)

demo.launch(mcp_server=True)
```

### 仅MCP函数

Gradio还允许你使用`gr.api()`创建仅出现在MCP服务器中（不在用户界面中）的函数：

```python
import gradio as gr

def slice_list(lst: list, start: int, end: int) -> list:
    """
    A tool that slices a list given a start and end index.
    Args:
        lst: The list to slice.
        start: The start index.
        end: The end index.
    Returns:
        The sliced list.
    """
    return lst[start:end]

with gr.Blocks() as demo:
    gr.Markdown("This app includes MCP-only tools not visible in the UI.")
    gr.api(slice_list)

demo.launch(mcp_server=True)
```

## Gradio <> MCP集成的关键特性

1.  工具转换：您 Gradio 应用中的每个 API 端点都会自动转换为一个 MCP 工具，并具有相应的名称、描述和输入模式。要查看工具和模式，请访问 `http://your-server:port/gradio_api/mcp/schema` 或前往您 Gradio 应用页脚的 "View API" 链接，然后点击 "MCP"。Gradio 允许开发者使用简单的 Python 代码创建复杂的界面，这些界面提供动态的 UI 操作，以实现即时视觉反馈。
2.  环境变量支持。有两种方法可以启用 MCP 服务器功能：使用 `mcp_server` 参数，如上所示：`demo.launch(mcp_server=True)` 使用环境变量：`export GRADIO_MCP_SERVER=True`
3.  文件处理：服务器自动处理文件数据转换，包括：将 base64 编码的字符串转换为文件数据处理图像文件并以正确的格式返回管理临时文件存储自动文件上传 MCP 服务器，实现无缝的本地文件支持最近的 Gradio 更新通过引入类似 Photoshop 的缩放平移和完全透明度控制等功能，提升了其图像处理能力。
4.  性能分析：Gradio 自动跟踪并显示您所有 MCP 工具和 API 端点的性能指标。直接在 "View API" 页面查看成功率、延迟百分位数和请求计数，以帮助您和您的用户选择最可靠、最快的工具。指标采用颜色编码：绿色表示 100% 成功，红色表示 0% 成功，橙色表示介于两者之间的成功率。
5.  在 🤗 Spaces 上托管 MCP 服务器：您可以在 Hugging Face Spaces 上免费发布您的 Gradio 应用，从而获得一个免费的托管 MCP 服务器。Gradio 是一个更广泛生态系统的一部分，该生态系统包括用于以编程方式构建或查询机器学习应用的 Python 和 JavaScript 库。

工具转换：您 Gradio 应用中的每个 API 端点都会自动转换为一个 MCP 工具，并具有相应的名称、描述和输入模式。要查看工具和模式，请访问 `http://your-server:port/gradio_api/mcp/schema` 或前往您 Gradio 应用页脚的 "View API" 链接，然后点击 "MCP"。

Gradio 允许开发者使用简单的 Python 代码创建复杂的界面，这些界面提供动态的 UI 操作，以实现即时视觉反馈。

环境变量支持。有两种方法可以启用 MCP 服务器功能：

*   使用 `mcp_server` 参数，如上所示：

    ```python
    demo.launch(mcp_server=True)
    ```

*   使用环境变量：

    ```bash
    export GRADIO_MCP_SERVER=True
    ```

文件处理：服务器自动处理文件数据转换，包括：

*   将 base64 编码的字符串转换为文件数据
*   处理图像文件并以正确的格式返回
*   管理临时文件存储
*   自动文件上传 MCP 服务器，实现无缝的本地文件支持

最近的 Gradio 更新通过引入类似 Photoshop 的缩放平移和完全透明度控制等功能，提升了其图像处理能力。

性能分析：Gradio 自动跟踪并显示您所有 MCP 工具和 API 端点的性能指标。直接在 "View API" 页面查看成功率、延迟百分位数和请求计数，以帮助您和您的用户选择最可靠、最快的工具。指标采用颜色编码：绿色表示 100% 成功，红色表示 0% 成功，橙色表示介于两者之间的成功率。

在 🤗 Spaces 上托管 MCP 服务器：您可以在 Hugging Face Spaces 上免费发布您的 Gradio 应用，从而获得一个免费的托管 MCP 服务器。Gradio 是一个更广泛生态系统的一部分，该生态系统包括用于以编程方式构建或查询机器学习应用的 Python 和 JavaScript 库。

这是一个此类 Space 的示例：`https://huggingface.co/spaces/abidlabs/mcp-tools`。请注意，您可以将此配置添加到您的 MCP 客户端，以立即开始使用此 Space 中的工具：

```json
{
  "mcpServers": {
    "gradio": {
      "url": "https://abidlabs-mcp-tools.hf.space/gradio_api/mcp/sse"
    }
  }
}
```

## 私有 Spaces 认证

您也可以通过提供认证信息，将私有的 Huggingface Spaces 用作 MCP 服务器：

```json
{
  "mcpServers": {
    "gradio": {
      "url": "https://your-private-space.hf.space/gradio_api/mcp/sse",
      "headers": {
        "Authorization": "Bearer <YOUR-HUGGING-FACE-TOKEN>"
      }
    }
  }
}
```

## 结论

通过使用 Gradio 构建您的 MCP 服务器，您可以轻松地为您的 LLM（大语言模型）添加多种不同类型的自定义功能。凭借最近的改进，包括资源、提示词、更好的认证、文件处理和性能指标，Gradio 为构建复杂的 MCP 服务器提供了一个全面的平台。

## 延伸阅读

如果您想深入了解，我们推荐以下文章：

*   MCP 协议简介
*   Gradio 指南：使用 Gradio 构建 MCP 服务器
*   Gradio MCP 服务器的五大改进
*   使用 Gradio MCP 服务器提升您的 LLM（大语言模型）技能
*   在 Python 中实现 MCP 服务器：使用 Gradio 构建 AI 购物助手
*   额外指南：使用 Gradio 构建 MCP 客户端

---

> 本文由AI自动翻译，原文链接：[How to Build an MCP Server with Gradio](https://huggingface.co/blog/gradio-mcp)
> 
> 翻译时间：2026-04-21 05:06
