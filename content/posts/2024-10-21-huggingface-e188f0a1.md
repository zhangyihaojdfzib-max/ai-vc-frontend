---
title: Keras现已支持Llama 3.2模型
title_original: “Llama 3.2 in Keras”
date: '2024-10-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/keras-llama-32
author: ''
summary: 文章宣布Llama 3.2模型在发布当天即可在Keras中使用，无需等待。通过keras-hub库，用户可以从Hugging Face直接加载标准检查点，并利用Keras的多后端特性（支持JAX、PyTorch、TensorFlow）运行模型。文章还介绍了Keras中LLM的便捷功能，包括开箱即用的分词器、直接字符串生成与训练、以及聊天对话支持。此外，提供了底层访问分词器和主干网络的方法，帮助开发者灵活使用模型。
categories:
- AI产品
tags:
- Keras
- Llama 3.2
- 多后端
- keras-hub
- 大语言模型
draft: false
translated_at: '2026-06-15T07:20:08.816868'
---

# Keras 中的 Llama 3.2

这将是有史以来最短的博客文章。

问题：Llama 3.2 两周前已在 Hugging Face / Transformers 上发布。它什么时候能在 Keras 中使用？

答案：它从第一天起就可以使用了 😀。没有什么可等待的。

是的，Keras Llama3 可以从任何标准（即 safetensors）Hugging Face 检查点加载，包括 3.2 检查点。如果需要转换，它会即时完成。试试这个：

```py
!pip install keras_hub

from keras_hub import models.Llama3CausalLM
model = Llama3CausalLM.from_preset("hf://meta-llama/Llama-3.2-1B-Instruct", dtype="bfloat16")
model.generate("Hi there!")

```

#### 这里有一个Colab可以试试。尽情享受吧！🤗

好吧，好吧，有人告诉我，如果我想发表一篇博客文章，我必须填满空间。以下是关于 Keras 的一些额外信息。

## Keras 是多后端的

Keras 是经过时间考验的 JAX、PyTorch 和 TensorFlow 建模库。你可能已经注意到演示 Colab 中的这一行：

```py
import os
os.environ["KERAS_BACKEND"] = "jax" 

```

它必须出现在import keras之前，并控制模型是在 JAX、PyTorch 还是 TensorFlow 上运行。非常方便，可以在 JAX 上使用 XLA 编译来尝试你最喜欢的模型 🚀。

## 什么是 keras-hub？

Keras 是一个建模库，而keras-hub是其预训练模型的集合。它以前被称为KerasNLP和KerasCV。重命名正在进行中。它拥有所有流行的预训练模型（Llama3、Gemma、StableDiffusion、Segment Anything……）及其在 Keras 中的规范实现。

## Keras 中的 LLM 是“开箱即用”的

我的意思是，“包含分词器”。model.generate()直接对字符串起作用：

```py
model.generate("Hi there!")
> "Hi there! I'm looking for information on how to ...

```

训练也是如此。你可以直接在一组字符串上进行训练：

```py
model.fit(strings) 

```

## 与 LLM 聊天

流行 LLM 的指令微调变体可用于逐轮对话。这里，Llama-3.2-1B-Instruct 理解以下对话标记（参见meta文档）。

```
<|start_header_id|>system<|end_header_id|>You  are a helpful assistant<|eot_id|>\n
\n
<|start_header_id|>user<|end_header_id|>Hello_<|eot_id|>\n
\n
<|start_header_id|>assistant<|end_header_id|>\n
\n

```

对话以这种方式格式化后，可以直接输入到model.generate()中。

为方便起见，演示Colab实现了一个名为ChatState的辅助类，它可以自动进行必要的字符串拼接。

## 更低级别的访问：分词器、主干网络

如果你不喜欢“开箱即用”并希望访问底层的分词器和模型，它们很容易访问：

```py

model.preprocessor.tokenizer


model.backbone


backbone = keras_hub.models.Llama3CausalLM.from_preset("hf://meta-llama/Llama-3.2-1B-Instruct", dtype="float16")
tokenizer = keras_hub.models.Llama3Tokenizer.from_preset("hf://meta-llama/Llama-3.2-1B-Instruct")

```

## 等等，分词器、预处理器？我有点困惑

分词器只是将文本转换为整数向量。这里 "Hello" 转换为单个 Token：

```py
tokenizer("Hello")
> Array([9906], dtype=int32)

```

预处理器是一个包罗万象的概念，用于执行模型所需的所有数据转换。例如，对于涉及图像的任务，可能是图像调整大小或增强，或者像这里对于文本模型一样的文本分词。对于 CausalLM 任务，预处理器负责处理三个额外的细节：

- 添加模型期望的文本开始和文本结束 Token
- 填充 Token 序列并生成掩码
- 为训练和微调生成“预期输出”。对于 CausalLM 任务，这是输入字符串向右移动一位。

```py
tokens = model.preprocessor("Hello")

tokens[0] 
> {'token_ids': Array([128000,   9906, 128009, 0, 0, 0], dtype=int32), 'padding_mask': Array([True, True, True, False, False, False], dtype=bool)}

tokens[1] 
> [9906, 128009, 0, 0, 0, 0]


model.backbone(model.preprocessor(["Hello", "Hi!"])[0]) 
> [[[ 0.9805   0.1664   0.625   ... -0.834   -0.264    0.05203]
  ...]]



```

## Keras 有内置的训练器

只需在你的训练数据集上调用model.fit(ds)。这个训练器与 Keras 中可用的各种分布式训练、混合精度、量化或LoRA/QLoRA选项兼容。它也是完全可选的。如果你愿意，可以编写自定义训练循环。

有关完整示例，请参阅演示Colab，我们在其中微调 Llama 3.2 使其像海盗一样说话：

## 你可以上传到 Hub

一旦你对微调后的模型感到满意，使用以下命令直接从 Keras 上传：

```py
model.save_to_preset("./pirate-llama")

keras_hub.upload_preset(
    uri = "hf://martin-gorner/llama-3.2-1B-pirate-instruct",
    preset = "./pirate-llama")

```

上传的模型可见这里。

## 用于推理或训练的分布式模型并行

#### 本节演示 Colab：Llama 3.1 Keras 模型并行

你们中的一些人可能会想，既然已经可以使用 Transformers 在 Hugging Face 上处理 LLM，为什么还要使用 Keras？答案：即使你不关心 Keras 作为建模框架的灵活性和可用性（你应该关心！），由于JAX及其强大的XLA编译器，Keras 是你实现高级模型并行性的最快途径。

让我们选择一个 8B 参数模型来演示：meta-llama/Llama-3.1-8B-Instruct（演示 Colab 在此）。没有量化，这个模型对于任何单个加速器来说都太大了。使用 Keras，你可以将其分片加载到多个加速器（GPU 或 TPU）上。如果你不确定“正确”的权重分片方式，大多数模型都提供了合理的默认值。这里，调用keras_hub.models.Llama3Backbone.get_layout_map(device_mesh)：

```py
devices = keras.distribution.list_devices() 
device_mesh = keras.distribution.DeviceMesh((2, 4), ["batch", "model"], devices)
layout_map = keras_hub.models.Llama3Backbone.get_layout_map(device_mesh) 
distrib = keras.distribution.ModelParallel(layout_map=layout_map, batch_dim_name="batch")
keras.distribution.set_distribution(distrib)


model = keras_hub.models.Llama3CausalLM.from_preset("hf://meta-llama/Llama-3.1-8B-Instruct")

```

如果你不信任模型提供的默认布局映射，你可以定义自己的布局映射。在这个运行在只有 8 个核心的“小型”TPU 设置上的示例中，以下布局映射比默认值稍快（54秒/周期，而不是62秒/周期）：

```py
layout_map = keras.distribution.LayoutMap(device_mesh)

layout_map["token_embedding/embeddings"] = ("model", None)
layout_map["token_embedding/reverse_embeddings"] = ("model", None)
layout_map["self_attention.*(query|key|value).kernel"] = ("model", None, None)
layout_map["self_attention.*attention_output.kernel"] = ("model", None, None)
layout_map["feedforward_intermediate_dense.kernel"] = (None, "model")
layout_map["feedforward_gate_dense.kernel"] = (None, "model")
layout_map["feedforward_output_dense.kernel"] = ("model", None)

```

查看这里的演示 Colab，它在 Google TPU v5e 上（可在Hugging Face Spaces 的 JupyterLab 中使用）在不到 8 分钟的时间内对更大的 8B Llama 进行了海盗语微调。微调后的模型在这里。如果你需要关于模型并行性和 Keras 的简短模型解释，我在这里为你准备好了。

---

> 本文由AI自动翻译，原文链接：[“Llama 3.2 in Keras”](https://huggingface.co/blog/keras-llama-32)
> 
> 翻译时间：2026-06-15 07:20
