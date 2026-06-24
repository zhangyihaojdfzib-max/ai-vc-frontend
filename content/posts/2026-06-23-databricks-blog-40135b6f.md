---
title: Genesis Workbench：生命科学AI的开放蓝图
title_original: 'Genesis Workbench: A blueprint for industry AI in life sciences,
  powered by Databricks and NVIDIA'
date: '2026-06-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/genesis-workbench-blueprint-industry-ai-life-sciences-powered-databricks-and-nvidia
author: ''
summary: Genesis Workbench是一个基于Databricks和NVIDIA技术构建的开放模块化蓝图，旨在为生命科学研发提供端到端的AI解决方案。它集成了NVIDIA的加速计算工具（如BioNeMo和Parabricks），通过无代码点击式界面简化基因组学、分子设计等复杂任务，同时利用Unity
  Catalog确保数据安全与IP保护。该平台集中管理数据，消除外部API依赖，加速从假设到候选药物的整个流程，解决了AI在药物发现中面临的安全、模型更新和微调等关键挑战。
categories:
- AI基础设施
tags:
- 生命科学
- 药物发现
- Databricks
- NVIDIA
- AI基础设施
draft: false
translated_at: '2026-06-24T06:13:06.951562'
---

- **Genesis Workbench** 是一个开放、模块化的 Databricks 蓝图，它将 NVIDIA 的加速计算工具（包括 BioNeMo 和 Parabricks）集成到一个统一、安全的环境中，用于端到端的药物发现。
- 该平台通过提供无代码、点击式的界面简化了复杂的研发工作，使实验科学家能够执行基因组学和分子设计任务，同时通过 Unity Catalog 治理保持严格的 IP 安全。
- 通过集中数据并消除外部 API 依赖，该工作台简化了从初始假设到排名候选治疗药物的整个研究流程，将专有数据保留在受控、可治理的边界内。

## 将 GPU 加速的药物发现带到您的数据中

生命科学领导者需要在其自身治理数据之上直接构建的、领域特定且生产就绪的 AI。Databricks 和 NVIDIA 共同推动了这一转变：通过将 Databricks（Unity Catalog 治理、MLflow、模型服务和无服务器 GPU 计算）与 NVIDIA BioNeMo Agent 工具包（包括 NVIDIA CUDA-X 库、Parabricks 以及不断增长的生物学和化学模型目录，如 Proteina-Complexa）相结合，客户可以在数据所在之处运行专门的 AI，而无需将敏感数据发送到第三方 API。

本文重点介绍这种结合最困难的应用之一：生命科学研发与药物发现——这项工作可能需要数年时间和数十亿美元的投资，所涉及的数据绝大多数是非结构化和敏感的，涵盖基因组学、转录组学、结构生物学和化学——这些学科很少共享通用的工具链。Genesis Workbench 正是这种结合在实践中的体现。

## 什么是 Genesis Workbench？

Genesis Workbench 是一个在 Databricks 上构建生命科学应用的开放蓝图——一个模块化的工作台，将计算药物发现的主要阶段整合到一个平台、一个用户界面和一个治理模型之下。每个科学领域都是一个可独立部署的模块：

- 基因组学
- 单细胞
- 大分子
- 小分子
- NVIDIA BioNeMo 模型微调

该平台将标准工具箱转变为一个有凝聚力的科学工作台。最重要的是，整个环境可以通过单个脚本轻松部署。借助由 Databricks Apps 驱动的点击式 UI，实验科学家无需编写代码即可导航整个发现工作流程。底层架构依赖于在 Unity Catalog 中管理的开源模型，通过 MLflow 进行跟踪，并在 GPU 端点上提供服务。通过使用 Databricks AI Search 集中公共和专有数据集，我们完全消除了外部 API 依赖。最终，这种无缝设置连接了流程的每一步——使基因组学发现能够轻松流入单细胞验证、靶点结构预测、候选分子对接、ADMET 和排序。

## Genesis Workbench 如何加速生命科学研发

通过将发现的每个阶段整合到一个 Databricks 原生且 NVIDIA 加速的平台上，Genesis Workbench 直接解决了历史上阻碍 AI 在生命科学研发中发挥作用的四个问题：

![](/images/posts/ba988ca7262e.jpg)

- **AI 辅助工作流生成。** 声明式地使用工作台——描述您想要的科学目标，即可获得一个可运行的流程，无需接线或样板代码。这将门槛从“我知道如何构建这个”降低到“我知道我想要什么”，从而使更多科学家能够将想法转化为实验并更快地创新。Vortex 是实现这一目标的视觉画布。
- **MCP 支持。** Genesis Workbench 成为更广泛 AI 生态系统的得力工具——其模型和工作流成为任何 Agent（智能体）或 MCP 客户端可以调用的工具，因此该平台为您的助手和流程提供动力，而不是孤立存在。一个配套的模型上下文协议（MCP）服务器将其暴露给 Databricks AI Playground、Claude、Cursor 或您自己的 Agent（智能体）；随核心功能自动部署。
- **IP 风险与安全。** 序列、化合物库、检测结果和患者数据是组织中最受监管的资产。模型和数据一次性下载到 Unity Catalog 中，推理在您自己的工作区中的模型服务端点上运行，并且没有运行时外部 API 依赖——您的 IP 永远不会离开您可治理的边界。
- **不断变化的模型格局。** 生物 AI 发展迅速。Genesis Workbench 的模块化架构将每个模型视为同一注册和服务基础架构中的可独立部署子模块，因此采用 GenMol、Proteina-Complexa 或更新的模型只是一个部署步骤，而不是重写。
- **微调。** 在您的 Lakehouse 中对高度治理的专有数据集进行开源模型微调，使得利用现有内部知识进行更快速的构思和候选发现变得容易。
- **复杂的跨学科管道连接。** 由于每个模块共享一个平台、治理模型以及作业/服务/MLflow 基础架构，这些学科能够原生连接——通过应用内交接（包括基因→序列解析），而不是系统间脆弱的复制粘贴。工作台本身就是集成层。

**让非计算科学家也能参与其中。** 一个点击式的 React UI——带有交互式 3D 查看器和 AI 生成的、用通俗语言解释的结果——让生物学家无需编写代码即可调用变异、模拟基因敲除、设计结合物并对候选分子进行排序，而计算同事则保留对底层作业、模型和工件的完全访问权限，并在流程的每个阶段使用 NVIDIA 技术。

在几乎每个阶段，繁重的工作都由 NVIDIA 加速计算和模型完成：

| 发现阶段 | NVIDIA 技术 | 在 Genesis Workbench 中的作用 |
| :--- | :--- | :--- |
| 基因组学 | Parabricks（基因组学工作流的一部分） | GPU 加速的胚系变异识别和注释——从您的 Lakehouse 数据中找出致病变异 |
| 单细胞 | RAPIDS-singlecell（scverse 的一部分） | GPU 加速的大规模数据集聚类、UMAP 和差异表达——将过夜的批处理作业转变为交互式探索 |
| 小分子 | GenMol（NV-GenMol-89M-v2） | 从种子骨架开始，在封闭的生成→评分→重新生成循环中生成新颖、可合成的分子，在硬约束下运行，并可选择在奖励中加入对接 |
| 大分子 | Proteina-Complexa | 流匹配蛋白质结合物设计和基序支架（结合 ProteinMPNN + ESMFold）——从靶点结构到排序后的设计结合物候选 |
| 各个阶段 | BioNeMo Recipes | 在您的数据上、您的基础设施上，在 BioNeMo 容器中使用预打包模型进行微调和推理运行 |

## Genesis Workbench 的未来

展望未来，我们专注于使工作台对科学发现更加易用和强大。我们的路线图包括：

- **自动化工作流生成：** 我们正在引入 AI 驱动的自动化来生成复杂的科学工作流，使集成新模型和多样化数据源更加无缝。
- **NVIDIA AI 技能集成：** 我们正在集成 NVIDIA BioNeMo Skills 以及 BioNeMo Agent 工具包如何增强平台的原生智能和能力。随着更多技能的出现，我们将集成它们。
- **MCP 服务：** 我们计划添加 MCP（模型上下文协议）服务，以确保 Genesis Workbench 能够轻松向下游消费应用提供高质量的数据和见解。

## 从疾病到候选药物，在一个受治理的平台上

Genesis Workbench 使科学家能够安全地驱动整个药物发现过程——从假设到排序的治疗方案——而无需让数据离开环境。通过将 Parabricks、CUDA-X Data Science、Proteina-Complexa、GenMol 和 BioNeMo Agent Toolkit 等 GPU 加速工具统一在 Unity Catalog 治理下，它提供了一个专为实验台科学家构建的直观用户界面。这一强大的计算机模拟管线确保只有最高概率的靶点才能进入湿实验室，从而大幅减少时间和资源的浪费。这正是行业人工智能的具体承诺：将专业、安全的人工智能直接带到您的数据中。

## 准备好加速您的药物发现了吗？

立即从我们的 GitHub 仓库部署 Genesis Workbench。我们还提供 Claude Code 技能，以协助您进行部署和修改。我们欢迎贡献，如果您有能力，欢迎为项目做出贡献！如果您已经是 Databricks 的客户，并对现场演示感兴趣，请与您的 Databricks 客户团队联系。

Genesis Workbench 是一个开放的 Databricks 行业解决方案蓝图。

---

> 本文由AI自动翻译，原文链接：[Genesis Workbench: A blueprint for industry AI in life sciences, powered by Databricks and NVIDIA](https://www.databricks.com/blog/genesis-workbench-blueprint-industry-ai-life-sciences-powered-databricks-and-nvidia)
> 
> 翻译时间：2026-06-24 06:13
