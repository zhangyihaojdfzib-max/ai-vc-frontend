---
title: smolagents新增视觉能力，赋能智能体浏览网页
title_original: We now support VLMs in smolagents!
date: '2025-01-24'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/smolagents-can-see
author: ''
summary: 文章介绍了smolagents框架新增的视觉语言模型（VLM）支持，使智能体能够处理图像信息。作者详细说明了两种传递图像的方式：在启动时一次性传递（适用于文档AI场景）和通过回调函数动态传递（适用于网页浏览等需要实时观察的场景）。文章还展示了如何利用helium和selenium构建一个具有视觉能力的网页浏览智能体，该智能体可以自主操作浏览器、识别图标和颜色等视觉元素，从而突破传统仅依赖文本的局限。
categories:
- AI产品
tags:
- smolagents
- 视觉语言模型
- 智能体
- 网页浏览
- 开源框架
draft: false
translated_at: '2026-05-28T06:10:16.545648'
---

# 我们刚刚为 smolagents 赋予了视觉

你这假冒为善的人，先去掉自己眼中的梁木，然后才能看得清楚，去掉你弟兄眼中的刺。——马太福音 7:3-5

## TL;DR

我们为 smolagents 增加了视觉支持，从而原生解锁了在 Agent（智能体）流程中使用视觉语言模型的能力。

- 概述
- 我们如何为 smolagents 赋予视觉
- 如何创建具有视觉能力的网页浏览 Agent（智能体）
- 后续步骤

## 概述

在 Agent（智能体）的世界中，许多能力都被一堵"视觉之墙"所遮蔽。一个常见的例子是网页浏览：网页包含丰富的视觉内容，仅通过提取文本永远无法完全还原这些内容，无论是对象的相对位置、通过颜色传递的信息，还是特定的图标……在这种情况下，视觉对于 Agent（智能体）来说是一项真正的超能力。因此，我们刚刚将这一能力添加到了我们的 smolagents 中！

预告一下这将带来什么：一个能够完全自主浏览网页的 Agent（智能体）浏览器！

以下是它的实际效果示例：

## 我们如何为 smolagents 赋予视觉

🤔 我们如何将图像传递给 Agent（智能体）？传递图像可以通过两种方式实现：

1. 可以在 Agent（智能体）启动时直接提供图像。这在文档 AI 场景中很常见。
2. 有时，图像需要动态添加。一个很好的例子是，当网页浏览器刚刚执行了一个操作，需要查看该操作在其视口中的影响。

#### 1. 在 Agent（智能体）启动时一次性传递图像

对于需要一次性传递图像的情况，我们在 `run` 方法中添加了向 Agent（智能体）传递图像列表的功能：`agent.run("Describe these images:", images=[image_1, image_2])`。

这些图像输入随后会与您要完成的任务的提示词一起，存储在 `TaskStep` 的 `task_images` 属性中。

运行 Agent（智能体）时，这些图像将被传递给模型。这在基于包含视觉元素的长 PDF 采取行动等场景中非常有用。

#### 2. 在每一步传递图像 ⇒ 使用回调函数

如何动态地将图像添加到 Agent（智能体）的记忆中？

要弄清楚这一点，我们首先需要了解我们的 Agent（智能体）是如何工作的。

smolagents 中的所有 Agent（智能体）都基于单一的 `MultiStepAgent` 类，该类是 ReAct 框架的抽象。在基本层面上，该类按照以下步骤循环执行操作，其中现有变量和知识被整合到 Agent（智能体）日志中，具体如下：

- **初始化**：系统提示词存储在 `SystemPromptStep` 中，用户查询记录在 `TaskStep` 中。
- **ReAct 循环（While）**：
  1. 使用 `agent.write_inner_memory_from_logs()` 将 Agent（智能体）日志写入 LLM 可读的聊天消息列表。
  2. 将这些消息发送给 `Model` 对象以获取其补全结果。解析补全结果以获取动作（对于 `ToolCallingAgent` 是 JSON 数据块，对于 `CodeAgent` 是代码片段）。
  3. 执行动作并将结果记录到记忆中（一个 `ActionStep`）。
  4. 在每一步结束时，运行 `agent.step_callbacks` 中定义的所有回调函数。
     ⇒ 这就是我们添加图像支持的地方：创建一个将图像记录到记忆中的回调函数！

下图详细说明了这一过程：

![](/images/posts/e432482133cd.png)

如您所见，对于动态获取图像的使用场景（例如网页浏览器 Agent（智能体）），我们支持将图像添加到模型的 `ActionStep` 中，具体位于属性 `step_log.observation_images`。

这可以通过一个回调函数来实现，该回调函数将在每一步结束时运行。

让我们演示如何创建这样一个回调函数，并使用它来构建一个网页浏览器 Agent（智能体）。👇👇

### 如何创建具有视觉能力的网页浏览 Agent（智能体）

我们将使用 `helium`。它提供了基于 `selenium` 的浏览器自动化功能：这将使我们的 Agent（智能体）更容易操作网页。

```bash
pip install "smolagents[all]" helium selenium python-dotenv

```

Agent（智能体）本身可以直接使用 helium，因此无需特定的工具：它可以直接使用 helium 执行操作，例如 `click("top 10")` 来点击页面上可见的名为 "top 10" 的按钮。
我们仍然需要制作一些工具来帮助 Agent（智能体）浏览网页：一个用于返回上一页的工具，另一个用于关闭弹出窗口的工具，因为这些窗口对于 helium 来说很难抓取，因为它们的关闭按钮上没有文本。

```python
from io import BytesIO
from time import sleep

import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from smolagents import CodeAgent, LiteLLMModel, OpenAIServerModel, TransformersModel, tool
from smolagents.agents import ActionStep


load_dotenv()
import os

@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    通过 Ctrl + F 在当前页面上搜索文本，并跳转到第 n 个匹配项。
    参数：
        text: 要搜索的文本
        nth_result: 要跳转到的匹配项序号（默认：1）
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(f"未找到第 {nth_result} 个匹配项（仅找到 {len(elements)} 个匹配项）")
    result = f"找到 {len(elements)} 个匹配 '{text}' 的结果。"
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"已聚焦到第 {nth_result} 个元素（共 {len(elements)} 个）"
    return result

@tool
def go_back() -> None:
    """返回上一页。"""
    driver.back()

@tool
def close_popups() -> str:
    """
    关闭页面上任何可见的模态框或弹出窗口。使用此工具来关闭弹出窗口！这不适用于 Cookie 同意横幅。
    """
    
    modal_selectors = [
        "button[class*='close']",
        "[class*='modal']",
        "[class*='modal'] button",
        "[class*='CloseButton']",
        "[aria-label*='close']",
        ".modal-close",
        ".close-modal",
        ".modal .close",
        ".modal-backdrop",
        ".modal-overlay",
        "[class*='overlay']"
    ]

    wait = WebDriverWait(driver, timeout=0.5)

    for selector in modal_selectors:
        try:
            elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )

            for element in elements:
                if element.is_displayed():
                    try:
                        
                        driver.execute_script("arguments[0].click();", element)
                    except ElementNotInteractableException:
                        
                        element.click()

        except TimeoutException:
            continue
        except Exception as e:
            print(f"处理选择器 {selector} 时出错：{str(e)}")
            continue
    return "模态框已关闭"

```

目前，Agent（智能体）还没有视觉输入。
因此，让我们演示如何通过使用回调函数，在其步骤日志中动态地为其提供图像。
我们创建一个名为 `save_screenshot` 的回调函数，该函数将在每一步结束时运行。

```python
def save_screenshot(step_log: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  
    driver = helium.get_driver()
    current_step = step_log.step_number
    if driver is not None:
        for step_logs in agent.logs:  
            if isinstance(step_log, ActionStep) and step_log.step_number <= current_step - 2:
                step_logs.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        step_log.observations_images = [image.copy()]  

    
    url_info = f"Current url: {driver.current_url}"
    step_log.observations = url_info if step_logs.observations is None else step_log.observations + "\n" + url_info
    return

```

这里最关键的一行是我们将图像添加到观察图像中：`step_log.observations_images = [image.copy()]`。

这个回调函数同时接受 `step_log` 和 `agent` 本身作为参数。将 `agent` 作为输入允许执行比仅修改最后日志更深入的操作。

让我们创建一个模型。我们已经在所有模型中添加了对图像的支持。
有一点需要注意：当将 TransformersModel 与 VLM 一起使用时，为了使其正常工作，你需要在初始化时将 `flatten_messages_as_text` 设置为 `False`，如下所示：

```py
model = TransformersModel(model_id="HuggingFaceTB/SmolVLM-Instruct", device_map="auto", flatten_messages_as_text=False)

```

对于这个演示，让我们通过 Fireworks API 使用一个更大的 Qwen2VL：

```py
model = OpenAIServerModel(
    api_key=os.getenv("FIREWORKS_API_KEY"),
    api_base="https://api.fireworks.ai/inference/v1",
    model_id="accounts/fireworks/models/qwen2-vl-72b-instruct",
)

```

现在让我们继续定义我们的 Agent（智能体）。我们将 `verbosity_level` 设置为最高，以显示 LLM（大语言模型）的完整输出消息，从而查看其思考过程，并将 `max_steps` 增加到 20，以便给 Agent（智能体）更多步骤来探索网页。
我们还为其提供了上面定义的 `save_screenshot` 回调函数。

```python
agent = CodeAgent(
    tools=[go_back, close_popups, search_item_ctrl_f],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks = [save_screenshot],
    max_steps=20,
    verbosity_level=2
)

```

最后，我们为 Agent（智能体）提供一些关于如何使用 helium 的指导。

```python
helium_instructions = """
你可以使用 helium 访问网站。不用担心 helium 驱动，它已经被管理好了。
首先你需要从 helium 导入所有内容，然后你可以执行其他操作！
代码：
```py
from helium import *
go_to('github.com/trending')
```<end_code>

你可以通过输入元素上显示的文本来直接点击可点击的元素。
代码：
```py
click("Top products")
```<end_code>

如果是链接：
代码：
```py
click(Link("Top products"))
```<end_code>

如果你尝试与某个元素交互但未找到，你会得到一个 LookupError。
通常，在每次点击按钮后停止你的操作，以查看截图上发生了什么。
永远不要尝试登录页面。

要向上或向下滚动，请使用 scroll_down 或 scroll_up，参数为要滚动的像素数。
代码：
```py
scroll_down(num_pixels=1200) # 这将向下滚动一个视口
```<end_code>

当出现带有叉号图标以关闭的弹出窗口时，不要尝试通过查找其元素或定位 'X' 元素来点击关闭图标（这通常会失败）。
只需使用你的内置工具 `close_popups` 来关闭它们：
代码：
```py
close_popups()
```<end_code>

你可以使用 .exists() 来检查元素是否存在。例如：
代码：
```py
if Text('Accept cookies?').exists():
    click('I accept')
```<end_code>

分几步进行，而不是试图一次性解决任务。
最后，只有当你得到答案时，才返回你的最终答案。
代码：
```py
final_answer("YOUR_ANSWER_HERE")
```<end_code>

如果页面似乎卡在加载中，你可能需要等待，例如 `import time` 并运行 `time.sleep(5.0)`。但不要过度使用！
要列出页面上的元素，不要尝试基于代码的元素搜索，如 'contributors = find_all(S("ol > li"))'：只需查看你最新的截图并直观地阅读它，或者使用你的工具 search_item_ctrl_f。
当然，你可以像用户导航时那样对按钮进行操作。
在你编写每个代码块之后，你将自动获得浏览器的最新截图和当前浏览器 URL。
但请注意，截图只会在整个操作结束时拍摄，它不会看到中间状态。
不要关闭浏览器。
"""

```

### 运行 Agent（智能体）

现在一切都准备好了：让我们运行我们的 Agent（智能体）！

```python
github_request = """
我想知道要付出多大努力才能让一个仓库出现在 github.com/trending 上。
你能导航到最热门仓库的顶级作者的资料页面，并告诉我他们过去一年的总提交次数吗？
"""

agent.run(github_request + helium_instructions)

```

但请注意，这个任务非常困难：取决于你使用的 VLM，它可能并不总是成功。像 Qwen2VL-72B 或 GPT-4o 这样的强大 VLM 成功率更高。

## 后续步骤

这将让你一窥支持视觉功能的 CodeAgent 的能力，但还有更多可以做的事情！

- 你可以从这里开始使用 Agent（智能体）网页浏览器。
- 在我们的公告博客文章中阅读更多关于 smolagents 的内容。
- 阅读 smolagents 文档。

我们期待看到你将使用视觉语言模型和 smolagents 构建什么！
```

---

> 本文由AI自动翻译，原文链接：[We now support VLMs in smolagents!](https://huggingface.co/blog/smolagents-can-see)
> 
> 翻译时间：2026-05-28 06:10
