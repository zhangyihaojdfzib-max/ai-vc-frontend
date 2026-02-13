---
title: 谷歌发布高效嵌入模型EmbeddingGemma，支持百种语言
title_original: Welcome EmbeddingGemma, Google's new efficient embedding model
date: '2025-09-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/embeddinggemma
author: ''
summary: 谷歌推出专为设备端设计的嵌入模型EmbeddingGemma，该模型拥有3.08亿参数和2K上下文窗口，支持超过100种语言，在MTEB基准测试中表现优异。其采用Gemma
  3双向注意力编码器架构，并应用Matryoshka表示学习，量化后内存占用低于200MB，适用于移动端RAG、智能体等场景。文章还介绍了其在多种框架中的使用方法及微调示例。
categories:
- AI产品
tags:
- 嵌入模型
- 谷歌
- 多语言AI
- 检索增强生成
- 设备端AI
draft: false
translated_at: '2026-02-13T04:28:17.151384'
---

# 欢迎 EmbeddingGemma，谷歌全新高效嵌入模型

## 内容提要

今天，谷歌发布了 **EmbeddingGemma**，这是一款专为设备端用例设计的先进多语言嵌入模型。该模型以速度和效率为核心，具备 **3.08 亿参数** 的紧凑规模和 **2K 上下文窗口**，为移动端 RAG（检索增强生成）流程、Agent（智能体）等应用开启了新的可能性。EmbeddingGemma 经过训练可支持 **超过 100 种语言**，在撰写本文时，是 Massive Text Embedding Benchmark (MTEB) 上排名最高的、参数规模在 5 亿以下的多语言纯文本嵌入模型。

- 简介
- 评估
- 演示
- 使用
    - Sentence Transformers
        - 检索
    - LangChain
    - LlamaIndex
    - Haystack
    - txtai
    - Transformers.js
    - Text Embeddings Inference
    - ONNX Runtime
- 微调
    - 完整微调脚本
    - 训练
    - 微调后评估
- 延伸阅读

## 简介

**文本嵌入** 已成为现代自然语言应用的基石，它将单词、句子和文档转化为能够捕捉含义、情感和意图的密集向量。这些向量支持在海量语料库中进行快速的相似性搜索、聚类、分类和检索，为从推荐引擎、语义搜索到检索增强生成和代码搜索工具等一切应用提供动力。计算这些嵌入的嵌入模型被广泛使用，在 Hugging Face 上每月下载量远超 **2 亿次**。

在此基础上，谷歌 DeepMind 推出了 **EmbeddingGemma**，这是目前最新、能力最强的小型多语言嵌入模型。凭借仅 3.08 亿参数、2K Token 的上下文窗口以及对 100 多种语言的支持，EmbeddingGemma 在 Massive Multilingual Text Embedding Benchmark (MMTEB) 上实现了最先进的性能，同时在量化后内存占用保持在 **200 MB 以下**。

各种设计选择的结果是，它成为了一个非常实用的开源工具，可在日常设备上计算高质量的多语言嵌入。

在这篇博客文章中，我们将介绍 EmbeddingGemma 的架构和训练，并向您展示如何与各种框架（如 Sentence Transformers、LangChain、LlamaIndex、Haystack、txtai、Transformers.js、Text Embedding Inference 和 ONNX）一起使用该模型。

之后，我们将演示如何针对您的领域对 EmbeddingGemma 进行微调，以获得更强的性能。在我们的示例中，我们使用 Medical Instruction and Retrieval Dataset (MIRIAD) 对 EmbeddingGemma 进行微调。生成的模型 `sentence-transformers/embeddinggemma-300m-medical` 在我们的任务上实现了最先进的性能：根据详细的医学问题检索科学医学论文的段落。它甚至**在性能上超过了参数规模是其两倍的模型**。

## 架构

EmbeddingGemma 建立在 **Gemma 3** Transformer 主干之上，但经过修改，使用双向注意力机制而非因果（单向）注意力。这意味着序列中较早的 Token 可以关注较晚的 Token，从而有效地将架构从解码器转变为编码器。在检索等嵌入任务上，编码器模型可以优于作为解码器的 LLM（大语言模型）（Weller 等人，2025）。凭借这个主干，模型可以一次性处理多达 2048 个 Token，足以满足典型的检索输入需求，特别是考虑到更大的输入通常会导致文本嵌入中的信息丢失。

除了新的基于 Gemma 3 的编码器主干（它生成 Token 嵌入）之外，一个平均池化层将这些 Token 嵌入转换为文本嵌入。最后，两个全连接层将文本嵌入转换为其最终形式：一个 768 维的向量。

EmbeddingGemma 模型使用 **Matryoshka Representation Learning (MRL)** 进行训练，允许您根据需要将 768 维输出截断为 512、256 或 128 维。这可以加快下游处理速度，并降低内存和磁盘空间使用率。请参阅 **Sentence Transformers 使用** 部分，查看展示如何执行此截断的代码片段。

该模型使用精心策划的多语言语料库进行训练，总计约 **3200 亿 Token**。这个专有数据集混合了公开可用的网络文本、代码和技术文档，以及合成的特定任务示例。它已经过过滤，以避免儿童性虐待材料 (CSAM)、敏感数据以及低质量或不安全的内容。

## 评估

EmbeddingGemma 在 MMTEB（多语言，v2）和 MTEB（英语，v2）测试套件上进行了基准测试，这些套件涵盖了广泛的任务、领域和语言。尽管其参数规模适中（3.08 亿），但该模型在保持非常小的内存占用的同时，始终优于可比较的基线模型。

![](/images/posts/4331c027513d.png)

![](/images/posts/6cf549cf5ff5.png)

结果将列在官方的 **MTEB 排行榜** 上。我们排除了任何在超过 20% 的 MTEB 数据上训练过的模型，以减轻潜在的过拟合问题。

**演示** 也可以全屏体验。

在桌面设备上亲自体验 **演示**。

## 使用

EmbeddingGemma 已与许多流行工具集成，便于融入您现有的工作流程和应用程序。该模型已集成到 Sentence Transformers 中，因此也集成到在后台使用 Sentence Transformers 的项目中，例如 LangChain、LlamaIndex、Haystack 和 txtai。请参阅以下示例，开始使用您偏好的框架。

对于生产部署，您可以使用 **Text Embeddings Inference (TEI)** 在各种硬件配置上高效地部署模型，也可以使用 **Transformers.js** 在 Web 应用程序中使用。

无论您选择何种框架，都应注意 **提示词**。对于嵌入模型，提示词会预置在输入文本之前，以便模型区分不同的任务。EmbeddingGemma 是使用这些提示名称和提示词进行训练的，因此在使用模型时也应包含它们：

- `query`: `"task: search result | query: "`
- `document`: `"title: none | text: "`
- `BitextMining`: `"task: search result | query: "`
- `Clustering`: `"task: clustering | query: "`
- `Classification`: `"task: classification | query: "`
- `InstructionRetrieval`: `"task: code retrieval | query: "`
- `MultilabelClassification`: `"task: classification | query: "`
- `PairClassification`: `"task: sentence similarity | query: "`
- `Reranking`: `"task: search result | query: "`
- `Retrieval-query`: `"task: search result | query: "`
- `Retrieval-document`: `"title: none | text: "`
- `STS`: `"task: sentence similarity | query: "`
- `Summarization`: `"task: summarization | query: "`

在 Sentence Transformers 中，调用 `model.encode_query` 和 `model.encode_document` 时会自动使用 `query` 和 `document` 提示词，但对于其他框架，您可能需要：
1. 指定提示名称（例如 "Reranking"），
2. 指定提示字符串（例如 "task: search result | query: "），或者
3. 手动将提示词预置到您的输入文本前。

以下示例脚本将使用各种框架演示这一点。

### Sentence Transformers

您需要安装以下软件包：

```shell
pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview
pip install sentence-transformers>=5.0.0
```

#### 检索

使用 Sentence Transformers 进行推理相当简单，请参阅以下语义搜索示例：

```py
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("google/embeddinggemma-300m")
```

query = "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]
query_embeddings = model.encode_query(query)
document_embeddings = model.encode_document(documents)
print(query_embeddings.shape, document_embeddings.shape)



similarities = model.similarity(query_embeddings, document_embeddings)
print(similarities)



ranking = similarities.argsort(descending=True)[0]
print(ranking)


```

- Sentence Transformers `encode_query` 方法文档
- Sentence Transformers `encode_document` 方法文档
- Sentence Transformers `similarity` 方法文档

如果您不打算将此模型用于信息检索，那么您最好使用最通用的 `encode` 方法，并结合最能描述您下游任务的模型提示词，从以下选项中选择：

- BitextMining：在两种语言中查找翻译后的句子对。
- Clustering：查找相似的文本以将其分组。
- Classification：为文本分配预定义的标签。
- InstructionRetrieval：基于自然语言指令检索相关的代码片段。
- MultilabelClassification：为文本分配多个标签。
- PairClassification：为文本分配预定义的标签。
- Reranking：根据相关性对搜索结果重新排序。
- Retrieval-query：基于查询检索文档。
- Retrieval-document：基于文档内容检索文档。
- STS：计算文本之间的语义文本相似度。
- Summarization：生成文本的简洁摘要。

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("google/embeddinggemma-300m")


print(model.prompts)

















texts = [
    "The weather is beautiful today.",
    "It's a lovely day outside.",
    "The stock market crashed yesterday.",
    "I enjoy programming with Python."
]
embeddings = model.encode(texts, prompt_name="STS")
print(embeddings.shape)



similarities = model.similarity(embeddings, embeddings)
print(similarities)
"""
tensor([[1.0000, 0.9305, 0.4660, 0.4326],
        [0.9305, 1.0000, 0.4227, 0.4434],
        [0.4660, 0.4227, 1.0000, 0.2638],
        [0.4326, 0.4434, 0.2638, 1.0000]])
"""

```

- Sentence Transformers `encode` 方法文档
- Sentence Transformers `similarity` 方法文档

由于 `google/embeddinggemma-300m` 是使用 MRL 训练的，因此该模型生成的嵌入/向量可以被截断到较低的维度，而不会显著影响评估性能。较低维度的嵌入/向量在磁盘和内存中存储成本更低，并且对于检索、聚类或分类等下游任务速度更快。

在 Sentence Transformers 中，您可以在初始化 `SentenceTransformer` 时或调用 `model.encode`/`model.encode_query`/`model.encode_document` 时使用 `truncate_dim` 参数来设置较低的维度：

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("google/embeddinggemma-300m", truncate_dim=256)


query = "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]
query_embeddings = model.encode_query(query)
document_embeddings = model.encode_document(documents)
print(query_embeddings.shape, document_embeddings.shape)



similarities = model.similarity(query_embeddings, document_embeddings)
print(similarities)



ranking = similarities.argsort(descending=True)[0]
print(ranking)


```

请注意，尽管使用了比完整尺寸小 3 倍的嵌入/向量，但排序结果得以保留。

- Sentence Transformers Matryoshka 嵌入/向量文档

### LangChain

如果您愿意，也可以使用 LangChain 的 `HuggingFaceEmbeddings`，它在幕后使用了 Sentence Transformers。请注意，您需要告诉 LangChain 分别对查询和文档使用名为 "query" 和 "document" 的提示词。此示例涉及一个简单的信息检索设置，但相同的嵌入模型也可用于更复杂的场景。

```
pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview
pip install sentence-transformers
pip install langchain
pip install langchain-community
pip install langchain-huggingface
pip install faiss-cpu

```

```py
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings




embedder = HuggingFaceEmbeddings(
    model_name="google/embeddinggemma-300m",
    query_encode_kwargs={"prompt_name": "query"},
    encode_kwargs={"prompt_name": "document"}
)

data = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]


documents = [Document(page_content=text, metadata={"id": i}) for i, text in enumerate(data)]




vector_store = FAISS.from_documents(documents, embedder, distance_strategy="MAX_INNER_PRODUCT")


query = "Which planet is known as the Red Planet?"
results = vector_store.similarity_search_with_score(query, k=3)


for doc, score in results:
    print(f"Text: {doc.page_content} (score: {score:.4f})")
"""
Text: Mars, known for its reddish appearance, is often referred to as the Red Planet. (score: 0.6359)
Text: Jupiter, the largest planet in our solar system, has a prominent red spot. (score: 0.4930)
Text: Saturn, famous for its rings, is sometimes mistaken for the Red Planet. (score: 0.4889)
"""

```

- LangChain HuggingFaceEmbeddings 文档

### LlamaIndex

EmbeddingGemma 在 LlamaIndex 中也受支持，因为它在底层使用了 Sentence Transformers。为了获得正确的行为，您需要按照模型配置中的定义指定查询和文档提示词。否则，您的性能将不理想。此脚本展示了在 LlamaIndex 中使用 EmbeddingGemma 的基本示例，但您也可以在更复杂的设置中使用 `HuggingFaceEmbedding` 类。

```
pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview
pip install sentence-transformers
pip install llama-index
pip install llama-index-embeddings-huggingface
pip install llama-index-vector-stores-faiss

```

```py
import faiss
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore




embeddings = HuggingFaceEmbedding(
    model_name="google/embeddinggemma-300m",
    query_instruction="task: search result | query: ",
    text_instruction="title: none | text: ",
)

data = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]


store = FaissVectorStore(faiss_index=faiss.IndexFlatIP(768))
store.add([TextNode(id=i, text=text, embedding=embeddings.get_text_embedding(text)) for i, text in enumerate(data)])

query = "Which planet is known as the Red Planet?"
query_embedding = embeddings.get_query_embedding(query)
results = store.query(VectorStoreQuery(query_embedding=query_embedding, similarity_top_k=3))


for idx, score in zip(results.ids, results.similarities):
    print(f"Text: {data[int(idx)]} (score: {score:.4f})")
"""
Text: Mars, known for its reddish appearance, is often referred to as the Red Planet. (score: 0.6359)
Text: Jupiter, the largest planet in our solar system, has a prominent red spot. (score: 0.4930)
Text: Saturn, famous for its rings, is sometimes mistaken for the Red Planet. (score: 0.4889)
"""

```

- LlamaIndex HuggingFaceEmbedding 文档

### Haystack

EmbeddingGemma 也可以与 Haystack 一起使用，这是一个用于构建生产就绪的搜索和语言应用程序的框架。与 LangChain 和 LlamaIndex 类似，Haystack 在后台使用 Sentence Transformers，并要求您指定适当的提示词。以下示例展示了如何使用 EmbeddingGemma 与 Haystack 设置一个基础的检索流程。

```
pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview
pip install sentence-transformers
pip install haystack-ai

```

```py
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


document_store = InMemoryDocumentStore()


document_embedder = SentenceTransformersDocumentEmbedder(
    model="google/embeddinggemma-300m", encode_kwargs={"prompt_name": "document"}
)
query_embedder = SentenceTransformersTextEmbedder(
    model="google/embeddinggemma-300m", encode_kwargs={"prompt_name": "query"}
)
document_embedder.warm_up()
query_embedder.warm_up()

data = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet.",
]


documents = [Document(content=text, id=str(i)) for i, text in enumerate(data)]
documents_with_embeddings = document_embedder.run(documents=documents)["documents"]
document_store.write_documents(documents_with_embeddings)


query_pipeline = Pipeline()
query_pipeline.add_component("text_embedder", query_embedder)
query_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store, top_k=3))
query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")


query = "Which planet is known as the Red Planet?"
results = query_pipeline.run({"text_embedder": {"text": query}})


for document in results["retriever"]["documents"]:
    print(f"Text: {document.content} (score: {document.score:.4f})")
"""
Text: Mars, known for its reddish appearance, is often referred to as the Red Planet. (score: 0.6359)
Text: Jupiter, the largest planet in our solar system, has a prominent red spot. (score: 0.4930)
Text: Saturn, famous for its rings, is sometimes mistaken for the Red Planet. (score: 0.4889)
"""

```

- Haystack InMemoryEmbeddingRetriever 文档

### txtai

txtai 也与 EmbeddingGemma 兼容。与其他框架类似，txtai 在底层使用 Sentence Transformers，并且需要适当的提示词以便 EmbeddingGemma 发挥最佳性能。以下示例演示了如何使用 txtai 设置一个基础的检索系统。

```
pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview
pip install sentence-transformers
pip install txtai

```

```py
from txtai import Embeddings




embeddings = Embeddings(
    path="google/embeddinggemma-300m",
    method="sentence-transformers",
    instructions={
        "query": "task: search result | query: ",
        "data": "title: none | text: ",
    }
)

data = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]


embeddings.index(data)


query = "Which planet is known as the Red Planet?"
results = embeddings.search(query, 3)


for idx, score in results:
    print(f"Text: {data[int(idx)]} (score: {score:.4f})")
"""
Text: Mars, known for its reddish appearance, is often referred to as the Red Planet. (score: 0.6359)
Text: Jupiter, the largest planet in our solar system, has a prominent red spot. (score: 0.4930)
Text: Saturn, famous for its rings, is sometimes mistaken for the Red Planet. (score: 0.4889)
"""

```

- Haystack InMemoryEmbeddingRetriever 文档

### Transformers.js

您甚至可以使用 Transformers.js 在浏览器中 100% 本地运行 EmbeddingGemma！如果您尚未安装，可以从 NPM 安装该库：

```shell
npm i @huggingface/transformers

```

然后，您可以按如下方式计算嵌入：

```javascript
import { AutoModel, AutoTokenizer, matmul } from "@huggingface/transformers";


const model_id = "onnx-community/embeddinggemma-300m-ONNX";
const tokenizer = await AutoTokenizer.from_pretrained(model_id);
const model = await AutoModel.from_pretrained(model_id, {
  dtype: "fp32", 
});


const prefixes = {
  query: "task: search result | query: ",
  document: "title: none | text: ",
};
const query = prefixes.query + "Which planet is known as the Red Planet?";
const documents = [
  "Venus is often called Earth's twin because of its similar size and proximity.",
  "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
  "Jupiter, the largest planet in our solar system, has a prominent red spot.",
  "Saturn, famous for its rings, is sometimes mistaken for the Red Planet.",
].map((x) => prefixes.document + x);

const inputs = await tokenizer([query, ...documents], { padding: true });
const { sentence_embedding } = await model(inputs);


const scores = await matmul(sentence_embedding, sentence_embedding.transpose(1, 0));
const similarities = scores.tolist()[0].slice(1);
console.log(similarities);



const ranking = similarities.map((score, index) => ({ index, score })).sort((a, b) => b.score - a.score);
console.log(ranking);







```

### Text Embeddings Inference

您可以使用 Text Embeddings Inference (TEI) 1.8.1 或更高版本，轻松地为开发和生产环境部署 EmbeddingGemma。

- CPU：

```shell
docker run -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:cpu-1.8.1 --model-id google/embeddinggemma-300m --dtype float32

```

- 使用 ONNX Runtime 的 CPU：

```shell
docker run -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:cpu-1.8.1 --model-id onnx-community/embeddinggemma-300m-ONNX --dtype float32 --pooling mean

```

- NVIDIA CUDA：

```shell
docker run --gpus all --shm-size 1g -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:cuda-1.8.1 --model-id google/embeddinggemma-300m --dtype float32

```

如果您使用 `cuda-1.8.1` 标签运行 Docker 容器，它包含对多种 GPU 架构的支持：Turing、Ampere、Ada Lovelace 和 Hopper。为了获得一个仅针对您 GPU 的轻量级镜像，您可以改用特定的标签，例如 `turing-1.8.1`、`ampere-1.8.1` (Ampere)、`ada-1.8.1` (Ada Lovelace) 或 `hopper-1.8.1`。

部署完成后，无论使用何种设备或运行时，您都可以利用基于 OpenAI Embeddings API 规范的 `/v1/embeddings` 端点来生成嵌入。

```shell
curl http://0.0.0.0:8080/v1/embeddings -H "Content-Type: application/json" -d '{"model":"google/embeddinggemma-300m","input":["task: search result | query: Which planet is known as the Red Planet?","task: search result | query: Where did Amelia Earhart first fly?"]}'

```

或者，您也可以利用 Text Embeddings Inference Embeddings API 的 `/embed` 端点，它支持 `prompt_name` 参数，这意味着无需手动将提示词前置到输入前，而是通过 `prompt_name` 来选择。

```shell
curl http://0.0.0.0:8080/embed -H "Content-Type: application/json" -d '{"inputs":["Which planet is known as the Red Planet?","Where did Amelia Earthart first fly?"],"prompt_name":"query","normalize":true}'

```

此外，请注意，由于 `google/embeddinggemma-300m` 是使用 Matryoshka Representation Learning (MRL) 训练的，您也可以在 `/v1/embeddings` 和 `/embed` 端点上利用 `dimensions` 参数，将嵌入/向量截断到更低的维度（512、256 和 128），而不会影响评估性能。

### ONNX Runtime

您也可以直接使用 ONNX Runtime 运行模型，这使得它具有高度的可移植性和跨平台兼容性。下面的示例展示了在 Python 中的用法，但同样的方法也可以应用于其他语言（Java、C#、C++ 等）。

```py
from huggingface_hub import hf_hub_download
import onnxruntime as ort
from transformers import AutoTokenizer


model_id = "onnx-community/embeddinggemma-300m-ONNX"
model_path = hf_hub_download(model_id, subfolder="onnx", filename="model.onnx") 
hf_hub_download(model_id, subfolder="onnx", filename="model.onnx_data") 
session = ort.InferenceSession(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_id)


prefixes = {
  "query": "task: search result | query: ",
  "document": "title: none | text: ",
}
query = prefixes["query"] + "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]
documents = [prefixes["document"] + x for x in documents]

inputs = tokenizer([query] + documents, padding=True, return_tensors="np")

_, sentence_embedding = session.run(None, inputs.data)
print(sentence_embedding.shape)  


query_embeddings = sentence_embedding[0]
document_embeddings = sentence_embedding[1:]
similarities = query_embeddings @ document_embeddings.T
print(similarities)  


ranking = similarities.argsort()[::-1]
print(ranking)  

```

## 微调

与所有兼容 Sentence Transformers 库的模型一样，EmbeddingGemma 可以轻松地在您的特定数据集上进行微调。为了展示这一点，我们将在 Medical Instruction and RetrIeval Dataset (MIRIAD) 数据集上微调 `google/embeddinggemma-300m`，使得我们的微调模型特别擅长根据详细的医学问题，从科学医学论文中查找最多 1000 个 Token 的段落。这些段落可以作为生成模型更有效回答问题的关键上下文。

下面，您可以通过可展开的选项卡探索微调过程的每个关键组成部分。每个选项卡包含相关代码和详细说明。

```python
from sentence_transformers import SentenceTransformer, SentenceTransformerModelCardData

model = SentenceTransformer(
    "google/embeddinggemma-300m",
    model_card_data=SentenceTransformerModelCardData(
        language="en",
        license="apache-2.0",
        model_name="EmbeddingGemma-300m trained on the Medical Instruction and RetrIeval Dataset (MIRIAD)",
    ),
)








```

此代码从 Hugging Face 加载 EmbeddingGemma 模型，并带有用于文档记录和共享的可选模型卡片元数据。`SentenceTransformer` 类加载模型权重和配置，而 `model_card_data` 参数附加了有助于包含在自动生成的模型卡片中的元数据。

- 文档：Sentence Transformers > Training Overview > Model

```python
from datasets import load_dataset

train_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="train").select(range(100_000))
eval_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="eval").select(range(1_000))
test_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="test").select(range(1_000))













```

此代码加载 MIRIAD 数据集，更准确地说，是一个已被划分为训练集、评估集和测试集的分割副本。使用大型、高质量的数据集可确保模型学习到有意义的表示，而取子集则允许更快的实验。`load_dataset` 函数从 Hugging Face Datasets 获取数据集，`.select()` 方法限制每个分割的样本数量。

- 文档：Sentence Transformers > Training Overview > Dataset

```python
from sentence_transformers.losses import CachedMultipleNegativesRankingLoss

loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=8)

```

此代码定义了用于训练的损失函数，使用 Cached Multiple Negatives Ranking Loss (CMNRL)。CMNRL 对于检索任务非常有效，因为它使用批次内的负样本来高效地训练模型区分正确和错误的配对。该损失函数接收问题-答案对，并将批次中的其他答案视为负样本，最大化嵌入空间中不相关配对之间的距离。`mini_batch_size` 参数控制内存使用，但不影响训练动态。

建议在 `SentenceTransformerTrainingArguments` 中使用较大的 `per_device_train_batch_size`，并在 `CachedMultipleNegativesRankingLoss` 中使用较低的 `mini_batch_size`，以便在低内存使用的情况下获得强烈的训练信号。此外，推荐使用 `NO_DUPLICATES` 批次采样器来避免意外的假负样本。

- 文档：Sentence Transformers > Training Overview > Loss Function

```python
from sentence_transformers.training_args import BatchSamplers
from sentence_transformers import SentenceTransformerTrainingArguments

run_name = "embeddinggemma-300m-medical-100k"
args = SentenceTransformerTrainingArguments(
    output_dir=f"models/{run_name}",
    num_train_epochs=1,
    per_device_train_batch_size=128,
    per_device_eval_batch_size=128,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=True,  
    bf16=False,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,
    prompts={
        "question": model.prompts["query"],
        "passage_text": model.prompts["document"],
    },
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
    logging_steps=20,
    run_name=run_name,
)

```

此代码设置了用于训练、评估和日志记录的所有超参数和配置。正确的训练参数对于高效、稳定和可复现的训练至关重要。这些参数控制批次大小、学习率、混合精度、评估和保存频率等。值得注意的是，`prompts` 字典将数据集列映射到模型用于区分查询和文档的提示词。

- 文档：Sentence Transformers > Training Overview > Training Arguments

```python
from sentence_transformers.evaluation import InformationRetrievalEvaluator

queries = dict(enumerate(eval_dataset["question"]))
corpus = dict(enumerate(eval_dataset["passage_text"] + train_dataset["passage_text"][:30_000]))
relevant_docs = {idx: [idx] for idx in queries}
dev_evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
    name="miriad-eval-1kq-31kd",
    show_progress_bar=True,
)
dev_evaluator(model)

```

此代码设置了一个信息检索评估器，使用查询和语料库来衡量模型性能。训练期间的评估有助于监控进展并避免过拟合。该评估器通过检查模型是否为每个查询检索到正确的段落来计算检索指标（NDCG、MRR、召回率、精确率、MAP等）。它可以在训练前、训练中和训练后运行，结果将被记录并整合到自动生成的模型卡中。

请注意，此代码片段特别使用了全部（1k个）评估问题，针对全部（1k个）评估段落和30k个训练段落组成的语料库，总计31k个文档。仅针对评估段落进行评估对模型来说过于简单。

- 文档：Sentence Transformers > 训练概览 > 评估器

```python
from sentence_transformers import SentenceTransformerTrainer

trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=dev_evaluator,
)
trainer.train()

```

此代码初始化并运行训练循环，协调所有组件。

- 文档：Sentence Transformers > 训练概览 > 训练器

### 完整微调脚本

以下是结合了上述所有组件的完整脚本：

```python
import logging
import traceback

from datasets import load_dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerModelCardData,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers.losses import CachedMultipleNegativesRankingLoss
from sentence_transformers.training_args import BatchSamplers


logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


model = SentenceTransformer(
    "google/embeddinggemma-300m",
    model_card_data=SentenceTransformerModelCardData(
        language="en",
        license="apache-2.0",
        model_name="EmbeddingGemma-300m trained on the Medical Instruction and RetrIeval Dataset (MIRIAD)",
    ),
)


train_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="train").select(range(100_000))
eval_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="eval").select(range(1_000))
test_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="test").select(range(1_000))









loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=8)


run_name = "embeddinggemma-300m-medical-100k"
args = SentenceTransformerTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=128,
    per_device_eval_batch_size=128,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=True,  
    bf16=False,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    prompts={  
        "question": model.prompts["query"],
        "passage_text": model.prompts["document"],
    },
    
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
    logging_steps=20,
    run_name=run_name,  
)


queries = dict(enumerate(eval_dataset["question"]))
corpus = dict(enumerate(eval_dataset["passage_text"] + train_dataset["passage_text"][:30_000]))
relevant_docs = {idx: [idx] for idx in queries}
dev_evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
    name="miriad-eval-1kq-31kd",  
    show_progress_bar=True,
)
dev_evaluator(model)


trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=dev_evaluator,
)
trainer.train()



dev_evaluator(model)

queries = dict(enumerate(test_dataset["question"]))
corpus = dict(enumerate(test_dataset["passage_text"] + train_dataset["passage_text"][:30_000]))
relevant_docs = {idx: [idx] for idx in queries}
test_evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
    name="miriad-test-1kq-31kd",  
    show_progress_bar=True,
)
test_evaluator(model)


final_output_dir = f"models/{run_name}/final"
model.save_pretrained(final_output_dir)



try:
    model.push_to_hub(run_name)
except Exception:
    logging.error(
        f"Error uploading model to the Hugging Face Hub:\n{traceback.format_exc()}To upload it manually, you can run "
        f"`huggingface-cli login`, followed by loading the model using `model = SentenceTransformer({final_output_dir!r})` "
        f"and saving it using `model.push_to_hub('{run_name}')`."
    )

```

### 训练

我们在配备24GB显存的RTX 3090上运行了完整的训练脚本，完成训练和评估脚本共耗时5.5小时。如果需要，可以通过减小`CachedMultipleNegativesRankingLoss`上的`mini_batch_size`和`InformationRetrievalEvaluator`实例上的`batch_size`来进一步减少内存占用。以下是我们训练运行的日志：

### 微调后评估

基础模型的性能已经非常出色，在我们的MIRIAD测试集上NDCG@10达到了强劲的0.8340。尽管如此，我们仍能在这个特定领域的数据集上显著提升其性能。

我们的微调过程在测试集上实现了NDCG@10 +0.0522的显著提升，得到的模型在此模型规模下，轻松超越了任何现有的通用嵌入模型在我们特定任务上的表现。投入更多时间和计算资源将能获得更强的结果，例如进行**困难负样本挖掘**或使用超过10万个数据对进行训练。

## 延伸阅读

- google/embeddinggemma-300m
- Google EmbeddingGemma 博客文章
- Google EmbeddingGemma 技术报告
- Sentence Transformers 文档
- Sentence Transformers > 训练概览 文档
- Transformers.js 文档
- Text Embeddings Inference (TEI) 文档

---

> 本文由AI自动翻译，原文链接：[Welcome EmbeddingGemma, Google's new efficient embedding model](https://huggingface.co/blog/embeddinggemma)
> 
> 翻译时间：2026-02-13 04:28
