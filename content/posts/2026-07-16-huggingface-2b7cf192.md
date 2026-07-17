---
title: NVIDIA Nemotron 3 Embed登顶RTEB，提升智能体检索
title_original: 'NVIDIA Nemotron 3 Embed Ranks #1 Overall on RTEB, Advancing Agentic
  Retrieval'
date: '2026-07-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/nemotron-3-embed-wins-rteb
author: ''
summary: NVIDIA发布Nemotron 3 Embed系列开放嵌入模型，在RTEB排行榜上综合排名第一。该系列包含8B和1B等变体，支持32k上下文窗口、多语言与代码检索，并针对Blackwell架构优化了4位部署。文章强调，更好的检索能显著提升多步骤Agent工作流的效率，减少重复查询和Token浪费。模型已开放权重、数据集和微调配方，并集成Hugging
  Face、NVIDIA NIM等生态系统。
categories:
- AI产品
tags:
- NVIDIA
- 嵌入模型
- 智能体检索
- RAG
- RTEB
draft: false
translated_at: '2026-07-17T05:11:42.376653'
---

# NVIDIA Nemotron 3 Embed 在 RTEB 上综合排名第一，推动 Agent（智能体）检索能力提升

在多步骤 Agent（智能体）工作流中，检索至关重要。检索质量不佳会导致 Agent（智能体）获取不相关的上下文、重复查询、浪费 Token 预算，并将噪声带入后续的推理步骤。

今天，我们发布 **NVIDIA Nemotron 3 Embed**，这是一系列开放且可商用的嵌入模型，旨在提升检索质量，同时为开发者提供面向生产级 RAG（检索增强生成）、Agent（智能体）检索、代码检索和 Agent（智能体）记忆的实用部署选项。

该系列包含三个开放模型，在精度-效率曲线上实现了最先进的检索性能。其中，一个 8B 模型领跑 RTEB 排行榜，而专为生产级部署设计的高效 1B 变体同样表现出色：

表 1. Nemotron 3 Embed 模型可用性与部署矩阵。

![image5](/images/posts/6bd31d90501d.png)

图 1. RTEB 多语言排行榜截图（2026 年 7 月 15 日），显示 Nemotron-3-Embed-8B-BF16 排名第一。

### 关键特性

除了 RTEB 的优异表现，Nemotron 3 Embed 还为企业级检索部署引入了一套生产就绪的功能集：

- **开放权重、数据集与配方：** 让团队能够在其自有基础设施上检查、调整、微调和部署检索模型。
- **32k 上下文窗口：** 支持对长文档、大型代码上下文和多轮 Agent（智能体）历史进行检索，同时减少截断。
- **多语言与代码检索：** 支持对全球企业数据、技术文档和多文件代码仓库进行检索。
- **NVIDIA NVFP4 效率：** 提供针对 Blackwell 优化的 4 位部署路径，实现高吞吐量检索并减少内存占用。
- **微调与蒸馏配方：** NVIDIA NeMo AutoModel 配方支持领域适配和模型压缩，方便团队根据自身数据调整检索模型。
- **Day-0 生态系统集成：** 即刻在 Hugging Face 上可用，可作为 NVIDIA NIM 微服务部署，受 vLLM 支持，并可通过领先的 AI 云和推理合作伙伴访问。

## 评估：检索质量、Agent（智能体）效率与部署权衡

我们从三个维度评估 Nemotron 3 Embed：检索质量、下游 Agent（智能体）效率以及部署权衡。8B 模型确立了该模型系列的质量上限，而 1B BF16 和 NVFP4 变体则将相同的检索导向设计应用于更低成本、更高吞吐量的部署场景。

### RTEB 领先地位与检索基准测试的显著提升

我们首先在 RTEB 上评估了这些模型，Nemotron-3-Embed-8B-BF16 排名第一。我们还在 ViDoRe V3 Text、MMTEB Retrieval 和 LongEmbed 上使用平均 NDCG@10 对这些模型进行了测试。

![retrieval_accuracy_vertical_longembed_with_gemma_no_gap_y0_y100_1dp](/images/posts/3a8e28ead736.png)

图 2. 使用平均 NDCG@10 在 RTEB、ViDoRe V3 Text、MMTEB Retrieval 和 LongEmbed 上的检索精度对比，将 Nemotron 3 Embed 模型与上一代 Nemotron 基线进行比较。

- **Nemotron-3-Embed-8B-BF16** 在 RTEB 上排名第一，在 RTEB 上得分为 78.5%，在 MMTEB Retrieval 上得分为 75.5%。
- **Nemotron-3-Embed-1B-BF16** 将 8B 模型的大部分检索质量带入了更小的部署规模。它在 RTEB 上得分为 72.4%，相比其前代 1B 模型（llama-nemotron-embed-vl-1b-v2）错误率降低了 27%；在 MMTEB Retrieval 上得分为 71.0%，错误率降低了 28%。

### 为什么更好的检索对 Agent（智能体）至关重要

为了评估 Agent（智能体）场景下的检索效果，我们使用了一个由 Nemotron 3 Ultra 驱动的搜索 Agent（智能体），并改变了检索系统所使用的嵌入模型。更好的检索可以更早地返回相关证据，帮助 Agent（智能体）避免重复搜索、不必要的推理轮次以及额外的上下文检查。我们比较了在 ViDoRe V3、BRIGHT 和 BrowseComp-Plus 上的平均检索精度与预估的下游 Agent（智能体）每次查询的 Token 成本。

![image2](/images/posts/4d34f5e97d4b.png)

图 3. 在 ViDoRe V3、BRIGHT 和 BrowseComp-Plus 上，平均检索精度与下游 Agent（智能体）每次查询 Token 成本的对比。

评估说明：搜索 Agent（智能体）使用 Nemotron 3 Ultra。下游 Token 成本根据 Nemotron 3 Ultra 的输入/输出 Token 数量，使用 GPT-5.5 定价公式估算。

图 3 显示，更强的检索能力降低了下游 Agent（智能体）的 Token 成本。更精确的检索器能更早地返回相关证据，这有助于 Agent（智能体）以更少的重复搜索和推理轮次完成任务。在这些评估中，Nemotron 3 Embed 模型改进了 Agent（智能体）检索的前沿性能，其中 8B 模型在 ViDoRe V3、BRIGHT 和 BrowseComp-Plus 上同时实现了最高的平均检索精度和最低的预估下游 Token 成本。

### 在 Blackwell 上使用 NVFP4 扩展检索能力

对于高吞吐量部署，团队通常会选择更小的嵌入模型以满足延迟和成本目标。Nemotron-3-Embed-1B-NVFP4 旨在通过在 NVIDIA Blackwell 架构上使用原生 NVFP4 加速，缩小服务效率与检索质量之间的差距。该模型将线性层的权重和激活量化为 NVFP4 以实现高效推理，并使用量化感知蒸馏（QAD）来帮助恢复长输入序列的精度。

![image3](/images/posts/9ce2816f8c68.png)

图 4. ViDoRe V3 检索精度与服务效率对比，将 Nemotron-3-Embed-1B-NVFP4 与选定的较小开放嵌入基线（包括 Qwen3-Embedding-0.6B 和 EmbeddingGemma-300M）进行比较。

- **服务效率：** Blackwell 上的 NVFP4 在高吞吐量、低延迟的检索服务中，吞吐量相比 BF16 可提升高达 2 倍。
- **精度保持：** NVFP4 变体保留了 BF16 检索精度的 99% 以上，同时减少了内存占用。

### Day 0 高性能 NIM

对于生产级检索系统，服务栈还需要在实际请求负载下，针对不同的输入序列长度和硬件目标保持这种效率。为了使 Nemotron 3 Embed 能够在企业级规模下立即发挥高性能，我们还为 1B 模型发布了一个优化的 NVIDIA NIM 微服务。如图 5 所示，基于 Rust 的 Nemotron 3 Embed NIM 在 NVIDIA GB200 和 RTX PRO 6000 GPU 上，在 256 和 1024 的输入序列长度下，性能与 vLLM 检查点相当或更优。

![image](/images/posts/5ddf0fe9891c.png)

图 5. Nemotron 3 Embed NIM 服务性能与 NVIDIA GB200 和 RTX PRO 6000 GPU 上 vLLM 检查点的对比。

## 我们如何构建 Nemotron 3 Embed 模型

Nemotron-3-Embed-8B-BF16 采用了 Ministral-3-8B-Instruct-2512 骨干网络，通过将其因果解码器转换为双向编码器来实现全序列检索。该模型使用网络来源和合成文本对的混合数据进行对比预训练，然后在涵盖法律、金融、医疗、商业和教育等领域的精选多语言检索数据集上进行微调。这个 8B 模型作为旗舰嵌入模型，而来自同一开发线的早期 8B 教师检查点则用于蒸馏出高效的 1B 变体。

### 缩小至 1B

1B 模型并非从头开始训练的小型检索器。我们首先将双向适配方法应用于 Ministral-3-3B-Instruct-2512 骨干网络，建立了一个 3B 检索器基础，然后通过两轮结构化剪枝和蒸馏对其进行压缩。

首先，使用 NVIDIA ModelOpt 的 mcore_minitron 神经架构搜索引擎，将 3B 父模型压缩到 2B 中间规模。NAS 流程在严格的参数预算下，搜索了隐藏宽度、前馈网络大小、注意力头数和深度，以确定适用于检索工作负载的高效架构。

然后，将得到的 2B 中间模型从 8B 教师检查点进行蒸馏，以恢复排序精度。我们在多语言、领域内的检索数据混合集上，结合使用余弦距离损失和均方误差损失，使学生的嵌入与教师对齐。

![image1](/images/posts/7ac058c0485c.png)

图6. 剪枝与蒸馏流程将检索器从3B基础模型压缩至最终的1B生产模型。

同样的流程——先进行ModelOpt结构化剪枝，再通过8B教师模型蒸馏——重复执行了一次，将2B中间模型压缩至最终的1.14B嵌入模型。最终训练采用渐进式两阶段上下文缩放方案：

- 第一阶段：聚焦于1024 Token上下文长度下的广泛多语言对齐，以重建父模型的核心检索行为。
- 第二阶段：将上下文长度扩展至4096 Token，并加入长上下文合成数据集与推理数据集，帮助1B模型在较长输入中保持判别性召回能力。

下表总结了Nemotron 3 Embed模型的核心技术规格与部署目标：

表2. Nemotron 3 Embed模型的架构规格与核心推理配置。

## 企业合作伙伴评估

企业ISV、AI原生公司及内存提供商已在Agent检索、Agent内存、代码检索及生产推理工作流中对Nemotron 3 Embed进行评估。

- "上下文是Agent准确性的关键。我们的上下文智能图谱利用嵌入和语义相似性，为Agent（如我们与NVIDIA在五月推出的EnterpriseClaw）提供最相关的企业上下文。NVIDIA新Nemotron 3 Embed模型的早期结果令人鼓舞，尤其在问答方面，其表现优于我们当前模型。我们对其进一步提升企业Agent准确性与可靠性的潜力充满期待。"——Adi Kuruganti，Automation Anywhere首席AI与开发官
- "我们对NVIDIA Nemotron 3 Embed模型的初步评估显示，其在我们的Agent检索用例中表现出强大的检索性能。1B和8B两种变体的提供，使团队能够在不同环境中灵活平衡质量、延迟与部署需求。我们期待继续评估这些模型，并探索它们如何支持生产级AI应用的高性能检索。"——Mani Gill，Boomi产品管理高级副总裁
- IBM在基于watsonx.data的概念验证中，对NVIDIA新Nemotron Embed模型进行了评估，早期结果令人鼓舞。
- "我们在自有技术栈中针对多种模型测试了Nemotron-3-Embed-1B，它表现最佳。例如，在LongMemEval的Retrieval@10指标上，它取得了80.38%的成绩，而Qwen-3-0.6B为78.71%。开放权重与微调方案最令我们感兴趣，因为这使我们能够将模型适配到记忆文本并自行提供服务。"——Rudraj Mehta，Mem0产品经理
- Palantir正与NVIDIA合作，评估Nemotron 3 Embed在边缘检索工作负载中为终端客户部署的方案，这是基于此前将NVIDIA嵌入模型纳入AIP模型目录的成果。
- ServiceNow正在评估NVIDIA Nemotron Embed，用于其文档检索，并持续关注领域内微调以提升检索准确性。
- turbopuffer正将Nemotron 3 Embed引入其原生嵌入服务，使开发者能够在其语义搜索引擎中使用这些模型。
- "在我们的重排序技术栈中替换为NVIDIA Nemotron 3 Embed模型后，性能实现了显著飞跃，使我们能够以远超以往任何模型的准确性从网页中选取查询相关片段。"——Rahul Mohan，You.com高级AI工程师
- Zep评估了NVIDIA Nemotron 3 Embed 1B在Agent内存与上下文检索方面的表现。在早期内部基准测试中，与包括一些远大于Nemotron 3 Embed 1B的模型在内的多个模型相比，该模型在所有内存检索任务中排名第一。Zep认为，FP4检查点的可用性也使其在存储和延迟方面极具竞争力。
- Zoom正在评估NVIDIA Nemotron 3 Embed，用于支撑企业Agent搜索的检索层——该搜索驱动Zoom的上下文层，帮助Agent跨会议及工作场所知识源（包括文档、聊天、工单及其他内部系统）检索相关上下文。

## 快速上手

NVIDIA Nemotron 3 Embed以开放权重和开源训练方案发布，使组织能够完全控制检索模型在生产级AI应用中的定制与部署方式。

开发者可根据最适合其工作流的部署选项快速上手：

- Hugging Face——访问模型权重、模型卡以及面向SentenceTransformers、Transformers和vLLM的示例代码。
- NVIDIA NIM——在build.nvidia.com上访问经过优化的微服务，用于生产级推理。
- AI云与推理合作伙伴——通过领先的生态系统合作伙伴（Baseten、Bitdeer AI、DeepInfra、Friendli AI、OpenRouter）部署Nemotron 3 Embed。

对于需要领域适配或缩小模型规模的工作负载，我们还开源了NVIDIA NeMo AutoModeltraining方案：

- 微调方案——将Nemotron 3 Embed适配至您的企业语料库与检索任务。
- 蒸馏方案——在保持排序质量的同时压缩更大检索模型，用于生产部署。

例如，在NV Docs评估中，对Nemotron-3-Embed-1B-BF16进行微调后，NDCG@10从56.7%提升至63.3%（+11.6%），Recall@5从56.1%提升至62.8%（+11.9%）。

无论您是在构建企业搜索、生产级RAG、Agent内存、代码检索还是Agent AI系统，NVIDIA Nemotron 3 Embed都提供了灵活的部署选项——从Hugging Face上的开源模型到完全托管的AI云平台及NVIDIA NIM微服务。

探索这些模型，在您偏好的平台上部署它们，并告诉我们您正在构建什么。

---

> 本文由AI自动翻译，原文链接：[NVIDIA Nemotron 3 Embed Ranks #1 Overall on RTEB, Advancing Agentic Retrieval](https://huggingface.co/blog/nvidia/nemotron-3-embed-wins-rteb)
> 
> 翻译时间：2026-07-17 05:11
