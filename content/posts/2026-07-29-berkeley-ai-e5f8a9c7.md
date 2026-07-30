---
title: CUDA内核知识迁移至Apple Silicon的自动化方法
title_original: 'From CUDA to MLX: How K-Search Brings Decades of Kernel Expertise
  to Apple Silicon'
date: '2026-07-29'
source: Berkeley AI Research (BAIR)
source_url: http://bair.berkeley.edu/blog/2026/07/29/cuda-to-mlx-k-search/
author: ''
summary: 本文介绍了一种将CUDA内核专业知识自动迁移到Apple Silicon MLX框架的方法。基于K-Search进化式内核搜索框架，作者开发了结构化CUDA到MLX转换层，使现有CUDA内核知识库能适配为高质量Apple
  Silicon内核。实验表明，该方法在MLX注意力内核上达到0.97倍加速，在Mamba SSM内核上预填充速度提升最高20倍，接近专家水平性能。该方法不限于MLX，可适用于任何需要迁移CUDA专业知识的生态系统。
categories:
- AI基础设施
tags:
- CUDA
- MLX
- Apple Silicon
- 内核优化
- K-Search
draft: false
translated_at: '2026-07-30T05:01:27.616920'
---

**图 1：CUDA 到 MLX 优化映射图。** CUDA 优化知识可以被转化为架构原生的 MLX 策略，而不是逐条指令地复制。

我们正面临计算的新纪元。硬件正在迅速变化——不仅是更快的 GPU，还有来自不同供应商的、日益多样化的芯片，每种芯片都有其独特的架构，并且通常针对特定的人工智能工作负载进行了定制。软件的变化同样迅速，人工智能编码工具现在能在几分钟内生成几年前需要数月努力才能完成的内容。

由于如今计算领域如此多地围绕人工智能展开，GPU 内核是其成功的关键组成部分。这些是在 GPU 内部运行的低级程序，编写高效的内核远非易事——需要多年的专业知识才能做好。将一个内核从一个供应商的硬件迁移到另一个供应商的硬件更加困难，并且通常意味着从头重新发现相同的优化方法。例如，CUDA 生态系统已经积累了数十年来之不易的内核专业知识：经过手工调优的注意力机制、状态空间模型以及其他关键操作的实现，代表了数千小时的工程投入。较新的硬件生态系统（Apple Silicon、定制人工智能加速器等）发展迅速，但缺乏这种深度。

在这项工作中，我们探究这种专业知识是否可以自动迁移。我们基于 K-Search 进行了构建，这是一个由加州大学伯克利分校 Sky Lab 的 Cao 等人提出的进化式内核搜索框架，该框架使用人工智能来优化 GPU 内核，并为其扩展了一个面向 MLX（苹果为其 Apple Silicon 芯片开发的机器学习框架）的后端。我们开发了一种新颖的结构化 CUDA 到 MLX 转换层，使得 K-Search 能够将现有的 CUDA 内核作为知识库，并将其适配为适用于 Apple Silicon 的高质量 GPU 内核，而不是从头开始重建。

我们证明，我们的方法在 Apple Silicon 上达到了接近专家水平的性能，与原生 MLX 注意力内核相比实现了 0.97 倍的加速，并且在 Mamba SSM 内核上，与社区 mlx-lm 实现相比，预填充速度最高提升了 20 倍；我们在下文中报告了这些数据，以及有多少性能提升来自转换层。尽管我们专注于 Apple Silicon 的 MLX 内核，但该方法并非 MLX 所特有，并且适用于任何可以迁移 CUDA 专业知识的生态系统。

## 为什么选择 MLX？

自 2023 年底以来，苹果的 MLX 框架获得了显著的应用。随着 Apple Silicon 被应用于数亿台 MacBook 和 Mac Studio 中，MLX 使得无需云成本的本地人工智能推理成为可能。统一内存架构使其对中型模型（M 系列芯片上 7B–70B 参数）尤其具有吸引力。

然而，在这一发展势头之下，存在着一个显著的差距：许多 NVIDIA 生态系统视为理所当然的性能关键型内核——分页注意力、优化的 SSM 扫描内核、融合的 MoE 路由——要么缺失，要么在没有硬件特定调优的情况下实现得很简陋。MLX 能够正确运行模型，但通常留下了显著的性能提升空间。

这一差距正是本文其余部分所要探讨的动机所在。

## 什么是 K-Search？

K-Search 是一个进化式内核优化框架，最初由我们的第一作者曹诗怡在加州大学伯克利分校 Sky Lab 开发。给定一个朴素的内核和一个硬件规格说明，它会运行一个迭代优化循环：一个 LLM（大语言模型）推理接下来应该尝试哪些优化，一个代码编写模型生成候选内核，然后这些候选内核在真实硬件上进行编译和基准测试。

测量结果反馈到搜索过程中，搜索过程不断优化，追求有希望的方向，放弃死胡同，直到性能收敛。

**算法 1：通过共同进化世界模型进行 K-Search。** 搜索过程在以下步骤之间交替：选择最有希望的动作，实例化和评估代码直到改进停滞，以及通过插入、更新和剪枝操作来进化世界模型。改编自 Cao 等人（2026 年）。

搜索过程由一个规范（Spec）指导：一个特定领域的文档，编码了硬件规则、优化模式和数学约束，这可以防止生成的代码产生无效的原语幻觉，并确保候选内核能够实际编译并高效运行。

在我们的运行中，一个单一的模型（Gemini 3.5 Pro Preview）扮演了两个角色：它维护推理状态并编写内核。推理部分被提示为“GPU 内核性能工程师”，并被要求在提出任何建议之前完成一个固定的分析：对内核进行分类（归约、扫描、注意力/softmax……），以规范形式重写参考计算，绘制数据布局和访问模式，并假设每个运行时状态下的可能瓶颈（带宽、延迟、计算或同步）。只有这样，它才会输出候选优化方案，每个方案都是一个可以在一次迭代中实现的单一更改。

我们将持久的推理状态称为**世界模型**。它不是一个扁平的要尝试的事项列表，而是一个决策（前缀）树：每个根到叶子的路径组成一个完整的优化计划，而兄弟分支则是相互竞争的替代方案。每个节点都被评分——一个在 [0, 10] 范围内的**总体评分**，一个在 [0, 1] 范围内的**置信度**，以及每个节点对内存带宽、寄存器压力和计算/硬件适配性的**影响**——这样搜索就可以对部分计划进行排序，并扩展最有希望的计划。该树在轮次之间持续存在并增长：完善一个想法会添加一个子节点，而不是覆盖其父节点，并且如果最佳评分在几轮内未能改善（一个停滞窗口），搜索会回退以探索替代分支。一个在注意力内核运行过程中出现的单个节点如下所示：

```
{
  "action": "将线程组内存 softmax 归约替换为仅寄存器归约：每个 SIMD 组拥有 8 个查询行，并使用 simd_shuffle_xor 在通道间进行归约，从而移除一个线程组屏障。",
  "difficulty_1_to_5": 4,
  "impacts": {
    "memory_bandwidth":  8,
    "register_pressure": 4,   // 风险：如果 Br > 8 则溢出
    "compute_hw_fit":    9    // SIMD 宽度 32；保持 tile 8x8
  },
  "overall_rating_0_to_10": 8,
  "confidence_0_to_1": 0.7
}

```

**列表 1：示例 K-Search 世界模型节点。** 每个候选优化记录了一个具体的动作、估计的硬件影响、一个总体优先级评分以及模型的置信度。

**图 2：K-Search 概述。** 该框架在一个结构化为搜索树的**搜索状态** $S_t$ 上运行。该树由**封闭节点**（蓝色，已访问状态并附有程序，如 $x_{12}$）和一个**前沿**的**开放节点**（橙色，待定假设，如 $u_{13}$）组成。工作流程迭代三个步骤：(1) **动作选择**，根据世界模型估计的优先级分数 $V$ 从前沿检索最有希望的动作节点；(2) **局部优化**，随机策略 $\pi_{\mathrm{code}}$ 采样具体的实现，直到停滞；以及 (3) **世界模型更新**，LLM（大语言模型）对轨迹进行推理，通过**插入**（添加新动作）、**更新**（调整 $V$，例如 $u_{11}$ 从 0.9 降至 0.6）和**剪枝**（移除不太有希望的节点，如 $u_{10}$）来更新搜索树。

原始的 K-Search 论文在来自 FlashInfer 的 CUDA 内核上评估了这种搜索策略。在 GQA 解码、MLA 解码、MLA 预填充和 MoE 上，在相同的 120 次迭代预算下，K-Search 比 OpenEvolve 和 ShinkaEvolve 实现了更一致的改进。这些结果奠定了我们在此构建的搜索框架；本文的其余部分探讨其优化知识是否可以迁移到 CUDA 之外。

**图 3：原始 K-Search 论文的主要结果。** 在三次运行中，K-Search 在四个 FlashInfer CUDA 内核上，比 OpenEvolve 和 ShinkaEvolve 实现了更强的迄今最佳搜索分数、每工作负载内核性能以及加速比分布。完全复制自 Cao 等人（2026 年）。

## 构建 MLX 后端

为了将K-Search引入Apple Silicon，我们首先构建了一个原生MLX后端。我们为K-Search实现了一个完整的MLX专用任务适配器，包括：

- 一个MLX任务后端，位于`ink_search/tasks/`，通过MLX的Metal/C++ API处理Apple Silicon上的内核编译与执行。
- 更新后的内核生成器提示词，用于编写和修改Metal/MLX内核。
- 使用`mlx.core`测量工具集成的MLX专用基准测试。

## 将CUDA专业知识迁移到MLX

然而，更有趣的挑战并非简单地在MLX上运行K-Search。关键在于，专家级CUDA内核编码了数十年的优化知识，只要你能弥合概念上的差距，这些知识就可以迁移到Apple GPU。仅仅将一个CUDA内核交给LLM并要求其移植是不够的：如果没有深入的硬件上下文，它生成的代码在语法上有效，但在架构上是错误的（错误的块大小、无效的原语、不匹配的内存假设）。

我们的迁移层包括：

- **概念映射表**：一个结构化的CUDA原语及其MLX/Metal对应物的术语表，并带有硬约束。例如：
  - `__shared__`映射到Metal的`threadgroup memory`，但有32 KB的硬限制（而NVIDIA为48 KB）
  - `warp_reduce`映射到MMA（首选）
  - `__syncthreads()`变为`threadgroup_barrier(mem_flags::mem_tg)`
  - H100约3.35 TB/s的HBM3映射到M3 Max约400 GB/s的统一DRAM——这一带宽差异重塑了哪些优化值得追求。
- **MLX专用提示与模式**：针对没有直接CUDA等价物的操作的具体代码级模式，例如在8×8 MMA块布局中使用`simd_shuffle_xor`进行基于寄存器的行归约，或“exp2技巧”（将$exp(x)$替换为$exp_2(x \log_2 e)$），以在Apple快速的$exp_2$硬件指令上实现更快的softmax。
- **可复用的断言**：将专家级内核行为重新定义为进化搜索必须保留的属性，而非需要复制的代码。

## 匹配专家级内核性能：注意力内核

我们评估了Apple Silicon上MLX注意力内核的三种配置：(1) 朴素基线，(2) 无额外上下文的纯进化，(3) 完整上下文迁移层，该层为优化器提供从高性能内核（如FlashAttention-2）中提取的架构特定实现知识，使进化搜索能够推理实现策略，而非从朴素内核开始。这三种配置共同让我们能够隔离迁移层的精确影响。

图4：通过堆叠优化实现的注意力内核性能扩展。“完整上下文”配置成功发现并实现了诸如双缓冲和循环展开等高级策略，达到了接近专家级的性能。

从Apple最先进注意力内核速度的0.26倍跃升至0.97倍——这充分说明了迁移层的重要性。在完整上下文下，进化后的内核独立发现了FlashAttention 2中的关键优化：线程组内存分块、在线softmax、用于内存访问的K矩阵转置，以及exp2技巧。最后一项将每个softmax指数替换为以2为底的指数，这是精确的，并允许内核直接使用Apple快速的`fast::exp2()`硬件指令，而无需在运行时进行底数转换。

## 20倍更快的预填充：Mamba SSM内核

为了评估K-Search是否能泛化到注意力内核之外，我们将其应用于Mamba使用的状态空间模型（SSM）内核。与注意力不同，其计算瓶颈是循环状态更新而非softmax，这提供了一个截然不同的优化挑战。我们将进化后的实现与社区MLX实现（mlx-lm）以及PyTorch参考实现（mamba.py）在M1 Max上进行了比较。

在mamba-370m f16、M1 Max 64GB上评估：

表1：mamba-370m（f16，M1 Max 64GB）上的预填充和解码吞吐量。mlx-mamba（我们的）的预填充吞吐量比社区mlx-lm基线高出约20倍，而解码吞吐量保持可比。

与mlx-lm相比约20倍的预填充加速归结于一个差异：mlx-lm没有为SSM实现并行扫描。状态循环

看起来本质上是顺序的，但每一步都可以在结合律组合下写为一对$(\bar{a}_t, \bar{b}_t)$，

这精确地再现了循环。由于该算子是结合性的，整个序列可以通过并行（前缀）扫描在$O(\log N)$个依赖步骤中评估，而不是$O(N)$。mlx-lm跳过了这一点，一次只处理一个Token，使Apple Silicon的大部分计算资源闲置；我们进化后的Metal内核应用了扫描，更充分地利用了GPU吞吐量。这种提升体现在预填充中，其中完整序列可用于并行扫描，而在单Token解码中，每一步只有一个新Token且没有可并行化的扫描——这就是为什么解码行大致持平而预填充提升了约20倍。

mamba.py在预填充和解码上都很慢，因为它是一个PyTorch参考实现，在Apple Silicon上回退到CPU或MPS，放弃了MLX的Metal后端所能实现的硬件特定优化。

## 下一步是什么？

在我们研究的两个内核上，基于结构化跨平台迁移知识的AI驱动进化内核搜索在Apple Silicon上达到了接近专家级的性能，而无需一个从零开始的GPU专家团队。我们尚不知道这能泛化到何种程度，但结果是令人鼓舞的。

对我们来说，主要收获是瓶颈不在于LLM编写Metal代码的能力，而在于我们提供给它的上下文和约束的质量。我们的CUDA迁移层将现有的NVIDIA内核专业知识转化为针对Apple Silicon的可操作指导，并让K-Search的进化搜索完成其余工作。

我们正在多个方向上积极扩展这项工作：支持新架构，当前工作重点是为IBM Spyre AIU和更广泛的硬件目标开发新内核；增加更多内核，如分页注意力和融合MoE路由；以及改进与K-Search进化循环的集成，使迁移上下文更加自动化。

## 致谢

这项工作由IBM Research完成，并基于加州大学伯克利分校Sky Lab的K-Search（Cao等人，2026）。我们欢迎来自MLX和更广泛AI系统社区的协作与反馈。如果您正在为非CUDA硬件进行内核优化，我们很乐意听取您的意见。

## 引用

```
@article{cao2026k,
  title={K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model},
  author={Cao, Shiyi and Mao, Ziming and Gonzalez, Joseph E and Stoica, Ion},
  journal={arXiv preprint arXiv:2602.19128},
  year={2026}
}

```

## 附录：亲自尝试

MLX后端构建在开源K-Search仓库之上，因此此处的结果可以直接复现。步骤如下：

1. 克隆并安装

```
git clone https://github.com/caoshiyi/K-Search.git
cd K-Search

uv pip install openai wandb
uv pip install git+https://github.com/caoshiyi/flashinfer-bench-ksearch.git

```

2. 设置你的凭证

打开`scripts/`下的相关脚本，并在顶部设置三个变量：

```
KSEARCH_ROOT=/path/to/K-Search
API_KEY=your-llm-api-key

```

3. 运行内核搜索

```
# 在Apple Silicon上优化Flash Attention（世界模型模式）
bash scripts/mac_flash_attention_wm.sh

# 或者一个Mamba SSM内核，例如选择性扫描
bash scripts/mamba_selective_scan_fwd_wm.sh

```

完整的CLI参考和文档位于README中。

---

> 本文由AI自动翻译，原文链接：[From CUDA to MLX: How K-Search Brings Decades of Kernel Expertise to Apple Silicon](http://bair.berkeley.edu/blog/2026/07/29/cuda-to-mlx-k-search/)
> 
> 翻译时间：2026-07-30 05:01
