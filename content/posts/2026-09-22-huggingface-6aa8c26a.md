---
title: Transformers now runs llama.cpp quants
title_original: Transformers now runs llama.cpp quants
date: '2026-09-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/transformers-llama-cpp-quants
author: ''
summary: '[翻译失败，原文如下]


  # Transformers now runs llama.cpp quants


  We''re adding support for running GGUF models efficiently in transformers, so you
  can use checkp...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-24T07:29:02.860779'
---

[翻译失败，原文如下]

# Transformers now runs llama.cpp quants

We're adding support for running GGUF models efficiently in transformers, so you can use checkpoints sized for your laptop's memory through the familiar transformers APIs. Pick a GGUF from the Hub, load it withfrom_pretrained, and start generating on your own machine.

Running AI models on your laptop has become much easier, andllama.cpphas been a big part of that. Its inference engine powers local AI tools such as Ollama, LM Studio, and Jan. Alongside projects likeMLX, it has helped make local inference a practical option for everyday use.

A recent example of what local AI can feel like:

This is where we are right now. And i’m not gonna lie it feels pretty magical 🧙‍♀️Qwen3.6 27B running inside of Pi coding agent via Llama.cpp on the MacBook ProFor non-trivial tasks on the@huggingfacecodebases, this feels very, very close to hitting the latest Opus in Claude…pic.twitter.com/lsIxLoUneU

GGUF, developed by the llama.cpp team, is a widely used format for local inference. The team also shares quantized checkpoints underggml-org on the Hub. Publishers such asUnsloth,LM Studio Community, andbartowskialso provide ready-to-use GGUF checkpoints in a range of quantizations, so users can pick the version that fits their machine. GGUF models have been downloaded millions of times.

We want to make it easier to run these models locally with transformers, too. Compatibility is only useful if the model is pleasant to run. To bring performance close to llama.cpp, we're reusing its underlying ggml kernels through thekernelslibrary, and reducing overhead ingenerate. Our initial focus is local inference on Apple Silicon, starting with the Qwen3.5 architecture.

## What is the GGUF file format?

GGUFpackages model weights and metadata, including tokenizer information and an optional chat template, in one file. It supports different quantization levels, letting you trade some precision for a smaller memory footprint. Variants such asQ4_K_Mmix tensor precisions, using mostly 4-bit weights while keeping sensitive tensors at higher precision.

Here's how quantization changes the file size ofUnsloth's Qwen3.5-4B:

We suggest starting withQ4_K_M, then tryingQ5_K_MorQ6_Kif you have more memory available. More aggressive quantization can help larger models fit, but the quality tradeoff depends on the model and the task. Evaluate it on the work you actually want the model to do. TheHub's GGUF documentationdescribes the available quantization types.

## Load GGUF with transformers

To get started, you need:

- An Apple Silicon Mac.
- A PyTorch version supported by the publishedggml-quantization kernel builds, usually the two latest PyTorch releases.
- The latest version of transformers (main for now, until the next release) and a compatible version ofkernels.

```bash
pip install -U "git+https://github.com/huggingface/transformers.git" kernels

```

To load a GGUF model, pass its Hubmodel_idand filename asgguf_filetofrom_pretrained.

No extra configuration is needed: when the weights stay packed on Metal, transformers automatically loads the compatible ggml/Metal layer kernels and usesggml-org/ggml-attnas the attention implementation. If that kernel cannot be fetched, the model falls back to"sdpa"with a warning, and you can always force"sdpa"by passingattn_implementation="sdpa"explicitly. See theGGUF documentationfor more loading options.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "unsloth/Qwen3.5-4B-GGUF"
filename = "Qwen3.5-4B-Q4_K_M.gguf"

tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=filename)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    gguf_file=filename
)

```

That is the only GGUF-specific step. Everything after it is the standard transformers API:

```python
messages = [{"role": "user", "content": "Explain why the sky is blue in a few sentences."}]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=256)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

```

Without a compatible quantization kernel, the loader falls back to dequantizing the model and uses more memory.

## Serve GGUF with your preferred interface

You can also use the same checkpoint withtransformers serve, which exposes an OpenAI-compatible API:

```bash
pip install -U "transformers[serving] @ git+https://github.com/huggingface/transformers.git" kernels

transformers serve "unsloth/Qwen3.5-4B-GGUF:Qwen3.5-4B-Q4_K_M.gguf"

```

The model argument uses<model_id>:<filename>.gguf: before the colon is the Hub repository (unsloth/Qwen3.5-4B-GGUF), and after it is the file to load (Qwen3.5-4B-Q4_K_M.gguf). This selects a specific quantization from a repository that may contain several.

For models whose chat template supports thinking, add--reasoning offto skip it or--reasoning onto enable it. The default,--reasoning auto, follows the chat template’s default. See thereasoning optionsfor details.

You can connect a client such asJanorPiby adding a custom OpenAI-compatible provider with these settings:

transformers runs the model on your Mac, while the client provides the conversation interface. The same endpoint can be used by other clients that support this API.

## Benchmarking against llama.cpp

Our reference for local inference performance is llama.cpp. The comparison below focuses on three GGUF checkpoints: a small dense model, a larger dense model, and a mixture-of-experts model.

The llama.cpp column comes from thellama-benchtool (build5f55650a7, release b10200, Metal backend from ggml 0.18.0), run asllama-bench -m <file> -p 0 -n 128 -r 3, which reportstg128: the token-generation rate over 128 decoded tokens, averaged across three repetitions, with prompt processing excluded. The transformers column isgenerateproducing the same 128 tokens from a 12-token prompt, best of three warmed runs, and it includes prefill.

Measured on a MacBook Pro M2 Max, 32 GB unified memory, macOS 26.6, PyTorch 2.12.1, kernels 0.17.0,
plugged in.

```python
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id, filename = "unsloth/Qwen3.5-4B-GGUF", "Qwen3.5-4B-Q4_K_M.gguf"

model = AutoModelForCausalLM.from_pretrained(model_id, gguf_file=filename)
tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=filename)
inputs = tokenizer("The capital of France is Paris. The capital of Germany is", return_tensors="pt")
inputs = inputs.to(model.device)


with torch.inference_mode():
    model.generate(**inputs, max_new_tokens=8, min_new_tokens=8, do_sample=False)  
    torch.mps.synchronize()
    for _ in range(3):
        time.sleep(90)  
        start = time.perf_counter()
        model.generate(**inputs, max_new_tokens=128, min_new_tokens=128, do_sample=False)
        torch.mps.synchronize()
        print(f"{128 / (time.perf_counter() - start):.1f} tok/s")

```

For the other column:

```bash
llama-bench -hf unsloth/Qwen3.5-4B-GGUF:Q4_K_M -p 0 -n 128 -r 3

```

Transformers is close to llama.cpp across all three checkpoints. The chart uses the same measurements described above; it does not imply identical benchmark conditions, since the Transformers measurement includes prefill whilellama-benchreports decode-only throughput.

## transformers and llama.cpp

WhenGGML and llama.cpp joined Hugging Face, we described their complementary roles: llama.cpp provides a foundation for local inference, while transformers provides a foundation for model definition. GGUF support brings those two closer together.

[翻译失败，原文如下]

llama.cpp remains our recommended engine when your priority is efficient local inference.Its dedicated runtime, memory management, and broad hardware support are built around that goal. This integration gives developers a convenient way to work with the same GGUF checkpoints inside transformers:

- Experiment with GGUF in Python and PyTorch.Inspect intermediate activations with hooks, modify a model's forward pass, or prototype custom layers using familiar PyTorch tools.
- Evaluate GGUF models.Use your existing transformers evaluation workflows to measure the quality of quantized checkpoints.
- Validate GGUF conversions.For us as developers, loading the original checkpoint and its GGUF conversion in transformers makes it easier to check that the weights were converted correctly, accounting for quantization error.
- Try new decoding ideas.Use custom logits processors and stopping criteria withgenerate, or write your own generation loop in Python.
- Fine-tune from a GGUF checkpoint.Dequantize the weights and continue with a standard transformers training workflow.

For that last case, useGgufConfig(dequantize=True):

```python
import torch
from transformers import AutoModelForCausalLM, GgufConfig

model = AutoModelForCausalLM.from_pretrained(
    "unsloth/Qwen3.5-4B-GGUF",
    gguf_file="Qwen3.5-4B-Q4_K_M.gguf",
    quantization_config=GgufConfig(dequantize=True),
    dtype=torch.bfloat16,
)

```

## Beyond GGUF: ggml kernels for more models

The bigger opportunity is bringing ggml's performance to models that llama.cpp does not support.

transformers already provides the PyTorch implementations of these architectures. With ggml kernels and quantization schemes available in PyTorch, we can work toward accelerating their supported operations without first implementing the entire model in llama.cpp. This is especially useful for new architectures, research models, and custom variants that may never receive a dedicated llama.cpp implementation.

That opportunity extends beyond the GGUF format itself. A kernel operates on tensors; it does not require the whole model to come from a GGUF file. The same building blocks can be integrated into other transformers models and loading workflows. This also opens a path to other modalities: computer vision models, audio models, and multimodal models could reuse compatible attention, normalization, and matrix multiplication kernels without first having a full implementation in llama.cpp. Each architecture still needs integration and validation; the initial GGUF examples here cover text generation.

## Fast local inference with Python and PyTorch

We also wanted to show how far we can get while keeping the model and generation loop in Python.With the right kernels and an efficient generation loop, Python and PyTorch can deliver strong local inference performance.The kernels handle the heavy computation, while the generation loop keeps the GPU busy by avoiding unnecessary synchronization.

Our focus was to make eager execution fast without requiringtorch.compile. For interactive use, we wanted a quick start and a steady stream of tokens, without compilation pauses or recompilation when input shapes change. The two main pieces of that work are the kernels andgenerateitself.

### Reusing ggml's Metal kernels

A kernel is a small program that performs an operation on the GPU. PyTorch supplies general-purpose implementations; a specialized kernel can do less work, combine several operations, or read quantized weights directly in their stored format.

Thekernelslibrary lets us distribute compatible builds of ggml's Metal kernels on the Hub and call them from transformers. That brings ggml's work into the PyTorch model without replacing the model with a separate inference runtime.

The first four packages build on ggml's kernels; the top-k kernel addresses a separate bottleneck in MoE routing. Together they reduce the GPU work needed for each generated token.

To show the contribution of the layer kernels, we compare the same packed GGUF checkpoints with and without them. The quantization kernel stays enabled in both configurations: disabling it would also change how weights are represented and would measure a different tradeoff.

### Keeping the CPU and GPU working together

Faster kernels only help if the GPU has work to do. During generation, the CPU schedules GPU operations and controls the loop that produces the next token. Reading a result back from the GPU can force the CPU to wait until queued operations finish. Repeating even a small wait for every token can noticeably reduce throughput.

Two changes address this ingenerate, which results in improvements for all transformers models (not just when running GGUF files):

- Drop an unnecessary attention mask early (#48814).When a supported decoder-only input has no padding, its all-ones padding mask can be removed at the start of generation. Downstream attention code no longer needs to inspect that mask repeatedly to determine whether it can be skipped. Causal attention is still preserved.
- Defer the stopping check (#47975).On supported paths,generatecopies the stopping decision asynchronously and consumes it on the following step. The CPU can keep scheduling work while the GPU runs. Streaming tokens use the same approach, and any extra step past the stopping condition is removed from the result.

These changes improve the generation loop around the model, so their usefulness extends beyond GGUF. They complement the kernel work: kernels reduce the cost of an operation, while fewer synchronization points let CPU scheduling and GPU execution overlap.

These measurements keep all layer kernels enabled; the bars isolate the changes to the generation loop.

## Current limitations and next steps

The initial target is a single interactive conversation on Apple Silicon. There are a few boundaries to keep in mind:

- The packed inference path is MPS-only for now.GGUF import through dequantization remains a separate option; support for the file format does not imply that packed kernels are available on every device.
- Padding and batching still need work.Unpadded inputs benefit from the mask optimization described above. Padded batches cannot take the same shortcut and can have lower performance. We want to extend the work togenerate_batchon MPS.
- Architecture coverage is limited.The packed loader currently covers the Qwen3.5 dense and MoE architectures, including compatible Qwen3.8 checkpoints. Adding support for other architectures is relatively straightforward, and we’ll expand coverage gradually.

If you have a GGUF model you would like to use in transformers,open an issuewith the checkpoint and your use case. That will help us prioritize support for the models people are running locally.

## Acknowledgments

We would like to thankArthur Zuckerfor initiating this work and reviewing all of my PRs, andCyril Vallezfor thegeneratePRs. We are grateful toSayak Paul, thellama.cpp team, and Bertrand Chevalier for their help integrating the kernels. We also thankAritra Roy GosthipatyandPedro Cuencafor reviewing this blog post, andLysandre Debutfor overseeing the project.

---

> 本文由AI自动翻译，原文链接：[Transformers now runs llama.cpp quants](https://huggingface.co/blog/transformers-llama-cpp-quants)
> 
> 翻译时间：2026-09-24 07:29
