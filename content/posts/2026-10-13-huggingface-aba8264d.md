---
title: Run fast, private agents on-device with LFM2.5-24B-A2B
title_original: Run fast, private agents on-device with LFM2.5-24B-A2B
date: '2026-10-13'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b
author: ''
summary: '[翻译失败，原文如下]


  # Run fast, private agents on-device with LFM2.5-24B-A2B


  LFM2.5-24B-A2Bis a 24B-parameter reasoning model with just 2B active parameters...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-24T07:04:43.364747'
---

[翻译失败，原文如下]

# Run fast, private agents on-device with LFM2.5-24B-A2B

LFM2.5-24B-A2Bis a 24B-parameter reasoning model with just 2B active parameters, built for fast, private agents on-device. It thinks before it answers, calls tools, and works through multi-step tasks inside popular agent harnesses. Because only 2B parameters are active per token, each reasoning token is cheap, so you can run agents continuously on your own hardware.

- Best-in-class agent:Competitive with Qwen3.6-35B-A3B, a model with ~50% more total and active parameters, on agentic and tool-use tasks, scoring 48.09 on LiveClaw versus 38.19.
- Reasoning at MoE speed:Always thinks before it answers. With only 2B active parameters per token, each reasoning token is cheap.
- Efficient inference:184 tok/s on an Apple M5 Max and up to 21K output tok/s on a single NVIDIA B300 GPU.

![LFM2.5-24B-A2B-benchmark](/images/posts/c326e160db4c.png)

## How we built a reasoning agent with 2B active parameters

LFM2.5-24B-A2B builds onLFM2-24B-A2Band keeps its architecture: 40 layers, 64 experts per MoE block with top-4 routing, and the same hybrid of gated short convolutions and GQA. The context window grows from 32K to 131K tokens, and anin-place tokenizer expansiondoubles the vocabulary from 65K to 128K tokens for better non-Latin tokenization. Unlike its predecessor, it is a reasoning-only model that produces an explicit chain of thought before its final answer.

Pre-training was scaled up from ~17T to ~33T tokens. Mid-training then adds 2T tokens at 32K context, weighted toward reasoning, math, code, instruction following, and multilingual text, and 300B tokens at 131K context, weighted toward long-context data. Tool calls and multi-turn trajectories appear throughout both phases. Post-training turns the base model into an agent in five stages:

1. Supervised fine-tuning (SFT)
2. Teacher specialization
3. Multi-domain on-policy distillation (MOPD), non-agentic:distill the specialist teachers on non-agentic tasks.
4. MOPD, agentic:a second distillation stage focused on agentic tasks.
5. Agentic reinforcement learning (Agentic RL):train the model inside agent harnesses, such asOpenClaw,Hermes Agent,Pi, andOpenCode.

![LFM2.5-24B-A2B-Training-Recipe](/images/posts/e77dacfdeaf3.png)

## Benchmark results

We evaluated LFM2.5-24B-A2B against Qwen3.6-35B-A3B, Gemma-4-26B-A4B-it, and Nemotron-3.5-Lightning on 16 benchmarks covering tool use and agentic workflows, knowledge, instruction following, math, and coding. It is the smallest model in the group, yet it is competitive with MoEs with ~50% more total and active parameters.

*All the models were evaluated with vLLM, using each benchmark's recommended generation parameters.

For your app, the strengths are tool use and instruction following. LFM2.5-24B-A2B leads or matches the competition on five of the eight tool-use and agentic benchmarks (AutomationBench, BFCLv4, ToolSandbox, LiveClaw, and τ³-Bench Banking), and on AutomationBench it scores more than three times the next-best model. It also leads on all three instruction-following benchmarks. Larger models keep an edge on knowledge-heavy benchmarks like GPQA Diamond, HLE, and AA-Omniscience, and on coding benchmarks like SWE-Bench Verified (OpenCode) and SciCode, so pair LFM2.5-24B-A2B with retrieval or web search for knowledge-heavy workloads.

These results make LFM2.5-24B-A2B a strong foundation for agents that need to reason, call tools, and run reliably on your device.

## Inference speed on CPU and GPU

LFM2.5-24B-A2B ships with day-one support across the inference ecosystem, including llama.cpp, MLX, vLLM, SGLang, and ONNX.

Edge inference.LFM2.5-24B-A2B is the fastest of the compared MoEs, decoding 184 tokens/s on an M5 Max and 114 tokens/s on a Ryzen AI Max+ 395. That is up to 1.7x faster than the next-best model, while using the least memory.

![LFM2.5-24B-A2B-edge-inference](/images/posts/5803d29e1830.png)

GPU inference.LFM2.5-24B-A2B is the fastest model in its size class, reaching over 21K output tokens per second at high concurrency on a single B300.

![LFM2.5-24B-A2B-gpu-inference](/images/posts/2aaedf067b14.png)

## How to use LFM2.5-24B-A2B

Reach for LFM2.5-24B-A2B when you need agents that reason, call tools, and run reliably on your device.

Install the latest version oftransformers(compatible withtransformers>=5.0.0):

```sh
pip install -U transformers

```

Then load and run the model:

```py
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

model_id = "LiquidAI/LFM2.5-24B-A2B"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype="bfloat16",

)
tokenizer = AutoTokenizer.from_pretrained(model_id)
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

prompt = "What is C. elegans?"

input_ids = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    add_generation_prompt=True,
    return_tensors="pt",
    tokenize=True,
)["input_ids"].to(model.device)

output = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.1,
    top_k=50,
    repetition_penalty=1.05,
    max_new_tokens=512,
    streamer=streamer,
)

```

### Use it in your agent harness

Serve LFM2.5-24B-A2B locally behind any OpenAI-compatible backend, then point your agent harness at it. For example, with Hermes Agent:

```sh
hermes config set model.provider custom
hermes config set model.base_url http://localhost:8080/v1
hermes config set model.default LFM2.5-24B-A2B
hermes config set model.context_length 131072
hermes config set model.api_mode chat_completions
hermes config set agent.tool_use_enforcement true

```

The port depends on your serving backend: llama.cpp and MLX use8080, vLLM uses8000, SGLang uses30000, and LM Studio uses1234. See themodel cardfor OpenClaw and Pi configs, andour guidefor the full setup. Check out ourrelease blogfor video examples.

## Get Started with LFM2.5-24B-A2B

Both LFM2.5-24B-A2B and LFM2.5-24B-A2B-Base are open-weight and available on Hugging Face today:

- Download:LFM2.5-24B-A2B-BaseandLFM2.5-24B-A2Bon Hugging Face.
- Use in your harness:follow ourguideon how to run a local agent, like OpenClaw, Hermes Agent, and Pi.
- Fine-tune:adapt LFM2.5-24B-A2B to your task with ourfine-tuning tutorials.

We can't wait to see what you build.

## Citation

If you use this work, please cite the release blog:

```
@article{liquidAI202624BA2B,
  author  = {Liquid AI},
  title   = {LFM2.5-24B-A2B: Built for Fast On-Device Agents},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm2-5-24b-a2b},
}

```

---

> 本文由AI自动翻译，原文链接：[Run fast, private agents on-device with LFM2.5-24B-A2B](https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b)
> 
> 翻译时间：2026-10-24 07:04
