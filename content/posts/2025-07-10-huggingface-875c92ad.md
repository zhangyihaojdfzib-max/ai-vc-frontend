---
title: ScreenEnv：一键部署全栈桌面AI智能体的Docker沙盒
title_original: 'ScreenEnv: Deploy your full stack Desktop Agent'
date: '2025-07-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/screenenv
author: ''
summary: ScreenEnv是一个Python库，用于在Docker容器中创建隔离的Ubuntu桌面环境，专门用于测试和部署GUI智能体（计算机使用智能体）。它提供完整的桌面控制能力，包括鼠标键盘自动化、窗口管理和屏幕录制，并支持直接沙盒API和模型上下文协议两种集成模式，使开发者能够轻松构建和部署能与真实应用程序交互的AI智能体。该工具简化了传统复杂的虚拟机设置，实现了快速、可复现的部署。
categories:
- AI基础设施
tags:
- 桌面自动化
- AI智能体
- Docker
- 沙盒环境
- MCP协议
draft: false
translated_at: '2026-03-14T04:46:31.038014'
---

# ScreenEnv：部署您的全栈桌面智能体

TL;DR：ScreenEnv 是一个强大的 Python 库，可让您在 Docker 容器中创建隔离的 Ubuntu 桌面环境，用于测试和部署 GUI 智能体（又称计算机使用智能体）。凭借对模型上下文协议的内置支持，部署能够查看、点击并与真实应用程序交互的桌面智能体变得前所未有的简单。

## 什么是 ScreenEnv？

想象一下，您需要自动化桌面任务、测试 GUI 应用程序或构建一个能与软件交互的 AI 智能体。过去这需要复杂的虚拟机设置和脆弱的自动化框架。

ScreenEnv 通过提供一个在 Docker 容器中运行的**沙盒化桌面环境**改变了这一切。您可以将其视为一个完整的虚拟桌面会话，您的代码可以完全控制它——不仅仅是点击按钮和输入文本，而是管理整个桌面体验，包括启动应用程序、组织窗口、处理文件、执行终端命令以及录制整个会话。

## 为什么选择 ScreenEnv？

- 🖥️ **完整的桌面控制**：完整的鼠标和键盘自动化、窗口管理、应用程序启动、文件操作、终端访问和屏幕录制
- 🤖 **双重集成模式**：同时支持用于 AI 系统的模型上下文协议和直接的沙盒 API——适应任何智能体或后端逻辑
- 🐳 **原生 Docker**：无需复杂的虚拟机设置——只需 Docker。环境是隔离的、可复现的，并且可以在不到 10 秒的时间内轻松部署到任何地方。支持 AMD64 和 ARM64 架构。

### 🎯**一行代码设置**

```python
from screenenv import Sandbox
sandbox = Sandbox()  

```

## 两种集成方法

ScreenEnv 提供了**两种互补的方式**来与您的智能体和后端系统集成，让您能够灵活选择最适合您架构的方法：

### 选项 1：直接沙盒 API

非常适合自定义智能体框架、现有后端或当您需要细粒度控制时：

```python
from screenenv import Sandbox


sandbox = Sandbox(headless=False)
sandbox.launch("xfce4-terminal")
sandbox.write("echo 'Custom agent logic'")
screenshot = sandbox.screenshot()
image = Image.open(BytesIO(screenshot_bytes))
...
sandbox.close()


```

### 选项 2：MCP 服务器集成

非常适合支持模型上下文协议的 AI 系统：

```python
from screenenv import MCPRemoteServer
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


server = MCPRemoteServer(headless=False)
print(f"MCP Server URL: {server.server_url}")


async def mcp_session():
    async with streamablehttp_client(server.server_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            print(await session.list_tools())

            response = await session.call_tool("screenshot", {})
            image_bytes = base64.b64decode(response.content[0].data)
            image = Image.open(BytesIO(image_bytes))

server.close()


```

这种双重方法意味着 ScreenEnv 会适应您现有的基础设施，而不是强迫您改变智能体架构。

## ✨ 使用 screenenv 和 smolagents 创建桌面智能体

screenenv 原生支持 smolagents，使得构建您自己的自定义桌面智能体进行自动化变得轻而易举。以下是如何仅用几个步骤创建您自己的 AI 驱动的桌面智能体：

### 1. 选择您的模型

选择您希望为智能体提供支持的后端 VLM。

```python
import os

from smolagents import OpenAIServerModel
model = OpenAIServerModel(
    model_id="gpt-4.1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


from smolagents import HfApiModel
model = HfApiModel(
    model_id="Qwen/Qwen2.5-VL-7B-Instruct",
    token=os.getenv("HF_TOKEN"),
    provider="nebius",
)


from smolagents import TransformersModel
model = TransformersModel(
    model_id="Qwen/Qwen2.5-VL-7B-Instruct",
    device_map="auto",
    torch_dtype="auto",
    trust_remote_code=True,
)


from smolagents import LiteLLMModel
model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514")



```

### 2. 定义您的自定义桌面智能体

从 `DesktopAgentBase` 继承并实现 `_setup_desktop_tools` 方法来构建您自己的动作空间！

```python
from screenenv import DesktopAgentBase, Sandbox
from smolagents import Model, Tool, tool
from smolagents.monitoring import LogLevel
from typing import List

class CustomDesktopAgent(DesktopAgentBase):
    """Agent for desktop automation"""

    def __init__(
        self,
        model: Model,
        data_dir: str,
        desktop: Sandbox,
        tools: List[Tool] | None = None,
        max_steps: int = 200,
        verbosity_level: LogLevel = LogLevel.INFO,
        planning_interval: int | None = None,
        use_v1_prompt: bool = False,
        **kwargs,
    ):
        super().__init__(
            model=model,
            data_dir=data_dir,
            desktop=desktop,
            tools=tools,
            max_steps=max_steps,
            verbosity_level=verbosity_level,
            planning_interval=planning_interval,
            use_v1_prompt=use_v1_prompt,
            **kwargs,
        )

        
        
        
        
        

    def _setup_desktop_tools(self) -> None:
        """Define your custom tools here."""
        
        
        @tool
        def click(x: int, y: int) -> str:
            """
            Clicks at the specified coordinates.
            Args:
                x: The x-coordinate of the click
                y: The y-coordinate of the click
            """
            self.desktop.left_click(x, y)
            
            return f"Clicked at ({x}, {y})"
        
        self.tools["click"] = click
        

        @tool
        def write(text: str) -> str:
            """
            Types the specified text at the current cursor position.
            Args:
                text: The text to type
            """
            self.desktop.write(text, delay_in_ms=10)
            return f"Typed text: '{text}'"

        self.tools["write"] = write

        @tool
        def press(key: str) -> str:
            """
            Presses a keyboard key or combination of keys
            Args:
                key: The key to press (e.g. "enter", "space", "backspace", etc.) or a multiple keys string to press, for example "ctrl+a" or "ctrl+shift+a".
            """
            self.desktop.press(key)
            return f"Pressed key: {key}"

        self.tools["press"] = press
        
        @tool
        def open(file_or_url: str) -> str:
            """
            Directly opens a browser with the specified url or opens a file with the default application.
            Args:
                file_or_url: The URL or file to open
            """

            self.desktop.open(file_or_url)
            
            self.logger.log(f"Opening: {file_or_url}")
            return f"Opened: {file_or_url}"

        @tool
        def launch_app(app_name: str) -> str:
            """
            Launches the specified application.
            Args:
                app_name: The name of the application to launch
            """
            self.desktop.launch(app_name)
            return f"Launched application: {app_name}"

        self.tools["launch_app"] = launch_app

        ... 

```

### 3. 在桌面任务上运行智能体

```python
from screenenv import Sandbox


sandbox = Sandbox(headless=False, resolution=(1920, 1080))


agent = CustomDesktopAgent(
    model=model,
    data_dir="data",
    desktop=sandbox,
)


task = "Open LibreOffice, write a report of approximately 300 words on the topic ‘AI Agent Workflow in 2025’, and save the document."

result = agent.run(task)
print(f"📄 Result: {result}")

sandbox.close()

```

如果您遇到 Docker 访问被拒绝的错误，可以尝试使用 `sudo -E python -m test.py` 运行智能体，或者将您的用户添加到 `docker` 组。

💡 有关完整的实现，请参阅 GitHub 上的这个 `CustomDesktopAgent` 源代码。

## 立即开始使用

```bash

pip install screenenv


git clone git@github.com:huggingface/screenenv.git
cd screenenv
python -m examples.desktop_agent


```

## 下一步计划？

ScreenEnv 的目标是超越 Linux，扩展到支持 Android、macOS 和 Windows，从而解锁真正的跨平台图形用户界面自动化。这将使开发者和研究人员能够构建只需最少设置即可在不同环境中通用的 Agent（智能体）。

这些进展为创建**可复现的、沙盒化的环境**铺平了道路，这种环境非常适合进行基准测试和评估。

代码仓库：https://github.com/huggingface/screenenv

---

> 本文由AI自动翻译，原文链接：[ScreenEnv: Deploy your full stack Desktop Agent](https://huggingface.co/blog/screenenv)
> 
> 翻译时间：2026-03-14 04:46
