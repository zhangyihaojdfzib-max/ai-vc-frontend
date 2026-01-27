---
title: Sentence Transformers 项目正式迁移至 Hugging Face
title_original: Sentence Transformers is joining Hugging Face!
date: '2025-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/sentence-transformers-joins-hf
author: ''
summary: 本文宣布广受欢迎的开源句子嵌入库 Sentence Transformers 正式从达姆施塔特工业大学 UKP 实验室迁移至 Hugging Face。该项目由
  Nils Reimers 博士于 2019 年创建，已成为语义文本处理的核心工具，Hub 上已有超 16,000 个模型。迁移后，项目将保持社区驱动和开源性质，由
  Hugging Face 的 Tom Aarsen 继续维护，并依托其强大基础设施推动未来发展。
categories:
- AI基础设施
tags:
- Sentence Transformers
- Hugging Face
- 开源项目
- 自然语言处理
- 句子嵌入
draft: false
translated_at: '2026-01-21T04:38:35.768857'
---

# Sentence Transformers 正式加入 Hugging Face！

- +80


项目历史致谢快速开始今天，我们宣布 Sentence Transformers 将从达姆施塔特工业大学 Iryna Gurevych 教授领导的普适知识处理实验室正式迁移至 Hugging Face。Hugging Face 的 Tom Aarsen 自 2023 年底起已开始维护该库，并将继续领导该项目。在新家，Sentence Transformers 将受益于 Hugging Face 强大的基础设施，包括持续集成和测试，确保其紧跟信息检索和自然语言处理领域的最新进展。

- 项目历史
- 致谢
- 快速开始

Sentence Transformers（又称 SentenceBERT 或 SBERT）是一个广受欢迎的开源库，用于生成能够捕捉语义的高质量嵌入。自 Nils Reimers 博士于 2019 年创建以来，Sentence Transformers 已被研究人员和从业者广泛用于各种自然语言处理任务，包括语义搜索、语义文本相似性、聚类和释义挖掘。经过社区多年的开发和训练，**Hugging Face Hub 上已公开提供了超过 16,000 个 Sentence Transformers 模型，每月服务超过一百万独立用户。**

“Sentence Transformers 是一个巨大的成功故事，也是我们实验室长期以来在计算语义相似性研究上的结晶。Nils Reimers 做出了一个非常及时的发现，不仅产出了杰出的研究成果，还创造了一个高度可用的工具。这持续影响着自然语言处理和人工智能领域一代又一代的学生和从业者。我还要感谢所有用户，特别是贡献者们，没有他们，这个项目就不会有今天的成就。最后，我要感谢 Tom 和 Hugging Face 带领这个项目走向未来。”

- Iryna Gurevych 教授，达姆施塔特工业大学普适知识处理实验室主任

“我们非常激动地正式欢迎 Sentence Transformers 加入 Hugging Face 大家庭！过去两年，看到这个项目在全球范围内获得大规模采用，这令人惊叹，这要归功于 UKP 实验室打下的不可思议的基础以及围绕它的出色社区。这仅仅是个开始：我们将继续加倍努力支持其增长和创新，同时保持使其最初得以蓬勃发展的开放、协作精神。”

- Clem Delangue，Hugging Face 联合创始人兼首席执行官

Sentence Transformers 将保持其**社区驱动、开源**项目的性质，并沿用之前的**开源许可证**。我们欢迎并鼓励研究人员、开发者和爱好者的贡献。该项目将继续优先考虑透明度、协作和广泛的可用性。

**Sentence Transformers 库**由 Nils Reimers 博士于 2019 年在达姆施塔特工业大学普适知识处理实验室，在 Iryna Gurevych 教授的指导下推出。受标准 BERT 嵌入在句子级语义任务上局限性的启发，**Sentence-BERT** 采用孪生网络架构来生成具有语义意义的句子嵌入，这些嵌入可以使用余弦相似度进行高效比较。得益于其模块化、开源的设计以及在语义文本相似性、聚类和信息检索等任务上的强大实证性能，该库迅速成为 NLP 研究工具包中的主力，催生了一系列依赖高质量句子表示的后续工作和实际应用。

2020 年，该库增加了多语言支持，将句子嵌入扩展到**超过 400 种语言**。2021 年，在 Nandan Thakur 和 Johannes Daxenberger 博士的贡献下，该库扩展至支持使用交叉编码器和句子 Transformer 模型进行句子对评分。Sentence Transformers 也与 Hugging Face Hub 集成。四年多来，UKP 实验室团队将该库作为一个社区驱动的开源项目进行维护，并持续提供研究驱动的创新。在此期间，该项目的发展得到了德国研究基金会、德国联邦教育与研究部以及黑森州科学艺术部授予 Gurevych 教授的资金支持。

2023 年底，来自 Hugging Face 的 Tom Aarsen 接管了该库的维护工作，引入了现代化的 Sentence Transformer 模型训练，以及对交叉编码器和稀疏编码器模型的改进。

达姆施塔特工业大学的普适知识处理实验室，在 Iryna Gurevych 教授的领导下，因其在自然语言处理和机器学习领域的研究而享誉国际。该实验室在表示学习、大语言模型和信息检索方面有着悠久的开创性工作历史，在顶级会议和期刊上发表了大量论文。除了 Sentence Transformers，UKP 实验室还开发了许多广泛使用的数据集、基准测试和开源工具，支持学术研究和实际应用。

Hugging Face 感谢 UKP 实验室以及所有过去和现在的贡献者，特别是 Nils Reimers 博士和 Iryna Gurevych 教授，感谢他们对该项目的奉献，并信任我们进行维护和现在的管理工作。我们也感谢研究人员、开发者和从业者社区，他们通过模型贡献、错误报告、功能请求、文档改进和实际应用为库的成功做出了贡献。我们很高兴能在 UKP 实验室奠定的坚实基础上继续建设，并与社区合作，进一步提升 Sentence Transformers 的能力。

对于 Sentence Transformers 的新用户或希望探索其功能的人：

- 文档：https://sbert.net
- GitHub 仓库：https://github.com/huggingface/sentence-transformers
- Hugging Face Hub 上的模型：https://huggingface.co/models?library=sentence-transformers
- 快速入门教程：https://sbert.net/docs/quickstart.html

## Transformers v5：为 AI 生态系统提供动力的简单模型定义

![](/images/posts/fb71dc93d9af.jpg)

![](/images/posts/ee041adb72f8.jpg)

![](/images/posts/f80373445ed0.jpg)

![](/images/posts/4402b0abc4cd.jpg)

![](/images/posts/ff16471348cd.png)

## 共同构建开放的 Agent 生态系统：介绍 OpenEnv

- +6

![](/images/posts/4bc561b5b8eb.jpg)

![](/images/posts/3b86f9871ff6.jpg)

![](/images/posts/dbbe3ad5abd9.png)

![](/images/posts/c99c7cbdf7fa.jpg)

- 1 

> 本文由AI自动翻译，原文链接：[Sentence Transformers is joining Hugging Face!](https://huggingface.co/blog/sentence-transformers-joins-hf)
> 
> 翻译时间：2026-01-21 04:38
