---
title: 开源视频生成模型在Diffusers中的现状与挑战
title_original: State of open video generation models in Diffusers
date: '2025-01-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/video_gen
author: ''
summary: 本文概述了开源视频生成模型在Diffusers中的发展现状，指出自OpenAI Sora演示后，视频生成领域竞争激烈，开源模型如CogVideoX、Mochi-1等涌现。文章分析了视频生成的高资源需求、泛化能力有限和延迟等局限性，并解释了视频生成在运动动态、时空一致性等方面的技术难点。同时介绍了开源模型的核心架构（如DiT、T5文本编码器）及Diffusers支持的文生视频、图像条件生成等推理方式，展望了未来优化方向。
categories:
- 技术趋势
tags:
- 视频生成
- Diffusers
- 开源模型
- AI推理
- 技术挑战
draft: false
translated_at: '2026-05-28T06:10:09.028759'
---

# 开源视频生成模型在 Diffusers 中的现状

OpenAI 的 Sora 演示标志着去年 AI 生成视频领域的显著进步，让我们得以一窥视频生成模型的潜在能力。其影响立竿见影，自那次演示以来，视频生成领域的竞争日益激烈，主要厂商和初创公司纷纷推出各自的高性能模型，例如 Google 的 Veo2、海螺 AI 的 Minimax、Runway 的 Gen3 Alpha、可灵、Pika 以及 Luma Lab 的 Dream Machine。

开源领域也涌现出一批视频生成模型，包括 CogVideoX、Mochi-1、Hunyuan、Allegro 和 LTX Video。视频社区是否正在经历其“Stable Diffusion 时刻”？

本文将简要概述视频生成模型的现状、开源视频生成模型的发展情况，以及 Diffusers 团队计划如何支持其大规模应用。

具体来说，我们将讨论：

- 视频生成模型的能力与局限性
- 视频生成为何困难
- 开源视频生成模型
- 使用 Diffusers 进行视频生成推理与优化微调
- 未来展望

- 推理与优化
- 微调

## 当今的视频生成模型及其局限性

以下是当前用于 AI 生成内容创作的最热门视频模型

局限性：

- **高资源需求**：生成高质量视频需要大型预训练模型，其开发和部署的计算成本高昂。这些成本源于数据集收集、硬件需求、大量的训练迭代和实验。这使得开发开源且免费可用的模型难以获得合理回报。尽管我们没有详细的技术报告说明所使用的训练资源，但本文提供了一些合理的估算。
- **泛化能力**：多个开源模型存在泛化能力有限的问题，未能达到用户预期。模型可能需要以特定方式进行提示，或使用类似 LLM 的提示词，或者无法泛化到分布外数据，这些都给用户广泛采用带来了障碍。例如，LTX-Video 等模型通常需要非常详细和具体的提示才能获得高质量的生成结果。
- **延迟**：视频生成的高计算和内存需求导致显著的生成延迟。对于本地使用而言，这通常是一个障碍。大多数新的开源视频模型，如果没有广泛的内存优化和量化方法（这些方法会影响推理延迟和生成视频的质量），社区硬件将无法运行。

## 为什么视频生成很困难？

在视频中，我们希望看到并控制以下几个因素：

- 对输入条件（如文本提示、起始图像等）的遵循程度
- 真实感
- 美学效果
- 运动动态
- 时空一致性与连贯性
- 帧率
- 时长

对于图像生成模型，我们通常只关心前三个方面。然而，对于视频生成，我们现在必须考虑运动质量、随时间变化的连贯性和一致性，并且可能涉及多个主体。在良好的数据、正确的归纳先验以及满足这些额外需求的训练方法之间找到合适的平衡，已被证明比其他模态更具挑战性。

## 开源视频生成模型

![图表](/images/posts/293ed81d2b56.jpg)

文生视频模型与其对应的文生图模型具有相似的组件：

- 用于提供输入文本提示丰富表示的文本编码器
- 一个去噪网络
- 用于在像素空间和潜在空间之间转换的编码器和解码器
- 一个负责管理所有时间步相关计算和去噪步骤的非参数调度器

最新一代的视频模型共享一个核心特征：去噪网络处理同时捕获空间和时间信息的 3D 视频 Token。负责生成和解码这些 Token 的视频编码器-解码器系统采用了空间和时间压缩。虽然解码潜在变量通常需要最多的内存，但这些模型提供了逐帧解码选项以减少内存使用。

文本条件通过联合注意力（在 Stable Diffusion 3 中引入）或交叉注意力来整合。T5 已成为大多数模型首选的文本编码器，HunYuan 是个例外，它同时使用了 CLIP-L 和 LLaMa 3。

去噪网络本身建立在 William Peebles 和 Saining Xie 开发的 DiT 架构之上，同时融入了 PixArt 的各种设计元素。

## 使用 Diffusers 进行视频生成

使用视频模型时，主要有三大类生成方式：

1. 文生视频
2. 图像或图像控制条件 + 文生视频
3. 视频或视频控制条件 + 文生视频

从文本（及其他条件）生成视频只需几行代码。下面我们展示如何使用 Lightricks 的 LTX-Video 模型进行文生视频。

```py
import torch
from diffusers import LTXPipeline
from diffusers.utils import export_to_video

pipe = LTXPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16).to("cuda")

prompt = "一位长着棕色长发、浅色皮肤的女性对另一位长着金色长发的女性微笑。棕色头发的女性穿着黑色夹克，右脸颊上有一个几乎不显眼的小痣。镜头是特写，聚焦在棕色头发女性的脸上。光线温暖而自然，可能是夕阳，给场景投下柔和的光晕。场景看起来像是真实的生活录像"
negative_prompt = "最差质量，运动不一致，模糊，抖动，扭曲"

video = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=704,
    height=480,
    num_frames=161,
    num_inference_steps=50,
).frames[0]
export_to_video(video, "output.mp4", fps=24)

```

### 内存需求

任何模型的内存需求可以通过以下方式计算：

- 权重所需内存
- 存储中间激活状态所需的最大内存

权重所需内存可以通过量化、降级到更低数据类型或卸载到 CPU 来降低。激活状态所需内存也可以降低，但这是一个更复杂的过程，不在本文讨论范围内。

以极低内存运行任何视频模型是可能的，但这会牺牲推理所需的时间。如果优化技术所需的时间超过用户认为合理的范围，那么运行推理就不可行。Diffusers 提供了许多此类优化，用户可选择启用，并且可以串联使用。

在下表中，我们提供了三种流行视频生成模型在合理默认设置下的内存需求：

这些数据是在 80GB A100 机器上使用以下设置获得的（完整脚本见此处）：

- torch.bfloat16 数据类型
- num_frames: 121, height: 512, width: 768
- max_sequence_length: 128
- num_inference_steps: 50

这些需求相当惊人，使得这些模型难以在消费级硬件上运行。使用 Diffusers，用户可以选择启用不同的优化来减少内存使用。
下表提供了 HunyuanVideo 在启用各种优化（对质量和推理时间影响最小）时的内存需求。

我们选择 HunyuanVideo 进行此项研究，因为它足够大，可以逐步展示优化的优势。

*与 4Bit 模型不同，bitsandbytes 中的 8Bit 模型无法从 GPU 移动到 CPU。^内存使用量没有进一步降低，因为峰值利用率来自计算注意力和前馈网络。使用 Flash Attention 和优化前馈网络可以帮助将此需求降低到约 5 GB。

我们使用与上述相同的设置来获取这些数字。另请注意，由于数值精度损失，量化可能会影响输出质量，这种影响在视频中比在图像中更为明显。

我们在以下部分提供了关于这些优化的更多细节，并附上了一些代码片段。但如果你已经感到兴奋，
我们鼓励你查看我们的指南。

### 优化套件

在资源受限的设备上进行视频生成可能相当困难，即使在性能更强的GPU上也可能耗时。Diffusers提供了一套实用工具，有助于优化这些模型的运行时间和内存消耗。这些优化分为以下几类：

- **量化**：模型权重被量化为更低精度的数据类型，从而降低模型的VRAM需求。目前，Diffusers支持三种不同的量化后端：`bitsandbytes`、`torchao`和`GGUF`。
- **卸载**：模型的各层可以在需要时动态加载到GPU上进行计算，然后卸载回CPU。这在推理过程中可以节省大量内存。通过`enable_model_cpu_offload()`和`enable_sequential_cpu_offload()`支持卸载。更多详情请参考[此处]。
- **分块推理**：通过在输入潜在张量的非嵌入维度上拆分推理，可以减少中间激活状态带来的内存开销。这种技术的常见应用见于编码器/解码器的切片/平铺。Diffusers中的分块推理通过前馈分块、解码器平铺与切片以及分离注意力推理来支持。
- **注意力与MLP状态复用**：如果特定算法的某些条件得到满足，可以跳过某些去噪步骤的计算并复用之前的状态，从而以最小的质量损失加速生成过程。

以下是一些目前正在开发中、即将合并的高级优化技术列表：

- **逐层类型转换**：允许用户以较低精度（如`torch.float8_e4m3fn`）存储参数，并以较高精度（如`torch.bfloat16`）运行计算。
- **分组卸载**：允许用户对内部块级或叶级模块进行分组卸载。这样做的好处是，只有模型计算所需的部分才会被加载到GPU上。此外，我们支持使用CUDA流将数据传输与计算重叠，从而减少因多次加载/卸载层而产生的大部分额外开销。

以下是将4bit量化、VAE平铺、CPU卸载和逐层类型转换应用于HunyuanVideo的示例，可将`121 x 512 x 768`分辨率视频所需的VRAM降低至仅约6.5 GB。据我们所知，这是在所有可用实现中，运行HunyuanVideo所需的最低内存要求，且不影响速度。

请从源代码安装Diffusers以试用这些功能！某些实现与所使用的模型无关，可以轻松应用于其他后端——请务必查看！

```shell
pip install git+https://github.com/huggingface/diffusers.git

```

```python
import torch
from diffusers import (
    BitsAndBytesConfig,
    HunyuanVideoTransformer3DModel,
    HunyuanVideoPipeline,
)
from diffusers.utils import export_to_video
from diffusers.hooks import apply_layerwise_casting
from transformers import LlamaModel

model_id = "hunyuanvideo-community/HunyuanVideo"
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16
)

text_encoder = LlamaModel.from_pretrained(model_id, subfolder="text_encoder", torch_dtype=torch.float16)
apply_layerwise_casting(text_encoder, storage_dtype=torch.float8_e4m3fn, compute_dtype=torch.float16)


transformer = HunyuanVideoTransformer3DModel.from_pretrained(
    model_id,
    subfolder="transformer",
    quantization_config=quantization_config,
    torch_dtype=torch.bfloat16,
)

pipe = HunyuanVideoPipeline.from_pretrained(
    model_id, transformer=transformer, text_encoder=text_encoder, torch_dtype=torch.float16
)


pipe.vae.enable_tiling()
pipe.enable_model_cpu_offload()

output = pipe(
    prompt="一只猫在草地上行走，逼真",
    height=320,
    width=512,
    num_frames=61,
    num_inference_steps=30,
).frames[0]
export_to_video(output, "output.mp4", fps=15)

```

我们也可以在训练过程中应用优化。应用于视频模型的两个最著名的技术包括：

- **时间步蒸馏**：这涉及以递归方式教导模型以更少的推理步骤更快地对噪声潜在表示进行去噪。例如，如果一个模型需要32步才能生成好的视频，可以增强它，使其尝试仅用16步、8步甚至2步来预测最终输出！根据使用的步数多少，这可能会伴随质量损失。一些时间步蒸馏模型的例子包括`Flux.1-Schnell`和`FastHunyuan`。
- **引导蒸馏**：无分类器引导是扩散模型中广泛使用的一种技术，可增强生成质量。然而，这会使生成时间加倍，因为每个推理步骤需要两次完整的前向传播，然后进行一次插值步骤。通过教导模型以一次前向传播的代价来预测两次前向传播和插值的输出，这种方法可以实现更快的生成。一些引导蒸馏模型的例子包括`HunyuanVideo`和`Flux.1-Dev`。

我们建议读者参考[本指南](this guide)，以详细了解视频生成以及Diffusers中当前的可能性。

### 微调

我们创建了`finetrainers`——一个允许你轻松微调最新一代开源视频模型的仓库。例如，以下是如何使用LoRA微调CogVideoX：

```bash

huggingface-cli download \
  --repo-type dataset Wild-Heart/Disney-VideoGeneration-Dataset \
  --local-dir video-dataset-disney


accelerate launch train.py \
  --model_name="cogvideox" --pretrained_model_name_or_path="THUDM/CogVideoX1.5-5B" \
  --data_root="video-dataset-disney" \
  --video_column="videos.txt" \
  --caption_column="prompt.txt" \
  --training_type="lora" \
  --seed=42 \
  --mixed_precision="bf16" \
  --batch_size=1 \
  --train_steps=1200 \
  --rank=128 \
  --lora_alpha=128 \
  --target_modules to_q to_k to_v to_out.0 \
  --gradient_accumulation_steps 1 \
  --gradient_checkpointing \
  --checkpointing_steps 500 \
  --checkpointing_limit 2 \
  --enable_slicing \
  --enable_tiling \
  --optimizer adamw \
  --lr 3e-5 \
  --lr_scheduler constant_with_warmup \
  --lr_warmup_steps 100 \
  --lr_num_cycles 1 \
  --beta1 0.9 \
  --beta2 0.95 \
  --weight_decay 1e-4 \
  --epsilon 1e-8 \
  --max_grad_norm 1.0




```

我们使用`finetrainers`来模拟“溶解”效果，并获得了有希望的结果。查看[该模型](the model)以获取更多详细信息。

## 展望未来

我们预计2025年视频生成模型将取得重大进展，在输出质量和模型能力方面都将有显著提升。
我们的目标是让这些模型易于使用和访问。我们将继续发展`finetrainers`库，并计划添加更多功能：Control LoRAs、蒸馏算法、ControlNets、适配器等。一如既往，欢迎社区贡献 🤗

我们仍然坚定地致力于与模型发布者、研究人员和社区成员合作，确保视频生成领域的最新创新成果惠及每一个人。

## 资源

我们在文章中引用了许多链接。为确保你不会错过最重要的内容，我们在下面提供一个列表：

- [视频生成指南](Video generation guide)
- [Diffusers中的量化支持](Quantization support in Diffusers)
- [Diffusers中的通用LoRA指南](General LoRA guide in Diffusers)
- [CogVideoX的内存优化指南](Memory optimization guide for CogVideoX)（也适用于其他视频模型）
- [用于微调的finetrainers](finetrainers for fine-tuning)

致谢：感谢Chunte为本篇文章制作了精美的缩略图。感谢Vaibhav和Pedro提供了宝贵的反馈意见。

---

> 本文由AI自动翻译，原文链接：[State of open video generation models in Diffusers](https://huggingface.co/blog/video_gen)
> 
> 翻译时间：2026-05-28 06:10
