---
title: 使用Sentence Transformers实现多模态嵌入与重排序
title_original: Multimodal Embedding & Reranker Models with Sentence Transformers
date: '2026-04-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/multimodal-sentence-transformers
author: ''
summary: 本文介绍了Sentence Transformers库v5.4版本新增的多模态功能，支持文本、图像、音频和视频的编码与比较。文章详细讲解了多模态嵌入模型如何将不同模态的输入映射到共享向量空间，以及多模态重排序模型如何为混合模态对进行相关性打分。通过具体代码示例，展示了模型加载、图像编码、跨模态相似性计算及混合文档排序等核心操作，为构建视觉文档检索、跨模态搜索和多模态RAG管道等应用提供了实用指南。
categories:
- AI基础设施
tags:
- 多模态AI
- Sentence Transformers
- 嵌入模型
- 语义搜索
- RAG
draft: false
translated_at: '2026-04-10T04:49:12.271794'
---

# 使用 Sentence Transformers 的多模态嵌入与重排序模型

Sentence Transformers 是一个用于使用和训练嵌入及重排序模型的 Python 库，适用于检索增强生成、语义搜索等应用。通过 v5.4 更新，您现在可以使用同样熟悉的 API 来**编码和比较文本、图像、音频和视频**。在这篇博客文章中，我将向您展示如何将这些新的多模态能力用于嵌入和重排序。

多模态嵌入模型将来自不同模态的输入映射到一个共享的嵌入空间，而多模态重排序模型则为混合模态对的相关性打分。这开启了诸如视觉文档检索、跨模态搜索和多模态 RAG 管道等用例。

-   什么是多模态模型？
-   安装
-   多模态嵌入模型
    -   加载模型
    -   编码图像
    -   跨模态相似性
    -   编码查询与文档
-   多模态重排序模型
    -   对混合模态文档进行排序
    -   预测配对分数
-   检索与重排序
-   输入格式与配置
    -   支持的输入类型
    -   检查模态支持
    -   处理器与模型参数
-   支持的模型
-   额外资源

## 什么是多模态模型？

传统的嵌入模型将文本转换为**固定大小的向量**。多模态嵌入模型通过将来自不同模态（文本、图像、音频或视频）的输入映射到一个共享的嵌入空间来扩展这一功能。这意味着您可以使用已经熟悉的相同相似度函数，将文本查询与图像文档（或反之）进行比较。

类似地，传统的重排序（交叉编码器）模型计算文本对之间的相关性分数。多模态重排序器可以为其中一个或两个元素是图像、图文组合文档或其他模态的配对进行打分。

例如，您可以将文本查询与图像文档进行比较，查找与描述匹配的视频片段，或者构建跨模态工作的 RAG 管道。

## 安装

多模态模型需要一些额外的依赖项。请根据需要安装对应模态的额外组件（更多详情请参见[安装](https://www.sbert.net/docs/installation.html)）：

```bash
pip install -U "sentence-transformers[image]"
pip install -U "sentence-transformers[audio]"
pip install -U "sentence-transformers[video]"
pip install -U "sentence-transformers[image,video,train]"
```

基于 VLM 的模型（如 Qwen3-VL-2B）需要至少约 8 GB 显存的 GPU。对于 8B 变体，预计需要约 20 GB。如果您没有本地 GPU，请考虑使用云 GPU 服务或 Google Colab。在 CPU 上，这些模型会极其缓慢；纯文本或 CLIP 模型更适合 CPU 推理。

## 多模态嵌入模型

### 加载模型

加载多模态嵌入模型与加载纯文本模型完全相同：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")
```

目前需要 `revision` 参数，因为这些模型的集成拉取请求仍在等待中。一旦它们被合并，您将能够在不指定修订版本的情况下加载它们。

模型会自动检测其支持的模态，因此无需额外配置。如果您想控制图像分辨率或模型精度等设置，请参阅**处理器与模型参数**。

### 编码图像

加载多模态模型后，`model.encode()` 可以接受图像和文本。图像可以作为 URL、本地文件路径或 PIL Image 对象提供（所有接受的格式请参见**支持的输入类型**）：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")

# 编码图像
img_embeddings = model.encode([
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
])
print(img_embeddings.shape)
# (2, 4096)
```

### 跨模态相似性

您可以计算文本嵌入和图像嵌入之间的相似性，因为模型将两者映射到了同一空间：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")

# 编码图像
img_embeddings = model.encode([
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
])

# 编码文本
text_embeddings = model.encode([
    "A green car parked in front of a yellow building",
    "A red car driving on a highway",
    "A bee on a pink flower",
    "A wasp on a wooden table",
])

# 计算相似性
similarities = model.similarity(text_embeddings, img_embeddings)
print(similarities)
# tensor([[0.5107, 0.2108],
#         [0.3928, 0.1835],
#         [0.2566, 0.6705],
#         [0.1958, 0.4636]])
```

正如预期的那样，"A green car parked in front of a yellow building" 与汽车图像最相似（0.51），而 "A bee on a pink flower" 与蜜蜂图像最相似（0.67）。硬负例（"A red car driving on a highway", "A wasp on a wooden table"）正确地获得了较低的分数。

您可能会注意到，即使是最佳匹配分数（0.51, 0.67）也并非非常接近 1.0。这是由于**模态鸿沟**：来自不同模态的嵌入倾向于聚集在空间的不同区域。跨模态相似性通常低于模态内相似性（例如，文本到文本），但相对顺序得以保留，因此检索仍然效果良好。

### 编码查询与文档

对于检索任务，`encode_query()` 和 `encode_document()` 是推荐的方法。许多检索模型会根据输入是查询还是文档来添加不同的指令提示词，类似于聊天模型根据目标应用不同系统提示词的方式。模型作者可以在模型配置中指定他们的提示词，而 `encode_query()`/`encode_document()` 会自动加载并应用正确的提示词：

-   `encode_query()` 使用模型的 "query" 提示词（如果可用）并设置 `task="query"`。
-   `encode_document()` 使用 "document"、"passage" 或 "corpus" 中第一个可用的提示词，并设置 `task="document"`。

在底层，两者都是 `encode()` 的简单封装，它们只是为您处理提示词选择。以下是跨模态检索的示例：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")

# 编码查询
query_embeddings = model.encode_query([
    "Find me a photo of a vehicle parked near a building",
    "Show me an image of a pollinating insect",
])

# 编码文档
doc_embeddings = model.encode_document([
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
])

# 计算相似性
similarities = model.similarity(query_embeddings, doc_embeddings)
print(similarities)
# tensor([[0.5107, 0.2108],
#         [0.2566, 0.6705]])
```

这些方法接受与 `encode()` 相同的输入类型（图像、URL、多模态字典等），并传递相同的参数。对于没有专门查询/文档提示词的模型，它们的行为与 `encode()` 完全相同。

## 多模态重排序模型

多模态重排序（交叉编码器）模型对输入对之间的相关性进行打分，其中每个元素可以是文本、图像、音频、视频或其组合。它们在质量上往往优于嵌入模型，但由于需要单独处理每个配对，因此速度较慢。目前可用的预训练多模态重排序器主要关注文本和图像输入，但其架构支持底层模型可以处理的任何模态。

### 对混合模态文档进行排序

`rank()` 方法根据查询对文档列表进行打分和排序，支持混合模态：

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("Qwen/Qwen3-VL-Rerank-2B", revision="refs/pr/11")

query = "一辆绿色汽车停在一栋黄色建筑前"
documents = [
    
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
    
    "一辆涂成亮绿色的复古大众甲壳虫停在车道上。",
    
    {
        "text": "欧洲城市里的一辆车",
        "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    },
]

rankings = model.rank(query, documents)
for rank in rankings:
    print(f"{rank['score']:.4f}\t(document {rank['corpus_id']})")
"""
0.9375  (document 0)
0.5000  (document 3)
-1.2500 (document 2)
-2.4375 (document 1)
"""

```

重排序器正确地将汽车图像（文档0）识别为最相关的结果，其次是关于欧洲城市汽车的图文混合文档（文档3）。蜜蜂图像（文档1）得分最低。
请注意，**模态差异**会影响绝对分数：图文对的分数范围可能与文-文对或图-图对的分数范围不同。

你也可以像使用嵌入模型一样，使用 `modalities` 和 `supports()` 来检查重排序器支持哪些模态：

```python
print(model.modalities)


print(model.supports("image"))



print(model.supports(("image", "text")))


```

### 预测配对分数

你也可以使用 `predict()` 来获取特定输入对的原始相关性分数：

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("jinaai/jina-reranker-m0", trust_remote_code=True)

scores = model.predict([
    ("一辆绿色汽车", "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg"),
    ("花朵上的一只蜜蜂", "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"),
    ("一辆绿色汽车", "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"),
])
print(scores)


```

## 检索与重排序

一种常见的模式是使用嵌入模型进行快速的初始检索，然后用重排序器对顶部结果进行精炼：

```python
from sentence_transformers import SentenceTransformer, CrossEncoder


embedder = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")

query = "收入增长图表"
query_embedding = embedder.encode_query(query)


document_screenshots = [
    "path/to/doc1.png",
    "path/to/doc2.png",
    
]
corpus_embeddings = embedder.encode_document(document_screenshots, show_progress_bar=True)


similarities = embedder.similarity(query_embedding, corpus_embeddings)
top_k_indices = similarities.argsort(descending=True)[0][:10]


reranker = CrossEncoder("nvidia/llama-nemotron-rerank-vl-1b-v2", trust_remote_code=True)

top_k_documents = [document_screenshots[i] for i in top_k_indices]
rankings = reranker.rank(query, top_k_documents)
for rank in rankings:
    print(f"{rank['score']:.4f}\t{top_k_documents[rank['corpus_id']]}")

```

由于语料库嵌入是预先计算好的，即使面对数百万文档，初始检索也很快。然后，重排序器在较小的候选集上提供更精确的评分。

## 输入格式与配置

### 支持的输入类型

多模态模型接受多种输入格式。以下是你可以传递给 `model.encode()` 的内容总结：

### 检查模态支持

你可以使用 `modalities` 属性和 `supports()` 方法来检查模型支持哪些模态：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B", revision="refs/pr/23")


print(model.modalities)



print(model.supports("image"))

print(model.supports("audio"))


```

`"message"` 模态表示模型接受带有交错内容的聊天式消息输入。在实践中，你很少需要直接使用它。当你传递字符串、URL 或多模态字典时，模型会在内部将它们转换为适当的消息格式。Sentence Transformers 支持两种消息格式：

- **结构化**（大多数 VLM，例如 Qwen3-VL）：内容是一个类型化字典的列表，例如 `[{"type": "text", "text": "..."}, {"type": "image", "image": ...}]`
- **扁平化**（例如 Deepseek-V3）：内容是直接的值，例如 `"some text"`

格式会根据模型的聊天模板自动检测。

由于所有输入在内部都会转换为相同的消息格式，你可以在单个 `encode()` 调用中混合输入类型：

```python
embeddings = model.encode([
    
    "一辆绿色汽车停在一栋黄色建筑前",
    
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    
    {
        "text": "欧洲城市里的一辆车",
        "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    },
])

```

如果一个模型不遵循上述任何一种格式，而你需要完全控制，你可以直接传递带有 `role` 和 `content` 键的原始消息字典：

```python
embeddings = model.encode([
    [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg"},
                {"type": "text", "text": "描述这辆车。"},
            ],
        }
    ],
])

```

这会绕过自动格式转换，直接将消息传递给处理器的 `apply_chat_template()`。

### 处理器和模型参数

你可能希望控制图像分辨率边界或模型精度。在加载模型时使用 `processor_kwargs` 和 `model_kwargs`：

```python
model = SentenceTransformer(
    "Qwen/Qwen3-VL-Embedding-2B",
    model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"},
    processor_kwargs={"min_pixels": 28 * 28, "max_pixels": 600 * 600},
    revision="refs/pr/23",
)

```

- `processor_kwargs` 控制输入如何预处理（例如，图像分辨率边界）。更高的 `max_pixels` 意味着更高的质量，但也需要更多的内存和计算。这些参数直接传递给 `AutoProcessor.from_pretrained(...)`。
- `model_kwargs` 控制底层模型的加载方式（例如，精度、注意力实现）。这些参数直接传递给相应的 `AutoModel.from_pretrained(...)` 调用（例如，`AutoModel`、`AutoModelForCausalLM`、`AutoModelForSequenceClassification` 等，具体取决于模型模块的配置）。

有关这些参数的更多详细信息，请参阅 `SentenceTransformer` API 参考文档。

在 Sentence Transformers v5.4 中，`tokenizer_kwargs` 已更名为 `processor_kwargs`，以反映多模态模型使用的是处理器而不仅仅是分词器。旧名称仍然被接受，但已弃用。

## 支持的模型

以下是 v5.4 版本支持的多模态模型，也可在 `v5.4 integrations` 集合中找到：

### 支持的多模态嵌入模型

### 支持的多模态重排序模型

### 纯文本重排序模型（同样在 v5.4 中新增）

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("mixedbread-ai/mxbai-rerank-base-v2")

query = "如何烘焙酸面包？"
documents = [
    "酸面包需要一种由面粉和水制成的酵种，发酵数天。",
    "面包的历史可以追溯到公元前 8000 年左右的古埃及。",
    "要烘焙酸面包，将你的酵种与面粉、水和盐混合，然后让它发酵一夜。",
    "黑麦面包是北欧地区小麦面包的一种流行替代品。",
]

pairs = [(query, doc) for doc in documents]
scores = model.predict(pairs)
print(scores)


rankings = model.rank(query, documents)
for rank in rankings:
    print(f"{rank['score']:.4f}\t{documents[rank['corpus_id']]}")





```

### CLIP 模型

较旧的CLIP模型仍将继续获得支持：

这些简单的CLIP模型在资源有限的硬件上依然表现良好。

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/clip-ViT-L-14")

images = [
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
    "https://huggingface.co/datasets/huggingface/cats-image/resolve/main/cats_image.jpeg"
]
texts = ["A green car", "A bee on a flower", "Some cats on a couch", "One cat sitting in the window"]

image_embeddings = model.encode(images)
text_embeddings = model.encode(texts)
print(image_embeddings.shape, text_embeddings.shape)


similarities = model.similarity(image_embeddings, text_embeddings)
print(similarities)




```

## 其他资源

### 文档

- Sentence Transformer > 使用指南
- Sentence Transformer > 预训练模型
- Cross Encoder > 使用指南
- Cross Encoder > 预训练模型
- 安装指南

### 训练

我将在未来几周内发布一篇关于训练和微调多模态模型的博客文章，敬请关注！在此期间，您可以尝试使用预训练模型进行推理，或者参考训练文档进行实验：

- Sentence Transformer > 训练概述
- Sentence Transformer > 训练示例
- Cross Encoder > 训练概述
- Cross Encoder > 训练示例
- Sparse Encoder > 训练概述
- Sparse Encoder > 训练示例

### Hugging Face Hub

- Hub上的Sentence Transformers模型
- Hub上的Sentence Transformers数据集
- v5.4 集成集合

---

> 本文由AI自动翻译，原文链接：[Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/multimodal-sentence-transformers)
> 
> 翻译时间：2026-04-10 04:49
