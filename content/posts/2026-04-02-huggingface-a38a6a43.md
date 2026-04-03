---
title: Gemma 4发布：开源多模态模型，支持设备端部署
title_original: 'Welcome Gemma 4: Frontier multimodal intelligence on device'
date: '2026-04-02'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gemma4
author: ''
summary: Google DeepMind在Hugging Face上发布了Gemma 4系列多模态模型。该系列模型采用Apache 2许可证开源，支持图像、文本和音频输入，并生成文本响应。模型在帕累托前沿竞技场评分中表现出色，提供多种尺寸，可在包括设备端在内的各种环境中部署。文章详细介绍了Gemma
  4的新特性、架构改进（如逐层嵌入和共享KV缓存）、多模态能力，并展示了如何通过transformers、llama.cpp等主流工具进行部署和微调。
categories:
- AI产品
tags:
- Gemma 4
- 多模态模型
- 开源AI
- 设备端AI
- Hugging Face
draft: false
translated_at: '2026-04-03T05:01:08.405085'
---

# 欢迎 Gemma 4：设备端的尖端多模态智能

Google DeepMind 的 Gemma 4 系列多模态模型现已在 Hugging Face 发布，支持您喜爱的 Agent（智能体）、推理引擎和微调库 🤗

这些模型是真正的实力派：采用 Apache 2 许可证，真正开源；在帕累托前沿竞技场评分中表现出色，质量上乘；支持包括音频在内的多模态功能；并且提供多种尺寸，可在包括设备端在内的任何地方使用。Gemma 4 建立在先前系列模型进步的基础上，并将这些优势完美融合。在我们使用预发布检查点进行的测试中，其能力给我们留下了深刻印象，以至于我们很难找到好的微调示例，因为它们开箱即用的表现就**非常出色**。

我们与 Google 和社区合作，确保它们能在任何地方使用：transformers、llama.cpp、MLX、WebGPU、Rust；应有尽有。这篇博文将向您展示如何使用**您最喜爱的工具**进行构建，请告诉我们您的想法！

-   Gemma 4 有哪些新特性？
-   能力与架构概述架构概览逐层嵌入共享 KV 缓存
-   多模态能力
-   随处部署transformersLlama.cpp接入您的本地 Agenttransformers.jsMLXMistral.rs
-   微调与演示使用 TRL 进行微调在 Vertex AI 上使用 TRL 进行微调使用 Unsloth Studio 进行微调
-   尝试 Gemma 4
-   基准测试结果
-   致谢

    -   架构概览
    -   逐层嵌入
    -   共享 KV 缓存

    -   transformers
    -   Llama.cpp
    -   接入您的本地 Agent
    -   transformers.js
    -   MLX
    -   Mistral.rs

    -   使用 TRL 进行微调在 Vertex AI 上使用 TRL 进行微调
    -   使用 Unsloth Studio 进行微调

        -   在 Vertex AI 上使用 TRL 进行微调

# Gemma 4 有哪些新特性？

与 Gemma-3n 类似，Gemma 4 支持图像、文本和音频输入，并生成文本响应。其文本解码器基于 Gemma 模型，支持长上下文窗口。图像编码器与 Gemma 3 的类似，但有两项关键改进：可变宽高比，以及可配置的图像 Token 输入数量，以便您在速度、内存和质量之间找到最佳平衡点。所有模型都支持图像（或视频）和文本输入，而小型变体（E2B 和 E4B）还支持音频。

## 能力与架构概述

如上方的基准测试所示，这种功能组合（结合训练数据和配方）使得 310 亿参数的稠密模型能够达到估计的 LMArena 评分（仅文本）1452 分，而 260 亿参数的 MoE 模型仅用 40 亿激活参数就达到了 1441 分 🤯。正如我们将看到的，至少在非正式和主观测试中，多模态操作的表现与文本生成相当。

以下是 Gemma 4 的主要架构特性：

-   交替的**局部滑动窗口**和**全局全上下文**注意力层。较小的稠密模型使用 512 个 Token 的滑动窗口，而较大的模型使用 1024 个 Token。
-   双重 RoPE 配置：滑动层使用标准 RoPE，全局层使用比例 RoPE，以实现更长的上下文。
-   **逐层嵌入**：第二个嵌入表，为每个解码器层馈送一个小的残差信号。
-   **共享 KV 缓存**：模型的最后 N 层复用较早层的键值状态，消除了冗余的 KV 投影。
-   视觉编码器：使用学习到的 2D 位置和多维 RoPE。保留原始宽高比，并可以将图像编码为几种不同的 Token 预算（70、140、280、560、1120）。
-   音频编码器：采用 USM 风格的 Conformer，其基础架构与 Gemma-3n 中的相同。

#### 逐层嵌入

较小的 Gemma 4 模型最显著的特征之一是逐层嵌入，该特性先前已在 Gemma-3n 中引入。在标准的 Transformer 中，每个 Token 在输入时获得一个单一的嵌入向量，并且相同的初始表示是残差流在所有层上构建的基础，这迫使嵌入必须预先加载模型可能需要的所有信息。PLE 在主残差流旁边增加了一个并行的、低维度的条件调节通路。对于每个 Token，它通过结合两个信号为每一层生成一个小的专用向量：一个是 Token 身份组件（来自嵌入查找），另一个是上下文感知组件（来自主嵌入的学习投影）。然后，每个解码器层在注意力和前馈网络之后，使用其对应的向量通过一个轻量级的残差块来调制隐藏状态。这为每一层提供了自己的通道，仅在相关信息变得相关时接收特定于 Token 的信息，而不是要求将所有信息都打包到一个单一的前期嵌入中。由于 PLE 的维度远小于主隐藏层大小，因此它以适中的参数成本增加了有意义的逐层专业化。对于多模态输入（图像、音频、视频），PLE 是在软 Token 合并到嵌入序列之前计算的——因为 PLE 依赖于 Token ID，而一旦多模态特征替换了占位符，这些 ID 就会丢失。多模态位置使用填充 Token ID，有效地接收中性的逐层信号。

#### 共享 KV 缓存

**共享 KV 缓存**是一项效率优化，可减少推理过程中的计算和内存消耗。模型的最后 `num_kv_shared_layers` 层不计算自己的键和值投影。相反，它们**复用**来自同一注意力类型（滑动或全局）的最后一个非共享层的 K 和 V 张量。

实际上，这对质量的影响微乎其微，同时对于生成长上下文和设备端使用来说，在内存和计算方面都更加高效。

## 多模态能力

我们在测试中发现，Gemma 4 开箱即用地支持全面的多模态能力。我们不清楚其训练数据的具体构成，但我们已成功将其用于 OCR、语音转文本、目标检测或指向等任务。它还支持纯文本和多模态的函数调用、推理、代码补全和修正。

在此，我们展示几个不同模型尺寸的推理示例。您可以使用[此笔记本](https://github.com/huggingface/notebooks/blob/main/notebooks/gemma-4-multimodal-inference.ipynb)方便地运行它们。我们鼓励您尝试这些演示，并在这篇博文下方分享您的体验！

### 目标检测与指向

### GUI 检测

我们在不同尺寸的模型上测试 Gemma 4 的 GUI 元素检测和指向能力，使用以下图像和文本提示词："图像中 'view recipe' 元素的边界框是什么？"

![Image](/images/posts/6408aa7bf6ad.png)

使用此提示词，模型会以 JSON 格式原生响应检测到的边界框——无需特定指令或语法约束生成。我们发现坐标指的是相对于输入尺寸的 1000x1000 图像大小。

为了方便您查看，我们在下方将输出可视化。我们从返回的 JSON 中解析边界框：`json\n[\n  {"box_2d": [171, 75, 245, 308], "label": "view recipe element"}\n]\n`

![E2B](/images/posts/9db012f3b723.png)

![E4B](/images/posts/99a2a00b81e0.png)

![31B](/images/posts/93603606e77a.png)

![31B](/images/posts/5e34aef0d1df.png)

### 目标检测

我们测试模型检测日常物体的能力，这里我们要求它们检测自行车并比较不同模型的输出。与之前的情况一样，我们从 json 中解析边界框并转换为图像空间坐标。

![E2B](/images/posts/1f7e54b73e1e.png)

![E4B](/images/posts/f1b0bf465a82.png)

![26B](/images/posts/b06fbd8e2233.png)

![31B](/images/posts/d8d0de00e8ca.png)

### 多模态思维与函数调用

我们要求 Gemma 4 编写 HTML 代码来重建我们使用 Gemini 3 制作的页面。您可以在下方找到执行此操作的代码，我们启用了思维链，并要求每个模型生成最多 4000 个新 Token，以确保万无一失。

![Reference](/images/posts/ce442ec93a16.png)

![Reference](/images/posts/146631d58144.png)

```py
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/landing_page.png",
            },
            {"type": "text", "text": "为此页面编写 HTML 代码。"},
        ],
    }
]
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
    enable_thinking=True,
).to(model.device)
output = model.generate(**inputs, max_new_tokens=4000)
input_len = inputs.input_ids.shape[-1]
generated_text_ids = output[0][input_len:]
generated_text = processor.decode(generated_text_ids, skip_special_tokens=True)
result = processor.parse_response(generated_text)
print(result["content"])

```

![参考](/images/posts/e87f2967d854.png)

![E4B](/images/posts/34f7e3ce8289.png)

![31B](/images/posts/8eb486757fee.png)

![MoE](/images/posts/d54b9a5280cb.png)

### 视频理解

较小的 Gemma 4 模型可以接收带音频的视频，而较大的模型可以接收不带音频的视频。虽然这些模型没有在视频数据上进行明确的后期训练，但它们能够理解带音频和不带音频的视频。该模型在音频方面表现尤为出色。

```py
messages = [
    {
        "role": "user",
        "content": [
            {"type": "video", "url": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/concert.mp4"},
            {"type": "text", "text": "视频中发生了什么？这首歌是关于什么的？"},
        ],
    },
]
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
    load_audio_from_video=True,
).to(model.device)
output = model.generate(**inputs, max_new_tokens=200)
input_len = inputs.input_ids.shape[-1]
generated_text_ids = output[0][input_len:]
generated_text = processor.decode(generated_text_ids, skip_special_tokens=True)
print(result["content"])

```

### 图像描述

我们已在图像描述任务上测试了所有模型。所有检查点都表现非常出色，能够准确捕捉复杂场景中的细微差别。
这是我们使用的图像，提示词为"为此图像写一个详细的描述。"。

![图像](/images/posts/f4e1ef9b17a5.png)

```py
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/bird.png"},
            {"type": "text", "text": "为此图像写一个详细的描述。"},
        ],
    },
]
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
).to(model.device)
output = model.generate(**inputs, max_new_tokens=512)
input_len = inputs.input_ids.shape[-1]
generated_text_ids = output[0][input_len:]
generated_text = processor.decode(generated_text_ids, skip_special_tokens=True)
result = processor.parse_response(generated_text)
print(result["content"])

```

### 音频问答

这些模型经过训练，能够回答关于音频中语音的问题。音乐和非语音声音不属于训练数据的一部分。

```py
messages = [
    {
        "role": "user",
        "content": [
            {"type": "audio", "url": "https://huggingface.co/datasets/hf-internal-testing/dummy-audio-samples/resolve/main/obama_first_45_secs.mp3"},
            {"type": "text", "text": "你能详细描述这段音频吗？"},
        ],
    },
]

inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
).to(model.device)

output = model.generate(
    **inputs,
    max_new_tokens=1000,
    do_sample=False,
)

print(processor.decode(output[0], skip_special_tokens=True))

```

如果你想进行转录，这里有一个示例：

```py
messages = [
    {
        "role": "user",
        "content": [
            {"type": "audio", "url": "https://huggingface.co/datasets/hf-internal-testing/dummy-audio-samples/resolve/main/obama_first_45_secs.mp3"},
            {"type": "text", "text": "转录这段音频？"},
        ],
    },
]

inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
).to(model.device)

output = model.generate(
    **inputs,
    max_new_tokens=1000,
    do_sample=False,
)

print(processor.decode(output[0], skip_special_tokens=True))

```

### 多模态函数调用

我们通过要求获取图像所示地点的天气来测试模型。

```py
import re
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取特定地点的当前天气。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
            },
            "required": ["city"],
        },
    },
}
tools = [WEATHER_TOOL]
messages = [
    {"role": "user", "content": [
        {"type": "image", "image": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/thailand.jpg"},
        {"type": "text", "text": "这张图片中的城市是哪里？查一下那里现在的天气。"},
    ]},
]
inputs = processor.apply_chat_template(
    messages,
    tools=[WEATHER_TOOL],
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
    enable_thinking=True,
).to(model.device)
output = model.generate(**inputs, max_new_tokens=1000)
input_len = inputs.input_ids.shape[-1]
generated_text_ids = output[0][input_len:]
generated_text = processor.decode(generated_text_ids, skip_special_tokens=True)
result = processor.parse_response(generated_text)
print(result["content"])

```

# 随处部署

## transformers

```bash
pip install -U transformers

```

使用小型 Gemma 4 模型进行推理的最简单方法是通过 `any-to-any` 流水线。您可以按如下方式初始化它。

```py
from transformers import pipeline
pipe = pipeline("any-to-any", model="google/gemma-4-e2b-it")

```

然后，您可以按如下方式传入图像和文本。

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/thailand.jpg",
            },
            {"type": "text", "text": "去这里旅行有什么建议吗？"},
        ],
    }
]
output = pipe(messages, max_new_tokens=100, return_full_text=False)
output[0]["generated_text"]


```

在使用视频进行推理时，您可以使用 `load_audio_from_video` 参数来包含音轨。

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "video",
                "image": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/rockets.mp4",
            },
            {"type": "text", "text": "这个视频中发生了什么？"},
        ],
    }
]
pipe(messages, load_audio_from_video=True)

```

更深入一层，您可以使用 `AutoModelForMultimodalLM` 类加载 Gemma 4，这对于微调尤其有用。内置的聊天模板负责正确格式化输入，请确保使用它，以防止手动构建提示词时出现细微错误。

```python
from transformers import AutoModelForMultimodalLM, AutoProcessor
model = AutoModelForMultimodalLM.from_pretrained("google/gemma-4-E2B-it", device_map="auto")
processor = AutoProcessor.from_pretrained("google/gemma-4-E2B-it")
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "video",
                "image": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/rockets.mp4",
            },
            {"type": "text", "text": "What is happening in this video?"},
        ],
    }
]
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)

generated_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)

```

## Llama.cpp

你可以通过以下方式安装 llama-cpp。

```bash
brew install llama.cpp 
winget install llama.cpp 

```

然后，你可以启动一个兼容 OpenAI API 的服务器。将命令末尾的量化方案替换为你选择的精度。

```bash
llama-server -hf ggml-org/gemma-4-E2B-it-GGUF

```

查看此链接，了解将 llama.cpp 与不同编码 Agent（智能体）和本地应用结合使用的更多选项。在此集合中查找所有 GGUF 检查点。

## 接入你的本地 Agent（智能体）

我们致力于确保新模型能在本地与 openclaw、hermes、pi 和 open code 等 Agent（智能体）协同工作。这一切都归功于 llama.cpp！运行以下命令即可立即尝试 Gemma 4。

首先，启动你的本地服务器：

```
llama-server -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M

```

对于 hermes：

```shell
hermes model

```

对于 openclaw：

```shell
openclaw onboard

```

对于 pi，定义一个 `~/.pi/agent/models.json` 文件：

```json
{
  "providers": {
    "llama-cpp": {
      "baseUrl": "http://localhost:8080/v1",	
      "api": "openai-completions",
      "apiKey": "none",
      "models": [
        {
          "id": "ggml-org-gemma-4-26b-4b-gguf"
        }
      ]
    }
  }
}

```

对于 open code，定义一个 `~/.config/opencode/opencode.json` 文件：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llama.cpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama-server (local)",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1"
      },
      "models": {
        "gemma-4-26b-4b-it": {
          "name": "Gemma 4 (local)",
          "limit": {
            "context": 128000,
            "output": 8192
          }
        }
      }
    }
  }
}

```

## transformers.js

transformers.js 使得 Gemma 4 可以直接在浏览器中运行。你可以查看模型卡片，详细了解纯文本、图像与文本、音频与文本的推理。我们也为你提供了一个演示。

使用开源 mlx-vlm 库可以获得 Gemma 4 的完整多模态支持。以下是如何让模型描述一张图片：

```shell
pip install -U mlx-vlm

```

```shell
mlx_vlm.generate \
--model google/gemma-4-E4B-it \
--image https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg \
--prompt "Describe this image in detail"

```

mlx-vlm 支持 TurboQuant，它在使用约 4 倍更少活动内存且端到端运行速度快得多的同时，能提供与未压缩基线相同的精度。这使得在不牺牲质量的情况下，在 Apple Silicon 上进行长上下文推理变得可行。使用方法如下：

```shell
mlx_vlm.generate \
--model "mlx-community/gemma-4-26B-A4B-it" \
--prompt "Your prompt here" \
--kv-bits 3.5 \
--kv-quant-scheme turboquant

```

关于音频示例和更多细节，请查看 MLX 集合。

### Mistral.rs

mistral.rs 是一个 Rust 原生的推理引擎，支持所有模态（文本、图像、视频、音频）的 Gemma 4 零日支持，并内置工具调用和 Agent（智能体）功能。安装 mistral.rs：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/EricLBuehler/mistral.rs/master/install.sh | sh 

irm https://raw.githubusercontent.com/EricLBuehler/mistral.rs/master/install.ps1 | iex 

```

然后，你可以启动一个兼容 OpenAI 的 HTTP 服务器：

```bash
mistralrs serve mistralrs-community/gemma-4-E4B-it-UQFF --from-uqff 8

```

或者，使用交互模式：

```
mistralrs run -m google/gemma-4-E4B-it --isq 8 --image image.png -i "Describe this image in detail."

mistralrs run -m google/gemma-4-E4B-it --isq 8 --audio audio.mp3 -i "Transcribe this fully."

```

在此集合中查找所有模型。在模型卡片中查找安装和推理的说明。

## 面向所有人的微调

## 使用 TRL 进行微调

为了展示这一点，我们构建了一个训练脚本示例，其中 Gemma 4 学习在 CARLA 模拟器中驾驶。模型通过摄像头观察道路，决定做什么，并从结果中学习。训练后，它能持续变道以避开行人。同样的方法适用于任何需要模型观察和行动的任务：机器人技术、网页浏览或其他交互式环境。

开始使用：

```shell
# pip install git+https://github.com/huggingface/trl.git

python examples/scripts/openenv/carla_vlm_gemma.py \
    --env-urls https://sergiopaniego-carla-env.hf.space \
            https://sergiopaniego-carla-env-2.hf.space \
    --model google/gemma-4-E2B-it

```

在此处查找示例。

### 在 Vertex AI 上使用 TRL 进行微调

此外，我们准备了一个关于如何在 Vertex AI 上使用 TRL 和 SFT 微调 Gemma 4 的示例，以展示如何扩展函数调用能力，同时冻结视觉和音频塔。示例包括如何在 Google Cloud 上构建一个支持 CUDA 的、包含最新 Transformers、TRL 等的自定义 Docker 容器，以及如何通过 Vertex AI 无服务器训练作业运行它。

```python

from google.cloud import aiplatform

aiplatform.init(
    project="<PROJECT_ID>",
    location="<LOCATION>",
    staging_bucket="<BUCKET_URI>",
)

job = aiplatform.CustomContainerTrainingJob(
    display_name="gemma-4-fine-tuning",
    container_uri="<CONTAINER_URI>",
    command=["python", "/gcs/gemma-4-fine-tuning/train.py"],
)

job = job.submit(
    replica_count=1,
    machine_type="a3-highgpu-1g",
    accelerator_type="NVIDIA_H100_80GB",
    accelerator_count=1,
    base_output_dir="<BUCKET_URI>/output-dir",
    environment_variables={
        "MODEL_ID": "google/gemma-4-E2B-it",
        "HF_TOKEN": <HF_TOKEN>,
    },
    boot_disk_size_gb=500,
)

```

你可以在 "Hugging Face on Google Cloud" 文档中找到完整示例，地址是 https://hf.co/docs/google-cloud/examples/vertex-ai-notebooks-fine-tune-gemma-4。

## 使用 Unsloth Studio 进行微调

如果你想在 UI 中微调和运行 Gemma 4 模型，可以试试 Unsloth Studio。它可以在本地或 Google Colab 上运行。首先，安装并启动应用：

```shell
# 在 MacOS, Linux, WSL 上安装 unsloth studio
curl -fsSL https://unsloth.ai/install.sh | sh

# 在 Windows 上安装 unsloth studio
irm https://unsloth.ai/install.ps1 | iex

# 启动 unsloth studio
unsloth studio -H 0.0.0.0 -p 8888
# 搜索 Gemma 4 模型，例如 google/gemma-4-E2B-it

```

然后从 Hub 中选择任意 Gemma 4 模型。

![Unsloth Studio](/images/posts/af8900fc3007.png)

## 尝试 Gemma 4

我们为你提供了演示，以尝试不同的 Gemma 4 模型。我们包含了基于 transformers 实现的 E4B、26B/A4B 和 dense31B 模型的演示，以及一个使用 transformers.js 的 WebGPU 演示 🚀

## 基准测试结果

![Gemma 4 Performance vs Size](/images/posts/3f83d835677c.png)

![Gemma 4 Arena Elo Score Comparison](/images/posts/cd824bf98f07.png)

来源：Google (blog.google)

以下是经过指令微调模型的详细基准测试结果：

## 致谢

将Gemma-4引入开源生态系统，离不开许多人的共同努力，远不止本文作者。在此，我们不分先后地感谢开源团队的众多成员：Gemma 4的transformers集成要归功于Cyril、Raushan、Eustache、Arthur和Lysandre。我们感谢Joshua负责transformers.js集成与演示，Eric负责mistral.rs集成，Son负责Llama.cpp，Prince负责MLX集成，Quentin、Albert和Kashif负责TRL，Adarsh负责SGLang transformers后端，以及Toshihiro负责构建多个演示。

这项工作离不开谷歌在模型构建上的巨大贡献，也离不开他们为将模型贡献给transformers以实现标准化所付出的重要努力。如今，开源生态系统因这款能力强大、许可自由的开源模型而变得更加完善。

Gemma 4的transformers集成由Cyril、Raushan、Eustache、Arthur和Lysandre负责。我们感谢Joshua负责transformers.js集成与演示，Eric负责mistral.rs集成，Son负责Llama.cpp，Prince负责MLX集成，Quentin负责TRL，Adarsh负责SGLang transformers后端，以及Toshihiro负责构建多个演示。

这项工作离不开谷歌在模型构建上的巨大贡献，也离不开他们为将模型贡献给transformers以实现标准化所付出的重要努力。如今，开源生态系统因这款能力强大、许可自由的开源模型而变得更加完善。

---

> 本文由AI自动翻译，原文链接：[Welcome Gemma 4: Frontier multimodal intelligence on device](https://huggingface.co/blog/gemma4)
> 
> 翻译时间：2026-04-03 05:01
