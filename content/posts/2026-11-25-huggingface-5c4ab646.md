---
title: Hill-climbing Inkling 2 Mini inference on one RTX PRO 6000
title_original: Hill-climbing Inkling 2 Mini inference on one RTX PRO 6000
date: '2026-11-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/inkling-2-mini-inference-hillclimb
author: ''
summary: '[翻译失败，原文如下]


  # Hill-climbing Inkling 2 Mini inference on one RTX PRO 6000


  Inkling 2 Minicame out last week and sets a new state of the art for local ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-27T10:43:00.187750'
---

[翻译失败，原文如下]

# Hill-climbing Inkling 2 Mini inference on one RTX PRO 6000

Inkling 2 Minicame out last week and sets a new state of the art for local AI and smaller open-source models. With ~26B total parameters (3B active per token), multimodal inputs, and a 1M-token context window, it leads its weight class on theArtificial Analysis Intelligence Index v5and across 32 of 48 benchmarks against models like Gemma 4 31B and Qwen3.8-27B, making it a strong open option for coding, tool use, and reasoning on modest hardware. We wrote an extensive blog post on how you can use it within the Hugging Face ecosystemhere.

One of the interesting aspects of Inkling 2 Mini that might explain its great performance is its unusual architecture. Inkling 2 Mini is a loopedMixture-of-Experts (MoE)model with 24 physical layers where the middle 12 layers run three times, so every token passes through 48 layers. The checkpoint ships in mixed NVFP4 and MXFP8 and bundles a DSpark drafter for speculative decoding. Both vLLM and SGLang, the go-to frameworks for LLM inference, support it on nightly builds, though the published serving recipes target NVIDIA B200 and GB300 GPUs (sm100), leaving outsm120cards like the NVIDIA RTX PRO 6000 where kernel compatibility can differ.

We wanted to see how fast we could serve it on a single NVIDIA RTX PRO 6000 96 GB, the GPU behind annvidia-rtx-pro-6000Inference Endpoint. Rather than tuning flags by hand, we gave a coding agent theinference-optimisationskill, thehfCLI, and access toHugging Face Jobs, and let it run experiments for an afternoon.

Across 46 valid benchmark runs, single-user decode went from136 to 190.6 tok/s (+40%)(ahead of the167.7 tok/s community SGLang + DSpark benchmark on LocalMaxxingfor the same GPU) and 8-user aggregate throughput went from~570 to 716 tok/s (+26%)using vLLM nightly with DSpark speculative decoding. Greedy outputs are byte-identical with and without speculation, long-context needle retrieval passes 3/3 up to 250K tokens, and the winning config is now running as an Inference Endpoint from a pinned image digest. All logs, scripts, and raw measurements are inNielsRogge/inkling-2-mini-hillclimb.

## The setup

Theinference-optimisationskill gives an agent a fixed experimental protocol and a small, engine-agnostic benchmark script (bench.py):

1. Measure the hardware and estimate theoretical ceilings before tuning.
2. Change one variable at a time and bracket every candidate between two control runs (control → candidate → control). Keep a change only if it beats both controls without regressing other metrics.
3. Log every run inPLAN.md, including regressions and dead ends.
4. Pass long-context, concurrency, and greedy-equivalence checks before declaring a winner.

bench.pymeasures single-user decode, aggregate decode at concurrency N, cold prefill at several lengths, and TTFT, using token counts directly from the server's usage response. All runs used a fixed panel of six prompts (code, an explanation, a story, a comparison table, a bash script, and a history summary) at temperature 1.0 (the model's default), thinking on, 512 output tokens, and 12 repetitions whenever speculative decoding was enabled.

The skill was written for a local GPU, so we adapted it to Hugging Face infrastructure:

- HF Jobsfor compute. Thertx-pro-6000Job flavor uses the same GPU as thenvidia-rtx-pro-6000Inference Endpoint ($2.75/h for both), so Job numbers transfer directly. A ~150-line driver (jobs/driver.py) takes a list of server configs, starts each one, runs an unmeasured warmup, callsbench.pyunmodified, shuts the server down, and prints one ledger line per run. Because Jobs run on separate machines, the agent swept SGLang (lmsysorg/sglang:inkling-2-mini) and vLLM nightly (vllm/vllm-openai:nightly) in parallel.
- CPU Jobs for reading engine source.When a flag was undocumented, the agent ran a cheapcpu-upgradeJob to grep the installed Python package inside the container. That is how it found SGLang'sSGLANG_OPT_*environment variables and vLLM'sspeculative-configfields.
- Inference Endpointsfor deployment, created viahf endpoints deployusing the exact image digest and flags that passed verification.

The baseline was our existing org endpoint config: SGLang with--attention-backend fa4and no speculative decoding.

## Results

![Single-user decode speed of Inkling 2 Mini on one RTX PRO 6000 for four configurations](/images/posts/1cb90f45d906.png)

Single-user decode speed (median of 12 requests). vLLM + DSpark reaches ~95% of the memory-bandwidth ceiling at its measured acceptance rate.

¹ SGLang's RTX PRO 6000 DSpark recipe caps--max-running-requestsat 4. Raising it to 8 reached 660 tok/s, still behind vLLM.
² Includes ~160 ms of client-to-endpoint network round trip.

All of the speedup comes from switching to vLLM nightly (+15% over SGLang without speculation, 136 → 157 tok/s), enabling DSpark with 7 drafts and probabilistic draft sampling (+21% on top, 157 → 190.6 tok/s across four runs: 189.3, 190.4, 191.1, and 190.7), and adding two memory flags so vLLM's DSpark setup actually starts on 96 GB:

```bash
vllm serve thinkingmachines/Inkling-2-Mini \
  --tool-call-parser inkling \
  --enable-auto-tool-choice \
  --reasoning-parser inkling \
  --max-model-len 262144 \
  --gpu-memory-utilization 0.85 \
  --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"probabilistic"}'

```

Bothnum_speculative_tokens: 7anddraft_sample_method: "probabilistic"were validated directly: shorter draft counts (such as 5) are rejected at startup because both engines enforce the checkpoint's fixed block size, and switching togreedydraft sampling dropped vLLM decode speed by 11% at temperature 1.0 (seeWhat didn't work).

### Why it stops around 190 tok/s

Before tuning, the agent probed the RTX PRO 6000 inside a Job (1,469 GB/scopy bandwidth,416 TFLOPSBF16,792 TFLOPSFP8) and read tensor sizes from the safetensors header. Because every token makes 48 layer visits, plain decode re-reads ~2.7 GB of attention and dense weights, ~2 GB of routed experts (8 of 128 per layer), and ~0.9 GB for the LM head. At 1,469 GB/s, that gives a single-user bandwidth ceiling of~256 tok/s. Without speculation, vLLM at 157 tok/s hits 61% of that ceiling, mostly limited by kernel launch latency across 48 visits.

Speculative decoding changes the memory math on an MoE. Verifying 8 positions together activates the union of their routed experts, reading roughly 40% of each layer's experts instead of 6%. At our measured acceptance of ~2.3 tokens per step at temperature 1.0 (per-position acceptance drops from 0.6 on the first draft to 0.33 and 0.19), the bandwidth ceiling falls to~201 tok/s. At 190.6 tok/s, vLLM + DSpark is already at~95% of hardware bandwidth, so further flag tuning has almost nowhere left to go. Moving past 190 tok/s would take a drafter with higher acceptance at temperature 1.0 or a verification path that touches fewer experts per layer.

## What didn't work

Most candidate flags were unsupported, noisy, or slower:

We also skippedrejection_sample_method: "fly"and"synthetic"on purpose because they alter the output distribution, and we wanted a strictly lossless speedup.

### SGLang

## Benchmarking gotchas

A few measurement issues caught us along the way:

[翻译失败，原文如下]

- Triton JIT during timed prefill.vLLM's first 4K prefill came back at 202 tok/s instead of 20K because Triton was compiling kernels during the timed request. Running an unmeasured warmup across prompt lengths and concurrency fixed 4K prefill, though the first run in each Job still under-reported 32K prefill due to last-chunk shape differences (flagged in the ledger).
- Orphaned servers holding GPU memory.The initial driver stopped servers via a PID saved fromsetsid … &, which is not guaranteed to match the process group ID. The previous server stayed alive on port 8000, broke the next launch, and turned into a zombie that still passedkill -0. Managing the process withsubprocess.Popen(start_new_session=True)and waiting until both GPU memory and port 8000 are free fixed it.
- Hidden OOM errors in vLLM logs.vLLM + DSpark twice died with"Engine core initialization failed"at the end of the log while the real causes sat 200 lines up. First, the default 1M-token KV cache needed 52.6 GiB with only 48.1 GiB free alongside the drafter (--max-model-len 262144fixed this). Next, because vLLM v0.34.0 raised the default--gpu-memory-utilizationfrom0.92to1.0, the KV cache claimed the remaining VRAM and OOMed the drafter's 5 GiB allocation (--gpu-memory-utilization 0.85fixed this). The driver now prints every error line from the server log instead of just the tail.
- Engine variance.Across identical runs with speculation, vLLM stayed within 0.4% while SGLang swung by ±4.5%. That was wide enough to makeSGLANG_ENABLE_NV_MEGA_RUNTIME_OPTIMIZATION=1look like a +4% win on its first run before repeat controls ruled it out.

## Verification and deployment

Before deploying, we pinned the exact vLLM nightly digest (vllm/vllm-openai@sha256:eaa63fd6…, build0.34.0rc1.dev1235+gf2f9edcac) and ran the acceptance gates inside a Job:

Once those passed, we deployed the endpoint with a singlehf endpoints deploycommand, pinning both the image digest and model revision (authenticated access, scale-to-zero after 60 idle minutes):

```bash
hf endpoints deploy inkling2mini-tuned-dspark --namespace <your-org> \
  --repo thinkingmachines/Inkling-2-Mini --revision 7a67ae2314b44ef05c87fd1d4d311c58aaeb18f6 \
  --framework custom --custom-image "vllm/vllm-openai@sha256:eaa63fd6ee3aac77f3158e80ed79ec425db3a53f7cd666bf1954e96abfaf19a7" \
  --health-route /health --port 8000 \
  --vendor aws --region us-east-2 --accelerator gpu --instance-type nvidia-rtx-pro-6000 --instance-size x1 \
  --min-replica 0 --max-replica 1 --scale-to-zero-timeout 60 --type authenticated \
  --container-command "vllm serve" \
  --container-args "/repository --served-model-name thinkingmachines/Inkling-2-Mini --host 0.0.0.0 --port 8000 --tool-call-parser inkling --enable-auto-tool-choice --reasoning-parser inkling --max-model-len 262144 --gpu-memory-utilization 0.85 --speculative-config '{\"method\":\"dspark\",\"num_speculative_tokens\":7,\"draft_sample_method\":\"probabilistic\"}'"

```

Runningbench.pyagainst the live endpoint gave 194.9 tok/s single-user, matching the Job runs once network latency is accounted for.

Everything from this run (PLAN.md,THEORY.md,jobs/driver.py,submit.sh,deploy.sh, and the rawledger-*.jsonlfiles) is inNielsRogge/inkling-2-mini-hillclimb. To reuse the loop on another model, put your candidate and control server commands into aconfigs/plan-*.jsonfile and submit it to whichever HF Jobs GPU flavor matches your target endpoint.

---

> 本文由AI自动翻译，原文链接：[Hill-climbing Inkling 2 Mini inference on one RTX PRO 6000](https://huggingface.co/blog/inkling-2-mini-inference-hillclimb)
> 
> 翻译时间：2026-11-27 10:43
