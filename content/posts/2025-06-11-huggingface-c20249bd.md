---
title: Hugging Face与NVIDIA合作推出训练集群即服务
title_original: Introducing Training Cluster as a Service - a new collaboration with
  NVIDIA
date: '2025-06-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia-training-cluster
author: ''
summary: Hugging Face与NVIDIA在巴黎GTC大会上联合宣布推出“训练集群即服务”，旨在降低大规模GPU集群的获取门槛。该服务整合了NVIDIA
  DGX Cloud的先进算力与Hugging Face的开源平台，允许研究机构按需申请GPU资源，并按使用时长付费。文中列举了该服务在罕见遗传病研究、数学AI及材料科学等领域的应用案例，强调其将助力全球AI研究社区更便捷地获取高性能计算资源，推动前沿模型的开发。
categories:
- AI基础设施
tags:
- 训练集群即服务
- Hugging Face
- NVIDIA
- GPU集群
- AI算力
draft: false
translated_at: '2026-04-03T04:58:46.374515'
---

# 推出训练集群即服务——与NVIDIA的全新合作

在今天的巴黎GTC大会上，我们激动地宣布与NVIDIA合作推出**训练集群即服务**，旨在让全球研究机构更便捷地获取大规模GPU集群，从而能够在各个领域训练未来的基础模型。

## 让GPU集群触手可及

许多千兆瓦级别的GPU超级集群项目正在建设中，以训练下一代AI模型。这似乎使得“GPU匮乏者”与“GPU富足者”之间的算力差距正在迅速扩大。但实际上，GPU资源是存在的，因为超大规模云服务商、区域性和AI原生云提供商都在快速扩张其容量。

那么，我们如何将AI算力与需要它的研究人员连接起来？我们如何让全球的大学、国家研究实验室和公司都能构建自己的模型？

这正是Hugging Face与NVIDIA通过训练集群即服务所要解决的问题——提供GPU集群的可访问性，并具有灵活性，只需为训练运行的时间付费即可。

要开始使用，Hugging Face平台上的25万家组织中的任何一家都可以在需要时，申请所需规模的GPU集群。

## 运作方式

要开始使用，您可以代表您的组织在 `hf.co/training-cluster` 申请GPU集群。

训练集群即服务将NVIDIA和Hugging Face的关键组件整合为一个完整的解决方案：

- **NVIDIA云合作伙伴** 在区域数据中心提供最新的NVIDIA加速计算（如NVIDIA Hopper和**NVIDIA GB200**）容量，所有这些都集中在**NVIDIA DGX Cloud**中。
- **NVIDIA DGX Cloud Lepton** —— 今天在巴黎GTC大会上宣布 —— 为研究人员提供便捷的基础设施访问，并支持训练运行调度和监控。
- **Hugging Face开发者资源和开源库** 使得启动训练运行变得简单。

一旦您的GPU集群申请被接受，Hugging Face和NVIDIA将根据您的规模、区域和时长需求，协作进行资源调配、定价、配置和设置您的GPU集群。

## 集群应用实例

### 与TIGEM合作推进罕见遗传病研究

**Telethon Institute of Genomics and Medicine**（简称TIGEM）是一个致力于理解罕见遗传病背后的分子机制并开发新疗法的研究中心。训练新的AI模型是预测致病性变异影响和药物重定位的新途径。

> AI为研究罕见遗传病的病因和开发治疗方法提供了新途径，但我们的领域需要训练新模型。训练集群即服务让我们能够在合适的时间轻松获取所需的GPU算力。
>
> -- Diego di Bernardo, TIGEM基因组医学项目协调员

### 与Numina合作推进数学AI

**Numina** 是一个非营利组织，致力于构建用于数学推理的开源、开放数据集的AI，并赢得了2024年**AIMO进步奖**。

> 我们正稳步朝着构建最佳闭源模型（如Deepmind的AlphaProof）的开源替代品这一目标前进。计算资源是我们当前的瓶颈——借助训练集群即服务，我们将能够实现目标！
>
> -- Yann Fleureau, Project Numina联合创始人

### 与Mirror Physics合作推进材料科学

Mirror Physics是一家初创公司，致力于为化学和材料科学创建前沿AI系统。

> 我们与MACE团队合作，致力于推动AI在化学领域的极限。借助训练集群即服务，我们正在以前所未有的规模生成高保真化学模型。这将是该领域向前迈出的重要一步。
>
> -- Sam Walton Norwood, Mirror首席执行官兼创始人

## 赋能多元化的AI研究

训练集群即服务是Hugging Face与NVIDIA之间的一项新合作，旨在让全球AI研究社区更便捷地获取AI算力。

> 获取大规模、高性能的计算资源对于跨领域和跨语言构建下一代AI模型至关重要。训练集群即服务将为研究人员和公司扫清障碍，释放训练最先进模型的能力，并突破AI领域的可能性边界。
>
> -- Clément Delangue, Hugging Face联合创始人兼首席执行官

> 将DGX Cloud Lepton与Hugging Face的训练集群即服务相结合，为开发者和研究人员提供了一种无缝的方式，通过广泛的云提供商网络访问高性能NVIDIA GPU。此次合作使AI研究人员和组织能够更轻松地扩展其AI训练工作负载，同时使用Hugging Face上熟悉的工具。
>
> -- Alexis Bjorlin, NVIDIA DGX Cloud副总裁

## 携手NVIDIA赋能AI构建者

我们很高兴与NVIDIA合作，向Hugging Face组织提供训练集群即服务——您今天就可以在 `hf.co/training-cluster` 开始使用。

在今天的巴黎GTC大会上，NVIDIA宣布了为Hugging Face用户带来的许多新贡献，从智能体到机器人！

- **NVIDIA DGX Cloud Lepton** 将欧洲开发者与全球NVIDIA计算生态系统连接起来。
- **NVIDIA AI客户** 现在可以通过NIM部署超过10万个Hugging Face模型。
- **Hugging Face用户** 可以使用NVIDIA Cosmos Predict-2构建自定义物理AI模型。
- **NVIDIA Isaac GR00T N1.5** 登陆Hugging Face，为人形机器人提供动力。

---

> 本文由AI自动翻译，原文链接：[Introducing Training Cluster as a Service - a new collaboration with NVIDIA](https://huggingface.co/blog/nvidia-training-cluster)
> 
> 翻译时间：2026-04-03 04:58
