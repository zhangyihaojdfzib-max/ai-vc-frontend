---
title: Hugging Face内核项目重大更新
title_original: '🤗 Kernels: Major Updates'
date: '2026-07-06'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/revamped-kernels
author: ''
summary: Hugging Face的🤗 Kernels项目迎来重大更新，旨在标准化自定义内核的打包、分发与使用。主要更新包括：引入新的“kernel”仓库类型，提升内核可发现性；加强安全性，引入可信发布者机制和代码签名，防止恶意内核；重构CLI，明确kernels与kernel-builder的分工；扩展框架和后端支持，为智能体内核开发奠定基础。这些改进使内核加载更安全、更易用，推动AI生态系统的健康发展。
categories:
- AI基础设施
tags:
- Hugging Face
- 内核
- 安全性
- CLI
- AI基础设施
draft: false
translated_at: '2026-07-06T06:50:23.905231'
---

# 🤗 Kernels：重大更新

在上一篇文章《从零到GPU》中，我们介绍了🤗 Kernels项目，该项目旨在标准化自定义内核的打包、分发和使用方式。我们希望该项目既无摩擦又安全，同时尽可能与Hub友好兼容。

过去几个月，我们一直朝着这个目标努力。在此过程中，我们几乎完全重新设计了该项目。本文将总结我们已发布的主要更新以及未来的规划。

- Kernels——一种新的仓库类型
- 改进的安全性
- 重构的CLI
- 更广泛的框架和后端支持
- Agent（智能体）内核开发的基础
- 其他
- 结论

## Kernels——一种新的仓库类型

我们在Hub上引入了一种名为"kernel"的新仓库类型。这使得我们能够满足具有计算相关特定需求的用户。例如，用户可以了解某个内核支持哪些加速器、操作系统和后端版本：

![内核页面：kernels-community/flash-attn3](/images/posts/666f9751b804.png)

用户可以在以下地址浏览Hub上所有可用的内核：https://huggingface.co/kernels。

将这些内核作为Hub的一等公民也有利于AI生态系统。用户现在可以查看内核、模型以及使用它们的应用程序的趋势。内核对用户来说更容易被发现。

## 改进的安全性

内核以与加载它们的Python进程相同的权限运行原生代码，因此恶意内核可能造成实际损害。因此，安全性一直是Kernels项目的重中之重。

这就是我们早期专注于可重现性的原因：你应该能够自己重新编译内核，并验证其与公开可用的源代码是否匹配。我们使用Nix来实现这一点，因为它通过对构建配方进行封闭评估和强隔离沙箱来保持构建的纯净性。我们通过将源代码Git SHA1嵌入内核本身来进一步提高来源可追溯性。

近几个月来，我们增加了额外的防御层：可信内核发布者和代码签名。

### 可信内核发布者

随着新仓库类型的引入，我们还引入了"可信发布者"。由于内核在机器上执行代码时具有与其使用的Python进程相同的权限，攻击者可能通过上传恶意内核并诱使你使用该内核来危害机器。为了帮助你避免此类恶意内核，内核包现在默认只加载来自可信发布者的内核。可信发布者是社区信任其诚信行事的组织。

我们仍然支持加载来自非可信发布者的组织或用户的内核，但你必须在使用`trust_remote_code`参数从Hub加载内核时明确选择加入：

```py
from kernels import get_kernel

kernel_module = get_kernel(  
   "Atlas-Inference/gdn", version=1, trust_remote_code=True  
)  

```

默认情况下，用户不能在Hub上发布内核仓库。他们必须申请成为内核发布者。用户和组织可以从其账户设置中请求访问权限。这使我们有时间逐案处理这些请求。

### 内核签名

我们正在添加的另一个安全层是代码签名。代码签名可以防止攻击者利用Hub凭据被泄露的可信发布者，向其内核仓库上传恶意内核的情况。在代码签名中，内核使用只有内核开发者知道的私钥进行签名，并使用公开可用的公钥进行验证。在Hub被攻破的情况下，攻击者无法签署恶意内核，因为他们没有签名所需的私钥。

为了进一步提高安全性，我们使用Sigstore的cosign通过临时私钥进行签名。由于这些签名密钥仅在有限时间内有效，攻击者通常无法使用私钥，即使它被泄露。我们还会验证内核是否由受信任的GitHub仓库中的受信任GitHub工作流签名。

内核签名已得到`kernel-builder`的支持，并且我们提供了`kernels verify-signature`来验证内核。Kernels在加载内核时尚未验证签名，因为我们希望在全面推出之前进一步测试这一新功能。关于为你的内核设置代码签名的初步说明，可以在kernels 0.16.0版本发布说明中找到：https://github.com/huggingface/kernels/releases/tag/v0.16.0。

## 重构的CLI

以前，许多实用程序在`kernels`和`kernel-builder`之间交织在一起。我们已经在`kernels`和`kernel-builder`的CLI之间建立了更好的关注点分离。这里的心智模型是，`kernels`是一个用于加载和准备内核以供使用的库。因此，它不应包含任何与"构建"内核相关的内容。

因此，`kernels`和`kernel-builder`现在都更加精简和专业化。请参阅文档了解更多信息：

- kernels CLI
- kernel-builder CLI

这种改进的CLI体验也使我们能够更好地适应Agent（智能体）内核开发的兴起。稍后将对此进行更多介绍。

## 更广泛的框架和后端支持

我们扩展了对框架的支持，最显著的变化是：

- 我们为kernels和kernel-builder增加了对Torch Stable ABI的支持。Torch Stable ABI允许内核开发者针对特定的Torch版本或其后大约两年内发布的任何版本。例如，针对Torch 2.9 Stable ABI的内核支持Torch >= 2.9。
- Apache TVM FFI是除Torch之外第一个受支持的框架。TVM FFI是一种标准化的ABI，用于与PyTorch、Jax和CuPy等其他框架互操作的内核。这使得内核开发者可以创建跨框架运行的内核。

## Agent（智能体）内核开发的基础

`kernel-builder`和`kernels`补充了Agent（智能体）内核开发的兴起，其中利用Agent从头开始创建（优化的）内核。它们共同支持一个工作流，在该工作流中，Agent可以搭建、构建、基准测试和迭代优化内核。

Agent（智能体）内核开发仍处于起步阶段，正确的开发循环将继续演变。这使得简单、清晰的基础知识尤为重要，工具应易于组合到人们选择使用的任何Agent工作流或框架中。

`kernel-builder`有助于强制执行内核源代码应如何搭建和用于执行可重现构建的结构。这为Agent提供了可预测的项目布局和可重复的工作流程。其CLI也旨在针对Agent进行优化。例如，这可能意味着非交互式命令和输出，以便Agent能够以编程方式直接解释。为此，我们还有针对后端的技能，以帮助Agent应对不同后端的特性。这些技能可以捕获特定后端的工具链、编译路径和性能考虑因素。

成功构建内核并不是唯一目标，我们需要确保它在目标硬件上比基线带来实际的加速。因此，成功的构建只是第一个验证步骤。通常，目标硬件可能包括许多不同的加速器，甚至是同一加速器的不同系列。

这使得跨相关硬件供应商和代际评估结果变得重要。我们与HF Jobs的紧密集成使这一基准测试过程变得简单。Agent可以利用此集成运行基准测试套件，收集性能结果，并将其与定义的基线进行比较。

这样，Agent可以跨不同硬件配置运行测试，以获得关于生成内核性能的可靠反馈，并确定需要做什么。然后，该反馈可以为下一次优化迭代提供信息。

以下是Agent（智能体）增强型内核的一些示例。这些示例展示了可通过此工作流开发和评估的内核类型：

- https://huggingface.co/kernels/drbh/yamoe
- https://huggingface.co/kernels/sayakpaul/qk-norm-rope

### 环境设置

使用`kernel-builder`构建内核的环境设置可能较为复杂。为方便用户，我们现在提供了一键安装脚本，可快速完成环境配置。如果您更倾向于使用临时实例，可参考我们的Terraform设置指南。

### 内核系统卡片

内核构建完成后，我们会为每个内核创建系统卡片，以展示包括使用方法及暴露接口在内的有用信息。当内核推送至Hub时，该系统卡片将成为内核的前置说明：

![系统卡片 - kernels-community/flash-attn3](/images/posts/c8854296641d.png)

### 内核是否与我的系统兼容？

这是用户为更好规划而需要多次确认的问题。可使用`has_kernel()`方法进行判断：

```py
from kernels import has_kernel

print(has_kernel("kernels-community/activation", version=1))  
```

该方法返回布尔值。如需了解内核不被支持的详细原因，可使用`get_kernel_variants()`：

```py
 from kernels import get_kernel_variants, VariantAccepted

for decision in get_kernel_variants("kernels-community/activation", version=1):  
    name = decision.variant.variant_str  
    if isinstance(decision, VariantAccepted):  
        print(f"{name}: 兼容")  
    else:  
        print(f"{name}: 不兼容 ({decision.reason})")  
```

输出结果（取决于当前机器）如下：

```bash
torch212-cxx11-cu130-aarch64-linux: 兼容  
torch210-cu128-x86_64-windows: 不兼容 (CPU (x86_64) 与系统 CPU (aarch64) 不匹配)  
torch211-cu128-x86_64-windows: 不兼容 (CPU (x86_64) 与系统 CPU (aarch64) 不匹配)  
torch212-metal-aarch64-darwin: 不兼容 (操作系统 (darwin) 与系统操作系统 (linux) 不匹配)  
torch211-metal-aarch64-darwin: 不兼容 (操作系统 (darwin) 与系统操作系统 (linux) 不匹配)  
torch210-metal-aarch64-darwin: 不兼容 (操作系统 (darwin) 与系统操作系统 (linux) 不匹配)  
torch29-metal-aarch64-darwin: 不兼容 (操作系统 (darwin) 与系统操作系统 (linux) 不匹配)  
…  
```

### 改进的 manylinux_2_28 支持

Kernel-builder 几乎从一开始就针对`manylinux_2_28`进行构建。我们曾通过使用基于 glibc 2.28 编译的现代 gcc 工具链来支持`manylinux`。为避免与旧版`libstdc++`的兼容性问题，我们静态链接了 libstdc++。

然而，这种方法近期引发了一些问题。某些`libstdc++`功能使用了全局初始化。当多个版本的`libstdc++`同时存在时（例如 PyTorch 动态链接的`libstdc++`与内核静态链接的`libstdc++`），可能导致数据损坏。近期一些内核使用了触发全局初始化的功能（如 C++ 正则表达式），进而导致此类数据损坏，引发段错误等问题。

为解决此问题，内核现在改为动态链接`libstdc++`。为确保与旧版`libstdc++`的兼容性，我们使用官方`manylinux_2_28`工具链编译内核。

## 结论

Kernels 项目的目标是为内核开发者及自定义内核用户提供支持。我们始终欢迎社区反馈，以帮助我们持续改进。欢迎贡献您的力量！

致谢：感谢Aritra审阅本文。

---

> 本文由AI自动翻译，原文链接：[🤗 Kernels: Major Updates](https://huggingface.co/blog/revamped-kernels)
> 
> 翻译时间：2026-07-06 06:50
