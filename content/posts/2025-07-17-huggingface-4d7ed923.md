---
title: Gradio MCP服务器五大升级：文件支持、进度通知、OpenAPI集成
title_original: Five Big Improvements to Gradio MCP Servers
date: '2025-07-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gradio-mcp-updates
author: ''
summary: Gradio 5.38.0版本为MCP服务器带来五项重要改进：新增本地文件上传支持，解决远程服务器文件输入难题；支持实时进度通知，便于监控AI任务状态；提供一行代码将OpenAPI规范转换为MCP工具，简化API集成流程；改进身份验证机制，通过gr.Header自动提取请求标头；优化MCP服务器开发体验。这些升级旨在让Gradio成为构建和托管AI驱动MCP服务器的最佳平台。
categories:
- AI基础设施
tags:
- Gradio
- MCP服务器
- AI开发工具
- API集成
- 开源框架
draft: false
translated_at: '2026-03-12T04:36:56.502994'
---

# Gradio MCP 服务器的五大重要改进

Gradio 是一个用于创建 AI 驱动的 Web 应用的开源 Python 包。Gradio 兼容 MCP 服务器协议，并为托管在 Hugging Face Spaces 上的数千个 MCP 服务器提供支持。Gradio 团队坚信，Gradio 和 Spaces 是构建和托管 AI 驱动的 MCP 服务器的最佳方式。

为此，我们在 5.38.0 版本中为 Gradio MCP 服务器添加了一些重大改进。

## 无缝的本地文件支持

如果你曾尝试使用一个需要文件（如图像、视频、音频）作为输入的远程 Gradio MCP 服务器，你可能遇到过这个错误：

![](/images/posts/fb2dec749d8e.png)

这是因为 Gradio 服务器托管在不同的机器上，意味着任何输入文件都必须可以通过公共 URL 访问，以便远程下载。

虽然在线托管文件的方法有很多，但它们都会给你的工作流程增加一个手动步骤。在 LLM Agent（智能体）时代，我们难道不应该期望它们为你处理这件事吗？

Gradio 现在包含一个"文件上传" MCP 服务器，Agent（智能体）可以使用它直接将文件上传到你的 Gradio 应用程序。如果你的 Gradio MCP 服务器中有任何工具需要文件输入，连接文档现在会向你展示如何启动"文件上传" MCP 服务器：

![](/images/posts/4ce2399816c2.png)

在 Gradio 指南中了解更多关于使用此服务器（以及重要的安全注意事项）的信息。

## 实时进度通知

根据 AI 任务的不同，获取结果可能需要一些时间。现在，Gradio 可以向你的 MCP 客户端流式传输进度通知，让你能够实时监控状态！

作为 MCP 开发者，强烈建议你实现你的 MCP 工具以发出这些进度状态。我们的指南向你展示了如何操作。

## 一行代码将 OpenAPI 规范转换为 MCP

如果你想将现有的后端 API 集成到 LLM（大语言模型）中，你必须手动将 API 端点映射到 MCP 工具。这可能是一项耗时且容易出错的工作。随着此版本的发布，Gradio 可以为你自动化整个过程！只需一行代码，你就可以将你的业务后端集成到任何兼容 MCP 的 LLM（大语言模型）中。

OpenAPI 是一个广泛采用的标准，用于以机器可读的格式（通常是 JSON 文件）描述 RESTful API。Gradio 现在具有 `gr.load_openapi` 函数，它可以直接从 OpenAPI 模式创建 Gradio 应用程序。然后，你可以使用 `mcp_server=True` 启动该应用，自动为你的 API 创建一个 MCP 服务器！

```python
import gradio as gr

demo = gr.load_openapi(
    openapi_spec="https://petstore3.swagger.io/api/v3/openapi.json",
    base_url="https://petstore3.swagger.io/api/v3",
    paths=["/pet.*"],
    methods=["get", "post"],
)

demo.launch(mcp_server=True)

```

在 Gradio 指南中查找更多详细信息。

## 身份验证的改进

MCP 服务器开发中的一个常见模式是使用身份验证标头来代表你的用户调用服务。作为 MCP 服务器开发者，你希望向用户清楚地说明他们需要提供哪些凭据才能正确使用服务器。

为了实现这一点，你现在可以将 MCP 服务器参数类型指定为 `gr.Header`。Gradio 将自动从传入请求中提取该标头（如果存在）并将其传递给函数。使用 `gr.Header` 的好处是，MCP 连接文档将自动显示连接到服务器时需要提供的标头！

在下面的示例中，`X-API-Token` 标头从传入请求中提取，并作为 `x_api_token` 参数传递给 `make_api_request_on_behalf_of_user`。

```python
import gradio as gr

def make_api_request_on_behalf_of_user(prompt: str, x_api_token: gr.Header):
    """Make a request to everyone's favorite API.
    Args:
        prompt: The prompt to send to the API.
    Returns:
        The response from the API.
    Raises:
        AssertionError: If the API token is not valid.
    """
    return "Hello from the API" if not x_api_token else "Hello from the API with token!"


demo = gr.Interface(
    make_api_request_on_behalf_of_user,
    [
        gr.Textbox(label="Prompt"),
    ],
    gr.Textbox(label="Response"),
)

demo.launch(mcp_server=True)

```

你可以在 Gradio 指南中阅读更多关于此功能的信息。

## 修改工具描述

Gradio 会根据你的函数名称和文档字符串自动生成工具描述。现在，你可以使用 `api_description` 参数进一步自定义工具描述。在此示例中，工具描述将显示为"对任何图像应用棕褐色滤镜。"

```python
import gradio as gr
import numpy as np

def sepia(input_img):
    """
    Args:
        input_img (np.array): The input image to apply the sepia filter to.

    Returns:
        The sepia filtered image.
    """
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

gr.Interface(sepia, "image", "image", 
             api_description="Apply a sepia filter to any image.")\
            .launch(mcp_server=True)

```

在指南中阅读更多信息。

## 结论

希望我们在 Gradio 中添加新的 MCP 相关功能吗？请在博客评论中或 GitHub 上告诉我们。另外，如果你构建了一个很酷的 MCP 服务器或 Gradio 应用，请在评论中告诉我们，我们会帮你宣传！

---

> 本文由AI自动翻译，原文链接：[Five Big Improvements to Gradio MCP Servers](https://huggingface.co/blog/gradio-mcp-updates)
> 
> 翻译时间：2026-03-12 04:36
