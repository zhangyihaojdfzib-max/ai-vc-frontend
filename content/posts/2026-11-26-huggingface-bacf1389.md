---
title: Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon
title_original: Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon
date: '2026-11-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ggml-org/llamacpp-amd-bench
author: ''
summary: '[翻译失败，原文如下]


  # Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon


  Thellama.cpp × AMD Benchmarkdashboard is available on Hugging F...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-27T10:42:59.230084'
---

[翻译失败，原文如下]

# Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon

Thellama.cpp × AMD Benchmarkdashboard is available on Hugging Face. It lets you track prompt processing and text generation performance across llama.cpp builds, models, and quantizations, so you can explore how local inference performs on AMD Ryzen and Radeon hardware.

Local inference performance changes as models, kernels, and builds evolve. We want those changes to be easy to inspect for any AMD developer: pick a hardware, a model and a build, compare quantizations, and follow performance over time. The benchmark workflow and underlying results are public, so you can also inspect how we benchmark inference performance.

## Quick start

You can chooseHardware,Model, andllama.cpp buildin the Configuration sidebar. The current hardware choices are Radeon 8060S (gfx1151) and Radeon AI Pro R9700S (gfx1201).

1. In theOverviewtab, compare quantizations for one hardware, model, and build. The two charts show PP512 (512 input tokens, no generation) and TG128 (128 generated tokens), both starting at context depth zero.
2. In theBuild historytab, track PP512 and TG128 across all recorded builds for the selected hardware, model, and quantization.
3. In theContextscalingtab, see how token-generation throughput changes as the existing context grows, for the selected build, hardware, model, and quantization.

## What the numbers mean

The dashboard shows two separate tests, both measured in tokens per second:

Both tests start at context depth zero (n_depth=0). PP512 measures processing 512 input tokens without generation; TG128 measures generating 128 tokens without a pre-existing context. The plotted value is the mean throughput (avg_ts). These are useful reference workloads, while the Context scaling tab lets you explore token generation throughput as the context grows.

## How we run the benchmarks

We benchmark the prebuilt binaries distributed throughllama-install.sh, the build and installation project behindllama.app. The publicgfx1151andgfx1201workflows are scheduled weekly and run the standard benchmarks using thellama-bench toolwith Flash Attention on and off, with 10 repetitions per configuration.

The model set evolves and currently includes Inkling 2 Mini, Qwen, Gemma, gpt-oss, and LFM models, covering both dense and mixture-of-experts architectures. Available GGUF formats includeQ4_K_M,Q8_0, other quantizations, and higher-precision formats such asBF16andF16.

## Inspect and reuse the results

The explorer reads directly from the publicggml-org/install.sh-benches-data Storage Bucketon Hugging Face. Thedata sourcelink beside the chart title opens the folder for the selected build, hardware, and model.

Standard results use<build>/<hardware>/<model>/<quant>.jsonl. Workload sweeps use the same folder<quant>-tg.jsonlfilename.

Use them to investigate a result, make your own charts, or compare with a local run.

## Join the conversation

Thanks to the AMD team for providing test infrastructure and helping validate the setup! Try thedashboard, inspect thedata, and let us know which models and workloads you would like to see next.

---

> 本文由AI自动翻译，原文链接：[Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon](https://huggingface.co/blog/ggml-org/llamacpp-amd-bench)
> 
> 翻译时间：2026-11-27 10:42
