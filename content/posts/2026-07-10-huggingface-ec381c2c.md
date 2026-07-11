---
title: PyTorch性能分析：注意力机制的优化之道
title_original: 'Profiling in PyTorch (Part 3): Attention is all you profile'
date: '2026-07-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/torch-attention-profile
author: ''
summary: 本文是PyTorch性能分析系列的第三篇，聚焦于注意力机制的优化。通过从朴素注意力实现开始，逐步引入原地操作、SDPA和内核优化等技巧，展示了不同实现方式在性能分析器下的表现差异。文章强调通过阅读性能分析追踪来驱动优化，帮助读者理解如何识别热点、优化内存访问和利用融合内核，从而提升Transformer模型中注意力模块的计算效率。
categories:
- AI基础设施
tags:
- PyTorch
- 性能分析
- 注意力机制
- GPU优化
- Transformer
draft: false
translated_at: '2026-07-11T05:27:03.047852'
---

# PyTorch 性能分析（第三部分）：Attention is all you profile

这是"PyTorch 性能分析"系列文章的第三篇，我们将逐步培养阅读性能分析追踪的能力，并利用它来驱动优化：

1. PyTorch 性能分析（第一部分）：torch.profiler 入门指南
2. PyTorch 性能分析（第二部分）：从 nn.Linear 到融合 MLP
3. PyTorch 性能分析（第三部分）：Attention is all you profile（当前）

"PyTorch 性能分析"系列旨在让你能够轻松阅读性能分析追踪和表格。在**第一部分**中，我们对加法和乘法等基本数学运算进行了性能分析。我们看到了性能分析表格如何揭示热点，以及性能分析追踪如何展示算法随时间运行的顺序。

在**第二部分**中，我们将加法和乘法封装到 torch 线性层中。然后我们将多个线性层堆叠在一起（多层感知机）并对其进行了性能分析。在此过程中，我们还分析了融合和手动调优的内核。

从 Transformer 架构的角度来看，下一个合乎逻辑的性能分析目标是另一个基础算法——注意力机制。虽然它因二次时间复杂度而臭名昭著，但存在许多巧妙的技巧来缓解这个问题并使其变得快速。我们的目标不是详细涵盖每一个技巧。相反，我们想看看每个技巧在性能分析器下呈现出的不同面貌。

本博客文章的脚本位于：`04_a_naive_attention.py`、`04_b_inplace_ops_attention.py`、`04_c_sdpa_attention.py` 和 `04_d_kernels_attention.py`。和之前一样，建议在单独的标签页中打开它们，并在阅读时对照代码。我们使用 **NVIDIA A100-SXM4-80GB** GPU 来运行脚本。在 Hugging Face 基础设施上设置 GPU 并使用 **Dev Mode with Spaces** 进行脚本实验非常容易。也可以使用 **Hugging Face Jobs** 管道来运行脚本。

## 朴素注意力机制

注意力机制使用查询（Query, q）、键（Key, k）和值（Value, v）。它们之间的交互可以写成一系列简短的步骤：

1. 计算注意力分数 scores：`matmul(q, k.T)`
2. 缩放分数：`scores * scale`
3. 对分数应用因果掩码：`scores.masked_fill(mask, "-inf")`
4. 使用 softmax 归一化分数得到注意力权重 attn：`softmax(scores)`
5. 使用这些权重重新加权值：`matmul(attn, v)`

所以注意力机制实际上是一组基本操作的集合。其中一些我们已经熟悉（矩阵乘法），其余的操作也很容易识别。让我们在 PyTorch 中编写一个朴素的注意力模块并对其进行分析。

```py
class NaiveCausalAttention(nn.Module):
    def __init__(self, head_dim):
        super().__init__()
        self.scale = 1.0 / math.sqrt(head_dim)

    def forward(self, q, k, v, mask):
        scores = torch.matmul(q, k.transpose(-2, -1))
        scores = scores * self.scale
        scores = scores.masked_fill(mask, float("-inf"))
        attn = torch.softmax(scores, dim=-1)
        out = torch.matmul(attn, v)
        return out
```

在打开追踪之前，让我们像往常一样进行练习，猜测我们应该看到什么。追踪这个模块的 `forward`，我们预期会看到：

- 一个矩阵乘法内核（q . k.T）
- 一个乘法内核（缩放）
- 一个掩码操作
- 一个 softmax 内核
- 一个矩阵乘法内核（atten . v）

```bash
uv run 04_a_naive_attention.py
uvx trace-util -f traces/ -b <hf_uname>/traces
```

图 1 显示了性能分析的 CPU 通道（GPU 通道已折叠以免信息过载）。在 `attn_fwd`（我们注释的前向调用）内部，我们可以精确地看到我们猜测的那些操作。矩阵乘法现在已经是老朋友了，新操作也很容易识别：

- `mul`：缩放
- `masked_fill`：因果掩码
- `softmax`：softmax 内核

现在让我们展开 GPU 通道，看看实际启动了哪些内核。

图 2 显示了 GPU 通道与 CPU 通道并列。让我们放大 GPU 通道上的单个 `attn_fwd` 块，逐一查看内核。

图 3 让我们能够读取一个性能分析步骤中的各个内核：

1. 矩阵乘法（查询和键）
2. 乘法（缩放）
3. 内存拷贝 🤔
4. 因果掩码
5. softmax（生成注意力权重）
6. 矩阵乘法（注意力权重和值）

其中五个是预期的。内存拷贝是例外，那么它从何而来？线索在于 PyTorch 有就地操作。当你以普通（非就地）方式操作张量时，PyTorch 通常会创建一个副本，对其应用请求的操作，然后返回该副本。按照操作顺序，这里的罪魁祸首是我们的 `masked_fill`。

如果我们将其替换为就地操作会怎样？

## 使用就地因果掩码的朴素注意力机制

我们只需将 `masked_fill` 改为 `masked_fill_`（注意末尾的下划线，这是 PyTorch 就地操作的约定），然后运行相同的脚本。

```diff
def forward(self, q, k, v, mask):
    # q, k, v: [batch, heads, seq, head_dim]
    scores = torch.matmul(q, k.transpose(-2, -1))  # [batch, heads, seq, seq]
    scores = torch.mul(scores, self.scale)
-    scores = scores.masked_fill(mask, float("-inf"))
+    scores.masked_fill_(mask, float("-inf"))
    attn = torch.softmax(scores, dim=-1)
    out = torch.matmul(attn, v)  # [batch, heads, seq, head_dim]
    return out
```

让我们查看追踪，看看是否有变化。

```bash
uv run 04_b_inplace_ops_attention.py
uvx trace-util -f traces/ -b <hf_uname>/traces
```

就地版本（图 5）在掩码步骤内部包装的 CPU 操作远少于非就地版本（图 4）。这是一个令人鼓舞的信号。让我们展开 GPU 通道来确认那里发生了什么。

在 GPU 通道上，`Memcpy` 内核彻底消失了（图 6 和图 7）。通过一行代码的更改，我们在每次前向传播中减少了一个完整的内核。单独来看这可能不算什么，但请记住这只是单个注意力操作。在基于 Transformer 的大模型（LLM、扩散模型等）的上下文中，它每层重复一次，并且有很多层，因此节省的开销会迅速累积（如果这为你带来了加薪，分给我们至少 10% 才显得公平）。

非就地操作是 PyTorch 的默认行为是有原因的。为了计算梯度，自动求导必须记住在前向传播中看到的张量值，因为许多反向传播公式会重用它们。就地操作会覆盖内存中的这些值，因此反向传播将读取错误的数值。由于我们在 `torch.no_grad` 下运行 `forward`，就地操作对我们来说是安全的，没有反向传播，也没有任何东西会被破坏。同样值得注意的是，就地操作不仅节省时间（就像我们在案例中看到的），还节省内存（因为没有额外的副本），这对于像 logits 这样的大张量来说非常棒！

## 缩放点积注意力

我们刚刚从基本操作构建了注意力机制，甚至减少了一个 `Memcpy`。好消息是 PyTorch 团队已经为我们完成了所有这些工作，并将整个流程打包成一个函数：

```py
from torch.nn import functional as F

F.scaled_dot_product_attention(q, k, v, is_causal=True)
```

这一行代码替换了我们手写的模块，而 `is_causal=True` 甚至省去了我们手动构建掩码的工作。值得停下来体会一下这一个调用隐藏了多少内容。而且它隐藏的不仅仅是代码行。缩放点积注意力（SDPA）并非只有单一实现。在底层，它会**分发**到多个后端之一，并选择支持我们输入（数据类型、头维度、掩码、硬件等）的最快后端。

**官方 SDPA 教程** 引导我们完成这个选择过程，而后端本身列在 `torch.nn.attention.SDPBackend` 枚举中：

```python
from torch.nn.attention import SDPBackend

BACKENDS = {
    "math": SDPBackend.MATH,
    "flash": SDPBackend.FLASH_ATTENTION,
    "efficient": SDPBackend.EFFICIENT_ATTENTION,
    "cudnn": SDPBackend.CUDNN_ATTENTION,
}
```

通常SDPA会为我们选择后端，但我们可以通过`torch.nn.attention.sdpa_kernel`上下文管理器固定使用特定后端。这正是我们在脚本中所做的。这使我们能够单独分析每个后端，并观察它们在追踪中呈现出的不同表现。让我们逐一来看。

### Math后端

```bash
uv run 04_c_sdpa_attention.py --backend math
uvx trace-util -f traces/ -b <hf_uname>/traces
```

在打开任何内容之前，我们先来猜测一下。我们已经将手写的注意力机制（matmul、mul、mask、softmax、matmul）替换为单行代码，因此我们预期追踪会变得更简单、更快。更少的内核、更少的CPU调度，甚至可能是一个融合内核。让我们先检查分析器表格。

这是我们遇到的第一个意外：单行代码的速度反而慢了**3.7倍**。

打开追踪（图9）就能看出警报响起的原因：Math后端每次前向传播启动了**20个**GPU内核，而我们朴素注意力实现（图8）只启动了**5个**。这与我们的猜测完全相反。让我们弄清楚为什么会这样。

#### Tensor Core闲置

在**第2部分**中，我们学会了像解读指纹一样解读内核名称。让我们在这里沿用这个习惯：

我们用于捕获这些追踪的A100配备了**Tensor Core**，这是一种专门用于加速矩阵乘法的专用硬件，其速度远快于普通的CUDA Core。要理解这为何重要，有必要了解GPU内部的结构。流式多处理器（SM）是GPU的计算单元，每个SM包含两种算术单元：CUDA Core和Tensor Core。CUDA Core是通用型的，一次处理少量元素，而Tensor Core则能在单条指令中完成整个小矩阵块的乘加运算。因此问题很简单：“每个后端是否真的在使用快速路径？”

内核名称给出了答案。朴素内核（图10）中的`s16816`是**bfloat16** Tensor Core矩阵乘法的特征标识（`16x8x16` Tensor Core指令），因此朴素版本走的是快速路径。而`sgemm`（图11）是在普通CUDA Core上运行的经典单精度（FP32）矩阵乘法。换句话说，Math后端从未触及Tensor Core：为了用速度换取数值精度，它将张量提升为**FP32**（即使输入是bf16，数据移动量也翻倍），并回退到较慢的CUDA Core。

#### 构建因果掩码

在朴素版本中，我们构建了一次因果掩码并重复使用。而在这里，我们传递了`is_causal=True`，Math后端在**每一次**调用中都为我们重新生成了掩码。你可以在CPU通道上观察到这一过程：

图12中我们看到的是：

```bash
aten::ones -> aten::tril            构建一个 [seq, seq] 的下三角矩阵
aten::scalar_tensor -> aten::fill_  生成 -inf 填充值
aten::where                         将其转换为加法偏置（0 或 -inf）
```

在GPU上，这表现为一个`triu_tril_kernel`、几个`where`内核和一个`add_`。这个让我们无需再考虑掩码的便利标志并没有消除工作量，只是将其下移了一层，每次前向传播都从头开始重建掩码。

#### 安全Softmax

我们手写的版本调用了普通的`aten::softmax`。而Math后端调用的是`aten::_safe_softmax`，其差异再次体现为额外的内核（图13）：

一个完全被掩码的行（每个条目都是`-inf`）会导致普通的softmax计算出`exp(-inf)/sum(exp(-inf)) = 0/0 = NaN`。`_safe_softmax`正是为了防止这种情况。我们的朴素内核从未考虑过这一点，在这种边界情况下会静默地产生NaN。

#### 那么Math后端是做什么用的？

综上所述，Math后端是参考实现。它将注意力机制直接、类型安全、NaN安全地分解为原始的ATen操作。它本质上就是我们手写的朴素注意力，但更加严谨。而这种严谨正是它极其缓慢的原因。

它的任务不是追求速度，而是**始终能工作**。这使其成为完美的基准线。我们接下来分析的每个后端（flash、efficient、cudnn）都试图将20个GPU内核压缩成一个融合内核，该内核保持bf16精度，并且从不实例化中间矩阵。

### Efficient后端

```bash
uv run 04_c_sdpa_attention.py --backend efficient
uvx trace-util -f traces -b <hf_uname>/traces
```

Math后端在一个分析器步骤中启动了20个内核，而Efficient后端只启动了一个`fmha_cutlassF_bf16_aligned_64x64_rf_sm80`内核（如图14所示）。

让我们解码这个内核的名称：

- `fmha`（融合多头注意力）：注意力中的所有原始操作现在都“融合”到一个操作中。
- `cutlassF`：基于CUTLASS（NVIDIA的开源Tensor Core GEMM模板）构建，`F`代表前向。
- `bf16_aligned`：以bfloat16运行（与Math不同，没有FP32提升）。
- `64x64`：分块大小。
- `rf`（寄存器文件）：工作集保存在寄存器中，这是芯片上最快的存储器。
- `sm80`：为Ampere架构编译（A100的计算能力为8.0）。

这就是源自Meta的`xformers`库并最终被纳入PyTorch的内存高效注意力内核。当人们提到“xformers后端”时，指的就是这个`fmha_cutlassF`内核。

### Flash后端

```bash
uv run 04_c_sdpa_attention.py --backend flash
uvx trace-util -f traces -b <hf_uname>/traces
```

`void pytorch_flash`内核（图15）是**FlashAttention-2**（Tri Dao的实现），已集成到PyTorch中。

在进一步解读追踪之前，值得回答你现在应该会问的问题：**为什么会有个名为“flash”的完整后端，它又为何如此重要？**

#### 为什么会有Flash Attention？

让我们暂时回到Math后端。它真正的问题不在于20个内核的数量，而在于这些内核之间相互传递的内容。

步骤1构建了完整的分数矩阵`attn = q . k.T`，每个头的大小是`[seq, seq]`。对于序列长度4096，单个头就是`4096 x 4096 ≈ 1600万`个数字。这个矩阵会被写入HBM（GPU的主内存），前提是有足够的空间。然后，它被读回进行缩放，再次写入以应用掩码，再次读回进行softmax，如此反复。注意力机制的成本主要来自这种**往返HBM的流量**，而不是矩阵乘法本身。

FlashAttention正是针对这一点。它不是先计算整个`s`矩阵再对其进行规约，而是遍历`k`和`v`的分块，在过程中维护一个运行中的softmax（“在线softmax”技巧），并逐块累积输出。完整的`[seq, seq]`分数矩阵**从不写入HBM**，它只存在于芯片上。正是这个单一的想法，使得整个注意力流程可以压缩成一个融合内核，并在Tensor Core上保持bf16精度。

#### 为什么Flash在分析器下看起来“不对劲”

这就是Flash让那些阅读分析器足迹的人感到惊讶的地方。它是最快的后端，但分析器报告其**占用率非常低**（如图16所示）。要理解为什么这没问题，我们需要三个快速定义。

GPU内核本质上是由许多小执行单元执行的一系列指令。这些独立的执行单元（线程）负责加载变量、相加、存储等操作。对于每个内核，我们会启动大量线程，为了管理它们，我们将其分组为线程块。

线程块被调度到流式多处理器（SM）上，SM是GPU的主要计算单元。一个线程块完全驻留在一个SM上，如果资源充足，一个SM可以同时容纳多个线程块。这些资源包括寄存器、共享内存、最大常驻线程数和最大常驻线程束数。因此，当我们说一个内核占用率低时，意味着每个SM上的常驻线程束数量少于其理论上能支持的数量。

如果你想了解更多关于线程、线程块、网格等信息，这里有一个**很好的资源**。

如果你在追踪中点击Flash内核，其足迹会说明一切（图17）。

Flash 使用了大量每线程寄存器和每块共享内存。例如，如果一个块有 128 个线程，每个线程使用 255 个寄存器，那么该块需要 128 × 255 = 32,640 个寄存器。在拥有 65,536 个寄存器的 Ampere SM 上，一次只能容纳两个这样的块。每个 128 线程的块有 128 / 32 = 4 个 warp，因此两个块只提供 8 个驻留 warp。相对于最多 64 个驻留 warp，这大约只有 13% 的占用率。Flash 的占用率低并非因为优化不佳，而是因为每个块在片上资源使用上故意设计得非常“重”。

而这正是关键所在。高占用率通过保持大量 warp 就绪来帮助隐藏延迟，但它并不能使工作本身更高效。Flash 故意使用这些寄存器和共享内存，是为了将注意力分块保留在片上，积极重用数据，并避免在全局内存中实例化完整的注意力矩阵。

### cuDNN 后端

```bash
uv run 04_c_sdpa_attention.py --backend cudnn
uvx trace-util -f traces -b <hf_uname>/traces

```

到目前为止，模式已经很熟悉了。与 flash 和 efficient 类似，cuDNN 在每次前向传播中为我们提供了一个融合的、flash 风格的内核（图 18）。因此，一个自然的问题是：如果 flash 已经融合了注意力，为什么 PyTorch 还要提供另一个 flash 后端？答案在于谁编写了内核以及它是如何构建的，而这种差异正是导致跟踪看起来不同的原因。

#### cuDNN 内核有何不同

Flash 和 efficient 是固定的、预编译的内核，随 PyTorch 一起提供。你每次都会得到相同的二进制文件。cuDNN 是 NVIDIA 自己的深度学习库，其注意力内核是针对特定问题生成和调优的。它在精神上更接近 `torch.compile` 的代码生成，而不是固定的 cuBLAS 二进制文件。你可以直接从（很长的）内核名称中看出这一点：

```bash
cudnn_generated_fort_native_sdpa_sm80_flash_fprop_wmma_f16_knob_6_128x64x64_4x1x1_cga1x1x1_kernel0_0

```

- `cudnn_generated`：不是预先提供的二进制文件，而是由 cuDNN 生成的。
- `flash_fprop`：一种 flash 注意力风格的前向传播。因此，该算法与 flash 后端属于同一系列。
- `wmma_f16`：它使用了 warp 级矩阵乘加（WMMA）API，即 16 位浮点流水线上的 Tensor Core 路径。
- `knob_6`：cuDNN 从一组预调优的配置（“旋钮”）中进行选择。不同的形状会选择不同的旋钮，很像 cuBLAS 选择分块变体。
- `128x64x64`：它选择的分块维度。

这一个事实——针对每个问题生成——解释了跟踪中看起来不寻常的所有其他内容。

1. 无转置操作：CPU 路径从 `_cudnn_attention_forward` 直接到几个 `aten::empty` 分配，然后是内核，零个 `aten::transpose`（图 19、20 和 21）。Flash 和 efficient 各插入四个（元数据）转置来重塑张量，而 cuDNN 直接使用原生的 `[B, H, S, D]` 布局，因为其生成器会为该布局生成内核。变体跟踪图 19：Flash 图 20：Efficient 图 21：cuDNN
2. 它通过 `cuLaunchKernelEx` 启动，而不是 `cudaLaunchKernel`：整个系列中的其他所有内核都通过运行时 API `cudaLaunchKernel` 启动。cuDNN 使用驱动级别的扩展启动，它携带启动属性（图 22）。图 22：cuDNN 后端的 CPU 路径，显示使用 `cuLaunchKernelEx` 驱动级启动而非 `cudaLaunchKernel`
3. 分析器报告 0% 的已实现占用率：不要只看表面值，这是一个测量差距，而不是 GPU 停滞。CUPTI（分析后端）无法像为 `cudaLaunchKernel` 那样将占用率归因于驱动 API（`cuLaunchKernelEx`）启动，因此该字段显示为 0。资源占用情况揭示了真相（图 23）：每个块 240 个寄存器 × 256 个线程 = 61,440 个寄存器，而 SM 有 65,536 个，因此每个 SM 只能容纳一个块（8 个 warp ≈ 12.5%），与 flash 完全一致。图 23：cuDNN 内核报告 0% 的已实现占用率，每个线程 240 个寄存器，每个块 256 个线程

无转置操作：CPU 路径从 `_cudnn_attention_forward` 直接到几个 `aten::empty` 分配，然后是内核，零个 `aten::transpose`（图 19、20 和 21）。Flash 和 efficient 各插入四个（元数据）转置来重塑张量，而 cuDNN 直接使用原生的 `[B, H, S, D]` 布局，因为其生成器会为该布局生成内核。

它通过 `cuLaunchKernelEx` 启动，而不是 `cudaLaunchKernel`：整个系列中的其他所有内核都通过运行时 API `cudaLaunchKernel` 启动。cuDNN 使用驱动级别的扩展启动，它携带启动属性（图 22）。

分析器报告 0% 的已实现占用率：不要只看表面值，这是一个测量差距，而不是 GPU 停滞。CUPTI（分析后端）无法像为 `cudaLaunchKernel` 那样将占用率归因于驱动 API（`cuLaunchKernelEx`）启动，因此该字段显示为 0。资源占用情况揭示了真相（图 23）：每个块 240 个寄存器 × 256 个线程 = 61,440 个寄存器，而 SM 有 65,536 个，因此每个 SM 只能容纳一个块（8 个 warp ≈ 12.5%），与 flash 完全一致。

#### 成本转移到了 CPU

“无转置操作”这一点很容易让我们期望 cuDNN 成为 CPU 上最精简的后端。但事实恰恰相反。

即使有零个转置操作，cuDNN 每次前向传播在 CPU 上花费约 214 µs，超过了 flash（138 µs）或 efficient（117 µs）。几乎所有时间都花在了 `aten::scaled_dot_product_attention` 自身时间（占整个运行时间的 26%）和 `_cudnn_attention_forward` 上。这是 cuDNN 的运行时引擎在每次调用时选择和准备计划（“旋钮”搜索）。

更少的可见 ATen 操作并不意味着更少的 CPU 工作，而是将工作转移到了库内部，分析器只能将其显示为一个粗大的不透明条。当跟踪突然变得更“干净”时，工作并不总是消失了，有时它只是转移到了分析器无法分解的地方。

在 GPU 上，cuDNN（186.3 µs）介于 efficient 和 flash 之间。在这个对 flash 非常友好的形状上，手写的 FlashAttention-2 略胜一筹。cuDNN 通常在其他形状（更大的头维度、不同的序列长度）上胜出，正是因为其生成器会针对每个问题重新调优，但这种重新调优也正是你在 CPU 上付出的代价。

## 我们涵盖的所有内容，一览无余

在结束之前，这里有一个表格，可以回顾我们分析过的每个注意力变体以及每个跟踪教给我们的一个经验。

## 系列总结

如果你从整个系列中只带走一件事，那就是我们在每次跟踪之前重复的习惯：先猜测，再查看。

大声说出你期望跟踪中包含的内容，打开它，并将任何不匹配视为屏幕上最有趣的事情。这三篇文章中的每一个真正洞见——隐藏的 Memcpy、addmm 尾声、20 个内核的数学后端、flash “看起来不对劲”的占用率、cuDNN 粗大的 CPU 条——都来自于与跟踪不匹配的猜测。

性能分析不是一项为 GPU 专家保留的、独立且令人生畏的技能。它只是一种仔细观察并追问“等等，为什么会发生这种情况？”直到答案浮现的纪律。你现在已经拥有了在自己的模型上这样做的词汇和反应能力。打开一个跟踪，形成一个猜测，然后去寻找不匹配之处。

感谢阅读《PyTorch 性能分析》系列。现在去分析点什么吧。🤗

感谢 Noe Flandre 对本文早期草稿的审阅。

这篇博文使用 LLM 进行了润色。这绝不意味着我们让一个 Agent（智能体）在后台运行并让它生成博客。我们团队中有些人的母语不是英语，我们认为 LLM（主要用英语训练）可以纠正愚蠢的语法错误或改写听起来不那么生硬、更清晰的句子。希望这有助于理解“如果是 LLM 生成的，我为什么还要读”这个想法。🤗

---

> 本文由AI自动翻译，原文链接：[Profiling in PyTorch (Part 3): Attention is all you profile](https://huggingface.co/blog/torch-attention-profile)
> 
> 翻译时间：2026-07-11 05:27
