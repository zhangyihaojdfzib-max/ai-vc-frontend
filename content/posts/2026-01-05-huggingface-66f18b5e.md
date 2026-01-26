---
title: NVIDIA发布DGX Spark与Reachy Mini，打造桌面智能体机器人
title_original: NVIDIA brings agents to life with DGX Spark and Reachy Mini
date: '2026-01-05'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia-reachy-mini
author: null
summary: NVIDIA在CES 2026上发布了一系列开源模型与工具，旨在推动智能体（Agent）在现实世界中的应用。文章重点介绍了如何结合DGX Spark的计算能力与Reachy
  Mini机器人硬件，通过NVIDIA NeMo Agent Toolkit等开源框架，构建一个能够对话、观察并执行动作的个性化桌面AI助手。内容提供了从环境配置、模型部署到系统集成的分步指南，强调该方案的开放性与可定制性，允许开发者自主控制模型、提示词及机器人行为，实现感知、推理与行动的融合。
categories:
- AI产品
tags:
- NVIDIA
- 智能体
- 机器人
- 开源模型
- 边缘AI
draft: false
translated_at: '2026-01-06T00:59:02.777Z'
---

NVIDIA通过DGX Spark与Reachy Mini将智能体带入现实
在2026年国际消费电子展上，NVIDIA发布了一系列全新的开源模型，旨在推动线上及现实世界中智能体的未来发展。从近期发布的NVIDIA Nemotron推理大语言模型，到全新的NVIDIA Isaac GR00T N1.6开源推理视觉语言模型，以及NVIDIA Cosmos世界基础模型——如今AI开发者构建专属智能体所需的所有基础组件均已就位。
但若能直接在办公桌上赋予你的智能体生命，会是怎样的体验？一个能为你提供帮助、并能私密处理数据的AI伙伴？
在今日的CES主题演讲中，黄仁勋向我们展示了如何借助NVIDIA DGX Spark的处理能力与Reachy Mini，创造属于你自己的小型办公室R2D2机器人，实现可对话、可协作的体验。
本篇博文将提供分步指南，帮助您在家中使用DGX Spark和Reachy Mini复现这一精彩体验。
让我们开始吧！

所需材料
若想立即着手实践，可在此获取演示源代码。
我们将使用以下组件：
- 推理模型：演示使用NVIDIA Nemotron 3 Nano
- 视觉模型：演示使用NVIDIA Nemotron Nano 2 VL
- 文本转语音模型：演示使用ElevenLabs
- Reachy Mini（或Reachy Mini仿真器）
- Python v3.10+环境，配备uv
您可自由调整方案并打造个性化版本——将模型集成至应用的方式多种多样：
- 本地部署——在自有硬件（DGX Spark或具备充足显存的GPU）上运行。我们的实现方案需要约65GB磁盘空间用于推理模型，约28GB用于视觉模型。
- 云端部署——通过NVIDIA Brev或Hugging Face推理终端在云端GPU部署模型。
- 无服务器模型终端——向NVIDIA或Hugging Face推理服务商发送请求。

赋予Reachy智能体能力
将AI智能体从简单的聊天界面转变为可自然交互的实体，能使对话体验更真实。当AI智能体能通过摄像头观察、语音输出并执行动作时，交互将更具沉浸感。这正是Reachy Mini所能实现的。
Reachy Mini设计为高度可定制。通过访问传感器、执行器和API，您可以轻松将其接入现有智能体技术栈，无论是通过仿真还是直接通过Python控制的实体硬件。
本文重点在于组合现有模块而非重新发明。我们融合了用于推理和视觉的开源模型、用于编排的智能体框架，以及用于执行动作的工具处理器。各组件松散耦合，便于更换模型、调整路由逻辑或添加新行为。
与封闭的个人助手不同，此设置保持完全开放。您可自主控制模型、提示词、工具及机器人行为。Reachy Mini仅作为智能体的物理终端，实现感知、推理与行动的融合。

构建智能体
在本示例中，我们使用NVIDIA NeMo Agent Toolkit——一个灵活、轻量、框架无关的开源库——将智能体所有组件连接起来。它能与LangChain、LangGraph、CrewAI等其他智能体框架无缝协作，处理模型间的交互、路由输入输出，并便于尝试不同配置或添加新功能而无需重写核心逻辑。该工具包还提供内置的性能分析与优化功能，让您能追踪跨工具和智能体的Token使用效率与延迟，识别瓶颈，并自动调优超参数以在降低成本和延迟的同时最大化准确性。

步骤0：设置并获取模型与服务访问权限
首先，克隆包含所有所需代码的存储库：
```
git clone git@github.com/brevdev/reachy-personal-assistant
cd reachy-personal-assistant
```
要访问由NVIDIA Nemotron模型驱动的智能层，您可通过NVIDIA NIM或vLLM部署模型，或通过build.nvidia.com提供的远程终端连接。
以下说明假设您通过终端访问Nemotron模型。在主目录中创建包含API密钥的.env文件。若进行本地部署则无需指定API密钥，可跳过此步骤。
```
NVIDIA_API_KEY=your_nvidia_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

步骤1：构建聊天界面
首先通过NeMo Agent Toolkit的API服务器运行基础的大语言模型聊天工作流。NeMo Agent Toolkit支持通过`nat serve`命令并提供配置文件来运行工作流。此处传递的配置文件包含智能体所需的所有设置信息，涵盖聊天用模型、图像理解模型以及智能体使用的路由模型。NeMo Agent Toolkit UI可通过HTTP/WebSocket连接，让您能像使用标准聊天产品一样与工作流对话。本实现方案中，NeMo Agent Toolkit服务器启动在8001端口（以便机器人和UI均可调用）：
```
cd nat
uv venv
uv sync
uv run --env-file ../.env nat serve --config_file src/ces_tutorial/config.yml --port 8001
```
接下来，通过独立终端发送纯文本提示词以验证一切设置正确：
```
curl -s http://localhost:8001/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"model": "test", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```
查看智能体配置时，您会注意到其定义的能力远超出简单聊天补全。后续步骤将详细解析这些内容。

步骤2：添加NeMo Agent Toolkit内置的ReAct智能体以实现工具调用
工具调用是AI智能体的核心功能。NeMo Agent Toolkit包含内置的ReAct智能体，可在工具调用间进行推理并在回答前使用多个工具。我们将“动作请求”路由至允许调用工具的ReAct智能体（例如触发机器人行为或获取当前机器人状态的工具）。
需注意的实践要点：
- 保持工具架构紧凑（清晰的名称/描述/参数），因为这是智能体决定调用的依据。
- 对步骤数设置硬性上限（max_tool_calls），防止智能体陷入循环。
- 若使用实体机器人，对于物理动作可考虑“执行前确认”模式以确保运动安全。
查看配置文件中定义工具（如维基百科搜索）并指定管理工具的ReAct智能体模式的部分：
```
functions:
  wikipedia_search:
    _type: wiki_search
    max_results: 2
..
react_agent:
  _type: react_agent
  llm_name: agent_llm
  verbose: true
  parse_agent_response_max_retries: 3
  tool_names: [wikipedia_search]
workflow:
  _type: ces_tutorial_router_agent
  agent: react_agent
```

步骤3：添加路由器以将查询定向至不同模型
核心思路：不同任务使用不同模型。基于意图进行路由：
- 文本查询使用快速文本模型
- 视觉查询必须通过视觉语言模型处理
- 动作/工具请求路由至ReAct智能体+工具
可通过多种方式实现路由（启发式规则、轻量级分类器或专用路由服务）。

如果您想要这个想法的“生产”版本，NVIDIA LLM Router 开发者示例是完整的参考实现，并包含了评估和监控模式。
一个基本的路由策略可能如下工作：
- 如果用户询问关于其环境的问题，则将请求连同从摄像头（或 Reachy）捕获的图像一起发送给 VLM。
- 如果用户询问需要实时信息的问题，则将输入发送给 ReACT Agent，以通过工具调用执行网络搜索。
- 如果用户询问简单问题，则将请求发送给为闲聊优化的、小而快的模型。
配置的这些部分定义了路由拓扑并指定了路由器模型。
functions:
..
router:
_type: router
route_config:
- name: other
description: 任何需要仔细思考、外部信息、图像理解或调用工具来执行操作的问题。
- name: chit_chat
description: 任何简单的闲聊、寒暄或随意对话。
- name: image_understanding
description: 需要助手看到用户的问题，例如关于其外貌、环境、场景或周围事物的问题。例如：我拿着什么、我穿着什么、我看起来怎么样、我周围有什么、白板上写着什么。关于着装的问题，例如：我的衬衫/帽子/夹克等是什么颜色。
llm_name: routing_llm
llms:
..
routing_llm:
_type: nim
model_name: microsoft/phi-3-mini-128k-instruct
temperature: 0.0
注意：如果您想降低延迟/成本或离线运行，可以自托管其中一个被路由的模型（通常是“快速文本”模型），并保持 VLM 远程运行。一种常见的方法是通过 NVIDIA NIM 或 vLLM 提供服务，并将 NeMo Agent Toolkit 指向一个 OpenAI 兼容的端点。

第 4 步：添加 Pipecat 机器人以实现实时语音 + 视觉
现在我们进入实时阶段。Pipecat 是一个为低延迟语音/多模态 Agent 设计的框架：它协调音频/视频流、AI 服务和传输，以便您可以构建自然的对话。在此代码库中，机器人服务负责：
- 捕获视觉（机器人摄像头）
- 语音识别 + 文本转语音
- 协调机器人运动和表情行为
您可以在 `reachy-personal-assistant/bot` 文件夹中找到所有 pipecat 机器人代码。

第 5 步：将所有内容连接到 Reachy（硬件或模拟）
Reachy Mini 公开了一个守护进程，系统的其余部分会连接到它。代码库默认在模拟中运行该守护进程（--sim）。如果您有真实的 Reachy，可以移除此标志，相同的代码将控制您的机器人。

运行完整系统
您需要三个终端来运行整个系统：
终端 1：Reachy 守护进程
cd bot
# macOS:
uv run mjpython -m reachy_mini.daemon.app.main --sim --no-localhost-only
# Linux:
uv run -m reachy_mini.daemon.app.main --sim --no-localhost-only
如果您使用物理硬件，请记得从命令中省略 --sim 标志。

终端 2：机器人服务
cd bot
uv venv
uv sync
uv run --env-file ../.env python main.py

终端 3：NeMo Agent Toolkit 服务
如果 NeMo Agent Toolkit 服务在第 1 步后尚未运行，现在请在终端 3 中启动它。
cd nat
uv venv
uv sync

所有终端设置完成后，有两个主要窗口需要关注：
Reachy 模拟器 – 当您在终端 1 启动模拟器守护进程时，此窗口会自动出现。如果您正在运行 Reachy mini 模拟器来代替物理设备，则适用此情况。
Pipecat Playground – 这是客户端 UI，您可以在此连接到 Agent、启用麦克风和摄像头输入并查看实时转录。在终端 2 中，打开机器人服务暴露的 URL：http://localhost:7860/。在浏览器中点击“连接”。初始化可能需要几秒钟，系统会提示您授予麦克风（以及可选的摄像头）访问权限。

两个窗口都启动并运行后：
- 客户端和 Agent 状态指示器应显示为“就绪”
- 机器人将用欢迎信息问候您：“您好，我今天能为您提供什么帮助？”

此时，您可以开始与您的 Agent 互动了！

尝试这些示例提示词
以下是一些简单的提示词，可帮助您测试您的个人助手。您可以从这些开始，然后尝试添加自己的提示词，看看 Agent 如何回应！
纯文本提示词（路由到快速文本模型）
- “用一句话解释你能做什么。”
- “总结我最后说的话。”
视觉提示词（路由到 VLM）
- “我正对着摄像头举着什么？”
- “阅读此页面上的文字并总结它。”

后续方向
这并非一个“黑盒”助手，而是为您构建了一个私有的、可定制的系统基础，您可以同时控制其智能和硬件。您可以在本地检查、扩展和运行它，完全了解数据流、工具权限以及机器人如何感知和行动。
根据您的目标，以下是接下来可以探索的几个方向：
- 性能优化：使用 LLM Router 开发者示例，通过智能地在不同模型之间引导查询，来平衡成本、延迟和质量。
- 查看使用 Nemotron 开源模型构建带有防护栏的语音驱动 RAG Agent 的教程。
- 掌握硬件：探索 Reachy Mini SDK 和模拟文档，在部署到物理系统之前设计和测试高级机器人行为。
- 探索并为社区为 Reachy 构建的应用程序做出贡献。

想立即尝试吗？在此处部署完整环境。一键点击，即可运行。


> 本文由AI自动翻译，原文链接：[NVIDIA brings agents to life with DGX Spark and Reachy Mini](https://huggingface.co/blog/nvidia-reachy-mini)
> 
> 翻译时间：2026-01-06 00:59
