---
title: NVIDIA GTC 2025发布物理AI开源模型与数据集
title_original: 'NVIDIA''s GTC 2025 Announcement for Physical AI Developers: New Open
  Models and Datasets'
date: '2025-03-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia-physical-ai
author: ''
summary: NVIDIA在GTC 2025大会上发布了三项突破性开源成果，加速物理AI开发：Cosmos Transfer世界基础模型（70亿参数）支持多控制机制生成高保真虚拟场景；开源物理AI数据集包含15TB数据、32万条机器人轨迹及1000个OpenUSD资产；以及全球首个面向人形机器人的开源基础模型Isaac
  GR00T N1，具备多模态输入和跨具身操作能力。这些成果为机器人系统和自动驾驶技术提供了强大工具。
categories:
- AI产品
tags:
- NVIDIA
- 物理AI
- 人形机器人
- 世界基础模型
- 开源数据集
draft: false
translated_at: '2026-05-07T05:31:22.499360'
---

# NVIDIA GTC 2025 面向物理AI开发者的公告：全新开源模型与数据集

![人形机器人抓取与放置](/images/posts/95b643234c9f.gif)

在年度GTC大会上，NVIDIA发布了三项突破性的开源成果，旨在加速物理AI开发。全新推出的多控制世界基础模型（WFM）套件——Cosmos Transfer、精心策划的物理AI数据集，以及首个面向通用人形机器人推理的开源模型——NVIDIA Isaac GR00T N1，标志着物理AI技术的重大飞跃，为开发者提供了推进机器人系统和增强自动驾驶技术的强大工具与资源。

## 全新世界基础模型——Cosmos Transfer

Cosmos Transfer是NVIDIA Cosmos™世界基础模型（WFM）系列的最新成员，在生成虚拟世界场景方面引入了全新的控制层级与精度。

该模型拥有70亿参数规模，利用多控制机制从结构化输入引导生成高保真世界场景，确保精确的空间对齐与场景构图。

### 工作原理

该模型通过为用于捕捉模拟世界的每种传感器模态分别训练独立的ControlNet来构建。

![3D边界框地图输入](/images/posts/d7431a61b067.gif)

![轨迹地图输入](/images/posts/d0bf5f499d6c.gif)

![深度地图输入](/images/posts/9eccf72efe7e.gif)

![分割地图输入](/images/posts/7deb52bf597d.gif)

输入类型包括3D边界框地图、轨迹地图、深度地图、分割地图。

- 在推理时，开发者可以使用多种输入类型，包括结构化视觉或几何数据（如分割地图、深度地图、边缘地图、人体运动关键点、激光雷达扫描、轨迹、高清地图和3D边界框）来引导输出。
- 每个控制分支的控制信号会乘以对应的自适应时空控制地图，然后求和，再添加到基础模型的Transformer模块中。
- 生成的输出是具备可控布局、物体放置和运动的逼真视频序列。开发者可以通过多种方式控制输出，例如保留结构与外观，或在保持结构的同时允许外观变化。

![输出1](/images/posts/1863bd74eaa4.gif)

![输出2](/images/posts/e342d9936a13.gif)

![输出3](/images/posts/fed30b3cd847.gif)

Cosmos Transfer在不同环境和天气条件下的输出。

Cosmos Transfer与NVIDIA Omniverse平台相结合，正在推动面向机器人和自动驾驶开发的大规模可控合成数据生成。在GitHub上查看更多Cosmos Transfer示例。

基于后训练基础模型构建的Cosmos Transfer样本也可用于自动驾驶。

## 开源物理AI数据集

NVIDIA还发布了物理AI数据集，这是一个在Hugging Face上用于开发物理AI的开源数据集。这个商业级、经过预验证的数据集包含15TB数据，涵盖超过32万条用于机器人训练的轨迹，以及多达1000个通用场景描述（OpenUSD）资产，其中包括一个SimReady集合。

该数据集专为Cosmos Predict等世界基础模型的后训练而设计，为开发者提供高质量、多样化的数据以增强其AI模型。

## 专为人形机器人设计的模型——NVIDIA Isaac GR00T N1

另一项令人振奋的发布是NVIDIA Isaac GR00T N1，这是全球首个面向通用人形机器人推理与技能的开源基础模型。这种跨具身模型接收多模态输入（包括语言和图像），在不同环境中执行操作任务。NVIDIA Isaac GR00T-N1-2B模型已在Hugging Face上提供。

Isaac GR00T N1在广泛的人形机器人数据集上进行了训练，该数据集包含真实采集数据、使用NVIDIA Isaac GR00T蓝图组件生成的合成数据，以及互联网规模的视频数据。它可通过针对特定具身形态、任务和环境的后续训练进行适配。

Isaac GR00T N1使用单一模型和权重集，能够在多种人形机器人（如Fourier GR-1和1X Neo）上实现操作行为。它在各类任务中展现出强大的泛化能力，包括用单臂或双臂抓取和操作物体，以及在双臂之间转移物品。它还能执行需要持续上下文理解和多种技能整合的复杂多步骤任务。这些能力使其非常适合物料搬运、包装和检测等应用场景。

Isaac GR00T N1采用受人类认知启发的双系统架构，包含以下互补组件：

- 视觉语言模型（系统2）：这一系统性思维模型基于NVIDIA-Eagle与SmolLM-1.7B。它通过视觉和语言指令解读环境，使机器人能够推理环境与指令，并规划正确的行动。
- 扩散Transformer（系统1）：这一动作模型生成连续动作以控制机器人运动，将系统2制定的行动计划转化为精确、连续的机器人运动。

## 未来路径

后训练是推进自主系统、为下游物理AI任务创建专用模型的前进方向。

请查看GitHub上的Cosmos Predict和Cosmos Transfer推理脚本。阅读Cosmos Transfer研究论文以获取更多详情。

NVIDIA Isaac GR00T-N1-2B模型已在Hugging Face上提供。使用自定义用户数据集进行后训练的样本数据集和PyTorch脚本（兼容Hugging Face LeRobot格式）已在GitHub上提供。有关Isaac GR00T N1模型的更多信息，请参阅研究论文。

在Hugging Face上关注NVIDIA以获取更多更新。

---

> 本文由AI自动翻译，原文链接：[NVIDIA's GTC 2025 Announcement for Physical AI Developers: New Open Models and Datasets](https://huggingface.co/blog/nvidia-physical-ai)
> 
> 翻译时间：2026-05-07 05:31
