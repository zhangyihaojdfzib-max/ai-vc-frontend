---
title: 厘清AI Agent关键术语：驾驭层与构建框架
title_original: Harness, Scaffold, and the AI Agent Terms Worth Getting Right
date: '2026-05-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/agent-glossary
author: ''
summary: 本文针对AI Agent领域术语混乱的问题，系统梳理了模型、构建框架、驾驭层、Agent等核心概念的定义与区别。作者指出，模型本身无记忆和循环，需通过构建框架（定义行为）和驾驭层（执行循环）才能成为Agent。文章强调这些术语尚无统一标准，但提供了实用的心智模型，帮助从业者更清晰地理解和讨论Agent系统的设计与部署。
categories:
- AI研究
tags:
- AI Agent
- 术语澄清
- 构建框架
- 驾驭层
- 模型
draft: false
translated_at: '2026-05-26T06:07:37.463391'
---

# 驾驭、构建框架，以及值得厘清的AI Agent术语

当一个领域快速发展时，其词汇往往比共识理解进化得更快。术语开始模糊，在不同语境中被重复使用，或成为从未被充分解释的概念的简写。我们目前正在AI Agent领域看到这种情况，各种概念被混为一谈，有些被重新命名，有些被广泛使用几个月后便悄然消失。

这对新手来说可能令人不知所措，甚至对试图跟上最新发展的从业者也是如此。在ICLR 2026之后，我们中的一位（@ariG23498）提出了一个很好地捕捉了这种困惑的问题：

"在Agent的语境中，你们所说的'harness'和'scaffold'是什么意思？我在ICLR上听到了很多解释，但我不明白为什么它们没有收敛到一个统一的解释上。"

这份术语表是我们试图为那些不断出现但缺乏清晰、一致解释的术语奠定基础的努力。它并非旨在成为该领域每个术语的全面词典。相反，我们专注于那些经常被混淆、以不同方式重复使用，或被认为显而易见但实际上并非如此的概念。

无论你是在构建Agent、部署Agent，还是仅仅使用像Claude Code、Codex或Hermes Agent这样的工具，这些术语中的大多数都会出现。最后一节涵盖了特定于训练模型的概念，如果你从事这方面的工作，这会更相关。

这些术语中的许多还没有被普遍接受的定义，不同的框架以不同的方式使用同一个词。这里的目标不是强制执行一套正确的词汇，而是提供一个实用的心智模型，使讨论更容易理解。

让我们开始吧。

- 模型
- 构建框架（Scaffolding）
- 驾驭层（Harness）
- Agent（智能体）
- 上下文工程
- 策略
- 工具使用
- 技能
- 子Agent（Sub-agents）
- 训练
  - 强化学习环境
  - 训练器
  - 展开（Rollout）
  - 奖励
- 了解更多

## 模型

模型就是LLM（大语言模型）：它接收文本输入并产生文本输出（例如，Claude、Qwen、GPT、Kimi、DeepSeek……）。它本身在调用之间没有记忆，也没有循环。模型可以表达调用工具的意图，但它需要一个驾驭层（harness）来实际执行它。它回答一个提示词然后停止。将其包裹在构建框架（scaffolding）和驾驭层（harness）中，它就变成了一个Agent（智能体）。

## 构建框架（Scaffolding）

模型周围的行为定义层：系统提示词、工具描述、模型的响应如何被解析、它在各步骤之间记住什么（上下文管理）。它塑造了模型如何看待世界并在其中行动，无论是在训练期间还是在推理时。

像Claude Code、Codex和Antigravity CLI这样的产品将整个东西称为驾驭层（harness）。Claude Code自己的文档直接说明："Claude Code充当围绕Claude的Agent（智能体）驾驭层。"这是广义的用法：驾驭层意味着除了模型之外的一切。当需要分别推理它们时，比如在训练流程中，构建框架（scaffold）/驾驭层（harness）的区别最为重要。你也会听到"构建框架（scaffold）"被更广泛地用于涵盖驾驭层所依赖的任何基础设施：钩子、运行时配置，甚至目录结构。

像Claude Code和Codex这样的产品与其提供商的模型紧密耦合。其他像Antigravity CLI和Hermes Agent则允许你插入任何模型。

## 驾驭层（Harness）

Agent（智能体）内部的执行层：它调用模型，处理模型的工具调用，决定何时停止。驾驭层是让Agent运行起来的东西。上面定义的构建框架（scaffolding）是模型工作的基础：它的指令、它的工具、它的格式。

驾驭层工程（Harness engineering）是良好设计这一层的学科：决定Agent何时应该停止，错误如何处理，以及什么护栏能让它保持在正轨上。它适用于训练和推理。Addy Osmani的文章和OpenAI关于使用Codex构建的叙述都从推理方面涵盖了这一点。

在评估时，同样的模式表现为评估驾驭层（eval harness）：它不是收集训练数据，而是在模型检查点运行一组固定的场景并记录指标，而不是更新权重。

## Agent（智能体）

这个术语来自强化学习，其中Agent（智能体）只是一个接收观察并返回动作的函数。环境接收该动作并返回一个新的观察，循环重复。这个循环仍然是LLM Agent（智能体）工作的核心。

在LLM世界中，这个术语已经扩展。Agent（智能体）是模型加上它周围所有使其能够行动而不仅仅是回应的东西。它将原始的文本生成转化为可以在循环中行动的东西：接收信息，决定做什么，并对结果采取行动。

以一个编码Agent（智能体）作为具体例子。系统提示词、工具描述以及模型遵循的输出格式构成了构建框架（scaffolding）。调用模型、处理其工具调用并决定何时停止的循环是驾驭层（harness）。在训练时，驾驭层还并行运行许多这样的循环，并将结果反馈回来更新模型。

![Agent diagram showing Harness, Scaffold, and Model as components inside Agent, with Sub-agent below](/images/posts/a92963b7e669.png)

在社区中，通常表述为Agent = Model + Harness（@Vtrivedy10和Will Brown的推文供参考）。如果你不是模型，你就是驾驭层。造成大部分混淆的驾驭层和构建框架之间的细微区别正是上面两节所讨论的。

当人们谈论像Claude Code、Codex或Cursor这样的产品时，他们指的是构建在特定模型之上的特定驾驭层，它们被一起设计和优化。两个使用相同底层模型的产品可能感觉完全不同，因为它们的驾驭层做出了不同的选择。而将更好的模型交换到相同的驾驭层中也会改变体验。模型、驾驭层和产品是三个不同的东西。

## 上下文工程

设计进入Agent（智能体）上下文窗口的内容：模型在每个步骤看到什么、系统提示词、工具描述、对话历史、检索到的知识。这不是一次性的决定：随着模型运行，之前的轮次会塑造进入未来调用的内容，而驾驭层在整个运行过程中积极管理这一点。它适用于训练和推理，但出错代价截然不同。在训练时，模型看到的内容塑造了学习的内容。搞错了就要重新训练。在推理时，它只是文本：更改提示词并重新部署。HF上下文工程课程深入介绍了这一点。

记忆是其中的一部分。短期记忆是在单次运行期间保持在上下文窗口中的内容：对话历史、工具结果、先前的推理。长期记忆跨会话持久存在，存储在外部并按需检索，然后在相关时重新注入到上下文中。

## 策略

策略是Agent（智能体）遵循的行为：给定任何情况，它定义了采取每个可能动作的概率。在LLM系统中，部分策略是在模型权重中学习的，但行为也依赖于周围的构建框架（scaffolding）和驾驭层（harness）。同一个模型根据其提示词、工具、记忆和执行循环，行为可能大相径庭。
策略不是Agent（智能体）。策略定义行为；Agent（智能体）是在环境中行动的完整系统。将一个检查点包裹在构建框架和驾驭层中并部署它，你就得到了一个Agent（智能体），其行为就是策略。

## 工具使用

Agent（智能体）如何触及外部世界：API、代码解释器、数据库、网络搜索、文件系统。模型以结构化格式表达使用工具的意图。现代推理API将其作为一等对象呈现：驾驭层直接接收调用并将其路由到正确的函数。结果被反馈回上下文，循环继续。

## 技能

可复用、结构化的知识包，用于实现多步骤任务。其中，**工具**是一个动作（"运行此命令"），而**技能**则打包了完成目标所需的一切（"调查此漏洞、形成假设、编写修复方案"）。技能可在不同Agent（智能体）间移植，并按需加载。工具、技能与子Agent（智能体）之间的界限在不同框架中有所差异。[HF上下文工程课程](https://huggingface.co/learn/context-engineering-course/)深入介绍了技能相关内容。

## 子Agent（智能体）

由另一个Agent（智能体）调用的Agent（智能体），用于处理特定子任务。它拥有自己的模型和框架，独立进行推理，并返回结果。调用方Agent（智能体）无需了解其内部工作原理。这正是**子Agent（智能体）**与**工具**（函数调用）或**技能**（打包知识）的区别所在：子Agent（智能体）能够自行推理、使用工具，并可调用更深层的子Agent（智能体）。

## 训练

上述术语在训练或部署场景中均适用。以下四个术语专属于训练阶段：Agent（智能体）执行任务、获得评分，其模型权重随之更新。所有面向LLM（大语言模型）的强化学习训练系统均基于同一流程构建：

![展示RL训练流程的图片，包含RL环境、训练器和奖励，通过策略展开和更新策略连接](/images/posts/0c49bbd913a6.png)

### RL环境

环境是指任何可与之交互的对象：一种有状态的对象，接收动作作为输入，更新其内部状态，并返回观测结果。在LLM（大语言模型）语境中，动作通常是工具调用。文件系统是一个简单示例：执行`touch foo.txt`动作会通过创建文件来更新状态，而观测结果可能是更新后的文件列表。不同框架对此的定义存在差异。

我们近期发布了关于此主题的专门指南，为避免内容压缩，请参阅[《RL环境终极指南》](https://huggingface.co/learn/context-engineering-course/)以获取关于类型、框架和示例的完整解析。

### 训练器

训练器是提升Agent（智能体）性能的核心：它运行多个Agent（智能体）回合，对结果进行评分，并利用这些评分更新内部模型的权重。TRL的[GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer)是一个具体示例：一个同时处理回合生成、奖励评分和权重更新的单一类。

### 策略展开

策略展开是指Agent（智能体）从开始到结束的完整运行过程：Agent（智能体）看到了什么、做了什么、每一步获得了什么奖励。根据上下文，它也被称为**轨迹**或**跟踪**。这是强化学习算法学习的原始数据。

### 奖励

用于告知训练算法模型是否在改进的评分。它可以是**可验证的**（测试通过/失败、答案匹配）、**学习得到的**（人类偏好、LLM（大语言模型）作为评判者）、**稀疏的**（回合结束时的一个评分）或**密集的**（每一步都有一个评分）。训练器正是利用这些评分来实际更新内部模型的权重。关于每种类型的详细解析，请参阅Adithya指南中的[奖励架构](https://huggingface.co/learn/context-engineering-course/)部分。

**评分细则**将奖励分解为带有权重的显式维度，而非单一数值。[OpenEnv](https://github.com/huggingface/open-rl)和[Verifiers](https://github.com/huggingface/verifiers)将评分细则实现为可组合的对象（加权求和、顺序执行、门控机制）。

## 了解更多

- [@Vtrivedy10: Agent（智能体）框架剖析](https://x.com/vtrivedy10/status/1234567890)：框架组件的详细解析及其存在原因
- [Agent（智能体）框架工程](https://huggingface.co/blog/agent-harness)：Agent（智能体）= 模型 + 框架的收敛性框架，附编码Agent（智能体）示例
- [框架工程](https://openai.com/blog/agent-harness)：在Agent（智能体）优先的世界中利用Codex：完全使用Codex Agent（智能体）构建产品的真实案例，涵盖推理时的框架构建、反馈循环和上下文管理
- [工具模式渲染图谱](https://evalstate.ai/tool-schema-rendering-atlas)（evalstate）：不同模型如何将工具模式转化为提示词文本，展示各模型在应用提供商模板后实际看到的内容
- [Simon Willison的编码Agent（智能体）工作原理博客](https://simonwillison.net/2024/Dec/19/coding-agents/)：编码Agent（智能体）作为框架的工作原理
- [AI工程师讲座：AI中的框架深度解析](https://www.youtube.com/watch?v=xyz)：什么是框架以及如何构建框架
- [RL环境终极指南](https://huggingface.co/learn/context-engineering-course/)：逐框架比较与词汇翻译
- [持续改进我们的Agent（智能体）框架](https://cursor.sh/blog/agent-harness)：Cursor如何将其框架作为产品进行迭代
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)：标准评估框架

如果您发现任何定义不够精确，或遇到我们遗漏的术语，欢迎随时反馈。

感谢**Pedro Cuenca**、**Quentin Gallouédec**、**Shaun Smith**和**Adithya S Kolavi**对本文的审阅。

---

> 本文由AI自动翻译，原文链接：[Harness, Scaffold, and the AI Agent Terms Worth Getting Right](https://huggingface.co/blog/agent-glossary)
> 
> 翻译时间：2026-05-26 06:07
