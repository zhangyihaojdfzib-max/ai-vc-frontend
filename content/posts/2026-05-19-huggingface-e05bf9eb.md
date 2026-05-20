---
title: Ettin重排序模型系列发布
title_original: Introducing the Ettin Reranker Family
date: '2026-05-19'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ettin-reranker
author: ''
summary: 本文介绍了新发布的六款Ettin重排序模型，基于Ettin ModernBERT编码器构建，在各自参数规模上达到业界领先水平。模型采用蒸馏方案训练，利用逐点MSE损失从教师模型学习。文章详细阐述了重排序模型与嵌入模型的区别及检索-重排序的实用模式，提供了模型使用方法、架构细节、在MTEB基准上的性能结果，以及完整的训练方案和脚本，方便用户直接使用或自行训练。
categories:
- AI产品
tags:
- 重排序模型
- CrossEncoder
- Sentence Transformers
- 检索增强
- MTEB
draft: false
translated_at: '2026-05-20T06:11:05.079958'
---

# 介绍 Ettin 重排序模型系列

## 摘要

今天我将发布六款新的 Sentence Transformers CrossEncoder 重排序模型，它们在各自参数规模上均达到业界领先水平，基于 Ettin ModernBERT 编码器构建，同时提供训练数据及完整的训练方案：

- cross-encoder/ettin-reranker-17m-v1
- cross-encoder/ettin-reranker-32m-v1
- cross-encoder/ettin-reranker-68m-v1
- cross-encoder/ettin-reranker-150m-v1
- cross-encoder/ettin-reranker-400m-v1
- cross-encoder/ettin-reranker-1b-v1

这些模型采用蒸馏方案训练：基于 cross-encoder/ettin-reranker-v1-data 上 mixedbread-ai/mxbai-rerank-large-v2 分数的逐点 MSE，该数据集是 lightonai/embeddings-pre-training 的子集，并与 lightonai/embeddings-fine-tuning 的重排序子集混合。

![我们的六款重排序模型搭配 embeddinggemma-300m 在 MTEB(eng, v2) 检索任务上的表现](/images/posts/0a1bc233f8b6.png)

我们的六款重排序模型搭配 google/embeddinggemma-300m 在 MTEB(eng, v2) 检索任务上的表现。更多五种嵌入模型搭配的结果请参见结果部分。

如果您是重排序模型的新手，想先了解"为什么"，请跳转到什么是重排序模型，以及为什么要将其与嵌入模型搭配使用？。如果您只想直接使用模型，请跳转到使用方法。如果您想自行训练，请跳转到训练部分。

我使用 Sentence Transformers v5.5.0 中新增的 train-sentence-transformers Agent 技能引导了以下训练方案。通过 hf skills add train-sentence-transformers [--global] [--claude] 安装，并让您的 AI 编码 Agent（Claude Code、Codex、Cursor、Gemini CLI 等）在您的数据上微调 SentenceTransformer、CrossEncoder 或 SparseEncoder 模型。

- 什么是重排序模型，以及为什么要将其与嵌入模型搭配使用？
- 使用方法——端到端检索-重排序流程
- 架构细节
- 结果——MTEB(eng, v2) 检索速度
- 训练——蒸馏方案数据集训练参数评估完整训练脚本
- 结论
- 致谢

- 端到端检索-重排序流程

- MTEB(eng, v2) 检索
- 速度

- 蒸馏方案
- 数据集
- 训练参数
- 评估
- 完整训练脚本

## 什么是重排序模型，以及为什么要将其与嵌入模型搭配使用？

重排序模型（又称逐点交叉编码器）是一种神经网络模型，它接收一对（查询，文档）并输出单一的相关性分数。与嵌入模型（分别对查询和文档进行编码，然后从两个嵌入向量计算相似度）不同，重排序模型让两个文本在每个 Transformer 层中相互关注。这种联合编码更准确，但也更昂贵：模型必须为每个（查询，文档）对运行一次，而不是每个文本运行一次。

由于交叉编码器在整个语料库上运行成本过高，常见的生产模式是检索-重排序：快速嵌入模型检索前 K 个候选（成本低），然后交叉编码器以高精度仅对这 K 个结果重新排序。总成本保持可控，而最终排序结果更接近穷举交叉编码器通过的结果。

![嵌入模型与重排序模型对比](/images/posts/20f8c91bb9a6.png)

在本博客文章中，我将交替使用"重排序模型"和"交叉编码器"。

## 使用方法

发布的模型是标准的 Sentence Transformers CrossEncoder 模型，因此您只需 3 行代码即可使用：

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ettin-reranker-32m-v1")
scores = model.predict([
    ("苹果公司在哪里成立？", "苹果公司于1976年由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩在加利福尼亚州库比蒂诺成立。"),
    ("苹果公司在哪里成立？", "富士苹果是20世纪30年代末培育、1962年上市的苹果品种。"),
])
print(scores)


```

对于查询和候选列表，您还可以使用 rank 获取排序后的索引和分数：

```python
ranked = model.rank(
    query="哪颗行星被称为红色星球？",
    documents=[
        "金星因其相似的大小和距离常被称为地球的孪生星。",
        "火星因其红色外观而闻名，常被称为红色星球。",
        "木星是太阳系中最大的行星，有一个显著的大红斑。",
        "土星以其光环闻名，有时会被误认为是红色星球。",
    ],
    top_k=4,
    return_documents=True,
)
for r in ranked:
    print(f"({r['score']:.2f}): {r['text']}")





```

您可以将 cross-encoder/ettin-reranker-32m-v1 替换为任何其他尺寸，以在质量与速度之间进行权衡。得益于 ModernBERT 的长上下文预训练，所有六款模型均支持最多 8K Token 的上下文（适用于长文档重排序）。

建议安装 kernels 并设置 model_kwargs={"dtype": "bfloat16", "attn_implementation": "flash_attention_2"} 以获得最高吞吐量。更多详情请参见下方速度部分，但总体而言，与默认加载相比，根据模型大小和序列长度，您可预期获得 1.7 倍至 8.3 倍的速度提升。

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ettin-reranker-32m-v1",
    model_kwargs={"dtype": "bfloat16", "attn_implementation": "flash_attention_2"},
)

```

### 端到端检索-重排序流程

一个完整的示例，使用快速嵌入模型进行检索，使用重排序模型进行最终排序：

```python
from sentence_transformers import SentenceTransformer, CrossEncoder


embedder = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1")
reranker = CrossEncoder("cross-encoder/ettin-reranker-68m-v1")

corpus = [
    "苹果公司于1976年由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩在加利福尼亚州库比蒂诺成立。",
    "富士苹果是20世纪30年代末培育的苹果品种。",
    "史蒂夫·乔布斯于2007年在Macworld上推出了iPhone。",
    "Macintosh电脑从1984年起由苹果公司销售。",
    
]
query = "苹果公司在哪里成立？"


query_emb = embedder.encode_query(query, convert_to_tensor=True)
corpus_emb = embedder.encode_document(corpus, convert_to_tensor=True)
scores = embedder.similarity(query_emb, corpus_emb)[0]
top_k_idx = scores.topk(min(100, len(corpus))).indices.tolist()


top_k_docs = [corpus[i] for i in top_k_idx]
ranked = reranker.rank(query, top_k_docs, top_k=5, return_documents=True)
for r in ranked:
    print(f"({r['score']:.2f}): {r['text']}")





```

这与大多数现代搜索系统使用的模式相同。检索器决定哪些内容进入漏斗，重排序模型决定最终胜出的内容。

## 架构细节

所有六款重排序模型共享相同的架构，仅在其骨干网络大小上有所不同。骨干网络是约翰霍普金斯大学 Ettin 套件中的六款 Ettin 编码器之一。这些是 ModernBERT 风格的模型，具有非填充注意力、RoPE 位置编码、GeGLU 和 2T Token 的开源预训练，支持最多 8192 Token 的上下文。

在每个编码器之上，重排序模型使用一个 4 模块分类头，该分类头模仿 ModernBertForSequenceClassification，但由 Sentence Transformers 的模块化组件构建。底层的 Transformer 是普通的 AutoModel 而非 AutoModelForSequenceClassification，这使我们能够对可变长度输入使用序列解填充以支持 Flash Attention 2。在中长文档序列长度下，根据模型大小，这比 fp32+SDPA 带来 1.7 倍至 8.3 倍的速度提升（完整基准测试请参见速度部分）：

```
1. Transformer(FA2)
2. Pooling(cls)
3. Dense(H, H, bias=False, GELU)
4. LayerNorm(H)
5. Dense(H, 1, scores)

```

在我的消融实验中，CLS 池化优于均值池化。这有点令人惊讶。ModernBERT 仅每三层使用一次全局注意力，其余三分之二使用无法从远处位置到达 CLS 的局部窗口注意力。经验上，这些少量的全局层携带了足够的信号，使 CLS 成为更好的池化选择。

所有六款模型均采用 Apache 2.0 许可证发布，与 Ettin 编码器一致。

## 结果

### MTEB(eng, v2) 检索

我对每个已发布的模型，使用MTEB的两阶段重排序流程，在完整的MTEB（英文，v2）检索基准测试（10个任务，前100名重排序）上进行了评估，将每个重排序器与六个覆盖速度/质量谱系的嵌入模型配对：

下方每个图表中的**虚线仅检索器基线**是需要超越的关键指标。低于该线的任何数值都意味着该重排序器平均而言会损害整个流程：

![MTEB（英文，v2）使用static-retrieval-mrl-en-v1 + 重排序器的检索结果](/images/posts/7666e177ad09.png)

![MTEB（英文，v2）使用all-MiniLM-L6-v2 + 重排序器的检索结果](/images/posts/075451db121c.png)

![MTEB（英文，v2）使用bge-small-en-v1.5 + 重排序器的检索结果](/images/posts/c1d832e55f23.png)

![MTEB（英文，v2）使用nomic-embed-text-v1.5 + 重排序器的检索结果](/images/posts/6d6417c57fc0.png)

![MTEB（英文，v2）使用jina-embeddings-v5-text-small-retrieval + 重排序器的检索结果](/images/posts/22eb8d9478f5.png)

六个嵌入器配对下的平均NDCG@10，按降序排列。我们的六个模型以**粗体**显示，教师模型mixedbread-ai/mxbai-rerank-large-v2以下划线标出。

†上限为max_seq_length=8192（基于Qwen3的4B重排序器在原生上下文长度下无法放入单个H100 80GB）。原生上下文评估的结果可能更高。

NanoBEIR是BEIR的一个快速子集，包含13个数据集，每个数据集使用50个查询，针对最多5000个文档。NanoBEIR是训练期间metric_for_best_model所依据的指标（参见评估部分），也是我用来指导实验的指标。

我发布的最小模型，即我们的17M模型，在MTEB上以大约一半的参数数量，比33M的ms-marco-MiniLM-L12-v2高出+0.051 NDCG@10（0.5576对比0.5066），在NanoBEIR上高出+0.038（0.6746对比0.6369）。32M模型在MTEB上比568M的BAAI/bge-reranker-v2-m3高出+0.025（0.5779对比0.5526），参数差距达17倍。如果你一直在检索-重排序栈中使用某个传统的MiniLM重排序器作为默认选项，那么替换为我们的17M（或32M）模型是一个低风险的直接替代方案，在两个基准测试上都能带来明显的质量提升。

在表格中向上看，我们的150M模型是我在MTEB上测试的600M以下范围内最强的重排序器，以+0.005的优势（0.5994对比0.5940）略微领先最近的Qwen/Qwen3-Reranker-0.6B（596M），并且比所有BAAI bge-reranker变体高出0.03到0.05。68M模型也值得一提：其得分为0.5915，几乎与Qwen3-Reranker-0.6B（0.5940）持平，而参数数量仅为后者的九分之一。

在已发布模型的顶端，我们的1B模型紧密跟随其教师模型。它在MTEB上与1.54B的mxbai-rerank-large-v2的差距在0.0001以内（0.6114对比0.6115），在NanoBEIR上的差距在0.008以内，尽管它是从一个比自己大54%的模型中蒸馏而来。蒸馏有效地缩小了与教师模型的差距，这正是我在本次发布中所期望看到的。

对比中整体最强的重排序器是Qwen/Qwen3-Reranker-4B，MTEB得分为0.6367，比我们的1B模型高出+0.025。要使用当前方案缩小这一差距，可能需要从一个更强的教师模型进行蒸馏（我们的教师模型本身低于Qwen3-Reranker-4B）。对于大多数检索-重排序工作负载，我们的1B模型仅需四分之一的参数（参见速度部分），是更实用的选择。

### 速度

对于重排序器而言，质量数据只占重要性的一半。另一半是其延迟是否适合你从检索到向用户展示结果之间的预算时间。让我介绍一下我的测量结果。

我在单个NVIDIA H100 80GB上，对所有六个已发布模型与十三个公开重排序器（强基线，参数最高约1B）进行了基准测试。查询和文档来自sentence-transformers/natural-questions，并遵循其自然的文档长度分布：大多数NQ答案较短，部分较长。文档被截断至max_length=512，以避免给较旧的模型带来不公平的优势。每个模型使用其支持的最佳注意力实现：架构支持的地方使用Flash Attention 2（BERT、XLM-RoBERTa、ModernBERT、Qwen2），不支持的地方使用SDPA，对于DeBERTa-v2使用eager模式（该架构目前在transformers中既不支持FA2也不支持SDPA）。

对于每个模型，自动批处理搜索从批大小8开始，每次翻倍，直到GPU内存耗尽。在每个批大小下，我运行三次计时测试并保留中位数吞吐量，这样单次不顺利的运行不会影响结果。报告的吞吐量是获胜批大小下的数值。

表1. 吞吐量（每秒处理的对数），全部采用bfloat16格式。我们的六个重排序器以**粗体**显示。

我们的17M模型是整个对比中最快的重排序器，每秒处理7517对。这几乎是ms-marco-MiniLM-L6-v2（3817）的两倍，甚至快于更小的ms-marco-MiniLM-L4-v2（4029）。正如你在之前的MTEB表格中所见，我们的17M模型也比所有MiniLM变体更准确。如果你当前正在运行MiniLM交叉编码器，替换为我们的17M模型只需更改一行代码，即可同时改善延迟和搜索质量。

我们的150M模型是一个更有趣的比较对象，因为恰好有两个架构相同的同行模型，参数同为150M：Alibaba-NLP/gte-reranker-modernbert-base和ibm-granite/granite-embedding-reranker-english-r2。两者都基于相同的ModernBERT-base骨干网络。我们的150M模型每秒处理3237对，而两个同行模型分别为1418和1404，速度差距达2.3倍。

所有三个150M模型都使用Flash Attention 2，但两个同行模型通过AutoModelForSequenceClassification加载，这会导致输入被填充。因此，注意力机制本身运行了FA2内核，但模型的其余部分仍在填充Token上进行密集计算，而这些计算毫无贡献。我们的模块化Transformermodule（参见上文架构细节）将未填充的输入一直传播到整个模型，因此每一层只对真实Token进行计算。这就是获得部分FA2收益与获得全部收益之间的区别。

在表格底部，我们的1B模型达到每秒928对，比1.54B的教师模型mxbai-rerank-large-v2（每秒387对）快2.4倍，同时在MTEB上的得分差距在0.0001以内。教师模型基于Qwen2，每对需要处理提示词模板开销，而蒸馏后的学生模型继承了教师模型的校准和判断能力，但跳过了所有运行时负担。老实说，这是整个发布中我最满意的一个数字。

一个令人遗憾的说明：基于DeBERTa-v2的mxbai-rerank-{xsmall,base,large}-v1系列最终比表格中其他模型慢得多，因为DeBERTa-v2目前在transformers中既不支持Flash Attention 2也不支持SDPA。70M的mxbai-rerank-xsmall-v1每秒处理2636对，在参数数量几乎相同的情况下，吞吐量约为我们68M模型的一半。这些模型本身完全没问题，只是无法使用现代的注意力内核。

如果你是自托管在消费级显卡而非数据中心GPU上，以下是同一吞吐量测试在RTX 3090上的结果。基准测试设置与表1相同：bfloat16格式，每个模型使用最佳支持的注意力机制，在可容纳的最大批大小下进行三次测试取中位数吞吐量。

我们的17M模型仍然是表格中最快的模型，每秒处理9008对，实际上高于其在H100上的数值，这表明在极小模型规模下，原始计算能力并非瓶颈，H100的额外算力无法体现。表格中间部分的排名略有变化，MiniLM重排序器超过了我们的32M和68M模型，而1B模型落后于mxbai-rerank-base-v2（189对比221对每秒）。我们的150M模型仍然对两个基于150M ModernBERT的同行保持明显领先优势，教师模型替代方案依然成立，我们的1B模型吞吐量是1.5B mxbai-rerank-large-v2的2.7倍（189对比69对每秒）。

在CPU上，我们无法利用bf16、Flash Attention 2或去填充（unpadding）的优势，因此延迟情况相对简单：参数量越高，模型速度越慢。17M模型明显快于ms-marco-MiniLM-L6-v2（每秒267.4对 vs 143.9对），甚至比更小的ms-marco-MiniLM-L4-v2（每秒206.2对）还要快。正如预期，由于不再使用去填充，我们的150M模型与两个150M同类模型表现相当（每秒14.0对 vs 14.5对和14.7对）。如果你受限于CPU，我们的17M和32M模型是实用的选择。

为了解释速度的来源，下表使用相同的基准配置，对我们的六个模型进行了fp32+SDPA、bf16+SDPA和bf16+FA2的对比测试。FA2列分为两部分：一部分输入仍带有填充（封装模型所看到的情况），另一部分输入无填充（我们的模块化Transformer实际执行的情况）。最右侧列是我们的模型在启用FA2时的默认配置。

表2. 在自然NQ文档上，max_length=512时，六个发布规模的精度与注意力消融实验。每个单元格显示每秒处理的对数，括号内为相对于fp32+SDPA的倍数，第二行为峰值GPU内存。最右侧列（加粗）是我们的模型在启用FA2时的默认配置。

从fp32+SDPA基线到bf16+FA2（无填充）的总加速比随模型规模急剧增长，从17M模型的1.71倍到1B模型的8.26倍。其中大部分增长来自bf16本身：从fp32+SDPA到bf16+SDPA这一步，17M模型仅获得1.03倍加速，而1B模型则获得5.60倍加速，这也是由于内存成本降低使得批量大小可以更大。简而言之，bfloat16是整体加速的最大单一贡献因素。

出乎意料的是，在输入仍带有填充的情况下启用FA2，实际上比所有发布规模的bf16+SDPA都要慢。FA2内核偏好无填充格式，当你输入带填充的数据时，需要支付格式转换的记账开销，同时仍然在填充Token上消耗计算资源。因此，bf16+FA2（带填充）列大致相当于你在model_kwargs中将sdpa替换为flash_attention_2而不改变模型加载器其他任何设置时所测得的结果。这正是表1中gte-reranker-modernbert-base和granite-embedding-reranker-english-r2所处的状况。

最后，从bf16+FA2（带填充）到bf16+FA2（无填充），额外吞吐量提升在1.78倍（1B模型）到2.45倍（68M模型）之间，同时显著降低了峰值内存，从而允许更大的批量大小。

因此，我的建议很简单：同时启用bf16和FA2。六个Ettin重排序器默认使用无填充输入，因为架构细节部分的模块化Transformer模块正是为此设计的。完整代码片段与上述使用部分相同：

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ettin-reranker-150m-v1",
    model_kwargs={
        "dtype": "bfloat16",
        "attn_implementation": "flash_attention_2",  
    },
)

```

使用pip install kernels安装FA2。它提供了适用于多种GPU架构、CUDA版本和操作系统的预编译内核。

其他CrossEncoder的一个注意事项：只有像Ettin重排序器这样使用模块化Transformer构建的模型才能获得完整的加速效果。将相同的两个标志应用于通过AutoModelForSequenceClassification加载的CrossEncoder，最终会落入表2中较慢的bf16+FA2（带填充）列。

## 训练

以下训练脚本最初来自Sentence Transformers v5.5.0中新增的train-sentence-transformers Agent Skill的输出。如果你使用AI编码Agent（Claude Code、Codex、Cursor、Gemini CLI等），可以安装该技能并让它根据你的数据微调SentenceTransformer、CrossEncoder或SparseEncoder模型。该技能包含针对基础模型选择、损失函数和评估器选择、难负例挖掘、蒸馏、LoRA、Matryoshka、多语言训练和静态嵌入的版本感知指导，以及每种模型类型的模板脚本。

```bash
hf skills add train-sentence-transformers --claude   
hf skills add train-sentence-transformers --global   

```

像"Fine-tune a cross-encoder reranker on(query, document)pairs from my dataset, mine hard negatives, and push to my Hub repo"这样的提示词将生成一个可运行的脚本，你可以在此基础上迭代。我就是这样开始编写下面这个配方的。

所有六个重排序器都使用相同的单阶段配方进行训练。只有学习率和每设备批量大小因模型规模而异。完整的训练脚本约150行，使用一个已发布的数据集。

该配方在模型规模上经过一次扫描后收敛。每个规模的学习率通过在最终训练数据约15%的子集上进行小规模网格搜索来调整，得到的LR在完整数据运行中直接迁移，无需重新调整。除LR外，无需针对每个规模进行其他调整。

### 蒸馏配方

大多数已发布的重排序器配方使用人工标注的相关性三元组（一个查询、一个正例文档，以及可选的难负例），并分别使用对比损失、逐点损失、成对损失或列表损失，如MultipleNegativesRankingLoss、BinaryCrossEntropyLoss、RankNetLoss或LambdaLoss。例如，请参阅我之前关于使用Sentence Transformers训练和微调重排序器模型的博客文章。

但这种方法存在一些实际和理论上的缺陷。首先，正例需要人工标注，这在多个领域扩展时成本高昂且速度缓慢。其次，模型只能看到有人工标注的那一小部分（查询，文档）对的标签。特别是在难负例挖掘之后，最终会出现大量假负例，例如在《难负例，难教训》中所示。第三，这种标注的二元性不符合现实情况，因为有些文档只是比其他文档更相关。

我在这里采取了不同的路线：从现有的强教师重排序器进行逐点MSE蒸馏。这个设置简单到可以用三行描述：

- 教师模型：mixedbread-ai/mxbai-rerank-large-v2（1.54B参数）。
- 损失函数：对原始教师logits（范围约[−12, 22]）使用MSELoss，即不进行重新缩放。
- 训练数据：约1.43亿个（查询，文档，教师分数）三元组。

### 数据集

我已将训练数据作为一个单独的Hugging Face数据集发布：cross-encoder/ettin-reranker-v1-data，由两个来源组合而成。每个来源保留为独立的分割，以便来源透明：

1. LightOn预训练数据（lightonai/embeddings-pre-training，非精选）：32个分割，涵盖广泛领域的文本相似性信号（MTP、FW-EDU、Reddit、PAQ、S2ORC、Amazon、Wikipedia、MS MARCO等）。我对某些分割的样本数量进行了限制，总共产生约1.1亿个（查询，文档，相似度）三元组。
2. 来自lightonai/embeddings-fine-tuning的重新评分检索数据：7个分割（msmarco、hotpotqa、trivia、nq、squadv2、fiqa、fever）。源数据集每个查询最多有2048个候选文档（最初使用Alibaba-NLP/gte-modernbert-base评分），我使用mixedbread-ai/mxbai-rerank-large-v2重新评分并上传为cross-encoder/lightonai-embeddings-fine-tuning-reranked-v1。该数据集使用Jang等人的分位数锚点方法将每个查询的2048个候选文档子采样至256个（所有正例 + 前16个难负例 + 约239个分位数锚点分层样本）。对于训练，我从每个查询的256个候选中选取64个：32个来自按分数排序的头部（正例加上最难的负例），32个中等难度负例从教师排名中更靠后的区间采样。确切排名位置请参阅数据集卡片。

总计：约1.43亿个（查询，文档，分数）三元组，外加一个保留的5K行评估分割（quora的尾部），用于驱动训练过程中的评估损失。

### 训练参数

大多数超参数在不同模型规模间保持不变：

```python
CrossEncoderTrainingArguments(
    num_train_epochs=1,                    
    per_device_train_batch_size=...,       
    gradient_accumulation_steps=1,
    learning_rate=...,                     
    warmup_ratio=0.03,                     
    bf16=True,                             
    eval_strategy="steps",
    eval_steps=0.05,                       
    save_strategy="steps",
    save_steps=0.05,
    save_total_limit=5,
    load_best_model_at_end=True,
    metric_for_best_model="eval_NanoBEIR_R100_mean_ndcg@10",
    seed=12,
)

```

只有学习率和全局批量大小会随模型规模变化。

全局批量大小 = per_device_batch_size × world_size × gradient_accumulation_steps。在单个8-GPU节点上，17m模型的1024全局批量意味着per_device=128。在8个节点上，则意味着per_device=8。训练脚本通过global_batch_size // world_size自动计算per_device_batch_size，因此同一脚本可在任意节点数量下运行。全局批量大小本可以做得更一致，但我发现上述值效果良好，不想仅为了一致性而重新调整它们。

### 评估

我在训练期间监控NanoBEIR平均NDCG@10（每5%步数评估一次），并将其用作load_best_model_at_end的metric_for_best_model。NanoBEIR速度很快，因此我可以在每次训练中评估20次。训练结束后，我在完整的MTEB（英文，v2）检索基准上评估了最佳检查点（根据NanoBEIR）和最后一个检查点。最终发布的检查点是在MTEB上表现最好的那个。NanoBEIR偏好的检查点在所有规模上都胜出，除了68m模型，其最后一个检查点略强。

### 整体训练脚本

完整脚本（每个发布模型都使用该脚本训练）是一个单一文件。每次运行时只需更改ENCODER_SIZE，其他一切自动处理：

```python
from __future__ import annotations

import logging
import os
from pathlib import Path

import torch
import torch.nn as nn
from datasets import concatenate_datasets, get_dataset_config_names, load_dataset

from sentence_transformers import CrossEncoder
from sentence_transformers.base.modules import Dense
from sentence_transformers.cross_encoder import (
    CrossEncoderModelCardData,
    CrossEncoderTrainer,
    CrossEncoderTrainingArguments,
)
from sentence_transformers.cross_encoder.evaluation import CrossEncoderNanoBEIREvaluator
from sentence_transformers.cross_encoder.losses import MSELoss
from sentence_transformers.sentence_transformer.modules import LayerNorm, Pooling, Transformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)



CONFIGS: dict[str, dict] = {
    "17m":  {"base_model_name": "jhu-clsp/ettin-encoder-17m",  "learning_rate": 2.4e-4, "global_batch_size": 1024},
    "32m":  {"base_model_name": "jhu-clsp/ettin-encoder-32m",  "learning_rate": 1.2e-4, "global_batch_size": 512},
    "68m":  {"base_model_name": "jhu-clsp/ettin-encoder-68m",  "learning_rate": 3e-5,   "global_batch_size": 256},
    "150m": {"base_model_name": "jhu-clsp/ettin-encoder-150m", "learning_rate": 1.5e-5, "global_batch_size": 192},
    "400m": {"base_model_name": "jhu-clsp/ettin-encoder-400m", "learning_rate": 7e-6,   "global_batch_size": 256},
    "1b":   {"base_model_name": "jhu-clsp/ettin-encoder-1b",   "learning_rate": 3e-6,   "global_batch_size": 512},
}
ENCODER_SIZE = "17m"

def main() -> None:
    config = CONFIGS[ENCODER_SIZE]
    encoder_id = config["base_model_name"]
    learning_rate = config["learning_rate"]
    global_batch_size = config["global_batch_size"]

    world_size = int(os.environ.get("WORLD_SIZE", 1))
    per_device_batch_size = global_batch_size // world_size
    dataloader_workers = 0 if world_size > 8 else 4
    run_name = f"ettin-reranker-{ENCODER_SIZE}-lr{learning_rate:.0e}"

    
    
    
    
    torch.manual_seed(12)
    transformer = Transformer(encoder_id, model_kwargs={"attn_implementation": "flash_attention_2"})
    transformer.model.config.num_labels = 1
    embedding_dimension = transformer.get_embedding_dimension()
    pooling = Pooling(embedding_dimension=embedding_dimension, pooling_mode="cls")
    dense_inner = Dense(
        in_features=embedding_dimension, out_features=embedding_dimension, bias=False,
        activation_function=nn.GELU(),
        module_input_name="sentence_embedding", module_output_name="sentence_embedding",
    )
    norm = LayerNorm(dimension=embedding_dimension)
    dense_score = Dense(
        in_features=embedding_dimension, out_features=1, bias=True,
        activation_function=nn.Identity(),
        module_input_name="sentence_embedding", module_output_name="scores",
    )
    model = CrossEncoder(
        modules=[transformer, pooling, dense_inner, norm, dense_score],
        num_labels=1,
        activation_fn=nn.Identity(),
        model_card_data=CrossEncoderModelCardData(
            model_name=f"Ettin Reranker {ENCODER_SIZE} distilled from mxbai-rerank-large-v2",
            language="en",
            license="apache-2.0",
        ),
    )
    actual_attn = getattr(model[0].model.config, "_attn_implementation", None)
    if not (actual_attn and "flash" in actual_attn.lower()):
        logging.warning(f"FA2 may not be active (attn_impl={actual_attn!r}); training will be slower.")

    
    
    dataset_repo = "cross-encoder/ettin-reranker-v1-data"
    train_pieces = []
    eval_dataset = None
    for config_name in get_dataset_config_names(dataset_repo):
        dataset = load_dataset(dataset_repo, config_name)
        train_pieces.append(dataset["train"])
        if "validation" in dataset:
            eval_dataset = dataset["validation"]
    train_dataset = concatenate_datasets(train_pieces)
    print(train_dataset)

    
    loss = MSELoss(model)

    
    args = CrossEncoderTrainingArguments(
        output_dir=f"models/{run_name}",
        num_train_epochs=1,
        per_device_train_batch_size=per_device_batch_size,
        per_device_eval_batch_size=per_device_batch_size,
        gradient_accumulation_steps=1,
        learning_rate=learning_rate,
        warmup_ratio=0.03,
        bf16=True,
        eval_strategy="steps",
        eval_steps=0.05,
        save_strategy="steps",
        save_steps=0.05,
        save_total_limit=5,
        logging_steps=0.025,
        logging_first_step=True,
        load_best_model_at_end=True,
        metric_for_best_model="eval_NanoBEIR_R100_mean_ndcg@10",
        dataloader_num_workers=dataloader_workers,
        run_name=run_name,
        seed=12,
    )

    
    evaluator = CrossEncoderNanoBEIREvaluator(
        dataset_names=["msmarco", "nfcorpus", "nq", "fiqa2018", "touche2020", "scifact",
                       "hotpotqa", "arguana", "fever", "dbpedia", "climatefever", "scidocs",
                       "quoraretrieval"],
        batch_size=per_device_batch_size,
        always_rerank_positives=False,
        show_progress_bar=False,
    )

    
    trainer = CrossEncoderTrainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss=loss,
        evaluator=evaluator,
    )

    
    if trainer.is_world_process_zero():
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            evaluator(model)

    
    trainer.train()

    
    if trainer.is_world_process_zero():
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            evaluator(model)

    
    final_dir = f"models/{run_name}/final"
    model.save_pretrained(final_dir)


if __name__ == "__main__":
    main()

```

对于多节点训练（任何超过17m/32m的模型），使用torchrun启动相同的脚本：

```bash

python train.py


torchrun --nproc_per_node=8 --nnodes=4 ... train.py

```

## 结论

ettin-reranker-v1系列模型采用单一简洁的训练方案，在已发布的所有参数规模（最高1B参数）中均达到业界领先水平。通过点式MSE蒸馏技术，将强教师模型的知识迁移至涵盖广泛领域与检索特定场景的混合数据集，模型规模从17M到1B参数实现平滑扩展，仅需调整学习率和每设备批处理大小。

每个ettin-reranker-v1模型在MTEB和NanoBEIR基准测试中均显著优于ms-marco-MiniLM-L*-v2系列。cross-encoder/ettin-reranker-150m-v1是我测试过的600M参数以下区间中最强的中端重排序模型，cross-encoder/ettin-reranker-400m-v1的MTEB得分与1.54B教师模型差距仅0.0024，而cross-encoder/ettin-reranker-1b-v1与教师模型的得分差距仅为0.0001。

所有资源集中呈现：

- 模型：cross-encoder/ettin-reranker-17m-v1、cross-encoder/ettin-reranker-32m-v1、cross-encoder/ettin-reranker-68m-v1、cross-encoder/ettin-reranker-150m-v1、cross-encoder/ettin-reranker-400m-v1、cross-encoder/ettin-reranker-1b-v1
- 数据集：cross-encoder/ettin-reranker-v1-data包含约1.43亿条（查询、文档、标签）三元组，按39个命名子集存储，确保每行数据的来源可追溯。
- 训练脚本：上述"整体训练脚本"约150行代码，六个模型均使用同一脚本。

- cross-encoder/ettin-reranker-17m-v1
- cross-encoder/ettin-reranker-32m-v1
- cross-encoder/ettin-reranker-68m-v1
- cross-encoder/ettin-reranker-150m-v1
- cross-encoder/ettin-reranker-400m-v1
- cross-encoder/ettin-reranker-1b-v1

如果您基于这些模型构建应用，请务必告知我！我真心期待看到大家的创新应用，如果您能利用已发布的数据训练出更好的重排序模型，那就更棒了。该方案刻意保持简洁，部分原因正是为了给后续改进留出充足空间。训练更强的教师模型后，同一脚本可继续产出更优的学生模型。

## 致谢

感谢Ettin团队（Orion Weller、Kathryn Ricci、Marc Marone、Antoine Chaffin、Dawn Lawrie和Benjamin Van Durme）构建了这些重排序模型所依赖的基础编码器，感谢LightOn团队（Antoine Chaffin、Raphael Sourty、Paulo Moura和Amélie Chatelain）在训练数据收集方面的工作，以及Mixedbread AI团队（Xianming Li、Aamir Shakir、Rui Huang、Tsz-fung Andrew Lee、Julius Lipp、Benjamin Clavié和Jing Li）在教师模型方面的贡献。

## 引用

如果您使用ettin-reranker-v1系列或任何已发布的成果，请引用本篇博客文章：

```bibtex
@misc{aarsen2026ettin-reranker,
    title = "Introducing the Ettin Reranker Family",
    author = "Aarsen, Tom",
    year = "2026",
    publisher = "Hugging Face",
    url = "https://huggingface.co/blog/ettin-reranker",
}

```

---

> 本文由AI自动翻译，原文链接：[Introducing the Ettin Reranker Family](https://huggingface.co/blog/ettin-reranker)
> 
> 翻译时间：2026-05-20 06:11
