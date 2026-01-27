---
title: 利用Hugging Face轻松构建与分享ROCm内核
title_original: Easily Build and Share ROCm Kernels with Hugging Face
date: '2025-11-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/build-rocm-kernels
author: null
summary: 本文介绍了如何使用Hugging Face的kernel-builder和kernels库来构建、测试和分享针对AMD GPU优化的ROCm兼容内核。文章以RadeonFlow
  GEMM内核为例，详细说明了从项目结构配置到集成至PyTorch工作流的完整步骤，旨在帮助开发者高效实现高性能、可移植的自定义GPU内核，并促进其在社区中的共享与应用。
categories:
- AI基础设施
tags:
- ROCm
- Hugging Face
- GPU内核
- PyTorch扩展
- 高性能计算
draft: false
translated_at: '2026-01-06T01:08:14.564Z'
---

轻松使用 Hugging Face 构建和分享 ROCm 内核

简介
自定义内核是高性能深度学习的支柱，它能实现针对您特定工作负载（无论是图像处理、张量变换还是其他计算密集型任务）量身定制的 GPU 操作。但是，为正确的架构编译这些内核、配置所有构建标志并将其干净地集成到 PyTorch 扩展中，可能会迅速演变成一团 CMake/Nix、编译器错误和 ABI 问题的乱麻，这并不有趣。Hugging Face 的 kernel-builder 和 kernels 库让与 kernels 社区分享这些内核变得容易，并支持包括 CUDA、ROCm、Metal 和 XPU 在内的多种 GPU 和加速器后端。这确保了您的内核快速、可移植，并能与 PyTorch 无缝集成。

在本指南中，我们将专门关注 ROCm 兼容内核，并展示如何使用 kernel-builder 构建、测试和分享它们。您将学习如何创建能在 AMD GPU 上高效运行的内核，以及关于可复现性、打包和部署的最佳实践。

这份针对 ROCm 的详细教程是原始 kernel-builder 指南的精简版本。如果您在寻找更广泛的、以 CUDA 为中心的版本，可以在这里找到：构建和扩展生产就绪 CUDA 内核指南。

构建步骤
我们将以 RadeonFlow_Kernels 中的 GEMM 内核为例。如果您想直接跳转到指南，请点击此处。

关于该内核
本节由 RadeonFlow GEMM 内核的作者撰写，用于介绍该内核。

作者：ColorsWind, Zesen Liu, 和 Andy

RadeonFlow GEMM 内核是一个高性能的 FP8 分块矩阵乘法实现，针对 AMD Instinct MI300X GPU 进行了优化。GEMM（通用矩阵乘法）是大多数深度学习工作负载背后的核心构建模块：给定两个矩阵 A 和 B，您计算它们的乘积 C = A × B。这里它使用 FP8 实现，这是一种低精度浮点格式，以牺牲少量精度为代价，换取更高的吞吐量和更低的内存带宽。该内核是为 2025 年 AMD 开发者挑战赛开发的，并于 2025 年 6 月荣获 🏆 大奖，以表彰其在 AMD 硬件上的卓越性能和创新能力。

该内核使用 e4m3fnuz 浮点格式对量化输入进行操作，并应用逐块缩放以在低精度计算期间保持准确性。e4m3fnuz 格式是一种具有 4 个指数位和 3 个尾数位的 FP8 变体，专为神经网络工作负载高效设计。由于 FP8 的动态范围比 FP16/FP32 小得多，我们应用逐块缩放因子（a_scale 和 b_scale），以便在计算前后将每个数值块重新缩放到数值上“舒适”的范围内，这有助于在低精度下保持准确性。它接受以下参数：
(a, b, a_scale, b_scale, c)
其中 a 和 b 是输入矩阵，a_scale 和 b_scale 分别是 a 和 b 的缩放因子，c 是输出矩阵：
a 是 K × M，格式为 e4m3fnuz
b 是 K × N，格式为 e4m3fnuz
a_scale 是 (K // 128) × M，格式为 fp32
b_scale 是 (K // 128) × (N // 128)，格式为 fp32
c 是 M × N，格式为 bf16

该内核已为特定矩阵形状预编译，并假设采用转置内存布局（如竞赛要求）。要支持其他形状或替代内存布局，您必须修改内核启动器。

那么，现在我们有了一个高性能的 ROCm 内核，自然而然的问题是：我们如何将其集成到真实的 PyTorch 工作流中并与他人分享？这正是我们接下来要介绍的内容，使用 kernel-builder 和 kernels 来构建、构建和发布 ROCm 内核。

这是一个技术性较强的指南，但您仍然可以一步一步地遵循它，即使不理解每个细节，一切也都能正常工作。如果您感到好奇，可以随时回过头来更深入地研究这些概念。

步骤 1：项目结构
Hugging Face Kernel Builder 期望您的文件按如下方式组织：
gemm/
├── build.toml
├── gemm
│ └── gemm_kernel.h
├── flake.nix
└── torch-ext
├── torch_binding.cpp
├── torch_binding.h
└── gemm
└── __init__.py

- build.toml：项目清单；它是构建过程的核心。
- gemm/：您的原始 CUDA 源代码，GPU 魔法发生的地方。
- flake.nix：实现完美可复现构建环境的关键。
- torch-ext/gemm/：原始 PyTorch 算子的 Python 包装器

有时您的项目可能依赖于其他文件，例如测试或辅助脚本，您可以毫无问题地添加它们。在我们的例子中，我们的项目结构将如下所示：
gemm/
├── build.toml
├── gemm
│ ├── gemm_kernel.h
│ ├── gemm_kernel_legacy.h
│ ├── transpose_kernel.h
│ └── gemm_launcher.hip
├── include
│ ├── clangd_workaround.h
│ ├── gpu_libs.h
│ ├── gpu_types.h
│ └── timer.h
├── src/utils
│ ├── arithmetic.h
│ └── timer.hip
├── tests/checker
│ ├── checker.cpp
│ ├── metrics.h
│ └── checker.h
├── flake.nix
└── torch-ext
├── torch_binding.h
└── gemm
└── __init__.py

如果您查看 RadeonFlow Kernels 中 gemm 内核的原始文件，它们是带有 .cpp 扩展名的 HIP 源文件。作为第一步，您需要根据其内容和用途将这些扩展名更改为 .h 或 .hip：
- 对于包含内核声明、内联函数或将被其他文件包含的模板代码的头文件，使用 .h
- 对于包含需要单独编译的 HIP/GPU 代码的实现文件（例如，内核启动器、具有复杂实现的设备函数），使用 .hip

在我们的示例中，gemm_kernel.h、gemm_kernel_legacy.h 和 transpose_kernel.h 是头文件，而 gemm_launcher.hip 是 HIP 实现文件。这种命名约定有助于 kernel-builder 正确识别和编译每种文件类型。

步骤 2：配置文件设置

build.toml 清单
此文件编排整个构建过程。它告诉 kernel-builder 要编译什么以及所有内容如何连接。
[general]
name = "gemm"
universal = false
[torch]
src = [
"torch-ext/torch_binding.cpp",
"torch-ext/torch_binding.h",
]
[kernel.gemm]
backend = "rocm"
rocm-archs = [
"gfx942",
]
depends = ["torch"]
src = [
"include/clangd_workaround.h",
"include/gpu_libs.h",
"include/gpu_types.h",
"include/timer.h",
"gemm/gemm_kernel.h",
"gemm/gemm_kernel_legacy.h",
"gemm/gemm_launcher.hip",
"gemm/transpose_kernel.h",
"src/utils/arithmetic.h",
"src/utils/timer.hip",
"tests/checker/metrics.h",
]
include = ["include"]

general
此部分包含常规项目配置设置。
- name（必需）：您的项目名称。这应与您的内核名称匹配，并将用于 Python 包。
- universal（可选）：当设置为 true 时，内核是通用内核。通用内核是纯 Python 包（无编译文件）。通用内核不使用下面描述的其他部分。Triton 内核是通用内核的一个很好的例子。默认值：false

torch
此部分描述 Torch 扩展配置。它定义了将您的内核暴露给 PyTorch 的 Python 绑定。
- src（必需）：PyTorch 扩展的源文件和头文件列表。在我们的例子中，这包括创建 Python 接口的 C++ 绑定文件。

kernel.gemm
名为 "gemm" 的内核规范。如果您有多个内核，可以在同一个 build.toml 文件中定义多个 kernel 部分。
- backend（必需）：内核的计算后端。我们使用 "rocm" 来支持 AMD GPU。
- rocm-archs（ROCm 必需）：内核应为其编译的 ROCm 架构列表。"gfx942" 针对 MI300 系列 GPU。
- depends（必需）：依赖项列表。我们依赖 "torch" 来使用 PyTorch 的张量操作。
- include（可选）：相对于项目根目录的包含目录。这有助于编译器找到头文件。

flake.nix 可复现性文件
为了确保任何人都能在任何机器上构建您的内核，我们使用 flake.nix 文件。

它会锁定 kernel-builder 及其依赖项的确切版本。（你可以直接复制粘贴此示例并修改描述）
{
description = "用于 GEMM 核的 Flake";
inputs = {
kernel-builder.url = "github:huggingface/kernel-builder";
};
outputs =
{
self,
kernel-builder,
}:
kernel-builder.lib.genFlakeOutputs {
inherit self;
path = ./.;
};
}

**编写核函数**

现在来看 GPU 代码。在 `gemm/gemm_launcher.hip` 中，我们定义了如何启动 GEMM 核函数。
根据配置，我们要么调用新的优化版 `gemm/gemm_kernel`，要么回退到旧版实现（`gemm/gemm_kernel_legacy`）。

```cpp
// ... 之前的包含和定义

extern "C" void run(
    void *a, void *b, void *as, void *bs, void *c,
    int m, int n, int k,
    PerfMetrics *metrics, hipStream_t job_stream0
) {
    const __FP8_TYPE *a_ptr = static_cast<const __FP8_TYPE *>(a);
    const __FP8_TYPE *b_ptr = static_cast<const __FP8_TYPE *>(b);
    __BF16_TYPE *c_ptr = static_cast<__BF16_TYPE *>(c);
    const float *as_ptr = static_cast<const float *>(as);
    const float *bs_ptr = static_cast<const float *>(bs);

    KernelTimerScoped timer(timers, 2LL * m * n * k,
                            metrics ? &metrics->entries[0].time : nullptr,
                            metrics ? &metrics->entries[0].gflops : nullptr, job_stream0);

    // 将 GEMM 分派到最快的可用实现
    switch (pack_shape(m, n, k)) {
        DISPATCH_GEMM(1024, 1536, 7168, 256, 128, 128, 4, 2, 512, 4, 16);
        DISPATCH_GEMM(6144, 7168, 2304, 256, 128, 128, 4, 2, 512, 1, 16);
        default: {
            printf("Error: Unsupported shape M=%d, K=%d, N=%d\n", m, k, n);
            abort();
        }
    }
}
// ...
```

**注册原生 PyTorch 算子**

这一步很关键。我们不仅仅是让这个函数在 Python 中可用；我们将其转变为一个原生的 PyTorch 算子。这意味着它成为 PyTorch 本身的一等公民，可以通过 `torch.ops` 访问。

文件 `torch-ext/torch_binding.cpp` 处理此注册。

```cpp
#include <torch/all.h>
#include <torch/library.h>
#include <hip/hip_runtime.h>
#include "registration.h"
#include "torch_binding.h"

// 来自 gemm_launcher.hip 的 C 函数的前向声明
extern "C" {
    struct PerfMetrics;
    void run(void *a, void *b, void *as, void *bs, void *c, int m, int n, int k, PerfMetrics *metrics, hipStream_t job_stream0);
}

void gemm(torch::Tensor &out, torch::Tensor const &a, torch::Tensor const &b,
          torch::Tensor const &as, torch::Tensor const &bs) {
    // 验证张量属性
    TORCH_CHECK(a.device().is_cuda(), "Input tensor a must be on GPU device");
    TORCH_CHECK(b.device().is_cuda(), "Input tensor b must be on GPU device");
    TORCH_CHECK(as.device().is_cuda(), "Scale tensor as must be on GPU device");
    TORCH_CHECK(bs.device().is_cuda(), "Scale tensor bs must be on GPU device");
    TORCH_CHECK(out.device().is_cuda(), "Output tensor out must be on GPU device");

    TORCH_CHECK(a.is_contiguous(), "Input tensor a must be contiguous");
    TORCH_CHECK(b.is_contiguous(), "Input tensor b must be contiguous");
    TORCH_CHECK(as.is_contiguous(), "Scale tensor as must be contiguous");
    TORCH_CHECK(bs.is_contiguous(), "Scale tensor bs must be contiguous");
    TORCH_CHECK(out.is_contiguous(), "Output tensor out must be contiguous");

    // 从张量形状获取矩阵维度
    // 假设 a 是 [M, K], b 是 [K, N], out 是 [M, N]
    int M = a.size(0);
    int K = a.size(1);
    int N = b.size(1);

    TORCH_CHECK(b.size(0) == K, "Matrix dimensions mismatch: a.size(1) != b.size(0)");
    TORCH_CHECK(out.size(0) == M, "Output tensor dimension mismatch: out.size(0) != M");
    TORCH_CHECK(out.size(1) == N, "Output tensor dimension mismatch: out.size(1) != N");

    // 使用默认 HIP 流（流 0）
    const hipStream_t stream = 0;

    // 调用 C 函数
    run(a.data_ptr(), b.data_ptr(), as.data_ptr(), bs.data_ptr(), out.data_ptr(),
        M, N, K, nullptr, stream);
}

TORCH_LIBRARY_EXPAND(TORCH_EXTENSION_NAME, ops) {
    ops.def("gemm(Tensor! out, Tensor a, Tensor b, Tensor a_scale, Tensor b_scale) -> ()");
    ops.impl("gemm", torch::kCUDA, &gemm);
}

REGISTER_EXTENSION(TORCH_EXTENSION_NAME)
```

`torch_binding.h` 文件包含函数声明。例如，`gemm` 核函数在 `torch_binding.h` 中有以下声明：

```cpp
#pragma once
#include <torch/torch.h>

          torch::Tensor const &as, torch::Tensor const &bs);
```

**设置 `__init__.py` 包装器**

在 `torch-ext/gemm/` 中，我们需要一个 `__init__.py` 文件来使此目录成为一个 Python 包，并以用户友好的方式公开我们的自定义算子。

```python
from typing import Optional
import torch
from ._ops import ops

def gemm(a: torch.Tensor, b: torch.Tensor, as_: torch.Tensor, bs: torch.Tensor,
         out: Optional[torch.Tensor] = None) -> torch.Tensor:
    if out is None:
        # 创建具有适当形状和数据类型的输出张量
        M, K = a.shape
        K_b, N = b.shape
        assert K == K_b, f"Matrix dimension mismatch: A has {K} cols, B has {K_b} rows"
        # 输出应为与输入相同设备上的 BF16 类型
        out = torch.empty((M, N), dtype=torch.bfloat16, device=a.device)

    ops.gemm(out, a, b, as_, bs)
    return out
```

**步骤 3：构建核函数**

核函数构建器使用 Nix 来构建核函数。如果你的系统上安装了 Nix，可以直接构建或运行核函数。我们建议按以下方式安装 Nix：
- Linux：使用官方的 Nix 安装程序。
- macOS：使用 Determinate Nix 安装程序。此外，目前构建核函数需要 Xcode 16.x。

**Nix 入门**

首先，运行以下命令：
```
nix flake update
```
这会生成一个 `flake.lock` 文件，用于锁定核函数构建器及其所有传递依赖项。将 `flake.nix` 和 `flake.lock` 都提交到你的仓库，以确保核函数构建是可复现的。

由于核函数构建器依赖许多包（例如，每个受支持的 PyTorch 版本），建议启用 Hugging Face 缓存以避免昂贵的重新构建：
```bash
# 安装 cachix 并配置缓存
cachix use huggingface
```
或者，在不永久安装 cachix 的情况下运行一次：
```bash
# 使用 cachix 但不安装它
nix run nixpkgs#cachix -- use huggingface
```

**使用 Nix 构建核函数**

拥有 `flake.nix` 文件的核函数可以使用 `build-and-copy` 命令构建：
```bash
cd Build_RadeonFlow_Kernels/gemm
nix build . -L
```
编译后的核函数将位于本地的 `build/` 目录中。

**用于本地开发的开发环境**

kernel-builder 提供了用于开发核函数的环境。在这样的环境中，所有必需的依赖项都可用，并且可以使用 `build2cmake` 来生成项目文件：
```bash
$ nix develop
$ build2cmake generate-torch build.toml
$ cmake -B build-ext
$ cmake --build build-ext
```
如果你想将核函数作为 Python 包进行测试，也可以这样做。`nix develop` 会自动在 `.venv` 中创建并激活一个虚拟环境：
```bash
$ nix develop
$ pip install --no-build-isolation -e .
```
每个构建配置都有对应的开发环境。例如，你可以使用以下命令获得一个带有 ROCm 6.3 的 Torch 2.7 开发环境：
```bash
$ rm -rf .venv # 如果存在，删除现有的 venv
$ nix develop .#devShells.torch27-cxx11-rocm63-x86_64-linux
```

**步骤 4：将核函数上传到 Hub**

现在我们已经构建了核函数，可以对其进行测试并上传到 Hub。

**为所有 PyTorch 和 ROCm 版本构建核函数**

在分享之前，我们想做的一件小事是清理构建过程中生成的所有开发工件，以避免上传不必要的文件。
```bash
build2cmake clean build.toml
```
要为所有受支持的 PyTorch 和 ROCm 版本构建核函数，kernel-builder 工具可以自动化此过程：
```bash
# 在开发环境之外，运行以下命令
# 如果你在沙盒内，可以用 `exit` 退出
nix build .
```

**注意：**
此过程可能需要一些时间，因为它将为所有受支持的 PyTorch 和 ROCm 版本构建内核。
输出将位于 `result` 目录中。
最后一步是将结果移动到预期的构建目录（这是内核库将查找它们的位置）。
```
mkdir -p build
rsync -av --delete --chmod=Du+w,Fu+w result/ build/
```

**推送到 Hugging Face Hub**
将构建产物推送到 Hub 将使其他开发者能够轻松使用你的内核。
首先，创建一个新的仓库：
```
hf repo create gemm
```
确保你已使用 `huggingface-cli login` 登录到 Hugging Face Hub。
现在，在你的项目目录中，将你的项目连接到新仓库并推送你的代码：
```
# 初始化 git 并连接到 Hugging Face Hub
git init
git remote add origin https://huggingface.co/<你的用户名>/gemm
# 拉取变更（仅默认的 .gitattributes 文件）
git pull origin main
git xet install
git checkout -b main
# 更新以使用 Xet 处理二进制文件
git xet track "*.so"
# 添加并提交你的更改（注意只包含必要的文件，
# 因为我们的 build2cmake 命令生成了许多开发专用的文件）
git add \
build/ gemm/ include/ src/utils tests/checker \
torch-ext/torch_binding.cpp torch-ext/torch_binding.h torch-ext/gemm \
flake.nix flake.lock build.toml
git commit -m "feat: Created a compliant gemm kernel"
git push -u origin main
```
太棒了！你的内核现在已在 Hugging Face Hub 上，可供他人使用，并且完全符合内核库的要求。

**步骤 5：让我们使用它 :)**
使用内核库时，你不需要以传统方式“安装”内核。你可以直接从其 Hub 仓库加载它，这将自动注册新的算子。
```python
import torch
from kernels import get_kernel

# 从 Hub 加载内核
gemm = get_kernel("kernels-community/gemm")

# 矩阵维度（必须受支持 - 参见 gemm_launcher.cpp）
M, N, K = 1024, 1536, 7168
QUANT_SIZE = 128

# 设置设备
device = torch.device("cuda")

# 创建输入 - 内核期望 A:(K,M), B:(K,N)
A_fp32 = torch.randn(M, K, device=device)
B_fp32 = torch.randn(K, N, device=device)

# 转换为 FP8
A_fp8 = A_fp32.to(torch.float8_e4m3fnuz)
B_fp8 = B_fp32.to(torch.float8_e4m3fnuz)

# 创建缩放因子（统一缩放）
A_scale = torch.ones(K // QUANT_SIZE, M, device=device, dtype=torch.float32)
B_scale = torch.ones(K // QUANT_SIZE, N // QUANT_SIZE, device=device, dtype=torch.float32)

C = torch.zeros(M, N, device=device, dtype=torch.bfloat16)

# 使用内核
result = gemm.gemm(A_fp8, B_fp8, A_scale, B_scale, C)
```
就是这样！你的 ROCm 内核现在可以从 Hugging Face Hub 使用了。

**结论**
现在，与 Hugging Face 一起构建和分享 ROCm 内核比以往任何时候都更容易。借助由 Nix 驱动的干净、可复现的工作流程以及与 PyTorch 的无缝集成，开发者可以专注于优化性能，而不是设置环境。一旦构建完成，你的自定义内核就可以在 Hugging Face Hub 上分享；只需几行代码，社区就能立即访问它，并可在各个项目中使用。🚀

**相关库和 Hub**
- kernel-builder – 构建和编译自定义内核。
- kernels – 用于从 Hub 管理和加载内核的库。
- Kernels Community Hub – 分享和发现社区的内核。

> 本文由AI自动翻译，原文链接：[Easily Build and Share ROCm Kernels with Hugging Face](https://huggingface.co/blog/build-rocm-kernels)
> 
> 翻译时间：2026-01-06 01:08
