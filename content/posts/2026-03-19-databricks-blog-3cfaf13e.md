---
title: Databricks发布AI Runtime：无服务器NVIDIA GPU助力分布式训练与微调
title_original: 'Introducing AI Runtime: Scalable, Serverless NVIDIA GPUs on Databricks
  for Training and Finetuning'
date: '2026-03-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-ai-runtime-scalable-serverless-nvidia-gpus-databricks-training-and-finetuning
author: ''
summary: Databricks宣布推出AI Runtime公开预览版，这是一个全新的训练技术栈，提供按需、无服务器的NVIDIA A10和H100 GPU，支持大规模分布式训练。该平台集成了优化的编排工具、高性能数据加载和集中式治理功能，旨在简化深度学习工作负载的管理，让研究人员专注于建模而非基础设施问题。用户可通过笔记本快速连接GPU，并利用Lakeflow进行生产级作业编排，同时享受内置的MLflow实验跟踪和Unity
  Catalog访问管理。
categories:
- AI基础设施
tags:
- AI Runtime
- Databricks
- GPU训练
- 分布式训练
- 无服务器计算
draft: false
translated_at: '2026-03-20T04:53:03.165388'
---

GPU驱动着当今最先进的AI工作负载——从预测和推荐系统到多模态基础模型。然而，团队在获取和管理GPU基础设施、配置分布式训练环境以及调试数据加载瓶颈方面面临挑战。深度学习研究人员更愿意专注于建模，而非排查基础设施问题。

我们很高兴地宣布**AI Runtime (AIR)** 公开预览版发布，这是一个全新的训练技术栈，支持在A10和H100 GPU上**按需**进行分布式训练。AI Runtime包含了用于大规模训练LLM（大语言模型）（如MPT和DBRX）的所有技术。即使在测试阶段，已有包括Rivian、Factset和YipitData在内的数百家客户使用AIR训练深度学习模型并投入生产。其应用场景涵盖计算机视觉模型、推荐系统，以及为Agent（智能体）任务微调的LLM（大语言模型）。我们自己的Databricks AI研究团队也使用AIR进行模型的强化学习，例如在我们最近的**KARL**论文中。

借助**AI Runtime**，Databricks用户现在拥有：

*   **无服务器、按需的NVIDIA GPU**：只需点击2-3下配置您的笔记本，即可快速连接到无服务器的A10和H100 GPU开始训练——无需集群。只为使用的GPU付费，无需担心闲置时间利用率。
*   **强大的编排工具**：利用Databricks编排套件的全部功能，Lakeflow Jobs和DABs支持长时间运行的GPU工作负载。
*   **优化的分布式训练**：AIR集成了分布式GPU性能增强功能，如RDMA和高性能数据加载。
*   **集中式治理与可观测性**：在您的数据所在之处运行、观测和管理GPU工作负载，内置通过MLflow进行的实验管理、通过Unity Catalog进行的访问管理，以及Agent（智能体）辅助调试。

## 笔记本中的按需NVIDIA H100和A10 GPU

![AI Runtime](/images/posts/6e1630741c5b.gif)

对于交互式开发和调试，只需点击几下即可在Databricks笔记本中连接到按需的A10和H100 GPU。在此基础上，您可以利用Databricks广为人知的所有开发者人体工程学设计，从常见Python包的环境管理，到借助**Genie Code**进行Agent（智能体）驱动的编写和调试。轻松挂载来自湖仓的数据来训练深度学习模型，甚至可以从您的GPU驱动笔记本调用远程CPU集群来处理Spark数据处理工作负载，以准备您的数据。

![Genie Code demo](/images/posts/3d9f6f3d7794.gif)

使用Genie Code帮助解决性能瓶颈、尝试新架构，或调试模型收敛或晦涩框架错误相关的棘手问题。

## 面向生产就绪工作负载的Lakeflow

AI Runtime是一个面向加速计算的生产级平台。在交互式笔记本中开发您的深度学习代码，然后利用**Lakeflow**的全部功能提交和编排GPU计算上的作业。笔记本和自定义代码仓库都可以由Lakeflow执行，用于长时间运行或计划作业。对于CI/CD（持续集成和持续部署）等生产需求，AI Runtime与我们的**Declarative Automation Bundles (DABs)** 完全兼容。

通过我们的Lakeflow集成，客户可以使模型训练和微调与上游数据管道和下游生产系统保持紧密同步。

![Test job](/images/posts/2c0452afd69d.gif)

## 为分布式深度学习优化的Runtime

分布式训练工作负载的准备、调试和观测可能非常痛苦。从排查RDMA设置到跟踪来自多个GPU的遥测数据，再到正确的软件配置，用户很容易忽略那些会显著减慢模型训练速度的关键细节。

相反，AI Runtime针对整个深度学习生命周期进行了优化——旨在为您节省时间。PyTorch和CUDA等关键依赖项已预装，同时优化支持Ray、Hugging Face Transformers、Composer等分布式训练框架及其他库，因此您可以立即开始训练而无需管理环境。客户也欢迎使用他们自己的库，从Unsloth到TorchRec，再到自定义训练循环。

![ Integrated SDKs and observability tools simplify the management of distributed training workloads. ](/images/posts/7c7740b92b34.png)

集成的SDK和可观测性工具简化了分布式训练工作负载的管理。MLFlow实现了对GPU工作负载的深度可观测性，自动跟踪GPU利用率和训练实验。无论您是在微调基础模型，还是训练预测和个性化模型，该Runtime都经过优化，能以最少的设置加速训练工作流程。

![MLFlow enables deep observability of GPU workloads, with automatic tracking of GPU utilization and training experiments. ](/images/posts/bc8b4738a6b6.gif)

今天发布的AI Runtime公开预览版支持在单节点内跨8个H100 GPU进行分布式训练，多节点支持目前处于私有预览阶段。

## 集中式数据治理与可观测性

AI Runtime与Databricks湖仓原生集成，使您能够在数据所在之处运行和管理GPU工作负载。这消除了碎片化的工作流程，简化了从实验到生产的路径。

*   **通过Unity Catalog进行集中治理**：在数据和AI工作负载上应用一致的访问控制、血缘关系和治理策略，实现GPU资源的安全合规使用。
*   **统一的可观测性**：使用原生系统表在一个地方跟踪和监控所有工作负载——CPU和GPU，实现统一的审计、使用情况跟踪和运营洞察。

您的AI工作负载完全运行在您的企业数据边界内，在提供强大治理和安全性的同时，不牺牲实验和扩展的灵活性。

## 集成来自NVIDIA的下一代GPU创新

在AI工作负载和Agent（智能体）系统中，对加速计算的需求持续增长。AI Runtime使更多Databricks客户能够利用NVIDIA硬件加速其AI工作负载并推动业务发展。我们很高兴能与NVIDIA继续合作，将**最新的NVIDIA技术**（例如在GTC 2026上发布的RTX PRO 4500 Blackwell服务器版）带给我们的客户。

## 立即开始使用AI Runtime

为了帮助您入门，我们准备了几个模板笔记本和入门指南：

*   请参阅我们的**文档**，了解设置和日常使用的详细说明。
*   **入门模板**，用于训练推荐系统、经典ML模型、微调LLM（大语言模型）等！
*   从经典计算GPU工作负载迁移到无服务器的**迁移指南**。

请联系您的客户团队以了解更多信息或提出任何问题！

---

> 本文由AI自动翻译，原文链接：[Introducing AI Runtime: Scalable, Serverless NVIDIA GPUs on Databricks for Training and Finetuning](https://www.databricks.com/blog/introducing-ai-runtime-scalable-serverless-nvidia-gpus-databricks-training-and-finetuning)
> 
> 翻译时间：2026-03-20 04:53
