---
title: Granite 4.1 LLM构建详解
title_original: 'Granite 4.1 LLMs: How They’re Built'
date: '2026-04-29'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-granite/granite-4-1
author: ''
summary: 本文由IBM Granite团队撰写，详细介绍了Granite 4.1系列密集解码器LLM（3B、8B、30B）的构建流程。模型采用五阶段预训练策略，在约15T
  Token上训练，包括通用预训练、数学/代码强化、高质量数据退火及长上下文扩展（512K Token）。随后通过410万精选样本进行监督微调，并采用基于DAPO损失的在线策略GRPO进行强化学习。8B指令模型在参数更少的情况下性能超越此前32B-A9B
  MoE模型。所有模型均以Apache 2.0许可证发布。
categories:
- AI研究
tags:
- Granite 4.1
- 大语言模型
- 预训练
- 强化学习
- IBM
draft: false
translated_at: '2026-04-30T05:30:52.371547'
---

# Granite 4.1 LLM：构建方式详解

深入技术解析 Granite 4.1 LLM 背后的数据工程、预训练、监督微调与强化学习。

作者：Granite 团队，IBM

摘要—— Granite 4.1 是一系列密集、仅解码器的 LLM（3B、8B 和 30B），使用多阶段预训练流程在约 15T Token 上训练，包括长达 512K Token 的长上下文扩展。这些模型进一步通过约 410 万个高质量精选样本的监督微调，以及使用 DAPO 损失（Yu 等人，2025）的在线策略 GRPO 进行强化学习来优化。值得注意的是，8B 指令模型在采用更简单的密集架构且参数更少的情况下，匹配或超越了之前的 Granite 4.0‑H‑Small（32B‑A9B MoE）。所有 Granite 4.1 模型均在 Apache 2.0 许可证下发布。

链接：

- Granite 4.1 HF 集合
- GitHub 仓库
- Granite 文档

## 概述

构建高质量的小语言模型不仅仅是扩展算力——它需要在训练过程中进行严格的数据整理。对于 Granite 4.1，我们优先考虑数据质量而非数量，在五个预训练阶段逐步优化数据混合。我们进一步使用 LLM 作为评判框架来整理监督微调数据，并应用多阶段强化学习流程，系统性地增强数学、编码、指令遵循和通用聊天方面的性能。

## 模型架构

Granite 4.1 模型采用仅解码器的密集 Transformer 架构。核心设计选择包括分组查询注意力（GQA）、旋转位置嵌入（RoPE）、SwiGLU 激活函数、RMSNorm 以及共享的输入/输出嵌入。

所有三种模型大小共享相同的训练流程和数据策略，仅在架构维度上有所不同。

## 预训练

Granite 4.1 使用五阶段训练策略，从零开始在约 15 万亿 Token 上进行训练。阶段 1-2 侧重于基础预训练，阶段 3-4 进行中期训练，并逐步采用更高质量的数据退火，阶段 5 引入长上下文训练，将上下文窗口扩展到 512K Token。每个阶段采用不同的数据混合和学习率调度，逐步从广泛的网络规模数据转向更精选的、特定领域的内容。

![五阶段预训练流程](/images/posts/312acd396fb0.png)

图 2：五阶段预训练流程。阶段 1-2 为预训练，阶段 3-4 为中期训练（高质量数据退火），阶段 5 为长上下文训练（LCE）。

### 阶段 1：通用预训练（10T Token）

第一阶段使用通用训练数据混合、幂律学习率调度和预热，建立广泛的语言理解能力。

数据组成：

- CommonCrawl ~59% — 通用网络数据
- 代码 ~20% — 编程语言和仓库
- 数学 ~7% — 数学推理数据
- 技术 ~10.5% — 科学论文、技术文档和手册
- 多语言 ~2% — 非英语语言数据
- 特定领域 ~1.5% — 特定领域内容

### 阶段 2：数学/代码预训练（2T Token）

阶段 2 大幅增加代码和数学数据的比例，转向更强的推理能力，同时仍保持通用语言覆盖。

- 数学 ~35% — 比阶段 1 增加 5 倍
- 代码 ~30% — 增加 1.5 倍
- CommonCrawl-HQ ~12% — 高质量 CommonCrawl 子集
- 合成数据 ~9% — 合成高质量数据
- 技术 ~10%
- 多语言 ~3%
- 领域 ~1%

### 阶段 3：高质量数据退火（2T Token）

阶段 3 进入中期训练，采用更平衡、高质量的混合数据以及指数衰减学习率调度。在此阶段，我们开始融入思维链和合成指令数据。

- CommonCrawl-HQ ~16.67%
- 数学 ~16.67%
- 代码 ~16.67%
- 合成数据 ~8.5%
- 技术 ~12.5%
- 多语言 ~4.5%
- 长思维链 ~12.5% — 推理轨迹
- 语言指令 ~7.5% — 指令微调数据
- 代码指令 ~4.5% — 指令微调数据

### 阶段 4：高质量数据退火——精炼（0.5T Token）

第四阶段继续中期训练，采用线性学习率衰减至零，使模型专注于可用的最高质量数据。

- CommonCrawl-HQ ~40%
- 代码 ~20%
- 数学 ~20%
- 长思维链 ~6%
- 代码指令 ~5%
- 语言指令 ~9%

![预训练阶段数据混合演变](/images/posts/631795f3a2bd.png)

图 3：数据混合在预训练阶段如何演变。注意从以网络为主（阶段 1）逐步转向以质量为主并包含指令和推理数据（阶段 3-4）。

### 阶段 5：长上下文训练（LCE）

第五个也是最后一个阶段（也属于中期训练的一部分）通过分阶段的长上下文扩展过程，将上下文窗口从 4K 扩展到 512K：

1. 32K 扩展——使用与阶段 4 相同的数据混合
2. 128K 扩展——与阶段 4 相同的数据混合
3. 512K 扩展——80% 书籍 + 20% 代码仓库数据（仅限 8b 和 30b）

LCE 阶段使用指数学习率调度，从 1e-4 开始衰减至 0。为确保模型原生处理长序列而不降低短上下文性能，我们在每个 LCE 阶段后进行模型合并。基础模型的 RULER 基准测试：

## SFT：数据准备与质量控制

监督微调（SFT）是将基础模型转变为可靠的指令遵循助手的环节，这使得数据质量至关重要——因为即使少量错误或幻觉样本也可能灌输不良行为。为解决此问题，我们应用严格的 LLM 作为评判框架以及基于规则的过滤，来整理高质量样本。该流程共同根据结构、语义和行为标准自动评估每个样本，尽可能修复问题，并过滤掉不符合我们质量标准的样本。

![SFT 数据质量流程](/images/posts/8ac0deaac34c.png)

图 4：SFT 数据质量流程。原始对话数据通过具有多维评分标准的 LLM 作为评判，产生接受/边缘/拒绝判定。硬拒绝缺陷（幻觉、错误前提、计算错误）无论得分如何都会触发自动拒绝。

我们严格的 LLM 作为评判框架仅评估助手的回复，将系统提示词、用户输入、检索文档和工具输出严格视为上下文信息。这确保评判评估的是模型所说的内容，而不是它被要求做什么。在 RAG 设置中，未基于检索上下文的回复被标记为幻觉，而工具使用输出则根据允许的工具集及其参数模式进行验证。

我们采用针对不同 SFT 数据类型定制的专门评判提示词，包括多轮对话、RAG 增强回复、工具调用交互和多语言对话。每个回复在六个加权维度上评分——指令遵循、正确性、完整性、简洁性、自然性和校准（可选批判性思维检查）。样本根据确定性分数阈值被接受、标记为边缘或拒绝，对于严重缺陷（如幻觉、错误前提或计算错误），硬拒绝规则会覆盖分数。

为补充语义评估，我们应用确定性规则流程，通过文本规范化、截断和长度过滤、模式验证以及泄漏检测来确保结构完整性。最终的全局去重步骤确保整个数据集唯一性。所有过滤和修正操作均可完全审计。

### SFT 训练细节

在通过 LLM 作为评判、基于规则的过滤和全局去重流程后，我们在这些约 410 万个高质量样本上微调基础模型。以下细节适用于所有三种模型变体：

训练配置：

## 强化学习：多阶段 RL 流程

在SFT之后，我们采用多阶段强化学习流水线，进一步提升模型在特定领域的能力。不同于单次RL训练，我们运行多个针对性的RL阶段，每个阶段针对不同能力进行优化。

### 训练方法

我们采用**On-policy GRPO（组相对策略优化）**（Shao等人，2024）结合**DAPO（解耦裁剪与动态采样策略优化）损失函数**（Yu等人，2025），相比标准GRPO能提供更稳定的训练信号。但由于动态采样的计算密集特性，我们在训练过程中将其关闭。

#### RL训练配置

### RL流水线

图10展示了用于训练Granite 4.1模型的强化学习流水线。通过大量实验探索多种强化学习方案，我们发现这一步骤序列能够在最小化灾难性遗忘的同时，最大化跨多个领域的性能表现。

![Granite 4.1 强化学习流水线](/images/posts/7eab32e56444.png)

图10：Granite 4.1强化学习流水线包含四个连续阶段：多领域RL、RLHF、身份与知识校准RL，以及数学RL。

#### 多领域RL

在此阶段，模型在来自多个领域的统一混合数据上进行联合训练。每次梯度更新都反映了任务的全面多样性，这有助于防止灾难性遗忘、提升整体基准性能，并最小化任何单个任务的性能退化。

本阶段涵盖的不同领域包括：

在此阶段，我们在45,504个独特提示词（取所有Granite 4.1模型的平均值）上训练模型，发现学习率为5e-7、KL损失系数（$\beta$）为0.05时，多领域强化学习效果最佳。

为进一步提升模型的有用性和对话能力，我们使用多语言标量奖励模型在通用对话提示词上训练模型。通过这一阶段，我们观察到Alpaca-Eval相比SFT检查点平均提升约**18.9分**（取三个Granite 4.1模型的平均值）。

为减轻策略偏离先前所学知识，我们在本阶段采用保守的学习率3e-7和更高的KL损失系数$\beta$为0.09。在此RLHF阶段，我们平均使用17,920个独特提示词。

#### 身份与知识校准RL

在此阶段，我们在身份和知识校准提示词上对模型进行少量步骤（约40个训练步骤）的训练。我们观察到，这一小型训练阶段显著提升了模型的自我识别能力。

与RLHF阶段类似，我们使用学习率3e-7和KL损失系数$\beta$为0.09，并在本阶段使用1,728个独特提示词。

#### 数学RL

在RL训练过程中，我们发现RLHF阶段导致数学基准分数下降（例如在GSM8K、DeepMind-Math上）。数学RL阶段使模型能够从这一下降中恢复，并在数学基准上超越原始SFT性能：GSM8K平均提升约**3.8分**，DeepMind-Math平均提升约**23.48分**。本阶段平均使用13,504个独特提示词，与多领域RL阶段类似，我们使用学习率5e-7和KL损失系数$\beta$为0.05。

## 结果

### 基础模型基准

### 指令模型基准

支持语言：英语、德语、西班牙语、法语、日语、葡萄牙语、阿拉伯语、捷克语、意大利语、韩语、荷兰语和中文。

### Granite 4.1与领先开源模型对比

Granite 4.1在不依赖长思维链的情况下，提供了具有竞争力的指令遵循和工具调用能力。通过避免扩展推理过程，它提供了可预测的延迟、稳定的Token使用量和更低的运营成本。这使得Granite 4.1成为企业工作负载中一个生产就绪、开源的选择，尤其适用于对效率、可靠性和成本控制要求严苛的场景。

![BFCL V3](/images/posts/6e5d04679a48.png)

![IFEval](/images/posts/623ad24d464e.png)

### Granite 4.1-8B vs. Granite 4.0-H-Small (32B-A9B)

一个引人注目的结果：Granite 4.1-8B密集模型**持续匹配或超越**上一代Granite 4.0-H-Small（一个拥有9B活跃参数的32B参数混合专家模型）。

![Granite 4.1-8B vs Granite 4.0-H-Small对比](/images/posts/33890b2d0b65.png)

图13：Granite 4.1-8B（深蓝色）与Granite 4.0-H-Small 32B-A9B（浅蓝色）在各项基准上的对比。8B密集模型在IFEval、AlpacaEval、MMLU-Pro、BBH、GSM8K、DeepMind-Math、Evalplus、ArenaHard、BFCL V3和MBPP(+)上匹配或超越更大的MoE模型。

### Granite 4.1模型家族对比

![Granite 4.1模型家族对比](/images/posts/36fa363ae0a6.png)

图14：Granite 4.1家族——30B、8B和3B模型的对比。分数随模型规模呈可预测的递增趋势，30B模型在所有基准上均领先。

## FP8量化

我们还发布了Granite 4.1模型的fp8量化版本，针对vLLM推理进行了优化。精度从16位降至8位，导致磁盘占用和GPU内存使用均减少约50%。量化仅应用于Transformer块内线性算子的权重和激活值（使用LLM Compressor），而所有其他层保持原始精度。

## 基础设施

我们在托管于CoreWeave的**NVIDIA GB200 NVL72集群**上训练了Granite 4.1语言模型：

- 机架内通信：72-GPU NVLink域
- 机架间通信：无阻塞、全胖树NDR 400 Gb/s InfiniBand网络
- 规模：集群内数千个GPU

该基础设施提供了可扩展的高带宽互连，满足所需Token量级（仅预训练阶段就超过15T Token）的高效分布式训练需求。

## 快速开始

Granite 4.1模型在**Apache 2.0许可证**下提供。以下是使用30B指令模型并包含工具调用示例的快速入门方法：

```bash
pip install torch torchvision torchaudio
pip install accelerate
pip install transformers

```

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"
model_path = "ibm-granite/granite-4.1-30b"
tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForCausalLM.from_pretrained(model_path, device_map=device)
model.eval()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的当前天气。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


chat = [
    { "role": "user", "content": "伦敦现在的天气怎么样？" },
]
chat = tokenizer.apply_chat_template(chat, \
                                     tokenize=False, \
                                     tools=tools, \
                                     add_generation_prompt=True)

input_tokens = tokenizer(chat, return_tensors="pt").to(device)

output = model.generate(**input_tokens, 
                        max_new_tokens=100)

output = tokenizer.batch_decode(output)

print(output[0])

```

预期输出：

```
<|start_of_role|>system<|end_of_role|>你是一个有帮助的助手，可以访问以下工具。你可以调用一个或多个工具来协助用户查询。

你在 `<tools></tools>` XML 标签内提供了函数签名：

<tools>
{"type": "function", "function": {"name": "get_current_weather", "description": "获取指定城市的当前天气。", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "城市名称"}}, "required": ["city"]}}}
</tools>

对于每个工具调用，请在 `<tool_call></tool_call>` XML 标签内返回一个包含函数名称和参数的 JSON 对象：

<tool_call>
{"name": <函数名称>, "arguments": <参数JSON对象>}
</tool_call>。如果提供的工具列表中不存在某个工具，请通知用户你无法满足该请求。<|end_of_text|>
<|start_of_role|>用户<|end_of_role|>伦敦现在的天气怎么样？<|end_of_text|>
<|start_of_role|>助手<|end_of_role|><tool_call>
{"name": "get_current_weather", "arguments": {"city": "London"}}
</tool_call><|end_of_text|>

```

资源：

- Granite 4.1 HF 集合
- PRISM：揭秘中期训练中的留存与交互
- GitHub：ibm-granite/granite-4.1-language-models
- Granite 文档
- Granite 社区资源

Granite 4.1 标志着高质量开源语言模型迈出了重要一步。通过在每一个阶段——从预训练数据筛选到监督微调再到多阶段强化学习——优先保证数据质量和严谨性，我们交付了一条显著改进的后训练流程。其结果是更强的指令遵循、工具使用和对话性能，表明经过精心训练的密集 8B 模型能够与规模大得多的 MoE 架构相抗衡。我们期待看到社区如何采用并基于这些模型进行构建。

---

> 本文由AI自动翻译，原文链接：[Granite 4.1 LLMs: How They’re Built](https://huggingface.co/blog/ibm-granite/granite-4-1)
> 
> 翻译时间：2026-04-30 05:30
