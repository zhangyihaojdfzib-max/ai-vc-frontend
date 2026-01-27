---
title: NVIDIA Earth-2开源三款气象AI模型，覆盖完整预报技术栈
title_original: '**NVIDIA Earth-2 Open Models Span the Whole Weather Stack**'
date: '2026-01-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/earth-2-open-models
author: ''
summary: NVIDIA宣布推出Earth-2开源模型家族，包含临近预报、中期预报和全球数据同化三款新模型，分别由StormScope、Atlas和HealDA架构驱动。这些模型覆盖从数据同化到预报的完整气象技术栈，能够在GPU上快速生成高精度天气预报，支持开发者利用自有数据和基础设施构建自主的气象预测能力。相关模型及配套工具Earth2Studio已在Hugging
  Face平台发布。
categories:
- AI产品
tags:
- NVIDIA
- 气象预报
- 生成式AI
- 开源模型
- AI基础设施
draft: false
translated_at: '2026-01-27T00:47:28.066861'
---

# NVIDIA Earth-2 开源模型覆盖完整气象技术栈

NVIDIA 兴奋地宣布，作为 NVIDIA Earth-2 家族的一部分，推出三款新的开源模型。这使得构建覆盖整个气象技术栈的天气预报能力变得前所未有的简单，包括数据同化、预报、临近预报、降尺度等任务。此外，开发者可以使用 NVIDIA 开源软件快速开始构建天气和气候模拟：使用 **Earth2Studio** 创建推理管道，使用 **Physics Nemo** 训练模型。

NVIDIA Earth-2 包含一套加速工具和模型，使开发者能够将通常分散的天气和气候 AI 能力整合在一起。由于 Earth-2 是完全开放的，开发者可以根据自己的特定需求，使用自己的数据和基础设施，定制和微调他们的模拟，从而构建完全拥有和控制的自主天气与气候预测能力。Earth-2：

- 是一套领先的开源天气和气候模型
- 得益于开源软件生态系统，易于使用
- 使您能够创建自己的自主能力

## Earth-2 临近预报：公里级恶劣天气预测

现已在 Hugging Face 发布：**Earth-2 临近预报**，由名为 StormScope 的新模型架构驱动，利用生成式 AI 在几分钟内生成国家尺度的公里级分辨率、零到六小时的局地风暴和危险天气预测。Earth-2 临近预报通过直接模拟风暴动力学，可以生成首个在短期降水预报上超越传统基于物理的天气预报模型的预测。它利用 AI 直接预测卫星和雷达数据。

此版本直接在美国本土（CONUS）上空可用的全球静止卫星观测数据（GOES）上进行训练。然而，该方法也可应用于在具有类似卫星覆盖的其他区域训练模型版本。

研究论文：从观测中学习精确的风暴尺度演变

## Earth-2 中期预报：高精度 15 天全球预报

现已在 Hugging Face 发布：**Earth-2 中期预报**，由名为 Atlas 的新模型架构驱动，能够对包括温度、气压、风和湿度在内的 70 多个气象变量进行高精度的中期预报（即最多提前 15 天的预报）。它使用潜在扩散 Transformer 架构来预测大气中的增量变化，从而保留关键的大气结构并减少预报误差。在标准基准测试中，它在行业最常测量的预报变量上，表现优于 GenCast 等领先的开源模型。

研究论文：揭秘数据驱动的概率性中期天气预报

## Earth-2 全球数据同化：端到端 AI 管道

即将登陆 Hugging Face：**Earth-2 全球数据同化**，由名为 HealDA 的新模型架构驱动，该架构为天气预报生成初始条件——即当前大气的快照，包括全球数千个地点的温度、风速、湿度和气压。Earth-2 全球数据同化可以在 GPU 上几秒钟内生成初始条件，而不是在超级计算机上花费数小时。当与 Earth-2 中期预报结合时，这将产生由开放的、完全 AI 驱动的管道所生成的最具技巧性的预报预测。

研究论文：HealDA：强调初始误差在端到端 AI 天气预报中的重要性

这些模型加入了已有的 NVIDIA 开源天气和气候模型行列，如 FourcastNet3、CorrDiff、cBottle、DLESym 等。

# 快速开始

NVIDIA **Earth2Studio** 是一个开源 Python 生态系统，用于快速创建强大的 AI 天气和气候模拟。它提供了所有必要的推理工具，以便开始使用 Hugging Face 上的新模型检查点。操作非常简单：

快速开始视频

# 资源

公司博客：NVIDIA 推出 Earth-2 开源模型家族——全球首个用于 AI 气象的完全开源模型和工具集

发布视频：NVIDIA Earth-2：AI 气象预报的未来是开放的

网页：Earth-2

Earth-2 临近预报的 Hugging Face 包

Earth-2 中期预报的 Hugging Face 包

---

> 本文由AI自动翻译，原文链接：[**NVIDIA Earth-2 Open Models Span the Whole Weather Stack**](https://huggingface.co/blog/nvidia/earth-2-open-models)
> 
> 翻译时间：2026-01-27 00:47
