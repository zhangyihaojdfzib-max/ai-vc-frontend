---
title: Claude微调开源大模型：Hugging Face技能实战指南
title_original: We Got Claude to Fine-Tune an Open Source LLM
date: '2025-12-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-skills-training
author: null
summary: 本文介绍了如何利用Claude Code通过Hugging Face Skills工具微调开源大语言模型的全过程。该技能不仅能让Claude编写训练脚本，还能直接向云端GPU提交任务、监控进度并将训练好的模型推送至Hugging
  Face Hub。文章详细说明了设置步骤，包括账户准备、技能安装、身份验证配置，并以微调Qwen3-0.6B模型为例展示了从指令下发到模型部署的完整工作流程。该方法支持生产级训练技术，适用于0.5B到70B参数规模的模型。
categories:
- AI基础设施
tags:
- Claude
- 大语言模型微调
- Hugging Face
- AI工具链
- 云端训练
draft: false
---

我们让Claude微调了一个开源LLM
我们赋予Claude使用名为Hugging Face Skills的新工具来微调语言模型的能力。不仅仅是编写训练脚本，还能实际向云端GPU提交任务、监控进度，并将训练完成的模型推送到Hugging Face Hub。本教程将展示其工作原理以及如何自行使用。

Claude Code可以使用“技能”——即打包的指令、脚本和领域知识——来完成专门任务。`hf-llm-trainer`技能教会了Claude关于训练所需了解的一切：根据模型规模选择GPU、如何配置Hub身份验证、何时使用LoRA而非全量微调，以及如何处理成功运行训练所需做出的数十项其他决策。

借助此技能，您可以这样指示Claude：
在数据集open-r1/codeforces-cots上微调Qwen3-0.6B

而Claude将：
- 验证您的数据集格式
- 选择合适的硬件（对于0.6B模型选择t4-small）
- 使用并更新带有Trackio监控的训练脚本
- 将任务提交到Hugging Face Jobs
- 报告任务ID和预估成本
- 在您询问时检查进度
- 如果出现问题，帮助您调试

当您处理其他事务时，模型在Hugging Face的GPU上进行训练。完成后，您微调好的模型会出现在Hub上，随时可用。

这不是一个玩具演示。该技能支持生产环境中使用的相同训练方法：监督微调、直接偏好优化以及带有可验证奖励的强化学习。您可以训练参数量从0.5B到70B的模型，将其转换为GGUF格式以便本地部署，并运行结合不同技术的多阶段流水线。

**设置与安装**
开始前，您需要：
- 一个拥有Pro或Team/Enterprise计划的Hugging Face账户（Jobs需要付费计划）
- 来自huggingface.co/settings/tokens的具有写入权限的token
- 一个编码智能体，如Claude Code、OpenAI Codex或Google的Gemini CLI

Hugging Face技能兼容Claude Code、Codex和Gemini CLI。与Cursor、Windsurf和Continue的集成正在开发中。

**Claude Code**
- 将仓库注册为市场插件：
`/plugin marketplace add huggingface/skills`
- 安装技能，运行：
`/plugin install <skill-folder>@huggingface-skills`
例如：
`/plugin install hf-llm-trainer@huggingface-skills`

**Codex**
- Codex将通过`AGENTS.md`文件识别技能。您可以通过以下命令验证指令是否已加载：
`codex --ask-for-approval never "Summarize the current instructions."`
- 更多详情，请参阅Codex AGENTS指南。

**Gemini CLI**
此仓库包含`gemini-extension.json`以便与Gemini CLI集成。
本地安装：
`gemini extensions install . --consent`
或使用GitHub URL：
`gemini extensions install https://github.com/huggingface/skills.git --consent`
- 更多帮助，请参阅Gemini CLI扩展文档。

**连接到Hugging Face**
您必须使用具有写入权限的token对您的Hugging Face账户进行身份验证，以便任务能够创建模型仓库。

设置您的token：
`hf auth login`
# 或
`export HF_TOKEN=hf_your_write_access_token_here`

通过将您的写入token发送到`HF_TOKEN`或`Authorization: Bearer` HTTP头部，来配置Hugging Face MCP服务器以使用它。
对于Claude Code：
`claude mcp add --transport http hf-skills https://huggingface.co/mcp?bouquet=skills --header "Authorization: Bearer $HF_TOKEN"`

**您的首次训练运行**
让我们通过一个完整示例来了解整个过程。我们将微调一个小模型以查看完整工作流程，然后探索更高级的功能。

**指示编码智能体进行微调**
从一个简单清晰的指令开始，以微调特定模型：
在open-r1/codeforces-cots数据集上微调Qwen3-0.6B，用于指令跟随。

编码智能体分析您的请求并准备训练配置。对于一个演示数据集上的0.6B模型，它选择t4-small——足够支持此模型规模且是最便宜的可用选项。

`open-r1/codeforces-cots`数据集是一个包含Codeforces问题及其解决方案的数据集。它是一个很好的数据集，用于对模型进行指令调优以解决困难的编码问题。

这也适用于视觉语言模型！您可以简单地运行“在llava-instruct-mix上微调Qwen/Qwen3-VL-2B-Instruct”。

**提交前审查**
在您的编码智能体提交任何内容之前，您会看到配置：
我将在open-r1/codeforces-cots上使用SFT微调Qwen/Qwen3-0.6B。
配置：
- 硬件：t4-small（约0.75美元/小时）
- 预计时间：约20分钟
- 预估成本：约0.30美元
- 输出：username/qwen-codeforces-cots-sft

模型将自动推送到Hub。我应该提交吗？

这是您调整任何内容的机会。更改输出仓库名称、选择不同的硬件，或要求Claude修改训练参数。一旦您批准，智能体就会提交任务。

例如，您可以要求智能体尝试一个测试运行：
在100个样本上做一个快速测试运行。

**跟踪进度**
提交后，您会获得任务详情：
✅ 任务提交成功！
任务ID：abc123xyz
监控：https://huggingface.co/jobs/username/abc123xyz
预计时间：约20分钟
预估成本：约0.30美元
查看实时指标：https://huggingface.co/spaces/username/trackio

该技能集成了Trackio，因此您可以实时观看训练损失下降。任务异步运行，因此您可以关闭终端稍后再回来。当您想了解更新时：
我的训练任务进展如何？

然后智能体会获取日志并总结进度。

**使用您的模型**
训练完成后，您的模型就在Hub上了：
```
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("username/qwen-codeforces-cots-sft")
tokenizer = AutoTokenizer.from_pretrained("username/qwen-codeforces-cots-sft")
```

这就是完整的循环。您用简单的英语描述了您想要什么，智能体处理了GPU选择、脚本生成、任务提交、身份验证和持久化。整个过程花费了大约三十美分。

**训练方法**
该技能支持三种训练方法。了解何时使用每种方法有助于您获得更好的结果。

**监督微调**
SFT是大多数项目的起点。您提供演示数据——输入和期望输出的示例——训练调整模型以匹配这些模式。

当您拥有所需行为的高质量示例时，使用SFT。客户支持对话、代码生成对、特定领域问答——任何您可以向模型展示“好”是什么样子的场景。
在my-org/support-conversations上微调Qwen3-0.6B，进行3个轮次。

智能体验证数据集，选择硬件（对于7B模型使用带LoRA的a10g-large），并配置带有检查点和监控的训练。

对于参数量大于3B的模型，智能体会自动使用LoRA来减少内存需求。这使得在单个GPU上训练7B或13B模型成为可能，同时保留了全量微调的大部分质量。

**直接偏好优化**
DPO在偏好对上训练——其中一个是“被选中”的响应，另一个是“被拒绝”的响应。这通常在一个初始的SFT阶段之后，将模型输出与人类偏好对齐。

当您拥有人工标注者或自动比较的偏好标注时，使用DPO。DPO直接针对偏好的响应进行优化，无需单独的奖励模型。
在我刚训练的SFT模型上运行DPO，使用my-org/preference-data进行对齐。
该数据集有'chosen'和'rejected'列。

DPO对数据集格式敏感。它要求列名必须恰好是`chosen`和`rejected`，或者有一个包含输入的`prompt`列。智能体会首先验证这一点，并在您的数据集使用不同名称时向您展示如何映射列。

您也可以使用Skills在视觉语言模型上运行DPO！尝试使用openbmb/RLAIF-V-Dataset。

Claude将进行小幅修改，但能成功完成训练。
群体相对策略优化（GRPO）
GRPO是一种强化学习任务，已被证实在可验证任务（如解决数学问题、编写代码或任何具有程序化成功标准的任务）上效果显著。
基于Qwen3-0.6B，在openai/gsm8k数据集上使用GRPO训练数学推理模型。
模型生成响应，根据正确性获得奖励，并从结果中学习。这比SFT或DPO更复杂，但配置方式相似。

硬件与成本
Agent会根据模型规模选择硬件，但了解其中的权衡能帮助您做出更好决策。

模型规模与GPU匹配指南
对于10亿参数以下的微型模型，t4-small
表现良好。这些模型训练速度快——完整训练预计花费1-2美元。非常适合教学或实验性运行。
对于小型模型（1-3B），可升级至t4-medium
或a10g-small
。训练耗时数小时，成本5-15美元。
对于中型模型（3-7B），需要使用a10g-large
或a100-large
配合LoRA。全参数微调不适用，但LoRA使其易于训练。生产环境预算为15-40美元。
对于大型模型（7B+），本HF技能任务不适用。

演示版与生产版
测试工作流时，请从小规模开始：
用my-org/support-conversations数据集的100个示例快速测试运行SFT Qwen-0.6B。
编码Agent会配置最低限度的训练——足以验证流程可行且无实际成本。
对于生产环境，需明确指定：
为生产环境在完整my-org/support-conversations数据集上SFT Qwen-0.6B。
每500步保存检查点，3个训练周期，余弦学习率。
在投入数小时的生产任务前，务必先运行演示版。花费0.50美元发现格式错误的演示，能避免30美元的失败运行。

数据集验证
数据集格式是训练失败的最常见原因。Agent可在您消耗GPU时间前验证数据集。
检查my-org/conversation-data是否适用于SFT训练。
Agent会在CPU上快速检查（成本极低）并报告：
my-org/conversation-data数据集验证结果：
SFT：✓ 就绪
找到符合对话格式的'messages'列
DPO：✗ 不兼容
缺少'chosen'和'rejected'列
若数据集需要转换，Agent会展示方法：
我的DPO数据集使用'good_response'和'bad_response'列
而非'chosen'和'rejected'。如何修复？
Agent提供映射代码，并可将其直接集成到训练脚本中。

训练监控
实时监控有助于及早发现问题。该技能默认配置Trackio——提交任务后，您可在以下地址查看指标：
https://huggingface.co/spaces/username/trackio
此处显示训练损失、学习率和验证指标。正常运行会呈现损失持续下降的趋势。
随时可向Agent查询状态：
我的训练任务状态如何？
任务abc123xyz正在运行（已进行45分钟）
当前步数：850/1200
训练损失：1.23（较初始值2.41↓）
学习率：1.2e-5
预计完成时间：约20分钟
若出现问题，Agent会协助诊断。内存不足？Agent建议减小批处理规模或升级硬件。数据集错误？Agent识别不匹配项。超时？Agent推荐延长时长或加速训练设置。

转换为GGUF格式
训练完成后，您可能希望在本地运行模型。GGUF格式兼容llama.cpp及LM Studio、Ollama等相关工具。
将我的微调模型转换为Q4_K_M量化的GGUF格式。
推送至username/my-model-gguf。
Agent会提交转换任务：合并LoRA适配器、转换为GGUF、应用量化并推送至Hub。
随后在本地使用：
llama-server -hf <username>/<model-name>:<quantization>
# 例如，在本地机器运行Qwen3-1.7B-GGUF模型：
llama-server -hf unsloth/Qwen3-1.7B-GGUF:Q4_K_M

后续步骤
我们已展示如Claude Code、Codex或Gemini CLI等编码Agent能处理模型微调的全生命周期：验证数据、选择硬件、生成脚本、提交任务、监控进度、转换输出。这将原本的专业技能转化为可通过对话完成的工作。

可尝试的方向：
- 在自有数据集上微调模型
- 通过SFT → DPO构建偏好对齐模型
- 使用GRPO训练数学或代码推理模型
- 将模型转换为GGUF格式并用Ollama运行

该技能为开源项目。您可以扩展它、为工作流定制，或将其作为其他训练场景的起点。

资源链接
- SKILL.md —— 完整技能文档
- 训练方法 —— SFT、DPO、GRPO详解
- 硬件指南 —— GPU选择与成本
- TRL文档 —— 底层训练库
- Hugging Face Jobs —— 云端训练基础设施
- Trackio —— 实时训练监控

---

> 本文由AI自动翻译，原文链接：[We Got Claude to Fine-Tune an Open Source LLM](https://huggingface.co/blog/hf-skills-training)
> 
> 翻译时间：2026-01-06 01:01
