---
title: Safetensors正式加入PyTorch基金会，迈向社区中立治理
title_original: Safetensors is Joining the PyTorch Foundation
date: '2026-04-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/safetensors-joins-pytorch-foundation
author: ''
summary: Hugging Face开发的Safetensors模型权重格式已作为托管项目加入PyTorch基金会，标志着该项目进入供应商中立、社区驱动的治理新阶段。Safetensors因其安全、高效的特点，已成为开源机器学习社区共享模型的首选格式。此次加入旨在通过更广泛的社区参与确保项目发展反映生态需求，未来将与PyTorch核心深度集成，并计划支持设备感知加载、张量并行及更多量化格式，以解决生态系统共同面临的挑战。
categories:
- AI基础设施
tags:
- Safetensors
- PyTorch基金会
- 模型格式
- 开源社区
- 机器学习安全
draft: false
translated_at: '2026-04-09T04:31:06.085021'
---

# Safetensors 正式加入 PyTorch 基金会

今天，我们宣布 Safetensors 已作为基金会托管项目加入 Linux 基金会旗下的 PyTorch 基金会，与 DeepSpeed、Helion、Ray、vLLM 以及 PyTorch 本身并列。

## 发展历程

Safetensors 最初是 Hugging Face 为满足一个具体需求而启动的项目：需要一种无法执行任意代码的模型权重存储与共享方式。当时生态系统中主流的基于 pickle 的格式意味着存在运行恶意代码的切实风险。在机器学习尚处萌芽阶段时，这种风险尚可接受，但随着开放模型共享成为机器学习社区工作的核心，这种风险变得不可接受。

我们构建的格式有意设计得简单：一个硬性限制为 100MB 的 JSON 头部，用于描述张量元数据，其后是原始张量数据。支持零拷贝加载，可将张量直接从磁盘映射到内存。支持惰性加载，因此无需反序列化整个检查点即可读取单个权重。

我们当时没有完全预料到的是它会被如此广泛地采用。如今，Safetensors 已成为 Hugging Face Hub 及其他平台模型分发的默认格式，被机器学习所有模态的数万个模型所使用。它已成为开源机器学习社区共享模型的首选方式。

## 为何选择 PyTorch 基金会

我们希望 Safetensors 真正属于社区。该项目一直是开源的，但代码贡献只是其发展的一部分。通过让更多公司和贡献者参与项目的治理，我们确保进展能反映基于其构建的社区的广度。加入 PyTorch 基金会意味着 Safetensors 现在有了一个供应商中立的归属地。项目的商标、代码库和治理权归属于 Linux 基金会，而非任何单一公司。Hugging Face 的两位核心维护者 Luc 和 Daniel 仍留在技术指导委员会，并继续负责项目的日常领导工作，但 Safetensors 现在正式属于依赖它的社区。

我们相信，当每位贡献者都能在现有基础上进行构建时，安全性才能得到最佳保障；这一原则现已嵌入项目治理本身。

## 这对用户和贡献者意味着什么

对于绝大多数用户来说，没有任何变化。格式相同，API 相同，Hub 集成相同：没有破坏性变更。目前以 Safetensors 格式存储的模型将继续完全按现有方式工作。

对于贡献者，成为维护者的路径现已正式记录在案，并对社区中的任何人开放。项目的治理规则位于代码库中的 GOVERNANCE.md 和 MAINTAINERS.md 文件。对于基于 Safetensors 构建的组织，Linux 基金会下的中立治理提供了一个稳定、长期、完全由社区驱动的基础。

## 未来展望

Safetensors 是一个成熟的项目，已被整个生态系统广泛采用，但我们仍然坚信项目才刚刚起步。

我们正在与 PyTorch 团队合作，以便 Safetensors 可以在 PyTorch 核心中用作 torch 模型的序列化系统。

未来几个月将见证显著的增长，我们认为 PyTorch 基金会是开启下一篇章的最佳归属。未来的路线图包括设备感知的加载和保存，以便张量可以直接加载到 CUDA、ROCm 和其他加速器上，无需不必要的 CPU 中转。

我们还在为张量并行和流水线并行加载构建一流的 API，以便每个计算单元或流水线阶段仅加载其所需的权重。随着生态系统量化格局的持续演进，我们将正式支持 FP8、GPTQ 和 AWQ 等块量化格式，以及亚字节整数类型。

这些都是整个生态系统都有责任去解决的问题，加入 PyTorch 基金会意味着我们可以与其他托管项目协作解决这些问题，而不是各自为战。

## 参与进来

Safetensors 是开源的，欢迎各个层面的贡献，从错误报告和文档编写，到新功能开发和参与治理。

- GitHub:github.com/huggingface/safetensors
- 文档:huggingface.co/docs/safetensors
- PyTorch 基金会:pytorch.org/foundation

如果您是基于 Safetensors 进行构建的开发者、研究人员或组织，并希望更多地参与其发展方向，请提交问题、发起讨论或直接联系维护者。该项目一直属于使用它的社区。现在的治理也反映了这一点。

---

> 本文由AI自动翻译，原文链接：[Safetensors is Joining the PyTorch Foundation](https://huggingface.co/blog/safetensors-joins-pytorch-foundation)
> 
> 翻译时间：2026-04-09 04:31
