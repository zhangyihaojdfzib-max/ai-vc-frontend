---
title: Palmyra-mini系列开源模型发布：轻量强大，专精推理
title_original: 'Introducing the Palmyra-mini family: Powerful, lightweight, and ready
  to reason!'
date: '2025-09-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Writer/announcing-palmyra-mini
author: ''
summary: WRITER团队发布了Palmyra-mini系列三款开源模型，参数量为15亿至17亿，主打轻量高效推理。该系列包括基础模型palmyra-mini，以及两个采用思维链方法训练的专精变体：擅长复杂逻辑的thinking-a和精于数学方程与推理的thinking-b。模型提供了GGUF和MLX量化版本，便于部署。基准测试显示，各模型在Big
  Bench Hard、GSM8K、AMC23等任务上表现优异，分别在不同领域成为高效的生成式或推理任务解决方案。
categories:
- AI产品
tags:
- 开源模型
- 轻量模型
- 推理优化
- 思维链
- 基准测试
draft: false
translated_at: '2026-02-10T04:33:01.359648'
---

# 隆重推出Palmyra-mini系列：强大、轻量，即刻启航推理！

WRITER团队激动地宣布，在Palmyra-mini系列中发布三款新的开源模型。这些模型旨在实现强大、轻量，并在其参数量级（15亿至17亿）上表现出色，使其成为需要高效推理的广泛应用的理想选择。

- **palmyra-mini**：一个强大、轻量的非思维基础模型。
- **palmyra-mini-thinking-a**：一个专为复杂逻辑推理优化的变体。
- **palmyra-mini-thinking-b**：另一个擅长数学方程和推理的专精变体。

"思维"模型采用了思维链（CoT）方法进行训练，从而提升了其推理能力。我们非常期待看到社区利用这些新模型创造出什么！

为方便使用，我们也提供了GGUF和MLX量化版本：

- palmyra-mini-GGUF
- palmyra-mini-thinking-a-GGUF
- palmyra-mini-thinking-b-GGUF
- palmyra-mini-MLX-BF16
- palmyra-mini-thinking-a-MLX-BF16
- palmyra-mini-thinking-b-MLX-BF16

palmyra-mini-GGUF

palmyra-mini-thinking-a-GGUF

palmyra-mini-thinking-b-GGUF

palmyra-mini-MLX-BF16

palmyra-mini-thinking-a-MLX-BF16

palmyra-mini-thinking-b-MLX-BF16

## 基准测试亮点：

- **palmyra-mini**：我们改进的非推理基础模型，在Big Bench Hard (get-answer)(exact_match)上获得了52.6%的分数，使其成为适用于各种生成式任务的出色全能选手。
- **palmyra-mini-thinking-a**：此变体是应对复杂逻辑挑战的首选。通过思维链（CoT）方法训练，它在GSM8K (strict match)上取得了令人印象深刻的82.87%分数，展示了其强大的推理能力。相对于本次发布的其他模型，它在基准测试中拥有最高的总体平均分。
- **palmyra-mini-thinking-b**：此模型将解决问题的边界推向了新高度，在AMC23上获得了坚实的92.5%分数。当你需要一个能够通过"思考"应对高要求任务的模型时，这是一个绝佳选择。相对于本次发布的其他模型，它在AIME24、AIME25、GPQA、HMMT25、HLE、MMLU_PRO、MATH500、LCB等基准测试中拥有最高的平均分。

palmyra-mini: Our non-reasoning improved base model, delivering a score of 52.6% on Big Bench Hard (get-answer)(exact_match), making it a fantastic all-rounder for a wide variety of generative tasks.

palmyra-mini-thinking-a: This variant is your go-to for complex logical challenges. Trained with a Chain of Thought (CoT) approach, it achieves an impressive 82.87% on GSM8K (strict match), demonstrating its powerful reasoning capabilities. It has the highest overall average score on benchmarks relative to other models in the release.

palmyra-mini-thinking-b: Pushing the boundaries of problem-solving, this model scores a solid 92.5% on AMC23. It's a great choice when you need a model that can "think" its way through demanding tasks. This has the highest average benchmark scores in the benchmarks AIME24,AIME25, GPQA, HMMT25, HLE, MMLU_PRO,MATH500, LCB relative to the other models in the release.

## 基准测试说明：

我们同时发布了pass@1(avg-of-1)和pass@1(avg-of-64)的结果。
基准测试方法（采样参数：temperature 0.6, top_p 0.95）：
Pass@1(avg-of-1) 分数：

GSM8K 至 MBPP：使用 lm_eval 框架收集。
AIME24 至 HMMT25：使用 lighteval 框架收集。

Pass@1(avg-of-64) 分数：
使用 nemoskills 框架收集。

## 脚注：

由于所有基础模型均采用Qwen架构，推理应可在流行的推理框架上运行，例如 vLLM、SGLang、TRTLLM、TGI。

对于 palmyra-thinking-b，其基础模型是 https://huggingface.co/nvidia/OpenReasoning-Nemotron-1.5B。我们进行了RL微调，并观察到它能够提升性能。虽然强化学习提高了单次采样的准确率（pass@1），但它降低了采样多样性，导致与SFT基础模型相比，majority@64性能有所下降。这突显了准确性与多样性之间的权衡，我们相信对这些发现的透明化将激发关于模式崩溃、小模型性能及其他领域的进一步研究。

通过这项工作，我们试图探索小参数量模型所能达到的极限，并热切期待社区如何在保持性能质量的同时，继续推进推理效率。

---

> 本文由AI自动翻译，原文链接：[Introducing the Palmyra-mini family: Powerful, lightweight, and ready to reason!](https://huggingface.co/blog/Writer/announcing-palmyra-mini)
> 
> 翻译时间：2026-02-10 04:33
