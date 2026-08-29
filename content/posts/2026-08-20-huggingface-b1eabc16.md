---
title: Up to 3.2x Faster Inference with LFM2.5-DSpark
title_original: Up to 3.2x Faster Inference with LFM2.5-DSpark
date: '2026-08-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/LiquidAI/lfm25-dspark
author: ''
summary: '[翻译失败，原文如下]


  # Up to 3.2x Faster Inference with LFM2.5-DSpark


  Today, we releaseDSpark draft model checkpointsfor three models from our LFM2.5
  family:...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-29T08:48:39.096737'
---

[翻译失败，原文如下]

# Up to 3.2x Faster Inference with LFM2.5-DSpark

Today, we releaseDSpark draft model checkpointsfor three models from our LFM2.5 family: LFM2.5-1.2B-Instruct, LFM2.5-2.6B, and LFM2.5-8B-A1B. These add a speculative decoding path that trades a minimal memory increase for a large decoding speedup without changing output quality:

- Faster inference: up to 3.18 throughput improvement on a GPU and up to 2.87x on-device.
- Toward on-device agentic inference: cuts function-calling latency by 57% on average for LFM2.5-2.6B
- Day-one support for llama.cpp and SGLang: LFM-compatible DSpark integration is open-sourced upstream

## How does DSpark work

The decode phase in LLM inference is traditionally memory-bound. Most latency comes from streaming weights from DRAM into SRAM, not from intense computation. Speculative decoding addresses this by using a lightweight draft model to produce candidate tokens, then having the target model verify them all in a single forward pass, sharing the cost of loading the weights across all tokens we verify.

Over the years, multiple approaches of speculation have been proposed, with the most prominent beingEAGLE-3,DFlash, and, most recently,DSpark, which combines three components:

- DFlash-style parallel backboneconditioned on the target model’s context features, producing hidden states for all draft tokens in a single forward pass.
- A lightweight sequential head, modeled as a Markov chain between neighboring tokens, that adds inter-token dependency, raising the acceptance rate at later positions.
- A confidence-scheduled verifierthat predicts each token’s survival probability and prunes low-confidence suffixes when verification would cost more than it saves.

![DSpark](/images/posts/8d923a8ba06c.png)

## Training and Architecture

We follow the DSpark recipe with a larger and more diverse data mix covering SFT, chat, code, and function-calling data. Based on our ablations, the first versions of the draft models are simplified attention-only draft models, with 5 layers and a block of 9. For each draft model, we ran 15 epochs on the entire dataset and selected the epoch with the highest acceptance rate rather than the lowest loss.

The resulting draft models are relatively small, with each around ~300M parameters.

## Quality parity

Under greedy decoding, a draft token is only accepted if it matches the target model’s distribution. On rejection, the target model's own token takes its place. The emitted sequence is thereforeidentical to baseline greedyby construction, so benchmark accuracy (pass@1 or exact match) is unchanged.

## Inference Speed Up on CPU and GPU

Our DSpark draft models for LFM2.5 ship with day-one support forllama.cpp(implementationbuilds on top of the official codebase, which we run withexperimental metal kernels) and **SGLang (**implementationbuilds on the official SGLang implementation of DSpark).

We measure on-device throughput with llama.cpp and Metal on an M4 Max MacBook Pro using FP16 GGUF weights and up to 256 output tokens. We measure GPU throughput with SGLang on a single H100 80 GB in BF16. Both configurations use a DSpark block size of 9, a batch size of 1, and a temperature of 0. We evaluate them on five benchmark datasets.

All three drafter models deliver noticeable throughput improvements on both the large-scale accelerator (H100) and the edge deployment (M4 Max MacBook).

ForLFM2.5-2.6B,speedup on the MacBook is especially noticeable, as it pushes the interactivity level a user can enjoy far beyond the throughput offered by most proprietary cloud models (around ~140 tok/s, depending on the dataset).

Across various multi-tool scenarios, DSpark reduces the latency by 57% on average for LFM2.5-2.6B.

![bfcl_latency_mac](/images/posts/565111e03aab.png)

ForLFM2.5-1.2B-Instruct, we see much more variance in dataset acceptance rates, so speedup varies by as much as 52% depending on the underlying text distribution.

ForLFM2.5-8B-A1B, the acceptance rate increases compared to two dense models, yet on-device we get only an 18% improvement on average. This gap is due to the current MoE implementation in llama.cpp's Metal backend, and to the fact that verifying k tokens activates more experts and thus more weight traffic than a single decode step.

## How to use LFM2.5-DSpark

Running the DSpark draft models withSGLangrequires an SGLang build with DSpark support for LFM2 targets (PR #31041). Launch the target with the draft attached:

```shell
python -m sglang.launch_server \
  --model-path LiquidAI/LFM2.5-2.6B \
  --speculative-algorithm DSPARK \
  --speculative-draft-model-path LiquidAI/LFM2.5-2.6B-DSpark \
  --speculative-draft-attention-backend flashinfer \
  --disable-radix-cache --mem-fraction-static 0.75 --port 30000

```

Then query the OpenAI-compatible endpoint athttp://localhost:30000/v1. The block size is read from the draft'sconfig.json; the baseline is the same command without the three--speculative-*flags.

Running them withllama.cpprequires the respective llama.cpp build (PR#27383).

```shell
llama-server -m LFM2.5-2.6B-F16.gguf \
  -md LFM2.5-2.6B-DSpark-F16.gguf \
  --spec-type draft-dspark --spec-draft-n-max 10 --spec-draft-n-min 0 \
  -fa on -ngl 99

```

The block size is read from the sidecar metadata (n-max is clamped to it). Speculative decoding isexact: the target verifies every proposed token, so greedy output equals the target alone; per-responsetimingsreportdraft_n/draft_n_accepted.

## Get Started

The DSpark draft model checkpoints are available on Hugging Face as Safetensors and in GGUF format:

- Safetensors:LFM2.5-2.6B-DSpark,LFM2.5-1.2B-Instruct-DSpark, andLFM2.5-8B-A1B-DSpark
- GGUF:LFM2.5-2.6B-DSpark-GGUF,LFM2.5-1.2B-Instruct-DSpark-GGUF,LFM2.5-8B-A1B-DSpark-GGUF

We can’t wait to see what you build.

## Citation

For citations, please use the following reference or BibTeX:

Liquid AI, "LFM2.5-DSpark: Up to 3.2x Faster Inference from H100 to MacBook", Liquid AI Blog, Aug 2026.

```
@article{liquidAI2026dspark,
  author = {Liquid AI},
  title = {LFM2.5-DSpark: Up to 3.2x Faster Inference from H100 to MacBook},
  journal = {Liquid AI Blog},
  year = {2026},
  note = {www.liquid.ai/blog/lfm2.5-dspark},
}

```

---

> 本文由AI自动翻译，原文链接：[Up to 3.2x Faster Inference with LFM2.5-DSpark](https://huggingface.co/blog/LiquidAI/lfm25-dspark)
> 
> 翻译时间：2026-08-29 08:48
