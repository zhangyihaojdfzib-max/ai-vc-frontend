---
title: ScreenAI：谷歌推出理解界面与视觉语言的视觉语言模型
title_original: 'ScreenAI: A visual language model for UI and visually-situated language
  understanding'
date: '2024-03-19'
source: Google AI Blog
source_url: http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html
author: null
summary: 谷歌研究团队推出ScreenAI，这是一个基于PaLI架构改进的视觉语言模型，专门用于理解用户界面（UI）和信息图等视觉内容。模型采用pix2struct的灵活分块策略，仅50亿参数，通过结合自监督学习与LLM自动生成数据，在UI导航、图表问答、文档理解等多项任务上取得了同类尺寸模型的最佳性能。文章还介绍了其两阶段训练方法、基于布局标注和LLM的数据生成流程，并发布了用于评估的新数据集。
categories:
- AI研究
tags:
- 视觉语言模型
- 用户界面理解
- 多模态AI
- 谷歌研究
- 信息图理解
draft: false
translated_at: '2026-01-05T16:35:07.380Z'
---

ScreenAI：用于界面与视觉语言理解的视觉语言模型  
2024年3月19日  
作者：Google Research 软件工程师 Srinivas Sunkara 与 Gilles Baechler  
快速链接  

屏幕用户界面（UI）与信息图（如图表、图示和表格）在人类交流和人机交互中扮演着重要角色，它们提供了丰富且交互性强的用户体验。UI和信息图共享相似的设计原则和视觉语言（如图标和布局），这为构建能够理解、推理并与这些界面交互的单一模型提供了机会。然而，由于其复杂性和多样的呈现形式，信息图和UI带来了独特的建模挑战。

为此，我们推出“ScreenAI：用于UI与信息图理解的视觉语言模型”。ScreenAI基于PaLI架构改进，并采用了pix2struct的灵活分块策略。我们在多种数据集和任务的独特组合上训练ScreenAI，其中包括一项新颖的屏幕标注任务，要求模型识别屏幕上的UI元素信息（即类型、位置和描述）。这些文本标注为大语言模型（LLM）提供了屏幕描述，使其能够自动大规模生成问答（QA）、UI导航和摘要训练数据集。ScreenAI仅拥有50亿参数，却在UI和信息图相关任务（WebSRC和MoTIF）上取得了最先进的结果，并在Chart QA、DocVQA和InfographicVQA上实现了同类尺寸模型中的最佳性能。我们还发布了三个新数据集：Screen Annotation（用于评估模型的布局理解能力），以及ScreenQA Short和Complex ScreenQA（用于更全面评估其问答能力）。

**ScreenAI**  
ScreenAI的架构基于PaLI，由多模态编码器块和自回归解码器组成。PaLI编码器使用视觉Transformer（ViT）创建图像嵌入，以及一个多模态编码器，该编码器将图像和文本嵌入的拼接作为输入。这种灵活的架构使ScreenAI能够解决可重构为“文本+图像到文本”问题的视觉任务。

在PaLI架构之上，我们采用了pix2struct引入的灵活分块策略。不使用固定的网格模式，而是选择能保持输入图像原始纵横比的网格尺寸。这使得ScreenAI能够在各种纵横比的图像上良好工作。

ScreenAI模型的训练分为两个阶段：预训练阶段和微调阶段。首先，应用自监督学习自动生成数据标签，然后使用这些标签训练ViT和语言模型。在微调阶段，ViT被冻结，此阶段使用的大部分数据由人工标注员手动标注。

**数据生成**  
为了创建ScreenAI的预训练数据集，我们首先从各种设备（包括台式机、手机和平板电脑）收集了大量截图。这是通过使用可公开访问的网页，并遵循为RICO数据集（针对移动应用）使用的程序化探索方法实现的。然后，我们应用基于DETR模型的布局标注器，识别并标注广泛的UI元素（如图像、象形图、按钮、文本）及其空间关系。象形图使用能够区分77种不同图标类型的图标分类器进行进一步分析。这种详细的分类对于解读图标传达的微妙信息至关重要。对于分类器未覆盖的图标，以及信息图和图像，我们使用PaLI图像描述模型生成提供上下文信息的描述性标题。我们还应用光学字符识别（OCR）引擎来提取和标注屏幕上的文本内容。我们将OCR文本与之前的标注结合，创建每个屏幕的详细描述。

**基于LLM的数据生成**  
我们使用PaLM 2通过两步流程生成输入-输出对，以增强预训练数据的多样性。首先，使用上述技术生成屏幕标注，然后围绕此模式设计提示词，让LLM创建合成数据。此过程需要提示词工程和迭代优化以找到有效的提示词。我们通过人工验证，根据质量阈值评估生成数据的质量。

> 你只能说JSON。不要写非JSON的文本。
> 给你以下用文字描述的移动截图。你能生成5个关于截图内容的问题以及相应的简短答案吗？
> 答案应尽可能简短，只包含必要信息。你的答案应结构如下：
> questions: [
> {{question: 问题,
> answer: 答案
> }},
> ...
> ]
> {屏幕模式}

通过将LLM的自然语言能力与结构化模式相结合，我们模拟了广泛的用户交互和场景，以生成合成的、现实的任务。具体来说，我们生成了三类任务：
- **问答**：要求模型回答关于截图内容的问题，例如：“餐厅什么时候开门？”
- **屏幕导航**：要求模型将自然语言表达转换为屏幕上的可执行操作，例如：“点击搜索按钮。”
- **屏幕摘要**：要求模型用一两句话总结屏幕内容。

**实验与结果**  
如前所述，ScreenAI的训练分为两个阶段：预训练和微调。预训练数据标签通过自监督学习获得，微调数据标签来自人工标注员。

我们使用公开的QA、摘要和导航数据集，以及与UI相关的各种任务对ScreenAI进行微调。对于QA，我们使用多模态和文档理解领域的成熟基准，如ChartQA、DocVQA、Multi page DocVQA、InfographicVQA、OCR VQA、Web SRC和ScreenQA。对于导航，使用的数据集包括Referring Expressions、MoTIF、Mug和Android in the Wild。最后，我们使用Screen2Words进行屏幕摘要。除了微调数据集，我们还使用三个新颖的基准评估微调后的ScreenAI模型：
- **Screen Annotation**：用于评估模型布局标注和空间理解能力。
- **ScreenQA Short**：ScreenQA的一个变体，其标准答案已被缩短，仅包含与其他QA任务更一致的相关信息。
- **Complex ScreenQA**：通过更困难的问题（计数、算术、比较和无法回答的问题）以及包含各种纵横比屏幕的截图，对ScreenQA Short进行补充。

与同类尺寸模型相比，微调后的ScreenAI模型在各种UI和信息图相关任务（WebSRC和MoTIF）上取得了最先进的结果，并在Chart QA、DocVQA和InfographicVQA上实现了同类最佳性能。ScreenAI在Screen2Words和OCR-VQA上也取得了有竞争力的表现。此外，我们在新引入的基准数据集上报告了结果，以作为进一步研究的基线。

接下来，我们研究了ScreenAI的扩展能力，并观察到在所有任务中，增加模型规模都能提升性能，并且在最大规模时改进尚未饱和。

**结论**  
我们介绍了ScreenAI模型以及一种统一的表示方法，使我们能够利用来自所有这些领域的数据开发自监督学习任务。我们还阐述了使用LLM进行数据生成的影响，并研究了通过修改训练组合来提升模型在特定方面的性能。

我们运用所有这些技术构建了多任务训练模型，这些模型在多项公开基准测试中达到了与最先进方法相竞争的水平。然而，我们也注意到，我们的方法仍落后于大型模型，需要进一步研究以弥合这一差距。

**致谢**

本项目是与Maria Wang、Fedir Zubach、Hassan Mansoor、Vincent Etter、Victor Carbune、Jason Lin、Jindong Chen以及Abhanshu Sharma共同合作的成果。我们感谢Fangyu Liu、Xi Chen、Efi Kokiopoulou、Jesse Berent、Gabriel Barcik、Lukas Zilka、Oriana Riva、Gang Li、Yang Li、Radu Soricut和Tania Bedrax-Weiss富有洞见的反馈与讨论，同时感谢Rahul Aralikatte、Hao Cheng和Daniel Kim在数据准备方面提供的支持。我们也感谢Jay Yagnik、Blaise Aguera y Arcas、Ewa Dominowska、David Petrou和Matt Sharifi的领导力、远见与支持。我们特别感谢Tom Small协助我们制作了本文中的动画。

> 本文由AI自动翻译，原文链接：[ScreenAI: A visual language model for UI and visually-situated language understanding](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)
> 
> 翻译时间：2026-01-05 13:06
