---
title: 5分钟上手Hugging Face Kernel Hub，轻松提升模型性能
title_original: Learn the Hugging Face Kernel Hub in 5 Minutes
date: '2025-06-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hello-hf-kernels
author: ''
summary: 本文介绍了Hugging Face新推出的Kernel Hub，这是一个用于管理和加载高性能优化计算内核的平台。它允许开发者直接从Hub获取预编译的内核（如FlashAttention、量化内核等），无需手动处理复杂的依赖和编译过程，从而显著简化了模型性能优化工作。文章通过代码示例说明了其基本用法，并阐述了其在简化部署、加速开发、促进社区共享等方面的优势。
categories:
- AI基础设施
tags:
- Hugging Face
- 模型优化
- GPU加速
- 机器学习工具
- AI开发
draft: false
translated_at: '2026-03-31T05:03:37.596085'
---

# 🏎️ 5分钟用Hugging Face Kernel Hub提升模型性能

通过预优化内核提升模型性能，轻松从Hub加载。

今天，我们将探索Hugging Face的一项激动人心的进展：Kernel Hub！作为机器学习从业者，我们都知道最大化性能通常需要深入研究优化代码、自定义CUDA内核或复杂的构建系统。Kernel Hub极大地简化了这一过程！

以下是一个简短的代码示例，展示如何在代码中使用内核。

```python
import torch

from kernels import get_kernel


activation = get_kernel("kernels-community/activation")


x = torch.randn((10, 10), dtype=torch.float16, device="cuda")


y = torch.empty_like(x)
activation.gelu_fast(y, x)

print(y)

```

在接下来的章节中，我们将涵盖以下主题：

1. 什么是Kernel Hub？- 理解核心概念。
2. 如何使用Kernel Hub - 一个快速代码示例。
3. 将内核添加到简单模型 - 使用RMSNorm的实际集成示例。
4. 评估性能影响 - 对RMSNorm差异进行基准测试。
5. 实际应用案例 - 其他项目如何使用内核库的示例。

我们将快速介绍这些概念——核心思想大约5分钟就能掌握（尽管实验和基准测试可能需要更长时间！）。

## 1. 什么是Kernel Hub？

Kernel Hub（👈 点击查看！）允许Python库和应用程序直接从Hugging Face Hub加载优化的计算内核。可以将其视为模型Hub，但用于加速特定操作（通常在GPU上）的低层、高性能代码片段（内核）。

示例包括：高级注意力机制（如FlashAttention，可显著提升速度并节省内存）。自定义量化内核（支持使用INT8或INT4等低精度数据类型进行高效计算）。复杂架构所需的专用内核，如专家混合（MoE）层，涉及复杂的路由和计算模式。以及激活函数和归一化层（如LayerNorm或RMSNorm）。

无需手动管理复杂的依赖关系、处理编译标志或从源代码构建Triton或CUTLASS等库，您可以使用kernels库即时获取并运行预编译的优化内核。

例如，启用FlashAttention只需一行代码——无需构建，无需标志：

```python
from kernels import get_kernel

flash_attention = get_kernel("kernels-community/flash-attn")

```

kernels会检测您确切的Python、PyTorch和CUDA版本，然后下载匹配的预编译二进制文件——通常只需几秒钟（在慢速连接上可能需要一两分钟）。

相比之下，自行编译FlashAttention需要：

- 克隆仓库并安装所有依赖项。
- 配置构建标志和环境变量。
- 预留约96 GB内存和大量CPU核心。
- 等待10分钟到数小时，具体取决于您的硬件。
（详见项目自身的安装指南。）

Kernel Hub消除了所有这些摩擦：一次函数调用，即时加速。

### Kernel Hub的优势：

- 即时访问优化内核：加载并运行针对各种硬件（从NVIDIA和AMD GPU开始）优化的内核，无需本地编译的麻烦。
- 共享与重用：跨不同项目和社区发现、共享和重用内核。
- 轻松更新：只需从Hub拉取最新版本，即可保持与最新内核改进同步。
- 加速开发：专注于模型架构和逻辑，而非内核编译和部署的复杂性。
- 提升性能：利用专家优化的内核，可能加速训练和推理。
- 简化部署：通过按需获取内核，降低部署环境的复杂性。
- 开发并分享您自己的内核：如果您创建了优化内核，可以轻松在Hub上分享供他人使用。这鼓励了社区内的协作和知识共享。

正如许多机器学习开发者所知，管理依赖关系和从源代码构建底层代码可能是一个耗时且容易出错的过程。Kernel Hub旨在通过提供一个可轻松加载和运行的优化计算内核集中存储库来简化这一过程。

花更多时间构建优秀模型，减少时间与构建系统斗争！

## 2. 如何使用Kernel Hub（基础示例）

Kernel Hub的设计旨在简单易用。kernels库提供了主要接口。以下是一个快速示例，加载一个优化的GELU激活函数内核。（稍后，我们将看到另一个关于如何将内核集成到模型中的示例）。

文件：activation_validation_example.py

```python








import torch
import torch.nn.functional as F
from kernels import get_kernel

DEVICE = "cuda"


torch.manual_seed(42)


activation_kernels = get_kernel("kernels-community/activation")


x = torch.randn((4, 4), dtype=torch.float16, device=DEVICE)


y = torch.empty_like(x)


activation_kernels.gelu_fast(y, x)


expected = F.gelu(x)


torch.testing.assert_close(y, expected, rtol=1e-2, atol=1e-2)

print("✅ Kernel output matches PyTorch GELU!")


print("\nInput tensor:")
print(x)
print("\nFast GELU kernel output:")
print(y)
print("\nPyTorch GELU output:")
print(expected)


print("\nAvailable functions in 'kernels-community/activation':")
print(dir(activation_kernels))

```

（注意：如果您安装了uv，可以将此脚本保存为script.py并运行uv run script.py来自动处理依赖项。）

### 这里发生了什么？

1. 导入get_kernel：此函数是通过kernels库访问Kernel Hub的入口点。
2. get_kernel("kernels-community/activation")：此行在kernels-community组织下查找activation内核仓库。它会下载、缓存并加载相应的预编译内核二进制文件。
3. 准备张量：我们在GPU上创建输入（x）和输出（y）张量。
4. activation_kernels.gelu_fast(y, x)：我们调用加载的内核模块提供的特定优化函数（gelu_fast）。
5. 验证：我们检查输出。

这个简单示例展示了如何轻松获取和执行高度优化的代码。现在，让我们看一个使用RMS归一化的更实际集成示例。

## 3. 将内核添加到简单模型

让我们将优化的RMS归一化内核集成到一个基础模型中。我们将使用kernels-community/triton-layer-norm仓库中提供的LlamaRMSNorm实现（注意：此仓库包含各种归一化内核），并将其与RMSNorm的基线PyTorch实现进行比较。

首先，在PyTorch中定义一个简单的RMSNorm模块，以及一个使用它的基线模型：

文件：rmsnorm_baseline.py

```python







import torch
import torch.nn as nn

DEVICE = "cuda"

DTYPE = torch.float16  



class RMSNorm(nn.Module):
    def __init__(self, hidden_size, variance_epsilon=1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = variance_epsilon
        self.hidden_size = hidden_size

    def forward(self, x):
        
        input_dtype = x.dtype
        
        variance = x.to(torch.float32).pow(2).mean(-1, keepdim=True)
        x = x * torch.rsqrt(variance + self.eps)

        
        return (self.weight * x).to(input_dtype)


class BaselineModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, eps=1e-5):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.norm = RMSNorm(hidden_size, variance_epsilon=eps)
        self.activation = nn.GELU()
        self.linear2 = nn.Linear(hidden_size, output_size)

        
        with torch.no_grad():
            self.linear1.weight.fill_(1)
            self.linear1.bias.fill_(0)
            self.linear2.weight.fill_(1)
            self.linear2.bias.fill_(0)
            self.norm.weight.fill_(1)

```python
def forward(self, x):
        x = self.linear1(x)
        x = self.norm(x)  
        x = self.activation(x)
        x = self.linear2(x)
        return x



input_size = 128
hidden_size = 256
output_size = 10
eps_val = 1e-5

baseline_model = (
    BaselineModel(input_size, hidden_size, output_size, eps=eps_val)
    .to(DEVICE)
    .to(DTYPE)
)
dummy_input = torch.randn(32, input_size, device=DEVICE, dtype=DTYPE)  
output = baseline_model(dummy_input)
print("Baseline RMSNorm model output shape:", output.shape)

```

现在，让我们创建一个使用通过 `kernels` 加载的 `LlamaRMSNorm` 内核的版本。

文件：`rmsnorm_kernel.py`

```python







import torch
import torch.nn as nn
from kernels import get_kernel, use_kernel_forward_from_hub



from rmsnorm_baseline import BaselineModel

DEVICE = "cuda"
DTYPE = torch.float16  


layer_norm_kernel_module = get_kernel("kernels-community/triton-layer-norm")



















@use_kernel_forward_from_hub("LlamaRMSNorm")
class OriginalRMSNorm(nn.Module):
    def __init__(self, hidden_size, variance_epsilon=1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = variance_epsilon
        self.hidden_size = hidden_size

    def forward(self, x):
        
        input_dtype = x.dtype
        
        variance = x.to(torch.float32).pow(2).mean(-1, keepdim=True)
        x = x * torch.rsqrt(variance + self.eps)

        
        return (self.weight * x).to(input_dtype)


class KernelModel(nn.Module):
    def __init__(
        self,
        input_size,
        hidden_size,
        output_size,
        device="cuda",
        dtype=torch.float16,
        eps=1e-5,
    ):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        
        
        self.norm = OriginalRMSNorm(hidden_size, variance_epsilon=eps)
        self.activation = nn.GELU()
        self.linear2 = nn.Linear(hidden_size, output_size)

        
        with torch.no_grad():
            self.linear1.weight.fill_(1)
            self.linear1.bias.fill_(0)
            self.linear2.weight.fill_(1)
            self.linear2.bias.fill_(0)
            self.norm.weight.fill_(1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.linear2(x)
        return x



input_size = 128
hidden_size = 256
output_size = 10
eps_val = 1e-5

kernel_model = (
    KernelModel(
        input_size, hidden_size, output_size, device=DEVICE, dtype=DTYPE, eps=eps_val
    )
    .to(DEVICE)
    .to(DTYPE)
)

baseline_model = (
    BaselineModel(input_size, hidden_size, output_size, eps=eps_val)
    .to(DEVICE)
    .to(DTYPE)
)

dummy_input = torch.randn(32, input_size, device=DEVICE, dtype=DTYPE)  

output = baseline_model(dummy_input)
output_kernel = kernel_model(dummy_input)
print("Kernel RMSNorm model output shape:", output_kernel.shape)


try:
    torch.testing.assert_close(output, output_kernel, rtol=1e-2, atol=1e-2)
    print("\nBaseline and Kernel RMSNorm model outputs match!")
except AssertionError as e:
    print("\nBaseline and Kernel RMSNorm model outputs differ slightly:")
    print(e)
except NameError:
    print("\nSkipping output comparison as kernel model output was not generated.")


```

关于 `KernelModel` 的重要说明：

- **内核继承**：`KernelRMSNorm` 类继承自 `layer_norm_kernel_module.layers.LlamaRMSNorm`，这是内核中的 RMSNorm 实现。这使我们能够直接使用优化的内核。
- **访问函数**：访问 RMSNorm 函数的确切方式（`layer_norm_kernel_module.layers.LlamaRMSNorm.forward`、`layer_norm_kernel_module.rms_norm_forward` 或其他）**完全取决于内核创建者在 Hub 上如何构建其代码库**。您可能需要检查加载的 `layer_norm_kernel_module` 对象（例如，使用 `dir()`）或查看 Hub 上该内核的文档，以找到正确的函数/方法及其签名。我使用了 `rms_norm_forward` 作为一个合理的占位符，并添加了错误处理。
- **参数**：我们现在只定义 `rms_norm_weight`（无偏置），这与 RMSNorm 保持一致。

## 4. 性能影响基准测试

优化的 Triton RMSNorm 内核与标准 PyTorch 版本相比快多少？让我们对前向传播进行基准测试来找出答案。

文件：`rmsnorm_benchmark.py`

```python







import torch



from rmsnorm_baseline import BaselineModel
from rmsnorm_kernel import KernelModel

DEVICE = "cuda"
DTYPE = torch.float16  



def benchmark_model(model, input_tensor, num_runs=100, warmup_runs=10):
    model.eval()  
    dtype = input_tensor.dtype
    model = model.to(input_tensor.device).to(dtype)

    
    for _ in range(warmup_runs):
        _ = model(input_tensor)
    torch.cuda.synchronize()

    
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    start_event.record()
    for _ in range(num_runs):
        _ = model(input_tensor)
    end_event.record()
    torch.cuda.synchronize()
    elapsed_time_ms = start_event.elapsed_time(end_event)
    avg_time_ms = elapsed_time_ms / num_runs
    return avg_time_ms


input_size_bench = 4096
hidden_size_bench = 4096  
output_size_bench = 10
eps_val_bench = 1e-5



baseline_model_bench = (
    BaselineModel(
        input_size_bench, hidden_size_bench, output_size_bench, eps=eps_val_bench
    )
    .to(DEVICE)
    .to(DTYPE)
)
kernel_model_bench = (
    KernelModel(
        input_size_bench,
        hidden_size_bench,
        output_size_bench,
        device=DEVICE,
        dtype=DTYPE,
        eps=eps_val_bench,
    )
    .to(DEVICE)
    .to(DTYPE)
)



warmup_input = torch.randn(4096, input_size_bench, device=DEVICE, dtype=DTYPE)
_ = kernel_model_bench(warmup_input)
_ = baseline_model_bench(warmup_input)

batch_sizes = [
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
]

print(
    f"{'Batch Size':<12} | {'Baseline Time (ms)':<18} | {'Kernel Time (ms)':<18} | {'Speedup'}"
)
print("-" * 74)

for batch_size in batch_sizes:
    
    torch.cuda.synchronize()

    
    
    bench_input = torch.randn(batch_size, input_size_bench, device=DEVICE, dtype=DTYPE)

    
    baseline_time = benchmark_model(baseline_model_bench, bench_input)

    kernel_time = -1  

    kernel_time = benchmark_model(kernel_model_bench, bench_input)

    baseline_time = round(baseline_time, 4)
    kernel_time = round(kernel_time, 4)
    speedup = round(baseline_time / kernel_time, 2) if kernel_time > 0 else "N/A"
    if kernel_time < baseline_time:
        speedup = f"{speedup:.2f}x"
    elif kernel_time == baseline_time:
        speedup = "1.00x (identical)"
    else:
        speedup = f"{kernel_time / baseline_time:.2f}x slower"
    print(f"{batch_size:<12} | {baseline_time:<18} | {kernel_time:<18} | {speedup}")

```

预期结果：与 LayerNorm 一样，使用 Triton 精心调优的 RMSNorm 实现相比 PyTorch 的默认版本可以带来显著的加速——尤其是在兼容硬件（例如，NVIDIA Ampere 或 Hopper GPU）上处理内存密集型工作负载，并使用低精度类型如 `float16` 或 `bfloat16` 时。

请记住：

- 结果可能因您的 GPU、输入大小和数据类型而异。
- 微基准测试可能无法真实反映实际性能。
- 性能取决于内核实现的质量。
- 由于开销，优化后的内核可能对小批量大小没有益处。

实际结果将取决于您的硬件和特定的内核实现。以下是您可能看到的结果示例（在 L4 GPU 上）：

## 5. 实际应用场景

`kernels` 库仍在发展中，但已在各种实际项目中使用，包括：

- 文本生成推理：TGI项目使用kernels库加载针对文本生成任务优化的内核，以提升性能和效率。
- Transformers：Transformers库已集成kernels库，可直接使用优化层而无需修改模型代码。这使得用户能够轻松在标准实现与优化实现之间切换。

## 快速开始与后续步骤！

您已经了解了通过Hugging Face Kernel Hub获取和使用优化内核是多么简单。准备好亲自尝试了吗？

1. 安装库：`pip install kernels torch numpy` 请确保已安装兼容的PyTorch版本和GPU驱动。
2. 浏览Hub：在Hugging Face Hub上通过`kernels`标签或在`kernels-community`等组织内探索可用内核。寻找与您所需操作相关的内核（激活函数、注意力机制、归一化如LayerNorm/RMSNorm等）。
3. 实验：尝试替换您自己模型中的组件。使用`get_kernel("用户或组织名/内核名")`。关键是要检查加载的内核对象（例如`print(dir(loaded_kernel))`）或查阅其Hub仓库文档，以了解如何正确调用其函数/方法以及它需要哪些参数（权重、偏置、输入、epsilon等）。
4. 基准测试：测量其对您特定硬件和工作负载的性能影响。别忘了检查数值正确性（`torch.testing.assert_close`）。
5. （高级）贡献：如果您开发了优化内核，请考虑在Hub上分享！

安装库：

```bash
pip install kernels torch numpy
```

请确保已安装兼容的PyTorch版本和GPU驱动。

浏览Hub：在Hugging Face Hub上通过`kernels`标签或在`kernels-community`等组织内探索可用内核。寻找与您所需操作相关的内核（激活函数、注意力机制、归一化如LayerNorm/RMSNorm等）。

实验：尝试替换您自己模型中的组件。使用`get_kernel("用户或组织名/内核名")`。关键是要检查加载的内核对象（例如`print(dir(loaded_kernel))`）或查阅其Hub仓库文档，以了解如何正确调用其函数/方法以及它需要哪些参数（权重、偏置、输入、epsilon等）。

基准测试：测量其对您特定硬件和工作负载的性能影响。别忘了检查数值正确性（`torch.testing.assert_close`）。

（高级）贡献：如果您开发了优化内核，请考虑在Hub上分享！

## 结论

Hugging Face Kernel Hub提供了一种强大而简单的方式来访问和利用优化的计算内核。通过将标准PyTorch组件替换为针对RMS归一化等操作的优化版本，您有可能在不涉及传统自定义构建复杂性的情况下，获得显著的性能提升。请记得查阅Hub上每个内核的具体说明以确保正确使用。尝试一下，看看它如何加速您的工作流程！

---

> 本文由AI自动翻译，原文链接：[Learn the Hugging Face Kernel Hub in 5 Minutes](https://huggingface.co/blog/hello-hf-kernels)
> 
> 翻译时间：2026-03-31 05:03
