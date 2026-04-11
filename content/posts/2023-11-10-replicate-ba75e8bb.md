---
title: 使用开源BGE模型：更快、更便宜的文本嵌入方案
title_original: Using open-source models for faster and cheaper text embeddings –
  Replicate blog
date: '2023-11-10'
source: Replicate Blog
source_url: https://replicate.com/blog/run-bge-embedding-models
author: ''
summary: 本文介绍了如何在Replicate平台上使用北京智源人工智能研究院开源的BAAI/bge-large-en-v1.5模型来生成文本嵌入。该模型在MTEB排行榜上表现优于OpenAI的嵌入模型，且成本便宜4倍。文章详细说明了从环境设置、身份验证到实际生成嵌入的完整步骤，包括如何从文本列表和JSONL文件生成向量，为开发者提供了高效、低成本处理语义搜索、聚类和分类等任务的实用指南。
categories:
- AI基础设施
tags:
- 文本嵌入
- 开源模型
- Replicate
- BGE模型
- 语义搜索
draft: false
translated_at: '2026-04-11T04:22:58.638184'
---

-   Replicate
-   Blog

# 使用开源模型实现更快、更便宜的文本嵌入

-   nateraw

嵌入是处理文本的强大工具。通过将文本“嵌入”为向量，你可以将其含义编码成一种表示形式，这种形式能更便捷地应用于语义搜索、聚类和分类等任务。如果你是嵌入技术的新手，可以查阅Simon Willison撰写的这篇精彩介绍来快速入门。如今，嵌入正被用于更多有趣的应用，例如检索增强生成，它通过对嵌入进行语义搜索来提高语言模型响应的质量。

在本指南中，我们将了解如何在 Replicate 上使用 `BAAI/bge-large-en-v1.5` 模型生成文本嵌入。由北京智源人工智能研究院发布的“BAAI 通用嵌入”模型系列是开源的，可在 Hugging Face Hub 上获取。

截至 2023 年 10 月，我们将在此使用的**大型 BGE 模型**是当前最先进的文本嵌入开源模型。它在 MTEB 排行榜上的排名高于 OpenAI 的嵌入模型，并且在 Replicate 上进行大规模文本嵌入时，运行成本便宜 4 倍（更多内容见后文！）。

👇 本文中的代码也以托管的、交互式 Google Colab 笔记本形式提供：

## 先决条件

你需要：

*   **Replicate 账户**：你将使用 Replicate 来运行 BAE 模型。注册是免费的，并且注册后你会获得一些初始额度。之后，你将按使用秒数付费。更多详情请参阅计费说明。
*   一个用于跟随操作的 **Python 环境**（或者你可以使用 Google Colab 笔记本）。

👀 在此处查看 Replicate UI 中的模型，以及更多运行方式（Node.js、cURL、Docker 等）。

## 安装依赖项

首先安装以下依赖项：

```
pip install replicate

# 用于统计 token：
pip install transformers sentencepiece

# 用于我们的示例 "samsum" 数据集：
pip install datasets py7zr scikit-learn
```

## 使用 Replicate 进行身份验证

从 replicate.com/account/api-tokens 获取一个 Replicate API token，并将其设置为环境变量：

```
export REPLICATE_API_TOKEN=...
```

## 从文本列表生成嵌入

现在你可以运行嵌入模型了。我们将使用 `replicate` 库在 Replicate 上运行该模型：

```
import json
import replicate

texts = [
    "the happy cat",
    "the quick brown fox jumps over the lazy dog",
    "lorem ipsum dolor sit amet",
    "this is a test",
]

output = replicate.run(
    "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
    input={"texts": json.dumps(texts)}
)
print(output)
```

这里的输出将是每个文本的嵌入列表。

## 从 JSONL 文件生成嵌入

JSONL（或称“JSON 行”）是一种用于以基于文本、行分隔的格式存储结构化数据的文件格式。文件中的每一行都是一个独立的 JSON 对象。

这是一个 JSONL 文件的示例，`dummy_example.jsonl`：

```
{"text": "the happy cat"}
{"text": "the quick brown fox jumps over the lazy dog"}
{"text": "lorem ipsum dolor sit amet"}
{"text": "this is a test"}
```

通过指定 `path` 输入，在此文件上运行模型。

```
output = replicate.run(
    "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
    input={"path": open("dummy_example.jsonl", "rb")}
)
len(output)
# 输出：
# 4
```

## 实际示例：嵌入 SAMSum 数据集

**SAMSum 数据集**是一个包含约 1.4 万个带有手动标注摘要的示例对话的集合。它通常用于训练和评估语言模型。

这里我们将对整个 SAMSum 数据集进行编码。我们将使用 `datasets` 库加载数据集，将其转换为 JSONL 文件，然后在其上运行 BGE 模型以生成文本嵌入。

```
from pathlib import Path

from datasets import load_dataset

dataset_name = "samsum"
text_field = "dialogue"
outfile_name = "samsum_dialogue.jsonl"

ds = load_dataset(dataset_name, split='train')
ds = ds.remove_columns([x for x in ds.column_names if x != text_field])
ds = ds.rename_column(text_field, "text")
texts = ds["text"]
texts[0]
# 输出：
# "Amanda: I baked cookies. Do you want some?\r\nJerry: Sure!\r\nAmanda: I'll bring you tomorrow :-)"
```

要将数据集转换为 JSONL 文件，请在数据集上调用 `.to_json`。

```
ds.to_json(outfile_name)
```

如果一切顺利，数据集应被写入 `samsum_dialogue.jsonl`。使用 `head` 命令查看文件的前几行：

```
head -n 5 {outfile_name}
```

你应该会看到以下内容：

```
{"text":"Amanda: I baked  cookies. Do you want some?\r\nJerry: Sure!\r\nAmanda: I'll bring you tomorrow :-)"}
{"text":"Olivia: Who are you voting for in this election? \r\nOliver: Liberals as always.\r\nOlivia: Me too!!\r\nOliver: Great"}
{"text":"Tim: Hi, what's up?\r\nKim: Bad mood tbh, I was going to do lots of stuff but ended up procrastinating\r\nTim: What did you plan on doing?\r\nKim: Oh you know, uni stuff and unfucking my room\r\nKim: Maybe tomorrow I'll move my ass and do everything\r\nKim: We were going to defrost a fridge so instead of shopping I'll eat some defrosted veggies\r\nTim: For doing stuff I recommend Pomodoro technique where u use breaks for doing chores\r\nTim: It really helps\r\nKim: thanks, maybe I'll do that\r\nTim: I also like using post-its in kaban style"}
{"text":"Edward: Rachel, I think I'm in ove with Bella..\r\nrachel: Dont say anything else..\r\nEdward: What do you mean??\r\nrachel: Open your fu**ing door.. I'm outside"}
{"text":"Sam: hey  overheard rick say something\r\nSam: i don't know what to do :-\/\r\nNaomi: what did he say??\r\nSam: he was talking on the phone with someone\r\nSam: i don't know who\r\nSam: and he was telling them that he wasn't very happy here\r\nNaomi: damn!!!\r\nSam: he was saying he doesn't like being my roommate\r\nNaomi: wow, how do you feel about it?\r\nSam: i thought i was a good rommate\r\nSam: and that we have a nice place\r\nNaomi: that's true man!!!\r\nNaomi: i used to love living with you before i moved in with me boyfriend\r\nNaomi: i don't know why he's saying that\r\nSam: what should i do???\r\nNaomi: honestly if it's bothering you that much you should talk to him\r\nNaomi: see what's going on\r\nSam: i don't want to get in any kind of confrontation though\r\nSam: maybe i'll just let it go\r\nSam: and see how it goes in the future\r\nNaomi: it's your choice sam\r\nNaomi: if i were you i would just talk to him and clear the air"}
```

让我们嵌入这个数据集。这次我们将指定 `convert_to_numpy=True` 以将嵌入作为 numpy 数组获取，这对于如此大的数据集来说是一种更高效的输出格式。

```
import time

start = time.time()
output = replicate.run(
    "nateraw/bge-large-en-v1.5:9cf9f015a9cb9c61d1a2610659cdac4a4ca222f2d3707a68517b18c198a9add1",
    input=dict(
        path=open(outfile_name, "rb"),
        convert_to_numpy=True,
        batch_size=64
    )
)
time_to_embed = time.time() - start
print(f"that took {time_to_embed:.2f} seconds.")
print("output", output)

# 输出：
# that took 65.51 seconds.
# output https://replicate.delivery/pbxt/ZpzzGcdZf5VbCCgynfufoXww7MtymKITDa0HfAZOOVsvNNJHB/embeddings.npy
```

## 加载预测结果

由于我们选择转换为 numpy 格式，这里我们将使用 numpy 加载。

```
import requests
from io import BytesIO

import numpy as np

embeds = np.load(BytesIO(requests.get(output).content))
embeds.shape
# 输出：
# (14732, 1024)
```

## 价格对比：Replicate 与 OpenAI

在撰写本文时，OpenAI 的 Ada v2 模型成本为每 1K token 0.0001 美元。

在 Replicate 上，你按秒为你运行的硬件付费。我们在此使用的 `nateraw/bge-large-en-v1.5` 运行在 A40（大型）实例上，成本为每秒 0.000725 美元。

下面，我们将比较 OpenAI 和 Replicate。为此，我们需要统计数据集中的 token 数量。我们将使用 `transformers` 库来完成：

```
from datasets import Dataset
from transformers import AutoTokenizer
```

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en-v1.5")

text = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
sed do eiusmod tempor a b
""" * 16  # 长度不够，需要 >= 512 个 token，所以乘以 16

ds = Dataset.from_dict({"text": [text] * 10000})

def count_tokens(ex):
    ex['num_tokens'] = len(tokenizer.encode(ex["text"], truncation=True, add_special_tokens=False))
    return ex

ds = ds.map(count_tokens)
```

在上面的代码片段中，我们准备了一个基准文件，每行包含 512 个 token。这是 BGE 模型支持的最大 token 数量。整个数据集总共有 5,120,000 个 token。我们来复核一下：

```
total_tokens = sum(ds['num_tokens'])
total_tokens
# 输出：
# 5120000
```

最后，我们将这个数据集写入一个 JSONL 文件，就像之前做的那样。

```
outfile_name = "benchmark.jsonl"
ds.to_json(outfile_name)
```

## 运行基准测试

现在我们来运行基准测试。我们将使用 `replicate.predictions.create` 来异步运行模型。这将返回一个 `Prediction` 对象，我们可以用它来获取运行结果及其相关指标。然后，我们可以使用 `predict_time` 来计算运行成本。

```
model = replicate.models.get("nateraw/bge-large-en-v1.5")
version = model.latest_version
prediction = replicate.predictions.create(
    version,
    input=dict(
        path=open(outfile_name, "rb"),
        convert_to_numpy=True,
        batch_size=64
    )
)
prediction.wait()
output = prediction.output
time_to_embed = prediction.metrics['predict_time']
print(f"that took {time_to_embed:.2f} seconds.")
print("output", output)
# 输出：
# that took 151.92 seconds.
# output https://replicate.delivery/pbxt/VVrkEaiaem3uHCzAqAOmCaewTobbvrmA20QNpJo8tE39VTyRA/embeddings.npy
```

让我们看看如果使用 OpenAI API，这次运行的成本会是多少：

```
openai_cost = 0.0001  # 每 1k token 的价格
openai_price = total_tokens / 1000 * openai_cost
print(f"OpenAI price: ${openai_price:.3f} USD")
# OpenAI price: $0.512 USD
```

以及在 Replicate 上的价格：

```
replicate_price = time_to_embed * 0.000725
print(f"Replicate price: ${replicate_price:.3f}")
# Replicate price: $0.110
```

Replicate 上的价格比 OpenAI 便宜了 4 倍多，而且使用的模型在 MTEB 排行榜上排名更高。🎉

## 后续步骤

如果你喜欢这篇文章，并想查看一个在真实场景中使用此文本嵌入模型的更深入示例，请查看 `@jakedahn` 的这篇博客文章，其中涵盖了如何使用 ChromaDB 和 Mistral 进行检索增强生成（RAG）。

祝你探索愉快！

---

> 本文由AI自动翻译，原文链接：[Using open-source models for faster and cheaper text embeddings – Replicate blog](https://replicate.com/blog/run-bge-embedding-models)
> 
> 翻译时间：2026-04-11 04:22
