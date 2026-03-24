---
title: Gemma 3n 全面登陆开源生态，高效多模态模型触手可及
title_original: Gemma 3n fully available in the open-source ecosystem!
date: '2025-06-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gemma3n
author: ''
summary: 谷歌最新多模态模型 Gemma 3n 正式在 transformers、timm、MLX 等主流开源库中全面可用。文章介绍了其发布的两种高效参数模型（E2B
  和 E4B），它们通过内存优化技术，仅需相当于 2B/4B 模型的 GPU 内存即可运行 5B/8B 参数的模型。模型集成了创新的 MobileNet-V5 视觉编码器和基于通用语音模型的音频编码器，采用
  MatFormer 嵌套架构，支持多语言与多模态交互，并在多项基准测试中表现出色。文章还提供了通过 Hugging Face Space 体验模型及使用 transformers
  库进行推理的快速入门指南。
categories:
- AI产品
tags:
- Gemma 3n
- 多模态AI
- 开源模型
- Transformer
- 模型推理
draft: false
translated_at: '2026-03-24T04:49:06.016303'
---

今天，Gemma 3n 终于在最常用的开源库中可用。这包括 transformers & timm、MLX、llama.cpp（文本输入）、transformers.js、ollama、Google AI Edge 等。

这篇文章将快速浏览一些实用的代码片段，展示如何在这些库中使用该模型，以及为其他领域进行微调是多么容易。

## 今日发布的模型

这里是 `Gemma 3n Release Collection`

今天发布了两种模型尺寸，每种都有两个变体（基础版和指导版）。模型名称遵循非标准命名法：它们被称为 `gemma-3n-E2B` 和 `gemma-3n-E4B`。参数数量前的 `E` 代表 **有效**。它们的实际参数数量分别是 **5B** 和 **8B**，但由于内存效率的改进，它们只需要 2B 和 4B 的 VRAM（GPU 内存）。

因此，这些模型在硬件支持方面表现得像 2B 和 4B 的模型，但在质量上却超越了 2B/4B 的模型。`E2B` 模型只需 2GB 的 GPU RAM 即可运行，而 `E4B` 只需 3GB 的 GPU RAM 即可运行。

## 模型详情

除了语言解码器，Gemma 3n 还使用了 **音频编码器** 和 **视觉编码器**。我们在下面重点介绍它们的主要特性，并描述它们是如何被添加到 `transformers` 和 `timm` 中的，因为它们是其他实现的参考。

*   **视觉编码器（MobileNet-V5）**。Gemma 3n 使用了新版本的 MobileNet：MobileNet-v5-300，该版本已添加到今天发布的新版 `timm` 中。
    *   具有 **3 亿参数**。
    *   支持 `256x256`、`512x512` 和 `768x768` 的分辨率。
    *   在 Google Pixel 上达到 60 FPS，性能优于 ViT Giant，同时使用的参数减少了 3 倍。
*   **音频编码器**：
    *   基于通用语音模型。
    *   以 **160 毫秒** 的块处理音频。
    *   支持语音转文本和翻译功能（例如，英语到西班牙语/法语）。

### 架构亮点

*   **MatFormer 架构**：
    *   一种嵌套的 Transformer 设计，类似于 Matryoshka 嵌入，允许提取不同的层子集，就像它们是独立的模型一样。
    *   E2B 和 E4B 是一起训练的，将 E2B 配置为 E4B 的子模型。
    *   用户可以根据其硬件特性和内存预算“混合搭配”层。
*   **逐层嵌入**：
    *   通过将嵌入卸载到 CPU 来减少加速器内存使用。这就是为什么 E2B 模型虽然拥有 5B 的实际参数，但占用的 GPU 内存大约相当于一个 2B 参数模型的原因。
*   **KV 缓存共享**：
    *   加速了音频和视频的长上下文处理，与 Gemma 3 4B 相比，预填充速度提高了 2 倍。

### 性能与基准测试：

*   **LMArena 分数**：E4B 是首个分数达到 1300+ 的 10B 以下模型。
*   **MMLU 分数**：Gemma 3n 在各种尺寸（E4B、E2B 和几种混合搭配配置）上都表现出有竞争力的性能。
*   **多语言支持**：支持 140 种语言的文本和 35 种语言的多模态交互。

## 演示空间

![Gemma 3n 的 Hugging Face Space GIF](/images/posts/d629fabe2bb8.gif)

感受模型最简便的方法是使用其专用的 Hugging Face Space。你可以在这里尝试不同模态的不同提示词。

📱 Space

## 使用 transformers 进行推理

安装最新版本的 timm（用于视觉编码器）和 transformers 来运行推理，或者如果你想进行微调。

```shell
pip install -U -q timm
pip install -U -q transformers

```

### 使用 pipeline 进行推理

开始使用 Gemma 3n 最简单的方法是使用 transformers 中的 pipeline 抽象：

```py
import torch
from transformers import pipeline

pipe = pipeline(
   "image-text-to-text",
   model="google/gemma-3n-E4B-it", 
   device="cuda",
   torch_dtype=torch.bfloat16
)

messages = [
   {
       "role": "user",
       "content": [
           {"type": "image", "url": "https://huggingface.co/datasets/ariG23498/demo-data/resolve/main/airplane.jpg"},
           {"type": "text", "text": "Describe this image"}
       ]
   }
]

output = pipe(text=messages, max_new_tokens=32)
print(output[0]["generated_text"][-1]["content"])

```

输出：

```
The image shows a futuristic, sleek aircraft soaring through the sky. It's designed with a distinctive, almost alien aesthetic, featuring a wide body and large

```

### 使用 transformers 进行详细推理

从 Hub 初始化模型和处理器，并编写 `model_generation` 函数，该函数负责处理提示词并在模型上运行推理。

```py
from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

model_id = "google/gemma-3n-e4b-it" 
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(model_id).to(device)

def model_generation(model, messages):
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    input_len = inputs["input_ids"].shape[-1]

    inputs = inputs.to(model.device, dtype=model.dtype)

    with torch.inference_mode():
        generation = model.generate(**inputs, max_new_tokens=32, disable_compile=False)
        generation = generation[:, input_len:]

    decoded = processor.batch_decode(generation, skip_special_tokens=True)
    print(decoded[0])

```

由于模型支持所有模态作为输入，这里简要说明如何通过 transformers 使用它们。

#### 仅文本

```py


messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What is the capital of France?"}
        ]
    }
]
model_generation(model, messages)

```

```
The capital of France is **Paris**. 

```

#### 与音频交错

```py


messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Transcribe the following speech segment in English:"},
            {"type": "audio", "audio": "https://huggingface.co/datasets/ariG23498/demo-data/resolve/main/speech.wav"},
        ]
    }
]
model_generation(model, messages)

```

```
Send a text to Mike. I'll be home late tomorrow.

```

#### 与图像/视频交错

对视频的支持是通过一系列图像帧来实现的。

```py


messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "https://huggingface.co/datasets/ariG23498/demo-data/resolve/main/airplane.jpg"},
            {"type": "text", "text": "Describe this image."}
        ]
    }
]
model_generation(model, messages)

```

```
The image shows a futuristic, sleek, white airplane against a backdrop of a clear blue sky transitioning into a cloudy, hazy landscape below. The airplane is tilted at

```

## 使用 MLX 进行推理

```
pip install -u mlx-vlm

```

从视觉开始：

```py
python -m mlx_vlm.generate --model google/gemma-3n-E4B-it --max-tokens 100 --temperature 0.5 --prompt "Describe this image in detail." --image https://huggingface.co/datasets/ariG23498/demo-data/resolve/main/airplane.jpg

```

以及音频：

```py
python -m mlx_vlm.generate --model google/gemma-3n-E4B-it --max-tokens 100 --temperature 0.0 --prompt "Transcribe the following speech segment in English:" --audio https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/audio-samples/jfk.wav

```

### 使用 llama.cpp 进行推理

除了 MLX，Gemma 3n（仅文本版本）也能在 llama.cpp 上开箱即用。请确保从源码安装 llama.cpp/ Ollama。

在此查看 llama.cpp 的安装说明：https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md

您可以按如下方式运行：

```shell
llama-server -hf ggml-org/gemma-3n-E4B-it-GGUF:Q8_0

```

### 使用 Transformers.js 和 ONNXRuntime 进行推理

最后，我们还发布了 `gemma-3n-E2B-it` 模型变体的 ONNX 权重，以便在各种运行时和平台上实现灵活的部署。对于 JavaScript 开发者，Gemma 3n 已集成到 `Transformers.js` 中，并从版本 `3.6.0` 开始可用。

有关如何使用这些库运行模型的更多信息，请查看模型卡中的使用部分。

## 在免费的 Google Colab 中进行微调

鉴于该模型的规模，针对特定跨模态下游任务对其进行微调非常方便。为了便于您微调模型，我们创建了一个简单的笔记本，让您可以在免费的 `Google Colab` 上进行实验！

我们还提供了一个专门的 `notebook` 用于音频任务微调，以便您可以轻松地将模型适配到您的语音数据集和基准测试中！

## Hugging Face Gemma 配方

随着本次发布，我们还推出了 `Hugging Face Gemma Recipes` 代码库。您可以在其中找到运行和微调模型的 `notebooks` 和 `scripts`。

我们非常希望您能使用 Gemma 系列模型，并为其添加更多配方！欢迎随时在代码库中提交 Issue 和创建 Pull Request。

## 结语

我们一直很高兴能够托管 Google 及其 Gemma 系列模型。我们希望社区能够团结起来，充分利用这些模型。多模态、小尺寸且能力强大，这是一次非常棒的模型发布！

如果您想更详细地讨论这些模型，请直接在本博客文章下方开始讨论。我们将非常乐意为您提供帮助！

衷心感谢 Arthur、Cyril、Raushan、Lysandre 以及 Hugging Face 的每一位成员，他们负责了集成工作并将其提供给社区！

---

> 本文由AI自动翻译，原文链接：[Gemma 3n fully available in the open-source ecosystem!](https://huggingface.co/blog/gemma3n)
> 
> 翻译时间：2026-03-24 04:49
