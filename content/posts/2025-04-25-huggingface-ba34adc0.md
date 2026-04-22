---
title: PipelineRL：实现大模型强化学习中推理与训练的高效协同
title_original: PipelineRL
date: '2025-04-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ServiceNow/pipelinerl
author: ''
summary: 本文介绍了开源项目PipelineRL，它通过实时权重更新技术，解决了大规模语言模型强化学习中推理吞吐量与同策略数据收集之间的固有矛盾。该方法允许在训练过程中持续更新推理服务器的模型权重，而无需停止推理，从而在保持高推理吞吐量的同时，确保训练数据的时效性，实现更高效、稳定的RL训练。实验表明，PipelineRL使用简化的算法在多个基准测试上取得了有竞争力的结果。
categories:
- AI研究
tags:
- 强化学习
- 大语言模型
- 开源项目
- 模型训练
- 推理优化
draft: false
translated_at: '2026-04-22T04:57:59.613218'
---

# PipelineRL

![PipelineRL](/images/posts/6d896728da60.jpg)

我们很高兴开源 PipelineRL，这是一个实验性的强化学习实现，旨在解决大规模 LLM（大语言模型）强化学习中的一个基本挑战：推理吞吐量与同策略数据收集之间的权衡。PipelineRL 的核心创新在于 RL 训练期间的**实时权重更新**（见下图图 1）。这使得 PipelineRL 能够持续保持高推理吞吐量，并最小化用于生成轨迹的权重与最近更新的模型权重之间的延迟。结果是：为大语言模型提供快速且稳定的 RL 训练。

![image/jpeg](/images/posts/baf037c24605.jpg)

在这篇博客文章中，我们将展示：1）实时权重更新不会损害训练过程；2）与 Open-Reasoner-Zero 相比，PipelineRL 使用更简单的 RL 算法取得了有竞争力的结果。我们还将介绍模块化的 PipelineRL 架构，该架构便于尝试新的推理/训练器组合。

## 传统 RL 与 PipelineRL

在传统的 RL 方法中（图 1a），高吞吐量推理与同策略数据收集之间存在权衡。为了解释这种权衡，让我们首先从算法上定义传统 RL：

```python
current_policy = initial_policy
opt_state = init_optimizer(current_policy)

while True:
    
    
    inference_policy = current_policy
    list_of_prompts = [sample_prompts(training_batch_size) \
        for _ in range(num_grad_steps)]
    list_of_rollouts = [sample_rollouts(prompts, inference_policy) \
        for prompts in list_of_prompts]
    
    lag = 0 
    for rollouts in list_of_rollouts:
        current_policy, opt_state = policy_update(current_policy, opt_state, rollouts)
        lag += 1
    

```

为了实现高吞吐量，推理服务器必须使用大批次大小，从而为多个策略优化步骤生成数据。然而，每个优化步骤都会增加当前策略与使用推理策略收集的数据之间的延迟，使得收集的数据逐渐变得更具异策略性，对训练的效果降低。同策略学习需要用于单个优化步骤的数据。但使用大量 GPU 生产少量数据是低效的，因为这意味着每个 GPU 的批次大小很小。此外，当推理服务器完成短序列处理，只剩下少数最长序列在处理时，批次大小会下降。

PipelineRL（图 1b）通过实时权重更新来弥补这种权衡。我们在每个优化器步骤后更新推理服务器中的权重，**而从不停止推理**。我们只在所有推理服务器上暂停推理，暂停时间仅够接收新权重。实时权重更新允许推理服务器持续保持最佳批次大小，同时确保数据保持同策略或接近同策略，这分别带来了更好的 GPU 利用率和更有效的学习。

## PipelineRL 行之有效！

![image/png](/images/posts/a4e7d9dbb7bf.png)

为了展示 PipelineRL 的有效性和实时权重更新的优势，我们在 Open-Reasoner-Zero 数据集上训练了一个 7B 模型和一个 32B 模型。观察学习曲线，我们发现 PipelineRL 在流行的推理测试基准（AIME 2024 和 MATH 500）上的表现与 Open-Reasoner 相当或更优（见上图图 2）。

值得注意的是，我们的 RL 实现比 Open-Reasoner-Zero 简单得多。Open-Reasoner-Zero 使用了价值函数，而我们的实现是 GRPO 的简化版本。特别是，我们发现稳定的训练不需要信任域重要性权重截断。也不需要来自 DAPO 论文的超长序列过滤或奖励塑形。对于损失归一化，我们仅使用批次中的序列数量作为分母，给予所有 Token 相等的权重。我们没有使用 KL 惩罚，也没有使用熵奖励（尽管我们的实现确实支持参考模型 KL）。尽管我们的实现很简单，或者可能正因为如此，训练非常稳定，正如您在这份 wandb 报告中看到的那样。

人们可能会认为实时权重更新会导致训练过程不稳定，因为**序列生成是使用 KV 缓存中由先前模型版本计算的陈旧键和值**进行的。然而，我们的实验表明这不会对稳定性产生不利影响。

## PipelineRL 架构

![image/jpeg](/images/posts/988472ac2c89.jpg)

PipelineRL 采用模块化设计，旨在利用高度专业化推理和训练软件（SGLang、vLLM、Nvidia Dynamo、DeepSpeed、FSDP、TorchTitan、FastLLM 等）的快速改进。我们提出了推理和训练组件之间的清晰契约，允许在新型推理和训练解决方案出现时轻松集成。

### 推理契约

推理软件必须向 PipelineRL 暴露以下 API[1]：

1.  进程组初始化：在启动时，训练器 0（指定的协调器）向所有推理服务器发送 HTTP `POST /init_process_group` 请求。此请求初始化将用于发送权重更新的进程组。
2.  权重更新触发器：一旦训练器完成一个学习步骤（优化器步骤和权重收集），训练器 0 向推理端点提交 HTTP `POST /request_weight_update` 请求。该请求包含主训练器进程即将通过 NCCL 传输的权重的顺序和形状的详细信息。推理服务器必须暂停推理并接收权重广播。
3.  聊天完成：Actor 进程使用 HTTP `POST /v1/chat/completion` 请求与 Actor LLM 交互。

如果 `init_process_group` 和 `request_weight_update` API 成为行业标准，人们将能够即插即用地尝试将不同的推理实现与 PipelineRL 一起使用。

### 训练器契约

PipelineRL 训练代码一旦为每个训练器工作进程累积了足够数量的训练 Token，就会立即将新生成的训练数据提供给它们。任何暴露以下 Python API 的训练软件都可以与 PipelineRL 协同工作：

*   **工作进程初始化**：加载并分片训练权重和优化器状态。
*   **前向传播**：根据输入生成 Token 对数似然。
*   **反向传播步骤**：计算并累积代表所选 RL 目标的标量的梯度。
*   **优化器步骤**：执行优化器步骤。
*   **权重收集与广播**：优化器步骤之后，训练器软件必须逐层收集更新后的模型权重，为将其广播到推理服务器做准备。

PipelineRL 目前使用 HuggingFace `accelerate` 库，让用户可以在 DeepSpeed 和 FSDP 之间选择。但我们发现 `accelerate` 的契约过于灵活，可能会造成混淆。我们将转向如上所述的更严格的契约，这将使使用其他训练器变得更加容易。

## PipelineRL 的下一步是什么？

**即将推出的功能**。我们的实现仍然是实验性的，缺少一些重要功能。我们的首要任务包括使用协程进行更精确的推理批次大小控制、多模态支持和序列并行训练。我们也欢迎贡献更多的推理服务器和训练器集成。然而，我们不会试图将 `pipeline-rl` 仓库变成一个支持所有可能算法和奖励函数的框架。我们的看法是，`pipeline-rl` 应该是一个可修改且快速的 GRPO 参考实现，具有易于验证的奖励。如果您想使用 PipelineRL 进行研究项目，可以直接 Fork 该仓库并愉快地修改代码！

更多研究即将发布。我们需要更多分析来理解实时权重更新如何影响训练动态，并精确测量PipelineRL带来的加速效果。此外，关于PipelineRL与先前高度相关的LLM异步强化学习研究之间的相似性，也有诸多值得探讨之处。关于这些内容及更多发现，敬请期待我们即将发布的研究论文！

## 贡献者与致谢

Alexandre Piché在开发TapeAgents期间编写了我们RL代码的第一个同步版本。Dzmitry Bahdanau将代码重构为异步分布式架构，并实现了实时权重更新功能。Rafael Pardinas实现了序列打包功能。Ehsan Kamaloo协助运行实验。Xiaoyin Chen协助调试框架。

我们感谢先前LLM强化学习实现项目（如TRL、OpenRLHF和veRL）提供的诸多技巧借鉴。其他开源推理项目（如Simple-RL、Deepscaler、DAPO和OpenReasoner）的成果对稳定PipelineRL起到了关键作用。我们感谢Christopher Manning和Michael Noukhovitch提出的深刻见解。最后，感谢ServiceNow研究院团队和ServiceNow CoreLLM团队的杰出同事们。

[1] 当前代码中的合约机制略有不同，但我们正在按上述描述进行重构。

## 实验细节

本文报告的7B和32B实验均采用相同超参数：

- 批大小 4096
- 学习率 1e-6
- 最大生成token数 8192（注：OpenReasoner运行中允许生成16K tokens）

实验所用计算资源：

- 7B模型：2个节点运行约3.5天
- 32B模型：4个节点运行约6天

---

> 本文由AI自动翻译，原文链接：[PipelineRL](https://huggingface.co/blog/ServiceNow/pipelinerl)
> 
> 翻译时间：2026-04-22 04:57
