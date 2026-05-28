---
title: Reachy Mini实现完全本地化语音交互
title_original: Reachy Mini goes fully local
date: '2026-05-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/local-reachy-mini-conversation
author: ''
summary: 本文介绍了如何为Reachy Mini机器人部署完全本地的语音对话系统，无需云端或API密钥。技术栈采用级联式语音到语音流水线（VAD→STT→LLM→TTS），通过speech-to-speech库和llama.cpp在本地运行。推荐使用Gemma
  4、Silero VAD、Parakeet-TDT STT和Qwen3-TTS等组件。文章详细说明了从LLM服务部署到机器人连接的完整步骤，并强调本地化带来的隐私保护、零API成本和组件可替换性三大优势。
categories:
- AI产品
tags:
- Reachy Mini
- 本地化部署
- 语音交互
- 开源AI
- 机器人
draft: false
translated_at: '2026-05-28T06:09:47.700066'
---

# Reachy Mini 实现完全本地化

构建完 Reachy Mini 后，您将安装对话应用并开始与它交谈。在此之前，您需要将音频发送到服务器。但现在不再需要了。今天我们将带您在本地运行整个技术栈。

该技术栈由 speech-to-speech 驱动，这是我们级联的 VAD → STT → LLM → TTS 流水线，它暴露了一个兼容 Realtime API 的 /v1/realtime WebSocket。启动后端后，从 UI 将机器人指向它。

级联是当今开源领域中最灵活的选择，并且使用合适的组件，它们也是最快的。我们会推荐我们最喜欢的组件，但级联的重点在于您可以替换它们。每周都有新模型发布。

TL;DR

- 为您的 Reachy Mini 部署本地语音后端。
- 我们使用 speech-to-speech 库，这是一种级联方法。
- 推荐：llama.cpp 搭配 Gemma 4、Silero VAD、Parakeet-TDT 0.6B v3 STT、Qwen3-TTS。

## 快速开始

这篇博客将带您了解如何完全在本地与 Reachy Mini 进行对话。无需云端，无需 API 密钥，数据不会离开您的机器。以下是展示此过程的视频：

### 本地提供 LLM 服务

为了提供 LLM 服务，我们将使用 Hugging Face 的 llama.cpp。如果您需要安装它，最简单的方式是 brew install llama.cpp 或 winget install llama.cpp，更多帮助请查阅文档。
首先，我们将运行：

```bash
llama-server -hf ggml-org/gemma-4-E4B-it-GGUF -np 2 -c 65536 -fa on --swa-full

```

完成！第一次会下载模型，后续启动会很快。

- -hf ggml-org/gemma-4-E4B-it-GGUF — 直接从 Hub 拉取模型。首次运行下载，后续运行使用缓存。
- -np 2 — 两个并行槽位。让服务器处理第二个请求（例如快速中断）而不会阻塞第一个请求。
- -c 65536 — 64k 上下文窗口，跨槽位共享。为长对话提供充足空间。
- -fa on — 闪存注意力。更快且内存占用更低，在现代硬件上基本免费。
- --swa-full — 保留完整的滑动窗口注意力缓存，而不是重新计算。以少量 RAM 换取 Gemma 上明显更快的提示词处理。

### 设置 speech-to-speech

我们首先安装该库

```bash
uv pip install speech-to-speech

```

然后，在另一个终端中运行 LLM 服务的同时，我们可以简单地运行：

```bash
speech-to-speech --responses_api_base_url "http://127.0.0.1:8080" --responses_api_api_key "" --mode local

```

然后您就可以通过终端与模型对话了！第一次需要下载 Parakeet-TDT 0.6B v3 和 Qwen3TTS，但后续启动会很快。

以下是展示本地对话模式的视频：

现在，在您尝试了 --mode local 之后，您可以不带该选项再次运行命令，以便为机器人提供 speech-to-speech 服务。

### 将 Reachy Mini 连接到 speech-to-speech

一旦 llama.cpp 和 speech-to-speech 运行起来，您就可以使用桌面应用启动机器人并启动对话应用。在对话应用的 UI 中，您需要通过点击 HF 后端中的 "edit connection" 来选择本地模式。以下是展示如何操作的视频：

这样就完成了。您可以开始与您的机器人对话了。流水线的每个阶段都是一种权衡：有更快但质量较低的 TTS 模型，也有更慢但质量更高的 STT 模型。我们针对多语言进行了优化，而您可能希望针对单一语言进行优化。博客的其余部分将介绍如何进行自定义。

## 深入探讨

### 为什么运行您自己的 Speech-to-Speech 服务器？

托管的实时后端很方便，但运行您自己的引擎可以解锁三件事：

- 隐私。音频永远不会离开您的网络，整个流水线在您控制的硬件上运行。
- 无 API 成本。无需按分钟或按 Token 付费。
- 完全控制流水线。替换任何组件：VAD、STT、LLM、TTS。每当 Hub 🤗 上有更好的东西出现时。

speech-to-speech 仓库通过一个 CLI 为您提供所有这些功能。它在 /v1/realtime 启动一个 WebSocket 服务器，该服务器使用 Reachy Mini 已经知道如何通信的相同协议。

### 我们的主观默认设置：VAD、STT、TTS

级联语音流水线有四个阶段：VAD、STT、LLM 和 TTS。对于其中三个，我们选择了可靠的默认设置，以便您可以专注于 LLM：

我们对这些选择有主观偏好，如果您有自己的偏好，可以随意替换它们。

### 选择您的 LLM

LLM 是对系统延迟和整体性能影响最大的层。我们支持两种选项：在本地运行模型（llama.cpp、MLX、Transformers、vLLM），或使用支持 Responses API 的服务器（OpenAI、Gemini、HF Inference Endpoints、llama.cpp、vLLM 等）。

#### Responses API：将大脑与语音循环解耦

系统的主要瓶颈是 LLM 推理延迟。为了解决这个问题，我们支持通过 Responses API 协议暴露的外部推理引擎。

因此，speech-to-speech 引擎支持第二种模式，即只要 LLM 使用 Responses API 协议，它就可以在单独的进程中运行。您在一个终端中启动模型服务器，在另一个终端中启动语音循环，两者通过 HTTP 通信。

##### 选项 1：一个终端中运行 llama.cpp，另一个终端中运行 speech-to-speech

终端 1：llama.cpp 服务器：

```bash
llama-server -hf ggml-org/gemma-4-E4B-it-GGUF -np 2 -c 65536 -fa on --swa-full

```

终端 2：speech-to-speech 客户端：

```bash
speech-to-speech \
  --mode realtime \
  --stt parakeet-tdt \
  --tts qwen3 \
  --llm_backend responses-api \
  --model_name "unsloth/Qwen3-4B-Instruct-2507-GGUF" \
  --responses_api_base_url "http://127.0.0.1:8080/v1"

```

##### 选项 2：一个终端中运行 vLLM，另一个终端中运行 speech-to-speech

需要 vLLM ≥ 0.21.0。对 Responses API 协议的完整支持，包括 speech-to-speech 后端使用的工具调用流式传输，已在 vLLM 0.21.0 中实现。旧版本可以启动，但一旦助手尝试调用工具就会出错。

通过 vLLM 为此流水线提供模型服务时，三个标志是必需的：

- --enable-auto-tool-choice
- --tool-call-parser <tool_parser_name> — 选择按系列划分的解析器，将模型的原始输出转换为结构化的工具调用（例如，Qwen3 指令模型使用 qwen3_coder，Llama 3 使用 llama3_json，Hermes 风格模型使用 hermes，...）。
- --default-chat-template-kwargs '{"enable_thinking":false}'：为支持该功能的模型禁用 <think> 推理通道。对于更困难的 Agent 任务，您可以将其设置为 true 并让模型进行推理，但对于自然的对话体验，我们强烈建议保持关闭：每个思考 Token 都是用户在机器人开始说话之前听到的静默延迟。

终端 1：vLLM 推理服务器（Qwen/Qwen3-4B-Instruct-2507）：

```bash
vllm serve Qwen/Qwen3-4B-Instruct-2507 \
  --port 8000 \
  --host 127.0.0.1 \
  --max-model-len 32768 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --default-chat-template-kwargs '{"enable_thinking":false}' \
  --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":1}'

```

--speculative-config 行启用了多 Token 预测（MTP）。它是可选的，但对端到端延迟有很大影响。只要模型支持，就保持启用。

```bash
speech-to-speech \
  --mode realtime \
  --stt parakeet-tdt \
  --tts qwen3 \
  --llm_backend responses-api \
  --model_name "Qwen/Qwen3-4B-Instruct-2507" \
  --responses_api_base_url "http://127.0.0.1:8000/v1"

```

##### 选项 3：Hugging Face Inference Endpoints

相同的协议，但模型在 Hugging Face 上的托管 GPU 上运行。将任何聊天模型部署为 Inference Endpoint，然后将语音循环指向端点 URL：

```bash
speech-to-speech \
  --mode realtime \
  --stt parakeet-tdt \
  --tts qwen3 \
  --llm_backend responses-api \
  --model_name "Qwen/Qwen3-4B-Instruct-2507" \
  --responses_api_base_url "https://<your-endpoint>.endpoints.huggingface.cloud/v1" \
  --responses_api_api_key "$HF_TOKEN"

```

##### 选项 4：Hugging Face Inference Providers

如果你不想管理自己的端点，可以使用**推理提供商**。Hugging Face 通过单一URL将你的请求路由到第三方后端（例如 Together、Fireworks、Replicate）：

```bash
speech-to-speech \
  --mode realtime \
  --stt parakeet-tdt \
  --tts qwen3 \
  --llm_backend responses-api \
  --model_name "Qwen/Qwen3.6-35B-A3B:deepinfra" \
  --responses_api_base_url "https://router.huggingface.co/v1" \
  --responses_api_api_key "$HF_TOKEN"

```

##### 选项5：OpenAI（或任何兼容OpenAI的提供商）

当你希望以零基础设施测试前沿模型时，可将相同的标志指向OpenAI：

```bash
speech-to-speech \
  --mode realtime \
  --stt parakeet-tdt \
  --tts qwen3 \
  --llm_backend responses-api \
  --model_name "gpt-5.4" \
  --responses_api_api_key "$OPENAI_API_KEY"

```

`--responses_api_*`标志对于任何实现该协议的提供商（OpenRouter、Together、Fireworks等）都同样适用。只需更换基础URL和API密钥，其余管道保持不变。

#### 在进程中运行LLM

##### 选项1：在MLX上运行本地LLM（Apple Silicon）

如果你使用的是Mac，MLX是以合理延迟运行真实模型的最低门槛方式。我们推荐`Qwen3-4B-Instruct-2507`，它在M系列芯片上足够小以实现即时响应，同时具备进行对话的能力。

```bash
speech-to-speech \
  --llm_backend mlx-lm \
  --model_name "mlx-community/Qwen3-4B-Instruct-2507-bf16"

```

服务器默认监听`ws://127.0.0.1:8765/v1/realtime`。保持其运行，将对话应用连接到本地后端，你就可以与你的机器人对话了。

##### 选项2：在Transformers上运行本地LLM（CUDA / CPU / MPS）

思路相同，但使用原生`transformers`。如果你使用CUDA设备、Linux系统，或者希望自由更换模型而无需为MLX重新转换权重，请使用此选项。

```bash
speech-to-speech \
  --llm_backend transformers \
  --model_name "Qwen/Qwen3-4B-Instruct-2507"

```

提示：`Qwen3-4B-Instruct-2507`是LLM的另一个好选择，因为它在单块消费级GPU上实现了良好的速度与质量平衡。你可以将`--model_name`指向后端支持的任何HF模型——例如更大的Gemma、Qwen或Mistral。

### 在笔记本上运行引擎，在机器人上运行应用

如果你在笔记本上运行语音引擎，在Reachy Mini Wireless上运行对话应用，唯一需要改变的是URL。确保引擎绑定到局域网地址（不仅仅是`127.0.0.1`），并在UI中选择IP时使用机器人的笔记本IP。

如果你不知道自己的IP，以下是查找方法：

```bash
ipconfig getifaddr en0    
ipconfig getifaddr en1    

```

```bash
hostname -I

```

在活动适配器下查找"IPv4 Address"。

你需要的是`192.168.x.x`或`10.x.x.x`的地址。如果看到`169.254.x.x`，说明你实际上并未连接到网络。

## 总结

你现在拥有了一个完全本地的语音循环：

- 机器人通过**Silero**进行监听，
- 通过**Parakeet-TDT 0.6B v3**进行转录，
- 通过你选择的LLM进行思考——无论是本地的MLX、本地的Transformers、隔壁的vLLM或llama.cpp服务器，还是托管的Responses API端点，
- 并通过**Qwen3-TTS**进行回答。

请为`huggingface/speech-to-speech`和`pollen-robotics/reachy_mini_conversation_app`加星标，并在讨论区告诉我们你最终在机器人上运行了哪个开源级联方案。

---

> 本文由AI自动翻译，原文链接：[Reachy Mini goes fully local](https://huggingface.co/blog/local-reachy-mini-conversation)
> 
> 翻译时间：2026-05-28 06:09
