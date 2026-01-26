---
title: RapidFire AI 集成 TRL，实现 20 倍速微调实验
title_original: 20x Faster TRL Fine-tuning with RapidFire AI
date: '2025-11-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/rapidfireai
author: null
summary: Hugging Face TRL 正式集成 RapidFire AI，通过创新的自适应分块并发训练技术，允许用户在单个或多个 GPU 上并行比较多种微调配置。该方案将数据集分片并在块边界循环切换配置，实现近乎实时的比较，实验吞吐量提升约16-24倍。用户可通过交互式仪表板实时监控、控制任务（停止、恢复、克隆-修改），并利用即插即用的
  TRL 包装器（RFSFTConfig、RFDPOConfig 等）快速启动实验，无需重大代码改动或额外 GPU 资源。
categories:
- AI基础设施
tags:
- TRL微调
- RapidFire AI
- 并发训练
- 模型优化
- Hugging Face
draft: false
translated_at: '2026-01-06T01:06:11.325Z'
---

**RapidFire AI 实现 20 倍速 TRL 微调**

Hugging Face TRL 现已正式集成 RapidFire AI，以加速您的微调和训练后实验。TRL 用户现在可以探索、安装并运行 RapidFire AI，作为无需重大代码改动、无需增加 GPU 需求即可比较多种微调/训练后配置以定制 LLM 的最快方式。

**为何重要**

在对 LLM 进行微调或训练后处理时，团队通常没有时间和/或预算去比较多种配置，即使这能显著提升评估指标。RapidFire AI 允许您并发启动多个 TRL 配置——甚至在单个 GPU 上——并通过一种新颖的自适应、基于分块的调度与执行方案进行近乎实时的比较。在 TRL 页面引用的内部基准测试中，与顺序逐一比较配置相比，这带来了约 16-24 倍的实验吞吐量提升，使您能够更快地达到更好的指标。

RapidFire AI 在您的 IDE、指标仪表板和多 GPU 执行后端之间建立了实时的三方通信。

**开箱即得的功能**

*   **即插即用的 TRL 包装器** — 使用 `RFSFTConfig`、`RFDPOConfig` 和 `RFGRPOConfig` 作为 TRL 的 SFT/DPO/GRPO 配置的近零代码替代品。
*   **自适应分块并发训练** — RapidFire AI 将数据集分片成指定数量的块，并在块边界处循环切换配置，从而实现更早的同类比较，并最大化 GPU 利用率。
*   **交互式控制操作** — 直接从仪表板，您可以对任何正在运行的任务执行**停止、恢复、删除**和**克隆-修改**（可选择**热启动**），以避免在表现不佳的配置上浪费资源，并加倍投入于表现更好的配置——无需重启任务，无需费力管理单独的 GPU 或集群，没有资源膨胀。

直接从实时仪表板克隆有潜力的配置并修改超参数，可选择从父配置权重进行热启动。

*   **多 GPU 编排** — RapidFire AI 调度器通过高效的共享内存机制，自动将配置放置并编排到可用 GPU 的数据块上。您只需专注于模型和评估指标，无需操心底层架构。
*   **基于 MLflow 的仪表板** — 实验一开始，实时指标、日志和交互式控制操作就集中在一处。即将支持更多仪表板，如 Trackio、W&B 和 TensorBoard。

**工作原理**

RapidFire AI 将您的数据集随机分割成多个"块"，并在块边界处通过 GPU 循环执行不同的 LLM 配置。您能更快地获得所有配置在评估指标上的增量信号。通过高效的基于共享内存的适配器/模型溢出/加载机制实现的自动检查点保存，确保了训练的平稳、稳定和一致。使用交互式控制操作在训练过程中进行调整，及早停止低性能配置，并克隆有潜力的配置并调整其参数，可选择从父配置权重进行热启动。

顺序执行 vs. 任务并行 vs. RapidFire AI：自适应调度器在多个配置和 GPU 间最大化 GPU 利用率。底行展示了交互式控制操作的实际应用——在训练过程中停止、克隆和修改运行任务。

**快速开始**

安装 RapidFire AI 并在一分钟内开始运行：

```bash
pip install rapidfireai
# 使用 Hugging Face 认证
huggingface-cli login --token YOUR_TOKEN
# 当前问题的临时解决方案
pip uninstall -y hf-xet
# 初始化并启动 RapidFire AI
rapidfireai init
rapidfireai start
```

仪表板将在 `http://localhost:3000` 启动，您可以在那里监控和控制所有实验。

**支持的 TRL 训练器**

*   使用 `RFSFTConfig` 进行 SFT
*   使用 `RFDPOConfig` 进行 DPO
*   使用 `RFGRPOConfig` 进行 GRPO

这些设计为即插即用的替代品，因此您可以保持 TRL 的思维模型，同时为您的微调/训练后应用获得更高的并发性和控制力。

**最小 TRL SFT 示例**

以下展示了即使在单个 GPU 上也能并发训练多个配置的样子：

```python
from rapidfireai import Experiment
from rapidfireai.automl import List, RFGridSearch, RFModelConfig, RFLoraConfig, RFSFTConfig
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

# 设置：加载数据集并定义格式化函数
dataset = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")
train_dataset = dataset["train"].select(range(128)).shuffle(seed=42)

def formatting_function(row):
    return {
        "prompt": [
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": row["instruction"]},
        ],
        "completion": [{"role": "assistant", "content": row["response"]}]
    }

dataset = dataset.map(formatting_function)

# 定义要比较的多个配置
config_set = List([
    RFModelConfig(
        model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        peft_config=RFLoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"]),
        training_args=RFSFTConfig(learning_rate=1e-3, max_steps=128, fp16=True),
    ),
    RFModelConfig(
        peft_config=RFLoraConfig(r=32, lora_alpha=64, target_modules=["q_proj", "v_proj"]),
        training_args=RFSFTConfig(learning_rate=1e-4, max_steps=128, fp16=True),
        formatting_func=formatting_function,
    )
])

# 使用基于分块的调度并发运行所有配置
experiment = Experiment(experiment_name="sft-comparison")
config_group = RFGridSearch(configs=config_set, trainer_type="SFT")

def create_model(model_config):
    model = AutoModelForCausalLM.from_pretrained(
        model_config["model_name"],
        device_map="auto", torch_dtype="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_config["model_name"])
    return (model, tokenizer)

experiment.run_fit(config_group, create_model, train_dataset, num_chunks=4, seed=42)
experiment.end()
```

**运行此代码会发生什么？**

假设您在 2-GPU 机器上运行上述代码。两个配置将并发训练，而不是顺序训练（配置 1 → 等待 → 配置 2 → 等待）：

| 方法 | 获得比较性决策的时间 | GPU 利用率 |
|---|---|---|
| 顺序执行（传统） | ~15 分钟 | 60% 利用率 |
| RapidFire AI（并发） | ~5 分钟 | 95%+ 利用率 |

在两个配置都处理完第一个数据块后，您就能在相同资源上提前 3 倍做出比较性决策，而无需等待它们逐一查看整个数据集。打开 `http://localhost:3000` 查看实时指标，并使用交互式控制操作根据您看到的情况实时停止、克隆或调整运行任务。

**基准测试：实际加速效果**

以下是团队从顺序比较切换到启用 RapidFire AI 的超并行实验时，为达到可比的总体最佳训练损失（在所有尝试的配置中）所看到的时间对比：

| 场景 | 顺序执行时间 | RapidFire AI 时间 | 加速比 |
|---|---|---|---|
| 4 个配置，1 GPU | 120 分钟 | 7.5 分钟 | 16× |
| 8 个配置，1 GPU | 240 分钟 | 12 分钟 | 20× |
| 4 个配置，2 GPU | 60 分钟 | 4 分钟 | 15× |

基于 NVIDIA A100 40GB、TinyLlama-1.1B 和 Llama-3.2-1B 模型的基准测试

**立即开始**

🚀 **动手尝试**：[交互式 Colab Notebook](https://colab.research.google.com/drive/1Yl8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l8l


> 本文由AI自动翻译，原文链接：[20x Faster TRL Fine-tuning with RapidFire AI](https://huggingface.co/blog/rapidfireai)
> 
> 翻译时间：2026-01-06 01:06
