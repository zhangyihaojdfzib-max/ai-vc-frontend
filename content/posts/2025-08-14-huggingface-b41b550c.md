---
title: Kimina-Prover-RL：开源Lean4定理证明训练流程
title_original: Kimina-Prover-RL
date: '2025-08-14'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/AI-MO/kimina-prover-rl
author: ''
summary: 本文介绍了kimina-prover-rl，一个用于训练大语言模型在Lean4中进行形式化定理证明的开源训练流程。该流程采用“先推理后生成”的两阶段范式，结合GRPO强化学习方法，并兼容Verl框架。作者发布了两个新模型：1.7B参数模型在MiniF2F基准测试达到76.63%
  Pass@32，0.6B参数模型达到71.30% Pass@32，均为同规模开源模型的新SOTA。文章还详细介绍了训练流程的核心组件、数据集构建方法及验证工具。
categories:
- AI研究
tags:
- 定理证明
- 强化学习
- 开源模型
- 形式化验证
- Lean4
draft: false
translated_at: '2026-02-18T04:35:24.105569'
---

# Kimina-Prover-RL

这是 Kimina Prover 的精简版训练流程，保留了核心功能，并与 verl 完全兼容。

![image/png](/images/posts/15ef1bd72057.png)

我们很高兴推出 kimina-prover-rl，这是一个用于在 Lean 4 中进行形式化定理证明的开源训练流程。它基于一种结构化的“先推理后生成”范式，灵感来源于 DeepSeek-R1。

该训练流程是我们用于训练 Kimina Prover 系统的简化版本，保留了系统的关键组件，并完全兼容开源的 Verl 框架。

它作为 Verl 的一个分支版本的一部分发布，其中包含了完整的训练配方，位于 `recipe/kimina-prover-rl` 目录下，允许任何人复现我们的实验或将该配置适配到他们自己的模型和数据集。设置和启动该流程的所有信息都可以在配方的 `README` 文件中找到。

作为该训练流程的成果，我们发布了两个模型：

- **AI-MO/Kimina-Prover-RL-1.7B**，一个拥有 17 亿参数的模型，在 MiniF2F 基准测试上达到了 **76.63% Pass@32** —— 为该规模类别的开源模型设定了新的技术水平。
- **AI-MO/Kimina-Prover-RL-0.6B**，一个拥有 6 亿参数的模型，在 MiniF2F 基准测试上达到了 **71.30% Pass@32** —— 同样为该规模类别的开源模型设定了新的技术水平。

## 简介

kimina-prover-rl 是一个训练流程，旨在教导大语言模型解决 Lean 4 中的形式化证明目标。它采用两阶段的输出结构：一段自然语言推理轨迹，后跟相应的 Lean 代码。

这种受 DeepSeek-R1 启发的范式，使模型能够将规划与执行分离，从而提升可解释性、错误恢复能力和更强的泛化能力。

为了在此推理框架下训练模型，我们应用了 GRPO —— 一种专为 LLM 设计的强化学习方法。这个开源版本的 Kimina-prover 训练流程是使用 RL 库 **Verl** 实现的。

在 GRPO 的 rollout 阶段，模型会为每个提示词生成 N 个输出。任何其 Lean 代码能通过我们的 `kimina-lean-server` 被 Lean 成功验证的输出，都会获得 1 的奖励。

我们为该框架添加了两个主要特性：

- **格式检查奖励**：教导模型结构化其输出。
- **错误纠正轮次**：鼓励模型从失败信号中学习。

## Kimina-Client

在训练期间，需要同时验证大量的 Lean 4 证明候选。为了高效处理，我们需要一个高吞吐量的验证系统。

为了满足这一需求，Numina 和 Kimi 开发了一个名为 `kimina-lean-server` 的开源服务器，它支持使用 Lean 4 进行大规模并行证明检查。

为了简化集成，我们还提供了 `kimina-client`，这是一个轻量级的 Python 包（可在 PyPI 上获取），它为与服务器 API 交互提供了一个简洁的接口。

## 数据集

我们使用 **Kimina-Prover-Promptset** 进行训练，这是 **NuminaMath-LEAN** 数据集的一个精选子集。

对于此训练设置，我们按如下方式过滤和预处理数据集：

- **移除简单问题**：历史胜率高于 `0.5` 的问题，只保留数据集中具有挑战性的陈述。
- **生成变体**：使用 Gemini 生成现有问题的变体，以增加多样性。
- **复制难题**：在训练期间给予难题更多权重。

最终得到的数据集包含了用于改进 Lean 4 定理证明模型的、具有挑战性的高价值问题。

NuminaMath-LEAN-RL 也是用于训练 **AI-MO/Kimina-Prover-RL-1.7B** 和 **AI-MO/Kimina-Prover-RL-0.6B** 的数据集。

输入格式示例：

```
Think about and solve the following problems step by step in Lean 4.

# Problem:
Find all primes that are the difference of the fourth powers of two integers.

# Formal Statement:
'''lean4
import Mathlib

theorem number_theory_4487 : {p : ℕ | p.Prime ∧ ∃ a b, p = a ^ 4 - b ^ 4} = ∅ := by
'''

```

## 格式奖励

我们推理训练流程的核心思想是将 LLM 的输出结构化为两个阶段：一个思考块后跟一个 lean4 代码块：

1.  一个推理块 ( ... )
2.  一个 Lean 4 代码块

```
<think>
To prove the statement, we use induction on n.
The base case is trivial, and the inductive step follows by applying the hypothesis.
</think>

'''lean4
theorem my_thm : ∀ n, f n = g n := by
  induction n with
  | zero => simp
  | succ n ih => simp [ih]
'''

```

每个 rollout 都会被**验证**以确保遵守此格式。如果输出格式错误 —— 例如缺少 `<think>` 块或代码放置不当 —— 无论证明是否实际有效，模型都会获得**零奖励**。

这强制执行了一致性，并教导模型可靠地结构化其输出。

在 kimina-prover 中，这些检查不仅仅是简单地验证 `<think>` 和 lean4 块的存在：

- 确保每个输出中恰好有一个 `<think>...</think>` 块和一个 lean4 代码块。
- 拒绝包含重复推理行的输出，这通常表明是幻觉或退化的生成。
- 检查思考部分中的策略块数量是否足够，并且包含足够的非注释行。
- 对注释密度（在推理和 Lean 代码中）应用阈值，以惩罚过于冗长或模板化的输出。
- 使用匹配分数（例如，交并比或子代码覆盖率）比较 `<think>` 块中描述的战术与最终 Lean 代码之间的语义对齐度。
- 惩罚不必要的长响应，鼓励模型更高效地使用 Token，同时仍能给出完整的回答。

只有通过所有这些检查的生成才被认为是格式良好的，才能获得奖励。这种结构化的过滤提高了训练稳定性，并鼓励清晰的推理。

## 错误纠正

为了使训练更具信息量，我们添加了一个**错误纠正机制**，让模型有机会修正自己失败的证明。

当一个 rollout 失败时（例如，由于 Lean 错误或不正确的证明），我们会：

1.  存储完整的提示词、响应和 Lean 反馈。
2.  创建一个**新的训练样本**，其中明确提示模型修改其先前的推理/代码。

这鼓励模型从失败信号中学习，因为训练期间会提供 Lean 反馈。

它还支持多轮交互链，其中来自 Lean 的反馈被注入为提示词的一部分，模型会因成功调试自己的输出而获得奖励。

由于多轮响应可能会变得很长，我们只允许一次错误修正轮次，并将错误消息限制在设定的 Token 数量内。

## 流程概述

论文《Understanding R1-Zero-Like Training: A Critical Perspective》声称 GRPO 中存在优化偏差，会导致人为地延长响应，特别是对于不正确的输出。

我们在实验中也注意到了这种行为，因此我们使用 DrGPO 进行优化。DrGRPO 通过使用全局常数进行归一化来聚合 Token 级别的损失，以消除长度偏差。

代码库中提供的配置文件适用于 8 个 GPU 的设置。

我们进行微调的模型是 **AI-MO/Kimina-Prover-Distill-1.7B**。该模型是 **Qwen/Qwen3-1.7B** 的微调版本，其冷启动数据由我们的 **AI-MO/Kimina-Prover-72B** 模型生成。

在每个训练步骤中，从训练数据集中获取 256 个样本。其中一半是错误纠正样本。我们为每个样本生成 8 个 rollout，因此总共是 2048 次生成。如果您使用超过一个节点，可以增加到 16 或 32 个 rollout。

我们每 5 个训练步骤评估一次模型，使用 verl 中的 best@8 指标进行快速验证。如果您使用超过一个节点，可以增加到 best@16 或 32。我们评估模型在错误纠正轮次之前和之后的性能。对于每个失败的响应，我们允许模型再进行一次尝试来修正其证明。

## 结果

经过几个训练步骤后，我们观察到性能持续提升。在本节中，我们将讨论在 8 个 H100 GPU 上训练 48 小时后的训练指标。

到第85步时，该流程将模型的准确率提升了4个百分点，在best@8指标上达到70%，经过纠错轮次后达到74%：

![image/png](/images/posts/73e6dec61869.png)

同时，我们观察到格式错误的数量在训练过程中持续减少，这表明模型正在学习生成结构有效的输出。

![image/png](/images/posts/acb728129c30.png)

最后，正如DeepSeek-R1风格训练设置所预期的那样，模型输出的平均Token长度随着训练而增加——这表明模型正在学习进行更长、更具结构化的推理追踪。

![image/png](/images/posts/62651f9c93b9.png)

训练结束后，我们使用pass@32指标（包含及不包含错误修正）对模型进行了评估。在MiniF2F数据集上，我们的17亿参数模型在pass@32指标上的性能提升了超过3%：

利用此训练流程，我们还微调了一个6亿参数的模型，其性能提升了超过2%。

## 结论

通过Kimina-Prover-RL，我们为训练Lean 4定理证明器提供了一套轻量而强大的强化学习流程。

通过结合结构化推理、格式奖励和错误修正机制，我们在6亿至17亿参数规模的开源模型中取得了最先进的结果。

除了模型之外，我们还发布了包含完整训练方案的Verl分支（位于recipe/kimina-prover-rl），以便社区能够复现我们的成果，或将该流程适配到自己的数据集和模型上。

我们希望本次发布能够为社区在形式化推理领域进行强化学习训练提供坚实基础，并推动Lean 4开源自动定理证明的边界。

---

> 本文由AI自动翻译，原文链接：[Kimina-Prover-RL](https://huggingface.co/blog/AI-MO/kimina-prover-rl)
> 
> 翻译时间：2026-02-18 04:35
