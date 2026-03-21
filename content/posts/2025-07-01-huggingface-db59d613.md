---
title: 使用Sentence Transformers v5训练和微调稀疏嵌入模型
title_original: Training and Finetuning Sparse Embedding Models with Sentence Transformers
  v5
date: '2025-07-01'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/train-sparse-encoder
author: ''
summary: 本文介绍了如何使用Sentence Transformers v5库训练和微调稀疏嵌入模型。稀疏嵌入模型能生成高维、可解释的向量表示，在混合搜索和重排序等场景中表现优异。文章详细阐述了训练所需的组件，包括模型架构、数据集、损失函数和评估器，并提供了从Hugging
  Face Hub获取预训练模型以及进行本地微调的实用指南。
categories:
- AI基础设施
tags:
- Sentence Transformers
- 稀疏嵌入
- 模型微调
- 语义搜索
- SPLADE
draft: false
translated_at: '2026-03-21T04:34:32.772795'
---

# 使用 Sentence Transformers v5 训练和微调稀疏嵌入模型

Sentence Transformers 是一个 Python 库，用于使用和训练嵌入及重排序模型，适用于多种应用场景，如检索增强生成、语义搜索、语义文本相似性、释义挖掘等。最近的几个主要版本在训练方面引入了重大改进：

- v3.0：（改进的）Sentence Transformer（密集嵌入）模型训练
- v4.0：（改进的）交叉编码器（重排序）模型训练
- v5.0：（新增的）稀疏嵌入模型训练

在这篇博客文章中，我将向你展示如何使用它来微调一个稀疏编码器/嵌入模型，并解释为什么你可能需要这样做。这将得到一个廉价的模型 `sparse-encoder/example-inference-free-splade-distilbert-base-uncased-nq`，该模型在混合搜索或检索后重排序的场景中表现尤为出色。

微调稀疏嵌入模型涉及几个组件：模型、数据集、损失函数、训练参数、评估器和训练器类。我将逐一审视这些组件，并辅以实际示例，说明如何利用它们来微调强大的稀疏嵌入模型。

除了训练你自己的模型，你还可以从 Hugging Face Hub 上选择多种预训练的稀疏编码器。为了帮助在这个不断增长的空间中导航，我们策划了一个 **SPLADE 模型集合**，突出展示了一些最相关的模型。我们在文档的 **预训练模型** 部分列出了最突出的模型及其基准测试结果。

-   什么是稀疏嵌入模型？
    -   查询和文档扩展
    -   为什么使用稀疏嵌入模型？
-   为什么进行微调？
-   训练组件
    -   模型
        -   Splade
        -   Inference-free Splade
        -   对比稀疏表示
        -   架构选择指南
    -   数据集
        -   Hugging Face Hub 上的数据
        -   本地数据
        -   需要预处理的本地数据
        -   数据集格式
    -   损失函数
    -   训练参数
    -   评估器
        -   SparseNanoBEIREvaluator
        -   使用 STSb 的 SparseEmbeddingSimilarityEvaluator
        -   使用 AllNLI 的 SparseTripletEvaluator
    -   训练器
        -   回调
        -   多数据集训练
-   评估
-   训练技巧
-   向量数据库集成
-   附加资源
    -   训练示例
    -   文档

## 什么是稀疏嵌入模型？

广义的"嵌入模型"指的是将某些输入（通常是文本）转换为向量表示（嵌入）的模型，这种表示能捕捉输入的语义含义。与原始输入不同，你可以对这些嵌入执行数学运算，从而得到可用于各种任务（如搜索、聚类或分类）的相似性分数。

对于密集嵌入模型（即常见类型），嵌入通常是低维向量（例如 384、768 或 1024 维），其中大多数值非零。而稀疏嵌入模型则产生高维向量（例如 30,000+ 维），其中大多数值为零。通常，稀疏嵌入中的每个活跃维度（即具有非零值的维度）对应于模型词汇表中的一个特定 Token，这使得它具有可解释性。

让我们以最先进的稀疏嵌入模型 `naver/splade-v3` 为例来看看：

```python
from sentence_transformers import SparseEncoder


model = SparseEncoder("naver/splade-v3")


sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]
embeddings = model.encode(sentences)
print(embeddings.shape)



similarities = model.similarity(embeddings, embeddings)
print(similarities)





decoded = model.decode(embeddings, top_k=10)
for decoded, sentence in zip(decoded, sentences):
    print(f"Sentence: {sentence}")
    print(f"Decoded: {decoded}")
    print()

```

```
Sentence: The weather is lovely today.
Decoded: [('weather', 2.754288673400879), ('today', 2.610959529876709), ('lovely', 2.431990623474121), ('currently', 1.5520408153533936), ('beautiful', 1.5046082735061646), ('cool', 1.4664798974990845), ('pretty', 0.8986214995384216), ('yesterday', 0.8603134155273438), ('nice', 0.8322536945343018), ('summer', 0.7702118158340454)]

Sentence: It's so sunny outside!
Decoded: [('outside', 2.6939032077789307), ('sunny', 2.535827398300171), ('so', 2.0600898265838623), ('out', 1.5397940874099731), ('weather', 1.1198079586029053), ('very', 0.9873268604278564), ('cool', 0.9406591057777405), ('it', 0.9026399254798889), ('summer', 0.684999406337738), ('sun', 0.6520509123802185)]

Sentence: He drove to the stadium.
Decoded: [('stadium', 2.7872302532196045), ('drove', 1.8208855390548706), ('driving', 1.6665740013122559), ('drive', 1.5565159320831299), ('he', 1.4721972942352295), ('stadiums', 1.449463129043579), ('to', 1.0441515445709229), ('car', 0.7002660632133484), ('visit', 0.5118278861045837), ('football', 0.502326250076294)]

```

在这个例子中，嵌入是 30,522 维的向量，其中每个维度对应于模型词汇表中的一个 Token。`decode` 方法返回了嵌入中值最高的前 10 个 Token，使我们能够解释哪些 Token 对嵌入的贡献最大。

我们甚至可以确定嵌入之间的交集或重叠，这对于判断两个文本为何被认为相似或不相似非常有用：

```python

intersection_embedding = model.intersection(embeddings[0], embeddings[1])
decoded_intersection = model.decode(intersection_embedding)
print(decoded_intersection)

```

```
Decoded: [('weather', 3.0842742919921875), ('cool', 1.379457712173462), ('summer', 0.5275946259498596), ('comfort', 0.3239051103591919), ('sally', 0.22571465373039246), ('julian', 0.14787325263023376), ('nature', 0.08582140505313873), ('beauty', 0.0588383711874485), ('mood', 0.018594780936837196), ('nathan', 0.000752730411477387)]

```

### 查询和文档扩展

神经稀疏嵌入模型的一个关键组成部分是**查询/文档扩展**。与 BM25 等仅匹配确切 Token 的传统词汇方法不同，神经稀疏模型通常会使用语义相关的术语自动扩展原始文本：

-   **传统的、词汇层面的方法（例如 BM25）**：仅匹配文本中的确切 Token
-   **神经稀疏模型**：自动使用相关术语进行扩展

例如，在上面的代码输出中，句子 "The weather is lovely today" 被扩展为包含 "beautiful"、"cool"、"pretty" 和 "nice" 等原始文本中没有的术语。同样，"It's so sunny outside!" 被扩展为包含 "weather"、"summer" 和 "sun"。

这种扩展使得神经稀疏模型即使没有确切的 Token 匹配，也能匹配语义相关的内容或同义词，处理拼写错误，并克服词汇不匹配问题。这就是为什么像 SPLADE 这样的神经稀疏模型通常优于传统的词汇搜索方法，同时保持了稀疏表示的高效性优势。

然而，扩展也有其风险。例如，对 "What is the weather on Tuesday?" 进行查询扩展，很可能也会扩展到 "monday"、"wednesday" 等，这可能不是期望的结果。

### 为什么使用稀疏嵌入模型？

简而言之，神经稀疏嵌入模型在 BM25 等传统词汇方法和 Sentence Transformers 等密集嵌入模型之间占据了一个有价值的利基位置。它们具有以下优势：

-   混合潜力：与稠密模型结合效果极佳，后者在词汇匹配至关重要的搜索场景中往往表现不佳
-   可解释性：可以清晰看到具体哪些Token对匹配结果有贡献
-   性能：在许多检索任务中与稠密模型相当或更优

本文中，"稀疏嵌入模型"和"稀疏编码器模型"将作为同义词交替使用。

## 为何需要微调？

大多数（神经）稀疏嵌入模型采用前述的查询/文档扩展技术，使得即使文本没有共享任何词汇，也能匹配语义几乎相同的内容。简而言之，模型需要识别同义词，以便将这些Token置入最终嵌入表示。

现成的稀疏嵌入模型通常能轻松识别"supermarket"、"food"和"market"是包含"grocery"文本的有效扩展，但例如：

-   "The patient complained of severe cephalalgia."

会扩展为：

```
'##lal', 'severe', '##pha', 'ce', '##gia', 'patient', 'complaint', 'patients', 'complained', 'warning', 'suffered', 'had', 'disease', 'complain', 'diagnosis', 'syndrome', 'mild', 'pain', 'hospital', 'injury'

```

而我们希望其扩展为"headache"——"cephalalgia"的常用词。这个例子可扩展到许多领域，例如：无法识别"Java"是编程语言，"Audi"生产汽车，或"NVIDIA"是制造显卡的公司。

通过微调，模型可以学会专注于对您重要的特定领域和/或语言。

## 训练组件

训练Sentence Transformer模型包含以下组件：

1.  模型：待训练或微调的模型，可以是预训练的稀疏编码器模型或基础模型
2.  数据集：用于训练和评估的数据
3.  损失函数：量化模型性能并指导优化过程的函数
4.  训练参数（可选）：影响训练性能及跟踪/调试的参数
5.  评估器（可选）：在训练前、中、后评估模型的工具
6.  训练器：整合模型、数据集、损失函数等组件进行训练

现在让我们更详细地探讨每个组件。

## 模型

稀疏编码器模型由一系列模块组成，包括稀疏编码器专用模块或自定义模块，具有高度灵活性。若需进一步微调稀疏编码器模型（例如包含`modules.json`文件），则无需关心具体使用的模块：

```python
from sentence_transformers import SparseEncoder

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")

```

但如果要从其他检查点或从头开始训练，以下是最常用的架构：

### Splade

Splade模型使用`MLMTransformer`后接`SpladePooling`模块。前者加载预训练的掩码语言建模Transformer模型（如BERT、RoBERTa、DistilBERT、ModernBERT等），后者通过池化MLMHead输出生成词汇表大小的单一稀疏嵌入。

```python
from sentence_transformers import models, SparseEncoder
from sentence_transformers.sparse_encoder.models import MLMTransformer, SpladePooling


mlm_transformer = MLMTransformer("google-bert/bert-base-uncased")


splade_pooling = SpladePooling(pooling_strategy="max")


model = SparseEncoder(modules=[mlm_transformer, splade_pooling])

```

若向SparseEncoder提供填充掩码模型架构，此架构为默认设置，因此使用快捷方式更简便：

```python
from sentence_transformers import SparseEncoder

model = SparseEncoder("google-bert/bert-base-uncased")





```

### 免推理Splade

免推理Splade使用`Router`模块为查询和文档配置不同模块。通常此类架构的文档部分采用传统Splade架构（`MLMTransformer`后接`SpladePooling`模块），查询部分则使用`SparseStaticEmbedding`模块——该模块仅返回查询中每个Token的预计算分数。

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.models import Router
from sentence_transformers.sparse_encoder.models import SparseStaticEmbedding, MLMTransformer, SpladePooling


doc_encoder = MLMTransformer("google-bert/bert-base-uncased")


router = Router.for_query_document(
    query_modules=[SparseStaticEmbedding(tokenizer=doc_encoder.tokenizer, frozen=False)],
    
    document_modules=[doc_encoder, SpladePooling("max")],
)


model = SparseEncoder(modules=[router], similarity_fn_name="dot")








```

此架构通过轻量级SparseStaticEmbedding方法实现快速查询处理（可训练并视为线性权重），而文档则使用完整的MLM Transformer和SpladePooling处理。

免推理Splade特别适用于查询延迟至关重要的搜索应用，因为它将计算复杂度转移至可离线执行的文档索引阶段。

使用`Router`模块训练模型时，必须在`SparseEncoderTrainingArguments`中使用`router_mapping`参数将训练数据集列映射到正确路由（"query"或"document"）。例如，若数据集包含`["question", "answer"]`列，可使用以下映射：

```python
args = SparseEncoderTrainingArguments(
    ...,
    router_mapping={
        "question": "query",
        "answer": "document",
    }
)

```

此外，建议为SparseStaticEmbedding模块设置远高于模型其他部分的学习率。为此，应在`SparseEncoderTrainingArguments`中使用`learning_rate_mapping`参数将参数模式映射到对应学习率。例如，若要对SparseStaticEmbedding模块使用`1e-3`学习率，其他部分使用`2e-5`，可配置如下：

```python
args = SparseEncoderTrainingArguments(
    ...,
    learning_rate=2e-5,
    learning_rate_mapping={
        r"SparseStaticEmbedding\.*": 1e-3,
    }
)

```

### 对比稀疏表示（CSR）

对比稀疏表示（CSR）模型（发表于《Beyond Matryoshka: Revisiting Sparse Coding for Adaptive Representation》）在稠密Sentence Transformer模型基础上应用`SparseAutoEncoder`模块，后者通常由`Transformer`后接`Pooling`模块构成。可按如下方式从头初始化：

```python
from sentence_transformers import models, SparseEncoder
from sentence_transformers.sparse_encoder.models import SparseAutoEncoder


transformer = models.Transformer("google-bert/bert-base-uncased")


pooling = models.Pooling(transformer.get_word_embedding_dimension(), pooling_mode="mean")


sparse_auto_encoder = SparseAutoEncoder(
    input_dim=transformer.get_word_embedding_dimension(),
    hidden_dim=4 * transformer.get_word_embedding_dimension(),
    k=256,  
    k_aux=512,  
)

model = SparseEncoder(modules=[transformer, pooling, sparse_auto_encoder])

```

若基础模型是1）稠密Sentence Transformer模型，或2）非MLM Transformer模型（默认加载为Splade模型），此快捷方式将自动初始化CSR模型：

```python
from sentence_transformers import SparseEncoder

model = SparseEncoder("mixedbread-ai/mxbai-embed-large-v1")






```

与（免推理）Splade模型不同，CSR模型的稀疏嵌入尺寸不等于基础模型的词汇表大小。这意味着无法像Splade模型那样直接解释嵌入中激活了哪些词汇（Splade模型的每个维度对应词汇表中的特定Token）。

此外，CSR模型在使用高维表示（如1024-4096维度）的稠密编码器模型上效果最佳。

### 架构选择指南

如果您不确定该使用哪种架构，这里有一份快速指南：

- 您是否希望对现有的稠密嵌入模型进行稀疏化？如果是，请使用 CSR。
- 您是否希望查询推理即时完成，即使以轻微的性能损失为代价？如果是，请使用 Inference-free SPLADE。
- 否则，请使用 SPLADE。

## 数据集

`SparseEncoderTrainer` 使用 `datasets.Dataset` 或 `datasets.DatasetDict` 实例进行训练和评估。您可以从 Hugging Face Datasets Hub 加载数据，或使用各种本地数据格式，如 CSV、JSON、Parquet、Arrow 或 SQL。

注意：许多开箱即用适用于 Sentence Transformers 的公共数据集已在 Hugging Face Hub 上标记了 `sentence-transformers` 标签，因此您可以轻松地在 https://huggingface.co/datasets?other=sentence-transformers 上找到它们。建议浏览这些数据集，以找到可能对您的任务、领域或语言有用的即用型数据集。

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

有些数据集，如 `nthakur/swim-ir-monolingual`，包含具有不同数据格式的多个子集。您需要同时指定数据集名称和子集名称，例如 `dataset = load_dataset("nthakur/swim-ir-monolingual", "de", split="train")`。

### 本地数据（CSV、JSON、Parquet、Arrow、SQL）

您也可以使用 `load_dataset` 加载某些文件格式的本地数据：

```python
from datasets import load_dataset

dataset = load_dataset("csv", data_files="my_file.csv")

dataset = load_dataset("json", data_files="my_file.json")
```

### 需要预处理的本地数据

如果您的本地数据需要预处理，可以使用 `datasets.Dataset.from_dict`。这允许您使用字典列表来初始化数据集：

```python
from datasets import Dataset

queries = []
documents = []



dataset = Dataset.from_dict({
    "query": queries,
    "document": documents,
})
```

字典中的每个键将成为结果数据集中的一列。

### 数据集格式

确保您的数据集格式与您选择的损失函数匹配至关重要。这涉及检查两点：

1.  如果您的损失函数需要一个 `Label`（如损失函数概览表所示），您的数据集必须有一个名为 `"label"` 或 `"score"` 的列。
2.  除了 `"label"` 或 `"score"` 之外的所有列都被视为 `Inputs`（如损失函数概览表所示）。这些列的数量必须与您所选损失函数所需的有效输入数量匹配。列的名称无关紧要，**只有它们的顺序重要**。

例如，如果您的损失函数接受 `(anchor, positive, negative)` 三元组，那么您的第一、第二和第三数据集列分别对应于 `anchor`、`positive` 和 `negative`。这意味着您的第一列和第二列必须包含应该嵌入得很接近的文本，而您的第一列和第三列必须包含应该嵌入得很远的文本。这就是为什么根据您的损失函数，您的数据集列顺序很重要。

考虑一个具有列 `["text1", "text2", "label"]` 的数据集，其中 `"label"` 列包含浮点相似度分数。该数据集可用于 `SparseCoSENTLoss`、`SparseAnglELoss` 和 `SparseCosineSimilarityLoss`，因为：

1.  数据集有一个 "label" 列，这是这些损失函数所要求的。
2.  数据集有 2 个非标签列，与这些损失函数所需的输入数量匹配。

如果数据集中的列顺序不正确，请使用 `Dataset.select_columns` 对它们重新排序。此外，使用 `Dataset.remove_columns` 移除任何无关的列（例如 `sample_id`、`metadata`、`source`、`type`），否则它们将被视为输入。

## 损失函数

损失函数衡量模型在给定数据批次上的表现，并指导优化过程。损失函数的选择取决于您可用的数据和目标任务。请参阅损失函数概览以获取完整的选项列表。

要训练一个 `SparseEncoder`，您需要一个 `SpladeLoss` 或 `CSRLoss`，具体取决于架构。这些是包装器损失函数，它们在主损失函数之上添加了稀疏性正则化，主损失函数必须作为参数提供。唯一可以独立使用的损失函数是 `SparseMSELoss`，因为它执行嵌入级别的蒸馏，通过直接复制教师的稀疏嵌入来确保稀疏性。

大多数损失函数只需使用您正在训练的 `SparseEncoder` 以及一些可选参数即可初始化，例如：

```python
from datasets import load_dataset
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.losses import SpladeLoss, SparseMultipleNegativesRankingLoss


model = SparseEncoder("distilbert/distilbert-base-uncased")



loss = SpladeLoss(
    model=model,
    loss=SparseMultipleNegativesRankingLoss(model=model),
    query_regularizer_weight=5e-5,  
    document_regularizer_weight=3e-5,
) 


train_dataset = load_dataset("sentence-transformers/natural-questions", split="train")
print(train_dataset)
"""
Dataset({
    features: ['query', 'answer'],
    num_rows: 100231
})
"""
```

文档

-   SpladeLoss
-   CSRLoss
-   损失函数 API 参考

## 训练参数

`SparseEncoderTrainingArguments` 类允许您指定影响训练性能和跟踪/调试的参数。虽然是可选的，但尝试这些参数可以帮助提高训练效率并提供对训练过程的洞察。

在 Sentence Transformers 文档中，我概述了一些最有用的训练参数。我建议阅读训练概览 > 训练参数部分。

以下是如何初始化 `SparseEncoderTrainingArguments` 的示例：

```python
from sentence_transformers import SparseEncoderTrainingArguments

args = SparseEncoderTrainingArguments(
    
    output_dir="models/splade-distilbert-base-uncased-nq",
    
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
    run_name="splade-distilbert-base-uncased-nq",  
)
```

请注意，`eval_strategy` 是在 `transformers` 版本 4.41.0 中引入的。更早的版本应使用 `evaluation_strategy`。

## 评估器

您可以向 `SparseEncoderTrainer` 提供一个 `eval_dataset` 以在训练期间获取评估损失，但在训练期间获取更具体的指标也可能很有用。为此，您可以使用评估器在训练前、训练期间或训练后使用有用的指标评估模型的性能。您可以同时使用 `eval_dataset` 和一个评估器，或者只使用其中一个，或者都不用。它们根据训练参数中的 `eval_strategy` 和 `eval_steps` 进行评估。

以下是 Sentence Transformers 为稀疏编码器模型提供的已实现评估器：

此外，应使用 `SequentialEvaluator` 将多个评估器组合成一个评估器，然后可以传递给 `SparseEncoderTrainer`。

有时您没有所需的评估数据来自行准备这些评估器之一，但您仍然希望跟踪模型在某些常见基准测试上的表现。在这种情况下，您可以将这些评估器与来自 Hugging Face 的数据一起使用。

### SparseNanoBEIREvaluator

-   sentence_transformers.sparse_encoder.evaluation.SparseNanoBEIREvaluator

```python
from sentence_transformers.sparse_encoder.evaluation import SparseNanoBEIREvaluator



dev_evaluator = SparseNanoBEIREvaluator()



```

### 使用 STSb 的 SparseEmbeddingSimilarityEvaluator

- sentence-transformers/stsb
- sentence_transformers.sparse_encoder.evaluation.SparseEmbeddingSimilarityEvaluator
- sentence_transformers.SimilarityFunction

```python
from datasets import load_dataset
from sentence_transformers.evaluation import SimilarityFunction
from sentence_transformers.sparse_encoder.evaluation import SparseEmbeddingSimilarityEvaluator


eval_dataset = load_dataset("sentence-transformers/stsb", split="validation")


dev_evaluator = SparseEmbeddingSimilarityEvaluator(
    sentences1=eval_dataset["sentence1"],
    sentences2=eval_dataset["sentence2"],
    scores=eval_dataset["score"],
    main_similarity=SimilarityFunction.COSINE,
    name="sts-dev",
)



```

### 使用 AllNLI 的 SparseTripletEvaluator

- sentence-transformers/all-nli
- sentence_transformers.sparse_encoder.evaluation.SparseTripletEvaluator
- sentence_transformers.SimilarityFunction

```python
from datasets import load_dataset
from sentence_transformers.evaluation import SimilarityFunction
from sentence_transformers.sparse_encoder.evaluation import SparseTripletEvaluator


max_samples = 1000
eval_dataset = load_dataset("sentence-transformers/all-nli", "triplet", split=f"dev[:{max_samples}]")


dev_evaluator = SparseTripletEvaluator(
    anchors=eval_dataset["anchor"],
    positives=eval_dataset["positive"],
    negatives=eval_dataset["negative"],
    main_distance_function=SimilarityFunction.DOT,
    name="all-nli-dev",
)



```

如果在训练过程中频繁评估（使用较小的 `eval_steps`），请考虑使用一个微小的 `eval_dataset` 以最小化评估开销。如果担心评估集的大小，可以采用 90-1-9 的训练-评估-测试分割来取得平衡，为最终评估保留一个合理大小的测试集。训练结束后，你可以使用 `trainer.evaluate(test_dataset)` 来评估模型的测试损失，或者使用 `test_evaluator(model)` 初始化一个测试评估器来获取详细的测试指标。

如果在训练结束后、保存模型之前进行评估，自动生成的模型卡片仍将包含测试结果。

使用**分布式训练**时，评估器只在第一个设备上运行，这与在所有设备间共享的训练和评估数据集不同。

## 训练器

`SparseEncoderTrainer` 是将之前所有组件整合在一起的地方。我们只需指定训练器及其模型、训练参数（可选）、训练数据集、评估数据集（可选）、损失函数、评估器（可选），就可以开始训练。让我们来看一个整合了所有这些组件的脚本示例：

```python
import logging

from datasets import load_dataset

from sentence_transformers import (
    SparseEncoder,
    SparseEncoderModelCardData,
    SparseEncoderTrainer,
    SparseEncoderTrainingArguments,
)
from sentence_transformers.models import Router
from sentence_transformers.sparse_encoder.evaluation import SparseNanoBEIREvaluator
from sentence_transformers.sparse_encoder.losses import SparseMultipleNegativesRankingLoss, SpladeLoss
from sentence_transformers.sparse_encoder.models import SparseStaticEmbedding, MLMTransformer, SpladePooling
from sentence_transformers.training_args import BatchSamplers

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


mlm_transformer = MLMTransformer("distilbert/distilbert-base-uncased", tokenizer_args={"model_max_length": 512})
splade_pooling = SpladePooling(
    pooling_strategy="max", word_embedding_dimension=mlm_transformer.get_sentence_embedding_dimension()
)
router = Router.for_query_document(
    query_modules=[SparseStaticEmbedding(tokenizer=mlm_transformer.tokenizer, frozen=False)],
    document_modules=[mlm_transformer, splade_pooling],
)

model = SparseEncoder(
    modules=[router],
    model_card_data=SparseEncoderModelCardData(
        language="en",
        license="apache-2.0",
        model_name="Inference-free SPLADE distilbert-base-uncased trained on Natural-Questions tuples",
    ),
)


full_dataset = load_dataset("sentence-transformers/natural-questions", split="train").select(range(100_000))
dataset_dict = full_dataset.train_test_split(test_size=1_000, seed=12)
train_dataset = dataset_dict["train"]
eval_dataset = dataset_dict["test"]
print(train_dataset)
print(train_dataset[0])


loss = SpladeLoss(
    model=model,
    loss=SparseMultipleNegativesRankingLoss(model=model),
    query_regularizer_weight=0,
    document_regularizer_weight=3e-3,
)


run_name = "inference-free-splade-distilbert-base-uncased-nq"
args = SparseEncoderTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    learning_rate_mapping={r"SparseStaticEmbedding\.weight": 1e-3},  
    warmup_ratio=0.1,
    fp16=True,  
    bf16=False,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    router_mapping={"query": "query", "answer": "document"},  
    
    eval_strategy="steps",
    eval_steps=1000,
    save_strategy="steps",
    save_steps=1000,
    save_total_limit=2,
    logging_steps=200,
    run_name=run_name,  
)


dev_evaluator = SparseNanoBEIREvaluator(dataset_names=["msmarco", "nfcorpus", "nq"], batch_size=16)


trainer = SparseEncoderTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=dev_evaluator,
)
trainer.train()


dev_evaluator(model)


model.save_pretrained(f"models/{run_name}/final")


model.push_to_hub(run_name)

```

在这个例子中，我从 `distilbert/distilbert-base-uncased` 进行微调，这是一个还不是稀疏编码器模型的基础模型。这比微调一个现有的稀疏编码器模型（如 `naver/splade-cocondenser-ensembledistil`）需要更多的训练数据。

运行此脚本后，模型 `sparse-encoder/example-inference-free-splade-distilbert-base-uncased-nq` 被上传。该模型在 NanoMSMARCO 上获得 0.5241 NDCG@10，在 NanoNFCorpus 上获得 0.3299 NDCG@10，在 NanoNQ 上获得 0.5357 NDCG@10，这对于一个仅使用 Natural Questions 数据集中 10 万对数据训练的、基于 distilbert 的无推理模型来说是一个很好的结果。

该模型在文档的稀疏嵌入中平均使用 184 个活跃维度，而查询的平均活跃维度为 7.7 个（即查询中的平均 Token 数）。这分别对应 99.39% 和 99.97% 的稀疏度。

所有这些信息都存储在自动生成的模型卡片中，包括基础模型、语言、许可证、评估结果、训练和评估数据集信息、超参数、训练日志等。无需任何额外努力，你上传的模型应包含潜在用户判断模型是否适合他们所需的所有信息。

### 回调函数

Sentence Transformers 训练器支持各种 `transformers.TrainerCallback` 子类，包括：

- `WandbCallback`：如果安装了 `wandb`，用于将训练指标记录到 W&B
- `TensorBoardCallback`：如果 `tensorboard` 可用，用于将训练指标记录到 TensorBoard
- `CodeCarbonCallback`：如果安装了 `codecarbon`，用于跟踪训练期间的碳排放

只要安装了所需的依赖项，这些回调函数会自动使用，无需你特别指定。

有关这些回调函数以及如何创建自定义回调的更多信息，请参阅 **Transformers 回调函数文档**。

### 多数据集训练

表现最佳的模型通常使用多个数据集同时进行训练。`SparseEncoderTrainer` 简化了这一过程，允许你使用多个数据集进行训练，而无需将它们转换为相同格式。你甚至可以对每个数据集应用不同的损失函数。以下是多数据集训练的步骤：

1.  使用一个由 `datasets.Dataset` 实例组成的字典（或一个 `datasets.DatasetDict`）作为 `train_dataset` 和 `eval_dataset`。
2.  （可选）如果您想为不同的数据集使用不同的损失函数，可以使用一个将数据集名称映射到损失函数的字典。

每个训练/评估批次将仅包含来自其中一个数据集的样本。从多个数据集中采样批次的顺序由 `MultiDatasetBatchSamplers` 枚举决定，可以通过 `multi_dataset_batch_sampler` 传递给 `SparseEncoderTrainingArguments`。有效的选项有：

- `MultiDatasetBatchSamplers.ROUND_ROBIN`：以轮询方式从每个数据集中采样，直到其中一个耗尽。此策略可能不会使用每个数据集的所有样本，但它确保从每个数据集进行等量采样。
- `MultiDatasetBatchSamplers.PROPORTIONAL`（默认）：根据数据集大小按比例从每个数据集中采样。此策略确保使用每个数据集的所有样本，并且更频繁地从较大的数据集中采样。

## 评估

让我们使用 NanoMSMARCO 数据集来评估我们新训练的无推理 SPLADE 模型，并看看它与密集检索方法相比如何。我们还将探索结合稀疏和密集向量的混合检索方法，以及重新排序以进一步提高搜索质量。

运行我们稍作修改的 `hybrid_search.py` 脚本后，我们针对 NanoMSMARCO 数据集使用以下模型得到了以下结果：

- 稀疏：`sparse-encoder/example-inference-free-splade-distilbert-base-uncased-nq`（我们刚刚训练的模型）
- 密集：`sentence-transformers/all-MiniLM-L6-v2`
- 重排序器：`cross-encoder/ms-marco-MiniLM-L6-v2`

稀疏和密集排名可以使用倒数排名融合（RRF）进行组合，这是一种组合多个排名结果的简单方法。如果应用了重排序器，它将重新排序先前检索步骤的结果。

结果表明，对于此数据集，结合密集和稀疏排名性能非常好，分别比密集和稀疏基线提高了 12.3% 和 18.7%。简而言之，结合稀疏和密集检索方法是提高搜索性能的一种非常有效的方式。

此外，对任何排名应用重排序器都将性能提升至约 66.3 NDCG@10，这表明无论是稀疏、密集还是混合（密集 + 稀疏）检索，都在其前 100 个结果中找到了相关文档，然后重排序器将这些文档排到了前 10 位。因此，用稀疏 -> 重排序器流程替换密集 -> 重排序器流程可能会改善延迟和成本：

- 稀疏嵌入的存储成本可能更低，例如，我们的模型对于 MS MARCO 文档仅使用约 180 个活跃维度，而不是密集模型常见的 1024 个维度。
- 一些稀疏编码器允许无推理查询处理，从而实现近乎即时的第一阶段检索，类似于 BM25 等词汇解决方案。

## 训练技巧

稀疏编码器模型有一些特点，在训练时需要注意：

1.  评估稀疏编码器模型不应仅使用评估分数，还应考虑嵌入的稀疏性。毕竟，低稀疏性意味着模型嵌入存储成本高且检索速度慢。
2.  较强的稀疏编码器模型几乎完全是通过从更强的教师模型（例如 `CrossEncoder` 模型）进行蒸馏来训练的，而不是直接从文本对或三元组训练。例如，参见 `SPLADE-v3` 论文，该论文使用 `SparseDistillKLDivLoss` 和 `SparseMarginMSELoss` 进行蒸馏。我们在本博客中没有详细讨论这一点，因为它需要更多的数据准备工作，但应认真考虑蒸馏设置。

## 向量数据库集成

训练完稀疏嵌入模型后，下一个关键步骤是在生产环境中有效地部署它们。向量数据库为大规模存储、索引和检索稀疏嵌入提供了必要的基础设施。流行的选择包括 Qdrant、OpenSearch、Elasticsearch 和 Seismic 等。

有关上述向量数据库的全面示例，请参阅 `semantic search with vector database documentation` 或下面的 Qdrant 示例。

### Qdrant 集成示例

Qdrant 为稀疏向量提供了出色的支持，具有高效的存储和快速检索能力。以下是一个全面的实现示例：

### 先决条件：

- Qdrant 在本地运行（或可访问），详情请参阅 `Qdrant Quickstart`。
- 已安装 Python Qdrant 客户端：`pip install qdrant-client`

```bash
pip install qdrant-client

```

此示例演示了如何为稀疏向量搜索设置 Qdrant，展示了如何使用稀疏编码器高效编码和索引文档，使用稀疏向量制定搜索查询，并提供交互式查询界面。见下文：

```python
import time

from datasets import load_dataset
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.search_engines import semantic_search_qdrant


dataset = load_dataset("sentence-transformers/natural-questions", split="train")
num_docs = 10_000
corpus = dataset["answer"][:num_docs]


queries = dataset["query"][:2]


sparse_model = SparseEncoder("naver/splade-cocondenser-ensembledistil")


corpus_embeddings = sparse_model.encode_document(
    corpus, convert_to_sparse_tensor=True, batch_size=16, show_progress_bar=True
)


corpus_index = None
while True:
    
    start_time = time.time()
    query_embeddings = sparse_model.encode_query(queries, convert_to_sparse_tensor=True)
    print(f"Encoding time: {time.time() - start_time:.6f} seconds")

    
    results, search_time, corpus_index = semantic_search_qdrant(
        query_embeddings,
        corpus_index=corpus_index,
        corpus_embeddings=corpus_embeddings if corpus_index is None else None,
        top_k=5,
        output_index=True,
    )

    
    print(f"Search time: {search_time:.6f} seconds")
    for query, result in zip(queries, results):
        print(f"Query: {query}")
        for entry in result:
            print(f"(Score: {entry['score']:.4f}) {corpus[entry['corpus_id']]}, corpus_id: {entry['corpus_id']}")
        print("")

    
    queries = [input("Please enter a question: ")]

```

## 其他资源

### 训练示例

以下页面包含带有解释的训练示例以及代码链接。我们建议您浏览这些内容以熟悉训练流程：

- `Model Distillation` - 使模型更小、更快、更轻的示例。
- `MS MARCO` - 在 MS MARCO 信息检索数据集上进行训练的示例训练脚本。
- `Retrievers` - 在通用信息检索数据集上进行训练的示例训练脚本。
- `Natural Language Inference` - 自然语言推理（NLI）数据对于预训练和微调模型以创建有意义的稀疏嵌入非常有帮助。
- `Quora Duplicate Questions` - Quora 重复问题是一个大型语料库，包含来自 Quora 社区的重复问题。该文件夹包含如何训练模型用于重复问题挖掘和语义搜索的示例。
- `STS` - 训练模型最基本的方法是使用语义文本相似性（STS）数据。在这里，我们使用句子对和一个表示语义相似性的分数。

此外，以下页面可能有助于您了解更多关于 Sentence Transformers 的信息：

- `Installation`
- `Quickstart`
- `Usage`
- `Pretrained Models`
- `Training Overview`（本博客是训练概述文档的精简版）
- `Dataset Overview`
- `Loss Overview`
- `API Reference`

最后，这里有一些您可能感兴趣的高级页面：

- `Hyperparameter Optimization`
- `Distributed Training`

---

> 本文由AI自动翻译，原文链接：[Training and Finetuning Sparse Embedding Models with Sentence Transformers v5](https://huggingface.co/blog/train-sparse-encoder)
> 
> 翻译时间：2026-03-21 04:34
