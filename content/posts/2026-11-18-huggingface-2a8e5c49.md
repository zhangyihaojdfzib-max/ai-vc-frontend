---
title: '180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers'
title_original: '180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit
  with Transformers'
date: '2026-11-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/moe-expert-streaming
author: ''
summary: '[翻译失败，原文如下]


  # 180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers


  Streaming MoE experts directly from SSD gets within...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:39.138046'
---

[翻译失败，原文如下]

# 180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers

Streaming MoE experts directly from SSD gets within 6% of Strata on token generation.

I've been trying to rely less on online models and run bigger ones locally.
At home I have a PC with two RTX 4090s (let's call itOrthrus- the two-headed hound
of Greek mythology), and for work I have a MacBook M5 with 32G of unified memory.

Orthrus runs on Windows 11, because my kids play games all the time. I had a
dual boot with Ubuntu, but their games ended up taking most of the two
terabytes of disk.

I am also a huge fan of RMD (rooms moving development): one hour in the kitchen
sipping my coffee, two hours at my office desk, then the sofa. A fixed desktop
tower is not for me.

My first experiment was to runQwen 3.8 27Bwithllama.appon Orthrus and use
it from my laptop throughpi. That model does the coding tasks, an online
model like Opus does the orchestration, and the second RTX runs a FIM model for
auto-completion in Neovim.

When I talked about this on social networks, I got very strong feedback: useStratawithQwen3.8-Flash-Next.

## What is Strata?

Strata is an inference engine for MoE models like Qwen. Only the hot experts
stay in VRAM, the rest goes to RAM, or even to disk. Experts are 90%+ of a MoE
model's weights, so a 180B model like this one can run on a GPU with much less
memory. Like my RTX 4090!

It works on a laptop too, and I stumbled onthis blog postdoing
exactly that: Qwen3.8-Flash-Next on a 32 GB Mac M4, faster thanllama.cpp, at
13.5 tok/s.

That's too slow for how I use coding agents, but it's an interesting itch to
scratch. A whole range of MoE models don't fit in a MacBook's unified memory and
could run at a decent speed.

## How do other engines offload?

Before committing to Strata, I looked at what llama.cpp,vLLMandTransformersdo when a MoE model doesn't fit. Three questions matter: where do the experts
live, where does the expert matmul run, and what moves on each token?

llama.cppmaps the GGUF file withmmapand can keep the experts on the
CPU (--cpu-moe,--n-cpu-moe N,-ot "exps=CPU", or--fit onto pick for
you). Those experts are alsocomputedon the CPU, so only the activations
cross PCIe, never the weights. Great when the experts fit in RAM. When they
don't, the page cache thrashes. A GPU expert cache (--moe-cache-mib) just
landed, but it fragments the graph (2 splits per token become 50) and loses
~10% even when everything fits.

vLLM's--cpu-offload-gb Nputs N GB of weights in pinned RAM, and kernels
read them in place over PCIe. For a MoE layer, that's only the routed experts,
but nothing is cached: a hot expert crosses PCIe again on every token, and
there's no disk tier. By default the offloaded weights include dense layers,
read on every token;--cpu-offload-params expertskeeps it to the experts. That fits vLLM's big
batches, which touch almost every expert anyway, less so one user on one GPU.

Transformersoffloads throughAccelerate(device_map="auto",offload_folder), onemoduleat a time: hooks copy its weights to the GPU
beforeforward. For a MoE, that module is a layer's whole expert bank, so
every token copies every expert of every offloaded layer to use 8 or 10 of them.
No cache, no notion of routing. And on a Mac, CPU and GPU share the same memory,
so "offload to CPU" frees nothing.

I ran all of them onQwen3.6-35B-A3Bon one A10G (24 GB), with plenty of RAM,
and Harry Mellor reran vLLM with better flags:

Offloading only the experts doubles vLLM's speed, and FP8 helps on top (half
the bytes per expert, more of the model on the GPU). vLLM's other offload
backend, which copies groups of layers ahead of time, ran under 1 tok/s.

If the experts fit in RAM, llama.cpp is hard to beat. If they don't, you have to
stream only what the router picks, through a bounded cache, fast enough that the
SSD is the bottleneck and not Python, ideally reusing the model's fast expert
kernels. That's Qwen3.8-Flash-Next on a 32 GB Mac, and Transformers couldn't do
it out of the box.

## Making Qwen3.8-Flash-Next work on my 32 GB Mac with Transformers

Strata was already too slow for me on the laptop, and Transformers was not going
to beat it anytime soon. But the Accelerate path was so far off that I wanted to
try fixing offloading in Transformers itself, with the big model on my laptop as
the target, knowing it would probably stay too slow for how I work.

All of the code was built with AI: the Transformers PR, the model-specific
package and the Metal kernels. My part was choosing what to try, reading the
profiles, and deciding what to keep. Everything is in a Space:tarekziade/moe-expert-streaming.

### Start small

I started withOLMoE-1B-7B, which fits in memory, so I could compare every token
with vanilla Transformers.

First version: experts on disk, an LRU cache on the device, and a Python loop
running one expert at a time. With every expert already cached, it did 10.1
tok/s. Vanilla did ~32. The I/O was fine, my loop was not: vanilla usesgrouped_mm, which runs all the experts of a layer in one kernel.

The fix, and the key idea of this project, was to turn the cache into aslot
pool: one preallocated device tensor shared by all layers, plus a per-layer
table from expert id to slot. Remap the router's expert ids to slots and the
pool looks like a regular expert bank, sogrouped_mmruns on it as is. No
custom expert matmul needed. That got it to 34.6 tok/s, against 38.1 for
vanilla.

### experts_offload

I then turned the standalone loader into an option offrom_pretrained, inhuggingface/transformers#50717.
To try it, install Transformers from that PR:

```bash
pip install "git+https://github.com/huggingface/transformers.git@refs/pull/50717/head"

```

Then, moving from OLMoE to the real target, Qwen3.8-Flash-Next:

```python
path = snapshot_download("tarekziade/Qwen3.8-Flash-Next-expert-streaming")

model = AutoModelForCausalLM.from_pretrained(
    f"{path}/dense",
    dtype=torch.bfloat16,
    device_map={"": "mps", "experts.*": "disk"},
    quantization_config=MetalConfig(bits=8),
    experts_offload={
        "cache_bytes": 12 << 30,
        "quantized_experts": f"{path}/experts-q3",
    },
)

```

That repoholds the output of the project'sconversion script:
the dense weights, the experts quantized to 3 bits, and the n-gram table.

Experts mapped to"disk"go through the streaming path instead of Accelerate's
offload: the loader skips their tensors and MoE layers switch to an offloaded
implementation. Misses are read by 8 I/O threads, one contiguous read per
expert. The next two layers' routers run early on the current hidden states to
guess which experts to prefetch. Experts can be quantized offline so reads are
smaller. It works for MoE models with the standard experts layout.

The API is still being discussed with the Transformers maintainers. Thedevice_mapform came out of that, and quantized experts will probably go
through the per-layer quantization plan of#50245rather than
their own option.

### Running 121 GB of experts on a 32 GB Mac

Qwen3.8-Flash-Next has 48 layers of 512 experts (10 active), 121 GB in FP8.
Streaming them isn't enough: there's also a 51 GB n-gram embedding
table that needs its own disk path. So:

- experts quantized to 3 bits: 49 GB on disk, 12 GiB cached on the device
- dense layers in 8 bits (~5.4 GB, +0.2% perplexity vs BF16)
- the n-gram table stays on disk, rows read when needed

The conversion takes ~5 hours. After loading, it uses ~18 GiB, and a 6K prompt
peaks at 25.4 GiB. That's about the limit: I have to close the browser, or macOS
starts swapping.

The model-specific bits (the n-gram table, Metal kernels) live in a small
package,moe-expert-streaming,
on top of the PR. The first version ran at about 10 tok/s.

Then I installed Strata on the same M5, with the same prompts:

[翻译失败，原文如下]

Strata 0.1.60 used IQ3_XXS experts. Both ran greedy, with thinking, MTP and
speculative drafts off, and 1,024-token prefill chunks. The full setup and raw
results are on the Space'sdetails page.

I also triedvllm-metal, vLLM on
Apple GPUs through MLX, which recently got expert offloading. It streams the
routed experts from an MLX checkpoint through a bounded cache, like this
project. But it can't run Qwen3.8-Flash-Next on 32 GB, for the n-gram reason
above: only the experts are streamed, and the n-gram tables stay in memory.
That's 32 GB in the MLX checkpoints on the Hub, before the ~5 GB of dense layers and any expert cache.

## Closing the gap

Most of the time wasn't spent on experts. Here's what helped:

- Committing GPU work early.PyTorchon MPS holds small kernels until the
next sync, so the GPU idled while Python worked. Forcing a commit after each
block gave +10%. This should really be fixed in PyTorch.
- Metal kernelsfor the parts without a fast path on macOS: Gated DeltaNet
and the hyper-connections.
- Strata's own weights.I switched toStrata's GGUF weights, reducing dense
weight traffic from 5.4 GB to 3.9 GB per token and individual expert size from
2.15 MB to 1.75 MB, with a separate cache pool for each expert size.
- Prefill, we went from 68 to ~228 tok/s using bigger chunks, and reading the next layer's
experts while the current layer is being computed.
- Long documents: attention over the indexer's selected blocks only, and a
KV cache that grows in place instead of being copied at every token.
- Misses: Strata doesn't hide them, it waits like I do, and no cache policy
beat LRU by much. What helped was reading just one guessed expert per layer,
while the SSD would otherwise be idle.

Here's one MoE layer for one token, as it runs now:

These are the final results after these optimizations on the same M5 with the same prompts:

That's about 6% behind Strata on short decode, with slightly faster prefill,
all through Transformers.

Most of what's left is host round trips, ~10 ms per token. Waking up after a
sync is only ~1 ms of that. The rest is the GPU running dry while Python queues
the next layer. Strata queues the whole token's work up front, and the GPU waits
on a Metal shared event at each layer while the host reads experts. PyTorch
doesn't expose that. I tried to fake it with a kernel spinning on a flag the CPU
writes, and the GPU took anywhere from a second to never to see the write. The
real fix would be a native op on PyTorch's MPS stream, with a risk of hangs, so
I haven't built it.

## Conclusion

It runs at ~14 tok/s, close to Strata, and it's still too slow for how I use
coding agents. Orthrus keeps doing the real work.

Transformers didn't beat Strata, and closing the last ~6% would take deeper
changes in the stack, starting with control over that per-layer sync, which
PyTorch doesn't give you today. The interesting part is how it got that
close: streaming only the routed experts, a bounded cache thatgrouped_mmruns
on as is, and a few targeted Metal kernels. There's no C++ extension in the
project: just Python, Metal kernels compiled at runtime withtorch.mps.compile_shader, and prebuiltkernels from the Hub.
All the Metal kernels written for this experiment are nowpublished on the Hub,
and the project loads them from there.

Beating Strata was never the only goal, though. Building this was a great way
to learn how MoEs and LLMs work from a systems perspective: how sparse the
routing really is, how much an expert cache buys you, where memory bandwidth
goes per token, and how much time the host and the GPU spend waiting on each
other. Transformers makes all of that easy to poke at, one module at a time.

The generic expert streaming implementation is inhuggingface/transformers#50717,
and the benchmarks are in theSpace.
Feedback on the approach and the API is welcome.

Thanks to Pedro, Lysandre and Arthur for their excellent feedback, and to Harry
for helping test vLLM.

Finally, thanks to Niko Veit forStrata.
Strata set the bar for what's possible with expert streaming on consumer
hardware, and having those numbers to chase is what pushed this work as far as
it went.

---

> 本文由AI自动翻译，原文链接：[180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers](https://huggingface.co/blog/moe-expert-streaming)
> 
> 翻译时间：2026-11-19 09:43
