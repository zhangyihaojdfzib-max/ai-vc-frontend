---
title: 从单节点到多GPU集群：Discord如何让分布式机器学习变得简单
title_original: 'From Single-Node to Multi-GPU Clusters: How Discord Made Distributed
  Compute Easy for ML Engineers'
date: '2025-10-09'
source: Discord Engineering
source_url: https://discord.com/blog/from-single-node-to-multi-gpu-clusters-how-discord-made-distributed-compute-easy-for-ml-engineers
author: Serrana Aguirregaray; Nathaniel Jenkins
summary: 本文介绍了Discord机器学习平台的发展历程。随着模型和数据集规模的增长，公司面临扩展性挑战，需要分布式计算能力。Discord以Ray为基础，构建了包含自定义CLI工具、Dagster+KubeRay编排系统和X-Ray可观测性层的平台，核心目标是提升开发者体验，将复杂的分布式机器学习变得简单易用。这一演进支撑了如广告排序等关键模型，实现了业务指标超过200%的提升。
categories:
- AI基础设施
tags:
- 分布式计算
- 机器学习平台
- Ray
- 开发者体验
- GPU集群
draft: false
---

Discord机器学习如何触及其扩展极限

在Discord，我们的机器学习系统已从简单的分类器发展为服务数亿用户的复杂模型。随着模型日益复杂、数据集不断增大，我们越来越多地遇到扩展性挑战：需要多GPU的训练任务、单机无法容纳的数据集，以及超越我们基础设施承载能力的计算需求。

获得分布式计算能力是必要的——但这还不够。我们需要让分布式机器学习变得简单易用。开源分布式计算框架Ray成为了我们的基础。在Discord，我们围绕它构建了一个平台：包括自定义CLI工具、基于Dagster + KubeRay的编排系统，以及名为X-Ray的可观测性层。我们的核心关注点是开发者体验，将分布式机器学习从难以使用的技术转变为开发者乐于使用的系统。

这就是Discord如何从零深度学习基础，到临时性实验，再到生产级编排平台的发展历程，也是这项工作如何催生了像广告排序这样的模型——该模型为我们的业务指标带来了超过200%的提升。

---

> 本文由AI自动翻译，原文链接：[From Single-Node to Multi-GPU Clusters: How Discord Made Distributed Compute Easy for ML Engineers](https://discord.com/blog/from-single-node-to-multi-gpu-clusters-how-discord-made-distributed-compute-easy-for-ml-engineers)
> 
> 翻译时间：2026-01-05 17:29
