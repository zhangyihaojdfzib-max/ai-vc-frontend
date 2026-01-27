---
title: 谷歌云C4联手英特尔与Hugging Face，GPT OSS推理成本降低70%
title_original: Google Cloud C4 Brings a 70% TCO improvement on GPT OSS with Intel
  and Hugging Face
date: '2025-10-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gpt-oss-on-intel-xeon
author: ''
summary: 英特尔与Hugging Face合作，在搭载英特尔至强6处理器的谷歌云最新C4虚拟机上优化GPT OSS开源大语言模型。通过专家执行优化消除冗余计算，相比上一代C3虚拟机，实现了1.7倍的总体拥有成本提升，每vCPU每美元吞吐量提高1.4至1.7倍，且每小时价格更低。文章详细介绍了基准测试配置、硬件环境搭建步骤及优化原理。
categories:
- AI基础设施
tags:
- 谷歌云
- 英特尔
- Hugging Face
- 大语言模型推理
- 成本优化
draft: false
translated_at: '2026-01-27T00:48:15.401118'
---

# Google Cloud C4 与英特尔及 Hugging Face 合作，为 GPT OSS 带来 70% 的总体拥有成本改善

英特尔与 Hugging Face 合作，展示了升级至运行在英特尔® 至强® 6 处理器（代号 Granite Rapids (GNR)）上的 Google 最新 C4 虚拟机（VM）所带来的实际价值。我们特别希望对标 OpenAI GPT OSS 大语言模型（LLM）在文本生成性能方面的改进。

结果已经出炉，令人印象深刻，与上一代 Google C3 VM 实例相比，总体拥有成本（TCO）提升了 1.7 倍。Google Cloud C4 VM 实例还带来了：

*   每 vCPU/每美元的 TPOT 吞吐量提升 1.4 倍至 1.7 倍
*   每小时价格低于 C3 VM

## 引言

GPT OSS 是 OpenAI 发布的一个开源混合专家（MoE）模型的通用名称。MoE 模型是一种深度神经网络架构，它使用专门的“专家”子网络和一个“门控网络”来决定对给定输入使用哪些专家。MoE 模型允许您高效扩展模型容量，而无需线性增加计算成本。它们还支持专业化，不同的“专家”学习不同的技能，使其能够适应多样化的数据分布。

即使参数量非常大，每个 Token 也只会激活一小部分专家，这使得 CPU 推理成为可能。

英特尔与 Hugging Face 合作，合并了一项专家执行优化（PR#40304），以消除每个专家处理所有 Token 到 Transformer 时的冗余计算。此优化引导每个专家仅在其被路由到的 Token 上运行，消除了 FLOPs 浪费并提高了利用率。

![gpt_oss_expert](/images/posts/86c1fcc6778e.png)

## 基准测试范围与硬件

我们在受控、可重复的生成工作负载下对 GPT OSS 进行了基准测试，以隔离架构差异（运行在英特尔至强 6 处理器 (GNR) 上的 GCP C4 VM 与运行在第四代英特尔至强处理器 (SPR) 上的 GCP C3 VM）以及 MoE 执行效率。重点是稳态解码（每 Token 延迟）和随着批次大小增加而保持序列长度固定时的端到端归一化吞吐量。所有运行均使用静态 KV 缓存和 SDPA 注意力机制以确保确定性。

### 配置摘要

*   模型：`unsloth/gpt-oss-120b-BF16`
*   精度：bfloat16
*   任务：文本生成
*   输入长度：1024 个 Token（左填充）
*   输出长度：1024 个 Token
*   批次大小：1, 2, 4, 8, 16, 32, 64
*   启用功能：
    *   静态 KV 缓存
    *   SDPA 注意力后端
*   报告指标：
    *   吞吐量（批次聚合的总生成 Token 数/秒）

### 被测硬件

## 创建实例

访问 Google Cloud Console，在您的项目下点击“创建 VM”。按照以下步骤创建一个 176 vCPU 的实例。

1.  在“机器配置”中选择 C3，并将“机器类型”指定为 `c3-standard-176`。您还需要设置“CPU 平台”并打开“全核睿频”以使性能更稳定：
2.  按如下配置操作系统和存储选项卡：
3.  保持其他配置为默认值
4.  点击“创建”按钮

![alt text](/images/posts/059e3d04dd67.png)

![alt text](/images/posts/0d600a111940.png)

访问 Google Cloud Console，在您的项目下点击“创建 VM”。按照以下步骤创建一个 144 vCPU 的实例。

1.  在“机器配置”选项卡中选择 C4，并将“机器类型”指定为 `c4-standard-144`。您也可以设置“CPU 平台”并打开“全核睿频”以使性能更稳定：
2.  按照 C3 所需的方式配置操作系统和存储选项卡。
3.  保持其他配置为默认值
4.  点击“创建”按钮

![alt text](/images/posts/a0d4fdfee750.png)

## 设置环境

通过 SSH 登录实例，然后安装 Docker。按照以下步骤轻松设置环境。为了可复现性，我们在命令中列出了我们使用的版本和提交。

1.  `$ git clone https://github.com/huggingface/transformers.git`
2.  `$ cd transformers/`
3.  `$ git checkout 26b65fb5168f324277b85c558ef8209bfceae1fe`
4.  `$ cd docker/transformers-intel-cpu/`
5.  `$ sudo docker build . -t <your_docker_image_tag>`
6.  `$ sudo docker run -it --rm --privileged -v /home/<your_home_folder>:/workspace <your_docker_image_tag> /bin/bash`

现在我们在容器中，执行以下步骤。

1.  `$ pip install git+https://github.com/huggingface/transformers.git@26b65fb5168f324277b85c558ef8209bfceae1fe`
2.  `$ pip install torch==2.8.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`

## 基准测试流程

对于每个批次大小，我们：

1.  构建一个固定长度为 1024 个 Token 的左填充批次。
2.  运行一轮预热。
3.  设置 `max_new_tokens=1024` 并测量总延迟，然后计算 `throughput = (OUTPUT_TOKENS * batch_size) / total_latency`。

运行 `numactl -l python benchmark.py` 执行以下代码。

```python
import os
import time
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

INPUT_TOKENS = 1024
OUTPUT_TOKENS = 1024

def get_inputs(tokenizer, batch_size):
    dataset = load_dataset("ola13/small-the_pile", split="train")
    tokenizer.padding_side = "left"
    selected_texts = []
    for sample in dataset:
        input_ids = tokenizer(sample["text"], return_tensors="pt").input_ids
        if len(selected_texts) == 0 and input_ids.shape[-1] >= INPUT_TOKENS:
            selected_texts.append(sample["text"])
        elif len(selected_texts) > 0:
            selected_texts.append(sample["text"])
        if len(selected_texts) == batch_size:
            break

    return tokenizer(selected_texts, max_length=INPUT_TOKENS, padding="max_length", truncation=True, return_tensors="pt")

def run_generate(model, inputs, generation_config):
    inputs["generation_config"] = generation_config
    model.generate(**inputs) 
    pre = time.time()
    model.generate(**inputs)
    latency = (time.time() - pre)
    return latency

def benchmark(model, tokenizer, batch_size, generation_config):
    inputs = get_inputs(tokenizer, batch_size)
    generation_config.max_new_tokens = 1
    generation_config.min_new_tokens = 1
    prefill_latency = run_generate(model, inputs, generation_config)
    generation_config.max_new_tokens = OUTPUT_TOKENS
    generation_config.min_new_tokens = OUTPUT_TOKENS
    total_latency = run_generate(model, inputs, generation_config)
    decoding_latency = (total_latency - prefill_latency) / (OUTPUT_TOKENS - 1)
    throughput = OUTPUT_TOKENS * batch_size / total_latency

    return prefill_latency, decoding_latency, throughput


if __name__ == "__main__":
    model_id = "unsloth/gpt-oss-120b-BF16"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model_kwargs = {"dtype": torch.bfloat16}
    model = AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)
    model.config._attn_implementation="sdpa"
    generation_config = model.generation_config
    generation_config.do_sample = False
    generation_config.cache_implementation="static"

    for batch_size in [1, 2, 4, 8, 16, 32, 64]:
        print(f"---------- Run generation with batch size = {batch_size} ----------", flush=True)
        prefill_latency, decoding_latency, throughput = benchmark(model, tokenizer, batch_size, generation_config)
        print(f"throughput = {throughput}", flush=True)

```

## 结果

### 每 vCPU 归一化吞吐量

在批次大小高达 64 的范围内，基于英特尔至强 6 处理器的 C4 始终优于 C3，每 vCPU 吞吐量高出 1.4 倍至 1.7 倍。计算公式为：

`normalized_throughput_per_vCPU = (throughput_C4 / vCPUs_C4) / (throughput_C3 / vCPUs_C3)`

![throughput-gpt-oss-per-vcpu](/images/posts/73cbeeabc3c3.png)

### 成本与 TCO

在批次大小为64时，C4提供的每vCPU吞吐量是C3的1.7倍；考虑到每vCPU价格近乎持平（每小时成本随vCPU数量线性增长），这带来了1.7倍的总拥有成本优势（C3需要花费1.7倍的成本才能生成相同的Token量）。

每vCPU吞吐量比率：
\[
\frac{\text{throughput\_C4} / \text{vCPUs\_C4}}{\text{throughput\_C3} / \text{vCPUs\_C3}}
= 1.7 
\Rightarrow 
\frac{\text{TCO\_C3}}{\text{TCO\_C4}} \approx 1.7
\]

![throughput-gpt-oss-per-dollar](/images/posts/1e45f4c7a0bb.png)

## 结论

由英特尔至强6处理器（GNR）驱动的Google Cloud C4虚拟机，在大型MoE模型推理方面，相比上一代由第四代英特尔至强处理器驱动的Google Cloud C3虚拟机，不仅提供了显著的性能提升，还具备更好的成本效益。对于GPT开源MoE模型推理，我们观察到了更高的综合吞吐量、更低的延迟以及更低的成本。这些结果表明，得益于英特尔和Hugging Face有针对性的框架优化，大型MoE模型可以在新一代通用CPU上高效运行。

---

> 本文由AI自动翻译，原文链接：[Google Cloud C4 Brings a 70% TCO improvement on GPT OSS with Intel and Hugging Face](https://huggingface.co/blog/gpt-oss-on-intel-xeon)
> 
> 翻译时间：2026-01-27 00:48
