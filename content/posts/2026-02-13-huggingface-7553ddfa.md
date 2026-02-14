---
title: 为所有人定制CUDA内核：基于Codex与Claude的智能体技能
title_original: Custom Kernels for All from Codex and Claude
date: '2026-02-13'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/custom-cuda-kernels-agent-skills
author: ''
summary: 本文介绍了一种通过构建智能体技能，让编程智能体（如Claude和Codex）能够自动编写生产级CUDA内核的方法。该技能将复杂的CUDA内核开发知识（包括GPU架构优化、PyTorch绑定、内存访问模式等）打包成结构化指导，使智能体能够针对特定模型（如transformers和diffusers中的模型）生成可工作的内核代码，并自动完成基准测试与集成。这降低了高性能内核开发的门槛，使定制化硬件加速更易实现。
categories:
- AI基础设施
tags:
- CUDA内核
- AI编程智能体
- GPU优化
- PyTorch
- 自动化代码生成
draft: false
translated_at: '2026-02-14T04:12:37.859782'
---

# 为所有人定制内核：从Codex到Claude

tl;dr：我们构建了一个Agent（智能体）技能，用于教导编程Agent如何编写生产级CUDA内核。随后，我们让Claude和Codex针对两个真实目标进行工作：一个`diffusers`流水线和一个`transformers`模型。这些Agent为两者都生成了可工作的内核，包括正确的PyTorch绑定和端到端的基准测试。

编写CUDA内核很难。编写能正确与`transformers`和`diffusers`集成的CUDA内核则更难。这其中涉及特定架构的内存访问模式、向量化策略、warp shuffle规约，以及十几种即使经验丰富的开发者也会踩坑的集成陷阱。这恰恰是Agent技能大放异彩的那种专业化、高风险问题。

我们为编程Agent提供了它们所需的领域知识，例如：针对哪种GPU架构、如何构建内核构建器项目、何时使用共享内存而非寄存器，以及如何编写PyTorch绑定。剩下的工作则由Agent完成。如果你使用过LLM训练技能或阅读过《我们让Claude教授开源模型》，你会对这种模式感到熟悉：将领域专业知识打包成技能，让Agent针对问题，然后让它工作。

## 为什么需要内核技能？

Kernel Hub解决了定制硬件内核的分发问题。你可以通过一个简单的`get_kernel`调用从Hub加载预编译的内核。无需构建，无需配置标志。然而，仍然需要有人来*编写这些内核*。这正是本技能所要填补的空白。

CUDA内核开发涉及的知识面极其广泛：

*   针对每一代GPU的硬件特定优化指南。H100、A100和T4各自拥有不同的计算能力、共享内存大小和带宽特性。
*   在库层面，`diffusers`和`transformers`有不同的模块层次结构、归一化约定和集成模式。自定义内核需要在PyTorch中注册，以便`torch.compile`能够识别。
*   在分发方面，内核可能依赖于CUDA、PyTorch和Python版本，这造成了庞大的环境矩阵。

这些领域知识往往散落在文档标签页和Stack Overflow的回答中。一个Agent技能将其打包成可按需加载的上下文。

首先，让我们展示如何立即使用这个技能，然后我们将深入探讨我们如何对内核进行基准测试的细节。

## 安装技能

该技能随`kernels`库一同提供。通过一个命令即可将其安装到你的编程Agent中：

```shell
# 我们需要从主分支安装kernels
pip install git+https://github.com/huggingface/kernels.git
kernels skills add cuda-kernels --claude
```

这会将技能放入`.claude/skills/cuda-kernels/`目录，Claude Code和Cursor会自动识别。对于其他Agent：

```shell
# Codex
kernels skills add cuda-kernels --codex

# OpenCode
kernels skills add cuda-kernels --opencode

# 自定义目标路径
kernels skills add cuda-kernels --dest ./my-agent/skills/

# 全局安装（在所有项目中可用）
kernels skills add cuda-kernels --global

# 覆盖现有安装
kernels skills add cuda-kernels --claude --force
```

安装完成后，向你的Agent发出提示：

```
为transformers中的Qwen3-8B模型，构建一个针对H100的向量化RMSNorm内核。
```

或者，你可以尝试更开放式的任务：

```
为transformers中的Qwen3-8B模型，构建一个针对H100的优化注意力内核。将其与PyTorch基线进行基准测试，并验证端到端性能的提升。
```

Agent可以读取该技能，选择合适的架构参数，生成CUDA源代码，编写PyTorch绑定，设置`build.toml`，并创建基准测试脚本。

如果你正在处理更复杂的内核，或技能未涵盖的特定架构优化，那么该技能提供了基础构建模块和模式供你起步。我们也欢迎对技能本身做出贡献。

## 技能包含什么

该技能包含大约**550个Token**的结构化指导，外加参考脚本、GPU优化指南、故障排除文档以及完整的工作示例。像Codex和Claude这样的Agent式编码工具可以读取这些内容并生成一个可工作的内核项目。

它涵盖：

*   针对H100、A100和T4的NVIDIA GPU架构感知优化（计算能力、内存带宽、共享内存大小、块大小调整）
*   针对`diffusers`和`transformers`的集成模式，包括每个库特有的陷阱
*   支持BF16、FP16和FP32向量化内存访问模式的内核模板
*   用于独立内核微基准测试和端到端流水线对比的基准测试工作流
*   通过`get_kernel`实现HuggingFace Kernel Hub集成，用于加载社区内核

```
.claude/skills/cuda-kernels/
├── SKILL.md                              # 主要说明（约550个Token）
├── scripts/
│   ├── benchmark_example.py              # 端到端基准测试模板
│   ├── benchmark_rmsnorm.py              # 独立内核微基准测试
│   ├── ltx_kernel_injection_example.py   # Diffusers集成模式
│   ├── transformers_injection_example.py # Transformers集成模式
│   └── huggingface_kernels_example.py    # Kernel Hub集成
└── references/
    ├── diffusers-integration.md          # Diffusers指南（含陷阱）
    ├── transformers-integration.md       # Transformers指南
    ├── huggingface-kernels-integration.md
    ├── h100-optimization-guide.md
    ├── a100-optimization-guide.md
    ├── t4-optimization-guide.md
    ├── kernel-templates.md
    └── troubleshooting.md
```

当Agent加载此技能时，它将获得从“给我写一个RMSNorm内核”到构建、可基准测试项目所需的一切。它会通过grep和glob在技能中查找相关文件和目录。因此，以易于查找的方式构建技能结构非常重要。

Agent被指示生成符合`references/kernel-templates.md`中模板的内核，并生成一个完整的内核项目：

```
examples/your_model/
├── kernel_src/
│   └── rmsnorm.cu              # 向量化CUDA内核
├── torch-ext/
│   ├── your_kernels/__init__.py
│   └── torch_binding.cpp       # PyTorch C++绑定
├── benchmark_rmsnorm.py        # 微基准测试脚本
├── build.toml                  # kernel-builder配置
├── setup.py                    # pip install -e .
└── pyproject.toml
```

我们在两个真实目标上对此进行了测试。

## 内核基准测试：Diffusers（H100上的LTX-Video）

Agent为`diffusers`中的视频生成流水线LTX-Video构建了RMSNorm、RoPE 3D、GEGLU和AdaLN内核。完整示例位于`examples/ltx_video/`。我们针对H100优化了RMSNorm内核。两项基准测试均在H100 80GB HBM3上以BFloat16精度运行。

如果你想查看生成的内核，请访问此示例

### 独立RMSNorm基准测试

首先，我们将独立的RMSNorm内核性能与PyTorch基线进行比较。这是优化流水线中的主要加速来源。

![isolated rmsnorm benchmark ltx-video](/images/posts/841c4bf4a399.png)

平均加速比：**1.88倍**，带宽效率：达到H100理论值（3,350 GB/s）的**34.7%**

### 端到端视频生成（49帧，30步，H100 80GB）

接下来，我们将优化内核的端到端视频生成性能与基线（无编译）和`torch.compile`基线进行比较。

![e2e benchmark ltx-video](/images/posts/0e63620fae12.png)

在LTX-Video中，RMSNorm约占**总计算量的5%**。其余时间花费在注意力机制、线性投影和VAE解码上。单一内核类型带来的**6%端到端加速比**与该计算分布相符。

## 内核基准测试：Transformers（H100上的Qwen3-8B）

Agent为`transformers`中的大语言模型Qwen3-8B构建了一个RMSNorm内核，该模型在32层中分布有65个RMSNorm模块。完整示例位于`examples/qwen3_8b/`。我们针对H100优化了RMSNorm内核。两项基准测试均在H100 80GB HBM3上以BFloat16精度运行。

如果你想探索该内核，请点击此处查看。

### 孤立 RMSNorm 基准测试

我们再次将孤立 RMSNorm 内核的性能与 PyTorch 基线进行比较。

![孤立 rmsnorm 基准测试 qwen3-8b](/images/posts/5efb93e75b97.png)

平均加速比：1.94倍，带宽效率：H100 理论值（3,350 GB/s）的 22.3%。

加速比随序列长度变化：128个 Token 时为 1.58倍，8192个 Token 时为 2.47倍。对于长上下文推理，定制内核大致将 RMSNorm 的延迟减半。

## 将你的内核发布到 Hub

Agent（智能体）为你提供一个可工作的内核。Kernel Hub 让你可以分享它，这样任何人都无需编译即可加载它。以下是从 Agent 输出到发布内核的完整路径。

### 1. 验证项目结构

Agent 生成的项目已经遵循 `kernel-builder` 的布局：

```
your_kernel/
├── build.toml               # 构建配置
├── kernel_src/
│   └── rmsnorm.cu           # CUDA 内核源代码
└── torch-ext/
    ├── torch_binding.cpp    # 注册 Torch 操作
    └── your_kernels/
        └── __init__.py      # 包装 _ops 的 Python API

```

`build.toml` 告诉 `kernel-builder` 要构建什么。Agent 会为你生成此文件，包括针对目标 GPU 的正确 `cuda-capabilities`：

```
[general]
name = "your_kernels"
backends = ["cuda"]

[torch]
src = ["torch-ext/torch_binding.cpp"]

[kernel.rmsnorm]
backend = "cuda"
src = ["kernel_src/rmsnorm.cu"]
depends = ["torch"]
cuda-capabilities = ["9.0"]  # H100

```

### 2. 使用 Nix 构建所有变体

Kernel Hub 的内核必须支持所有最近的 PyTorch 和 CUDA 配置。kernel-builder Nix flake 会自动处理这个问题。将示例 `flake.nix` 复制到你的项目中并运行：

```shell
nix flake update
nix run .#build-and-copy -L

```

这将为每个所需的 PyTorch/CUDA 变体构建内核，并将结果放在 `build/` 目录中。为了更快的构建速度，可以启用 HuggingFace Nix 缓存：

```shell
nix run nixpkgs#cachix -- use huggingface

```

### 3. 创建 Hub 仓库并推送

在 Hub 上创建一个模型仓库并上传构建好的内核：

```shell
huggingface-cli repo create your-org/your-kernel --type model
huggingface-cli upload your-org/your-kernel ./build

```

### 4. 其他人只需一行代码即可加载

一旦发布，任何人都可以零编译使用你的内核：

```py
from kernels import get_kernel

rmsnorm = get_kernel("your-org/your-kernel")

```

`get_kernel` 会检测用户的 Python、PyTorch 和 CUDA 版本，并下载匹配的预编译二进制文件。无需构建，无需设置标志，通常几秒钟内即可就绪。

技能和 Hub 是互补的。技能负责开发。Hub 负责分发。用技能构建一个内核，用基准测试脚本验证它，将其发布到 Hub，对其他人来说它就变成了一行代码。

我们构建了一个 Agent 技能，它教导编码 Agent 如何编写生产级的 CUDA 内核。然后，我们让 Claude 和 Codex 针对两个真实目标：一个 `diffusers` 管道和一个 `transformers` 模型。Agent 为两者都生成了可工作的内核，包括正确的 PyTorch 绑定和基准测试，端到端完成。我们对这些内核进行了基准测试，发现优化后的内核在孤立性能和端到端性能上都能提供加速。

- kernels 中的 CUDA Kernels 技能
- HuggingFace Kernel Hub 博客
- 我们让 Claude 微调了一个开源 LLM（大语言模型）
- 我们让 Claude 教导开源模型
- HuggingFace Kernels 社区

---

> 本文由AI自动翻译，原文链接：[Custom Kernels for All from Codex and Claude](https://huggingface.co/blog/custom-cuda-kernels-agent-skills)
> 
> 翻译时间：2026-02-14 04:12
