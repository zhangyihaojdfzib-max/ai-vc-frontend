---
title: MMCTAgent：实现大规模视频库多模态推理的智能体系统
title_original: MMCTAgent enables multimodal reasoning over large video collections
date: '2025-11-12'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/mmctagent-enabling-multimodal-reasoning-over-large-video-and-image-collections/
author: Brenda Potts
summary: 本文介绍了多模态批判性思维智能体MMCTAgent，旨在解决现有AI模型在处理长视频和大规模视觉数据时面临的挑战。该系统基于AutoGen构建，采用规划者-批判者架构，通过迭代式推理循环分析复杂查询。MMCTAgent包含针对图像和视频的专用智能体，支持工具集成与模块化扩展，并采用先结构化摄取、再智能推理的两阶段设计，尤其擅长对长篇幅视频进行时序推理与跨模态对齐，提升了可解释性、可扩展性和推理准确性。
categories:
- AI研究
tags:
- 多模态AI
- 视频理解
- 智能体系统
- 迭代推理
- AutoGen
draft: false
translated_at: '2026-01-06T00:51:06.603Z'
---

现代多模态AI模型能够识别物体、描述场景并回答关于图像和短视频片段的问题，但在处理长篇幅和大规模视觉数据时却面临挑战，因为现实世界的推理需要超越物体识别和短片段分析。

现实世界的推理日益涉及分析长篇幅视频内容，其上下文跨度可达数分钟甚至数小时，远超大多数模型的上下文限制。它还需要在包含视频、图像和文本转录的海量多模态库中进行查询，其中寻找并整合相关证据需要的不仅仅是检索——它需要策略性推理。现有模型通常执行单次推理，产生一次性答案。这限制了它们处理需要时序推理、跨模态对齐和迭代优化的任务的能力。

**MMCTAgent**
为了应对这些挑战，我们开发了多模态批判性思维智能体，即MMCTAgent，用于对长篇幅视频和图像数据进行结构化推理。该智能体已在GitHub上开源（在新标签页中打开），并在Azure AI Foundry Labs上展示（在新标签页中打开）。

MMCTAgent基于微软开源的多智能体系统AutoGen构建，采用规划者-批判者架构提供多模态问答。这种设计实现了规划、反思和基于工具的推理，在多模态任务中连接了感知与深思熟虑。它将语言、视觉和时序理解联系起来，将静态的多模态任务转变为动态的推理工作流。

与产生一次性答案的传统模型不同，MMCTAgent拥有针对特定模态的智能体，包括ImageAgent和VideoAgent，它们包含诸如`get_relevant_query_frames()`或`object_detection-tool()`等工具。这些智能体执行审慎的、迭代式的推理——为每种模态选择合适的工具，评估中间结果，并通过批判者循环优化结论。这使得MMCTAgent能够以可解释性、可扩展性和可伸缩性，分析跨越长视频和大型图像库的复杂查询。

**播客系列**
**MMCTAgent如何工作**
MMCTAgent集成了两个协调的智能体：规划者和批判者，通过AutoGen进行编排。规划者智能体分解用户查询，识别合适的推理工具，执行多模态操作，并草拟初步答案。批判者智能体审查规划者的推理链，验证证据对齐情况，并为了事实准确性和一致性而优化或修订响应。

这种迭代式推理循环使MMCTAgent能够通过结构化的自我评估来改进其答案——将反思引入AI推理。MMCTAgent的一个关键优势在于其模块化的可扩展性。开发者可以通过将新的、特定领域的工具（如医学图像分析器、工业检测模型或专用检索模块）添加到ImageQnATools或VideoQnATools中，轻松集成它们。这种设计使MMCTAgent能够适应不同领域。

**VideoAgent：从摄取到长篇幅多模态推理**
VideoAgent将此架构扩展到长篇幅视频推理。它在两个相连的阶段中运行：库创建（摄取）和查询时推理。

**阶段 1 – 视频摄取与库创建**
在推理之前，长篇幅视频会经过一个摄取流程，该流程对齐多模态信息以便检索和理解：
- **转录与翻译**：将音频转换为文本，如果是多语言内容，则将转录文本翻译成一致的语言。
- **关键帧识别**：提取标记主要视觉或场景变化的代表性帧。
- **语义分块与章节生成**：将转录片段和视觉摘要组合成连贯的、按语义分段的章节，并关联关键帧。受微软Deep Video Discovery智能体搜索工具的启发，此步骤还会提取每个视频片段中存在的物体、屏幕文本和角色的详细描述，并将这些洞察直接整合到相应的章节中。
- **多模态嵌入创建**：为关键帧生成图像嵌入，并将其链接到对应的转录文本和章节数据。

所有结构化元数据，包括转录文本、视觉摘要、章节和嵌入，都使用Azure AI Search（在新标签页中打开）索引到多模态知识库中，这为可扩展的语义检索和下游推理奠定了基础。

**阶段 2 – 视频问答与推理**
当用户提交查询时，VideoAgent使用专门的规划者和批判者工具，在索引的视频内容中进行检索、分析和推理。

**规划者工具**
- `get_video_analysis`：查找最相关的视频，提供摘要，并列出检测到的物体。
- `get_context`：从Azure AI Search索引中检索上下文信息和相关章节。
- `get_relevant_frames`：选择与用户查询最相关的关键帧。
- `query_frame`：对选定的帧执行详细的视觉和文本推理。
- `get_context`和`get_relevant_frames`协同工作，确保推理从语义上最相关的证据开始。

**批判者工具**
- `critic_tool`：评估推理输出在时序对齐、事实准确性以及视觉与文本模态间一致性方面的表现。

这种两阶段设计——先进行结构化摄取，再进行智能体推理——使MMCTAgent能够为信息密集的长视频提供准确、可解释的洞察。

**ImageAgent：静态视觉的结构化推理**
VideoAgent处理长篇幅视频的时序推理，而ImageAgent则将相同的规划者-批判者范式应用于静态视觉分析。它对图像执行模块化的、基于工具的推理，将用于识别、检测和光学字符识别的感知工具与用于解释和说明的基于语言的推理相结合。

**规划者工具**
- `vit_tool`：利用Vision Transformer或视觉语言模型进行高级视觉理解和描述。
- `recog_tool`：执行场景、人脸和物体识别。
- `object_detection_tool`：定位并标注图像中的实体。
- `ocr_tool`：从视觉元素中提取嵌入的文本。

**批判者工具**
- `critic_tool`：验证规划者结论的事实对齐性和一致性，优化最终响应。

这种轻量级的ImageAgent为图像集合提供了细粒度的、可解释的推理——支持视觉问答、内容检查和多模态检索——同时保持了与VideoAgent的架构对称性。

**评估结果**
为了评估MMCTAgent的有效性，我们使用多个基础LLM模型以及一系列基准数据集和现实场景对ImageAgent和VideoAgent进行了评估。部分关键结果如下所示。

| 图像数据集 | GPT-4V | MMCT with GPT-4V | GPT4o | MMCT with GPT-4o | GPT-5 | MMCT with GPT-5 |
|---|---|---|---|---|---|---|
| MM-Vet [1] | 60.20 | 74.24 | 77.98 | 79.36 | 80.51 | 81.65 |
| MMMU [2] | 56.80 | 63.57 | 69.10 | 73.00 | 84.20 | 85.44 |

| 视频数据集 | GPT4o | MMCT with GPT-4o |
|---|---|---|
| VideoMME [3] | 72.10 | 76.70 |

MMCTAgent通过为较弱模型配备物体检测和光学字符识别等适当工具，或为较强模型配备特定领域工具，来增强基础模型的性能，从而带来显著改进。例如，集成这些工具将GPT-4V在MM-Vet数据集上的准确率从60.20%提升至74.24%。此外，可配置的批判者智能体提供了额外的验证，这在关键领域尤其有价值。更多评估结果可在此处查看（在新标签页中打开）。

**要点与后续步骤**
MMCTAgent展示了一种采用规划者-批判者架构的、可扩展的智能体方法来进行多模态推理。

其统一的多模态设计同时支持图像与视频处理流程，而可扩展的工具链则能快速集成特定领域的工具与能力。它提供Azure原生部署支持，并可在更广泛的开源生态系统中进行配置。

展望未来，我们致力于提升检索与推理工作流的效率与适应性，并将MMCTAgent的应用拓展至当前农业评估之外的领域，通过"壁虎计划"等项目探索新的现实场景，以推动为全球用户开发易于使用、具有创新性的多模态应用。

**致谢**  
我们要感谢团队成员对本工作的宝贵贡献：Aman Patkar、Ogbemi Ekwejunor-Etchie、Somnath Kumar、Soumya De 和 Yash Gadhia。

**参考文献**  
[1] W. Yu, Z. Yang, L. Li, J. Wang, K. Lin, Z. Liu, X. Wang, and L. Wang. “MM-VET: Evaluating large multimodal models for integrated capabilities”, 2023.  
[2] X. Yue, Y. Ni, K. Zhang, T. Zheng, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, C. Wei, B. Yu, R. Yuan, R. Sun, M. Yin, B. Zheng, Z. Yang, Y. Liu, W. Huang, H. Sun, Y. Su, and W. Chen. “MMMU: A massive multi-discipline multimodal understanding and reasoning benchmark for expert AGI”, 2023.  
[3] Chaoyou Fu, Yuhan Dai, Yondong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou, Yunhang Shen, Mengdan Zhang, et al. “Video-MME: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis”, 2024.

> 本文由AI自动翻译，原文链接：[MMCTAgent enables multimodal reasoning over large video collections](https://www.microsoft.com/en-us/research/blog/mmctagent-enabling-multimodal-reasoning-over-large-video-and-image-collections/)
> 
> 翻译时间：2026-01-06 00:51
