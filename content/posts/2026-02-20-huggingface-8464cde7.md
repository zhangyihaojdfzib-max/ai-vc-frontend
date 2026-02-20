---
title: 免费使用Unsloth与Hugging Face Jobs高效微调小型AI模型
title_original: Train AI models with Unsloth and Hugging Face Jobs for FREE
date: '2026-02-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/unsloth-jobs
author: ''
summary: 本文介绍了如何利用Unsloth和Hugging Face Jobs免费微调小型语言模型（如LFM2.5-1.2B-Instruct）。Unsloth能提升约2倍训练速度并减少60%显存占用，大幅降低训练成本。文章详细说明了通过Hugging
  Face Jobs提交训练任务的具体步骤，并指导用户如何为Claude Code、Codex等编码智能体安装模型训练技能，使AI模型微调过程更加高效便捷。
categories:
- AI基础设施
tags:
- 模型微调
- Hugging Face
- Unsloth
- AI训练
- 低成本AI
draft: false
translated_at: '2026-02-20T04:34:59.240136'
---

# 免费使用 Unsloth 和 Hugging Face Jobs 训练 AI 模型

这篇博客文章介绍了如何通过 Claude Code 和 Codex 等编码 Agent（智能体），使用 Unsloth 和 Hugging Face Jobs 来快速进行 LLM（大语言模型）微调（具体针对 LiquidAI/LFM2.5-1.2B-Instruct）。与标准方法相比，Unsloth 提供了约 2 倍的训练速度和约 60% 的 VRAM 使用量减少，因此训练小型模型的成本可能只需几美元。

为什么选择小型模型？像 LFM2.5-1.2B-Instruct 这样的小型语言模型是微调的理想选择。它们训练成本低，迭代速度快，并且在特定任务上正变得与大型模型越来越有竞争力。LFM2.5-1.2B-Instruct 运行所需内存低于 1GB，并针对设备端部署进行了优化，因此您微调后的模型可以在 CPU、手机和笔记本电脑上运行。

![观看视频](/images/posts/fff71851b29b.png)

## 您需要准备

我们正在赠送免费额度，用于在 Hugging Face Jobs 上微调模型。加入 Unsloth Jobs Explorers 组织以领取您的免费额度和一个月的 Pro 订阅。

- 一个 Hugging Face 账户（使用 HF Jobs 必需）
- 账单设置（用于验证，您可以在您的账单页面监控使用情况和管理账单）
- 一个具有写入权限的 Hugging Face Token
- （可选）一个编码 Agent（智能体）（Open Code、Claude Code 或 Codex）

## 运行任务

如果您想使用 HF Jobs 和 Unsloth 训练模型，可以简单地使用 `hf jobs` CLI 来提交任务。

首先，您需要安装 `hf` CLI。您可以通过运行以下命令来完成：

```
# mac or linux
curl -LsSf https://hf.co/cli/install.sh | bash

```

接下来，您可以运行以下命令来提交任务：

```sh
hf jobs uv run https://huggingface.co/datasets/unsloth/jobs/resolve/main/sft-lfm2.5.py \
    --flavor a10g-small  \
    --secrets HF_TOKEN  \
    --timeout 4h \
    --dataset mlabonne/FineTome-100k \
    --num-epochs 1 \
    --eval-split 0.2 \
    --output-repo your-username/lfm-finetuned

```

查看训练脚本和 Hugging Face Jobs 文档以获取更多详情。

## 安装技能

Hugging Face 模型训练技能通过简单的提示词降低了训练模型的门槛。首先，使用您的编码 Agent（智能体）安装该技能。

### Claude Code

Claude Code 通过其插件系统发现技能，因此我们需要先安装 Hugging Face 技能。操作如下：

1.  添加市场：

```text
/plugin marketplace add huggingface/skills

```

1.  在 Discover 标签页中浏览可用技能：

1.  安装模型训练器技能：

```text
/plugin install hugging-face-model-trainer@huggingface-skills

```

更多详情，请参阅关于使用技能中心的文档或 Claude Code 技能文档。

### Codex

Codex 通过 AGENTS.md 文件和 `.agents/skills/` 目录发现技能。

使用 `$skill-installer` 安装单个技能：

```text
$skill-installer install https://github.com/huggingface/skills/tree/main/skills/hugging-face-model-trainer

```

更多详情，请参阅 Codex 技能文档和 AGENTS.md 指南。

### 其他方式

一个通用的安装方法就是克隆技能仓库并将技能复制到您的 Agent（智能体）的技能目录。

```text
git clone https://github.com/huggingface/skills.git
mkdir -p ~/.agents/skills && cp -R skills/skills/hugging-face-model-trainer ~/.agents/skills/

```

## 快速开始

技能安装完成后，请您的编码 Agent（智能体）训练一个模型：

```text
在 HF Jobs 上使用 Unsloth 训练 LiquidAI/LFM2.5-1.2B-Instruct，数据集为 mlabonne/FineTome-100k

```

Agent（智能体）将根据技能中的一个示例生成训练脚本，将训练任务提交到 HF Jobs，并通过 Trackio 提供一个监控链接。

## 工作原理

训练任务在 Hugging Face Jobs（完全托管的云端 GPU）上运行。Agent（智能体）会：

1.  生成一个带有内联依赖项的 UV 脚本
2.  通过 `hf` CLI 将其提交到 HF Jobs
3.  报告任务 ID 和监控 URL
4.  将训练好的模型推送到您的 Hugging Face Hub 仓库

### 示例训练脚本

该技能会根据技能中的示例生成类似以下的脚本。

```python




from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

model, tokenizer = FastLanguageModel.from_pretrained(
    "LiquidAI/LFM2.5-1.2B-Instruct",
    load_in_4bit=True,
    max_seq_length=2048,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    lora_dropout=0,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "out_proj",
        "in_proj",
        "w1",
        "w2",
        "w3",
    ],
)

dataset = load_dataset("trl-lib/Capybara", split="train")

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="./output",
        push_to_hub=True,
        hub_model_id="username/my-model",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        report_to="trackio",
    ),
)

trainer.train()
trainer.push_to_hub()

```

有关 Hugging Face Spaces 定价的完整概述，请查看此处的指南。

## 使用编码 Agent（智能体）的技巧

-   明确指定要使用的模型和数据集，并包含 Hub ID（例如，`Qwen/Qwen2.5-0.5B` 和 `trl-lib/Capybara`）。Agent（智能体）将搜索并验证这些组合。
-   如果您想使用 Unsloth，请明确提及。否则，Agent（智能体）将根据模型和预算选择一个框架。
-   在启动大型任务之前询问成本估算。
-   请求 Trackio 监控以获取实时损失曲线。
-   提交任务后，通过要求 Agent（智能体）检查日志来查看任务状态。

## 资源

-   Hugging Face 技能仓库
-   Unsloth Jobs Explorers 免费额度
-   Hugging Face Jobs 上的 Unsloth 教程
-   Unsloth Jobs 脚本示例

---

> 本文由AI自动翻译，原文链接：[Train AI models with Unsloth and Hugging Face Jobs for FREE](https://huggingface.co/blog/unsloth-jobs)
> 
> 翻译时间：2026-02-20 04:34
