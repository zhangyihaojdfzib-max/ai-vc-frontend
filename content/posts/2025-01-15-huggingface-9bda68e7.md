---
title: 静态嵌入模型训练提速400倍
title_original: Train 400x faster Static Embedding Models with Sentence Transformers
date: '2025-01-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/static-embeddings
author: ''
summary: 本文介绍了一种训练静态嵌入模型的方法，使模型在CPU上的运行速度比最先进的嵌入模型快100到400倍，同时保留大部分质量。作者发布了两个高效模型：英文检索模型和多语言相似度模型，并公开了详细训练策略、数据集列表及训练脚本。这些模型适用于设备端、浏览器、边缘计算等低功耗场景，使用方式与标准Sentence
  Transformers流程一致。
categories:
- AI研究
tags:
- 静态嵌入
- Sentence Transformers
- 模型加速
- 检索
- 多语言相似度
draft: false
translated_at: '2026-06-01T06:54:40.186667'
---

# 使用 Sentence Transformers 训练速度提升 400 倍的静态嵌入模型

## TL;DR

本文介绍了一种训练静态嵌入模型的方法，该模型在 CPU 上的运行速度比最先进的嵌入模型快 100 到 400 倍，同时保留了大部分质量。这开启了许多令人兴奋的应用场景，包括设备端和浏览器内执行、边缘计算、低功耗及嵌入式应用。

我们应用这一方案训练了两个极其高效的嵌入模型：`sentence-transformers/static-retrieval-mrl-en-v1` 用于英文检索，以及 `sentence-transformers/static-similarity-mrl-multilingual-v1` 用于多语言相似度任务。这些模型在 CPU 上的速度比常见的同类模型（如 `all-mpnet-base-v2` 和 `multilingual-e5-small`）快 100 到 400 倍，同时在各种基准测试中达到其性能的至少 85%。

今天，我们发布：

- 上述两个模型（分别用于英文检索和多语言相似度）。
- 我们遵循的详细训练策略，从构思到数据集选择，再到实现和评估。
- 两个基于开源 sentence transformers 库的训练脚本。
- 两份 Weights and Biases 报告，包含训练期间收集的训练和评估指标。
- 我们使用的数据集详细列表：30 个用于训练，13 个用于评估。

我们还讨论了潜在的改进方向，并鼓励社区探索这些方向并在此基础上继续开发！

这些模型的使用非常简单，与正常的 Sentence Transformers 流程相同：

英文检索

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")

sentences = [
    'Gadofosveset-enhanced MR angiography of carotid arteries: does steady-state imaging improve accuracy of first-pass imaging?',
    'To evaluate the diagnostic accuracy of gadofosveset-enhanced magnetic resonance (MR) angiography in the assessment of carotid artery stenosis, with digital subtraction angiography (DSA) as the reference standard, and to determine the value of reading first-pass, steady-state, and "combined" (first-pass plus steady-state) MR angiograms.',
    'In a longitudinal study we investigated in vivo alterations of CVO during neuroinflammation, applying Gadofluorine M- (Gf) enhanced magnetic resonance imaging (MRI) in experimental autoimmune encephalomyelitis, an animal model of multiple sclerosis. SJL/J mice were monitored by Gadopentate dimeglumine- (Gd-DTPA) and Gf-enhanced MRI after adoptive transfer of proteolipid-protein-specific T cells. Mean Gf intensity ratios were calculated individually for different CVO and correlated to the clinical disease course. Subsequently, the tissue distribution of fluorescence-labeled Gf as well as the extent of cellular inflammation was assessed in corresponding histological slices.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)

similarities = model.similarity(embeddings[0], embeddings[1:])
print(similarities)
```

多语言相似度

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/static-similarity-mrl-multilingual-v1", device="cpu")

sentences = [
    'It is known for its dry red chili powder.',
    'It is popular for dried red chili powder.',
    'These monsters will move in large groups.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)

similarities = model.similarity(embeddings, embeddings)
print(similarities)
```

![NanoBEIR 性能与推理速度对比](/images/posts/3396033b9ba2.png)

- TL;DR
- 什么是嵌入？现代嵌入静态嵌入
- 我们的方法
- 训练细节训练要求模型灵感英文检索多语言相似度训练数据集选择英文检索多语言相似度代码损失函数选择代码Matryoshka 表示学习代码训练参数选择代码评估器选择代码硬件细节整体训练脚本英文检索多语言相似度
- 使用方法英文检索多语言相似度Matryoshka 维度截断第三方库LangChainLlamaIndexHaystacktxtai
- 性能英文检索NanoBEIRGPUCPUMatryoshka 评估多语言相似度Matryoshka 评估
- 结论
- 下一步计划

- 现代嵌入
- 静态嵌入

- 训练要求
- 模型灵感英文检索多语言相似度
- 训练数据集选择英文检索多语言相似度代码
- 损失函数选择代码Matryoshka 表示学习代码
- 训练参数选择代码
- 评估器选择代码
- 硬件细节
- 整体训练脚本英文检索多语言相似度

- 英文检索
- 多语言相似度

- 英文检索
- 多语言相似度
- 代码

- 代码
- Matryoshka 表示学习代码

- 代码

- 英文检索
- 多语言相似度

- 英文检索
- 多语言相似度
- Matryoshka 维度截断
- 第三方库LangChainLlamaIndexHaystacktxtai

- LangChain
- LlamaIndex
- Haystack
- txtai

- 英文检索NanoBEIRGPUCPUMatryoshka 评估
- 多语言相似度Matryoshka 评估

- NanoBEIRGPUCPU
- Matryoshka 评估

- GPU
- CPU

- Matryoshka 评估

## 什么是嵌入？

嵌入是自然语言处理中最通用的工具之一，使从业者能够解决大量不同类型的任务。本质上，嵌入是更复杂对象（如文本、图像、音频等）的数值表示。

![嵌入模型](/images/posts/3d166056ba7d.png)

嵌入模型始终会生成固定大小的嵌入。然后，你可以通过计算相应嵌入的相似度来计算复杂对象的相似度。

![嵌入相似度](/images/posts/fd8ca75a94da.png)

这有大量的应用场景，并作为推荐系统、检索、异常检测、单样本或少样本学习、相似度搜索、聚类、释义检测、分类等任务的基础。

### 现代嵌入

当今许多嵌入模型由几个转换步骤组成。遵循这些步骤被称为"推理"。

Tokenizer 和 Pooler 分别负责 Encoder 的前处理和後处理。前者将文本切分为 Encoder 可以理解的 Token（即单词或子词），而后者将所有 Token 的嵌入合并为整个文本的一个嵌入。

在此流程中，Encoder 通常是一个带有注意力层的语言模型，这使得每个 Token 可以在其他 Token 的上下文中进行计算。例如，bank 可能是一个 Token，但如果文本指的是"river bank"（河岸）还是金融机构，该 Token 的嵌入可能会不同。

具有大量注意力层的大型编码器模型能够有效利用上下文生成有用的嵌入，但代价是推理速度缓慢。值得注意的是，在流程中，Encoder 步骤通常占据了几乎所有的计算时间。

### 静态嵌入

静态嵌入指的是一组 Encoder 模型，它们不使用大型且缓慢的基于注意力的模型，而是依赖预先计算的 Token 嵌入。静态嵌入在 Transformer 架构开发之前就已使用多年。常见的例子包括 GLoVe 和 word2vec。最近，Model2Vec 被用于将预训练的嵌入模型转换为静态嵌入模型。

对于静态嵌入，Encoder 步骤简单到如同字典查找：给定 Token，返回预先计算的 Token 嵌入。因此，推理不再受 Encoder 阶段的瓶颈限制，从而实现了数个数量级的加速。本文表明，对质量的影响可以非常小！

## 我们的方法

我们着手重新审视静态嵌入模型，采用现代技术对其进行训练。我们的主要改进来自对比学习损失函数的使用，稍后将详细说明。此外，我们还可以通过使用马特罗什卡表示学习来获得额外的速度提升，这使得使用截断版本的嵌入向量成为可能。

我们将使用 Sentence Transformers 库进行训练。关于如何使用该库训练嵌入模型的更全面概述，请参阅《使用 Sentence Transformers 训练和微调嵌入模型》博客文章或《Sentence Transformers 训练概述》文档。

## 训练细节

这些重新构想的静态嵌入的目标是，在这些高效的嵌入模型上实验现代嵌入模型微调技术。特别是，与 GLoVe 和 word2vec 不同，我们将使用：

1. 对比学习：在大多数机器学习中，你输入 $X$ 并期望输出 $Y$，然后训练模型使得 $X$ 经过模型后产生接近 $Y$ 的结果。对于嵌入模型，我们没有 $Y$：我们事先不知道一个好的嵌入应该是什么。相反，在对比学习中，我们有多个输入 $X_1$ 和 $X_2$，以及一个相似度。我们将两个输入都送入模型，然后对比两个嵌入，得到一个预测的相似度。如果真实相似度低，我们可以将嵌入推得更远；如果真实相似度高，我们可以将嵌入拉得更近。
2. 马特罗什卡表示学习 (MRL)：马特罗什卡嵌入模型（博客文章）是一种巧妙的训练方法，允许用户将嵌入模型截断为更小的维度，而性能损失极小。它涉及不仅使用正常大小的嵌入，还使用其截断版本来应用对比损失函数。因此，模型学会将信息主要存储在嵌入的开头部分。截断后的嵌入在下游应用（如检索、分类和聚类）中会更快。

对比学习：在大多数机器学习中，你输入 $X$ 并期望输出 $Y$，然后训练模型使得 $X$ 经过模型后产生接近 $Y$ 的结果。对于嵌入模型，我们没有 $Y$：我们事先不知道一个好的嵌入应该是什么。

相反，在对比学习中，我们有多个输入 $X_1$ 和 $X_2$，以及一个相似度。我们将两个输入都送入模型，然后对比两个嵌入，得到一个预测的相似度。如果真实相似度低，我们可以将嵌入推得更远；如果真实相似度高，我们可以将嵌入拉得更近。

马特罗什卡表示学习 (MRL)：马特罗什卡嵌入模型（博客文章）是一种巧妙的训练方法，允许用户将嵌入模型截断为更小的维度，而性能损失极小。它涉及不仅使用正常大小的嵌入，还使用其截断版本来应用对比损失函数。因此，模型学会将信息主要存储在嵌入的开头部分。

截断后的嵌入在下游应用（如检索、分类和聚类）中会更快。

对于未来的研究，我们留下了各种其他用于提高数据质量的现代训练方法。请参阅《后续步骤》了解具体想法。

### 训练要求

如 Sentence Transformers 中的《训练概述》文档所示，训练包含 3 到 5 个组件：

1. 数据集
2. 损失函数
3. 训练参数（可选）
4. 评估器（可选）
5. 训练器

在接下来的部分中，我们将逐一介绍我们对每个组件的思考过程。

### 模型灵感

根据我们的经验，嵌入模型要么 1) 专门用于检索，要么 2) 用于各种任务（分类、聚类、语义文本相似度等）。我们着手各训练一个模型。

对于检索模型，可用的多语言检索训练数据有限，因此我们选择仅使用英文模型。相比之下，我们决定训练一个多语言通用相似度模型，因为对于此任务，多语言数据更容易获取。

对于这些模型，我们希望使用 `StaticEmbedding` 模块，它实现了一个高效的 `tokenize` 方法（避免填充）和一个高效的 `forward` 方法（负责计算和池化嵌入）。它就像使用一个 `torch.EmbeddingBag` 一样简单，后者本质上就是一个带有均值池化的高效 `Embedding`（即嵌入查找表）。

我们可以通过几种方式初始化它：`StaticEmbedding.from_model2vec` 加载 Model2Vec 模型，`StaticEmbedding.from_distillation` 执行 Model2Vec 风格的蒸馏，或者使用一个 `Tokenizer` 和嵌入维度初始化以获得随机权重。

根据我们的发现，当使用大量数据进行完整训练时，最后一种方式效果最佳。为了匹配常见的模型，如 `all-mpnet-base-v2` 或 `bge-large-en-v1.5`，我们选择嵌入维度为 1024，即每个嵌入向量由 1024 个值组成。

对于英文检索模型，我们依赖 `google-bert/bert-base-uncased` 分词器。因此，初始化模型如下所示：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=1024)

model = SentenceTransformer(modules=[static_embedding])

```

`modules` 列表中的第一个条目必须实现 `tokenize`，最后一个条目必须产生池化后的嵌入。这里两者都满足，因此我们可以开始训练这个模型了。

对于多语言相似度模型，我们转而依赖 `google-bert/bert-base-multilingual-uncased` 分词器，这是我们初始化代码中唯一改变的地方：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-multilingual-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=1024)

model = SentenceTransformer(modules=[static_embedding])

```

### 训练数据集选择

除了数十个 Sentence Transformer 模型外，Hugging Face 上的 Sentence Transformers 组织还托管了 70 多个数据集（截至撰写本文时）：

- 嵌入模型数据集

除此之外，许多数据集已被标记为 `sentence-transformers`，以表明它们对训练嵌入模型有用：

- 带有 `sentence-transformers` 标签的数据集

对于英文检索数据集，我们主要寻找满足以下条件的数据集：

- 问答对，可选地包含负样本（即错误答案），以及
- 与 BEIR 基准（即 MTEB 上的“检索”选项卡）无重叠。我们的目标是避免在这些数据集上进行训练，以便将 MTEB 用作零样本基准。

我们选择了以下数据集：

- gooaq
- msmarco - “triplet” 子集
- squad
- s2orc - “title-abstract-pair” 子集
- allnli - “triplet” 子集
- paq
- trivia_qa
- msmarco_10m
- swim_ir - “en” 子集
- pubmedqa - “triplet-20” 子集
- miracl - “en-triplet-all” 子集
- mldr - “en-triplet-all” 子集
- mr_tydi - “en-triplet-all” 子集

对于多语言相似度数据集，我们目标是满足以下条件的数据集：

- 跨语言的平行句子，即同一文本的多种语言版本，或
- 正样本对，即具有高相似度的句子对，可选地包含负样本（即低相似度）。

我们选择了以下包含平行句子的数据集：

- wikititles
- tatoeba
- talks
- europarl
- global_voices
- muse
- wikimatrix
- opensubtitles

以及这些包含某种正样本对的数据集：

- stackexchange - "post-post-pair" 子集  
- quora - "triplet" 子集  
- wikianswers_duplicates  
- all_nli - "triplet" 子集  
- simple_wiki  
- altlex  
- flickr30k_captions  
- coco_captions  
- nli_for_simcse  
- negation  

加载这些数据集相当简单，例如：

```python
from datasets import load_dataset, Dataset

gooaq_dataset = load_dataset("sentence-transformers/gooaq", split="train")
gooaq_dataset_dict = gooaq_dataset.train_test_split(test_size=10_000, seed=12)
gooaq_train_dataset: Dataset = gooaq_dataset_dict["train"]
gooaq_eval_dataset: Dataset = gooaq_dataset_dict["test"]

print(gooaq_train_dataset)
"""
Dataset({
    features: ['question', 'answer'],
    num_rows: 3002496
})
"""

print(gooaq_eval_dataset)
"""
Dataset({
    features: ['question', 'answer'],
    num_rows: 10000
})
"""

```

`gooaq` 数据集本身没有训练-评估划分，因此我们可以使用 `train_test_split` 创建一个。否则，我们也可以直接加载预计算好的划分，例如使用 `split="eval"`。

请注意，`train_test_split` 意味着数据集必须加载到内存中，而通常情况下它只保存在磁盘上。这种内存增加在训练时并不理想，因此建议：1) 加载数据，2) 进行划分，3) 使用 `save_to_disk` 将其保存到磁盘。在训练之前，你可以使用 `load_from_disk` 再次加载。

### 损失函数选择

在 Sentence Transformers 中，你的损失模型必须与训练数据格式匹配。[损失函数概述](https://sbert.net/docs/sentence_transformer/loss_overview.html) 旨在概述哪些损失函数与哪些格式兼容。

具体来说，我们的数据中目前有以下几种格式：

- (anchor, positive) 对，无标签
- (anchor, positive, negative) 三元组，无标签
- (anchor, positive, negative_1, ..., negative_n) 元组，无标签

对于这些格式，我们有一些极好的选择：

1. **MultipleNegativesRankingLoss (MNRL)**：也称为批内负样本损失或 InfoNCE 损失，这种损失函数已被用于训练现代嵌入模型数年。简而言之，该损失函数优化以下目标：给定一个锚点（例如一个问题），在批次中的所有正样本和负样本（例如所有答案）中，为对应的正样本（即答案）分配最高的相似度。如果你提供了可选的负样本，它们将仅作为额外的选项（也称为批内负样本），模型必须从中选出正确的正样本。在合理范围内，这种“挑选”越困难，模型就会变得越强。因此，更大的批次大小会产生更多的批内负样本，从而（在一定程度上）提升性能。
2. **CachedMultipleNegativesRankingLoss (CMNRL)**：这是 MNRL 的一个扩展，实现了 GradCache，一种允许在不增加内存的情况下任意增大批次大小的方法。除非你仅使用 MNRL 就能在内存中容纳足够大的批次大小，否则建议使用此损失函数而非 MNRL。在这种情况下，你可以使用 MNRL 来节省 CMNRL 带来的 20% 训练速度成本。
3. **GISTEmbedLoss (GIST)**：这也是 MNRL 的一个扩展，它使用一个引导 Sentence Transformer 模型，从模型必须“挑选”正确正样本的选项列表中移除潜在的假负样本。假负样本会损害性能，但困难的真负样本（接近正确但又不完全正确的文本）有助于提升性能，因此这种过滤需要谨慎权衡。

MultipleNegativesRankingLoss (MNRL)：也称为批内负样本损失或 InfoNCE 损失，这种损失函数已被用于训练现代嵌入模型数年。简而言之，该损失函数优化以下目标：

给定一个锚点（例如一个问题），在批次中的所有正样本和负样本（例如所有答案）中，为对应的正样本（即答案）分配最高的相似度。

如果你提供了可选的负样本，它们将仅作为额外的选项（也称为批内负样本），模型必须从中选出正确的正样本。在合理范围内，这种“挑选”越困难，模型就会变得越强。因此，更大的批次大小会产生更多的批内负样本，从而（在一定程度上）提升性能。

CachedMultipleNegativesRankingLoss (CMNRL)：这是 MNRL 的一个扩展，实现了 GradCache，一种允许在不增加内存的情况下任意增大批次大小的方法。

除非你仅使用 MNRL 就能在内存中容纳足够大的批次大小，否则建议使用此损失函数而非 MNRL。在这种情况下，你可以使用 MNRL 来节省 CMNRL 带来的 20% 训练速度成本。

GISTEmbedLoss (GIST)：这也是 MNRL 的一个扩展，它使用一个引导 Sentence Transformer 模型，从模型必须“挑选”正确正样本的选项列表中移除潜在的假负样本。

假负样本会损害性能，但困难的真负样本（接近正确但又不完全正确的文本）有助于提升性能，因此这种过滤需要谨慎权衡。

由于这些静态嵌入模型非常小，我们可以在硬件（一块 24GB 的 RTX 3090）上容纳所需的 2048 个样本的批次大小，因此我们不需要使用 CMNRL。

此外，由于我们训练的是非常快速的模型，GISTEmbedLoss 中的引导模型会使训练变得慢得多。因此，我们选择使用 MultipleNegativesRankingLoss 来训练我们的模型。

如果我们再次尝试这些实验，我们会选择更大的批次大小，例如使用 CMNRL 达到 16384。如果你尝试了，请告诉我们效果如何！

使用方法相当简单：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.losses import MultipleNegativesRankingLoss


tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=1024)
model = SentenceTransformer(modules=[static_embedding])


loss = MultipleNegativesRankingLoss(model)

```

#### 套娃表示学习

除了常规的损失函数，Sentence Transformers 还实现了一些[损失函数修饰器](https://sbert.net/docs/sentence_transformer/loss_overview.html#loss-modifiers)。它们作用于标准损失函数之上，但以不同的方式应用它们，以试图向训练好的嵌入模型注入有用的特性。

一个非常有趣的修饰器是 MatryoshkaLoss，它将训练好的模型转变为[套娃模型](https://arxiv.org/abs/2205.13147)。这使得用户可以在性能损失最小的情况下截断输出嵌入，从而由于维度更小，可以加快检索或聚类速度。

MatryoshkaLoss 应用于常规损失函数之上。建议在 matryoshka_dims 列表中也包含正常的嵌入维度：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.losses import MultipleNegativesRankingLoss, MatryoshkaLoss


tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=1024)
model = SentenceTransformer(modules=[static_embedding])


base_loss = MultipleNegativesRankingLoss(model)
loss = MatryoshkaLoss(model, base_loss, matryoshka_dims=[1024, 768, 512, 256, 128, 64, 32])

```

### 训练参数选择

Sentence Transformers 支持大量训练参数，其中最有价值的已在[训练概述 > 训练参数](https://sbert.net/docs/sentence_transformer/training_overview.html#training-arguments)文档中列出。

我们使用相同的核心训练参数来训练两个模型：

- `num_train_epochs: 1`：我们有足够的数据，如果需要训练更多轮次，可以添加更多数据，而不是用相同数据多次训练。
- `per_device_train_batch_size/per_device_eval_batch_size: 2048`：2048维向量在我们的RTX 3090上运行良好。多篇论文（Xiao等人、Li等人）表明，更大的批次大小仍能提升性能。未来版本中，我们将使用更大的批次大小（例如16384）应用`CachedMultipleNegativesRankingLoss`。
- `learning_rate: 2e-1`：注意！这远高于常规嵌入模型训练（通常使用约2e-5的损失值）。
- `warmup_ratio: 0.1`：0.1或10%是非常标准的热身比例，用于让模型平滑适应高学习率。
- `bf16: True`：如果您的GPU支持`bf16`，通常建议使用它进行训练。否则，如果支持`fp16=True`，也可以使用。
- `batch_sampler: BatchSamplers.NO_DUPLICATES`：所有使用批次内负样本的损失函数（如MNRL）都受益于这种避免批次内重复的批次采样器。重复样本常导致假负例，削弱训练后的模型。
- `multi_dataset_batch_sampler: MultiDatasetBatchSamplers.PROPORTIONAL`：当使用多个数据集训练时，各数据集大小通常不同。此时有两种选择：轮询法：从每个数据集采样相同数量的批次，直到某个数据集耗尽。数据分布均匀，但并非所有数据都会被使用。比例法：对每个数据集持续采样直到全部耗尽。所有数据都会被使用，但数据分布不均匀。我们选择后者，因为不太担心数据不平衡问题。

- 我们有足够的数据，如果需要训练更多轮次，可以添加更多数据，而不是用相同数据多次训练。

- 2048维向量在我们的RTX 3090上运行良好。多篇论文（Xiao等人、Li等人）表明，更大的批次大小仍能提升性能。未来版本中，我们将使用更大的批次大小（例如16384）应用`CachedMultipleNegativesRankingLoss`。

- 注意！这远高于常规嵌入模型训练（通常使用约2e-5的损失值）。

- 0.1或10%是非常标准的热身比例，用于让模型平滑适应高学习率。

- 如果您的GPU支持`bf16`，通常建议使用它进行训练。否则，如果支持`fp16=True`，也可以使用。

- 所有使用批次内负样本的损失函数（如MNRL）都受益于这种避免批次内重复的批次采样器。重复样本常导致假负例，削弱训练后的模型。

- 当使用多个数据集训练时，各数据集大小通常不同。此时有两种选择：轮询法：从每个数据集采样相同数量的批次，直到某个数据集耗尽。数据分布均匀，但并非所有数据都会被使用。比例法：对每个数据集持续采样直到全部耗尽。所有数据都会被使用，但数据分布不均匀。我们选择后者，因为不太担心数据不平衡问题。

- 轮询法：从每个数据集采样相同数量的批次，直到某个数据集耗尽。数据分布均匀，但并非所有数据都会被使用。
- 比例法：对每个数据集持续采样直到全部耗尽。所有数据都会被使用，但数据分布不均匀。我们选择后者，因为不太担心数据不平衡问题。

除了这些核心参数，我们还设置了一些用于跟踪和调试的训练参数：`eval_strategy`、`eval_steps`、`save_strategy`、`save_steps`、`save_total_limit`、`logging_steps`、`logging_first_step`和`run_name`。

最终，我们为两个模型使用了以下`SentenceTransformerTrainingArguments`：

```python
run_name = "static-retrieval-mrl-en-v1"



args = SentenceTransformerTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=2048,
    per_device_eval_batch_size=2048,
    learning_rate=2e-1,
    warmup_ratio=0.1,
    fp16=False,  
    bf16=True,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL,
    
    eval_strategy="steps",
    eval_steps=1000,
    save_strategy="steps",
    save_steps=1000,
    save_total_limit=2,
    logging_steps=1000,
    logging_first_step=True,
    run_name=run_name,  
)

```

### 评估器选择

如果我们向Sentence Transformer训练器提供评估数据集，则在评估时会得到评估损失值。这有助于跟踪是否过拟合，但对于实际下游性能而言意义不大。

因此，Sentence Transformers额外支持`Evaluators`。与训练损失不同，这些评估器提供定性指标，如信息检索中的NDCG、MAP、MRR，语义文本相似度中的Spearman相关系数，或三元组准确率（`similarity(anchor, positive)>similarity(anchor, negative)`的样本数量）。

由于简单易用，我们将为检索模型使用`NanoBEIREvaluator`。该评估器在`NanoBEIR`数据集集合上运行信息检索基准测试。该数据集是更大（因此更慢）的BEIR基准测试的子集，后者通常用作MTEB排行榜中的检索选项卡。

由于所有数据集都已预定义，我们可以无需任何参数直接加载评估器：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import NanoBEIREvaluator


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


evaluator = NanoBEIREvaluator()


evaluator(model)

```

### 硬件详情

我们在消费级硬件上训练这些模型，具体配置如下：

- GPU：RTX 3090
- CPU：i7-13700K
- 内存：32GB

### 完整训练脚本

本节包含两个模型的最终训练脚本，整合了之前描述的所有组件（数据集、损失函数、训练参数、评估器、训练器）。

```python
import random
import logging
from datasets import load_dataset, Dataset, DatasetDict
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
    SentenceTransformerModelCardData,
)
from sentence_transformers.losses import MatryoshkaLoss, MultipleNegativesRankingLoss
from sentence_transformers.training_args import BatchSamplers, MultiDatasetBatchSamplers
from sentence_transformers.evaluation import NanoBEIREvaluator
from sentence_transformers.models.StaticEmbedding import StaticEmbedding

from transformers import AutoTokenizer

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)
random.seed(12)


def load_train_eval_datasets():
    """
    从磁盘加载训练和评估数据集，或从datasets库加载并保存到磁盘。

    保存到磁盘后，我们执行quit()以确保数据集在训练前不会加载到内存中。
    """
    try:
        train_dataset = DatasetDict.load_from_disk("datasets/train_dataset")
        eval_dataset = DatasetDict.load_from_disk("datasets/eval_dataset")
        return train_dataset, eval_dataset
    except FileNotFoundError:
        print("正在加载gooaq数据集...")
        gooaq_dataset = load_dataset("sentence-transformers/gooaq", split="train")
        gooaq_dataset_dict = gooaq_dataset.train_test_split(test_size=10_000, seed=12)
        gooaq_train_dataset: Dataset = gooaq_dataset_dict["train"]
        gooaq_eval_dataset: Dataset = gooaq_dataset_dict["test"]
        print("已加载gooaq数据集。")

```python
print("正在加载msmarco数据集...")
        msmarco_dataset = load_dataset("sentence-transformers/msmarco-co-condenser-margin-mse-sym-mnrl-mean-v1", "triplet", split="train")
        msmarco_dataset_dict = msmarco_dataset.train_test_split(test_size=10_000, seed=12)
        msmarco_train_dataset: Dataset = msmarco_dataset_dict["train"]
        msmarco_eval_dataset: Dataset = msmarco_dataset_dict["test"]
        print("msmarco数据集加载完成。")

        print("正在加载squad数据集...")
        squad_dataset = load_dataset("sentence-transformers/squad", split="train")
        squad_dataset_dict = squad_dataset.train_test_split(test_size=10_000, seed=12)
        squad_train_dataset: Dataset = squad_dataset_dict["train"]
        squad_eval_dataset: Dataset = squad_dataset_dict["test"]
        print("squad数据集加载完成。")

        print("正在加载s2orc数据集...")
        s2orc_dataset = load_dataset("sentence-transformers/s2orc", "title-abstract-pair", split="train[:100000]")
        s2orc_dataset_dict = s2orc_dataset.train_test_split(test_size=10_000, seed=12)
        s2orc_train_dataset: Dataset = s2orc_dataset_dict["train"]
        s2orc_eval_dataset: Dataset = s2orc_dataset_dict["test"]
        print("s2orc数据集加载完成。")

        print("正在加载allnli数据集...")
        allnli_train_dataset = load_dataset("sentence-transformers/all-nli", "triplet", split="train")
        allnli_eval_dataset = load_dataset("sentence-transformers/all-nli", "triplet", split="dev")
        print("allnli数据集加载完成。")

        print("正在加载paq数据集...")
        paq_dataset = load_dataset("sentence-transformers/paq", split="train")
        paq_dataset_dict = paq_dataset.train_test_split(test_size=10_000, seed=12)
        paq_train_dataset: Dataset = paq_dataset_dict["train"]
        paq_eval_dataset: Dataset = paq_dataset_dict["test"]
        print("paq数据集加载完成。")

        print("正在加载trivia_qa数据集...")
        trivia_qa = load_dataset("sentence-transformers/trivia-qa", split="train")
        trivia_qa_dataset_dict = trivia_qa.train_test_split(test_size=5_000, seed=12)
        trivia_qa_train_dataset: Dataset = trivia_qa_dataset_dict["train"]
        trivia_qa_eval_dataset: Dataset = trivia_qa_dataset_dict["test"]
        print("trivia_qa数据集加载完成。")

        print("正在加载msmarco_10m数据集...")
        msmarco_10m_dataset = load_dataset("bclavie/msmarco-10m-triplets", split="train")
        msmarco_10m_dataset_dict = msmarco_10m_dataset.train_test_split(test_size=10_000, seed=12)
        msmarco_10m_train_dataset: Dataset = msmarco_10m_dataset_dict["train"]
        msmarco_10m_eval_dataset: Dataset = msmarco_10m_dataset_dict["test"]
        print("msmarco_10m数据集加载完成。")

        print("正在加载swim_ir数据集...")
        swim_ir_dataset = load_dataset("nthakur/swim-ir-monolingual", "en", split="train").select_columns(["query", "text"])
        swim_ir_dataset_dict = swim_ir_dataset.train_test_split(test_size=10_000, seed=12)
        swim_ir_train_dataset: Dataset = swim_ir_dataset_dict["train"]
        swim_ir_eval_dataset: Dataset = swim_ir_dataset_dict["test"]
        print("swim_ir数据集加载完成。")

        
        print("正在加载pubmedqa数据集...")
        pubmedqa_dataset = load_dataset("sentence-transformers/pubmedqa", "triplet-20", split="train")
        pubmedqa_dataset_dict = pubmedqa_dataset.train_test_split(test_size=100, seed=12)
        pubmedqa_train_dataset: Dataset = pubmedqa_dataset_dict["train"]
        pubmedqa_eval_dataset: Dataset = pubmedqa_dataset_dict["test"]
        print("pubmedqa数据集加载完成。")

        
        print("正在加载miracl数据集...")
        miracl_dataset = load_dataset("sentence-transformers/miracl", "en-triplet-all", split="train")
        miracl_dataset_dict = miracl_dataset.train_test_split(test_size=10_000, seed=12)
        miracl_train_dataset: Dataset = miracl_dataset_dict["train"]
        miracl_eval_dataset: Dataset = miracl_dataset_dict["test"]
        print("miracl数据集加载完成。")

        
        print("正在加载mldr数据集...")
        mldr_dataset = load_dataset("sentence-transformers/mldr", "en-triplet-all", split="train")
        mldr_dataset_dict = mldr_dataset.train_test_split(test_size=10_000, seed=12)
        mldr_train_dataset: Dataset = mldr_dataset_dict["train"]
        mldr_eval_dataset: Dataset = mldr_dataset_dict["test"]
        print("mldr数据集加载完成。")

        
        print("正在加载mr_tydi数据集...")
        mr_tydi_dataset = load_dataset("sentence-transformers/mr-tydi", "en-triplet-all", split="train")
        mr_tydi_dataset_dict = mr_tydi_dataset.train_test_split(test_size=10_000, seed=12)
        mr_tydi_train_dataset: Dataset = mr_tydi_dataset_dict["train"]
        mr_tydi_eval_dataset: Dataset = mr_tydi_dataset_dict["test"]
        print("mr_tydi数据集加载完成。")

        train_dataset = DatasetDict({
            "gooaq": gooaq_train_dataset,
            "msmarco": msmarco_train_dataset,
            "squad": squad_train_dataset,
            "s2orc": s2orc_train_dataset,
            "allnli": allnli_train_dataset,
            "paq": paq_train_dataset,
            "trivia_qa": trivia_qa_train_dataset,
            "msmarco_10m": msmarco_10m_train_dataset,
            "swim_ir": swim_ir_train_dataset,
            "pubmedqa": pubmedqa_train_dataset,
            "miracl": miracl_train_dataset,
            "mldr": mldr_train_dataset,
            "mr_tydi": mr_tydi_train_dataset,
        })
        eval_dataset = DatasetDict({
            "gooaq": gooaq_eval_dataset,
            "msmarco": msmarco_eval_dataset,
            "squad": squad_eval_dataset,
            "s2orc": s2orc_eval_dataset,
            "allnli": allnli_eval_dataset,
            "paq": paq_eval_dataset,
            "trivia_qa": trivia_qa_eval_dataset,
            "msmarco_10m": msmarco_10m_eval_dataset,
            "swim_ir": swim_ir_eval_dataset,
            "pubmedqa": pubmedqa_eval_dataset,
            "miracl": miracl_eval_dataset,
            "mldr": mldr_eval_dataset,
            "mr_tydi": mr_tydi_eval_dataset,
        })

        train_dataset.save_to_disk("datasets/train_dataset")
        eval_dataset.save_to_disk("datasets/eval_dataset")
        
        
        quit()
    

def main():
    
    static_embedding = StaticEmbedding(AutoTokenizer.from_pretrained("google-bert/bert-base-uncased"), embedding_dim=1024)
    model = SentenceTransformer(
        modules=[static_embedding],
        model_card_data=SentenceTransformerModelCardData(
            language="en",
            license="apache-2.0",
            model_name="使用BERT未分词分词器在各种数据集上微调的静态嵌入",
        ),
    )

    
    train_dataset, eval_dataset = load_train_eval_datasets()
    print(train_dataset)

    
    loss = MultipleNegativesRankingLoss(model)
    loss = MatryoshkaLoss(model, loss, matryoshka_dims=[32, 64, 128, 256, 512, 1024])

    
    run_name = "static-retrieval-mrl-en-v1"
    args = SentenceTransformerTrainingArguments(
        
        output_dir=f"models/{run_name}",
        
        num_train_epochs=1,
        per_device_train_batch_size=2048,
        per_device_eval_batch_size=2048,
        learning_rate=2e-1,
        warmup_ratio=0.1,
        fp16=False,  
        bf16=True,  
        batch_sampler=BatchSamplers.NO_DUPLICATES,  
        multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL,
        
        eval_strategy="steps",
        eval_steps=250,
        save_strategy="steps",
        save_steps=250,
        save_total_limit=2,
        logging_steps=250,
        logging_first_step=True,
        run_name=run_name,  
    )

    
    evaluator = NanoBEIREvaluator()
    evaluator(model)
```

```python
trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss=loss,
        evaluator=evaluator,
    )
    trainer.train()

    
    evaluator(model)

    
    model.save_pretrained(f"models/{run_name}/final")

    
    model.push_to_hub(run_name, private=True)

if __name__ == "__main__":
    main()

```

该脚本在训练17.8小时后生成了`sentence-transformers/static-retrieval-mrl-en-v1`。总共消耗了2.6千瓦时能量，排放了1千克二氧化碳。这大致相当于一个普通人每天呼出的二氧化碳量。

请参阅我们的Weights and Biases报告，了解训练期间收集的训练和评估指标。

```python
import random
import logging
from datasets import load_dataset, Dataset, DatasetDict
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
    SentenceTransformerModelCardData,
)
from sentence_transformers.losses import MatryoshkaLoss, MultipleNegativesRankingLoss
from sentence_transformers.training_args import BatchSamplers, MultiDatasetBatchSamplers
from sentence_transformers.models.StaticEmbedding import StaticEmbedding

from transformers import AutoTokenizer

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)
random.seed(12)


def load_train_eval_datasets():
    """
    从磁盘加载训练和评估数据集，或从datasets库加载并保存到磁盘。

    保存到磁盘后，我们执行quit()以确保数据集在训练前不会加载到内存中。
    """
    try:
        train_dataset = DatasetDict.load_from_disk("datasets/train_dataset")
        eval_dataset = DatasetDict.load_from_disk("datasets/eval_dataset")
        return train_dataset, eval_dataset
    except FileNotFoundError:
        print("正在加载wikititles数据集...")
        wikititles_dataset = load_dataset("sentence-transformers/parallel-sentences-wikititles", split="train")
        wikititles_dataset_dict = wikititles_dataset.train_test_split(test_size=10_000, seed=12)
        wikititles_train_dataset: Dataset = wikititles_dataset_dict["train"]
        wikititles_eval_dataset: Dataset = wikititles_dataset_dict["test"]
        print("已加载wikititles数据集。")

        print("正在加载tatoeba数据集...")
        tatoeba_dataset = load_dataset("sentence-transformers/parallel-sentences-tatoeba", "all", split="train")
        tatoeba_dataset_dict = tatoeba_dataset.train_test_split(test_size=10_000, seed=12)
        tatoeba_train_dataset: Dataset = tatoeba_dataset_dict["train"]
        tatoeba_eval_dataset: Dataset = tatoeba_dataset_dict["test"]
        print("已加载tatoeba数据集。")

        print("正在加载talks数据集...")
        talks_dataset = load_dataset("sentence-transformers/parallel-sentences-talks", "all", split="train")
        talks_dataset_dict = talks_dataset.train_test_split(test_size=10_000, seed=12)
        talks_train_dataset: Dataset = talks_dataset_dict["train"]
        talks_eval_dataset: Dataset = talks_dataset_dict["test"]
        print("已加载talks数据集。")

        print("正在加载europarl数据集...")
        europarl_dataset = load_dataset("sentence-transformers/parallel-sentences-europarl", "all", split="train[:5000000]")
        europarl_dataset_dict = europarl_dataset.train_test_split(test_size=10_000, seed=12)
        europarl_train_dataset: Dataset = europarl_dataset_dict["train"]
        europarl_eval_dataset: Dataset = europarl_dataset_dict["test"]
        print("已加载europarl数据集。")

        print("正在加载global voices数据集...")
        global_voices_dataset = load_dataset("sentence-transformers/parallel-sentences-global-voices", "all", split="train")
        global_voices_dataset_dict = global_voices_dataset.train_test_split(test_size=10_000, seed=12)
        global_voices_train_dataset: Dataset = global_voices_dataset_dict["train"]
        global_voices_eval_dataset: Dataset = global_voices_dataset_dict["test"]
        print("已加载global voices数据集。")

        print("正在加载jw300数据集...")
        jw300_dataset = load_dataset("sentence-transformers/parallel-sentences-jw300", "all", split="train")
        jw300_dataset_dict = jw300_dataset.train_test_split(test_size=10_000, seed=12)
        jw300_train_dataset: Dataset = jw300_dataset_dict["train"]
        jw300_eval_dataset: Dataset = jw300_dataset_dict["test"]
        print("已加载jw300数据集。")

        print("正在加载muse数据集...")
        muse_dataset = load_dataset("sentence-transformers/parallel-sentences-muse", split="train")
        muse_dataset_dict = muse_dataset.train_test_split(test_size=10_000, seed=12)
        muse_train_dataset: Dataset = muse_dataset_dict["train"]
        muse_eval_dataset: Dataset = muse_dataset_dict["test"]
        print("已加载muse数据集。")

        print("正在加载wikimatrix数据集...")
        wikimatrix_dataset = load_dataset("sentence-transformers/parallel-sentences-wikimatrix", "all", split="train")
        wikimatrix_dataset_dict = wikimatrix_dataset.train_test_split(test_size=10_000, seed=12)
        wikimatrix_train_dataset: Dataset = wikimatrix_dataset_dict["train"]
        wikimatrix_eval_dataset: Dataset = wikimatrix_dataset_dict["test"]
        print("已加载wikimatrix数据集。")

        print("正在加载opensubtitles数据集...")
        opensubtitles_dataset = load_dataset("sentence-transformers/parallel-sentences-opensubtitles", "all", split="train[:5000000]")
        opensubtitles_dataset_dict = opensubtitles_dataset.train_test_split(test_size=10_000, seed=12)
        opensubtitles_train_dataset: Dataset = opensubtitles_dataset_dict["train"]
        opensubtitles_eval_dataset: Dataset = opensubtitles_dataset_dict["test"]
        print("已加载opensubtitles数据集。")

        print("正在加载stackexchange数据集...")
        stackexchange_dataset = load_dataset("sentence-transformers/stackexchange-duplicates", "post-post-pair", split="train")
        stackexchange_dataset_dict = stackexchange_dataset.train_test_split(test_size=10_000, seed=12)
        stackexchange_train_dataset: Dataset = stackexchange_dataset_dict["train"]
        stackexchange_eval_dataset: Dataset = stackexchange_dataset_dict["test"]
        print("已加载stackexchange数据集。")

        print("正在加载quora数据集...")
        quora_dataset = load_dataset("sentence-transformers/quora-duplicates", "triplet", split="train")
        quora_dataset_dict = quora_dataset.train_test_split(test_size=10_000, seed=12)
        quora_train_dataset: Dataset = quora_dataset_dict["train"]
        quora_eval_dataset: Dataset = quora_dataset_dict["test"]
        print("已加载quora数据集。")

        print("正在加载wikianswers duplicates数据集...")
        wikianswers_duplicates_dataset = load_dataset("sentence-transformers/wikianswers-duplicates", split="train[:10000000]")
        wikianswers_duplicates_dict = wikianswers_duplicates_dataset.train_test_split(test_size=10_000, seed=12)
        wikianswers_duplicates_train_dataset: Dataset = wikianswers_duplicates_dict["train"]
        wikianswers_duplicates_eval_dataset: Dataset = wikianswers_duplicates_dict["test"]
        print("已加载wikianswers duplicates数据集。")

        print("正在加载all nli数据集...")
        all_nli_train_dataset = load_dataset("sentence-transformers/all-nli", "triplet", split="train")
        all_nli_eval_dataset = load_dataset("sentence-transformers/all-nli", "triplet", split="dev")
        print("已加载all nli数据集。")
```

print("正在加载简单维基数据集...")
        simple_wiki_dataset = load_dataset("sentence-transformers/simple-wiki", split="train")
        simple_wiki_dataset_dict = simple_wiki_dataset.train_test_split(test_size=10_000, seed=12)
        simple_wiki_train_dataset: Dataset = simple_wiki_dataset_dict["train"]
        simple_wiki_eval_dataset: Dataset = simple_wiki_dataset_dict["test"]
        print("已加载简单维基数据集。")

        print("正在加载AltLex数据集...")
        altlex_dataset = load_dataset("sentence-transformers/altlex", split="train")
        altlex_dataset_dict = altlex_dataset.train_test_split(test_size=10_000, seed=12)
        altlex_train_dataset: Dataset = altlex_dataset_dict["train"]
        altlex_eval_dataset: Dataset = altlex_dataset_dict["test"]
        print("已加载AltLex数据集。")

        print("正在加载Flickr30k描述数据集...")
        flickr30k_captions_dataset = load_dataset("sentence-transformers/flickr30k-captions", split="train")
        flickr30k_captions_dataset_dict = flickr30k_captions_dataset.train_test_split(test_size=10_000, seed=12)
        flickr30k_captions_train_dataset: Dataset = flickr30k_captions_dataset_dict["train"]
        flickr30k_captions_eval_dataset: Dataset = flickr30k_captions_dataset_dict["test"]
        print("已加载Flickr30k描述数据集。")

        print("正在加载COCO描述数据集...")
        coco_captions_dataset = load_dataset("sentence-transformers/coco-captions", split="train")
        coco_captions_dataset_dict = coco_captions_dataset.train_test_split(test_size=10_000, seed=12)
        coco_captions_train_dataset: Dataset = coco_captions_dataset_dict["train"]
        coco_captions_eval_dataset: Dataset = coco_captions_dataset_dict["test"]
        print("已加载COCO描述数据集。")

        print("正在加载用于SimCSE的NLI数据集...")
        nli_for_simcse_dataset = load_dataset("sentence-transformers/nli-for-simcse", "triplet", split="train")
        nli_for_simcse_dataset_dict = nli_for_simcse_dataset.train_test_split(test_size=10_000, seed=12)
        nli_for_simcse_train_dataset: Dataset = nli_for_simcse_dataset_dict["train"]
        nli_for_simcse_eval_dataset: Dataset = nli_for_simcse_dataset_dict["test"]
        print("已加载用于SimCSE的NLI数据集。")

        print("正在加载否定数据集...")
        negation_dataset = load_dataset("jinaai/negation-dataset", split="train")
        negation_dataset_dict = negation_dataset.train_test_split(test_size=100, seed=12)
        negation_train_dataset: Dataset = negation_dataset_dict["train"]
        negation_eval_dataset: Dataset = negation_dataset_dict["test"]
        print("已加载否定数据集。")

        train_dataset = DatasetDict({
            "wikititles": wikititles_train_dataset,
            "tatoeba": tatoeba_train_dataset,
            "talks": talks_train_dataset,
            "europarl": europarl_train_dataset,
            "global_voices": global_voices_train_dataset,
            "jw300": jw300_train_dataset,
            "muse": muse_train_dataset,
            "wikimatrix": wikimatrix_train_dataset,
            "opensubtitles": opensubtitles_train_dataset,
            "stackexchange": stackexchange_train_dataset,
            "quora": quora_train_dataset,
            "wikianswers_duplicates": wikianswers_duplicates_train_dataset,
            "all_nli": all_nli_train_dataset,
            "simple_wiki": simple_wiki_train_dataset,
            "altlex": altlex_train_dataset,
            "flickr30k_captions": flickr30k_captions_train_dataset,
            "coco_captions": coco_captions_train_dataset,
            "nli_for_simcse": nli_for_simcse_train_dataset,
            "negation": negation_train_dataset,
        })
        eval_dataset = DatasetDict({
            "wikititles": wikititles_eval_dataset,
            "tatoeba": tatoeba_eval_dataset,
            "talks": talks_eval_dataset,
            "europarl": europarl_eval_dataset,
            "global_voices": global_voices_eval_dataset,
            "jw300": jw300_eval_dataset,
            "muse": muse_eval_dataset,
            "wikimatrix": wikimatrix_eval_dataset,
            "opensubtitles": opensubtitles_eval_dataset,
            "stackexchange": stackexchange_eval_dataset,
            "quora": quora_eval_dataset,
            "wikianswers_duplicates": wikianswers_duplicates_eval_dataset,
            "all_nli": all_nli_eval_dataset,
            "simple_wiki": simple_wiki_eval_dataset,
            "altlex": altlex_eval_dataset,
            "flickr30k_captions": flickr30k_captions_eval_dataset,
            "coco_captions": coco_captions_eval_dataset,
            "nli_for_simcse": nli_for_simcse_eval_dataset,
            "negation": negation_eval_dataset,
        })

        train_dataset.save_to_disk("datasets/train_dataset")
        eval_dataset.save_to_disk("datasets/eval_dataset")
        
        
        quit()

def main():
    
    static_embedding = StaticEmbedding(AutoTokenizer.from_pretrained("google-bert/bert-base-multilingual-uncased"), embedding_dim=1024)
    model = SentenceTransformer(
        modules=[static_embedding],
        model_card_data=SentenceTransformerModelCardData(
            license="apache-2.0",
            model_name="基于BERT多语言未分词分词器并在多种数据集上微调的静态嵌入",
        ),
    )

    
    train_dataset, eval_dataset = load_train_eval_datasets()
    print(train_dataset)

    
    loss = MultipleNegativesRankingLoss(model)
    loss = MatryoshkaLoss(model, loss, matryoshka_dims=[32, 64, 128, 256, 512, 1024])

    
    run_name = "static-similarity-mrl-multilingual-v1"
    args = SentenceTransformerTrainingArguments(
        
        output_dir=f"models/{run_name}",
        
        num_train_epochs=1,
        per_device_train_batch_size=2048,
        per_device_eval_batch_size=2048,
        learning_rate=2e-1,
        warmup_ratio=0.1,
        fp16=False,  
        bf16=True,  
        batch_sampler=BatchSamplers.NO_DUPLICATES,  
        multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL,
        
        eval_strategy="steps",
        eval_steps=1000,
        save_strategy="steps",
        save_steps=1000,
        save_total_limit=2,
        logging_steps=1000,
        logging_first_step=True,
        run_name=run_name,  
    )

    
    trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss=loss,
    )
    trainer.train()

    
    model.save_pretrained(f"models/{run_name}/final")

    
    model.push_to_hub(run_name, private=True)

if __name__ == "__main__":
    main()

```

该脚本在训练3.1小时后生成了`sentence-transformers/static-similarity-mrl-multilingual-v1`。总共消耗了0.5千瓦时的能源，排放了0.2千克的二氧化碳。这大约相当于普通人每天呼出二氧化碳量的20%。

请参阅我们的Weights and Biases报告，了解训练过程中收集的训练和评估损失。

## 使用方法

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")

```python
sentences = [
    '钆弗塞特增强颈动脉MR血管成像：稳态成像能否提高首过成像的准确性？',
    '以数字减影血管造影（DSA）为参考标准，评估钆弗塞特增强磁共振（MR）血管成像在颈动脉狭窄评估中的诊断准确性，并确定解读首过、稳态及"联合"（首过加稳态）MR血管成像的价值。',
    '在一项纵向研究中，我们通过应用钆氟平M（Gf）增强磁共振成像（MRI）在实验性自身免疫性脑脊髓炎（多发性硬化的动物模型）中，研究了神经炎症期间CVO的体内变化。在过继转移蛋白脂质蛋白特异性T细胞后，使用钆喷酸葡胺（Gd-DTPA）和Gf增强MRI监测SJL/J小鼠。分别计算不同CVO的平均Gf强度比，并与临床病程进行关联。随后，在相应的组织切片中评估荧光标记Gf的组织分布以及细胞炎症的程度。',
]
embeddings = model.encode(sentences)
print(embeddings.shape)



similarities = model.similarity(embeddings[0], embeddings[1:])
print(similarities)


```

接下来的`性能 > 英文检索`部分将显示，这些结果相当可靠，与常用的基于Transformer的编码器模型（如`all-mpnet-base-v2`）相比，误差在15%以内。

- SentenceTransformer API参考。
- SentenceTransformer.encode API参考。
- SentenceTransformer.similarity API参考。

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/static-similarity-mrl-multilingual-v1", device="cpu")

sentences = [
    '它以干红辣椒粉而闻名。',
    '它以干红辣椒粉而受欢迎。',
    '这些怪物会成群结队地移动。',
]
embeddings = model.encode(sentences)
print(embeddings.shape)



similarities = model.similarity(embeddings, embeddings)
print(similarities)




```

与流行但速度慢得多的`multilingual-e5-small`相比，该模型仅损失约8%的性能，如接下来的`性能 > 多语言相似度`部分所示。

- SentenceTransformer API参考。
- SentenceTransformer.encode API参考。
- SentenceTransformer.similarity API参考。

### 俄罗斯套娃维度截断

要降低计算出的嵌入的维度，只需传递`truncate_dim`参数即可。这适用于所有Sentence Transformer模型。

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/static-retrieval-mrl-en-v1",
    device="cpu",
    truncate_dim=256,
)

sentences = [
    '钆弗塞特增强颈动脉MR血管成像：稳态成像能否提高首过成像的准确性？',
    '以数字减影血管造影（DSA）为参考标准，评估钆弗塞特增强磁共振（MR）血管成像在颈动脉狭窄评估中的诊断准确性，并确定解读首过、稳态及"联合"（首过加稳态）MR血管成像的价值。',
    '在一项纵向研究中，我们通过应用钆氟平M（Gf）增强磁共振成像（MRI）在实验性自身免疫性脑脊髓炎（多发性硬化的动物模型）中，研究了神经炎症期间CVO的体内变化。在过继转移蛋白脂质蛋白特异性T细胞后，使用钆喷酸葡胺（Gd-DTPA）和Gf增强MRI监测SJL/J小鼠。分别计算不同CVO的平均Gf强度比，并与临床病程进行关联。随后，在相应的组织切片中评估荧光标记Gf的组织分布以及细胞炎症的程度。',
]
embeddings = model.encode(sentences)
print(embeddings.shape)



similarities = model.similarity(embeddings[0], embeddings[1:])
print(similarities)


```

### 第三方库

该模型也可在各种第三方库中直接使用，例如LangChain、LlamaIndex、Haystack和txtai。

#### LangChain

```python

from langchain_huggingface import HuggingFaceEmbeddings

model_name = "sentence-transformers/static-retrieval-mrl-en-v1"
model_kwargs = {'device': 'cpu'} 
model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
)

```

- HuggingFaceEmbeddings文档。

#### LlamaIndex

```python

from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


model_name = "sentence-transformers/static-retrieval-mrl-en-v1"
device = "cpu"
embed_model = HuggingFaceEmbedding(
    model_name=model_name,
    device=device,
    
)
Settings.embed_model = embed_model

```

- HuggingFaceEmbedding文档及API参考。

#### Haystack

```python

from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)

model_name = "sentence-transformers/static-retrieval-mrl-en-v1"
device = "cpu"
document_embedder = SentenceTransformersDocumentEmbedder(
    model=model_name,
    device=device,
    
)
text_embedder = SentenceTransformersTextEmbedder(
    model=model_name,
    device=device,
    
)

```

- SentenceTransformersDocumentEmbedder文档。
- SentenceTransformersTextEmbedder文档。

#### txtai

```python

from txtai import Embeddings

model_name = "sentence-transformers/static-retrieval-mrl-en-v1"
embeddings = Embeddings(path=model_name)

```

- Embeddings文档

## 性能

训练完成后，我们在NanoBEIR（标准维度和俄罗斯套娃维度）以及BEIR上评估了最终模型`sentence-transformers/static-retrieval-mrl-en-v1`。

#### NanoBEIR

我们在NanoBEIR上评估了`sentence-transformers/static-retrieval-mrl-en-v1`，并将其与在我们的硬件上计算的推理速度进行了对比绘图。在推理速度测试中，我们计算了GooAQ数据集每秒处理的查询嵌入数量，分别在CPU或GPU上进行。

我们针对3类模型进行评估：

1. 基于注意力的密集嵌入模型，例如传统的Sentence Transformer模型，如`all-mpnet-base-v2`、`bge-base-en-v1.5`和`gte-large-en-v1.5`。
2. 基于静态嵌入的模型，例如`static-retrieval-mrl-en-v1`、`potion-base-8M`、`M2V_base_output`和`glove.6B.300d`。
3. 稀疏词袋模型BM25，通常是一个强基线。点击展开BM25实现细节我们依赖于高效的`bm25s`实现，在分词和词干提取（使用英语PyStemmer）后，对Token使用`model.get_scores()`。

基于注意力的密集嵌入模型，例如传统的Sentence Transformer模型，如`all-mpnet-base-v2`、`bge-base-en-v1.5`和`gte-large-en-v1.5`。

基于静态嵌入的模型，例如`static-retrieval-mrl-en-v1`、`potion-base-8M`、`M2V_base_output`和`glove.6B.300d`。

稀疏词袋模型BM25，通常是一个强基线。

我们依赖于高效的`bm25s`实现，在分词和词干提取（使用英语PyStemmer）后，对Token使用`model.get_scores()`。

注意：许多基于注意力的密集嵌入模型在(Nano)BEIR评估数据集的训练集上进行了微调。这使这些模型在此基准测试中获得了不公平的优势，并可能导致在实际检索任务中下游性能降低。

`static-retrieval-mrl-en-v1`特意未在任何这些数据集上进行训练。

- *: 对于7B LLM，我们没有进行推理实验，因为它们的推理速度在图中将接近于0。
- 我们进行了实验以确定每个模型的最佳批量大小。

![NanoBEIR性能与推理速度对比](/images/posts/82949f009288.png)

从这些图中我们可以得出一些显著结论：

1. static-retrieval-mrl-en-v1 在所有静态嵌入模型中表现最佳，超越了 GloVe 或 Model2Vec 等模型。  
2. static-retrieval-mrl-en-v1 是唯一在性能上超越 BM25 的静态嵌入模型。  
3. static-retrieval-mrl-en-v1 的性能达到常用模型 all-mpnet-base-v2 的 87.4%，在 GPU 上速度快 24 倍，在 CPU 上速度快 397 倍。  
4. static-retrieval-mrl-en-v1 在 CPU 上的速度比 GPU 更快：该模型可在各类设备上极速运行，包括消费级 PC、小型服务器、手机或浏览器内。  

- 性能达到常用模型 all-mpnet-base-v2 的 87.4%，  
- 在 GPU 上速度快 24 倍，  
- 在 CPU 上速度快 397 倍。  

#### 套娃评估  

此外，我们通过将输出嵌入截断至更低维度进行套娃式降维，并实验了其对 NanoBEIR 性能的影响。  

![NanoBEIR 性能与套娃降维的关系](/images/posts/7ad9a7376b19.png)  

这些发现表明，将维度降低 2 倍仅导致性能下降 1.47%（NDCG@10 从 0.5031 降至 0.4957），同时检索速度实际提升 2 倍。  

我们还对最终模型 sentence-transformers/static-similarity-mrl-multilingual-v1 在 5 种语言上进行了评估，这些语言在 MTEB 的各类任务中拥有大量基准测试。  

我们重申，该模型并非为检索场景设计，而是在语义文本相似度（STS）、分类和配对分类任务上进行评估。我们将其与优秀且小巧的 multilingual-e5-small 模型进行了对比。  

![MTEB 上的 STS、分类与配对分类](/images/posts/09af2fc0e49e.png)  

在所有被测语言中，static-similarity-mrl-multilingual-v1 相对于 multilingual-e5-small 在 STS 上平均达到 92.3%，在配对分类上达到 95.52%，在分类上达到 86.52%。  

![每秒处理的文本数](/images/posts/d568598c78c8.png)  

为弥补这一性能差距，static-similarity-mrl-multilingual-v1 在 CPU 设备上比 multilingual-e5-small 快约 125 倍，在 GPU 设备上快约 10 倍。由于注意力模型的超线性特性与静态嵌入模型的线性特性，随着待编码 Token 数量的增加，速度优势将进一步扩大。  

最后，我们实验了将输出嵌入截断至更低维度进行套娃式降维对 MTEB 上英文 STS 性能的影响。  

![英文 STS MTEB 性能与套娃降维的关系](/images/posts/f1f0176d3a89.png)  

如图所示，您可以轻松将维度降低 2 倍或 4 倍，而性能损失极小（0.15% 或 0.56%）。若下游任务的速度或存储成本成为瓶颈，此方法可缓解部分问题。  

## 结论  

本文描述了从构思到完成模型的所有步骤，以及两个最终模型（static-retrieval-mrl-en-v1 和 static-similarity-mrl-multilingual-v1）的使用与评估细节。  

评估结果表明：  

- 基于静态嵌入的模型性能可超过常用注意力密集模型的 85%，  
- 基于静态嵌入的模型在 GPU 上实际比 all-mpnet-base-v2 和 multilingual-e5-small 等高效替代方案快 10 至 25 倍，在 CPU 上快 100 至 400 倍，且速度优势随文本长度增加而扩大，  
- 使用套娃损失训练可显著保留下游性能：static-similarity-mrl-multilingual-v1 在英文 STS 上维度缩小 4 倍仅导致性能下降 0.56%，static-retrieval-mrl-en-v1 在英文检索上维度缩小 2 倍仅导致性能下降 1.47%。  

- 维度缩小 4 倍仅导致 static-similarity-mrl-multilingual-v1 在英文 STS 上性能下降 0.56%，  
- 维度缩小 2 倍仅导致 static-retrieval-mrl-en-v1 在英文检索上性能下降 1.47%。  

若您需要用于检索或相似度任务的高效纯 CPU 密集嵌入模型，static-retrieval-mrl-en-v1 和 static-similarity-mrl-multilingual-v1 将以极低成本提供极高性能，且结果惊人地接近基于注意力的密集模型。  

## 后续步骤  

试试看！如果您已在某处使用 Sentence Transformer 模型，欢迎将其替换为 static-retrieval-mrl-en-v1 或 static-similarity-mrl-multilingual-v1。或者，更好的方式是：使用代表您感兴趣任务和语言的数据训练自己的模型。  

此外，关于训练后的模型仍存在一些问题：  

1. 由于基于静态嵌入的模型不受位置嵌入或超线性时间复杂度的限制，它们可以支持任意高的最大序列长度。然而，对于极长文档，大数定律可能会“归一化”所有嵌入，使其不再有用。需要更多实验来确定合适的截断点。目前，我们将最大序列长度、分块等设置交由用户决定。  

由于基于静态嵌入的模型不受位置嵌入或超线性时间复杂度的限制，它们可以支持任意高的最大序列长度。然而，对于极长文档，大数定律可能会“归一化”所有嵌入，使其不再有用。  

需要更多实验来确定合适的截断点。目前，我们将最大序列长度、分块等设置交由用户决定。  

此外，还有多种可能的扩展方向有望提升模型性能，我们乐于留给其他模型作者探索。我们也欢迎合作：  

1. 难负例挖掘：搜索相似但不相关的文本，以增加训练数据难度。  
2. 模型融合：将多个以相同方式训练但使用不同种子或数据分布的模型权重进行组合。  
3. 课程学习：按难度递增的顺序训练样本。  
4. 引导式批次内假负例过滤：通过高效的预训练嵌入模型排除假负例。  
5. 随机权重初始化的种子优化：使用不同种子训练初始步骤，以找到有用的权重初始化。  
6. 分词器重新训练：使用现代文本和知识重新训练分词器。  
7. 梯度缓存：通过 CachedMultipleNegativesRankingLoss 应用 GradCache，支持更大批次，通常带来更优性能。  
8. 模型蒸馏：除了使用监督训练数据，还可将无监督数据输入更大的嵌入模型，并将这些嵌入蒸馏到基于静态嵌入的学生模型中。  

## 相关博文  

关于训练其他 Sentence Transformer 模型类型，或可与静态嵌入叠加的效率技术：  

- 使用 Sentence Transformers 训练和微调嵌入模型：双编码器嵌入模型的通用训练指南；本文中的静态方案是其特例。  
- 使用 Sentence Transformers 训练和微调重排序模型：交叉编码器训练；是静态检索器之上的自然第二阶段。  
- 使用 Sentence Transformers 训练和微调稀疏嵌入模型：SPLADE 训练；在混合设置中与静态密集检索互补。  
- 使用 Sentence Transformers 的多模态嵌入与重排序模型，以及训练和微调多模态嵌入与重排序模型：文本+图像+音频+视频模型的推理与训练。  
- 🪆 套娃嵌入模型介绍：本文所用套娃损失的背景，支持静态嵌入的截断。  
- 二进制与标量嵌入量化：实现显著更快的检索与更低成本：训练后压缩，可与本文展示的速度优势叠加。  

## 致谢

我要感谢The Minish Lab的Stéphan Tulkens和Thomas van Dongen，他们通过Model2Vec的工作让我关注到静态嵌入模型。此外，我还要感谢Vaibhav Srivastav和Pedro Cuenca对这篇博文的协助，以及Antoine Chaffin在发布检查点方面的头脑风暴。

最后，衷心感谢所有致力于嵌入模型、数据集和开源Python包的研究人员。你们夯实了整个行业，而我正是站在你们的肩膀上开展工作。希望有一天，你们也能站在我的肩膀上。

---

> 本文由AI自动翻译，原文链接：[Train 400x faster Static Embedding Models with Sentence Transformers](https://huggingface.co/blog/static-embeddings)
> 
> 翻译时间：2026-06-01 06:54
