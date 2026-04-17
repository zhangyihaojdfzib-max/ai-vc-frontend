---
title: 使用Sentence Transformers训练多模态嵌入与重排序模型
title_original: Training and Finetuning Multimodal Embedding & Reranker Models with
  Sentence Transformers
date: '2026-04-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/train-multimodal-sentence-transformers
author: ''
summary: 本文详细介绍了如何利用Sentence Transformers库训练和微调多模态嵌入与重排序模型，特别是针对视觉文档检索任务。文章以微调Qwen3-VL-Embedding-2B模型为例，展示了在特定领域数据上微调能显著提升性能（NDCG@10从0.888提升至0.947），并优于更大尺寸的模型。文中系统讲解了训练组件，包括模型、数据集、损失函数、训练参数、评估器和训练器，为读者提供了完整的多模态模型训练指南。
categories:
- AI研究
tags:
- 多模态模型
- Sentence Transformers
- 视觉文档检索
- 模型微调
- 嵌入模型
draft: false
translated_at: '2026-04-17T04:49:30.185592'
---

# 使用 Sentence Transformers 训练和微调多模态嵌入与重排序模型

Sentence Transformers 是一个用于使用和训练嵌入及重排序模型的 Python 库，适用于检索增强生成、语义搜索等应用。在我之前的博客文章中，我介绍了新的多模态功能，展示了如何使用能处理文本、图像、音频和视频的嵌入和重排序模型。在这篇博客文章中，我将向你展示如何在自己的数据上**训练或微调**这些多模态模型。

作为一个实际例子，我将详细介绍如何为视觉文档检索任务微调 **Qwen/Qwen3-VL-Embedding-2B**。视觉文档检索的任务是根据给定的文本查询，从语料库中检索出相关的文档页面。这些页面以图像形式呈现，其中的图表、表格和布局都保持完整。最终得到的模型 **tomaarsen/Qwen3-VL-Embedding-2B-vdr** 展示了通过在自己领域的数据上进行微调能获得多大的性能提升。在我的评估数据上，微调后的模型 NDCG@10 达到了 0.947，而基础模型为 0.888，并且性能优于我测试过的所有现有 VDR 模型，包括尺寸是其 4 倍的模型。

![VDR 模型的模型大小与 NDCG 对比图](/images/posts/f2154bf2c3e7.png)

如果你不熟悉 Sentence Transformers 中的多模态模型，我建议先阅读《使用 Sentence Transformers 的多模态嵌入与重排序模型》。要训练纯文本嵌入、重排序或稀疏嵌入模型，请参阅文末的“先前博客文章”部分。

- 为何要微调？
- 训练组件
    - 模型
    - 数据集
        - 视觉文档检索数据集
        - 数据集格式
    - 损失函数
        - CachedMultipleNegativesRankingLoss
        - MatryoshkaLoss
    - 训练参数
    - 评估器
    - 训练器
- 结果
    - 模型大小 vs NDCG@10
    - Matryoshka 维度 vs NDCG@10
- 训练多模态重排序模型
- 额外资源
    - 先前博客文章
    - 训练示例
    - 文档

## 为何要微调？

像 **Qwen/Qwen3-VL-Embedding-2B** 这样的通用多模态嵌入模型，是在多样化的数据上训练的，以便在广泛的语言和任务中表现良好：图文匹配、视觉问答、文档理解等等。但这种通用性意味着该模型对于任何特定任务来说，很少是最佳选择。

以视觉文档检索为例：给定一个文本查询，例如“公司第三季度的收入是多少？”，模型必须从包含数千个文档的语料库中找到最相关的文档截图。这需要理解文档布局、图表、表格和文本，这与例如将鞋子图片与产品描述相匹配所需的技能截然不同。

通过在特定领域的数据上进行微调，模型可以学习这些专门的模式。在我的实验中，微调将 NDCG@10 从 0.888 提高到了 0.947，优于我测试过的所有近期多模态模型，包括尺寸是其 4 倍的模型。

## 训练组件

训练多模态 Sentence Transformer 模型涉及的组件与训练纯文本模型相同：

1.  **模型**：要训练或微调的多模态模型。
2.  **数据集**：用于训练和评估的数据。
3.  **损失函数**：量化模型性能并指导优化过程的函数。
4.  **训练参数**：影响训练性能和跟踪/调试的参数。
5.  **评估器**：用于在训练前、训练中或训练后评估模型的工具。
6.  **训练器**：将模型、数据集、损失函数和其他组件整合在一起进行训练。

多模态训练流程使用与纯文本训练相同的 **SentenceTransformerTrainer**。关键区别在于你的数据集除了文本外还包含图像，并且模型的处理器会自动处理图像预处理。

让我们以视觉文档检索为例，逐一介绍每个组件。

## 模型

最常见的方法是微调现有的多模态嵌入模型，或者从视觉语言模型检查点开始。**Transformer** 模块会自动从模型的处理器中检测支持的模态。

要微调现有的多模态嵌入模型，你可以传递 `processor_kwargs` 和 `model_kwargs` 来分别控制预处理和模型加载。`processor_kwargs` 直接传递给 `AutoProcessor.from_pretrained(...)`，而 `model_kwargs` 则传递给相应的 `AutoModel.from_pretrained(...)` 调用：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "Qwen/Qwen3-VL-Embedding-2B",
    model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"},
    processor_kwargs={"min_pixels": 28 * 28, "max_pixels": 600 * 600},
)
```

你也可以从一个尚未针对嵌入任务训练的全新 VLM 检查点开始。Sentence Transformers 将尝试识别架构，从处理器推断支持的模态，并设置适当的前向方法和池化层。如果自动检测对某个特定模型效果不理想，可以编辑保存的 `sentence_bert_config.json` 中的配置来调整模态设置、前向方法和输出处理：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-VL-2B")
```

在这两种情况下，**Transformer** 模块都会检查处理器以确定可用的模态，如果需要，会自动添加 **Pooling**。你可以验证支持的模态：

```python
print(model.modalities)


print(model.supports("image"))


```

除了使用单个 VLM 主干网络，你还可以使用 **Router** 模块为不同模态组合单独的编码器。这允许你结合任何现有的编码器，并根据检测到的模态将输入路由到相应的编码器：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Dense, Pooling, Router, Transformer


text_encoder = Transformer("sentence-transformers/all-MiniLM-L6-v2")
text_pooling = Pooling(text_encoder.get_embedding_dimension(), pooling_mode="mean")
text_projection = Dense(text_encoder.get_embedding_dimension(), 768)


image_encoder = Transformer("google/siglip2-base-patch16-224")


router = Router(
    sub_modules={
        "text": [text_encoder, text_pooling, text_projection],
        "image": [image_encoder],
    },
)

model = SentenceTransformer(modules=[router])
```

由于基于 Router 的多模态模型为每个模态使用独立的编码器，它们的嵌入空间最初是未对齐的。需要进行训练来对齐这些空间，以实现有意义的跨模态相似性计算。上面展示的 **Dense** 投影层有助于将来自不同编码器的嵌入映射到一个共享空间。

当你希望使用轻量级、专门的编码器而不是大型 VLM 时，这种方法很有用。你还可以使用 `route_mappings` 将基于 Router 的多模态与基于任务的路由结合起来。有关高级路由场景，请参阅 **Router** 文档。

## 数据集

### 视觉文档检索数据集

在本示例中，我使用了 `tomaarsen/llamaindex-vdr-en-train-preprocessed` 数据集，这是 `llamaindex/vdr-multilingual-train` 的一个经过预处理的英文子集。源数据集由 LlamaIndex 随其博客文章《Visual Document Retrieval Goes Multilingual》一同发布，包含从公开互联网 PDF 中收集的约 50 万条多语言查询-图像样本，其中的查询是使用 VLM（gemini-1.5-pro 和 Qwen2-VL-72B）合成生成的。
我预处理的版本筛选出 53,512 个英文样本，并将每个样本中 16 个基于 ID 的困难负例中的 4 个解析为实际的文档截图图像，因此无需进一步预处理即可直接用于训练：

```python
from datasets import load_dataset

train_dataset = load_dataset("tomaarsen/llamaindex-vdr-en-train-preprocessed", "train", split="train")
train_dataset = train_dataset.select_columns(["query", "image", "negative_0"])
eval_dataset = load_dataset("tomaarsen/llamaindex-vdr-en-train-preprocessed", "eval", split="train")

```

`train` 配置包含前 10,000 个样本，`eval` 配置包含接下来的 300 个样本（也提供了包含全部 53,512 个样本的 `full` 配置）。对于训练，我选择 `query`、`image` 和 `negative_0` 来构成（锚点、正例、困难负例）三元组。包含更多困难负例可能会提升训练信号，但每个额外的负例也会增加内存使用和训练时间，因此我只使用一个。对于评估，我为每个查询保留全部四个困难负例，以构建一个更具挑战性的检索语料库（更多细节见“评估器”部分）。

### 数据集格式

与纯文本训练一样，数据集格式必须与你选择的**损失函数**匹配。规则相同：

1.  如果你的损失函数需要一个**标签**，你的数据集必须有一个名为 `"label"` 或 `"score"` 的列。
2.  除 `"label"` 或 `"score"` 之外的所有列都被视为**输入**。这些列的数量必须与你所选损失函数的有效输入数量匹配。除了标签列，列名无关紧要，重要的是顺序。

对于多模态数据集，输入可以包含：

*   **文本**：字符串。
*   **图像**：PIL 图像、文件路径、URL 或 numpy/torch 数组。
*   **音频**：文件路径、numpy/torch 数组、包含 `"array"` 和 `"sampling_rate"` 键的字典，或（如果安装了 `torchcodec`）`torchcodec.AudioDecoder` 实例。
*   **视频**：文件路径、numpy/torch 数组、包含 `"array"` 和 `"video_metadata"` 键的字典，或（如果安装了 `torchcodec`）`torchcodec.VideoDecoder` 实例。
*   **多模态字典**：将模态名称映射到值的字典，例如 `{"text": ..., "image": ...}`。键必须是 `"text"`、`"image"`、`"audio"` 或 `"video"`。

数据整理器会自动调用 `model.preprocess()`，它会检测每个输入的模态并应用适当的预处理。无需手动进行分词或图像处理。

许多开箱即用支持 Sentence Transformers 的 Hugging Face 数据集都已被标记为 `sentence-transformers`，你可以轻松在 `https://huggingface.co/datasets?other=sentence-transformers` 找到它们。

## 损失函数

### CachedMultipleNegativesRankingLoss

对于本次训练，我使用 `CachedMultipleNegativesRankingLoss`，这是检索任务的常见选择。它接受（查询，正例）对以及任意数量的额外困难负例列（从 0 到 n），只要每个样本具有相同数量的负例。
在训练期间，该损失函数会推动每个查询与其正例的相似度**上升**，与其所有负例的相似度**下降**。负例来自两个来源：

1.  **困难负例**：数据集中明确提供的负例列（在我们的三元组设置中仅为 `negative_0`）。
2.  **批次内负例**：同一批次中**其他**样本的正例和困难负例，被重新用作该查询的额外负例，且无需额外成本。

每个查询的负例越多，训练信号越强，因此更大的批次大小直接提升了训练质量。此外，该损失函数的“缓存”变体使用梯度缓存，使得即使在 GPU 内存有限的情况下，也能实现大的有效批次大小。

`mini_batch_size` 参数控制在缓存前向传播过程中一次处理的样本数量。对于大型多模态模型，将其设置为较小的值（例如 1）非常重要，这样可以在不牺牲大有效批次大小优势的情况下避免内存不足错误：

```python
from sentence_transformers.sentence_transformer.losses import CachedMultipleNegativesRankingLoss

loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=1)

```

### MatryoshkaLoss

为了生成在多种维度下都能良好工作的嵌入，我用 `MatryoshkaLoss` 包装了基础损失函数。这可以训练模型，使得将嵌入截断到更少的维度后仍能保持良好的性能：

```python
from sentence_transformers.sentence_transformer.losses import CachedMultipleNegativesRankingLoss, MatryoshkaLoss

loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=1)
loss = MatryoshkaLoss(model, loss, matryoshka_dims=[2048, 1536, 1024, 512, 256, 128, 64])

```

这对于多模态模型尤其有用，因为其嵌入可能很大（Qwen3-VL 为 2048 维）。通过 Matryoshka 训练，你可以在部署时使用截断的嵌入（例如 256 或 128 维）以实现更快的搜索，同时质量损失最小。正如我将在“结果”部分展示的，微调后的模型即使在 512 维也能达到接近峰值的性能。

## 训练参数

`SentenceTransformerTrainingArguments` 类允许你控制训练超参数。以下是用于 VDR 微调的配置：

```python
from sentence_transformers.sentence_transformer.training_args import SentenceTransformerTrainingArguments, BatchSamplers

run_name = "Qwen3-VL-Embedding-2B-vdr"
args = SentenceTransformerTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=False,
    bf16=True,
    batch_sampler=BatchSamplers.NO_DUPLICATES,
    
    eval_strategy="steps",
    eval_steps=0.1,
    save_strategy="steps",
    save_steps=0.1,
    save_total_limit=2,
    logging_steps=0.05,
    run_name=run_name,
)

```

关于（多模态）训练需要注意的几点：

*   `bf16=True`：bfloat16 通常优于 float16，因为它具有更好的数值稳定性。
*   `batch_sampler=BatchSamplers.NO_DUPLICATES`：当使用 `MultipleNegativesRankingLoss` 或其缓存变体时，确保批次中没有重复样本，以保证每个批次内负例都是真正不同的样本。
*   `per_device_train_batch_size=64`：对于一个 20 亿参数的 VLM 来说，这看起来可能很大，但 `CachedMultipleNegativesRankingLoss` 配合 `mini_batch_size=1` 通过梯度缓存处理了内存限制。
*   `eval_steps`、`save_steps` 和 `logging_steps`：将这些设置为一个分数（例如 0.1）意味着评估、保存和日志记录将在每个训练周期的 10% 时进行，这对于监控训练进度很有用。

## 评估器

为了在训练前、训练中和训练后跟踪检索性能，我使用 `InformationRetrievalEvaluator`。它计算标准的检索指标，如 NDCG@10、MAP 和 Recall@k：

```python
from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator



eval_queries = {qid: sample["query"] for qid, sample in enumerate(eval_dataset)}
eval_corpus = {did: sample["image"] for did, sample in enumerate(eval_dataset)}
num_eval = len(eval_dataset)



negative_columns = ["negative_0", "negative_1", "negative_2", "negative_3"]
for neg_idx, neg_col in enumerate(negative_columns):
    for did, sample in enumerate(eval_dataset):
        eval_corpus[num_eval * (neg_idx + 1) + did] = sample[neg_col]


eval_relevant_docs = {idx: [idx] for idx in range(len(eval_dataset))}
```

eval_evaluator = InformationRetrievalEvaluator(
    queries=eval_queries,
    corpus=eval_corpus,
    relevant_docs=eval_relevant_docs,
    batch_size=1,
    show_progress_bar=True,
    name="vdr-eval-hard",
)

```

评估器接收文本查询、一个图像语料库（包含困难负样本）以及一个文档与查询相关性的映射。请注意，该语料库混合了正样本和困难负样本的文档截图，这使得评估具有挑战性。使用`batch_size=1`可以防止在评估大型视觉语言模型时出现内存不足的问题。

## 训练器

`SentenceTransformerTrainer` 将所有组件整合在一起。以下是完整的训练脚本：

```python
from datasets import load_dataset

from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator
from sentence_transformers.sentence_transformer.losses import CachedMultipleNegativesRankingLoss, MatryoshkaLoss
from sentence_transformers.sentence_transformer.model_card import SentenceTransformerModelCardData
from sentence_transformers.sentence_transformer.trainer import SentenceTransformerTrainer
from sentence_transformers.sentence_transformer.training_args import (
    BatchSamplers,
    SentenceTransformerTrainingArguments,
)


model = SentenceTransformer(
    "Qwen/Qwen3-VL-Embedding-2B",
    model_card_data=SentenceTransformerModelCardData(
        language="en",
        license="apache-2.0",
        model_name="Qwen3-VL-Embedding-2B model trained on Visual Document Retrieval query-document screenshot pairs",
    ),
    model_kwargs={"attn_implementation": "flash_attention_2", "torch_dtype": "bfloat16"},
    
    processor_kwargs={"min_pixels": 28 * 28, "max_pixels": 600 * 600},
)



train_dataset = load_dataset("tomaarsen/llamaindex-vdr-en-train-preprocessed", "train", split="train")
train_dataset = train_dataset.select_columns(["query", "image", "negative_0"])
eval_dataset = load_dataset("tomaarsen/llamaindex-vdr-en-train-preprocessed", "eval", split="train")


loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=1)
loss = MatryoshkaLoss(model, loss, matryoshka_dims=[2048, 1536, 1024, 512, 256, 128, 64])


run_name = "Qwen3-VL-Embedding-2B-vdr"
args = SentenceTransformerTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=False,  
    bf16=True,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    
    eval_strategy="steps",
    eval_steps=0.1,
    save_strategy="steps",
    save_steps=0.1,
    save_total_limit=2,
    logging_steps=0.05,
    run_name=run_name,  
    
)


eval_queries = {qid: sample["query"] for qid, sample in enumerate(eval_dataset)}
eval_corpus = {did: sample["image"] for did, sample in enumerate(eval_dataset)}
num_eval = len(eval_dataset)
negative_columns = ["negative_0", "negative_1", "negative_2", "negative_3"]
for neg_idx, neg_col in enumerate(negative_columns):
    for did, sample in enumerate(eval_dataset):
        eval_corpus[num_eval * (neg_idx + 1) + did] = sample[neg_col]
eval_relevant_docs = {idx: [idx] for idx in range(len(eval_dataset))}

eval_evaluator = InformationRetrievalEvaluator(
    queries=eval_queries,
    corpus=eval_corpus,
    relevant_docs=eval_relevant_docs,
    batch_size=1,
    show_progress_bar=True,
    name="vdr-eval-hard",
)
eval_evaluator(model)


trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=eval_evaluator,
)
trainer.train()


eval_evaluator(model)
for dim in [2048, 1536, 1024, 512, 256, 128, 64]:
    dim_evaluator = InformationRetrievalEvaluator(
        queries=eval_queries,
        corpus=eval_corpus,
        relevant_docs=eval_relevant_docs,
        truncate_dim=dim,
        batch_size=1,
        show_progress_bar=True,
        name=f"vdr-eval-hard-{dim}d",
    )
    dim_evaluator(model)


model.save_pretrained(f"models/{run_name}/final")



model.push_to_hub("Qwen3-VL-Embedding-2B-vdr")

```

该训练脚本与纯文本训练脚本几乎完全相同。唯一的区别在于：

1.  模型加载：我们传递 `model_kwargs` 用于精度和注意力实现，传递 `processor_kwargs` 用于图像分辨率边界。
2.  损失函数：我们使用 `CachedMultipleNegativesRankingLoss` 并设置 `mini_batch_size=1`，以处理大型视觉语言模型而不耗尽内存。
3.  评估器：评估器使用语料库中的图像和文本作为查询，实现跨模态检索评估。

其他所有部分（训练器、训练参数、数据集加载）的工作方式与纯文本训练完全相同。

## 结果

### 模型大小 vs NDCG@10

仅训练 1 个周期后，微调后的 `tomaarsen/Qwen3-VL-Embedding-2B-vdr` 模型在评估集（300 个查询，1500 个语料库文档，余弦相似度）上实现了 **0.947** 的 NDCG@10。这比基础 `Qwen/Qwen3-VL-Embedding-2B` 模型的 0.888 有显著提升，并且优于所有现有的视觉文档检索模型：

微调后的 2B 模型甚至超越了 8B 的 Qwen3-VL-Embedding 模型，展示了任务特定微调的力量。即使有更大的通用模型可用，针对您自己的领域进行微调通常也是值得考虑的！

### Matryoshka 维度 vs NDCG@10

上面的比较使用了全尺寸的 2048 维嵌入。得益于 Matryoshka 训练，微调后的模型在截断到更少维度时也表现良好，让您可以在部署时权衡嵌入大小和检索质量：

![MRL dimensions vs NDCG@10](/images/posts/b93582503939.png)

微调模型的峰值在完整的 2048 维度（0.948），但一直到 512 维度（缩小 4 倍）都保持在峰值 0.3% 以内，即使在 64 维度（缩小 32 倍）也保留了超过 92% 的峰值。Matryoshka 训练将最重要的信息集中在靠前的维度中，因此适度的截断对性能影响很小。

1024 维和 2048 维之间的差距很小（0.946 vs. 0.948），因此我已将模型配置中的 `truncate_dim` 设置为 1024 并保存。这意味着 `SentenceTransformer("tomaarsen/Qwen3-VL-Embedding-2B-vdr")` 默认生成 1024 维嵌入，与完整的 2048 维相比，存储占用减少了一半。如果您想要不同的维度，可以在加载时传递 `truncate_dim=N` 来覆盖它。

## 训练多模态重排序模型

您也可以使用相同的训练基础设施来微调多模态交叉编码器（重排序）模型。关键区别在于使用 `CrossEncoderTrainer` 和交叉编码器特定的损失函数。本节提供一个简要概述；完整的、可运行的脚本（包含数据集准备和评估）请参阅完整的训练示例。

以下是一个基于涂鸦训练脚本的简化示例，该脚本训练一个重排序器来匹配图像和文本描述：

```python
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss
from sentence_transformers.cross_encoder.modules import LogitScore, Transformer
from sentence_transformers.cross_encoder.trainer import CrossEncoderTrainer
from sentence_transformers.cross_encoder.training_args import CrossEncoderTrainingArguments


transformer = Transformer(
    "Qwen/Qwen3.5-0.8B",
    transformer_task="any-to-any",
    model_kwargs={"torch_dtype": "bfloat16", "device_map": "auto", "attn_implementation": "flash_attention_2"},
    processing_kwargs={"chat_template": {"add_generation_prompt": True}},
)


transformer.processor.chat_template = transformer.processor.chat_template.replace(
    'message.role == "user"', 'message.role in ["user", "query", "document"]'
)


score_head = LogitScore(
    true_token_id=transformer.tokenizer.convert_tokens_to_ids("1"),
    false_token_id=transformer.tokenizer.convert_tokens_to_ids("0"),
)

model = CrossEncoder(
    modules=[transformer, score_head],
    num_labels=1,
    prompts={
        "image_to_text": "给定图像，判断文本是否与之匹配。如果匹配，请回复1；如果不匹配，请回复0。",
        "text_to_image": "给定文本，判断图像是否与之匹配。如果匹配，请回复1；如果不匹配，请回复0。",
    },
)


loss = BinaryCrossEntropyLoss(model)


trainer = CrossEncoderTrainer(
    model=model,
    args=args,
    train_dataset={"image_to_text": train_image_to_text, "text_to_image": train_text_to_image},
    eval_dataset={"image_to_text": eval_image_to_text, "text_to_image": eval_text_to_image},
    loss=loss,
    evaluator=[image_to_text_evaluator, text_to_image_evaluator],
)
trainer.train()

```

对于多模态重排序器，存在多种有效的架构选择，包括：

1.  任意到任意 + LogitScore：使用多模态大语言模型生成一个Token，然后计算"1"与"0"的对数几率。
2.  特征提取 + 池化 + 密集层：仅使用多模态基础模型，提取最后一个Token的隐藏状态，并通过一个密集层将其投影为一个分数，从而避免语言建模头部的计算。

这两种方法都在多模态交叉编码器训练示例中进行了演示。

上面链接的两个脚本将训练数据分成两个数据集，每个方向一个（图像到文本和文本到图像），并为每个方向提供特定任务的提示词，告诉模型如何在该方向上进行评分。然后，每个正样本对都会通过随机采样的负样本进行扩展，以便损失函数能看到匹配和不匹配的平衡混合。

## 附加资源

### 先前博客文章

-   使用Sentence Transformers进行多模态嵌入和重排序器模型：多模态推理
-   使用Sentence Transformers v3训练和微调嵌入模型：训练嵌入模型
-   使用Sentence Transformers v4训练和微调重排序器模型：训练重排序器模型
-   使用Sentence Transformers v5训练和微调稀疏嵌入模型：训练稀疏嵌入模型

### 训练示例

Sentence Transformers代码库包含多个多模态训练示例：

-   视觉文档检索：本博客文章中用于微调基于VLM的嵌入模型以进行文档截图检索的训练脚本
-   多模态重排序器（任意到任意）：使用LogitScore训练多模态重排序器
-   多模态重排序器（特征提取）：使用池化 + 密集层训练多模态重排序器

### 文档

此外，以下页面可能有助于了解更多关于使用Sentence Transformers进行训练的信息：

-   Sentence Transformer > 训练概述
-   Sentence Transformer > 损失函数概述
-   Cross Encoder > 训练概述
-   Cross Encoder > 损失函数概述
-   数据集概述
-   API参考

---

> 本文由AI自动翻译，原文链接：[Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-multimodal-sentence-transformers)
> 
> 翻译时间：2026-04-17 04:49
