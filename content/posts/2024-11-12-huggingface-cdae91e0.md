---
title: 在Hugging Face Hub上分享开放机器学习数据集
title_original: Share your open ML datasets on Hugging Face Hub!
date: '2024-11-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/researcher-dataset-sharing
author: ''
summary: 本文介绍了在Hugging Face Hub上托管和共享开放机器学习数据集的优势与功能。Hub支持TB级大型数据集，提供数据集查看器、全文搜索、排序等探索工具，并兼容Pandas、Polars、DuckDB等第三方库，用户可一行代码加载数据。此外，SQL控制台允许在浏览器中直接查询数据。这些特性降低了数据使用门槛，提升了研究影响力，受到Nvidia、Google、NASA等机构的信赖。
categories:
- AI基础设施
tags:
- Hugging Face Hub
- 数据集托管
- 机器学习
- 开源数据
- 数据共享
draft: false
translated_at: '2026-06-09T06:07:33.278324'
---

# 在 Hugging Face Hub 上分享你的开放机器学习数据集！

如果你正在从事数据密集型研究或机器学习项目，你需要一种可靠的方式来共享和托管数据集。像 Common Crawl、ImageNet、Common Voice 等公共数据集对开放的机器学习生态系统至关重要，然而它们可能难以托管和共享。

Hugging Face Hub 让托管和共享数据集变得无缝顺畅，受到了许多领先研究机构、公司和政府机构的信赖，包括 Nvidia、Google、Stanford、NASA、THUDM 和 Barcelona Supercomputing Center。

通过在 Hugging Face Hub 上托管数据集，你可以立即获得能够最大化你工作影响力的功能：

- 慷慨的限制
- 数据集查看器
- 第三方库支持
- SQL 控制台
- 安全性
- 覆盖范围与可见性

## 慷慨的限制

### 支持大型数据集

Hub 可以托管 TB 级的数据集，具有较高的单文件和单仓库限制。如果你有数据要共享，Hugging Face 数据集团队可以帮助建议上传数据以供社区使用的最佳格式。
🤗 Datasets 库使得上传和下载文件，甚至从头创建数据集变得简单。🤗 Datasets 还支持数据集流式传输，使得无需下载整个数据集就能处理大型数据集成为可能。这对于允许计算资源较少的研究人员使用你的数据集，或者从大型数据集中选择小部分用于测试、开发或原型设计来说，可能是非常宝贵的。

Hugging Face Hub 可以托管通常为机器学习研究创建的大型数据集。

![数据集文件大小信息的截图](/images/posts/e061db0b0c18.png)

注意：Xet 团队目前正在进行后端更新，将把单文件限制从当前的 50 GB 提高到 500 GB，同时提高存储和传输效率。

## 数据集查看器

除了托管你的数据，Hub 还提供了强大的探索工具。借助数据集查看器，用户可以直接在浏览器中探索和与 Hub 上托管的数据集进行交互。这为其他人提供了一种无需先下载即可查看和探索你的数据的简便方式。

Hugging Face 数据集支持多种模态（音频、图像、视频等）和文件格式（CSV、JSON、Parquet 等），以及压缩格式（Gzip、Zip 等）。请查看数据集文件格式页面了解更多详情。

Infinity-Instruct 数据集的数据集查看器。

![数据集查看器截图](/images/posts/2c5df0cbffa1.png)

数据集查看器还包括一些使探索数据集更容易的功能。

### 全文搜索

内置的全文搜索是数据集查看器最强大的功能之一。数据集中的任何文本列都会立即可搜索。

Arxiver 数据集包含 63.4k 行转换为 Markdown 格式的 arXiv 研究论文。通过使用全文搜索，很容易找到包含特定作者（如下面的 Ilya Sutskever）的论文。

### 排序

数据集查看器允许你通过点击列标题对数据集进行排序。这使得在数据集中找到最相关的示例变得容易。

下面是一个示例，展示了 HelpSteer2 数据集按 helpfulness 列降序排序的结果。

## 第三方库支持

Hugging Face 很幸运能与领先的开源数据工具进行第三方集成。通过在 Hub 上托管数据集，可以立即使该数据集与用户最熟悉的工具兼容。

以下是 Hugging Face 开箱即用支持的一些库：

这些库中的大多数允许你仅用一行代码加载或流式传输数据集。

以下是使用 Pandas、Polars 和 DuckDB 的一些示例：

```python

import pandas as pd
df = pd.read_parquet("hf://datasets/neuralwork/arxiver/data/train.parquet")


import polars as pl
df = pl.read_parquet("hf://datasets/neuralwork/arxiver/data/train.parquet")


import duckdb
duckdb.sql("SELECT * FROM 'hf://datasets/neuralwork/arxiver/data/train.parquet' LIMIT 10")

```

你可以在数据集文档中找到关于集成库的更多信息。除了上面列出的库之外，还有许多社区支持的工具也支持 Hugging Face Hub，例如 Lilac 和 Spotlight。

## SQL 控制台

SQL 控制台提供了一个完全在浏览器中运行的交互式 SQL 编辑器，无需任何设置即可进行即时数据探索。主要功能包括：

- 一键操作：只需单击一次即可打开 SQL 控制台查询数据集
- 可共享和可嵌入的结果：共享和嵌入有趣的查询结果
- 完整的 DuckDB 语法：使用完整的 SQL 语法以及用于正则表达式、列表、JSON、嵌入等的内置函数

在每个公共数据集上，你应该会看到一个新的 SQL 控制台徽章。只需单击一下，你就可以打开一个 SQL 控制台来查询该数据集。

## 安全性

虽然使数据集可访问很重要，但保护敏感数据同样至关重要。Hugging Face Hub 提供了强大的安全功能，帮助你在与合适的受众共享数据的同时保持对数据的控制。

### 访问控制

Hugging Face Hub 支持针对谁可以访问数据集的独特访问控制选项。

- 公开：任何人都可以访问数据集。
- 私有：只有你和你的组织成员可以访问数据集。
- 门控：通过两个选项控制对数据集的访问：
  - 自动批准：用户必须提供所需信息（如姓名和电子邮件）并同意条款后才能获得访问权限
  - 手动批准：你审查并手动批准/拒绝每个访问请求

有关门控数据集的更多详细信息，请参阅门控数据集文档。对于更细粒度的控制，还有企业计划功能，组织可以创建资源安全组、使用 SSO 等。

### 内置安全扫描

除了访问控制，Hugging Face Hub 还提供多种安全扫描器：

## 覆盖范围与可见性

拥有一个具有强大功能的安全平台很有价值，但研究的真正影响来自于触达正确的受众。覆盖范围和可见性对于共享数据集的研究人员至关重要——它有助于最大化研究影响，实现可重复性，促进协作，并确保有价值的数据能够惠及更广泛的科学界。

拥有超过 500 万活跃使用该平台的构建者，Hugging Face Hub 为研究人员提供了强大的社区参与和可见性工具。以下是你可以期待的：

### 更好的社区参与

- 每个数据集内置的讨论标签页，用于社区互动
- 组织作为分组和协作处理多个数据集的集中场所
- 数据集使用情况和影响力的指标

### 更广的覆盖范围

- 访问一个庞大而活跃的研究人员、开发者和实践者社区
- SEO 优化的 URL 使你的数据集易于被发现
- 与更广泛的模型、数据集和库生态系统的集成
- 你的数据集与相关模型、论文和演示之间的清晰链接

### 改进的文档

- 可定制的 README 文件，用于全面的文档
- 支持详细的数据集描述和适当的学术引用
- 指向相关研究论文和出版物的链接

Hub 使得提问和讨论数据集变得容易。

![Hub 上数据集讨论的截图。](/images/posts/64541ab5cbf9.png)

## 如何将我的数据集托管在 Hugging Face Hub 上？

既然你已经了解了在 Hub 上托管数据集的好处，你可能想知道如何开始。以下是一些全面的资源，可以指导你完成整个过程：

- 在Hub上创建和共享数据集的一般指南  
- 特定模态的指南：创建音频数据集、创建图像数据集、创建视频数据集  
- 关于如何组织仓库以便数据集能够从Hub自动加载的指导  

- 创建音频数据集  
- 创建图像数据集  
- 创建视频数据集  

如果您想共享大型数据集，以下页面将非常有用：  

- 仓库限制与建议提供了关于共享大型数据集时需要考虑的一些事项的一般指导。  
- 大型上传的技巧与窍门页面提供了如何将大型数据集上传到Hub的一些指导。  

如果您在将数据集上传到Hub时需要任何进一步帮助，或者想上传特别大的数据集，请联系datasets@huggingface.co。

---

> 本文由AI自动翻译，原文链接：[Share your open ML datasets on Hugging Face Hub!](https://huggingface.co/blog/researcher-dataset-sharing)
> 
> 翻译时间：2026-06-09 06:07
