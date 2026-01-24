---
title: 小而强大：Llama Nemotron RAG模型提升多模态搜索与文档检索精度
title_original: 'Small Yet Mighty: Improve Accuracy In Multimodal Search and Visual
  Document Retrieval with Llama Nemotron RAG Models'
date: '2026-01-06'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/llama-nemotron-vl-1b
author: ''
summary: 本文介绍了NVIDIA推出的两款小型多模态RAG模型——llama-nemotron-embed-vl-1b-v2和llama-nemotron-rerank-vl-1b-v2，旨在解决纯文本检索系统在处理包含图表、表格、图像等元素的PDF文档时的信息遗漏问题。文章阐述了多模态RAG需要强大检索能力的原因，展示了模型在多个视觉文档检索基准测试中的表现，并说明了其架构特点：模型小巧、兼容标准向量数据库、能通过提供更准确的证据来减少生成式AI的幻觉。这些模型为开发者在企业级规模上构建低延迟、高精度的多模态问答和搜索系统提供了实用工具。
categories:
- AI产品
tags:
- 多模态检索
- RAG模型
- 视觉文档检索
- Llama Nemotron
- 向量数据库
draft: false
translated_at: '2026-01-07T03:12:32.195Z'
---

# 小而强大：利用 Llama Nemotron RAG 模型提升多模态搜索与视觉文档检索的准确性

- 
- 
- 
- 
- 

![](/images/posts/811b17370977.webp)

![](/images/posts/ae67c6ab504e.webp)

![](/images/posts/3ee14a6dad2d.webp)

![NVIDIA's avatar](/images/posts/ef2e4339456d.webp)

![Gabriel de Souza Pereira Moreira's avatar](/images/posts/8c772fb90843.webp)

![NVIDIA's avatar](/images/posts/ef2e4339456d.webp)

![NVIDIA's avatar](/images/posts/ef2e4339456d.webp)

### 如何利用小巧的 Llama Nemotron 模型构建准确、低延迟的视觉文档检索系统，并能与标准向量数据库开箱即用

为何多模态 RAG 需要世界级的检索能力商业多模态搜索的先进水平视觉文档检索（页面检索）基准测试架构亮点与训练方法组织机构如何使用这些模型开始使用在实际应用中，数据不仅仅是文本。它存在于包含图表、扫描合同、表格、截图和幻灯片的 PDF 中，因此纯文本检索系统会遗漏重要信息。多模态 RAG 流水线通过实现对文本、图像和布局的联合检索与推理，改变了这一现状，从而获得更准确、更具可操作性的答案。

- 为何多模态 RAG 需要世界级的检索能力
- 商业多模态搜索的先进水平视觉文档检索（页面检索）基准测试
- 架构亮点与训练方法
- 组织机构如何使用这些模型
- 开始使用

- 视觉文档检索（页面检索）基准测试

本文将介绍两款用于视觉文档多模态检索的小型 Llama Nemotron 模型：

- **llama-nemotron-embed-vl-1b-v2**：一个密集的单向量多模态（图像+文本）嵌入模型，用于页面级检索和相似性搜索。
- **llama-nemotron-rerank-vl-1b-v2**：一个交叉编码器重排序模型，用于查询-页面相关性评分。

- 足够小巧，可在大多数 NVIDIA GPU 资源上运行
- 兼容标准向量数据库（每页一个密集向量）
- 旨在通过将生成过程建立在更好的证据而非更长的提示词上，来减少幻觉

我们将在下文中展示它们在现实文档基准测试上的表现。

## 为何多模态 RAG 需要世界级的检索能力

多模态 RAG 流水线将检索器与视觉语言模型（VLM）相结合，使得响应不仅基于检索到的页面文本，还基于视觉内容，而不仅仅是原始文本提示词。

嵌入控制着哪些页面被检索并呈现给 VLM。重排序模型则决定这些页面中哪些最相关并应影响答案。如果其中任何一步不准确，VLM 就更可能出现幻觉——而且通常置信度很高。将多模态嵌入与多模态重排序器结合使用，可以确保生成过程基于正确的页面图像和文本。

## 商业多模态搜索的先进水平

**llama-nemotron-embed-vl-1b-v2** 和 **llama-nemotron-rerank-vl-1b-v2** 模型专为开发人员设计，用于在大量 PDF 和图像语料库上构建多模态问答和搜索系统。

llama-nemotron-embed-vl-1b-v2 模型是一个单向量（密集）嵌入模型，能高效地将视觉和文本信息压缩成单一表示。这种设计确保了与所有标准向量数据库的兼容性，并能在企业规模上实现毫秒级延迟的搜索。

llama-nemotron-rerank-v1-1b-v2 是一个交叉编码器重排序模型，它对检索到的顶部候选结果进行重新排序，以提高相关性并提升下游答案质量，而无需更改存储或索引格式。

我们在五个视觉文档检索数据集上评估了 llama-nemotron-embed-vl-1b-v2 和 llama-nemotron-rerank-vl-1b-v2：流行的 **ViDoRe V1、V2 和 V3**（一个由 8 个公共数据集组成的企业级现实视觉文档检索基准），以及两个内部视觉文档检索数据集：

- **DigitalCorpora-10k**：一个包含超过 1300 个问题的数据集，基于来自 **DigitalCorpora** 的 10,000 份文档语料库，这些文档很好地混合了文本、表格和图表。
- **Earnings V2**：一个包含 287 个问题的内部检索数据集，基于 500 份 PDF，主要由大型科技公司的财报组成。

### 视觉文档检索（页面检索）基准测试

下表报告了五个数据集上的平均检索准确率（Recall@5），特别关注商业上可行的密集检索模型。

我们可以看到，**llama-nemotron-embed-vl-1b-v2** 在图像和图像+文本模态上提供了比其前身 **llama-3.2-nemoretriever-1b-vlm-embed-v1** 更好的检索准确率（Recall@5），并且在文本模态上也优于我们的小型文本嵌入模型 **llama-nemotron-embed-1b-v2**。最后，我们的 VLM 重排序器 **llama-nemotron-rerank-vl-1b-v2** 将每个模态的检索准确率进一步提高了 7.2%、6.9% 和 6%。

注意：**图像+文本模态**意味着页面图像及其文本（使用如 **NV-Ingest** 等摄取库提取）都作为输入提供给嵌入模型，以获得更准确的表示和检索。

视觉文档检索基准测试（页面检索） – 在 DigitalCorpora-10k、Earnings V2、ViDoRe V1、V2、V3 上的平均 Recall@5

下表展示了 **llama-nemotron-rerank-vl-1b-v2** 与另外两个公开可用的多模态重排序模型 **jina-reranker-m0** 和 **MonoQwen2-VL-v0.1** 的准确率评估对比。尽管 **jina-reranker-m0** 在纯图像任务上表现良好，但其公开权重仅限于非商业用途（CC-BY-NC）。相比之下，**llama-nemotron-rerank-vl-1b-v2** 在文本和图像+文本组合模态上提供了更优越的性能，其宽松的商业许可使其成为企业部署的理想选择。

## 架构亮点与训练方法

llama-nemotron-embed-vl-1b-v2 嵌入模型是一个基于 Transformer 的编码器模型，约有 17 亿参数。它是 NVIDIA Eagle 系列模型的微调版本，使用了 Llama 3.2 1B 语言模型和 SigLip2 400M 视觉编码器。用于检索的嵌入模型通常使用双编码器架构进行训练，该架构独立编码查询和文档。该模型对语言模型输出的 Token 嵌入应用平均池化，从而输出一个 2048 维的单一嵌入。使用对比学习来训练嵌入模型，以增加查询与相关文档之间的相似性，同时减少与负样本的相似性。

llama-nemotron-rerank-vl-1b-v2 是一个交叉编码器模型，约有 17 亿参数。它同样是 NVIDIA Eagle 系列模型的微调版本。语言模型的最终层隐藏状态使用平均池化策略进行聚合，并为排序任务微调了一个二元分类头。该模型使用公开可用和合成生成的数据集，通过交叉熵损失进行训练。

## 组织机构如何使用这些模型

以下是组织机构如何应用新的 Nemotron 嵌入和重排序模型的三个示例，您可以将其适配到自己的系统中。

**Cadence：设计与 EDA 工作流**
Cadence 将微架构和规范文档、约束条件以及验证相关材料等逻辑设计资产建模为相互连接的多模态文档。因此，工程师可以提问：“我想扩展中断控制器以支持低功耗状态，请告诉我哪些规范部分需要修改”，并立即呈现最相关的要求。然后，系统可以建议几种替代的规范更新策略，比较它们的权衡，并为用户选择的选项生成相应的规范修改。

IBM：领域密集的存储与基础设施文档
IBM Storage 将长篇 PDF（产品指南、配置手册和架构图）的每一页视为多模态文档，对其进行嵌入，并在发送给下游 LLM（大语言模型）之前，使用重排序器优先选择那些领域特定术语、缩写和产品名称出现在正确上下文中的页面。这提升了 AI 系统解读存储概念以及对复杂基础设施文档进行推理的能力。

ServiceNow：基于海量 PDF 的聊天
ServiceNow 使用多模态嵌入来索引组织内部 PDF 的页面，然后在其“与 PDF 聊天”体验中应用重排序器，为每个用户查询选择最相关的页面。通过在多轮对话中保持高分页面的上下文，其 Agent（智能体）能够维持更连贯的对话，并帮助用户更有效地浏览大型文档集合。

您可以直接试用这些模型：

- 在您选择的向量数据库中运行 `llama-nemotron-embed-vl-1b-v2`，以支持对 PDF 和图像的多模态搜索。
- 将 `llama-nemotron-rerank-vl-1b-v2` 作为第二阶段的重排序器应用于您的 top-k 结果，以在不更改索引的情况下提升检索质量。
- 如果您需要用于 Agent（智能体）的端到端组件，可以下载 Nemotron RAG 模型。这些模型不仅限于独立使用，也可以集成到数据摄取管道中。

将这些新模型接入您现有的 RAG（检索增强生成）技术栈，或者将它们与 Hugging Face 上的其他开源模型结合，构建能够理解您的 PDF（而不仅仅是提取的文本）的多模态 Agent（智能体）。

通过订阅 NVIDIA 新闻，并在 LinkedIn、X、YouTube 以及 Discord 的 Nemotron 频道上关注 NVIDIA AI，及时获取 NVIDIA Nemotron 的最新动态。

· 注册或登录以发表评论

- 
- 
- 
- 
- 

![](/images/posts/811b17370977.webp)

![](/images/posts/ae67c6ab504e.webp)

![](/images/posts/3ee14a6dad2d.webp)

---

> 本文由AI自动翻译，原文链接：[Small Yet Mighty: Improve Accuracy In Multimodal Search and Visual Document Retrieval with Llama Nemotron RAG Models](https://huggingface.co/blog/nvidia/llama-nemotron-vl-1b)
> 
> 翻译时间：2026-01-07 02:41
