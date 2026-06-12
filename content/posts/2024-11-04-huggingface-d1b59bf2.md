---
title: Argilla 2.4：零代码在Hub上构建AI数据集
title_original: 'Argilla 2.4: Easily Build Fine-Tuning and Evaluation Datasets on
  the Hub — No Code Required'
date: '2024-11-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/argilla-ui-hub
author: ''
summary: Argilla 2.4版本推出了一项重大功能：无需编写任何代码，即可从Hugging Face Hub导入数据集、定义问题并收集人类反馈，用于微调或评估AI模型。该工具面向AI开发者和领域专家，支持社区协作，简化了从23万个公开数据集中筛选、标注和改进数据的过程。用户只需部署Argilla
  Space，即可通过UI操作，适合开源数据集贡献、从头标注或优化现有数据集等场景。
categories:
- AI产品
tags:
- Argilla
- Hugging Face Hub
- 数据集构建
- 零代码
- 人类反馈
draft: false
translated_at: '2026-06-12T06:35:58.861784'
---

# Argilla 2.4：轻松在Hub上构建微调和评估数据集——无需代码

我们无比激动地分享自Argilla加入Hugging Face以来最具影响力的功能：无需任何代码即可准备AI数据集，从任意Hub数据集开始！使用Argilla的UI，您可以轻松从Hugging Face Hub导入数据集、定义问题，并开始收集人类反馈。

不熟悉Argilla？Argilla是一款免费的开源数据导向工具。通过Argilla，AI开发者和领域专家可以协作构建高质量数据集。Argilla是Hugging Face家族的一员，并与Hub完全集成。想了解更多？这里有篇介绍博客文章。

为什么这项新功能对您和社区如此重要？

- Hugging Face Hub包含23万个数据集，可作为您AI项目的基础。
- 它简化了从Hugging Face社区或专业团队收集人类反馈的过程。
- 它让对特定领域有深入了解但不熟悉编写代码的用户也能创建数据集。

## 使用场景

这项新功能让在Hub上构建高质量数据集变得更加普及：

- 如果您已发布开源数据集并希望社区贡献，将其导入公共Argilla Space并分享URL给全世界！
- 如果您想从头开始标注新数据集，将CSV上传至Hub，导入到您的Argilla Space，然后开始标注！
- 如果您想为微调或评估模型而整理现有Hub数据集，将其导入Argilla Space并开始筛选！
- 如果您想改进现有Hub数据集以造福社区，将其导入Argilla Space并开始提供反馈！

## 工作原理

首先，您需要部署Argilla。推荐方式是按照此指南在Spaces上部署。默认部署已启用Hugging Face OAuth，这意味着您的Space将对任何Hub用户开放标注贡献。当您希望社区为数据集做贡献时，OAuth是理想选择。如果您希望仅限您和其他协作者进行标注，请查看此指南了解额外配置选项。

Argilla运行后，登录并点击首页上的"从Hugging Face导入数据集"按钮。您可以从我们的示例数据集开始，或输入要使用的数据集的仓库ID。

在此初始版本中，Hub数据集必须为公开。如果您对私有数据集支持感兴趣，欢迎在GitHub上告诉我们。

Argilla会根据数据集特征自动建议初始配置，因此您无需从头开始，但可以添加问题或删除不必要的字段。字段应包含您希望获得反馈的数据，如文本、对话或图像。问题则是您希望收集的反馈，如标签、评分、排名或文本。所有更改都会实时显示，因此您可以清晰了解正在配置的Argilla数据集。

对结果满意后，点击"创建数据集"以导入配置好的数据集。现在您可以开始提供反馈了！

您可以按照快速入门指南自行尝试，整个过程不到5分钟！

这个新工作流程简化了从Hub导入数据集的过程，但如果您需要进一步定制，仍可使用Argilla的Python SDK导入数据集。

我们期待听到您的想法和初次体验。请在GitHub或HF Discord上告诉我们！

---

> 本文由AI自动翻译，原文链接：[Argilla 2.4: Easily Build Fine-Tuning and Evaluation Datasets on the Hub — No Code Required](https://huggingface.co/blog/argilla-ui-hub)
> 
> 翻译时间：2026-06-12 06:35
