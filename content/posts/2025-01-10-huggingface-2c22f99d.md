---
title: 视觉文档检索多语言模型发布
title_original: Visual Document Retrieval Goes Multilingual
date: '2025-01-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/vdr-2b-multilingual
author: ''
summary: 文章介绍了vdr-2b-multi-v1，一个专为多语言视觉文档检索设计的嵌入模型。该模型基于MrLight/dse-qwen2-2b-mrl-v1，在包含50万高质量样本的多语言数据集上训练，支持意大利语、西班牙语、英语、法语和德语。相比前代模型，它实现了更低显存占用和更快推理速度，支持跨语言检索（如用意大利语查德语文档），并采用套娃表示学习可缩减向量大小3倍而保持98%嵌入质量。文章还提供了通过SentenceTransformers和LlamaIndex集成的使用示例。
categories:
- AI产品
tags:
- 视觉文档检索
- 多语言嵌入
- 开源模型
draft: false
translated_at: '2026-06-02T06:34:15.936512'
---

# 视觉文档检索实现多语言化

TL;DR：我们发布了vdr-2b-multi-v1，这是用于视觉文档检索的最佳多语言嵌入模型。我们还发布了其纯英文版本vdr-2b-v1，并开源了新的vdr-multilingual-train数据集。该数据集包含50万个高质量样本，是目前最大的开源多语言合成视觉文档检索数据集。

![image/png](/images/posts/7edc374703d1.png)

介绍vdr-2b-multi-v1（🤗），这是一个专为跨多种语言和领域的视觉文档检索而设计的多语言嵌入模型。该模型旨在将文档页面截图编码为稠密单向量表示，从而有效实现对视觉丰富的多语言文档进行搜索和查询，无需任何OCR、数据提取管道、分块等操作。

vdr-2b-multi-v1模型基于MrLight/dse-qwen2-2b-mrl-v1，并在一个自建的大规模多语言查询-图像对数据集上进行了训练。该模型与LlamaIndex合作构建，是mcdse-2b-v1的下一代迭代版本。我们的vdr-2b-multi-v1扩展并改进了训练所用的学习方法和流程，从而打造出更强大、更优秀的模型。

- 基于🇮🇹意大利语、🇪🇸西班牙语、🇬🇧英语、🇫🇷法语和🇩🇪德语训练：它们共同构成了一个包含50万个高质量样本的新的大型开源多语言训练数据集。
- 低显存占用与更快推理：在合成视觉文档检索（ViDoRe）基准测试中，我们的纯英文模型使用768个图像块，性能优于使用2560个图像块的基座模型。这使得推理速度提升3倍，显存占用大幅降低。
- 跨语言检索：在真实场景中表现显著更优。例如，您可以使用意大利语查询搜索德语文档。
- 套娃表示学习：您可以将向量大小缩减3倍，同时仍保持98%的嵌入质量。这显著提升了检索速度，同时降低了存储成本。

基于🇮🇹意大利语、🇪🇸西班牙语、🇬🇧英语、🇫🇷法语和🇩🇪德语训练：它们共同构成了一个包含50万个高质量样本的新的大型开源多语言训练数据集。

低显存占用与更快推理：在合成视觉文档检索（ViDoRe）基准测试中，我们的纯英文模型使用768个图像块，性能优于使用2560个图像块的基座模型。这使得推理速度提升3倍，显存占用大幅降低。

跨语言检索：在真实场景中表现显著更优。例如，您可以使用意大利语查询搜索德语文档。

套娃表示学习：您可以将向量大小缩减3倍，同时仍保持98%的嵌入质量。这显著提升了检索速度，同时降低了存储成本。

## 使用方法

🎲 立即试用vdr-2b-multi-v1，可在该Hugging Face Space上获取！

通过SentenceTransformers和LlamaIndex的直接集成，使用vdr-2b-multi-v1生成嵌入比以往任何时候都更简单。只需几行代码即可开始：

```bash
pip install -U llama-index-embeddings-huggingface

```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

model = HuggingFaceEmbedding(
    model_name="llamaindex/vdr-2b-multi-v1",
    device="cpu",  
    trust_remote_code=True,
)

image_embedding = model.get_image_embedding("image.png")
query_embedding = model.get_query_embedding("Chi ha inventato Bitcoin?")

```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    model_name_or_path="llamaindex/vdr-2b-multi-v1",
    device="cuda",
    trust_remote_code=True,
    
    model_kwargs={
        "torch_dtype": torch.bfloat16, 
        "device_map": "cuda:0", 
        "attn_implementation": "flash_attention_2"
    },
)

embeddings = model.encode("image.png")

```

## 训练数据集

训练用于视觉文档检索的优秀单向量模型需要高质量数据，但当前现成的多模态数据集非常稀缺且不具备多语言能力。

因此，我们投入了大量时间从头构建该数据集。原始数据集包含50万个多语言查询-图像样本，通过使用公开互联网PDF文件从头收集和生成。与每张图像关联的查询是使用VLM合成的。作为对比，我们的数据集样本量是此前最大的开源多模态视觉文档检索合成数据集（即为ColPali训练数据集生成的抓取文档）的10倍。

![image/png](/images/posts/e11d0da396f1.png)

### 数据收集

针对每种语言，我们生成了一个涵盖众多不同主题的搜索查询长列表，然后用这些查询搜索PDF文件。我们利用搜索引擎的语言过滤功能，仅抓取指定语言的文档。这种"按主题搜索"技术确保了模型接触到大量多样化的主题和领域，从而在真实场景中表现良好。

抓取过程产生了约5万个多语言文档。与之前mcdse-2b-v1模型使用的方法不同，页面并非随机提取。相反，每个PDF的每一页都经过文档布局分析模型处理，以判断该页包含更多文本元素还是视觉元素。结果是一个数字，将页面分类为纯文本、纯视觉或混合类型。随后利用这一标注步骤采样了约10万个页面，确保它们按页面类型均匀分布。

### 合成生成

随后使用gemini-1.5-pro和Qwen2-VL-72B生成查询。它们的任务是提出一个具体问题和一个一般性问题。只有具体问题被用于训练模型，但强制LLM区分两者通常会产生更高质量的具体问题，适用于信息检索训练。

生成之后，进一步的清洗步骤确保问题质量足以用于训练。这包括：

- 确保语言正确
- 修复格式问题
- 移除Markdown
- 确保只提出一个问题
- 移除引用短语（例如"根据图1"、"本文档"等）

### 过滤与难负样本挖掘

这一清洗步骤确保了查询在语法上正确并遵循一些严格准则。但这仍不能保证查询对信息检索足够有效。

为了过滤掉低质量问题，我们使用voyage-3嵌入模型对每个宽泛查询进行了嵌入和索引。对于每个具体问题，我们搜索索引。如果其关联的宽泛问题出现在前100个结果中，则该查询被标记为"良好"。这种方法移除了低熵、重复或过于相似的问题。平均而言，每个语言数据集中有40%的查询被移除。

随后，仅针对具体问题使用voyage-3进行难负样本挖掘，固定阈值为0.75。还按照nvidia/NV-Retriever-v1中描述的方法进行了正感知负样本挖掘实验，但在该数据集上，这种方法似乎产生了过于简单/距离过远的负样本。

### 下载

vdr-multilingual-train（🤗）训练数据集现已开源，可直接在Hugging Face上获取。该训练数据集包含496,167个PDF页面，其中只有280,679个页面与经过过滤的查询相关联（使用上述方法）。没有关联查询的图像仍被用作难负样本。

该数据集由5个不同的子集组成，每种语言对应一个。您可以在此处直接探索：

或者，您可以通过在load_dataset中指定语言子集来单独下载各语言数据：

```python
from datasets import load_dataset

italian_dataset = load_dataset("llamaindex/vdr-multilingual-train", "it", split="train")

english_dataset = load_dataset("llamaindex/vdr-multilingual-train", "en", split="train")

french_dataset = load_dataset("llamaindex/vdr-multilingual-train", "fr", split="train")

```

```python
german_dataset = load_dataset("llamaindex/vdr-multilingual-train", "de", split="train")

spanish_dataset = load_dataset("llamaindex/vdr-multilingual-train", "es", split="train")

```

## 评估

![image/png](/images/posts/cd879c536974.png)

该模型已在ViDoRe基准测试以及自建评估集上进行了评估，这些评估集能够测试其在纯文本、纯视觉及混合页面截图上的多语言能力。评估数据集同样在Hugging Face上公开提供（vdr-multilingual-test 🤗）。

我们确保这些数据集中的页面均未出现在训练集中，以避免任何评估污染。数据集采用与训练集相同的方法收集和生成，但样本量更小。过滤步骤全部由人工完成：每个查询都经过评估、整理和（必要时）改进，以确保数据质量。

所有评估均通过计算NDCG@5分数完成，使用1536维向量以及最多可用768个Token表示的图像分辨率。

多语言模型在每种语言和每种页面类型上的表现均优于基础模型，平均提升+2.3%。在ViDoRe基准测试上，其表现也略好（+0.5%）。
我们微调后的vdr-2b-multi-v1在性能上取得了巨大飞跃，尤其是在非英语的纯视觉或混合页面场景中。例如，在德语纯视觉检索中，相比基础模型，NDCG@5提升了+6.33%。

我们还训练了一个仅使用英语子集的版本（vdr-2b-v1 🤗）。在完整的ViDoRe基准测试（使用768个图像Token评估）上，多语言版本和纯英语版本的表现均优于基础模型。

### 更快的推理

![image/png](/images/posts/f70ea1a8f8e4.png)

纯英语版本的vdr-2b-v1模型在ViDoRe基准测试的合成数据集上也达到了与基础模型相当的性能，同时仅使用了30%的图像Token（768 vs. 2560）。这实际上实现了3倍的推理速度提升和更低的VRAM使用量。

### 跨语言检索

尽管模型是针对每种语言分别训练的，但它在跨语言检索方面也有所改进。为了测试这一能力，德语评估集的查询使用DeepL翻译成了意大利语。文档页面截图仍保留原始德语。

该模型在所有文档类型上均有显著提升，平均改进幅度为+2.3%。这些检索能力对于实际应用场景至关重要，尤其是在像欧洲这样语言多样的大陆。例如，它能够对复杂的多语言来源（如欧洲具有约束力的裁决、使用说明书、金融资产KID、药品说明书等）进行与语言无关的搜索。

### MRL与二值嵌入

该模型使用Matryoshka表示学习（MRL）进行训练。训练过程中使用的损失函数经过校准，以跟踪所有维度的性能，从而引导模型将最重要的识别信息前置。这实际上允许您根据规模和预算缩减嵌入维度。
要了解更多关于MRL的信息，Hugging Face的这篇博文解释得非常清楚。

为了测试模型在不同向量维度下的检索能力，我们在意大利语→德语的跨语言基准上进行了评估。

#### NDCG@5（浮点型）

#### NDCG@5（二值型）

1024维浮点向量在质量和大小之间提供了非常好的平衡。它们小了约30%，但仍保留了99%的检索性能。这对于1536维的二值向量同样成立，其每个向量的字节数减少了10倍，但仍保留了97%的检索质量。同样有趣的是，1536维二值向量的性能几乎与基础模型的1536维浮点向量相当。

## 结论与下一步计划

我们相信vdr-2b-multi-v1和vdr-2b-v1将对许多用户大有裨益。

我们的多语言模型是同类首创，它显著提升了多语言和跨语言场景下的性能，并且得益于MRL和二值量化，检索比以往任何时候都更高效、更快速。我们相信这将开启新的用例和机遇，尤其是在像欧洲这样语言多样的大陆。

其纯英语孪生模型相比基础模型有了显著改进，现在能够以3倍的速度嵌入文档，消耗更少的VRAM，并保持相同（或更好）的检索质量。

所有这些都得益于新的vdr-multilingual-train数据集。该数据集包含50万个高质量样本，是用于视觉文档检索的最大规模多语言开源合成数据集。

未来的工作将探索我们的模型在适应新的特定领域时的表现。这仍处于早期开发阶段，在结果公布之前还需要做更多工作，但早期测试似乎已经表明，使用极少的数据和计算资源即可获得令人印象深刻的检索增益。

敬请期待未来的更新！

## 链接

- 🎲 模型演示：Hugging Face Space
- 🤗 多语言模型：vdr-2b-multi-v1
- 🤗 纯英语模型：vdr-2b-v1
- 📂 训练数据集：vdr-multilingual-train
- 📂 评估数据集：vdr-multilingual-test
```

---

> 本文由AI自动翻译，原文链接：[Visual Document Retrieval Goes Multilingual](https://huggingface.co/blog/vdr-2b-multilingual)
> 
> 翻译时间：2026-06-02 06:34
