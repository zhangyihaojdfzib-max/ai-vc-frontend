---
title: EVA-Bench 2.0：三大领域121工具213场景的语音Agent基准
title_original: 'EVA-Bench Data 2.0: 3 Domains, 121 Tools, 213 Scenarios'
date: '2026-06-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ServiceNow-AI/eva-bench-data
author: ''
summary: EVA-Bench 2.0将语音Agent评估从单一企业领域扩展至航空客服、企业IT服务管理和医疗HR服务三大领域，覆盖121个工具上的213个场景。数据集遵循语音优先、真实性、多样性、身份验证和可复现性五项原则，包含单一意图、多意图及对抗性通话场景。所有场景均经GPT-5.4、Gemini
  3.1 Pro和Claude Opus 4.6验证可解，并开源提供。文章详细介绍了数据设计原则、场景生成流程及SyGra流水线，为语音Agent评估提供标准化基准。
categories:
- AI研究
tags:
- 语音Agent
- 基准测试
- 企业AI
- 数据集
- 多领域评估
draft: false
translated_at: '2026-06-05T06:20:35.962609'
---

# EVA-Bench 数据 2.0：3 个领域、121 个工具、213 个场景

![截图 2026-06-03 下午 4.59.53](/images/posts/f0b6d6eeccc8.png)

## 引言

语音 Agent（智能体）的失败通常高度依赖于特定领域。一个能够完美处理航班改签交易中字母数字确认码的系统，可能在处理 HR 系统中的复杂政策时出现问题。不同领域考验 Agent（智能体）适应不同词汇、工作流复杂度和用户期望的能力。因此，在此次发布中，EVA-Bench 从一个企业领域扩展到三个：航空公司客户服务管理（CSM）、企业 IT 服务管理（ITSM）和医疗 HR 服务交付（HRSD）。它们共同涵盖了 121 个工具上的 213 个评估场景，场景覆盖范围相比我们最初的发布增加了约 4 倍。每个场景都针对三个前沿模型（OpenAI GPT-5.4、Google Gemini 3.1 Pro 和 Anthropic Claude Opus 4.6）验证了可解性，确保该基准既具有挑战性又公平。所有三个数据集均为开源并可下载：

```python
from datasets import load_dataset


airline = load_dataset("ServiceNow-AI/eva-bench", "airline", split="test")

itsm = load_dataset("ServiceNow-AI/eva-bench", "itsm", split="test")

hrsd = load_dataset("ServiceNow-AI/eva-bench", "medical", split="test")

```

EVA-Bench 面向多个受众构建。如果你正在评估一个语音 Agent（智能体），你可以让它运行在一组多样化的、涵盖 35 个以上不同工作流的真实企业场景上。如果你正在构建自己的评估数据集，本文详细描述了我们的端到端生成和验证过程，足以作为实用参考。我们逐步介绍了每个领域是如何设计和生成的，并深入探讨了两个新增领域。我们还预告了即将推出的多语言扩展，这将把该基准的覆盖范围扩展到仅限英语的企业部署之外。

## 数据设计原则

五项原则指导了所有三个领域的 EVA-Bench 数据集设计。

**语音优先范围。** 并非每个企业工作流都适合纳入语音基准。我们首先确定了每个领域中实际通过电话处理的哪些任务，然后从该子集中选择了最常见的流程。这使场景立足于真实的通话模式。

**真实性。** 工具模式（Schema）是根据生产平台使用的 API 类型建模的。场景策略源自实际的企业约束。对于医疗 HRSD 领域，这意味着将场景立足于真实的美国医疗政策和行政系统，包括 NPI 号码、FMLA 和保险覆盖范围，以便基准能够反映从业者在现实生活中遇到的领域情况。

**多样性。** 仅仅通过重复相同的任务来扩展数据集提供的评估信号有限。为避免这种情况，我们为每个领域定义了特定的工作流，并在三种场景类型中进行采样：单一意图通话、单个对话中包含最多四个意图的多意图通话，以及对抗性通话（呼叫者试图绕过故障排除步骤、错误分类紧急程度或访问其无权查看的记录）。在单一和多意图场景中，我们还包含了用户目标无法满足的情况，因为真实的通话量并非全是顺利路径，并且根据我们的经验，模型在处理无法满足的目标时往往比处理成功交互时更困难。

**身份验证。** 先前的工作（EVA-Bench 和 τ-Voice）已将身份验证确定为语音 Agent（智能体）最一致的失败点之一。EVA-Bench 中的每个领域都包含身份验证流程，并且具体机制根据任务进行调整。例如，基于 OTP 的权限提升仅在生产系统实际需要时出现，而非统一应用于所有场景。

**可复现性。** 如果没有可复现的场景，就很难知道分数差异反映的是真实的能力差距还是场景执行方式的产物。我们设计数据集时确保每个场景只有一条正确的解决路径。用户目标构建确保模拟器始终拥有保持一致行为所需的信息和指令，并且场景生成会明确检查并消除任何多个有效操作序列可能产生相同结果的情况。

## 场景生成

**联合生成。** 场景使用 SyGra（一种基于图的合成数据生成流水线）生成，以 GPT-5.4 作为骨干模型。每个场景需要三个联合一致的组件，这些组件一起生成，以防止独立生成组件时出现的不一致：

**用户目标。** 可复现性要求用户模拟器在每次运行场景时行为一致。模糊的意图陈述无法实现这一点：模拟器会在不同运行中做出不同的判断，产生不一致的评估信号。为消除这种情况，用户目标被构建为一个决策树，覆盖模拟器可能遇到的每种情况。用户目标明确指定了用户应该询问的具体内容，以及一个协商序列，该序列明确指定何时坚持、何时询问替代方案以及何时接受。常见的边缘情况，例如是否接受候补航班或备选机场，通过明确的指令处理，而不是留给模拟器去解释。解决条件要求有已完成操作的证据，例如确认号码或案例 ID，而不是口头承诺，因此模拟器会一直通话直到操作实际确认。结果是用户表现得像一个一致、真实的呼叫者，而不是即兴发挥。

**初始场景数据库。** Agent（智能体）的工具将在场景期间查询和修改的后端状态。与用户目标联合生成，以确保用户目标中引用的每个实体（例如预订 ID、账户详情和身份验证凭据）在数据库中都存在且一致。

**预期最终数据库状态（真实值）。** 我们通过让生成 LLM（大语言模型）基于 Agent（智能体）指令、用户目标和初始场景数据库运行，生成完整的操作轨迹，从而推导出预期结果。当 LLM（大语言模型）执行写入工具调用时，数据库会逐步更新，由此产生的最终状态成为评估期间验证器检查的真实值。

联合生成至关重要，因为这三个组件是深度相互依赖的。独立生成会引入静默的不一致，例如用户目标中引用的案例 ID 在场景数据库中不存在，这将完全破坏评估信号。为确保一致性，我们在每次生成尝试后运行一个多阶段验证循环，并将任何失败反馈给生成步骤，该步骤会重试直到所有检查通过。验证分三步进行。

- 结构检查根据 Pydantic 模式（Schema）验证场景数据库，捕获类型错误和缺失字段。
- 基于 LLM（大语言模型）的验证器更全面地检查场景的一致性：目标中面向用户的细节是否与数据库记录匹配，交叉引用是否内部有效，以及身份验证数据是否正确配置。
- 基于 LLM（大语言模型）的轨迹验证过程根据策略合规性、正确的操作顺序、所有必需最终操作的完成情况以及不存在会引入非确定性的替代写入路径，检查完整的对话轨迹。

## 进一步验证

在SyGra生成之后，所有场景都经过了多轮人工审核。审核人员验证了以下内容：(1) 同一领域内各场景的策略应用保持一致；(2) 用户目标足够明确，仅对应唯一正确的解决方案；(3) 预期最终状态与用户目标及初始数据库在逻辑上保持一致；(4) 对抗性场景被正确设定，并具有清晰可识别的策略违规行为。存在歧义或不一致的记录已被修正或剔除。

作为最终检查，我们在每个场景的纯文本版本上运行了三个前沿模型——OpenAI GPT-5.4、Google Gemini 3.1 Pro和Anthropic Claude Opus 4.6，跳过了音频管道并直接提供对话转录文本。对于任何模型在任务完成度上得分为零的场景，我们均手动调查了失败原因：是真正的模型错误，还是数据集问题——例如策略表述模糊、用户目标定义不充分、工具执行器存在缺陷，或初始与预期数据库状态不一致。存在已识别数据集问题的记录已被修正或移除。所有选定的样本至少能被其中一个前沿模型解决。

## 数据集深度解析

我们创建了三个面向不同企业领域的数据集，每个数据集都针对语音Agent的特定难度维度进行设计。三者均要求对语音中的结构化命名实体（如确认码和员工标识符）进行准确转录，但在主要挑战和工具数量上有所不同。

以下是我们对两个新数据集的深度解析：企业ITSM与医疗HRSD。

![Screenshot 2026-06-03 at 4.19.42 PM](/images/posts/ade583916a19.png)

![Screenshot 2026-06-03 at 4.25.43 PM](/images/posts/dd1bcd011e60.png)

## 多语言支持

仅基于英语的评估无法充分反映语音Agent在其他语言中的实际表现。语音识别准确率、转录保真度和对话流畅度可能因语言特性而各有下降，这意味着在英语中表现优异的语音Agent在部署到其他语言环境时可能完全失效。为了让从业者深入了解多语言部署的真实情况，我们正在增加对更多语言的支持，不仅调整对话语言，还针对每种目标语言和文化调整评估管道：

- 场景中提及的地点名称
- 用户的姓名和电子邮件地址
- 本地化的电话号码

这使得用户模拟器能够以所选语言提供真实的体验。除数据集外，我们还在更新评估指标和评判机制，以构建跨语言的可信评估体系。

## 获取数据

EVA-Bench在MIT许可证下完全开源。数据集、评估框架和排行榜均公开可用。您可以在HuggingFace数据集页面下载数据集并查看单个记录。使用Hugging Face的datasets库可直接加载任意数据集：

```python
from datasets import load_dataset


airline = load_dataset("ServiceNow-AI/eva-bench", "airline", split="test")

itsm = load_dataset("ServiceNow-AI/eva-bench", "itsm", split="test")

hrsd = load_dataset("ServiceNow-AI/eva-bench", "medical", split="test")

```

每条记录包含结构化的用户目标、初始场景数据库以及真实预期的最终数据库状态——运行完整的Bot-to-Bot评估所需的一切。有关设置说明、代码和贡献指南，请参阅GitHub仓库。

## 引用

```
@misc{bogavelli2026evabenchnewendtoendframework,
      title={EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents}, 
      author={Tara Bogavelli and Gabrielle Gauthier Melançon and Katrina Stankiewicz and Oluwanifemi Bamgbose and Fanny Riols and Hoang H. Nguyen and Raghav Mehndiratta and Lindsay Devon Brin and Joseph Marinier and Hari Subramani and Anil Madamala and Sridhar Krishna Nemala and Srinivas Sunkara},
      year={2026},
      eprint={2605.13841},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2605.13841}, 
}

@misc{ray2026tauvoicebenchmarkingfullduplexvoice,
      title={$\tau$-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains}, 
      author={Soham Ray and Keshav Dhandhania and Victor Barres and Karthik Narasimhan},
      year={2026},
      eprint={2603.13686},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2603.13686}, 
}

@misc{pradhan2025sygraunifiedgraphbasedframework,
      title={SyGra: A Unified Graph-Based Framework for Scalable Generation, Quality Tagging, and Management of Synthetic Data}, 
      author={Bidyapati Pradhan and Surajit Dasgupta and Amit Kumar Saha and Omkar Anustoop and Sriram Puttagunta and Vipul Mittal and Gopal Sarda},
      year={2025},
      eprint={2508.15432},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2508.15432}, 
}

```

---

> 本文由AI自动翻译，原文链接：[EVA-Bench Data 2.0: 3 Domains, 121 Tools, 213 Scenarios](https://huggingface.co/blog/ServiceNow-AI/eva-bench-data)
> 
> 翻译时间：2026-06-05 06:20
