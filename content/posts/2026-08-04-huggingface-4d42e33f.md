---
title: LFM2.5-2.6B：在任意设备上部署本地Agent
title_original: Deploy local agents everywhere with LFM2.5-2.6B
date: '2026-08-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b
author: ''
summary: LFM2.5-2.6B是一款专为设备端Agent设计的小型语言模型，支持工具调用和多步工作流，在保持低内存占用（<2.5GB）的同时，实现了与4倍大小模型竞争的性能。其训练采用四阶段后训练流程，包括SFT、教师模型专业化、多领域策略蒸馏和Agent强化学习，确保在真实框架中的兼容性。在基准测试中，该模型在指令遵循和工具使用上表现优异，推理速度在Apple
  M5 Max上达220 tok/s，在CPU和GPU上均具高效性。文章还提供了使用方法和推理生态支持，强调其适合高吞吐量设备端应用。
categories:
- AI产品
tags:
- 本地Agent
- 模型部署
- 工具调用
- 推理优化
- 边缘计算
draft: false
translated_at: '2026-08-05T05:29:20.948453'
---

# 使用LFM2.5-2.6B在任意位置部署本地Agent

LFM2.5-2.6B旨在完全在设备端驱动强大的Agent。它支持工具调用和多步骤工作流，同时保持足够小巧和快速，适用于从笔记本电脑到手机的日常硬件。这使得开发者能够在任何地方部署Agent，保持数据在设备上的私密性，并且无需云端推理账单即可扩展使用规模。

- **一流的Agent能力**：在工具使用、指令遵循和多步骤Agent任务上，与4倍大小的模型竞争。
- **Agent强化学习**：在最流行的Agent框架内进行训练，以提高兼容性。
- **高效推理**：在Apple M5 Max上达到220 tok/s，在AMD Ryzen CPU上达到113 tok/s，内存占用低于2.5 GB。

![lfm2_5_2_6b_evaluations](/images/posts/b3d3acf10329.png)

## 我们如何为边缘设备构建可靠的Agent模型

LFM2.5-2.6B在约34T Token上进行了预训练，中间训练阶段将上下文窗口扩展到128K。随后，后训练通过四个阶段将基础模型转变为Agent：

1. **监督微调（SFT）**：两轮SFT，重点加权于Agent数据，如工具使用、网络搜索和框架轨迹。
2. **教师模型专业化**：为每个领域（数学、代码、工具使用等）训练一个专业教师模型。
3. **多领域策略蒸馏（MOPD）**：将专业教师模型蒸馏到单个学生模型中。
4. **Agent强化学习（Agentic RL）**：在真实的Agent框架内运行多轮强化学习，使模型学会在不同的工具、系统提示词和多轮任务环境中工作。

![LFM2.5-2.6B-Training-Recipe](/images/posts/20bc4bfd4f47.png)

Agentic RL流水线将模型优化、推理和环境执行分离为不同的组件。**训练引擎**优化模型，而**推演引擎**使用最新策略生成动作。**RL框架**通过启动推演、收集轨迹和奖励以及更新模型来编排训练循环。

动作在**沙箱服务**内执行，其中**黑盒框架**托管Agent（例如，OpenClaw或Hermes Agent）并协调与任务环境的交互。**框架代理**使我们能够将Agent框架视为黑盒而无需修改，同时透明地捕获重建和验证RL训练样本所需的Token级轨迹。

![LFM2.5-2.6B-Agentic-RL](/images/posts/84b1bc18587e.png)

## 基准测试结果

我们在STEM、指令遵循、工具使用和Agent任务上，将LFM2.5-2.6B与高达其约4倍大小的模型进行了评估。它是该组中最小的模型，但能与其余模型竞争并经常超越它们。

对于您的应用而言，其优势在于指令遵循和工具使用。LFM2.5-2.6B在此处的所有指令遵循基准测试中均排名第一，并且在除BFCLv4之外的所有工具使用基准测试中均排名第一，在BFCLv4中仅9.7B的Qwen略微领先。在Agent任务上，它击败了两个Gemma模型，并与Qwen模型持平。它在知识方面也处于领先地位，在数学方面保持接近。编码是较大模型保持明显领先的唯一领域，因此在该领域请选择更大的模型。

## CPU和GPU上的推理速度

LFM2.5-2.6B在推理生态系统中提供首日支持，包括llama.cpp、MLX、vLLM、SGLang和ONNX。

**CPU推理**。由于其高效的LFM2架构，LFM2.5-2.6B是我们测试过的最快模型，在M5 Max上解码速度为220 tokens/s，在Ryzen AI Max+ 395上为113 tokens/s。在30 tokens/s的速度下，即使在手机上也能运行强大的Agent。

![lfm2_5_2_6b_cpu_inference](/images/posts/c9f4c7fbfb4f.png)

**GPU推理**。LFM2.5-2.6B是其尺寸类别中最快的模型，在高并发下达到近15K输出Token/秒，单个H100上每天约1.3B Token。

![lfm2_5_2_6b_gpu_inference](/images/posts/de7fa1cad67b.png)

## 如何使用LFM2.5-2.6B

当您需要用于高吞吐量工作负载的设备端Agent时，请选择LFM2.5-2.6B。

安装最新版本的`transformers`（兼容`transformers>=5.0.0`）：

```shell
pip install -U transformers

```

然后加载并运行模型：

```py
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "LiquidAI/LFM2.5-2.6B"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype="bfloat16",

)
tokenizer = AutoTokenizer.from_pretrained(model_id)

prompt = "What is C. elegans?"
input_ids = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    add_generation_prompt=True,
    return_tensors="pt",
    tokenize=True,
).to(model.device)

output = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.2,
    top_k=80,
    repetition_penalty=1.05,
    max_new_tokens=512,
)
print(tokenizer.decode(output[0], skip_special_tokens=False))

```

## LFM2.5-2.6B演示

查看这个由LFM2.5-2.6B驱动的研究Agent的浏览器演示。该Agent帮助您研究特定问题并生成摘要。

## 开始使用

LFM2.5-2.6B和LFM2.5-2.6B-Base今天都可以在Hugging Face上获取。

通过LFM2.5，我们正在实现AI随处运行的愿景。这些模型：

- **下载**：在Hugging Face上获取LFM2.5-2.6B-Base和LFM2.5-2.6B。
- **试用**：在浏览器中运行WebGPU演示，无需设置。
- **在您的框架中使用**：按照我们的指南运行本地Agent，如OpenClaw、Hermes Agent和Pi。

我们迫不及待地想看到您构建的成果。

## 引用

请引用本文为：

```
Liquid AI, "LFM2.5-2.6B: Deploy Agents Everywhere", Liquid AI Blog, Aug 2026.

```

或使用BibTeX引用：

```
@article{liquidAI202626B,
  author  = {Liquid AI},
  title   = {LFM2.5-2.6B: Deploy Agents Everywhere},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm2-5-2-6b},
}

```

---

> 本文由AI自动翻译，原文链接：[Deploy local agents everywhere with LFM2.5-2.6B](https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b)
> 
> 翻译时间：2026-08-05 05:29
