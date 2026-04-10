---
title: Liger GRPO优化TRL训练器，内存降低40%并支持多GPU扩展
title_original: 🐯 Liger GRPO meets TRL
date: '2025-05-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/liger-grpo
author: ''
summary: 本文介绍了Liger对TRL中组相对策略优化（GRPO）训练器的增强优化。通过引入分块损失方法，在保持模型质量零损失的前提下，将训练期间的峰值内存使用量降低了40%。同时新增了对FSDP和PEFT的支持，使得在多GPU上扩展GRPO训练变得更加容易。文章还解释了GRPO相比传统PPO方法的优势，即依赖可验证奖励函数而非外部奖励模型，并提供了代码集成示例。
categories:
- AI基础设施
tags:
- GRPO
- TRL
- 模型训练优化
- 内存优化
- 强化学习
draft: false
translated_at: '2026-04-10T04:48:36.386609'
---

# 🐯 Liger GRPO 与 TRL 的融合

TL;DR：Liger 通过将内存使用量降低 40% 且模型质量零损失，极大地增强了 TRL 的组相对策略优化（GRPO）训练器。我们还增加了对 FSDP 和 PEFT 的支持，使得在多 GPU 上扩展 GRPO 比以往任何时候都更容易。

## 动机

使用强化学习（RL）对大语言模型进行微调，是模型训练生命周期中的关键一步，旨在引导模型产生比典型监督微调所能实现的更复杂的期望行为。传统上，RL 被应用于使用近端策略优化（PPO）算法来优化大语言模型（LLM）。这种方法通常与基于人类反馈的强化学习（RLHF）相关联，它利用一个单独训练好的奖励模型来指导主模型的微调。

然而，使用 PPO 的 RLHF 是一种非常消耗资源的方法——PPO 需要在内存中加载多个模型（策略模型、价值模型、奖励模型和参考模型），并且还需要对奖励模型和基础模型进行多次迭代微调才能达到预期效果。RLHF 的成功还取决于奖励模型有效区分模型期望行为与非期望行为的能力。

组相对策略优化（GRPO）最近随着 DeepSeek 的 R1 模型而广受欢迎。GRPO 摒弃了 RLHF 中使用的预训练奖励模型和价值模型，转而依赖**可验证的奖励函数**，这些函数可以以闭式方式检查模型输出的正确性，而无需外部奖励模型。在那些易于验证的领域（例如教模型进行推理，以及在数学和编码任务上表现良好），使用 GRPO 替代 PPO 进行微调已经带来了巨大的改进。

下图展示了 GRPO 与 PPO 的训练流程对比（参考：DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models 的图 4）：

![PPO-vs-GRPO](/images/posts/aeab19401b31.png)

尽管如此，RL 训练仍然会消耗大量的 GPU 内存，因此这里仍有很大的优化空间。在这篇博客文章中，我们将讨论我们最近添加到 TRL 中的一个优化，该优化在 GRPO 训练期间将峰值内存使用量降低了 40%，同时我们还将深入探讨如何在不损失性能或正确性的情况下将 GRPO 扩展到多个 GPU 和节点。

## Liger Kernel 如何为 GRPO 大幅降低内存

我们将 Liger 分块损失方法扩展到了 GRPO 损失，这使我们无需在每个训练步骤中在内存中存储完整的逻辑值。逻辑值的计算涉及模型的输出头，是导致峰值内存使用量的重要因素，尤其是在处理大词汇表、长序列长度或大批量大小时。我们通过将 `lm_head` 的输入在批次维度上进行分块，并一次处理一个分块的前向传递来解决这个问题。

但是，如果你只是以简单直接的方式实现它，实际上并不能降低峰值内存，因为在反向传播过程中你仍然需要将所有逻辑值保存在 GPU 内存中。为了解决这个问题，我们在前向传递过程中计算每个损失分块的梯度（相对于输入分块和 `lm_head` 权重），然后在处理每个分块时累积这些梯度。

以下是该优化的可视化（参考：Byron Hsu）：

![liger-chunked-loss](/images/posts/af9712a819f6.gif)

## 与 TRL 的即插即用集成

我们最近在 PR#3184 中将 Liger GRPO 与 TRL 集成，所以现在你只需在 `GRPOConfig` 中将 `use_liger_loss` 设置为 `True` 即可使用 Liger GRPO 损失，并享受内存节省！

请注意：这些功能尚未包含在最新的 TRL 版本中，因此目前你需要从源代码安装 TRL：

```bash
pip install "trl[liger] @ git+https://github.com/huggingface/trl.git"
```

然后你可以像这样使用它：

```python
from trl import GRPOConfig, GRPOTrainer
from datasets import load_dataset


train_dataset = load_dataset("trl-lib/tldr", split="train")
training_args = GRPOConfig(output_dir="Qwen3-0.6B-GRPO", use_liger_loss=True)

def reward_len(completions, **kwargs):
    return [-abs(20 - len(completion)) for completion in completions]

trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B-Instruct",
    reward_funcs=reward_len,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()
```

## 基准测试

我们运行了一系列使用和不使用 Liger GRPO 损失的 GRPO 实验，以比较两者的差异。对于策略模型，我们使用了 `Qwen3-0.6B`，并尝试了不同的批量大小。所有实验均在 `gsm8k` 数据集上使用其奖励函数运行。

以下是 FP32 和 BF16 训练下峰值内存使用量与批量大小的关系图。正如预期的那样，由于我们沿批次维度进行分块，批量越大，内存节省效果越好。因此，当批量大小增加时，与常规（非 Liger）版本相比，Liger 分块损失最终使用的内存要少得多，最多可减少 40%。

快速说明：目前，我们仅支持 FP32，但我们正在努力为 TRL 中的 Liger GRPO 开源 BF16 支持。此处显示的 BF16 结果来自我们一直在测试的内部补丁。

![Mem-vs-batch-size-fp32](/images/posts/2e24f52b45a5.png)

![Mem-vs-batch-size-bf16](/images/posts/550cf2de4973.png)

我们还展示了 Liger 损失是准确有效的。从图中可以看出，训练步骤中的奖励与使用标准 TRL 实现所看到的结果基本保持一致。

![reward-vs-step](/images/posts/9c6a9e115a4b.png)

## 通过 FSDP 和 PEFT 进一步扩展

我们分别在 PR#3260 和 PR#3355 中为 Liger GRPO 损失增加了 FSDP 和 PEFT 支持，使用户能够轻松地在多个 GPU 或节点上扩展实验。PEFT 技术（如 LoRA 和 QLoRA）通过仅调整原始模型之上较小适配器权重的权重来减少可训练参数的数量，由于无需将整个模型的梯度、激活和优化器状态保存在内存中，从而显著降低了内存压力。此外，在 GRPO 中使用 PEFT 可以避免在训练期间加载单独的参考模型，因为我们可以通过简单地禁用 LoRA 适配器来获得原始的、未经修改的模型。

在这里，我们展示了一个使用 FSDP 和 PEFT 的多 GPU GRPO 训练图，其中我们比较了在不同 Qwen3 模型大小下，使用和不使用 Liger 损失时可能的最大训练批量大小。我们发现，使用 Liger 后，我们能够将批量大小提高约 1.5 到 1.8 倍！

![peft-batch-size-vs-model-size](/images/posts/61fd3de71009.png)

## 通过 vLLM 进一步扩展

为了加速训练期间的文本生成，Liger 损失可以有效地与 TRL 集成的 vLLM 服务器结合使用。这能以最小的开销显著加快 rollout 数据的收集，并提供无缝的集成体验。

以下是设置方法：

1.  启动 vLLM 服务器：首先，启动 vLLM 服务器。该服务器将处理来自训练脚本的生成请求。打开终端并运行：`CUDA_VISIBLE_DEVICES=1 trl vllm-serve --model "Qwen/Qwen3-0.6B"` 注意：我们分配 `CUDA_VISIBLE_DEVICES=1` 在特定 GPU（本例中为 GPU 1）上运行 vLLM 服务器，为训练留出其他 GPU。
2.  配置并运行训练脚本：接下来，修改你的训练脚本以使用 vLLM 服务器。关键更改是在 `GRPOConfig` 中设置 `use_vllm=True`。`from trl import GRPOConfig, GRPOTrainer from datasets import load_dataset def reward_len(completions, **kwargs): return [-abs(20 - len(completion)) for completion in completions]`

dataset = load_dataset("trl-lib/tldr", split="train[:1%]")
training_args = GRPOConfig(
    output_dir="Qwen3-0.6B-GRPO",
    use_liger_loss=True,
    use_vllm=True,logging_steps=10)
trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",reward_funcs=reward_len,
    args=training_args,
    train_dataset=dataset,
)
trainer.train()
3. 启动训练：最后，使用 `accelerate launch`（或者如果不使用 `Accelerate` 进行多 GPU/分布式训练，则使用 `python`）运行你的训练脚本。如果你的 vLLM 服务器占用了一个 GPU，请确保为训练指定另一个 GPU。`CUDA_VISIBLE_DEVICES=0 accelerate launch train.py`（假设你的脚本名为 `train.py` 并且你想在 GPU 0 上运行训练）。

启动 vLLM 服务器：首先，启动 vLLM 服务器。该服务器将处理来自训练脚本的生成请求。打开一个终端并运行：

```bash
CUDA_VISIBLE_DEVICES=1 trl vllm-serve --model "Qwen/Qwen3-0.6B"

```

注意：我们指定 `CUDA_VISIBLE_DEVICES=1` 在特定的 GPU（本例中为 GPU 1）上运行 vLLM 服务器，为训练留出其他 GPU。

配置并运行你的训练脚本：接下来，修改你的训练脚本以使用 vLLM 服务器。关键更改是在你的 `GRPOConfig` 中设置 `use_vllm=True`。

```python
from trl import GRPOConfig, GRPOTrainer
from datasets import load_dataset


def reward_len(completions, **kwargs):
    return [-abs(20 - len(completion)) for completion in completions]

dataset = load_dataset("trl-lib/tldr", split="train[:1%]")
training_args = GRPOConfig(
    output_dir="Qwen3-0.6B-GRPO",
    use_liger_loss=True,
    use_vllm=True,
    logging_steps=10
)
trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",
    reward_funcs=reward_len,
    args=training_args,
    train_dataset=dataset,
)
trainer.train()

```

启动训练：最后，使用 `accelerate launch`（或者如果不使用 `Accelerate` 进行多 GPU/分布式训练，则使用 `python`）运行你的训练脚本。如果你的 vLLM 服务器占用了一个 GPU，请确保为训练指定另一个 GPU。

```bash
CUDA_VISIBLE_DEVICES=0 accelerate launch train.py

```

（假设你的脚本名为 `train.py` 并且你想在 GPU 0 上运行训练）。

遵循这些步骤，你可以在使用 Liger Loss 进行 GRPO 训练时，利用 vLLM 实现更快的生成周转。

## 结论

随着 Liger-GRPO 集成到 TRL 中，以及 FSDP 和 PEFT 的支持，使用 GRPO 微调语言模型现在比以往任何时候都更加内存高效和可扩展。我们鼓励社区尝试这些新功能并分享反馈，以帮助我们进一步改进针对 LLM（大语言模型）的 RL（强化学习）训练。

---

> 本文由AI自动翻译，原文链接：[🐯 Liger GRPO meets TRL](https://huggingface.co/blog/liger-grpo)
> 
> 翻译时间：2026-04-10 04:48
