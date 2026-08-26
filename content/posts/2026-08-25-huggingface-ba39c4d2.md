---
title: 'Quantization-Aware Healing: a compressed, 4-bit model that outperforms its
  full-precision original'
title_original: 'Quantization-Aware Healing: a compressed, 4-bit model that outperforms
  its full-precision original'
date: '2026-08-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing
author: ''
summary: '[翻译失败，原文如下]


  # Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision
  original


  Making a large language model small...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T02:59:42.085024'
---

[翻译失败，原文如下]

# Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision original

Making a large language model smaller almost always comes with a cost. The now-standard recipe for efficient deployment is to compress the architecture first, cutting the parameter count by removing layers, heads, or neurons, and then quantize the remaining weights down to 4 bits to shrink memory and compute further. Both steps save a lot, but together they systematically degrade the capabilities people actually care about: reasoning, mathematical problem-solving, and code generation. Because of this, serious deployment pipelines add a recovery step, usually called healing, before the model goes into production. Recent open-weight releases such asgpt-oss, NVIDIA'sNemotronfamily, and our ownHypernova 60Ball rely on some version of this compress-then-heal approach.

Our latest paper,Quantization-Aware Healing: A Practical Recipe for Recovering Compressed, 4-Bit LLMs, asks a question that the field has mostly left open: once a model has already been through structural compression, not just quantization, how well does that recovery step actually work, and what is the right way to do it? We introduce Quantization-Aware Healing (QAH), and applied to a GPT-OSS 120B model compressed to 60B parameters and quantized to MXFP4, it produces a model that beats its own full-precision (bfloat16) version on 7 of 9 benchmarks. The 4-bit model ends up smaller, cheaper to run, and more accurate than the checkpoint it was quantized from. This inverts the usual relationship between a 4-bit model and the 16-bit model it came from.

## Why the usual healing methods fall short here

Most efficiency pipelines follow the same three steps: compress the architecture, quantize the compressed weights, then heal the damage. The difference between methods is entirely in that last step.

The dominant healing recipe is quantization-aware training (QAT). It inserts fake-quantization operators into the forward pass and keeps fine-tuning the model on a task loss, so the weights learn to tolerate the low-precision representation. In practice this means re-running an already expensive multi-stage post-training process, supervised fine-tuning, RLHF, agentic tuning, through a noisier, lower-precision forward pass. It is costly, and as our results show, it can also become unstable if training continues too long past its best point.

An alternative, quantization-aware distillation (QAD), avoids re-running that history. Instead of a task loss, it distills a frozen full-precision teacher directly into the quantized student through aKL-divergenceloss on the output logits. This works well when the only change is quantization, because a genuine full-precision version of the exact same model exists to act as teacher. But once a model has gone through structural compression, fewer layers, heads, or neurons, and not just fewer bits, that assumption breaks. There is no independently trained full-precision version of the smaller architecture. The only candidate teacher is the recovered bfloat16 checkpoint, which is itself a distilled approximation of the original model. Distilling from it anchors the quantized student to a degraded target and caps its accuracy at that recovered checkpoint's own ceiling.

So the question of how to heal a model that has been both structurally compressed and quantized was, until now, genuinely open.

## Our approach

QAH removes that ceiling with one change: it distills directly from the original, pre-compression model rather than from the recovered one. Teacher and student do not even share an architecture. The teacher is full-size and full-precision, the student is half the size and running in MXFP4. Because a teacher's output distribution is architecture-agnostic, nothing about the size or shape mismatch prevents the transfer. The student never sees hard labels, only the teacher's output distribution, matched through KL divergence on the logits.

This reframes what the quantization stage is doing. Under QAH it is no longer a lossy postprocessing step applied after healing is finished. It is a second, full pass of distillation against the original teacher, supervision that the bfloat16 checkpoint never received. The 4-bit student is not compensating for information lost to quantization; it is picking up information the earlier recovery stage did not have the time or data to transfer.

There is also a stability benefit that falls out of the loss itself. Because KL distillation ties the student to a fixed teacher distribution, once the student catches up there is no further pressure for it to drift. A cross-entropy task loss, by contrast, keeps pushing the student toward hard labels indefinitely. That difference turns out to matter for both accuracy and training stability, as the comparison below shows.

To make QAH work at long context, where the healing corpus includes documents up to 32k tokens, we reuse the memory-efficient chunked KL-divergence loss from our companion paper on efficient distillation. That loss computes the KL one slice of the sequence at a time and never materializes the full vocabulary-by-sequence grid, which is what makes 32k-token healing fit inside a fixed GPU memory budget. We covered the mechanics of that loss in aprevious post.

![QAH overview: after structural compression and quantization, capabilities drop sharply. QAH distills from the original pre-compression model as a frozen teacher, restoring performance without retracing the multi-stage post-training.](/images/posts/790a2afd64cf.png)

QAH overview. After structural compression and quantization, capabilities drop sharply. QAH distills from the original model, a frozen teacher whose logits are precomputed offline, rather than from the recovered checkpoint. Source: paper Figure 1.

## Results

We applied QAH to a GPT-OSS 120B model, compressed to 60B parameters and recovered in bfloat16, then re-quantized to MXFP4 under QAH. The natural comparison is against that same 60B model's bfloat16 checkpoint, the best full-precision version of this architecture that exists. The QAH model wins on 7 of the 9 benchmarks.

The two benchmarks where QAH trails, MMLU-Pro and SciCode, lose by less than a point and a half. Everywhere else the 4-bit model is ahead of its own 16-bit source, and the largest gains land on exactly the capabilities compression usually damages most: long-context reasoning (+7.4 on AA-LCR) and math (+5.6 on AIME 2025).

The comparison against the original 120B teacher is just as telling. Despite running at half the teacher's parameter count and roughly a quarter of its weight memory, the QAH model surpasses the full-size teacher on LiveCodeBench (66.5 vs. 66.0) and comes within 1.6 points on GPQA Diamond (67.4 vs. 69.0). The largest remaining gap against the teacher is on AA-LCR, an extreme long-context benchmark where the capacity lost to compression is intrinsically the hardest to recover.

![Benchmark performance of the three checkpoints: the original GPT-OSS-120B teacher (MXFP4), the compressed and recovered 60B model in bfloat16, and the same 60B model re-quantized to MXFP4 with QAH, across nine benchmarks.](/images/posts/2ff52b604e4d.png)

The 4-bit QAH model matches or beats its bfloat16 source on 7 of 9 benchmarks, and beats the full-size teacher on LiveCodeBench. Source: paper Figure 2.

### QAH against QAT, head to head

To isolate the effect of the loss function from everything else, we also compared QAH directly against QAT under matched conditions, quantizing a GPT-OSS 9B model to MXFP4 and tracking average performance across MMLU-Pro, LiveCodeBench, and GPQA Diamond as training progresses.

[翻译失败，原文如下]

Both methods reach a similar peak, 54.9 for QAH against 54.6 for QAT, so on best-case accuracy they are effectively tied. The difference is in how they get there and what happens afterwards. QAH reaches its peak in about 100 steps, roughly 7 times faster than QAT's 700, and then stays within about two points of that peak for the rest of training. QAT collapses sharply once past its peak, shedding nearly 19 points by step 1,200.

The practical consequence is a real deployment risk difference. A QAT checkpoint needs careful early stopping against a held-out signal to avoid shipping a model that has already started to degrade, whereas a sufficiently trained QAH checkpoint can be served safely because it simply does not drift. This is consistent with the mechanism: KL distillation against a frozen teacher gives the student no incentive to move once it matches the teacher, while a cross-entropy objective keeps pushing on hard labels and eventually erodes capabilities the model inherited from the original.

![Average performance of QAH and QAT as training progresses, quantizing GPT-OSS 9B to MXFP4. QAH peaks early and stays stable through 1,200 steps; QAT reaches a comparable peak much later, then collapses.](/images/posts/f8c6bdb65b1a.png)

QAH peaks at 54.9 in roughly 100 steps and holds; QAT reaches 54.6 only around step 700, then loses nearly 19 points by step 1,200. Source: paper Figure 3.

## What this changes in practice

The accuracy story comes paired with the efficiency story that motivated compression in the first place. At 4-bit precision the QAH model uses roughly 4 times less weight memory than the bfloat16 student, and at half the parameter count of the 120B teacher it roughly halves compute per token, which is what lets it run on substantially smaller hardware. For model families that ship in bfloat16 rather than 4-bit, the combined parameter and precision reduction would be closer to 8 times less compute per token.

The takeaway is that a compressed, 4-bit model does not have to be a lower-accuracy version of its full-precision counterpart. With this healing recipe it can be smaller, cheaper to serve, and more accurate at the same time, and it reaches that point in a fraction of the training a QAT recipe would need. Quantization stops being a tax you pay for efficiency and becomes an extra opportunity to teach the model.

This work is part of Multiverse Computing's ongoing research into making large models smaller and cheaper to run without giving up the capabilities that make them useful. It sits alongside our companion work on efficient distillation, which supplies the long-context training machinery QAH depends on.

Want the full technical details, including the healing pipeline, the chunked KL implementation for long-context healing, and the distributed-training findings? Read thefull paper, or get in touch with our team to talk about applying compression and healing to your own models.

---

> 本文由AI自动翻译，原文链接：[Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision original](https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing)
> 
> 翻译时间：2026-08-26 02:59
