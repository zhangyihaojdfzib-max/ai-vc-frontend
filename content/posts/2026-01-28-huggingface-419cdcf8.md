---
title: Claude赋能开源模型：自动生成CUDA内核技能
title_original: We Got Claude to Build CUDA Kernels and teach open models!
date: '2026-01-28'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/upskill
author: ''
summary: 本文介绍了使用Claude Opus 4.5生成CUDA内核编写技能，并通过upskill工具将该技能迁移到更小开源模型的方法。文章展示了如何通过记录专家模型交互过程创建可复用的Agent技能文件，并评估不同模型在使用该技能后的性能变化。实验表明，技能迁移能提升部分开源模型在专业任务上的表现，为降低AI应用成本、实现特定领域能力转移提供了实用方案。
categories:
- AI基础设施
tags:
- Agent技能
- CUDA内核
- 模型迁移
- 开源模型
- AI工具链
draft: false
translated_at: '2026-01-29T04:05:40.132087'
---

# 我们让Claude教会开源模型如何编写CUDA内核！

Agent（智能体）技能最棒的一点在于：**让您的Agent（智能体）在难题上实现技能升级**。这可以从两个角度来看：

1.  您可以使用Opus 4.5或其他SOTA模型，去攻克最棘手的难题。
2.  您可以让在您笔记本电脑上运行的模型实现技能升级，以处理更困难的问题。在这篇博客中，我们将向您展示如何实现后者。

这篇博客将详细介绍使用一个新工具 `upskill` 的过程，该工具可以利用大模型生成和评估Agent（智能体）技能，并让更小的模型使用这些技能。我们将在为 `diffusers` 模型编写CUDA内核的任务上对 `upskill` 进行基准测试，但这个过程通常对于降低成本，或在困难且特定领域的问题上使用更小的模型很有用。

## 什么是Agent（智能体）技能？

如果您错过了相关介绍，Agent（智能体）技能正在席卷编码Agent（智能体）领域。实际上，它们是一个将模型上下文定义为文件的简单概念，例如将指令保存为Markdown文件，将代码保存为脚本文件。这种文件格式使得它们易于生成、共享和审查。简而言之，它们是跨模型和工具共享能力的一种实用媒介，在特定领域或难题上最为有用。而不是那些模型本来就能做得很好的事情。

本文通过使用Claude生成一个技能文件来展示这个过程，该技能文件可供开源模型用于一项复杂且专业的任务：编写CUDA内核。
我们首先尝试了一个基于现有文档的简单技能，发现它提高了一些模型的性能，但并非所有模型。事实上，对于某些模型，它甚至可能降低性能或增加Token使用量。查看下面的图表，了解模型在使用和不使用基础技能时的性能表现。

![模型性能图表](/images/posts/ad757a563aeb.png)

现在，让我们逐步了解如何使用 `upskill` 让您的Agent（智能体）在难题上实现技能升级，并衡量其性能。

# 1. 让老师（Claude Opus 4.5）构建一个内核

首先，我们使用Claude Code交互式地构建一个内核并导出交互记录。我们通过指导、验证和添加文档链接来完成这个过程。这个略显朴素的过程对于揭示模型最初的挑战很重要。实际上，您可以多次迭代这个过程：尝试用技能的草稿版本解决任务，并用更小的模型进行实验。每次，您都可以指导Agent（智能体）改进技能，并在更小的模型上进行测试。

这是我们创建并一直用于构建内核的**技能示例**。我们从这个**Agent（智能体）交互记录**开始，其中Agent（智能体）能够构建内核，但并非没有一些帮助。

# 2. 从交互记录中创建Agent（智能体）技能

一旦教师模型完成了任务，我们需要让它制作一个技能。有几种有效的方法可以做到这一点。

*   在同一会话中，指导Agent（智能体）为其刚刚完成的任务创建一个技能文件。
*   在Agent（智能体）会话内部，或者使用导出的交互记录和新的Agent（智能体）会话，使用**Anthropic的‘skill creator’技能**。
*   使用 `upskill` 工具基于交互记录创建技能。

在大多数情况下，前两种选择会产生可用的技能。然而，拥有该技能的Agent（智能体）的性能是未知的。这就是 `upskill` 有用的地方，因为它还会根据交互记录为您的技能生成测试用例。然后，它会比较两种场景下的结果：使用交互记录，或应用技能。我们在下面看到，原始模型（Claude Opus）在使用和不使用技能时达到了相同的性能。这意味着该技能**为这个模型**捕捉到了任务。太好了！

![终端评估](/images/posts/1ff618cc9caf.png)

## 3. 将您的技能应用到开源、更小或更便宜的模型上

最后，我们需要将新创建的技能转移到我们打算使用的工具或模型上。大多数工具如 `codex`、`cursor` 和 `opencode` 已经为技能采用了一致的格式，即在 `{agent}/skills/{skill_name}/SKILL.md` 目录下，所以我们只需要将技能目录复制到这个位置。

使用 `upskill`，我们可以将一个技能和一组模型传递给 `eval` 命令，`upskill` 将在这些模型上运行测试用例，比较使用和不使用技能时的性能。我们在这里可以看到，该技能提高了一些开源模型的准确性，但并非所有模型。

![性能评估](/images/posts/74e307dddae4.png)

在这种情况下，我们可能希望通过重新生成技能来进一步迭代 `gpt-oss` 技能。我们可以执行 `upskill generate --from {skill}`。

Agent（智能体）技能的意义不仅在于模型性能。通常，无论有没有技能，Agent（智能体）都能达到给定的准确度，它们只是需要消耗更多的Token来达到目标。对于重复性任务，我们希望优化Agent（智能体）使用更少的Token来达到相同的准确度。下面的结果揭示了技能的另一个维度。一些模型显著减少了性能Token的使用量，而另一些模型**使用**技能后反而使用了更多Token。例如，对于 `moonshotai/Kimi-K2-Thinking`，该技能在准确性和Token使用方面显然是有效的。然而，对于Claude Opus 4.5，性能没有明显提升，Token使用量却增加了，因此您不会想在Claude Opus 4.5上使用这个技能。

![Token使用量](/images/posts/05e1856b919c.png)

**太长不看版**：用您创建的技能尝试和评估模型。使用 `upskill eval` 或类似工具来评估模型在使用和不使用技能时的性能。

以上就是让您的编码Agent（智能体）在难题上实现技能升级的高层次端到端流程。现在就像这样尝试使用upskill：

```shell
# 安装 upskill
pip install upskill

# 或使用 uvx
uvx upskill --help

# 基于Agent（智能体）交互记录生成技能
upskill generate "write nvidia kernels" --from ./trace.md

# 在技能上评估模型
upskill eval ./skills/my-skill/ --model haiku --model sonnet

# 为本地模型生成技能
upskill generate "parse YAML"
    --model opus
    --eval-model "unsloth/GLM-4.7-Flash-GGUF:Q4_0"
    --eval-base-url http://localhost:8080/v1

```

# 使用Agent（智能体）技能构建内核的深度教程

我们已经对如何提升Agent（智能体）技能有了高层次的理解。现在让我们看看我们为解决编写CUDA内核问题而构建的用例。

我们不仅仅想编写内核代码，还想理解完整的内核构建器工作流程：项目结构、`build.toml` 配置、特定架构的优化以及PyTorch绑定。本教程展示了 `upskill` 如何创建经过验证且真正有效的技能。

`kernel-builder-cuda-kernels` 技能教会了Claude关于CUDA开发所需了解的一切：目标GPU架构是什么、如何构建内核构建器项目、何时使用共享内存与寄存器、以及如何编写PyTorch绑定。

有了这个技能，您可以告诉Claude类似这样的话：

```
为H100构建一个融合的LayerNorm + GELU内核并进行优化。

```

然后Claude将创建完整的项目结构、CUDA实现和构建配置——遵循内核构建器所期望的确切约定。

这不仅仅是生成样板代码。该技能编码了领域专业知识：H100使用计算能力9.0，共享内存应对齐到128字节，异步内存复制需要 `__CUDA_ARCH__ >= 900`。这些需要花费数小时从文档中收集的知识被打包成约500个Token，可以按需加载。

## 设置与安装

安装 upskill：

```shell
pip install upskill
# 或使用 uvx 进行一次性运行
uvx upskill --help

```

设置您的API密钥：

```shell
export ANTHROPIC_API_KEY=sk-ant-...
export HF_TOKEN=hf_...

```

就这样。Upskill默认使用Anthropic Claude Opus-4.5模型，但也支持通过OpenAI兼容的端点作为生成器来使用OpenAI和本地模型。我们希望使用更昂贵、质量更高的模型来生成技能，而让更小的模型来使用它们。想想罗宾汉。

## 技能生成

让我们逐步了解生成一个技能的过程，该技能教会Agent（智能体）如何使用HuggingFace的 `kernels` 库构建CUDA内核。

### 生成技能

从一个清晰的任务描述开始：

```shell
upskill generate "build optimized CUDA kernels for PyTorch using HuggingFace kernel-builder"

```

上面我们使用了 upskill，但实际上它可以是任何 Agent（智能体）或聊天工具以及一个导出的执行记录。

```shell
upskill generate "write kernels" —-from <agent-trace>.md

```

此外，我们可以从一个现有技能开始并对其进行补充：

```shell
upskill generate "add more error handling and edge cases" 
    --from ./skills/kernel-builder-cuda-kernels/

```

upskill 会加载现有技能，应用你的改进，并重新评估以确保更改有效。

upskill 会创建一个技能，生成测试用例，评估性能，并根据失败情况进行优化：

```
Generating skill with sonnet...
Generating test cases...
Evaluating on sonnet... (attempt 1)
  60% -> 95% (+35%) OK

  kernel-builder-cuda-kernels
  Build optimized CUDA kernels for PyTorch using HuggingFace kernel-builder.

  SKILL.md              ~520 tokens

  baseline   ████████████                60%
  with skill ███████████████████    95%  (+35%)

Saved to ./skills/kernel-builder-cuda-kernels

```

基线显示了模型在没有任何技能的情况下的表现。"with skill" 结果显示了将技能注入上下文后的性能。35% 的提升意味着该技能是有效的。

该技能按照 Agent Skills 规范保存为一个目录：

```
./skills/kernel-builder-cuda-kernels/
├── SKILL.md           # 主要指令 (~520 tokens)
└── skill_meta.json    # 元数据和测试用例

```

```
---
name: kernel-builder-cuda-kernels
description: Build optimized CUDA kernels for PyTorch using HuggingFace kernel-builder.
---

# 使用 kernel-builder 构建 CUDA 内核

## 概述

本指南解释了如何使用 HuggingFace 的 kernel-builder 为 PyTorch 模型创建优化的 CUDA 内核。它涵盖了项目设置、内核实现以及为特定 GPU 架构（如 NVIDIA H100）进行构建。

## 项目结构

project/
├── build.toml              # 构建配置
├── kernel_src/             # CUDA 内核实现
│   ├── attention.cu
│   ├── layernorm.cu
│   └── geglu.cu
└── torch-ext/              # PyTorch C++ 绑定
    └── torch_binding.cpp

## 构建配置

创建 `build.toml` 来定义你的内核包：

[general]
name = "diffuser_kernels"
backends = ["cuda"]

[general.cuda]
# H100 的计算能力是 9.0
capabilities = ["9.0"]

...

```

### 在不同模型上评估

重要的测试是：这个技能是否有助于本地或更便宜的模型来构建内核？

```shell
# 启动一个带有 Web UI 的本地 OpenAI 兼容服务器：
llama-server -hf unsloth/GLM-4.7-Flash-GGUF:Q4_K_M

# 在本地模型上评估 (llama.cpp 服务器)
upskill eval ./skills/my-skill/ 
    --model "unsloth/GLM-4.7-Flash-GGUF:Q4_0" 
    --base-url http://localhost:8080/v1

```

```
Generating skill with sonnet...
Generating test cases...
Evaluating on "unsloth/GLM-4.7-Flash-GGUF:Q4_0"... (attempt 1)
  40% -> 85% (+45%) OK

  baseline   ████████░░░░░░░░░░░░   40%
  with skill █████████████████░░░   85%  (+45%)

Saved to ./skills/kernel-builder-cuda-kernels

```

在 "unsloth/GLM-4.7-Flash-GGUF:Q4_0" 上获得 45% 的提升，意味着该技能成功地将领域知识从一个能力强的模型转移到了一个更快、更便宜的模型上。能在较弱模型上工作的技能，在更强的模型上肯定也能工作。

这是核心价值主张：使用昂贵的模型来创建技能，然后用便宜或本地的模型来部署这些技能。

## upskill 中的评估如何工作

upskill 使用一种师生方法来评估模型，其中教师模型生成测试用例，供被评估的学生模型使用。

1.  教师模型 (Opus) 生成技能
2.  测试用例 (Opus) 根据任务描述自动生成
3.  学生模型 (本地) 在有技能和无技能的情况下被评估
4.  技能提升衡量改进程度

如果你将一个现有技能传递给 `upskill eval`，它会为该技能生成测试用例，并在这些用例上评估模型。测试用例是简单的输入/输出对，用于验证 Agent（智能体）是否理解任务：

```json
{
  "cases": [
    {
      "input": "Create a build.toml for a CUDA kernel targeting H100",
      "expected": {"contains": "9.0"}
    },
    {
      "input": "Write a basic CUDA kernel template with proper includes",
      "expected": {"contains": "cuda_runtime.h"}
    }
  ]
}

```

我们还可以测试一个技能在不同模型上的表现：

```shell
upskill eval ./skills/kernel-builder-cuda-kernels/ 
    --model haiku --m kimi --runs 5

```

```
Evaluating kernel-builder-cuda-kernels across 2 model(s)
  3 test case(s), 5 run(s) per model

haiku
  Pass rate: 4/5 (80%)  Avg assertions: 2.8/3

sonnet  
  Pass rate: 5/5 (100%)  Avg assertions: 3.0/3

┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Model  ┃ Pass Rate ┃ Avg Assertions ┃ Avg Tokens ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ haiku  │ 4/5       │ 2.8/3          │ 1250       │
│ kimi   │ 5/5       │ 3.0/3          │ 1890       │
└────────┴───────────┴────────────────┴────────────┘

```

这有助于你找到成本与性能的最佳平衡点：也许带有技能的 Haiku 模型就足够满足你的用例，从而节省大量的 API 成本。

## 下一步

我们已经展示了 upskill 可以创建经过验证的技能，将领域专业知识从强大的模型转移到更便宜的模型。内核构建器技能只是众多可能性中的一个例子。

可以尝试的事情：

-   为你的内部工具生成技能
-   为你的代码库构建技能库
-   捕获团队内部知识
-   跨模型进行基准测试

这种方法适用于任何你原本需要反复编写详细提示词的专业任务。技能可以在支持 Agent Skills 规范的 Claude Code、Codex、Cursor 和其他工具之间移植。

## 资源

- Upskill 仓库
- Agent Skills 规范
- HuggingFace kernel-builder

---

> 本文由AI自动翻译，原文链接：[We Got Claude to Build CUDA Kernels and teach open models!](https://huggingface.co/blog/upskill)
> 
> 翻译时间：2026-01-29 04:05
