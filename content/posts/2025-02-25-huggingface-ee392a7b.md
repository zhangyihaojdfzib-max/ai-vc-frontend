---
title: FastRTC：Python实时通信库发布
title_original: 'FastRTC: The Real-Time Communication Library for Python'
date: '2025-02-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/fastrtc
author: ''
summary: FastRTC是一个专为Python设计的实时通信库，旨在简化构建实时音频和视频AI应用的流程。文章指出，尽管实时语音模型（如OpenAI的ChatGPT、Google的Gemini、Kyutai的Moshi等）和融资活动爆发式增长，但Python开发者仍面临构建流式传输音频/视频应用的困难。FastRTC提供了内置自动语音检测、轮流发言、Gradio
  UI支持、电话呼叫、WebRTC和WebSocket支持等功能，让开发者只需关注业务逻辑。文章通过构建实时音频回显和LLM语音聊天示例，展示了FastRTC的易用性和强大功能。
categories:
- AI基础设施
tags:
- FastRTC
- 实时通信
- Python库
- 语音AI
- WebRTC
draft: false
translated_at: '2026-05-11T05:59:06.387184'
---

# FastRTC：Python 实时通信库

在过去几个月里，许多新的实时语音模型相继发布，围绕开源和闭源模型成立了许多公司。仅举几个里程碑事件：

- OpenAI 和 Google 发布了 ChatGPT 和 Gemini 的实时多模态 API。OpenAI 甚至推出了 1-800-ChatGPT 电话号码！
- Kyutai 发布了 Moshi，一个完全开源的音频到音频 LLM。阿里巴巴发布了 Qwen2-Audio，Fixie.ai 发布了 Ultravox——两个原生理解音频的开源 LLM。
- ElevenLabs 在 C 轮融资中筹集了 1.8 亿美元。

尽管模型和融资方面呈现爆发式增长，但构建流式传输音频和视频的实时 AI 应用程序仍然困难，尤其是在 Python 中。

- ML 工程师可能缺乏构建实时应用程序所需的技术经验，例如 WebRTC。
- 即使是 Cursor 和 Copilot 这样的代码辅助工具，也难以编写支持实时音频/视频应用的 Python 代码。我深有体会！

因此，我们很高兴地宣布 FastRTC，这是 Python 的实时通信库。该库旨在让您完全用 Python 轻松构建实时音频和视频 AI 应用程序！

在这篇博客文章中，我们将通过构建实时音频应用程序来介绍 FastRTC 的基础知识。最后，您将了解 FastRTC 的核心功能：

- 🗣️ 内置自动语音检测和轮流发言，您只需关注响应用户的逻辑。
- 💻 自动 UI - 内置支持 WebRTC 的 Gradio UI，用于测试（或部署到生产环境！）。
- 📞 电话呼叫 - 使用 fastphone() 获取免费电话号码，呼叫您的音频流（需要 HF Token。PRO 账户有更高限额）。
- ⚡️ 支持 WebRTC 和 WebSocket。
- 💪 可定制 - 您可以将流挂载到任何 FastAPI 应用程序上，以便提供自定义 UI 或超越 Gradio 进行部署。
- 🧰 大量实用工具，包括文本转语音、语音转文本、停用词检测，助您快速上手。

让我们开始吧。

## 快速入门

我们将从构建实时音频的"hello world"开始：回显用户所说的话。在 FastRTC 中，这非常简单：

```python
from fastrtc import Stream, ReplyOnPause
import numpy as np

def echo(audio: tuple[int, np.ndarray]) -> tuple[int, np.ndarray]:
    yield audio

stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch()

```

让我们分解一下：

- ReplyOnPause 将为您处理语音检测和轮流发言。您只需关注响应用户的逻辑。任何返回音频元组（表示为 (sample_rate, audio_data)）的生成器都可以工作。
- Stream 类将为您构建一个 Gradio UI，以便快速测试您的流。完成原型设计后，您可以通过一行代码将 Stream 部署为生产就绪的 FastAPI 应用程序——stream.mount(app)。其中 app 是一个 FastAPI 应用程序。

实际效果如下：

## 进阶：LLM 语音聊天

下一步是使用 LLM 来响应用户。FastRTC 内置了语音转文本和文本转语音功能，因此与 LLM 配合使用非常容易。让我们相应地修改 echo 函数：

```python
import os

from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
from openai import OpenAI

sambanova_client = OpenAI(
    api_key=os.getenv("SAMBANOVA_API_KEY"), base_url="https://api.sambanova.ai/v1"
)
stt_model = get_stt_model()
tts_model = get_tts_model()

def echo(audio):
    prompt = stt_model.stt(audio)
    response = sambanova_client.chat.completions.create(
        model="Meta-Llama-3.2-3B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    prompt = response.choices[0].message.content
    for audio_chunk in tts_model.stream_tts_sync(prompt):
        yield audio_chunk

stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch()

```

我们使用 SambaNova API，因为它速度快。get_stt_model() 将从 Hub 获取 Moonshine Base，get_tts_model() 将获取 Kokoro，两者都针对设备端 CPU 推理进行了进一步优化。但您可以使用任何 LLM/文本转语音/语音转文本 API，甚至语音转语音模型。使用您喜欢的工具——FastRTC 只处理实时通信层。

## 额外功能：电话呼叫

如果您不调用 stream.ui.launch()，而是调用 stream.fastphone()，您将获得一个免费电话号码，用于呼叫您的流。注意，需要 Hugging Face Token。PRO 账户有更高限额。

您的终端将显示类似以下内容：

```
INFO:	  Your FastPhone is now live! Call +1 877-713-4471 and use code 530574 to connect to your stream.
INFO:	  You have 30:00 minutes remaining in your quota (Resetting on 2025-03-23)

```

然后您可以拨打该号码，它将连接到您的流！

## 下一步

- 阅读文档以了解更多关于 FastRTC 的基础知识。
- 开始构建的最佳方式是查看食谱。了解如何与流行的 LLM 提供商（包括 OpenAI 和 Gemini 的实时 API）集成，将您的流与 FastAPI 应用程序集成并进行自定义部署，从处理程序返回额外数据，进行视频处理等！
- ⭐️ 给仓库加星，并提交错误和功能请求！
- 在 HuggingFace 上关注 FastRTC Org 以获取更新，并查看已部署的示例！

感谢您关注 FastRTC！

---

> 本文由AI自动翻译，原文链接：[FastRTC: The Real-Time Communication Library for Python](https://huggingface.co/blog/fastrtc)
> 
> 翻译时间：2026-05-11 05:59
