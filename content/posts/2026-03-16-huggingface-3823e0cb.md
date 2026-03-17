---
title: 首个医疗机器人数据集Open-H-Embodiment及基础物理AI模型发布
title_original: The First Healthcare Robotics Dataset and Foundational Physical AI
  Models for Healthcare Robotics
date: '2026-03-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/physical-ai-for-healthcare-robotics
author: ''
summary: 本文介绍了由全球35个组织共同构建的首个大规模医疗机器人开放数据集Open-H-Embodiment，包含778小时的训练数据，涵盖手术、超声等领域。基于此数据集，研究团队发布了GR00T-H视觉语言动作模型和Cosmos-H-Surgical-Simulator世界基础模型，旨在解决医疗机器人领域缺乏标准化数据、仿真与现实差距等挑战，为医疗物理AI的发展奠定基础。
categories:
- AI研究
tags:
- 医疗机器人
- 人工智能
- 数据集
- 物理AI
- 手术机器人
draft: false
translated_at: '2026-03-17T04:33:35.226695'
---

# 首个医疗机器人数据集及医疗机器人基础物理AI模型

## 介绍Open-H-Embodiment：首个由社区协作构建的医疗机器人开放数据集

作者：Nigel Nelson, Lukas Zbinden, Mostafa Toloui, Sean Huver

医疗AI主要基于感知，专注于解读信号并对病理/解剖结构进行分类或分割的模型。然而，医疗涉及"操作"，这使得过去缺乏具身性、接触动力学和闭环控制的静态、纯感知数据集显得不足。该领域需要标准化的机器人本体、同步的视觉-力-运动学数据、仿真到现实的配对以及跨本体基准，为物理AI奠定基础。

## 1. Open-H-Embodiment

Open-H-Embodiment是一项社区驱动的数据集计划，旨在为手术机器人和超声AI自主性与世界基础模型的训练和评估构建开放、共享的基础。该计划由包括Axel Krieger教授（约翰斯·霍普金斯大学）、Nassir Navab教授（慕尼黑工业大学）和Mahdi Azizian博士（英伟达）在内的指导委员会发起，现已涵盖35个组织。

来自世界各地的参与者共同构建了首个大规模数据集，以推动医疗机器人领域物理AI事业的发展。

Open-H-Embodiment 样本数据

![open_h_sample](/images/posts/4a8de73848e3.png)

### 参与者

Balgrist, CMR Surgical, 香港中文大学, 大湾区大学, 香港浸会大学, Hamlyn, ImFusion, 约翰斯·霍普金斯大学, 利兹大学, 穆罕默德·本·扎耶德人工智能大学, Moon Surgical, 英伟达, Northwell Health, 奥布达大学, 香港理工大学, 山东大学齐鲁医院, Rob Surgical, Sanoscience, 手术数据科学联盟, Semaphor Surgical, 斯坦福大学, 德累斯顿工业大学, 慕尼黑工业大学, 拓道, 都灵, 不列颠哥伦比亚大学, 加州大学伯克利分校, 加州大学圣地亚哥分校, 伊利诺伊大学芝加哥分校, 田纳西大学, 德克萨斯大学, 范德堡大学, 以及 Virtual Incision。

### 数据集

- 包含**778小时**的CC-BY-4.0许可的医疗机器人训练数据，主要为手术机器人数据，但也包含超声和结肠镜检查自主性数据。
- 涵盖仿真、台架练习（如缝合）和真实临床手术。
- 使用商业机器人（CMR Surgical, Rob Surgical, 拓道）和研究机器人（dVRK, Franka, Kuka）。
- 随数据集一同发布的还有两个基于此数据后训练、采用宽松开源许可的新模型。

## 2. GR00T-H：用于手术机器人的视觉语言动作模型

首先是GR00T-H，它是Isaac GR00T N系列视觉-语言-动作模型的一个衍生版本。基于约600小时的Open-H-Embodiment数据训练，GR00T-H是首个用于手术机器人任务的政策模型。

基于英伟达的开源生态系统，Isaac GR00T-H利用Cosmos Reason 2 2B作为其视觉语言模型骨干。

![pyramid](/images/posts/b67e33016915.jpg)

### 架构设计选择

手术机器人需要高精度，但专用硬件（如线缆驱动系统）使得模仿学习变得困难。为了解决这个问题，GR00T-H采用了四个关键设计选择：

- **独特的本体投影器**：一个独特的、可学习的MLP将每个机器人的特定运动学映射到一个共享的、归一化的动作空间。
- **状态丢弃（100%）**：在推理过程中丢弃本体感受输入，为每个系统创建一个学习到的偏置项，从而在现实世界中获得更好的结果。
- **相对末端执行器动作**：训练使用一个通用的相对末端执行器动作空间，以克服运动学不一致性。
- **任务提示词中的元数据**：器械名称和控制索引映射被直接注入到VLM任务提示词中。

GR00T-H的原型已在**SutureBot基准测试**中展示了执行完整端到端缝合的能力，突显了其强大的长时程灵巧性。

GR00T-H执行端到端缝合。

![gr00t_suture](/images/posts/dd2aad39c021.gif)

## 3. Cosmos-H-Surgical-Simulator

Cosmos-H-Surgical-Simulator是一个用于动作条件化手术机器人的世界基础模型。传统仿真器因软组织、反光、血液和烟雾等现实世界的复杂性而失效。

### 关键能力

- **克服仿真到现实的差距**：基于英伟达Cosmos Predict 2.5 2B微调，它能直接从运动学动作生成物理上合理的手术视频。
- **效率提升**：对于600次推演，仿真仅需**40分钟**，而使用现实世界台架方法则需要**2天**。
- **WFM作为物理仿真器**：从数据中隐式学习组织形变和器械交互。
- **合成数据生成**：生成逼真的合成视频-动作对，以增强代表性不足的数据集。

![cosmos_h_surg_sim](/images/posts/7707ef902458.gif)

### 微调细节

该模型在Open-H-Embodiment数据集（9种机器人本体，32个数据集）上进行了微调，使用了64块A100 GPU，耗时约10,000 GPU小时。它采用了一个统一的44维动作空间。

## 4. 未来展望：迈向手术机器人推理

Open-H-Embodiment计划第二版的目标是超越感知控制，实现具备推理能力的自主性——即手术机器人的"ChatGPT时刻"——使系统能够在长时间手术中解释、规划和适应。这需要将Open-H-Embodiment扩展为支持推理的数据，其中包含捕获意图、结果和失败模式的任务轨迹标注。这项工作需要社区的参与，我们邀请您加入。访问我们的**Open-H GitHub仓库**，共同塑造医疗机器人的未来。

## 5. 立即开始

访问以下资源，开始使用Open-H-Embodiment数据集和模型：

- **Open-H-Embodiment**：HF数据集 / GitHub仓库
- **英伟达 Isaac GR00T-H 模型**：HF模型 / GR00T-H GitHub仓库
- **英伟达 Cosmos-H-Surgical-Simulator**：HF模型 / GitHub仓库
- **Cosmos Cookbook**：分步工作流，指导您为自己的机器人本体构建自己的WFM。
- **在 Hugging Face 上探索**：在 Hugging Face 和 GitHub 上查看新的开源 Cosmos 模型和数据集，或在 build.nvidia.com 上试用模型。

---

> 本文由AI自动翻译，原文链接：[The First Healthcare Robotics Dataset and Foundational Physical AI Models for Healthcare Robotics](https://huggingface.co/blog/nvidia/physical-ai-for-healthcare-robotics)
> 
> 翻译时间：2026-03-17 04:33
