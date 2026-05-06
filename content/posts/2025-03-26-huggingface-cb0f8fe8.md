---
title: 用Sentence Transformers微调重排序模型实战指南
title_original: Training and Finetuning Reranker Models with Sentence Transformers
date: '2025-03-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/train-reranker
author: ''
summary: 本文详细介绍了如何使用Sentence Transformers库微调重排序模型（交叉编码器），以在特定领域数据上超越通用模型。文章涵盖了训练的核心组件：数据集加载与格式、损失函数选择、训练参数设置、评估器使用以及训练器整合。作者通过实际案例展示了微调后的小型模型在GooAQ评估数据集上轻松击败13个常用公开模型，甚至超越体积大4倍的模型，强调了领域微调的巨大潜力。
categories:
- AI研究
tags:
- Sentence Transformers
- 重排序模型
- 交叉编码器
- 模型微调
- 检索增强生成
draft: false
translated_at: '2026-05-06T05:29:28.223433'
---

# 使用 Sentence Transformers 训练和微调重排序模型

Sentence Transformers 是一个 Python 库，用于使用和训练嵌入模型和重排序模型，适用于检索增强生成、语义搜索、语义文本相似度、释义挖掘等多种应用场景。在本文中，我将向您展示如何使用它来微调一个重排序模型（也称为交叉编码器），该模型在您的特定数据上能够超越所有现有选项。这种方法还可以从头开始训练极其强大的全新重排序模型。

微调重排序模型涉及多个组件：数据集、损失函数、训练参数、评估器以及训练器类本身。我将逐一介绍这些组件，并附上实际示例，说明如何使用它们来微调强大的重排序模型。

最后，在评估部分，我将向您展示，我随本文一同训练的小型微调模型 `tomaarsen/reranker-ModernBERT-base-gooaq-bce` 在我的评估数据集上轻松超越了 13 个最常用的公开重排序模型。它甚至击败了体积大 4 倍的模型。

使用更大的基础模型重复这一流程，可以得到 `tomaarsen/reranker-ModernBERT-large-gooaq-bce`，这是一个在我的数据上碾压所有现有通用重排序模型的重排序模型。

![GooAQ 上重排序模型的模型大小与 NDCG 对比](/images/posts/65857b6b3c08.png)

如果您对微调嵌入模型感兴趣，也请阅读我之前撰写的《使用 Sentence Transformers 训练和微调嵌入模型》一文。

- 什么是重排序模型？
- 为什么要微调？
- 训练组件
- 数据集
  - Hugging Face Hub 上的数据
  - 本地数据（CSV、JSON、Parquet、Arrow、SQL）
  - 需要预处理的本地数据
  - 数据集格式
  - 难负样本挖掘
- 损失函数
- 训练参数
- 评估器
  - 使用 STSb 的 CrossEncoderCorrelationEvaluator
  - 使用 GooAQ 挖掘负样本的 CrossEncoderRerankingEvaluator
- 训练器
  - 回调函数
  - 多数据集训练
- 训练技巧
- 评估
- 其他资源
  - 训练示例
  - 文档

## 什么是重排序模型？

重排序模型通常采用交叉编码器架构实现，旨在评估文本对之间的相关性（例如，查询与文档，或两个句子）。与 Sentence Transformers（也称为双编码器、嵌入模型）不同——后者将每个文本独立嵌入为向量并通过距离度量计算相似度——交叉编码器通过共享神经网络将成对文本一起处理，输出一个分数。通过让两个文本相互关注，交叉编码器模型可以超越嵌入模型。

然而，这种优势伴随着权衡：交叉编码器模型速度较慢，因为它们需要处理每一对可能的文本（例如，10 个查询与 500 个候选文档需要 5,000 次计算，而嵌入模型只需 510 次）。这使得它们在大规模初始检索中效率较低，但非常适合重排序：对由更快的 Sentence Transformers 模型首先识别出的 top-k 结果进行精炼。最强大的搜索系统通常采用这种两阶段的"检索并重排序"方法。

![嵌入模型与重排序模型对比](/images/posts/20f8c91bb9a6.png)

在本文中，我将交替使用"重排序模型"和"交叉编码器模型"这两个术语。

## 为什么要微调？

重排序模型通常面临一个具有挑战性的问题：

在这 k 个高度相关的文档中，哪一个最能回答查询？

通用重排序模型经过训练，能够在广泛领域和主题中较好地回答这一问题，但这限制了它们在您特定领域中的最大潜力。通过微调，模型可以学会专注于对您重要的领域和/或语言。

在本文的评估部分，我将展示，在您的领域上训练模型可以超越任何通用重排序模型，即使这些基线模型大得多。不要低估在您的领域上进行微调的力量！

## 训练组件

训练重排序模型涉及以下组件：

1. **数据集**：用于训练和/或评估的数据。
2. **损失函数**：衡量模型性能并指导优化过程的函数。
3. **训练参数**（可选）：影响训练性能、跟踪和调试的参数。
4. **评估器**（可选）：用于在训练前、训练中或训练后评估模型的类。
5. **训练器**：将所有训练组件整合在一起。

让我们仔细看看每个组件。

## 数据集

`CrossEncoderTrainer` 使用 `datasets.Dataset` 或 `datasets.DatasetDict` 实例进行训练和评估。您可以从 Hugging Face Datasets Hub 加载数据，或使用您偏好的任何格式（例如 CSV、JSON、Parquet、Arrow 或 SQL）的本地数据。

注意：许多可直接与 Sentence Transformers 配合使用的公开数据集已在 Hugging Face Hub 上标记了 `sentence-transformers`，因此您可以轻松地在 https://huggingface.co/datasets?other=sentence-transformers 上找到它们。请考虑浏览这些数据集，以找到可能对您的任务、领域或语言有用的现成数据集。

### Hugging Face Hub 上的数据

您可以使用 `load_dataset` 函数从 Hugging Face Hub 的数据集中加载数据。

```python
from datasets import load_dataset

train_dataset = load_dataset("sentence-transformers/natural-questions", split="train")

print(train_dataset)
"""
Dataset({
    features: ['query', 'answer'],
    num_rows: 100231
})
"""
```

某些数据集（如 `nthakur/swim-ir-monolingual`）具有多个子集，且数据格式不同。您需要同时指定数据集名称和子集名称，例如 `dataset = load_dataset("nthakur/swim-ir-monolingual", "de", split="train")`。

### 本地数据（CSV、JSON、Parquet、Arrow、SQL）

您也可以使用 `load_dataset` 加载特定文件格式的本地数据：

```python
from datasets import load_dataset

dataset = load_dataset("csv", data_files="my_file.csv")

dataset = load_dataset("json", data_files="my_file.json")
```

### 需要预处理的本地数据

如果您的本地数据需要预处理，可以使用 `datasets.Dataset.from_dict`。这允许您使用列表字典来初始化数据集：

```python
from datasets import Dataset

queries = []
documents = []

# ... 填充列表 ...

dataset = Dataset.from_dict({
    "query": queries,
    "document": documents,
})
```

字典中的每个键都会成为结果数据集中的一列。

### 数据集格式

确保您的数据集格式与损失函数匹配（或者选择一个与数据集格式和模型匹配的损失函数）非常重要。验证数据集格式和模型是否与损失函数兼容需要三个步骤：

1. 根据损失概览表，所有未命名为 "label"、"labels"、"score" 或 "scores" 的列都被视为输入。剩余列的数量必须与所选损失函数的有效输入数量匹配。
2. 如果根据损失概览表，您的损失函数需要标签，那么您的数据集必须有一个名为 "label"、"labels"、"score" 或 "scores" 的列。该列会自动被视为标签。
3. 模型输出标签的数量必须与损失概览表中损失函数所需的数量匹配。

例如，给定一个包含列 `["text1", "text2", "label"]` 的数据集，其中 "label" 列包含 0 到 1 之间的浮点相似度分数，且模型输出 1 个标签，我们可以将其与 `BinaryCrossEntropyLoss` 一起使用，因为：

1. 数据集必须包含一个“label”列，这是该损失函数所要求的。
2. 数据集必须有2个非标签列，正好符合该损失函数所需的数量。
3. 模型必须有1个输出标签，正好符合该损失函数的要求。

如果数据集的列顺序不正确，请务必使用`Dataset.select_columns`重新排列列顺序。例如，如果数据集的列是["good_answer", "bad_answer", "question"]，那么从技术上讲，该数据集可以用于需要（anchor, positive, negative）三元组的损失函数，但`good_answer`列会被当作anchor，`bad_answer`列会被当作positive，而`question`列会被当作negative。

此外，如果数据集中包含多余的列（例如sample_id、metadata、source、type），应使用`Dataset.remove_columns`将其移除，否则它们会被当作输入。你也可以使用`Dataset.select_columns`仅保留所需的列。

### 困难负样本挖掘

训练重排序器模型是否成功，通常取决于负样本的质量，即查询-负样本得分应较低的那些段落。负样本可分为两类：

- 软负样本：完全不相关的段落。也称为简单负样本。
- 困难负样本：看似可能与查询相关，但实际上并不相关的段落。

一个简洁的例子是：

- 查询：苹果公司是在哪里成立的？
- 软负样本：Cache River Bridge是一座帕克式 pony truss桥，横跨阿肯色州Walnut Ridge和Paragould之间的Cache River。
- 困难负样本：富士苹果是20世纪30年代末培育的一个苹果品种，于1962年推向市场。

最强大的CrossEncoder模型通常训练用于识别困难负样本，因此能够“挖掘”困难负样本进行训练非常有价值。Sentence Transformers支持一个强大的`mine_hard_negatives`函数，给定一个查询-答案对的数据集，该函数可以提供帮助：

```python
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import mine_hard_negatives


train_dataset = load_dataset("sentence-transformers/gooaq", split="train").select(range(100_000))
print(train_dataset)


embedding_model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")
hard_train_dataset = mine_hard_negatives(
    train_dataset,
    embedding_model,
    num_negatives=5,  
    range_min=10,  
    range_max=100,  
    max_score=0.8,  
    margin=0.1,  
    sampling_strategy="top",  
    batch_size=4096,  
    output_format="labeled-pair",  
    use_faiss=True,  
)
print(hard_train_dataset)
print(hard_train_dataset[1])

```

```
Dataset({
    features: ['question', 'answer'],
    num_rows: 100000
})

Batches: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 22/22 [00:01<00:00, 13.74it/s]
Batches: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 25/25 [00:00<00:00, 36.49it/s]
Querying FAISS index: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:19<00:00,  2.80s/it]
Metric       Positive       Negative     Difference
Count         100,000        436,925
Mean           0.5882         0.4040         0.2157
Median         0.5989         0.4024         0.1836
Std            0.1425         0.0905         0.1013
Min           -0.0514         0.1405         0.1014
25%            0.4993         0.3377         0.1352
50%            0.5989         0.4024         0.1836
75%            0.6888         0.4681         0.2699
Max            0.9748         0.7486         0.7545
Skipped 2420871 potential negatives (23.97%) due to the margin of 0.1.
Skipped 43 potential negatives (0.00%) due to the maximum score of 0.8.
Could not find enough negatives for 63075 samples (12.62%). Consider adjusting the range_max, range_min, margin and max_score parameters if you'd like to find more valid negatives.
Dataset({
    features: ['question', 'answer', 'label'],
    num_rows: 536925
})

{
    'question': 'how to transfer bookmarks from one laptop to another?',
    'answer': 'Using an External Drive Just about any external drive, including a USB thumb drive, or an SD card can be used to transfer your files from one laptop to another. Connect the drive to your old laptop; drag your files to the drive, then disconnect it and transfer the drive contents onto your new laptop.',
    'label': 0
}

```

- sentence-transformers/gooaq
- sentence-transformers/static-retrieval-mrl-en-v1

## 损失函数

损失函数有助于评估模型在一组数据上的性能，并指导训练过程。适合你任务的损失函数取决于你拥有的数据以及你想要实现的目标。你可以在损失函数概览中找到所有可用损失函数的完整列表。

大多数损失函数都很容易设置——你只需要提供正在训练的CrossEncoder模型：

```python
from datasets import load_dataset
from sentence_transformers import CrossEncoder
from sentence_transformers.cross_encoder.losses import CachedMultipleNegativesRankingLoss


model = CrossEncoder("xlm-roberta-base", num_labels=1) 



loss = CachedMultipleNegativesRankingLoss(model)


train_dataset = load_dataset("sentence-transformers/gooaq", split="train")

...

```

## 训练参数

你可以使用`CrossEncoderTrainingArguments`类自定义训练过程。这个类允许你调整可能影响训练速度的参数，并帮助你了解训练过程中发生的事情。

关于最有用的训练参数的更多信息，请查看Cross Encoder > 训练概览 > 训练参数。为了充分利用你的训练，值得一读。

以下是如何设置`CrossEncoderTrainingArguments`的示例：

```python
from sentence_transformers.cross_encoder import CrossEncoderTrainingArguments

args = CrossEncoderTrainingArguments(
    
    output_dir="models/reranker-MiniLM-msmarco-v1",
    
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=True,  
    bf16=False,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
    logging_steps=100,
    run_name="reranker-MiniLM-msmarco-v1",  
)

```

## 评估器

为了在训练期间跟踪模型的性能，你可以向`CrossEncoderTrainer`传递一个`eval_dataset`。然而，你可能希望获得比仅仅评估损失更详细的指标。这时，评估器可以帮助你在训练的不同阶段使用特定指标评估模型的性能。你可以根据需要使用评估数据集、评估器、两者都用，或者两者都不用。评估策略和频率由训练参数中的`eval_strategy`和`eval_steps`控制。

Sentence Transformers包含以下内置评估器：

你也可以使用`SequentialEvaluator`将多个评估器合并为一个，然后将其传递给`CrossEncoderTrainer`。你也可以直接向训练器传递一个评估器列表。

有时，你手头没有所需的评估数据来自己准备这些评估器，但你仍然希望跟踪模型在一些常见基准测试上的表现。在这种情况下，你可以使用来自Hugging Face的数据与这些评估器一起使用。

### 使用STSb的CrossEncoderCorrelationEvaluator

STS基准测试（简称STSb）是一个常用的基准测试数据集，用于衡量模型对短文本（如“A man is feeding a mouse to a snake.”）语义文本相似性的理解能力。

请随意浏览Hugging Face上的`sentence-transformers/stsb`数据集。

```python
from datasets import load_dataset
from sentence_transformers import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CrossEncoderCorrelationEvaluator


model = CrossEncoder("cross-encoder/stsb-TinyBERT-L4")


eval_dataset = load_dataset("sentence-transformers/stsb", split="validation")
pairs = list(zip(eval_dataset["sentence1"], eval_dataset["sentence2"]))


dev_evaluator = CrossEncoderCorrelationEvaluator(
    sentence_pairs=pairs,
    scores=eval_dataset["score"],
    name="sts_dev",
)





```

### 使用GooAQ挖掘负样本的CrossEncoderRerankingEvaluator

为CrossEncoderRerankingEvaluator准备数据可能比较困难，因为除了查询-正样本数据外，你还需要负样本。

`mine_hard_negatives`函数有一个方便的`include_positives`参数，可以设置为`True`来同时挖掘正文本。当作为`documents`（必须1. 已排序且2. 包含正样本）提供给CrossEncoderRerankingEvaluator时，评估器不仅会评估CrossEncoder的重排序性能，还会评估用于挖掘的嵌入模型的原始排序结果。

例如：

```
CrossEncoderRerankingEvaluator: Evaluating the model on the gooaq-dev dataset:
Queries:  1000     Positives: Min 1.0, Mean 1.0, Max 1.0   Negatives: Min 49.0, Mean 49.1, Max 50.0
          Base  -> Reranked
MAP:      53.28 -> 67.28
MRR@10:   52.40 -> 66.65
NDCG@10:  59.12 -> 71.35

```

请注意，默认情况下，如果你使用带有`documents`的CrossEncoderRerankingEvaluator，评估器会使用**所有**正样本进行重排序，即使它们不在documents中。这对于从评估器中获得更强的信号很有用，但会带来略微不切实际的性能表现。毕竟，最大性能现在是100，而通常情况下它受限于第一阶段检索器是否实际检索到了正样本。

你可以通过在初始化CrossEncoderRerankingEvaluator时设置`always_rerank_positives=False`来启用更符合实际的行为。使用这种更符合实际的两阶段性能重复相同的脚本会得到以下结果：

```
CrossEncoderRerankingEvaluator: Evaluating the model on the gooaq-dev dataset:
Queries:  1000     Positives: Min 1.0, Mean 1.0, Max 1.0   Negatives: Min 49.0, Mean 49.1, Max 50.0
          Base  -> Reranked
MAP:      53.28 -> 66.12
MRR@10:   52.40 -> 65.61
NDCG@10:  59.12 -> 70.10

```

```python
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CrossEncoderRerankingEvaluator
from sentence_transformers.util import mine_hard_negatives


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")


full_dataset = load_dataset("sentence-transformers/gooaq", split=f"train").select(range(100_000))
dataset_dict = full_dataset.train_test_split(test_size=1_000, seed=12)
train_dataset = dataset_dict["train"]
eval_dataset = dataset_dict["test"]
print(eval_dataset)
"""
Dataset({
    features: ['question', 'answer'],
    num_rows: 1000
})
"""


embedding_model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")
hard_eval_dataset = mine_hard_negatives(
    eval_dataset,
    embedding_model,
    corpus=full_dataset["answer"],  
    num_negatives=50,  
    batch_size=4096,  
    output_format="n-tuple",  
    include_positives=True,  
    use_faiss=True,  
)
print(hard_eval_dataset)
"""
Dataset({
    features: ['question', 'answer', 'negative_1', 'negative_2', 'negative_3', 'negative_4', 'negative_5', 'negative_6', 'negative_7', 'negative_8', 'negative_9', 'negative_10', 'negative_11', 'negative_12', 'negative_13', 'negative_14', 'negative_15', 'negative_16', 'negative_17', 'negative_18', 'negative_19', 'negative_20', 'negative_21', 'negative_22', 'negative_23', 'negative_24', 'negative_25', 'negative_26', 'negative_27', 'negative_28', 'negative_29', 'negative_30', 'negative_31', 'negative_32', 'negative_33', 'negative_34', 'negative_35', 'negative_36', 'negative_37', 'negative_38', 'negative_39', 'negative_40', 'negative_41', 'negative_42', 'negative_43', 'negative_44', 'negative_45', 'negative_46', 'negative_47', 'negative_48', 'negative_49', 'negative_50'],
    num_rows: 1000
})
"""

reranking_evaluator = CrossEncoderRerankingEvaluator(
    samples=[
        {
            "query": sample["question"],
            "positive": [sample["answer"]],
            "documents": [sample[column_name] for column_name in hard_eval_dataset.column_names[2:]],
        }
        for sample in hard_eval_dataset
    ],
    batch_size=32,
    name="gooaq-dev",
)

results = reranking_evaluator(model)
"""
CrossEncoderRerankingEvaluator: Evaluating the model on the gooaq-dev dataset:
Queries:  1000     Positives: Min 1.0, Mean 1.0, Max 1.0   Negatives: Min 49.0, Mean 49.1, Max 50.0
          Base  -> Reranked
MAP:      53.28 -> 67.28
MRR@10:   52.40 -> 66.65
NDCG@10:  59.12 -> 71.35
"""


```

## 训练器

CrossEncoderTrainer是整合所有先前组件的地方。我们只需要指定训练器及其模型、训练参数（可选）、训练数据集、评估数据集（可选）、损失函数、评估器（可选），就可以开始训练了。让我们看一个整合了所有这些组件的脚本：

```python
import logging
import traceback

import torch
from datasets import load_dataset

from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import (
    CrossEncoder,
    CrossEncoderModelCardData,
    CrossEncoderTrainer,
    CrossEncoderTrainingArguments,
)
from sentence_transformers.cross_encoder.evaluation import (
    CrossEncoderNanoBEIREvaluator,
    CrossEncoderRerankingEvaluator,
)
from sentence_transformers.cross_encoder.losses.BinaryCrossEntropyLoss import BinaryCrossEntropyLoss
from sentence_transformers.evaluation.SequentialEvaluator import SequentialEvaluator
from sentence_transformers.util import mine_hard_negatives


logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


def main():
    model_name = "answerdotai/ModernBERT-base"

    train_batch_size = 16
    num_epochs = 1
    num_hard_negatives = 5  

    
    model = CrossEncoder(
        model_name,
        model_card_data=CrossEncoderModelCardData(
            language="en",
            license="apache-2.0",
            model_name="ModernBERT-base trained on GooAQ",
        ),
    )
    print("Model max length:", model.max_length)
    print("Model num labels:", model.num_labels)

    
    logging.info("Read the gooaq training dataset")
    full_dataset = load_dataset("sentence-transformers/gooaq", split="train").select(range(100_000))
    dataset_dict = full_dataset.train_test_split(test_size=1_000, seed=12)
    train_dataset = dataset_dict["train"]
    eval_dataset = dataset_dict["test"]
    logging.info(train_dataset)
    logging.info(eval_dataset)

    
    embedding_model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")
    hard_train_dataset = mine_hard_negatives(
        train_dataset,
        embedding_model,
        num_negatives=num_hard_negatives,  
        margin=0,  
        range_min=0,  
        range_max=100,  
        sampling_strategy="top",  
        batch_size=4096,  
        output_format="labeled-pair",  
        use_faiss=True,
    )
    logging.info(hard_train_dataset)

    
    
    
    

    
    
    loss = BinaryCrossEntropyLoss(model=model, pos_weight=torch.tensor(num_hard_negatives))

    
    nano_beir_evaluator = CrossEncoderNanoBEIREvaluator(
        dataset_names=["msmarco", "nfcorpus", "nq"],
        batch_size=train_batch_size,
    )
```

```python
hard_eval_dataset = mine_hard_negatives(
        eval_dataset,
        embedding_model,
        corpus=full_dataset["answer"],  
        num_negatives=30,  
        batch_size=4096,
        include_positives=True,
        output_format="n-tuple",
        use_faiss=True,
    )
    logging.info(hard_eval_dataset)
    reranking_evaluator = CrossEncoderRerankingEvaluator(
        samples=[
            {
                "query": sample["question"],
                "positive": [sample["answer"]],
                "documents": [sample[column_name] for column_name in hard_eval_dataset.column_names[2:]],
            }
            for sample in hard_eval_dataset
        ],
        batch_size=train_batch_size,
        name="gooaq-dev",
        always_rerank_positives=False,
    )

    
    evaluator = SequentialEvaluator([reranking_evaluator, nano_beir_evaluator])
    evaluator(model)

    
    short_model_name = model_name if "/" not in model_name else model_name.split("/")[-1]
    run_name = f"reranker-{short_model_name}-gooaq-bce"
    args = CrossEncoderTrainingArguments(
        
        output_dir=f"models/{run_name}",
        
        num_train_epochs=num_epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=train_batch_size,
        learning_rate=2e-5,
        warmup_ratio=0.1,
        fp16=False,  
        bf16=True,  
        dataloader_num_workers=4,
        load_best_model_at_end=True,
        metric_for_best_model="eval_gooaq-dev_ndcg@10",
        
        eval_strategy="steps",
        eval_steps=4000,
        save_strategy="steps",
        save_steps=4000,
        save_total_limit=2,
        logging_steps=1000,
        logging_first_step=True,
        run_name=run_name,  
        seed=12,
    )

    
    trainer = CrossEncoderTrainer(
        model=model,
        args=args,
        train_dataset=hard_train_dataset,
        loss=loss,
        evaluator=evaluator,
    )
    trainer.train()

    
    evaluator(model)

    
    final_output_dir = f"models/{run_name}/final"
    model.save_pretrained(final_output_dir)

    
    
    try:
        model.push_to_hub(run_name)
    except Exception:
        logging.error(
            f"上传模型到Hugging Face Hub时出错：\n{traceback.format_exc()}如需手动上传，可运行"
            f"`huggingface-cli login`，然后加载模型`model = CrossEncoder({final_output_dir!r})`"
            f"并保存`model.push_to_hub('{run_name}')`。"
        )


if __name__ == "__main__":
    main()
```

在这个示例中，我从`answerdotai/ModernBERT-base`进行微调，这是一个基础模型，还不是交叉编码器模型。这通常需要比微调现有重排序模型（如`Alibaba-NLP/gte-multilingual-reranker-base`）更多的训练数据。我使用了来自GooAQ数据集的9.9万个查询-答案对，然后使用`sentence-transformers/static-retrieval-mrl-en-v1`嵌入模型挖掘困难负样本。这产生了57.8万个标注对：9.9万个正样本对（即标签=1）和47.9万个负样本对（即标签=0）。

我使用了`BinaryCrossEntropyLoss`，它非常适合这些标注对。我还设置了两种评估形式：`CrossEncoderNanoBEIREvaluator`用于评估NanoBEIR基准测试，以及`CrossEncoderRerankingEvaluator`用于评估对前述静态嵌入模型的前30个结果进行重排序的性能。之后，我定义了一套相当标准的超参数，包括学习率、预热比例、bf16、结束时加载最佳模型以及一些调试参数。最后，我运行训练器，进行训练后评估，并将模型保存在本地和Hugging Face Hub上。

运行此脚本后，`tomaarsen/reranker-ModernBERT-base-gooaq-bce`模型被自动上传。请参阅即将发布的"评估"部分，其中包含证据表明该模型优于13种常用的开源替代方案，包括更大的模型。我还以`answerdotai/ModernBERT-large`为基础模型运行了该模型，生成了`tomaarsen/reranker-ModernBERT-large-gooaq-bce`。

评估结果在保存模型时会自动存储在生成的模型卡片中，同时还包括基础模型、语言、许可证、评估结果、训练和评估数据集信息、超参数、训练日志等。无需额外操作，您上传的模型应包含潜在用户判断模型是否适合他们所需的所有信息。

### 回调函数

CrossEncoder训练器支持各种`transformers.TrainerCallback`子类，包括：

- `WandbCallback`：如果安装了`wandb`，用于将训练指标记录到W&B
- `TensorBoardCallback`：如果可以访问`tensorboard`，用于将训练指标记录到TensorBoard
- `CodeCarbonCallback`：如果安装了`codecarbon`，用于跟踪训练期间的碳排放

只要安装了所需的依赖项，这些回调函数会自动使用，无需您指定任何内容。

有关这些回调函数以及如何创建自己的回调函数的更多信息，请参阅Transformers回调函数文档。

### 多数据集训练

通常，性能最佳的通用模型会在多个数据集上同时训练。然而，由于每个数据集的格式不同，这种方法可能具有挑战性。幸运的是，`CrossEncoderTrainer`允许您在多个数据集上训练，而无需统一格式。此外，它还提供了对每个数据集应用不同损失函数的灵活性。以下是同时使用多个数据集进行训练的步骤：

- 使用`datasets.Dataset`实例的字典（或`datasets.DatasetDict`）作为`train_dataset`（以及可选的`eval_dataset`）。
- （可选）使用将数据集名称映射到损失函数的损失函数字典。仅当您希望对不同数据集使用不同损失函数时才需要。

每个训练/评估批次将仅包含来自其中一个数据集的样本。从多个数据集中采样批次的顺序由`MultiDatasetBatchSamplers`枚举定义，该枚举可以通过`multi_dataset_batch_sampler`传递给`CrossEncoderTrainingArguments`。有效选项包括：

- `MultiDatasetBatchSamplers.ROUND_ROBIN`：从每个数据集进行轮询采样，直到其中一个数据集耗尽。使用此策略，可能不会使用每个数据集中的所有样本，但每个数据集的采样频率相同。
- `MultiDatasetBatchSamplers.PROPORTIONAL`（默认）：根据数据集的大小按比例采样。使用此策略，将使用每个数据集中的所有样本，并且较大的数据集被更频繁地采样。

## 训练技巧

交叉编码器模型有其独特的特性，因此这里有一些技巧可以帮助您：

1. 交叉编码器模型过拟合相当快，因此建议使用像`CrossEncoderNanoBEIREvaluator`或`CrossEncoderRerankingEvaluator`这样的评估器，结合`load_best_model_at_end`和`metric_for_best_model`训练参数，在训练后加载具有最佳评估性能的模型。
2. 交叉编码器对强困难负样本（`mine_hard_negatives`）特别敏感。它们教会模型非常严格，例如在区分回答问题的段落和与问题相关的段落时非常有用。请注意，如果只使用困难负样本，您的模型在较简单的任务上可能会意外表现更差。这可能意味着对来自第一阶段检索系统（例如使用`SentenceTransformer`模型）的前200个结果进行重排序，实际上可能比仅对前100个结果进行重排序得到更差的前10个结果。将随机负样本与困难负样本一起训练可以缓解这个问题。
3. 不要低估`BinaryCrossEntropyLoss`，尽管它比学习排序（`LambdaLoss`、`ListNetLoss`）或批次内负样本（`CachedMultipleNegativesRankingLoss`、`MultipleNegativesRankingLoss`）损失更简单，但它仍然是一个非常强大的选择，并且其数据易于准备，特别是使用`mine_hard_negatives`时。

交叉编码器模型容易过拟合，因此建议使用`CrossEncoderNanoBEIREvaluator`或`CrossEncoderRerankingEvaluator`等评估器，并结合`load_best_model_at_end`和`metric_for_best_model`训练参数，在训练后加载评估性能最佳的模型。

交叉编码器对强难负样本（`mine_hard_negatives`）特别敏感。它们能训练模型变得非常严格，例如在区分回答问题的段落与仅与问题相关的段落时非常有用。

1. 请注意，如果仅使用难负样本，模型在简单任务上的表现可能会意外变差。这意味着对第一阶段检索系统（例如使用`SentenceTransformer`模型）返回的前200个结果进行重排序，实际得到的前10个结果可能比仅重排序前100个结果更差。在训练中同时使用随机负样本和难负样本可以缓解这一问题。

不要低估`BinaryCrossEntropyLoss`，尽管它比学习排序（`LambdaLoss`、`ListNetLoss`）或批次内负样本（`CachedMultipleNegativesRankingLoss`、`MultipleNegativesRankingLoss`）损失函数更简单，但它仍然是一个非常强大的选择，并且其数据易于准备，尤其是使用`mine_hard_negatives`时。

## 评估

我在GooAQ开发集上，使用重排序评估器中的`always_rerank_positives=False`和`always_rerank_positives=True`两种设置，将训练部分的模型与多个基线进行了重排序评估。这两种设置分别代表实际场景（仅重排序检索器找到的结果）和评估场景（重排序所有正样本，即使检索器未找到）。

提醒一下，我使用了极其高效的`sentence-transformers/static-retrieval-mrl-en-v1`静态嵌入模型来检索前30个结果进行重排序。

以下是评估脚本：

```python
import logging
from pprint import pprint
from datasets import load_dataset

from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CrossEncoderRerankingEvaluator


logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


def main():
    model_name = "tomaarsen/reranker-ModernBERT-base-gooaq-bce"
    eval_batch_size = 64

    
    model = CrossEncoder(model_name)

    
    logging.info("Read the gooaq reranking dataset")
    hard_eval_dataset = load_dataset("tomaarsen/gooaq-reranker-blogpost-datasets", "rerank", split="eval")

    
    
    
    samples = [
        {
            "query": sample["question"],
            "positive": [sample["answer"]],
            "documents": [sample[column_name] for column_name in hard_eval_dataset.column_names[2:]],
        }
        for sample in hard_eval_dataset
    ]
    reranking_evaluator = CrossEncoderRerankingEvaluator(
        samples=samples,
        batch_size=eval_batch_size,
        name="gooaq-dev-realistic",
        always_rerank_positives=False,
    )
    realistic_results = reranking_evaluator(model)
    pprint(realistic_results)

    reranking_evaluator = CrossEncoderRerankingEvaluator(
        samples=samples,
        batch_size=eval_batch_size,
        name="gooaq-dev-evaluation",
        always_rerank_positives=True,
    )
    evaluation_results = reranking_evaluator(model)
    pprint(evaluation_results)


if __name__ == "__main__":
    main()

```

该脚本使用了我的`tomaarsen/gooaq-reranker-blogpost-datasets`数据集中的`rerank`子集。该数据集包含：

- `pair`子集，`train`划分：直接从GooAQ中提取的99k训练样本。这些样本不直接用于训练，而是用于准备`hard-labeled-pair`子集，该子集用于训练。
- `pair`子集，`eval`划分：直接从GooAQ中提取的1k训练样本，与之前的99k样本无重叠。这些样本不直接用于评估，而是用于准备`rerank`子集，该子集用于评估。
- `hard-labeled-pair`子集，`train`划分：578k个标记对，用于训练，通过使用`sentence-transformers/static-retrieval-mrl-en-v1`对`pair`子集和`train`划分中的99k样本进行挖掘得到。该数据集用于训练。
- `rerank`子集，`eval`划分：1k个样本，包含问题、答案以及由`sentence-transformers/static-retrieval-mrl-en-v1`使用我的GooAQ子集中全部100k训练和评估答案检索到的恰好30个文档。该排序结果已具有59.12的NDCG@10。

仅使用gooaq数据集中300万训练对中的99k对，并在我的RTX 3090上训练30分钟，我的小型150M参数模型`tomaarsen/reranker-ModernBERT-base-gooaq-bce`就轻松超越了所有小于1B参数的通用重排序器。更大的`tomaarsen/reranker-ModernBERT-large-gooaq-bce`训练时间不到一小时，在实际场景中以79.42的NDCG@10独占鳌头。GooAQ训练和评估数据集与这些基线的训练目标非常吻合，因此在更细分领域进行训练时，差距应该会更大。

请注意，这并不意味着`tomaarsen/reranker-ModernBERT-large-gooaq-bce`在所有领域都是最强的模型：它只是在我们领域中最强。这完全没问题，因为我们只需要这个重排序器在我们的数据上表现良好。

不要低估在您的领域微调重排序模型的力量。通过微调（小型）重排序器，您可以同时提升搜索性能和搜索栈的延迟！

## 附加资源

### 训练示例

以下页面包含带有解释的训练示例以及训练脚本代码的链接。您可以使用它们来熟悉重排序器的训练流程：

- 语义文本相似度
- 自然语言推理
- Quora重复问题
- MS MARCO
- 重排序器
- 模型蒸馏

### 文档

如需进一步学习，您可能还想探索Sentence Transformers的以下资源：

- 安装
- 快速入门
- 迁移指南
- 使用方法
- 预训练模型
- 训练概述（本篇博文是训练概述文档的精华版）
- 损失函数概述
- API参考

以下是一个可能让您感兴趣的高级页面：

- 分布式训练

### 配套博文

关于训练其他类型的Sentence Transformers模型，或与重排序器配合使用的技术：

- 使用Sentence Transformers训练和微调嵌入模型：驱动检索-重排序第一阶段的双编码器（嵌入）模型的等效指南。
- 使用Sentence Transformers训练和微调稀疏嵌入模型：训练SPLADE和其他稀疏编码器，它们与重排序器配合良好。
- 使用Sentence Transformers的多模态嵌入与重排序模型：在推理时使用多模态重排序器。
- 使用Sentence Transformers训练和微调多模态嵌入与重排序模型：多模态模型的等效指南，包括重排序器训练示例。
- 🪆 Matryoshka嵌入模型介绍：可变大小嵌入，与重排序器配合用于初筛+重排序。
- 使用Sentence Transformers训练速度提升400倍的静态嵌入模型：适合CPU的第一阶段检索器，为您的重排序器提供输入。
- 二进制和标量嵌入量化，实现显著更快、更便宜的检索：压缩后的第一阶段嵌入，由重排序器重新评分。

---

> 本文由AI自动翻译，原文链接：[Training and Finetuning Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-reranker)
> 
> 翻译时间：2026-05-06 05:29
