---
title: Diffusers集成Nunchaku 4-bit量化推理
title_original: Bringing Nunchaku 4-bit Diffusion Inference to Diffusers
date: '2026-07-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nunchaku-diffusers
author: ''
summary: 本文介绍了将Nunchaku 4-bit扩散推理引擎集成到Hugging Face Diffusers库中的方法。Nunchaku基于SVDQuant方法，采用4位权重和激活量化（W4A4），相比传统仅权重量化，能在减少显存占用的同时加速推理。用户可通过简单的from_pretrained()调用加载预量化模型，无需本地编译。文章展示了在RTX
  5090上生成1024x1024图像仅需1.7秒、显存约12GB的性能，并提供了量化自有模型的工具包。
categories:
- AI基础设施
tags:
- 模型量化
- Diffusers
- Nunchaku
- 扩散模型
- 推理加速
draft: false
translated_at: '2026-07-24T05:29:21.749876'
---

# 将 Nunchaku 4-bit 扩散推理引入 Diffusers

大型扩散 Transformer 可以生成令人惊叹的图像（甚至视频、音频片段，以及现在的文本），但以 BF16 精度加载现代文生图模型通常需要 20-30 GB 的显存，这使得这些模型超出了大多数消费级 GPU 的能力范围。量化是解决这一问题的强大方案，Diffusers 已经集成了多个量化后端，例如 bitsandbytes、GGUF、torchao 和 Quanto，我们在《探索 Diffusers 中的量化后端》一文中介绍过这些内容。

大多数这些后端都是**仅权重量化**。这意味着它们以低精度存储权重，并在计算时将其反量化为高精度。这显著减少了内存使用，但通常不会使推理更快，甚至可能增加少量延迟开销。

SVDQuant 是流行的 Nunchaku 推理引擎背后的量化方法，它采用了不同的方式。它以 4 位权重和激活（W4A4）运行主要的 Transformer 层，在减少内存的同时加速去噪循环。具体细节将在下文介绍，但在此之前，使用这些检查点需要单独的推理库。

在当前的 Diffusers 中，加载 Nunchaku 检查点就像调用 `from_pretrained()` 一样简单，得益于 `kernels` 包，无需本地 CUDA 编译。此外，配套的 `diffuse-compressor` 工具包让您可以自行量化新的架构，并将其发布为常规的 Diffusers 仓库。

![Nunchaku Lite 图像质量和性能对比](/images/posts/0332b857df42.png)

- Nunchaku Lite 入门
- 背景：SVDQuant 和 Nunchaku
- Nunchaku Lite 介绍
- Diffusers 中的原生加载
- 获得更高速度和更低内存
- 基准测试
- 量化您自己的模型
- 即用型检查点
- 结论
- 致谢

## Nunchaku Lite 入门

首先，安装所需依赖。您需要最新版本的 Diffusers 和 Hugging Face 的 `kernels` 包：

```bash
pip install -U diffusers transformers accelerate kernels bitsandbytes

```

然后像加载任何其他 Diffusers 模型一样加载预量化流水线：

```python
import torch
from diffusers import ErnieImagePipeline

pipe = ErnieImagePipeline.from_pretrained(
    "lite-infer/ERNIE-Image-Turbo-nunchaku-lite-nvfp4_r32-bnb4-text-encoder",
    torch_dtype=torch.bfloat16,
).to("cuda")

image = pipe(
    prompt="A cinematic portrait of a red fox in a misty forest at sunrise, "
           "detailed fur, volumetric light",
    height=1024,
    width=1024,
    num_inference_steps=8,
    guidance_scale=1.0,
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]
image.save("output.png")

```

![BF16 和 Nunchaku Lite 对红狐提示词的输出](/images/posts/d538db120a5f.png)

无需自定义流水线类或单独的推理引擎，也无需在本地编译任何内容。NVFP4 内核在首次使用时通过 Nunchaku Lite 内核页面从 Hub 下载。该检查点将 Nunchaku NVFP4 Transformer 与 bitsandbytes NF4 文本编码器配对，在 RTX 5090 上生成一张 1024x1024 图像大约需要 1.7 秒，峰值内存使用约 12 GB，而 BF16 流水线则需要约 24 GB。您可以在官方 Diffusers 文档中找到关于 Nunchaku Lite 检查点格式的更多详细信息。

NVFP4 检查点需要 NVIDIA Blackwell GPU（RTX 50 系列、RTX PRO 6000、B200）。对于早期代次，请使用 INT4 变体。详情请参见下面的硬件支持表。

## 背景：SVDQuant 和 Nunchaku

SVDQuant 是 Nunchaku（其参考 CUDA 推理引擎）背后的量化方法。标准的 4 位量化对于扩散 Transformer 来说很困难，因为权重和激活都包含较大的异常值。SVDQuant 通过将激活异常值转移到权重中来解决这个问题，用一个小型 16 位低秩分支表示每个权重矩阵中最困难的部分，并将剩余残差量化为 4 位。Nunchaku 通过用于 4 位路径和低秩分支的融合内核使其变得快速。

![Nunchaku 将低秩下投影与量化内核融合，并将低秩上投影与 4 位计算内核融合，消除了 16 位分支的内存访问开销。图片来自 SVDQuant 论文。](/images/posts/069d12fe15d3.png)

## Nunchaku Lite 介绍

原始的 Nunchaku 引擎的许多速度优势来自于**特定于模型的融合执行路径**，例如融合的 QKV 投影和融合的 GELU/MLP 内核。这些优化与每种架构的模块布局和检查点格式紧密相关，因此支持新的模型系列通常需要特定于模型的集成工作。

Nunchaku Lite 是 Diffusers 中的新集成路径。通过它，Diffusers 可以加载 Nunchaku 风格的检查点，而无需自定义流水线或单独的推理引擎。在底层，Nunchaku Lite 在加载检查点之前，用运行时 SVDQ/AWQ 线性层替换标准 Diffusers 模型中相关的 `nn.Linear` 模块。CUDA 内核通过 `kernels` 包来自 Hub。使用了两种内核系列：

- `svdq_w4a4`：4 位权重和激活，带有 SVDQuant 低秩校正。该层用于 Transformer 的注意力和 MLP 投影，几乎所有的计算都集中在此，并提供 INT4 和 NVFP4 变体。
- `awq_w4a16`：4 位权重和 16 位激活，用于自适应归一化和调制投影，例如 FLUX 的 `adanorm_single`/`adanorm_zero` 或 Qwen-Image 调制层。这些层是内存受限且对精度敏感的，使得 AWQ 成为在节省内存和空间的同时保持精度的良好选择。

权衡之处在于，没有特定于架构的融合内核和模块，Nunchaku Lite 无法达到原始 Nunchaku 引擎的加速效果。然而，这个精简实现仍然可以提供约 30% 的加速，同时保持相同水平的显存减少。

## Diffusers 中的原生加载

如果您在 Diffusers 中使用过 bitsandbytes 或 torchao，那么其机制会感觉很熟悉。Nunchaku Lite 模型仓库是一个普通的 Diffusers 仓库。唯一特殊的部分是 Transformer 的 `config.json` 中的 `quantization_config` 块：

```json
"quantization_config": {
    "quant_method": "nunchaku_lite",
    "compute_dtype": "bfloat16",
    "svdq_w4a4": {
        "precision": "nvfp4",
        "group_size": 16,
        "rank": 32,
        "targets": [
            "layers.0.self_attention.to_q",
            "layers.0.self_attention.to_k",
            "..."
        ]
    },
    "awq_w4a16": {
        "precision": "int4",
        "group_size": 64,
        "targets": [
            "adaLN_modulation.1",
            "..."
        ]
    }
}

```

此配置告诉 Diffusers 哪些模块被量化、使用了哪种方案以及要实例化哪个 Nunchaku Lite 运行时层（`SVDQW4A4Linear` 或 `AWQW4A16Linear`）。

由于量化模型保持了密集模型的确切模块结构，所有下游组件（调度器、LoRA 加载钩子、卸载、`torch.compile`）看到的都是一个正常的 Diffusers 模型。

### 硬件支持

Nunchaku Lite 根据 GPU 代次和检查点精度使用不同的内核变体：

Volta 和 Hopper GPU 目前不受 4 位内核支持。量化器在加载时会验证 GPU 的 CUDA 能力，并在无法支持时引发明确的错误，而不是产生错误的输出。

## 获得更高速度和更低内存

Nunchaku Lite 可以与其他 Diffusers 内存和速度优化结合使用。

`torch.compile`。编译 Transformer 可将端到端加速从 1.35 倍提升到 1.8 倍：

```python
pipe.transformer.compile(fullgraph=True)

pipe.transformer.compile_repeated_blocks(fullgraph=True)

```

量化文本编码器。Transformer并非唯一占用大量内存的组件。像T5或Qwen3这样的文本编码器本身就能占据数GB空间。在我们的基准测试中，使用bitsandbytes NF4进一步量化文本编码器可将峰值显存降低约22%。

卸载。如果你需要将流水线适配到更小的GPU上，Diffusers的卸载辅助工具（如`enable_model_cpu_offload()`和`enable_sequential_cpu_offload()`）可以照常使用。

## 基准测试

以下所有数据均使用`rootonchair/ERNIE-Image-Turbo-nunchaku-lite-int4-bnb4-text-encoder`，在NVIDIA RTX PRO 6000 (Blackwell)上以1024x1024分辨率测得。

### 端到端延迟与内存

如上所示，Nunchaku将峰值显存降低了高达50%，同时还将延迟改善了约30%。剩余的开销主要来自额外的内核启动，而`torch.compile`可以缓解这一问题，将整个流水线降至1.68秒，比BF16基线快1.8倍。

### 图像质量

![使用相同种子和设置的BF16与4位输出对比。](/images/posts/70bd5cd7b760.png)

## 量化你自己的模型

Diffusers中对Nunchaku Lite的支持与架构无关，`diffuse-compressor`工具包为Diffusers模型提供了端到端的SVDQuant工作流：校准、量化、打包和发布。

下面，我们以量化FLUX.2 Klein 4B为例进行说明。它涵盖了主要步骤：检查模型、校准并量化Transformer、将结果打包为Diffusers流水线，然后验证并推送到Hub。完整教程详细介绍了每个参数。

### 1. 检查将被量化的内容

通用扫描器会遍历模型并决定量化目标：重复的Transformer块堆栈中兼容的线性层成为SVDQ W4A4目标，识别出的调制线性层成为AWQ W4A16目标，其余部分保持密集。

```bash
python examples/text_to_image/quantize_hf.py black-forest-labs/FLUX.2-klein-4B \
  --precision int4 --rank 32 --inspect-config

```

在量化之前务必阅读此报告。对于FLUX.2 Klein 4B，预期结果是100个SVDQ目标、3个AWQ目标和6个密集的外部线性层，没有缺失的模式或重复的名称。

### 2. 运行量化

以下命令对Transformer运行SVDQuant，并将量化后的检查点写入`outputs/checkpoints/svdq-int4_r32-flux-2-klein-4b.safetensors`：

```bash
python examples/text_to_image/quantize_hf.py black-forest-labs/FLUX.2-klein-4B \
  --precision int4 \
  --output outputs/checkpoints/svdq-int4_r32-flux-2-klein-4b.safetensors

```

将`--precision int4`替换为`nvfp4`以构建Blackwell原生权重。

### 3. 打包Diffusers流水线

转换器将量化后的Transformer与基础流水线的其他组件结合，将紧凑的`nunchaku_lite`配置写入`transformer/config.json`，并可选择将文本编码器转换为NF4：

```bash
python examples/convert_nunchaku_lite_diffusers.py \
  --checkpoint outputs/checkpoints/svdq-int4_r32-flux-2-klein-4b.safetensors \
  --model-id black-forest-labs/FLUX.2-klein-4B \
  --bnb4-text-encoder text_encoder \
  --compute-dtype bfloat16 \
  --output-dir outputs/diffusers/FLUX.2-klein-4B-nunchaku-lite-int4-bnb4-text-encoder

```

### 4. 加载、验证并推送到Hub

```python
import torch
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "outputs/diffusers/FLUX.2-klein-4B-nunchaku-lite-int4-bnb4-text-encoder",
    device_map="cuda",
)
image = pipe(
    "温室里的玻璃机器人，电影级灯光",
    num_inference_steps=4, guidance_scale=1.0,
    generator=torch.Generator("cuda").manual_seed(12345),
).images[0]

```

一旦输出效果满意，运行`pipe.push_to_hub("your-name/your-model-nunchaku-lite-int4")`。其他用户随后即可使用上述相同的`from_pretrained()`模式加载该模型。

### 量化具有结构重写的模型

请注意，通用路径假设架构可以在没有结构重写的情况下进行量化。为了获得额外的加速，原始的Nunchaku引擎将Diffusers层组重写为融合模块。通用路径无法自行推断这些更改，例如将独立的Q、K和V投影合并为一个模块，或将一个融合的投影拆分为多个模块。

FLUX.1-dev的QKV投影是一个具体的例子。Diffusers定义了三个独立的模块：

```python
self.to_q = torch.nn.Linear(query_dim, self.inner_dim, bias=bias)
self.to_k = torch.nn.Linear(query_dim, self.inner_dim, bias=bias)
self.to_v = torch.nn.Linear(query_dim, self.inner_dim, bias=bias)

```

Nunchaku FLUX模块将这些层合并为一个量化的`to_qkv`模块：

```python
to_qkv = fuse_linears([other.to_q, other.to_k, other.to_v])
self.to_qkv = SVDQW4A4Linear.from_linear(to_qkv, **kwargs)

```

这个分组模块是必需的，因为Nunchaku的融合算子会一起处理QKV投影、Q/K归一化和旋转位置嵌入。相比之下，默认的Diffusers路径是分别执行它们：

```python
query = attn.to_q(hidden_states)
key = attn.to_k(hidden_states)
value = attn.to_v(hidden_states)

query = query.unflatten(-1, (attn.heads, -1))
key = key.unflatten(-1, (attn.heads, -1))
value = value.unflatten(-1, (attn.heads, -1))

query = attn.norm_q(query)
key = attn.norm_k(key)

if image_rotary_emb is not None:
    query = apply_rotary_emb(query, image_rotary_emb, sequence_dim=1)
    key = apply_rotary_emb(key, image_rotary_emb, sequence_dim=1)

```

Nunchaku路径将分组投影、归一化模块和旋转位置嵌入提供给一个融合算子：

```python
qkv = fused_qkv_norm_rottary(
    hidden_states, attn.to_qkv, attn.norm_q, attn.norm_k, image_rotary_emb
)

```

这就是通用路径无法推断的结构重写。Diffusers有三个目标模块，参数前缀为`to_q`、`to_k`和`to_v`，而Nunchaku有一个分组模块，前缀为`to_qkv`。一个特定于模型的目标配置或适配器必须声明Q、K和V参数应按输出维度顺序拼接，并加载到`to_qkv`中。

像这样的结构重写在量化期间由特定于模型的目标配置描述，并在加载检查点时由一个小型运行时适配器处理。
FLUX.2 Klein 4B量化脚本提供了一个具体的目标配置示例，用于生成结构重写的检查点，而`rootonchair/nunchaku-lite`提供了加载分组QKV张量、拆分融合投影和其他融合操作所需的运行时适配器。
有关完整的工作流，你可以查看添加新模型指南。

## 即用型检查点

要立即开始使用，请查看以下仓库：

- rootonchair/ERNIE-Image-Turbo-nunchaku-lite-int4-bnb4-text-encoder：INT4 ERNIE-Image-Turbo，带有bitsandbytes NF4文本编码器
- rootonchair/ERNIE-Image-Turbo-nunchaku-lite-nvfp4-bnb4-text-encoder：NVFP4 ERNIE-Image-Turbo，带有bitsandbytes NF4文本编码器
- OzzyGT/Krea_2_Turbo_nunchaku_lite_nvfp4：NVFP4 Krea 2 Turbo检查点
- lite-infer：更多Nunchaku Lite检查点和集合

Nunchaku的SVDQuant内核是在消费级硬件上高效运行扩散Transformer的最有效方法之一，并且现在已在Diffusers中得到原生支持。预量化检查点可通过`from_pretrained()`加载，而`diffuse-compressor`工具包使得无需等待引擎支持即可量化新架构。通过量化权重和激活，W4A4路径降低了内存使用，同时改善了去噪延迟，使图像质量接近BF16原始版本。

如果你量化并发布了一个新模型，我们很乐意听到你的消息。在Hub上分享它并告诉我们！如果你对此功能有任何疑问，欢迎加入我们的Discord。

要了解更多信息，请查看以下资源：

- Diffusers Nunchaku 文档  
- 集成 PR（huggingface/diffusers#14100）  
- SVDQuant 论文及 Nunchaku 引擎  
- diffuse-compressor  
- 往期文章：探索 Diffusers 中的量化后端 及 使用 Quanto 和 Diffusers 实现内存高效的扩散 Transformer  

## 致谢

感谢 Diffusers 维护者在整个集成过程中提供的审阅与指导，感谢 MIT HAN Lab / Nunchaku 团队在 SVDQuant 方面的原创工作。感谢 Marc Sun 对博客文章提出的反馈意见。感谢 Álvaro Somoza 试用 nunchaku-lite 并提供反馈。

rootonchair 同时感谢 SilverAI 对这项工作的支持，以及为本开发工作提供主要环境。

---

> 本文由AI自动翻译，原文链接：[Bringing Nunchaku 4-bit Diffusion Inference to Diffusers](https://huggingface.co/blog/nunchaku-diffusers)
> 
> 翻译时间：2026-07-24 05:29
