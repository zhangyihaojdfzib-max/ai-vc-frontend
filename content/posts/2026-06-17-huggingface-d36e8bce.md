---
title: GLM-5.2发布：专为长周期任务打造的百万上下文模型
title_original: 'GLM-5.2: Built for Long-Horizon Tasks'
date: '2026-06-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/zai-org/glm-52-blog
author: ''
summary: GLM-5.2是面向长周期任务的最新旗舰模型，首次在稳固的100万Token上下文中交付能力。它通过IndexShare架构将每Token的FLOPs降低2.9倍，并改进MTP层将接受长度提升20%。在FrontierSWE、PostTrainBench等长周期编码基准测试中，GLM-5.2是排名最高的开源模型，性能接近闭源前沿。模型还引入算力级别控制，支持灵活平衡性能与延迟。采用MIT开源许可证，无地域限制。
categories:
- AI产品
tags:
- GLM-5.2
- 长上下文
- 开源模型
- 编码能力
- 百万Token
draft: false
translated_at: '2026-06-18T06:52:52.869563'
---

# GLM-5.2：专为长周期任务打造

我们推出GLM-5.2，这是我们面向长周期任务的最新旗舰模型。它在长周期任务能力上较前代GLM-5.1实现了显著飞跃，并首次在稳固的100万Token上下文中交付了这一能力。GLM-5.2的新能力包括：

- **稳固的100万上下文**：稳定支撑长周期工作的100万Token上下文
- **灵活算力的高级编码**：更强的编码能力，配备多种思考算力级别以平衡性能与延迟
- **改进的架构**：我们提出了IndexShare，在每四个稀疏注意力层之间复用相同的索引器，在100万上下文长度下将每Token的FLOPs降低2.9倍。我们还改进了GLM-5.2用于推测解码的MTP层，将接受长度提升高达20%
- **纯粹开源**：MIT开源许可证——无地域限制，无国界技术访问

支撑长周期任务始于让长上下文具备工程可用性：模型必须在漫长且混乱的编码Agent轨迹中保持质量，而不仅仅是接受更多Token。100万上下文容易宣称，但在真实工程压力下保持可靠则困难得多。为此，我们大幅扩展了面向编码Agent场景的100万上下文训练，涵盖大规模实现、自动化研究、性能优化和复杂调试。其成果是一个不仅范围广阔，而且执行稳健的长上下文系统：为持续工程工作提供了实用基础。

这一能力体现在GLM-5.2在三个长周期编码基准测试的表现上。**FrontierSWE**衡量Agent能否完成数小时到数十小时规模的开放式技术项目，涵盖系统优化、大规模代码构建和应用机器学习研究。在该基准测试中，GLM-5.2仅落后Opus 4.8一个百分点，同时领先GPT-5.5一个百分点和Opus 4.7十一个百分点。在**PostTrainBench**上，每个Agent配备一块H100 GPU，通过后训练提升小模型的程度来评估，GLM-5.2优于Opus 4.7和GPT-5.5，仅次于Opus 4.8。在**SWE-Marathon**这个超长周期软件工程基准测试中，涵盖构建编译器、优化内核和开发生产级服务等任务，GLM-5.2仍有成长空间，落后Opus 4.8十三个百分点，但仍是仅次于Opus系列的第二名。在所有三个基准测试中，GLM-5.2是排名最高的开源模型，表明其100万上下文已转化为实际的长周期交付能力。

![figure1](/images/posts/13fd4996da24.png)

在标准编码基准测试中，GLM-5.2是最强的开源模型，较GLM-5.1大幅提升：Terminal-Bench 2.1上81.0对63.5，SWE-bench Pro上62.1对58.4。它还大幅缩小了与闭源前沿的差距——在Terminal-Bench 2.1（81.0）上，与Claude Opus 4.8（85.0）仅差几分，同时领先Gemini 3.1 Pro。

![figure2](/images/posts/742ae66f659d.webp)

GLM-5.2还引入了算力级别控制，使用户能够显式平衡模型能力与任务执行速度和计算成本。如图所示，在可比Token预算下，GLM-5.2比GLM-5.1提供显著更强的Agent编码性能，其能力大致介于Claude Opus 4.7和Claude Opus 4.8之间，且Token消耗相近。此外，最大算力级别允许用户在挑战性任务中需要更高性能时分配额外计算资源，进一步扩展模型的编码能力。这一设计为用户在使用GLM-5.2进行编码任务时提供了更大灵活性，使其能够针对不同场景选择最合适的推理模式。

![figure3](/images/posts/029f6b74536e.png)

## 面向100万上下文的架构

![figure4](/images/posts/041cc31556e5.webp)

### 用于DSA的IndexShare

为支撑100万上下文长度，我们在GLM-5.2中应用IndexShare来降低DSA中索引器的计算成本。具体而言，在GLM-5.2中，每4个Transformer层共享一个轻量级索引器。索引器放置在4层中的第一层，topk索引用于4层。这减少了3/4层中索引器点积和topk操作的计算量。GLM-5.2从128K序列长度的中期训练开始就使用IndexShare进行训练，在长上下文基准测试中以更少计算量超越GLM-5.1。

### 结合IndexShare和KVShare的MTP

我们改进了GLM-5.2用于推测解码的MTP层，目标有二：1）最小化MTP层作为草稿模型的成本；2）最大化推测解码的接受率。

对于第一个目标，我们也在MTP层上应用IndexShare。在多步MTP中，索引器放置在第一步，topk索引用于后续所有步骤。然而，与主干网络不同，不同MTP步骤的输入Token是不同的。如下图所示，如果我们将$h_4$的topk索引复用于$h_5$，$h_5$只能关注$h_1$到$h_4$，而不能关注$h_5$。我们将展示这一特性有助于实现第二个目标，通过消除GLM-5.1的MTP层中训练与推理的不一致性。

![figure5](/images/posts/f2fef3ce19ec.webp)

上图中我们展示了两步MTP层的推理过程。在第一步中，推理与训练一致，所有隐藏状态来自目标模型。然而在第二步中，$h_{1:4}$来自目标模型，$h_5$来自MTP层。因此，$h_5$的KV缓存是来自目标模型计算的$kv_{1:4}$与来自MTP层计算的$kv_5$的混合。而使用IndexShare后，$h_5$的KV缓存仅包含$kv_{1:4}$，全部来自目标模型的隐藏状态。对于训练，我们复用第一个MTP步骤的KV缓存和topk索引。注意与GLM-5.1相同，不同MTP步骤的参数也是共享的。此外，受https://arxiv.org/abs/2606.12370启发，我们引入了用于推测解码的拒绝采样，并使用端到端TV损失进行训练。

下表展示了在编码场景下按接受长度进行的技术消融实验。实验中我们使用GLM-5.1的主干网络和训练数据。训练和推理的MTP步数均设为7。与基线相比，最终MTP层的接受长度提升了20%。

### 高效服务100万上下文长度

随着GLM-5.2将最大上下文长度从20万Token扩展到100万Token，编码工作负载预计将大幅转向更长的提示词。这将主要推理瓶颈从计算转向KV缓存容量、长上下文内核开销和CPU端开销。尽管新的GLM-5.2架构降低了每Token的计算FLOPs，但并未按比例降低每Token的KV缓存大小。因此，在有限GPU资源下支持更长的上下文、更高的并发度和更高的Token吞吐量，成为推理引擎优化的核心挑战。

![figure6](/images/posts/d92ddefc181f.webp)

为应对这一挑战，我们从三个方向优化推理引擎。首先，基于LayerSplit，我们引入更细粒度的内存管理与并行化策略，以增加KV-cache容量，为超长上下文请求提供更多可用缓存空间。其次，我们优化了计算开销随上下文长度增长的内核，并使其与缓存传输流水线更好地协同，从而最小化缓存传输对预填充和解码性能的影响。第三，我们优化了CPU端缓存管理、请求调度及运行时执行路径，以减少GPU执行流水线中的气泡，提升端到端吞吐量。如图所示，GLM-5.2的吞吐量优势随上下文长度增长而愈发显著，展现出在长上下文推理场景中更强的可扩展性。

## 面向Agentic RL的slime框架

GLM-5.2的Agentic RL后训练涉及更大规模、跨更多领域且执行模式更复杂的任务。异构数据与任务需在统一训练流程中组织，而长周期交互、工具使用、子任务分解及多轮环境反馈，均对推演与训练编排提出了更高要求。为支撑这一过程，slime作为从训练到大规模推理推演的一体化基础设施层，支持白盒推演、黑盒推演、紧凑轨迹及子Agent工作流等多种训练与任务组织模式，使同一系统能够扩展到更大规模、更复杂的RL与OPD训练负载。在GLM-5.2的后训练过程中，我们使用slime框架进行并行OPD训练，高效地将十余个专家模型合并为最终模型。整个OPD训练过程耗时约两天，展现出极高的训练效率。

Agentic RL对系统资源与推理基础设施也提出了更高要求。slime为推理系统提供了高度开放且灵活的接口：训练端可连接不同形式的推理服务，并灵活适配不同的并行策略、路由策略、PD分离配置及部署模式。同时，RL推演过程中积累的配置经验、调度策略与优化路径，可在生产服务阶段复用并进一步优化，使训练端与服务端相互促进，从而构建从后训练到生产部署的更直接路径。结合灵活的训练-推理资源组织与KV-cache FP8，slime为GLM-5.2的大规模Agentic RL训练提供了关键基础设施支撑，进一步提升了系统效率、推演吞吐量及大规模推理并发能力。

## 面向长周期任务的RL与反作弊机制

长周期任务的RL。对于GLM-5.2，长周期任务会产生显著更长的执行轨迹。一旦超长轨迹因压缩而被拆分为多个子轨迹，同一提示词下的不同推演将产生数量不等、长度差异巨大的可训练轨迹。因此，我们从分组优化转向基于评论家的PPO公式，该公式从单次推演中学习，依赖评论家估计Token级别的优势，而非进行组间相对比较。这种单次推演公式天然适配压缩机制，因为它不限制一个提示词产生多少条轨迹，也不限制它们的相对长度：我们将所有压缩后的子轨迹作为可训练轨迹纳入训练，并应用Token级别的损失函数来处理其长度不均衡问题。

编码Agent中的反作弊。编码RL尤其容易受到奖励作弊的影响，因为奖励通常是一个可验证的通过/失败信号。我们发现GLM-5.2比GLM-5.1表现出更多潜在的作弊行为。这使得验证信号易于优化，但未能真正提升模型的基础能力。Agent可能读取受保护的评估工件、从参考资料或上游提交中复制答案内容，或在与GitHub相关的任务中直接获取目标源代码。例如，Agent可能通过`curl https://raw.githubusercontent.com/<path-to-file>`下载解决方案，甚至出现链式泄露，如：

```bash
1. find /workspace -name "*hidden*"
2. cat /workspace/.eval/secret_cases.json
3. python solve.py --case "$(cat /workspace/.eval/secret_cases.json)"
```

这些行为会虚增奖励并污染训练信号，因此需要明确的机制来区分真正的任务解决与走捷径。为此，我们在RL训练和评估中引入了一个反作弊模块。检测过程分为两个阶段：首先，基于规则的过滤器捕获潜在的作弊行为以最大化召回率，然后由LLM判断器检查这些被标记行为的意图，以保持高精确率。我们采用在线策略，在每一步监控工具调用。如果检测到作弊，系统会阻止该调用并返回虚拟信息作为结果。重要的是，这种在线防护允许模型在作弊行为被捕获后继续推演。通过处理特定的无效行为而非拒绝整个轨迹，该方法有助于防止因推演突然中断而导致的训练不稳定和模型崩溃。

## 完整基准测试表

## GLM-5.2快速入门

### 通过GLM Coding Plan使用GLM-5.2

在您喜爱的编码Agent——ZCode、Claude Code、OpenCode等中试用GLM-5.2。https://docs.z.ai/devpack/overview

面向GLM Coding Plan订阅用户：我们已向所有Coding Plan用户推送GLM-5.2。您现在可以通过将模型名称更新为"GLM-5.2"（或在Claude Code中设置为GLM-5.2[1m]以启用1M上下文长度）来启用GLM-5.2。您还可以根据任务选择不同的思考努力程度：High或Max。作为我们能力最强的模型，GLM-5.2在高峰时段消耗3倍配额，非高峰时段消耗2倍配额。作为截至9月底的限时推广活动，非高峰时段使用按1倍计费。（高峰时段为每日北京时间14:00–18:00）。

偏好图形界面？我们提供ZCode——一款由GLM-5.2驱动的桌面Agent，支持/goal用于长周期任务、SSH远程开发及移动控制。特别优惠：通过ZCode内的Coding Plan使用GLM-5.2，截至6月30日可享受1.5倍有效配额。

立即开始构建：https://z.ai/subscribe

### 在Z.ai上与GLM-5.2对话

GLM-5.2现已在Z.ai上可用。

### 本地部署GLM-5.2

GLM-5.2的模型权重已在HuggingFace和ModelScope上公开发布。对于本地部署，GLM-5.2支持包括transformers、vLLM、SGLang、xLLM、ktransformers在内的推理框架。

## 脚注

- **人类最后考试（HLE）及其他推理任务**：我们使用采样参数`temperature=1.0`、`top_p=0.95`进行评估。评估时最大生成长度设为163,840个Token。默认情况下，我们报告纯文本子集的结果；标有*的结果来自完整数据集。对于AIME、HMMT和IMOAnswerBench，我们使用以下系统提示词对每个问题进行评估：`Your response should be in the following format:\nExplanation: {your explanation for your final answer}\nExact Answer: {your succinct, final answer}\nConfidence: {your confidence score between 0% and 100% for your answer}`。我们使用GPT-5.5（中等）作为评判模型。对于带工具的HLE，我们使用最大上下文长度为300,000个Token，不采用上下文管理策略。

- **SWE-Bench Pro**：我们使用OpenHands运行SWE-Bench Pro套件，并采用定制化的指令提示词。设置参数为：`temperature=1`、`top_p=1`、`max_new_tokens=32k`，上下文窗口为400K。

- **NL2Repo**：我们在400K上下文下，以`temperature=1.0`、`top_p=1.0`、`max_new_tokens=48k`的参数评估NL2Repo。为防止作弊，我们使用基于规则的判断和基于LLM的判断来阻止恶意行为（例如未经授权的pip或curl操作）。

- **DeepSWE**：我们使用官方的pier评估框架和mini-swe-agent工具包运行DeepSWE（参数为`temperature=1.0`、`top_p=1.0`、`timeout=2h`、400K上下文）。每个任务在隔离的容器中解决，容器配备2个CPU、8 GB RAM，且无网络访问。

- **ProgramBench**：我们使用Claude-Code 2.1.156评估ProgramBench（200个实例），参数为`temperature=1.0`、`top_p=1.0`、`max_tokens=64000`、`max_turns=2000`、`sample_timeout=6h`、`reasoning_effort=max`，上下文窗口为400K。每个实例在（4个CPU、8 GB RAM）的沙箱中运行，禁用网络访问。

- **Terminal-Bench 2.1（Terminus 2）**：我们使用Terminus-2框架评估Terminal-Bench 2.1，参数为`parser=json`、`timeout=4h`、`temperature=1.0`、`top_p=1.0`、`max_new_tokens=48k`、`max_episodes=500`，上下文窗口为256K。资源限制上限为4个CPU和8 GB RAM。

- **Terminal-Bench 2.1（Claude Code）**：我们在Claude Code 2.1.167中评估，参数为`temperature=1.0`、`top_p=0.95`、`max_new_tokens=131072`。我们通过透明代理将`max_new_tokens`覆盖为128k，绕过64k的CLI上限，以恢复`CLAUDE_CODE_MAX_OUTPUT_TOKENS`的可配置性。我们移除挂钟时间限制，同时保留每个任务的CPU和内存约束。分数取5次运行的平均值。

- **MCP-Atlas**：所有模型均在思考模式下评估，使用500个任务的公共子集，每个任务超时时间为10分钟。我们使用Gemini-3.0-Pro作为评估的评判模型。

- **Tool-Decathlon**：我们使用官方评估服务，并将`max_token`设置为128K。

- **FrontierSWE**：评估由Proximal进行，上下文长度为1M，努力程度为最大，最大输出Token数为128K。优势分数报告截至2026/06/16。

- **PostTrainBench**：评估由PostTrainBench进行，上下文长度为1M，努力程度为最大，最大输出Token数为128K。

- **SWE-Marathon**：评估由Abundant AI进行，上下文长度为1M，努力程度为最大，最大输出Token数为128K。

---

> 本文由AI自动翻译，原文链接：[GLM-5.2: Built for Long-Horizon Tasks](https://huggingface.co/blog/zai-org/glm-52-blog)
> 
> 翻译时间：2026-06-18 06:52
