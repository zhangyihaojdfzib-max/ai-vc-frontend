---
title: 谷歌发布Gemma 3：多模态多语言开源LLM
title_original: 'Welcome Gemma 3: Google''s all new multimodal, multilingual, long
  context open LLM'
date: '2025-03-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gemma3
author: ''
summary: 谷歌发布Gemma 3，这是其Gemma系列的新迭代，参数规模从1B到27B，支持128k上下文窗口、图像和文本输入以及140多种语言。模型在多项基准测试中表现优异，Gemma-3-27B-IT超越Gemini
  1.5-Pro。技术改进包括更长的上下文长度、多模态能力和多语言支持，通过调整位置嵌入、优化KV缓存管理和扩展预训练数据集实现。模型已上架Hugging Face
  Hub，并与生态系统紧密集成。
categories:
- AI产品
tags:
- Gemma 3
- 谷歌
- 多模态
- 开源LLM
- 多语言
draft: false
translated_at: '2026-05-09T05:21:03.833395'
---

# 欢迎 Gemma 3：谷歌全新多模态、多语言、长上下文开源 LLM

## 摘要

今天谷歌发布了 Gemma 3，这是其 Gemma 模型系列的新迭代版本。模型参数规模从 1B 到 27B 不等，上下文窗口最高可达 128k Token，可接受图像和文本输入，并支持 140 多种语言。

立即体验 Gemma 3 👉🏻 Gemma 3 Space

所有模型均已上架 Hub，并与 Hugging Face 生态系统紧密集成。

预训练模型和指令微调模型均已发布。Gemma-3-4B-IT 超越了 Gemma-2-27B IT，而 Gemma-3-27B-IT 在各项基准测试中均优于 Gemini 1.5-Pro。

![帕累托图](/images/posts/c660af9db7a6.png)

## 什么是 Gemma 3？

输入上下文窗口长度已从 Gemma 2 的 8k 提升至：1B 变体为 32k，其他所有变体为 128k。与其他 VLM（视觉语言模型）一样，Gemma 3 根据用户输入（可包含文本，也可选包含图像）生成文本。示例用途包括问答、分析图像内容、总结文档等。

虽然这些是多模态模型，但也可以将其作为纯文本模型（作为 LLM）使用，无需将视觉编码器加载到内存中。我们将在后面的推理部分详细讨论这一点。

## Gemma 3 的技术改进

Gemma 3 相较于 Gemma 2 的三项核心改进是：

- 更长的上下文长度
- 多模态能力
- 多语言能力

在本节中，我们将介绍实现这些改进的技术细节。从了解 Gemma 2 开始，探索如何让这些模型变得更好，这是一件有趣的事情。这一过程将帮助你像 Gemma 团队一样思考，并欣赏其中的细节！

### 更长的上下文长度

将上下文长度扩展到 128k Token 可以高效实现，无需从头训练模型。相反，模型使用 32k 序列进行预训练，仅在预训练结束时将 4B、12B 和 27B 模型扩展到 128k Token，从而节省了大量计算资源。位置嵌入（如 RoPE）进行了调整——从 Gemma 2 的 10k 基频升级到 Gemma 3 的 1M——并缩放 8 倍以支持更长的上下文。

KV 缓存管理通过使用 Gemma 2 的滑动窗口交错注意力进行了优化。超参数经过调整，将 5 个局部层与 1 个全局层交错（之前为 1:1），并将窗口大小减少到 1024 Token（从 4096 降低）。关键在于，在降低困惑度的同时实现了内存节省。

### 多模态能力

与 PaliGemma 类似，Gemma 3 中的注意力机制对文本和图像输入的处理方式不同。文本采用单向注意力，模型只关注序列中前面的词。而图像则获得完全注意力，没有掩码，允许模型以双向方式查看图像的每个部分，从而对视觉输入获得完整、不受限制的理解。

从下图可以看出，图像 Token `<img>` 采用双向注意力（整个方块被点亮），而文本 Token 采用因果注意力。该图还展示了注意力机制如何与滑动窗口算法配合工作。

![注意力可视化](/images/posts/b7fa086cbe89.png)

### 多语言能力

为了使 LLM 具备多语言能力，预训练数据集融入了更多语言。Gemma 3 的数据集包含两倍的多语言数据量，以改善语言覆盖范围。

为适应这些变化，分词器与 Gemini 2.0 相同。它是一个包含 262K 条目的 SentencePiece 分词器。新的分词器显著改善了对中文、日文和韩文文本的编码，代价是英文和代码的 Token 数量略有增加。

对于好奇的读者，这里是 Gemma 3 的技术报告，可深入了解这些改进。

LMSys Elo 评分是一个根据语言模型在人工评判的正面竞争中表现优劣进行排名的分数。在 LMSys Chatbot Arena 上，Gemma 3 27B IT 报告的 Elo 评分为 1339，跻身前 10 名最佳模型之列，包括领先的闭源模型。该 Elo 评分与 o1-preview 相当，且高于其他非推理型开源模型。该评分是 Gemma 3 在纯文本输入下取得的，与表中其他 LLM 相同。

![聊天机器人竞技场](/images/posts/957aec268540.png)

![IT 模型性能](/images/posts/a128b76bfccf.png)

## 使用 🤗 transformers 进行推理

```
$ pip install git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3

```

#### 使用 pipeline 进行推理

开始使用 Gemma 3 最简单的方法是使用 transformers 中的 pipeline 抽象。

模型在使用 bfloat16 数据类型时效果最佳。否则质量可能会下降。

```py
import torch
from transformers import pipeline

pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3-4b-it", 
    device="cuda",
    torch_dtype=torch.bfloat16
)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "糖果上是什么动物？"}
        ]
    }
]

output = pipe(text=messages, max_new_tokens=200)
print(output[0]["generated_text"][-1]["content"])

```

![手上的糖果](/images/posts/23d25615febb.jpg)

你可以将图像与文本交错排列。只需在要插入图像的位置截断输入文本，并使用如下图像块插入即可。

```py
messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "你是一个乐于助人的助手。"}]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "我已经在使用这种补充剂 "},
                {"type": "image", "url": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/IMG_3018.JPG"},
                {"type": "text", "text": "并且我也想使用这种 "},
                {"type": "image", "url": "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/IMG_3015.jpg"},
                {"type": "text", "text": " 有什么注意事项？"},
            ]
        },

    ]

```

#### 使用 Transformers 进行详细推理

Transformers 集成引入了两个新的模型类：

1. Gemma3ForConditionalGeneration：用于 4B、12B 和 27B 视觉语言模型。
2. Gemma3ForCausalLM：用于 1B 纯文本模型，以及将视觉语言模型作为语言模型加载（省略视觉塔）。

在下面的代码片段中，我们使用模型对图像进行查询。Gemma3ForConditionalGeneration 类用于实例化视觉语言模型变体。要使用该模型，我们将其与 AutoProcessor 类配对使用。运行推理就像创建 messages 字典、在其上应用聊天模板、处理输入并调用 model.generate 一样简单。

```py
import torch
from transformers import AutoProcessor, Gemma3ForConditionalGeneration

ckpt = "google/gemma-3-4b-it"
model = Gemma3ForConditionalGeneration.from_pretrained(
    ckpt, device_map="auto", torch_dtype=torch.bfloat16,
)
processor = AutoProcessor.from_pretrained(ckpt)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/spaces/big-vision/paligemma-hf/resolve/main/examples/password.jpg"},
            {"type": "text", "text": "密码是什么？"}
        ]
    }
]
inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device)

input_len = inputs["input_ids"].shape[-1]

generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
generation = generation[0][input_len:]

decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)

```

对于仅使用LLM的模型推理，我们可以使用`Gemma3ForCausalLM`类。`Gemma3ForCausalLM`应与`AutoTokenizer`配合使用进行文本处理。我们需要使用聊天模板来预处理输入。Gemma 3使用非常简短的系统提示词，后跟用户提示词，如下所示。

```py
import torch
from transformers import AutoTokenizer, Gemma3ForCausalLM

ckpt = "google/gemma-3-4b-it"
model = Gemma3ForCausalLM.from_pretrained(
    ckpt, torch_dtype=torch.bfloat16, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(ckpt)

messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant who is fluent in Shakespeare English"},]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "Who are you?"},]
        },
    ],
]
inputs = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device)

input_len = inputs["input_ids"].shape[-1]

generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
generation = generation[0][input_len:]

decoded = tokenizer.decode(generation, skip_special_tokens=True)
print(decoded)

```

## 在设备端及低资源设备上

首先，通过以下命令安装`mlx-vlm`：

```
pip install git+https://github.com/Blaizzy/mlx-vlm.git

```

安装`mlx-vlm`后，可以通过以下命令开始推理：

```
python -m mlx_vlm.generate --model mlx-community/gemma-3-4b-it-4bit --max-tokens 100 --temp 0.0 --prompt "What is the code on this vehicle??"
 --image https://farm8.staticflickr.com/7212/6896667434_2605d9e181_z.jpg

```

![airplane](/images/posts/c150ceabcd17.jpg)

### Llama.cpp

预量化的GGUF文件可以从该集合中下载

请参考此指南来构建或下载预构建的二进制文件：https://github.com/ggml-org/llama.cpp?tab=readme-ov-file#building-the-project

然后您可以从终端运行本地聊天服务器：

```
./build/bin/llama-cli -m ./gemma-3-4b-it-Q4_K_M.gguf

```

输出应如下所示：

```
> who are you  
I'm Gemma, a large language model created by the Gemma team at Google DeepMind. I’m an open-weights model, which means I’m widely available for public use!

```

### 在Hugging Face端点上部署

您可以从我们的推理目录中一键部署`gemma-3-27b-it`和`gemma-3-12b-it`。该目录配置了合适的硬件、优化的TGI配置以及用于尝试模型的合理默认设置。
也支持部署任何GGUF/llama.cpp变体（例如上述集合中提到的那些），您可以在此处找到创建端点的指南。

## 致谢

培养一个gemma需要整个社区的努力！我们要感谢（排名不分先后）Raushan、Joao、Lysandre、Kashif、Matthew、Marc、David、Mohit、Yih Dah，感谢他们为将Gemma集成到我们开源栈的各个部分（从Transformers到TGI）所做的努力。感谢我们的设备端、gradio和推广团队——Chris、Kyle、Pedro、Son、Merve、Aritra、VB、Toshiro，感谢他们帮助构建了展示Gemma的精彩演示。

最后，衷心感谢Georgi、Diego和Prince在llama.cpp和MLX移植方面提供的帮助。

---

> 本文由AI自动翻译，原文链接：[Welcome Gemma 3: Google's all new multimodal, multilingual, long context open LLM](https://huggingface.co/blog/gemma3)
> 
> 翻译时间：2026-05-09 05:21
