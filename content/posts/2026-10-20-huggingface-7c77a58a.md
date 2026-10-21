---
title: 'Hugging Face ❤️ TorchTPU: TPUs, Natively'
title_original: 'Hugging Face ❤️ TorchTPU: TPUs, Natively'
date: '2026-10-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-torchtpu
author: ''
summary: '[翻译失败，原文如下]


  # Hugging Face ❤️ TorchTPU: TPUs, Natively


  If you ever tried to run PyTorch on a TPU, you probably ported your code totorch_xla,
  or you ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:00.798097'
---

[翻译失败，原文如下]

# Hugging Face ❤️ TorchTPU: TPUs, Natively

If you ever tried to run PyTorch on a TPU, you probably ported your code totorch_xla, or you ended up having to learn JAX. WithTorchTPU, a native PyTorch backend, TPU is now just another device. It opens up native support of TPU in the Hugging Face ecosystem. Transformers, Diffusers and Kernels run natively on TPU. Pick a model from the Hub, send it to"tpu", and you're done.

## Wait, what's a TPU? 🤔

TPU stands forTensor Processing Unit. TPUs are Google's own AI accelerators. They are chips built for one job: the matrix math that neural networks spend most of their time on. Google has been designing them for about ten years, and uses them to train and serve its own models, including Gemini.

TPUs are available onGoogle Cloud, from a single chip up to pods of thousands of chips. They shine when you need a lot of compute, for training or for serving at scale.

The catch has always been software. The TPU stack grew up around TensorFlow and JAX, and PyTorch users had to work harder to get in.

## The old way

Until now, running PyTorch on TPUs meant going through PyTorch/XLA (torch_xla). It worked, but it had its quirks. Tensors were lazy (the tensors, not you), so your code didn't always run when you thought it did. Small changes could trigger graph recompilations, and debugging was hard to reason about.

To make life easier, we built Optimum TPU. It gave Hugging Face models inference and training support on TPUs. Now that TorchTPU brings native support, Optimum TPU is not required anymore to run Hugging Face models with Transformers and Diffusers.

## Enter TorchTPU 🚀

TorchTPUadds TPU as a new backend to PyTorch. You write regular PyTorch code. It comes with Pallas kernels tuned for TPUs, support for distributed training, and atorch.compileintegration for when you want more speed. Installing it on a TPU VM takes one command:

```shell
pip install torch-tpu --extra-index-url https://download.pytorch.org/whl/cpu

```

The extra index gives you the CPU build oftorch. Without it, pip pulls the much bigger CUDA build, which you don't need on a TPU.

## Your favourite libraries, now on TPU

### Transformers

Transformers v5 was built around one idea: be the source of truth for model definitions, so they can run anywhere. "Anywhere" now includes TPUs. To load a model on a TPU, passdevice_map="tpu". That's it.

```py
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen3.5-9B"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="tpu", 
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
inputs = tokenizer("The future of AI is", return_tensors="pt").to("tpu")
out = model.generate(**inputs, max_new_tokens=64)
print(tokenizer.decode(out[0], skip_special_tokens=True))

```

The model runs in eager mode by default. You can also usetorch.compilefor better performance, or run it in a distributed setup.

### Images? Videos? Diffusers paints them on TPUs 🎨

TPU is now a first-class device in Diffusers. For prototyping or debugging, eager mode only needspipe.to("tpu"). For deployment, compiled mode adds onecompilecall. Your pipelines and code stay the same, and there's no TPU fork to maintain.

```py
import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-medium", dtype=torch.bfloat16
)
pipe.to("tpu")  

pipe.transformer.compile(backend="tpu", fullgraph=True, dynamic=False)

image = pipe("a corgi astronaut planting a flag on a pizza moon").images[0]

```

The first call compiles, and every call after that with the same image size reuses the graph.

Models too big for one chip? Pass aTensorParallelConfigtofrom_pretrainedand the transformer is sharded across chips as it loads, so the full model never has to fit in one place. Many popular pipelines support it out of the box, and the ones that don't are just atp_planaway. TheDiffusers TPU guidehas the full recipe.

Here are some examples run on a Cloud TPU v6e-4:

TP=4 (each model split across four chips) · bf16 · batch 1

![A capybara wearing a wizard hat, reading a book by candlelight, oil painting](/images/posts/38d10b6bf99c.jpg)

![Neon shop sign reading QWEN IMAGE 2.1](/images/posts/64d7c0433471.jpg)

### Kernels

TheKernels Hubhas ready-to-use TPU kernels. Load one with the Kernels library and give your model a speed boost.

TPU kernels are written inPallas, which gives you low-level control over the hardware. You can also bring in kernels from theTokamaxlibrary. Here is a ragged-dot kernel from Tokamax plugged into a Mixture-of-Experts model:

```py
from kernels import get_kernel
from transformers import AutoModelForCausalLM
from transformers.integrations.moe import ALL_EXPERTS_FUNCTIONS

repo_id = "tengomucho/ragged-dot-tpu"
kernel = get_kernel(repo_id, version=1, trust_remote_code=[repo_id])
ALL_EXPERTS_FUNCTIONS.register("tokamax_ragged_dot", kernel.experts_forward)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-30B-A3B-Instruct-2507",
    experts_implementation="tokamax_ragged_dot",
)

```

The bigger the batch, the bigger the win. At batch size 64, decoding is 21.5× faster on Qwen3-30B-A3B and 12.8× faster on Gemma 4 26B-A4B.

Decode throughput on a TPU v6e-8, Hub kernel vs. the default implementation.

![Decode throughput with the Hub ragged-dot kernel versus the default grouped_mm, for Qwen3-30B-A3B and Gemma 4 26B-A4B](/images/posts/a94d8e077cb8.png)

## We test it so you don't have to 🧪

We're continuously improving TPU support in transformers by running the library test suite. We are working to add a nightly CI on TPU and make the results available in the (transformers dashboard)[https://huggingface.co/spaces/transformers-community/transformers-ci-dashboard].

The Transformers CI dashboard, with TPU results next to other accelerators. Work in progress!

![Transformers CI dashboard with TPU test results next to other accelerators](/images/posts/3895fa970ac9.png)

It's not all green yet, and we're fine with that. Of the tests that run on TPU, 96.5% pass. Every failure we find becomes a small repro script and an issue on the TorchTPU repo. So far we have reported 34 issues, and 19 are already fixed. Running on TPU also caught a few bugs in Transformers itself, like inStaticCacheand the Qwen3 tensor-parallel plans. We fixed those upstream.

If something breaks on TPU, we want to find out before you do.

## Get started

TPUs are no longer a side quest for PyTorch users. Install TorchTPU, grab a model from the Hub, and send it to"tpu".

- TorchTPU on GitHub
- TPU kernels on the Hub
- Cloud TPU documentation

We can't wait to see what you build 🤗. If you hit a problem, open an issue and tell us about it.

---

> 本文由AI自动翻译，原文链接：[Hugging Face ❤️ TorchTPU: TPUs, Natively](https://huggingface.co/blog/hf-torchtpu)
> 
> 翻译时间：2026-10-21 06:58
