---
title: 开源社区力挺OpenEnv推动智能体强化学习
title_original: The Open Source Community is backing OpenEnv for Agentic RL
date: '2026-06-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/openenv-agentic-rl
author: ''
summary: OpenEnv是一个用于创建智能体执行环境的开源工具，现由Meta-PyTorch、Nvidia、Hugging Face等多家机构组成的委员会协调，旨在标准化RL环境的发布、部署与使用。它作为互操作层，连接工具包、环境和训练器，不规定奖励或训练逻辑，而是提供通用接口。文章强调开放治理对开源智能体训练的重要性，并规划了未来任务集、外部奖励、工具包集成等方向，呼吁社区共同参与构建开源RL基础。
categories:
- AI基础设施
tags:
- OpenEnv
- 强化学习
- 开源智能体
- AI基础设施
- 社区治理
draft: false
translated_at: '2026-06-09T06:07:11.594126'
---

# 开源社区支持OpenEnv用于基于强化学习的智能体训练

OpenEnv是一个用于创建智能体执行环境的工具，例如终端、浏览器或任何智能体可以交互的对象。今天，我们激动地宣布OpenEnv将变得更加开放，以推动智能体训练的开源未来。

从今天起，OpenEnv将由一个委员会协调，该委员会目前包括Meta-PyTorch、Reflection、Unsloth、Modal、Prime Intellect、Nvidia、Mercor、Fleet AI和Hugging Face。OpenEnv现已托管在huggingface/OpenEnv。

OpenEnv项目得到了AI生态系统中一些领先组织的支持和采用，包括PyTorch Foundation、vLLM、SkyRL（UCB）、Lightning AI、Axolotl AI、Stanford Scaling Intelligence Lab、Mithril、OpenMined、Scaler AI Labs、Scale AI、Patronus AI、Surge AI、Halluminate、Turing、Scorecard和Snorkel AI。

## 为什么我们需要OpenEnv来训练开源智能体

像Claude Code、Codex、OpenClaw和Hermes这样的智能体工具包正在不断改进。它们改进的一个原因是，像GPT-5.5和Opus 4.8这样的模型经过训练，能够使用各自的工具包。

我们也希望开源模型能获得这些收益：训练本地模型以有效使用工具包，并通过为特定任务专业化模型来节省计算资源。

## 为什么我们需要（更加）开放

前沿实验室训练的模型和工具包，在很大程度上是紧密配合的。模型经过训练以使用工具包，并针对其特性进行了优化。模型可以在一定程度上泛化到这些工具包之外，但没有什么能比得上训练的效率。

![开源强化学习生态系统](/images/posts/09a295e0c67b.png)

在开源环境中，情况并非如此。开发者根据他们重视的任何用例，使用任何工具包、任何模型、任何推理引擎。这对社区来说是根本性的，但也是一个需要基础设施和工具来应对的挑战。

这就是OpenEnv的用武之地。它是一个连接工具包、环境和训练器的库，适用于任何模型。为了使其持久发展，它需要由所有主要利益相关者共同拥有。

## 一个协议层，而非奖励框架

伴随着治理结构的变更，我们也在明确OpenEnv的定位。

在最近的版本中，OpenEnv已成为RL环境的互操作层。它的工作是标准化环境的发布、部署以及被智能体使用的方式。它不会规定奖励如何定义或训练循环如何运作。奖励定义、评分规则和训练器特定的逻辑应归属于专门处理这些的库。OpenEnv是它们都可以插入的通用接口。

在实践中，这意味着：

一个接口，多种环境，所有这些环境都暴露了熟悉的Gymnasium风格API（reset()、step()、state()），运行在客户端/服务器架构上。一个支持OpenEnv的训练器可以驱动任何兼容的环境，而无需定制代码。

熟悉的协议和规范的打包方式。环境通过HTTP和WebSocket等标准协议提供服务，并使用Docker打包。MCP是一等公民，因此OpenEnv环境与MCP服务器即时兼容，并且同一环境在模拟（训练/评估）和生产模式下行为一致。

跨环境库的互操作性。您可以在不同的生态系统（verifiers、harbor等）中定义和使用环境，并在您选择的基础设施和中心上运行。OpenEnv是它们底层的部署和接口层，而不是它们的竞争对手。

## 下一步计划

在接下来的几个月里，我们将专注于将OpenEnv从一个快速增长的项目转变为一个可靠的标准：

1. 通过数据集实现任务集：将环境任务与Hugging Face数据集连接起来，使环境和基准测试能够干净地组合（RFC 006）。
2. 外部奖励：允许在您已使用的任何库中定义奖励，而OpenEnv作为部署层（RFC 007）。
3. 持续的工具包集成：对智能体工具包的一等支持。
4. 端到端示例：在TRL、Unsloth等中提供完整的训练和评估演练。
5. 自动验证：衡量环境质量及其对模型学习的贡献。这将为社区提供一种可扩展的方式来评估其环境并提高质量（想想黑客马拉松！）。RFC 008。

## 参与进来

OpenEnv在设计上以社区为中心，而且现在还处于早期阶段——期待一些不完善之处，并帮助我们改进。查看代码和RFC：github.com/huggingface/OpenEnv

感谢所有帮助实现这一转变的人。让我们一起为开源的基于强化学习的智能体构建共同的基础。

---

> 本文由AI自动翻译，原文链接：[The Open Source Community is backing OpenEnv for Agentic RL](https://huggingface.co/blog/openenv-agentic-rl)
> 
> 翻译时间：2026-06-09 06:07
