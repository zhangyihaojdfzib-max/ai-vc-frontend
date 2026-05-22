---
title: MagenticLite：专为小模型优化的智能体体验
title_original: 'MagenticLite: An agentic experience optimized for small models'
date: '2026-05-21'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/
author: ''
summary: 微软研究院发布MagenticLite，一款专为小模型设计的实验性智能体应用，可在单个工作流中跨浏览器和本地文件系统运行。它由MagenticBrain（规划与委派）和Fara1.5（计算机视觉与操作）两个小模型驱动，通过协同设计实现高效执行。项目核心假设是智能体能力依赖工具编排而非知识，使得小模型也能支持广泛任务。该发布探索了在更小模型、协同设计工具和优化执行框架下智能体性能的极限。
categories:
- AI产品
tags:
- 微软研究院
- 小模型
- 智能体
- MagenticLite
- 计算机使用
draft: false
translated_at: '2026-05-22T06:05:43.273372'
---

![MagenticLite](/images/posts/a3dfc5310d35.jpg)

## 概览

- MagenticLite 是一款 Agent（智能体）应用，可在单个工作流中跨浏览器和本地文件系统运行。作为 Magentic-UI 的下一代产品，它结合了重新设计的应用和针对小模型优化的执行框架。
- MagenticBrain 和 Fara1.5 分别是专为编排和计算机使用任务设计的小模型。Fara1.5 是 Fara 的下一代迭代版本，在真实浏览器任务上实现了可衡量的性能提升。
- 这些发布共同探索了在更小模型、协同设计工具和优化执行框架下，Agent（智能体）性能能够被推向何种程度。

今天，Microsoft Research AI Frontiers 发布了 MagenticLite（在新标签页中打开），这是一款专为小模型设计的实验性 Agent（智能体）应用。作为 Magentic-UI 的下一代产品，它可在单个工作流中跨浏览器和本地文件系统运行。

MagenticLite 由两个专用模型驱动：MagenticBrain，用于推理、委派和终端使用；以及 Fara1.5，一个用于基于浏览器任务的计算机使用模型系列。这三个组件被设计为作为一个单一系统协同工作。其结果是形成了一个高效运行的 Agent（智能体），将数据保留在用户机器上，并支持广泛的 Agent（智能体）任务。它也指向了一个更广泛的目标：能够在用户硬件上直接运行的高能力 Agent（智能体）。

该项目围绕一个关键研究假设构建：Agent（智能体）能力依赖于工具编排和行动，而非仅仅依赖知识。这一洞察使得使用更小模型成为可能，同时仍能以极低的成本支持广泛的 Agent（智能体）任务。

MagenticLite 也反映了我们端到端处理 Agent（智能体）AI 的方式——从训练数据和模型设计，到编排、交互设计，以及贯穿整个体验的人工监督。

![图 1. 一个体验，三个组件：MagenticLite、MagenticBrain 和 Fara1.5。](/images/posts/cb7924551b27.png)

## 本次发布内容

MagenticLite（在新标签页中打开）

Magentic-UI 的下一代产品，我们的实验性 Agent（智能体）体验，由一个为小模型重建的 Agent（智能体）执行框架驱动，并采用了根据社区反馈更新的用户界面。它可在单个工作流中跨用户浏览器和本地文件系统运行。

MagenticBrain（在新标签页中打开）

MagenticBrain 集 MagenticLite 的规划器、编码器和委派器于一身。它将模糊的请求转化为具体计划，为每一步选择正确的工具或子 Agent（智能体），在需要时编写代码，并在任务中途出现故障时进行恢复。

Fara1.5

我们计算机使用模型系列的下一代产品，Fara1.5 提供三种尺寸，其中旗舰版 90 亿参数模型适用于大多数用例。Fara1.5 在小规模计算机使用模型中取得了新的最先进（SOTA）成果，在网页导航上的性能几乎是 Fara-7B 的两倍，并且在处理表单、需要凭据的网站和长时间运行任务方面更加精准。

每个组件本身都很有用，但它们协同工作效果最佳。对应用、模型和执行框架进行协同设计，使得在此规模下能够实现强大且可靠的 Agent（智能体）性能。

### 我们的研究方法：以少胜多

我们从一个问题开始：如何让一个小模型真正擅长 Agent（智能体）任务？答案贯穿了整个生命周期——数据生成、训练目标、模型设计和编排必须被重新设计，而非孤立进行。

我们从真实用例（如填写表单、进行浏览器研究和本地文件管理）中识别出需求，并围绕这些需求构建了一个评估数据集。标准基准测试捕捉了部分情况，但它们并不总是衡量真实世界实用性的直接指标。基于场景的评估补充了这些基准测试，并成为模型和执行框架迭代改进的关键信号，如图 2 所示。

![图 2. 构建 Agent（智能体）系统的迭代过程包括定义成功标准、评估性能，以及优化模型或系统设计（或两者）。然后重复。](/images/posts/98fb3127523a.png)

在用户体验方面，我们保留了 Magentic-UI 的关键元素，包括对 Agent（智能体）推理和行动的可视性、用户直接控制的能力，以及在关键节点进行明确批准。基于近期的用户研究，我们还通过更新的浏览器和聊天视图使 MagenticLite 更易于学习和协作，旨在让用户更容易理解 Agent（智能体）的行动并在需要时进行干预。如图 3 所示。

视频系列

![与 Sinead Bovell 的《再思考》](/images/posts/c0f56ba91e8d.jpg)

## 再思考

一个与 Sinead Bovell 合作的视频系列，围绕每个人都在问的关于 AI 的问题展开。借助来自微软各地的专家声音，我们解析了这一快速变化技术的紧张与承诺，探索正在演变的事物和可能的未来。

## 系统组件

### Fara1.5：性能超越其体量级别的计算机使用模型

Fara1.5 是我们计算机使用模型系列的下一代产品，提供三种尺寸，其中旗舰版 9B 模型推荐用于大多数用例。Fara1.5 在小规模计算机使用模型中取得了新的最先进（SOTA）性能，在网页导航上的性能几乎是 Fara-7B 的两倍，并且在处理表单、需要凭据的网站和长时间运行任务方面表现更佳。

去年十一月，我们发布了 Fara-7B，这是一个专为在网页浏览器中完成任务而构建的小型 Agent（智能体）模型。它使用一种新颖的合成数据生成引擎进行训练，实现了同类最佳性能。Fara1.5 是这一假设的下一步：一个基于 Qwen 3.5 的三种尺寸模型系列（4B、9B、27B），旨在弥补我们在先前发布中看到的差距。

### 新特性

最先进的结果。在流行的 Online-Mind2Web 基准测试上，该测试包含跨广泛使用网页领域的 300 个任务，Fara1.5 在其尺寸级别的模型中取得了新的最先进（SOTA）结果。Fara1.5 优于所有类似尺寸的模型，性能几乎是 Fara-7B 的两倍。更大的 Fara1.5-27B 变体在同一基准测试上实现了超过 90% 的性能。

![图 4. 在 OnlineMind2Web 基准测试上，Fara-1.5-9B 在其尺寸级别的模型中取得了最先进的性能，并大幅优于之前的模型。](/images/posts/9c23a89e03f8.png)

改进的用户体验。除了基准测试上的改进，我们还提升了 Fara1.5 的用户体验。用户应能观察到在日常任务（如填写表单、处理需要凭据的网站登录以及预约）上的更强性能。这些改进由我们 FaraGen 数据生成管线的下一代演进所驱动。除了在真实网站上进行训练，我们还在高度逼真的合成环境上训练了模型，这些环境旨在模拟登录和不可逆操作等场景。

为长时间运行任务调优的原生动作空间。除了点击和键盘操作，Fara1.5 还内置了工具，可在数百个步骤中在其上下文中存储关键信息，并在需要时向用户请求权限或偏好，帮助其在跨越数分钟实际工作的任务中保持连贯性。

重新校准的关键节点。Fara-7B 被训练用于检测交易、登录流程或不可逆提交等活动中的关键节点并进行标记。在 Fara1.5 中，我们根据实际使用中的经验教训，围绕关键节点优化了设计，使得安全触发在应该发生时仍然发生，但不会阻止有用的任务，例如表单填写。

### MagenticBrain：编排器模型

MagenticBrain 是一个 140 亿参数的编排模型——集规划器、编码器和委派器于一身。从 Qwen 3 14B 微调而来，MagenticBrain 在 MagenticLite 执行框架内进行了端到端训练，使用了它在推理时会遇到的相同工具模式和执行环境。因此，它学习编排的方式与其运行方式之间没有差距。

在许多Agent（智能体）系统中，编排（规划与协调）是推理密集度最高的组件，因此团队历来依赖其最强大的模型来承担这一角色。我们的判断是，小型模型也能在不牺牲能力的前提下胜任这一角色。两个设计选择使这成为可能。

第一个选择是将多步骤工具调用轨迹——模型在此学习选择正确的工具并正确调用它——与编码和终端轨迹相结合——在此正确的答案有时是五行Python代码，而非工具调用。这与训练和推理期间使用的工具格式之间的紧密耦合相辅相成。

第二个选择是计算机使用Agent（CUA）委托。编排器的一项关键任务是知道何时不应自行行动，而是将任务移交给Fara1.5。我们的数据管道包含明确的委托轨迹：编排器识别出浏览器或用户界面（UI）任务、向CUA模型发出结构化移交、等待结果、然后继续执行任务的序列。其结果是，一个编排器模型能够在单个14B参数规模内流畅地进行推理、编码、调用工具和委托任务。我们正在发布MagenticBrain，它被设计用于与MagenticLite配合使用。

![图6. MagenticBrain是一个小型编排模型，能够将自然语言请求分解为更小的步骤，选择正确的工具，在需要时编写代码，并将浏览器任务委托给Fara1.5。](/images/posts/9a3a74fab47e.png)

### 框架：专为小型模型构建

该框架将编排器和浏览器使用模型整合到一个工作流中。三个设计选择最为重要：

- 逐步规划。该框架增量式地进行规划，保持系统的灵活性，并在长时间运行的任务中实现更平滑的路线修正和恢复。
- 主动上下文管理。小型模型的有效上下文窗口较小，并且随着上下文增长，其性能下降更快。该框架主动管理每个模型在每个步骤接收的内容，保持提示词的聚焦，仅呈现必要信息，将早期交互压缩为简洁摘要，并卸载其余内容，从而使编排器和Fara1.5在长时间任务中保持高效。
- 通过子Agent进行委托。该框架不依赖单个小型模型处理所有任务，而是让编排器充当主Agent，并将专门工作委托给子Agent。这意味着将浏览器任务移交给Fara1.5。这种模式通过允许每个模型处理问题中更狭窄、更专门化的部分，发挥了小型语言模型的优势。它也为未来的扩展奠定了基础：后续版本可以引入额外的子Agent，并让它们并行运行，以实现更丰富、更高效的工作流。

该框架保留了Magentic-UI 1.0中的人机协同保障机制。浏览器和代码操作中的关键节点仍然会暂停以等待用户明确批准，并且整个系统运行在Quicksand（在新标签页中打开）内，这是一个为基于QEMU的沙箱创建的开源封装器，可将浏览器会话和代码执行与主机系统隔离。

### 实际应用

MagenticLite可以在浏览器和本地文件系统中执行各种任务，例如填写表单、预约、整理本地文件以及搜索和分析信息。

## 尝试使用，并与我们一起构建

MagenticLite、MagenticBrain和Fara1.5是研究版本，旨在支持持续的探索和开发。我们发布它们是为了鼓励更广泛社区的实验、评估和反馈。

- MagenticLite是Magentic-UI的更新版本，可在GitHub（在新标签页中打开）上获取。
- MagenticBrain可在Microsoft Foundry（在新标签页中打开）上获取。
- Fara1.5模型可在Microsoft Foundry（在新标签页中打开）上获取。

## 贡献者

- Agentic体验：Cheng Tan, Maya Murad, Weili Shi
- Agentic框架：Adam Fourney, Tyler Payne
- Fara1.5：Alexey Taymanov, Andrew Zhao, Aravind Rajeswaran, Corby Rosset, Hussein Mozannar, Luiz Do Valle, Spencer Whitehead, Vibhav Vineet, Zach Nussbaum, Sahil Gupta, Yadong Lu
- MagenticBrain：Ahmed Elgohary Ghoneim, Akshay Nambi, Amir Saeidi, Caio César Teodoro Mendes, Harkirat Behl, Karan Gupta, Pashmina Cameron, Pranav Vajreshwari, Shital Shah, Yash Lara, Yash Pandya
- 合作者：Abhishek Gowami, Amanda Swearngin, Michael Harrison, Sara Abdali, Sarthak Harne, Vidhisha Balachandran
- 项目负责人：Ahmed Awadallah, Rafah Hosn
- 赞助人：Ahmed Awadallah, Ece Kamar, Rafah Hosn, Saleema Amershi, Shital Shah

## 认识作者

### 微软研究院AI前沿

---

> 本文由AI自动翻译，原文链接：[MagenticLite: An agentic experience optimized for small models](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/)
> 
> 翻译时间：2026-05-22 06:05
