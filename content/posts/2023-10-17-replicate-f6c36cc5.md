---
title: 使用ChromaDB与Mistral实现检索增强生成（RAG）
title_original: How to use retrieval augmented generation with ChromaDB and Mistral
  – Replicate blog
date: '2023-10-17'
source: Replicate Blog
source_url: https://replicate.com/blog/how-to-use-rag-with-chromadb-and-mistral-7b-instruct
author: ''
summary: 本文是一篇实践指南，介绍了如何利用检索增强生成技术，结合ChromaDB向量数据库和Mistral-7B模型，构建一个能够为Hacker News生成吸引人标题的示例应用。文章首先解释了RAG的基本原理，即通过从外部数据源检索相关信息来增强大语言模型的提示词，从而提升其输出的相关性和准确性。随后，文章详细规划了构建流程，包括数据准备、向量存储、查询测试以及最终与语言模型的整合，旨在通过具体案例帮助读者理解并掌握RAG技术的核心应用方法。
categories:
- AI基础设施
tags:
- 检索增强生成
- RAG
- ChromaDB
- Mistral
- 向量数据库
draft: false
translated_at: '2026-04-11T04:24:13.847049'
---

- Replicate
- Blog

# 如何使用 ChromaDB 和 Mistral 实现检索增强生成

- jakedahn

过去几个月，检索增强生成（RAG）已成为充分发挥 Llama-2-70b-chat 等大语言模型（LLM）潜力的热门技术。

本文将探讨如何创建一个示例 RAG“应用”，帮助您为 Hacker News 提交生成吸引点击的标题。您只需提供一个现有标题、想法或短语，即使最枯燥的文字也能被改造成有望登上 Hacker News 首页的标题。

诚然，这只是个基础的概念演示。它并非革命性创新，也不保证您的帖子能登上 Hacker News 首页。但这没关系，因为重点在于：通过实践让您切身感受 RAG 的工作原理，并掌握在自己项目和系统中运用该技术所需的理解。

![DALL·E 3 生成的羊驼数据垂钓图像。总得有人检索数据。](/images/posts/f1e8c4187f4c.webp)

## 那么，什么是检索增强生成？

检索增强生成是一种通过从外部数据源检索上下文信息，并将该信息作为语言模型提示词组成部分来丰富语言模型输出的技术。其核心思想是：当用有意义的外部数据增强语言模型提示词时，语言模型能够以更深层次的理解和相关性作出回应。

这种模式有效扩展了特定语言模型的功能性上下文长度。因为您不再受限于 4096 个 Token（约 5 页文本），而是可以查询整本 1000 页的书籍以寻找有意义的段落，仅提取生成高质量回应所需的少量句子。

RAG 的灵活性体现在：您可以在多个语言模型间复用相同数据源，或升级至最新语言模型，而无需重新训练或微调任何特定模型。

其他技术（如微调）可为特定用例提供出色效果，例如设定语言模型的风格/语调，或教授语言模型执行难以解释或过于复杂的任务。但如果您的目标是将 LLM 与数据集成，RAG 是正确选择。

## 检索增强生成基础

您可能听说过构建 RAG 应用需要使用嵌入和向量存储，但这并非完全正确。这些组件确实有帮助（我们将在本文中介绍），但并非绝对必需。

在最基础的层面上，RAG 本质上只是将额外上下文粘贴到语言模型提示词的文本中。它可以简单到从实时天气 API 检索旧金山当前天气，然后将 JSON 响应传入提示词文本。无需复杂操作。

在以下示例提示词中，我们指示 mistral-7b-instruct 模型读取输入的 JSON 数据，并像人类气象学家那样撰写天气报告：

```
[INST]
根据以下 JSON 天气数据撰写天气报告：

{
  "location": "San Francisco, CA",
  "temperature: "65ºF",
  "forecast_high": "81ºF",
  "forecast_low": "63ºF",
  "time": "2023-10-09 10:00"
}

必须仅报告 JSON 中提供的数据。不要提及超出所提供 JSON 范围的天气细节。不要提及 JSON 上下文数据。

所有回应必须听起来像人类气象学家。

[/INST]
```

模型回应：

```
早上好！今天在加利福尼亚州旧金山，当前气温为华氏 65 度。
今日天气预报显示最高气温 81 度，最低气温 63 度。
这是探索城市、享受户外活动的美好一天。
如果您计划在阳光下活动，请确保补充水分并涂抹防晒霜。
祝您有美好的一天！
```

向 LLM 提示词传递任意文本信息的能力，正是其如此引人入胜的部分原因。您可以包含小型 CSV 表格、书籍段落、代码、哲学家的励志语录，甚至应用程序状态。实际上，任何内容都可以，只要不超过语言模型的最大上下文长度（Llama2 为 4096 个 Token）。

## 让我们规划构建内容

既然我们已达成共识，并理解 RAG 将解决您所有问题🤭，让我们通过实践示例探索如何实际运用它。

如上所述，我们将构建一个将标题、想法或短语转换为 hackernews 风格标题的示例。为实现这个示例，我们将通过将 Hacker News 热门故事标题索引到向量存储中，并使其可通过嵌入相似性搜索进行查询，从而汲取集体智慧。

其理念是：从经过验证的成功标题中获取灵感，将有助于创建更好的标题建议。

整体协作流程大致如下：

1.  构建可索引和查询的数据集。
2.  将数据集加载到 ChromaDB（向量数据库）中。
3.  对 ChromaDB 运行测试查询并可视化数据库内容。
4.  整合所有环节。从 ChromaDB 查询 10 个相关热门标题，然后提示 Replicate 上的 mistral-7b-instruct 模型，根据相关热门标题的启发建议新标题。

## 1. 构建可索引和查询的数据集

首先需要创建 Hacker News 标题数据集。从头开始创建此类数据集既繁琐又异常复杂，因此我已完成了繁重工作：抓取 Hacker News API 并将故事提炼为包含 13,509 个热门故事的数据集，每个故事在 2023 年 1 月至 2023 年 10 月初期间均获得了 100+ 点赞。

数据集包含 id、score、title、url 和 time 字段。

您可以从本文的 git 仓库下载数据：13509-hn-topstories-2023.jsonl

![数据集视图](/images/posts/e2f9ee4177d0.webp)

我不会用所有细节烦扰您，但已包含了我为构建这个优质 jsonl 文件而拼凑的两个脚本。第一个脚本通过故事 ID 抓取 hackernews API，并将特定 ID 范围内的所有故事保存到 sqlite 数据库。第二个脚本从 sqlite 数据库查询获得 100 个以上点赞的故事，并将其写入 .jsonl 文件。

就我们的目的而言，我们真正只关心 title 字段，因为我们将使用该字段进行嵌入，且所有条目都是“流行的”，因为每个都拥有超过 100 个点赞。

## 2. 将数据集加载到 ChromaDB

很好，现在我们有了 JSONL 数据集，需要为 13,509 个标题中的每一个生成嵌入，然后将所有内容加载到向量存储中。

但让我们分解一下，因为嵌入和向量存储背后的整个概念可能令人困惑。

## 什么是嵌入？

嵌入向量是内容的数值表示，格式为大型浮点数列表。我喜欢将嵌入视为某种令人费解的坐标系。类似于 GPS 地图拥有称为纬度和经度的 2 个坐标。嵌入有点类似，只不过不是 2 维，而是 1024 维🤯。

当嵌入向量开始聚集在一起时，它们所代表的文档在语义、句法或风格上往往相似。

如果这还不理解，请不要担心，我们将在后文中尝试帮助您可视化事物。

有许多嵌入模型可供选择。对于本文，我们将使用 Replicate 上的 bge-large-en-v1.5 模型生成嵌入。该模型于 2023 年 9 月发布，在撰写本文时，它是 HuggingFace 嵌入模型排行榜上表现最佳的嵌入模型。

我们为您整理了一系列可在 Replicate 上尝试的嵌入模型。其中包括更多文本嵌入模型，如 `all-mpnet-base-v2`；图像嵌入模型，如 `clip-features`；甚至还有多模态嵌入模型，例如 `imagebind`，它可以在同一空间中为文本、图像和音频生成嵌入。

## 什么是向量数据库？

向量数据库是一种特殊类型的数据库，我们可以用来存储和查询嵌入及其关联的文档。当您搜索“语义上相似”的内容时，向量数据库的优势就显现出来了。例如，如果您想搜索与“戴帽子的猫”类似的文档，您可能会找到与猫、帽子或其他戴帽子的动物相关的结果。

在本文中，我们将使用 **ChromaDB**，一个开源的向量数据库。我们对 Chroma 的使用模式非常基础，您可以轻松地替换成其他多种向量数据库。

一些流行的替代品有 **Pinecone**、**Weaviate** 和 **pgvector**。

## 让我们写一些代码

在运行任何代码之前，您需要安装一些 Python 依赖项。

```
pip install replicate chromadb tqdm
```

在下面的脚本中，我们执行了几个操作。

1.  在磁盘上的 `./chromadb` 目录初始化 ChromaDB。数据库文件将存储在此处。
2.  将所有 `JSONL` 条目加载到一个字典列表中。
3.  以 250 个条目为一批：
    1.  通过**一次 Replicate 预测**生成 250 个嵌入向量。
    2.  为 id、标题、元数据和嵌入构建 ChromaDB 友好的输入列表。
    3.  将 250 个条目及其所有嵌入和元数据插入（Upsert）到 ChromaDB。

```
import json
import replicate
import chromadb
from tqdm.auto import tqdm

# 初始化 chromadb 目录和客户端。
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(
    name=f"hackernews-topstories-2023"
)

# 创建一个空列表，我们将用 jsonl 条目填充它。
hn_dataset = []

# 将 13509-hn-topstories-2023.jsonl 加载到字典列表中
with open("13509-hn-topstories-2023.jsonl", "r") as f:
    for line in f:
        hn_dataset.append(json.loads(line))

# 以 250 个为一批生成嵌入并索引标题。
batch_size = 250

# 使用 tqdm 显示友好的进度条。
for i in tqdm(range(0, len(hn_dataset), batch_size)):
    # 设置批次的结束位置
    i_end = min(i + batch_size, len(hn_dataset))

    # 获取下一批 250 行
    batch = hn_dataset[i : i + batch_size]

    # 将数据存储到 Chromadb 时，我们构建标题、id 和元数据的列表。
  # 注意：这些列表的大小必须相同，并且每个列表的索引位置必须相互对应，这一点非常重要。
    batch_titles = [story["title"] for story in batch]
    batch_ids = [str(story["id"]) for story in batch]
    batch_metadata = [dict(score=story["score"], time=story['time']) for story in batch]

    # 一次生成 250 个标题的嵌入。
    batch_embeddings = replicate.run(
        "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
        input={"texts": json.dumps(batch_titles)},
    )

  # 将所有嵌入、id、元数据和标题字符串插入（Upsert）到 Chromadb。
    collection.upsert(
        ids=batch_ids,
        metadatas=batch_metadata,
        documents=batch_titles,
        embeddings=batch_embeddings,
    )
```

该脚本使用 `tqdm` 来显示进度条和时间估算。为 250 个标题生成嵌入并插入所有元数据大约需要 5.5 秒。整个过程大约需要 5 分钟。

当您运行 `python index_hn_titles.py` 脚本时，您会发现 ChromaDB 数据被持久化到 `./chromadb` 目录。

![tqdm indexer](/images/posts/31070b49260e.webp)

## 3. 使用 Chromadb 运行示例查询

太棒了。现在我们有了一个已填充的向量数据库，如何验证一切是否按预期工作呢？我喜欢用两种方式来测试索引后的嵌入。

首先，也是最简单的，我喜欢直接用示例字符串进行查询，看看结果是否正确。其次，我喜欢在 2D 或 3D 空间中可视化嵌入，看看它们是否以有意义的方式聚集在一起。

在这个脚本中，我们执行以下操作：

1.  初始化 chromadb 客户端
2.  使用测试字符串查询 chromadb
3.  打印结果

```
import json
import chromadb
import replicate
from chromadb import Documents

# 此函数将用于将查询字符串转换为嵌入，以便我们可以在嵌入空间中进行相似性搜索。
#
# 这里配置为使用 bge-large-en-v1.5 嵌入模型
def generate_embeddings(texts: Documents):
    return replicate.run(
        "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
        input={"texts": json.dumps(texts)},
    )

# 初始化 Chromadb 客户端
client = chromadb.PersistentClient(path="./chromadb")

# 注意 `embedding_function` 关键字参数。当这样提供时，Chrombdb 将无缝地将查询字符串转换为嵌入向量，用于相似性搜索。
collection = client.get_or_create_collection(
    name=f"hackernews-topstories-2023", embedding_function=generate_embeddings
)

# 我们将搜索与这个字符串相似的结果
query_string = "how to create a sqlite extension"

# 执行 Chromadb 查询。
results = collection.query(
    query_texts=[query_string],
    n_results=10,
)

# 从所有结果中创建一个字符串
results = '\n'.join(results['documents'][0])

# 打印结果
print(results)
```

这段代码打印出以下标题，它们似乎都与测试查询字符串 `"how to create a sqlite extension"` 大致相似。

```
Making SQLite extensions pip install-able
SQLite-Utils
sqlean: A set of SQLite extensions
Lightweight SQLite Editor for Windows
Libgsqlite: A SQLite extension which loads a Google Sheet as a virtual table
SQLite 3.43
Code Generator for SQLite
SQLite 3.42.0
Mycelite: SQLite extension to synchronize changes across SQLite instances
Cloud Backed SQLite
```

## 🤓 侧边栏题外话：可视化嵌入

作为题外话，我喜欢通过视觉化的方式来建立对复杂主题的直觉。

可视化嵌入空间内部情况的最简单方法是将嵌入向量绘制在图表上，就像它们是 2D 或 3D 图表中的点一样。为此，我们首先需要将嵌入向量从 768 维投影到 3 维。我们可以使用降维技术，如 **t-SNE（t-分布随机邻域嵌入）** 或 **UMAP（均匀流形近似和投影）** 来执行这种降到 3D 空间的操作，然后我们就可以轻松地在屏幕上显示。

我最喜欢的显示这类数据的方式是使用 **Tensorflow Projector** 工具来可视化和交互 3D 空间中的嵌入向量。

即使第一眼看到下面的视频，您也能直观地看到这些点正在聚集在一起。当发生这种聚类时，就表示聚类的点在语义上彼此相似。

如果没有视觉上的聚集，只是一大堆没有可辨模式的点，那就表明您的嵌入可能有些问题。

您的浏览器不支持视频标签。

下面的视频展示了 t-SNE 降维过程在数百次迭代中演变成聚类的可视化。在视频的末尾，您可以看到，当我点击一个关于 sqlite 的点时，所有最近的邻居也都是关于 sqlite 的。

这总是让我感到震撼，仿佛魔法一般。

要使用 Tensorflow Projector，你需要将元数据和嵌入向量转换为特定的 TSV 格式。我不会逐步介绍如何操作，但我在 git 仓库中包含了一个脚本，可以将整个 Chromadb 集合转换为两个文件（embeddings.tsv 和 metadata.tsv），这两个文件可以加载到 Tensorflow Projector 中，并以交互方式进行可视化。

## 4. 整合所有步骤

现在，我们将通过传入一个工作标题、查询 ChromaDB 获取 10 个相关的热门标题，然后提示 `mistral-7b-instruct` 来生成受这 10 个相关热门标题启发的新标题，从而将所有步骤整合起来。

```
import json
import sys
import chromadb
import replicate
from chromadb import Documents

# 使用 Replicate 上的 bge-large-en-v1.5 生成嵌入向量。
def generate_embeddings(texts: Documents):
    return replicate.run(
        "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
        input={"texts": json.dumps(texts)},
    )

# 实例化 chromadb 客户端，并指定嵌入函数
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(
    name=f"hackernews-topstories-2023", embedding_function=generate_embeddings
)

# 从第一个命令行参数接受用户提示。
user_prompt = sys.argv[1]

# 查询 Chromadb，获取与用户提示最相似的 10 个标题。
results = collection.query(
    query_texts=[user_prompt],
    n_results=10,
)

# 将结果连接成一个字符串，我们将把它塞进提示词中。
successful_titles = '\n'.join(results['documents'][0])

# LLM 提示词模板。
# 注意：[INST] 和 [/INST] 标签是 mistral-7b-instruct 利用指令微调所必需的。
PROMPT_TEMPLATE = f'''[INST]
You are an expert in all things hackernews. Your goal is to help me write the most click worthy hackernews title that will get the most upvotes. You will be given a USER_PROMPT, and a series of SUCCESSFUL_TITLES. You will respond with 5 suggestions for better hackernews titles.

All of your suggestions should be structured in the same format and tone as the previously successful SUCCESSFUL_TITLES. Make sure you do not include specific versions from the SUCCESSFUL_TITLES in your suggestions.

USER_PROMPT: {user_prompt}

SUCCESSFUL_TITLES: {successful_titles}

SUGGESTIONS:

[/INST]
'''

# 提示 mistral-7b-instruct LLM
mistral_response = replicate.run(
    "a16z-infra/mistral-7b-instruct-v0.1:83b6a56e7c828e667f21fd596c338fd4f0039b46bcfa18d973e8e70e455fda70",
    input={
        "prompt": PROMPT_TEMPLATE,
        "temperature": 0.75,
        'max_new_tokens': 2048,
    },
)

# 将响应连接成一个字符串。
suggestions = ''.join([str(s) for s in mistral_response])

# 打印建议。
print(suggestions)

print('====')

print('PROMPT_TEMPLATE', PROMPT_TEMPLATE)
```

我将这个脚本命名为 `hnify.py`，因此我能够使用以下命令运行它：`python hnify.py "teaching Elixir to my toddler"`。该脚本将打印出 5 个建议的标题，然后是发送给 `mistral-7b-instruct` 的完整文本提示词。

在尝试像这样的新 RAG 提示词时，检查完整填充的提示词模板总是有益的。阅读整个提示词将帮助你理解向量数据库返回了什么，并让你感受到你所选择的语言模型是如何对检索到的数据做出响应的。

Replicate 使得迭代调整提示词变得非常容易。例如，在我运行这个脚本后，我能够在 Replicate 仪表板中找到运行语言模型提示词的单个预测记录。这是我的链接：https://replicate.com/p/aosuuqlb43zvxbsptfylyewknq

在该链接上，你可以点击“Replicate”按钮，并快速在页面上的文本字段中测试提示词的更改。这种工作流程使得在使用真实的向量数据库上下文时，能够非常快速地迭代语言模型提示词。

以下是我的完整提示词内容：

```
# 发送给 mistral-7b-instruct 的提示词模板

[INST]
You are an expert in all things hackernews. Your goal is to help me write the most click worthy hackernews title that will get the most upvotes. You will be given a USER_PROMPT, and a series of SUCCESSFUL_TITLES. You will respond with 5 suggestions for better hackernews titles.

All of your suggestions should be structured in the same format and tone as the previously successful SUCCESSFUL_TITLES. Make sure you do not include specific versions from the SUCCESSFUL_TITLES in your suggestions.

USER_PROMPT: teaching Elixir to my toddler

SUCCESSFUL_TITLES: Elixir for Humans Who Know Python
Scripting with Elixir
Teaching ChatGPT to speak my son’s invented language
Physical Knobs and Elixir
Unpacking Elixir: Syntax
The Comprehensive Guide to Elixir's List Comprehension (2022)
From Python to Elixir Machine Learning
How to sell Elixir again
Elixir is still safe
Unpacking Elixir: Real-Time and Latency
Elixir for Ruby developers: the three most important differences
Show HN: Learn Python with Minecraft
Single File Elixir Scripts
Unpacking Elixir: Resilience
Unpacking Elixir: Concurrency
Elixir – Why the dot when calling anonymous functions?
Elixir and Rust is a good mix
Owl: A toolkit for writing command-line user interfaces in Elixir
A Breakdown of HTTP Clients in Elixir
Visual programming with Elixir: Learning to write binary parsers (2019)

SUGGESTIONS:

[/INST]

```

最后，脚本打印出以下这些经过 Hacker News 风格化的标题：

```
python hnify.py "teaching Elixir to my toddler"

1. Elixir for Toddlers: Teaching the Basics of Functional Programming
2. A Beginner's Guide to Elixir: Teaching Your Toddler to Code
3. Elixir for Kids: A Step-by-Step Guide to Learning Functional Programming
4. Teaching Elixir to Your Toddler: A Fun and Easy Approach
5. Elixir for Toddlers: An Introduction to Functional Programming for Beginners
```

这些相当不错！我发现它通常倾向于过于频繁地建议“释放”和“革命性”这类词，或者营销流行语。我们将把这作为一个练习留给读者，你会对提示词做哪些修改，以使其减少营销色彩？

到此结束！现在是时候发布到 Hacker News 上，看看我们新的检索增强生成霸主是否帮助我获得了网络名声。

## 后续步骤

- 在 Replicate 上尝试 `mistralai/mistral-7b-v0.1` 和 `mistralai/mistral-7b-instruct-v0.1`。这个模型只有 70 亿参数，效果却如此出色，令人震惊。
- Mistral 团队在 2023 年 10 月发布了一篇论文，描述了他们是怎样以优于更大模型的方式构建该模型的。
- 在 Replicate 上测试一些有趣的新 Mistral 微调模型。例如，`nateraw/mistral-7b-openorca` 是在 Open Orca 数据集上针对聊天进行微调的，可能成为检索增强生成的理想大语言模型。
- 查看 GitHub 上的相关 git 仓库，其中包含本文的所有代码，以及一些用于创建 hackernews 数据集和将 chromadb 嵌入向量导出到 Tensorflow Projector tsv 文件的额外脚本。
- 如果你觉得这篇文章有帮助，请在 X 上通过 @replicate 告诉我们，或者加入我们的社区 Discord。

---

> 本文由AI自动翻译，原文链接：[How to use retrieval augmented generation with ChromaDB and Mistral – Replicate blog](https://replicate.com/blog/how-to-use-rag-with-chromadb-and-mistral-7b-instruct)
> 
> 翻译时间：2026-04-11 04:24
