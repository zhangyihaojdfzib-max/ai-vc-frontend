---
title: Codex开源AI模型，集成Hugging Face技能实现自动化训练
title_original: Codex is Open Sourcing AI models
date: '2025-12-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-skills-training-codex
author: null
summary: Codex正在开源AI模型，并集成Hugging Face技能仓库，使编码智能体能够自动化执行机器学习任务。通过HF技能，Codex可以微调大语言模型、监控训练指标、评估检查点、创建报告、量化模型并发布到Hub。文章详细介绍了如何设置环境、安装Codex和HF技能，并展示了端到端机器学习实验的自动化流程，支持从0.5B到7B参数的模型训练，适用于监督微调、直接偏好优化和强化学习等生产级方法。
categories:
- AI产品
tags:
- Codex
- Hugging Face
- AI模型训练
- 自动化机器学习
- 开源AI
draft: false
translated_at: '2026-01-06T01:00:44.769Z'
---

Codex 正在开源 AI 模型
基于我们让 Claude Code 训练开源模型的工作，我们现在正推动 Codex 更进一步。我们让 Codex 能够访问 Hugging Face Skills 仓库，该仓库包含用于机器学习和 AI 任务的技能，例如训练或评估模型。借助 HF 技能，一个编码智能体可以：
*   对大语言模型进行微调并应用 RL 对齐
*   审查、解释来自 Trackio 的实时训练指标并据此采取行动
*   评估检查点并根据评估结果采取行动
*   根据实验创建报告
*   导出模型并使用 GGUF 进行量化以供本地部署
*   将模型发布到 Hub

本教程将更深入地探讨，向您展示其工作原理以及如何自己使用它。那么，让我们开始吧。

Codex 使用 `AGENTS.md` 文件来完成专门任务，而 Claude Code 使用“技能”。幸运的是，“HF 技能”与这两种方法都兼容，并且适用于主要的编码智能体，如 Claude Code、Codex 或 Gemini CLI。

借助 HF 技能，您可以向 Codex 发出如下指令：
```
在数据集 open-r1/codeforces-cots 上微调 Qwen3-0.6B
```
而 Codex 将会：
*   验证您的数据集格式
*   选择合适的硬件（对于 0.6B 模型使用 t4-small）
*   使用并更新带有 Trackio 监控的训练脚本
*   将任务提交到 Hugging Face Jobs
*   报告任务 ID 和预估成本
*   在您询问时检查进度
*   在出现问题时帮助您调试

模型在 Hugging Face 的 GPU 上进行训练，而您可以处理其他事情。完成后，您微调好的模型会出现在 Hub 上，随时可以使用。

这不是一个玩具演示。该扩展支持生产中使用的相同训练方法：监督微调、直接偏好优化以及带有可验证奖励的强化学习。您可以训练参数从 0.5B 到 7B 的模型，将其转换为 GGUF 格式以进行本地部署，并运行结合了不同技术的多阶段流水线。

**目标：端到端的机器学习实验**
我们在 Claude Code 教程中探索了这种单一提示词方法。然而，我们现在可以更进一步，让 OpenAI Codex 进行端到端的机器学习实验。例如，Codex 应该能够监控进度、评估模型并维护最新的训练报告。这将使工程师能够将实验委托给 Codex，并以一种更放手的方式审查报告。这也将使 Codex 能够根据训练报告和评估结果自行做出更多决策。

那么，让我们开始吧！

**设置与安装**
开始之前，您需要：
*   一个具有 Pro 或 Team / Enterprise 计划的 Hugging Face 账户（使用 Jobs 需要付费计划）
*   一个来自 huggingface.co/settings/tokens 的具有写入权限的 Token
*   已安装并配置好 Codex

**安装 Codex**
Codex 是 OpenAI 的 AI 编码智能体，包含在 ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划中。Codex 将 AI 辅助直接带入您的开发工作流程。
有关安装和设置说明，请参阅 Codex 文档。

**安装 Hugging Face 技能**
Hugging Face 技能仓库包含一个 `AGENTS.md` 文件，Codex 会自动检测并使用它。
克隆仓库：
```
git clone https://github.com/huggingface/skills.git
cd skills
```
Codex 将自动检测仓库中的 `AGENTS.md` 文件并加载技能。您可以通过以下命令验证指令是否已加载：
```
codex --ask-for-approval never "Summarize the current instructions."
```
更多详情请参阅 Codex AGENTS 指南。

**连接到 Hugging Face**
使用 `hf auth login` 命令和来自 hf.co/settings/tokens 的具有写入权限的 Token 向 Hugging Face 进行身份验证：
```
hf auth login
```
Codex 支持 MCP（模型上下文协议）服务器。您可以配置 Hugging Face MCP 服务器以获得额外的 Hub 集成功能。您可以通过将以下内容添加到您的 `~/.codex/config.toml` 文件中，将 Hugging Face MCP 服务器添加到您的 Codex 配置中：
```
[mcp_servers.huggingface]
command = "npx"
args = ["-y", "mcp-remote", "https://huggingface.co/mcp?login"]
```
在设置页面配置 Hugging Face MCP 服务器以使用相关的 MCP 服务器，例如 Jobs。
然后启动 Codex，您将被引导至 Hugging Face MCP 身份验证页面。

**您的第一个 AI 实验**
让我们来看一个完整的例子。我们将微调一个小模型以提高代码解决能力，使用 open-r1/codeforces-cots 数据集和 openai_humaneval 基准测试。

`open-r1/codeforces-cots` 数据集是一个包含 Codeforces 问题和解决方案的数据集。它是一个很好的数据集，用于对模型进行指令微调以解决困难的编码问题。

**指示 Codex 进行端到端的微调实验**
在您的项目目录中启动 Codex。然后给它一个简单明了的指令：
```
开始一个新的微调实验，以使用 SFT 提高代码解决能力。
- 为实验维护一份报告。
- 使用 openai_humaneval 基准测试评估模型
- 使用 open-r1/codeforces-cots 数据集
```
您会注意到，我们已经比 Claude Code 教程中的单一提示词方法更进一步。我们在指令中添加了更多细节，同时也为实验添加了更多步骤。
为什么不尝试自己用更开放的问题来迭代这个实验呢？例如“什么模型最适合代码解决能力？”或“什么数据集最适合代码解决能力？”

Codex 分析您的请求并准备训练配置。对于演示数据集上的 0.6B 模型，它选择了 `t4-small` —— 对于这个模型大小来说足够的 GPU，并且是最便宜的可用选项。Codex 将在 `training_reports/<model>-<dataset>-<method>.md` 处开始一份新的报告，如下例所示。随着实验的进行，Codex 将用最新信息和每次运行报告来更新报告。

**示例训练报告**
```
# Base Model & Dataset
[Base Model](https://huggingface.co/Qwen/Qwen3-0.6B)
[Dataset](https://huggingface.co/datasets/open-r1/codeforces-cots)
# `sft-a10g` - `TBD` - `In Progress`
## Training Parameters
| Parameter | Value |
|-----------|-------|
| Method | SFT (TRL) |
| Model | `Qwen/Qwen3-0.6B` |
| Dataset | `open-r1/codeforces-cots` (train, 5% eval split) |
| Max Length | 2048 |
| Epochs | 1 (extend to 3 after first check) |
| Per-Device Batch Size | 1 |
| Grad Accum Steps | 8 |
| Effective Batch | 8 |
| Learning Rate | 5e-5 |
| Weight Decay | 0.01 |
| Warmup Ratio | 0.03 |
| Eval Strategy | steps (500) |
| Save Strategy | steps (500), `hub_strategy=every_save`, limit=2 |
| Precision | bf16 |
| Gradient Checkpointing | true |
| Packing | false |
| Hub Model | `burtenshaw/qwen3-codeforces-cots-sft` |
| Hardware | a10g-small |
| Timeout | 2h |
| Trackio | project `qwen3-codeforces-cots`, run `sft-a10g` |
## Run Status
In Progress (queued to submit)
## Run Logs
Pending submission (job link will be added)
## Trackio Logs
Pending (will link after job starts)
## Run Evaluations
Pending (lighteval `openai_humaneval` for base + checkpoints)
# Experiment Evaluations
| Run Title | Benchmark | Score | Evaluation Job Link | Model Link |
|-----------|-----------|-------|---------------------|------------|
| `sft-a10g` - `TBD` - `In Progress` | HumanEval pass@1 | TBD | TBD | [burtenshaw/qwen3-codeforces-cots-sft](https://huggingface.co/burtenshaw/qwen3-codeforces-cots-sft)
```

**更新训练报告**
随着实验的进行，Codex 将用最新信息和每次运行报告来更新报告。

您可以在 `training_reports/<model>-<dataset>-<method>.md` 文件中查看报告。
例如，当实验进行中时，codex 会将报告标题更新为 sft-a10g
- TBD
- 进行中
# `base-humaneval-a10g` - `2025-12-09 13:47:47 UTC` - `进行中`
它可以链接到运行日志和 trackio 日志。
## 运行日志
[运行日志](https://huggingface.co/jobs/burtenshaw/6938272ec67c9f186cfe1ae3)
## Trackio 日志
[Trackio 日志](https://burtenshaw-trackio.hf.space/?project=qwen3-codeforces-sft&metrics=train/loss&runs=sft-qwen3-codeforces-20251209-175806&sidebar=hidden&navbar=hidden)
并且它会在一个合并的表格中更新评估结果。
# 实验评估
| 运行标题 | 基准测试 | 分数 | 评估任务链接 | 模型链接 |
| `base-humaneval-a10g` - `2025-12-09 13:47:47 UTC` - `已完成` | HumanEval pass@1 | 0.304 | [日志](https://huggingface.co/jobs/burtenshaw/69382863c67c9f186cfe1ae7) | [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) |
| `qwen3-0.6b-lora-v1` - `2025-12-09 13:47:47 UTC` - `进行中` | HumanEval pass@1 | TBD | TBD | [burtenshaw/qwen3-codeforces-cots-sft](https://huggingface.co/burtenshaw/qwen3-codeforces-cots-sft)
数据集验证
数据集格式和处理是训练失败最常见的原因，通常训练脚本中需要完成大量工作。Codex 可以在任务开始前验证数据集，并定义 TRL 的配置或单独处理数据集。
在大多数情况下，Codex 会在训练前验证数据集，但您始终可以在提交任务前检查数据集验证。
检查 open-r1/codeforces-cots 是否适用于 SFT 训练。
Codex 在 CPU 上运行快速检查（成本极低）并报告：
数据集验证 my-org/conversation-data：
SFT：✓ 就绪
找到包含对话格式的 'messages' 列
DPO：✗ 不兼容
缺少 'chosen' 和 'rejected' 列
如果您的数据集需要转换，Codex 可以在训练前预处理数据集。
预处理数据集 open-r1/codeforces-cots，使用 'good_response' 和 'bad_response' 代替 'chosen' 和 'rejected'。
Codex 将预处理数据集，并使用新配置更新训练脚本。
提交前审查
在 Codex 提交任何内容之前，您会看到配置：
我将使用 SFT 方法在 open-r1/codeforces-cots 上微调 Qwen/Qwen3-0.6B。
配置：
- 硬件：t4-small（约 0.75 美元/小时）
- 预计时间：约 20 分钟
- 预计成本：约 0.30 美元
- 输出：username/qwen-codeforces-cots-sft
模型将自动推送到 Hub。我应该提交吗？
这是您调整任何内容的机会。更改输出仓库名称、选择不同的硬件，或要求 Codex 修改训练参数。一旦您批准，任务就会被提交。
例如，您可以要求 Codex 尝试一个测试运行：
在 100 个样本上进行快速测试运行。
使用训练报告跟踪进度
提交后，您可以使用训练报告跟踪进度，并获取运行日志和 trackio 日志的链接。您还可以告诉 Codex 获取日志、总结进度并更新训练报告。随着 codex 运行任务，它将用最新信息更新训练报告。
Codex 响应示例
─ 已运行 10m 38s ─────────────────────────────────────────────────────────────────────────────────────────────────────────
• 训练和评估任务已启动。关键细节：
- 在 open-r1/codeforces-cots（solutions_py_decontaminated，98/2 分割）上启动 SFT，使用 LoRA 微调 Qwen/Qwen3-0.6B，硬件 a10g-large，bf16，max_steps=1000，batch=1，grad_accum=8，lr=2e-5，每 200 步保存/评估一次，推送至 Hub 仓库 burtenshaw/qwen3-codeforces-cots-sft。任务：https://huggingface.co/jobs/burtenshaw/6938272ec67c9f186cfe1ae3（Trackio 项目 codeforces-cots-sft，运行 qwen3-0.6b-lora-v1）。
- 在基础模型上排队的基线 lighteval（HumanEval）任务，硬件 a10g-large。任务：https://huggingface.co/jobs/
- 实验报告已更新当前运行和链接：training_reports/qwen3-codeforces-cots-sft.md。
一旦 SFT 任务将微调后的检查点推送到 hub，要评估它们，请重用相同的 lighteval 脚本：
hf jobs uv run --flavor a10g-large --timeout 1h --secrets HF_TOKEN -e MODEL_ID=burtenshaw/qwen3-codeforces-cots-sft -e
RESULTS_ORG=burtenshaw -d /tmp/lighteval_humaneval.py
（或将 MODEL_ID 替换为特定的检查点路径）。这将把结果记录到 hub 上相同的结果目录。
1. 监控两个正在运行的任务；我可以根据请求获取日志或指标。
2. 检查点落地后，触发上述 lighteval 运行以与基线进行比较；然后我们可以在报告中填写 pass@1。
Trackio 将通过运行评估任务并选择最佳检查点来为您监控训练和评估分数。如果您想知道训练任务的状态，可以要求 Codex 获取日志并在表格中总结进度。
模型是否优于基础模型？
| 模型 | 基准测试 | 分数 | 评估任务链接 | 模型链接 |
| `qwen3-0.6b-lora-v1` - `2025-12-09 13:47:47 UTC` - `已完成` | HumanEval pass@1 | 0.342 | [日志](<训练任务链接>) | [burtenshaw/qwen3-codeforces-cots-sft](https://huggingface.co/burtenshaw/qwen3-codeforces-cots-sft)
| `base-humaneval-a10g` - `2025-12-09 13:47:47 UTC` - `已完成` | HumanEval pass@1 | 0.306 | [日志](<评估任务链接>) | [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)
您还可以实时监控训练损失。
Codex 获取日志并总结进度。
点击此处查看包含一些已完成运行的 Trackio 仪表板示例。
使用您的模型
训练完成后，您的模型就在 Hub 上：
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("burtenshaw/qwen3-codeforces-cots-sft")
tokenizer = AutoTokenizer.from_pretrained("burtenshaw/qwen3-codeforces-cots-sft")
Transformers 作为标准库非常出色，我们可以轻松地将训练好的模型转换为 GGUF 以进行本地部署。这是因为训练技能包含了将模型转换为 GGUF 的说明和支持脚本。
将我的微调模型转换为 GGUF，使用 Q4_K_M 量化。
推送到 username/my-model-gguf。
然后 Codex 会转换为 GGUF，应用量化，并推送到 Hub。如果我们训练了 LoRA 适配器，它会将 LoRA 适配器合并到基础模型中。
然后在本地使用它：
llama-server -hf <username>/<model-name>:<quantization>
# 例如，在本地机器上运行 Qwen3-1.7B-GGUF 模型：
llama-server -hf unsloth/Qwen3-1.7B-GGUF:Q4_K_M
硬件与成本
Codex 会根据您的模型大小选择硬件，但了解权衡有助于您做出更好的决策。您可以使用硬件指南查看硬件选项和成本，但 codex 会为您完成并选择最佳选项。
对于参数小于 1B 的微型模型，t4-small
效果很好。这些模型训练速度快——完整运行预计花费 1-2 美元。这非常适合教育或实验性运行。
对于小型模型（1-3B），升级到 t4-medium
或 a10g-small
。训练需要几个小时，成本为 5-15 美元。
对于中型模型（3-7B），您需要 a10g-large
或 a100-large
配合 LoRA。完全微调不适合，但 LoRA 使这些模型非常易于训练。生产环境预算为 15-40 美元。
对于大型模型（7B+），此 HF 技能任务目前尚不适合此规模。但请保持关注，因为我们正在努力！
下一步
我们已经展示了 Codex 可以处理模型微调的完整生命周期：验证数据、选择硬件、生成脚本、提交任务、监控进度以及转换输出。
可以尝试的一些事情：
- 在您自己的数据集上微调一个模型
- 使用更多模型和数据集进行更大的实验，并让 Agent（智能体）为您创建报告。
- 使用 GRPO 在数学或代码上训练一个推理模型，并让 Agent（智能体）为您创建报告。
该扩展是开源的。

您可以扩展它，为您的流程进行定制，或将其作为其他训练场景的起点。

资源
Codex
- Codex 文档 — OpenAI 的 AI 编程 Agent（智能体）
- Codex 快速入门 — 开始使用 Codex
- Codex AGENTS 指南 — 使用 AGENTS.md 文件

Hugging Face Skills
- SKILL.md — 完整的技能文档
- 训练方法 — 详解 SFT、DPO、GRPO
- 硬件指南 — GPU 选择与成本
- TRL 文档 — 底层训练库
- Hugging Face Jobs — 云端训练基础设施
- Trackio — 实时训练监控。


> 本文由AI自动翻译，原文链接：[Codex is Open Sourcing AI models](https://huggingface.co/blog/hf-skills-training-codex)
> 
> 翻译时间：2026-01-06 01:00
