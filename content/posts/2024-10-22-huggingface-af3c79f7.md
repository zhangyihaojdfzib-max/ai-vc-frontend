---
title: Diffusers集成Stable Diffusion 3.5 Large模型
title_original: Diffusers welcomes Stable Diffusion 3.5 Large
date: '2024-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/sd3-5
author: ''
summary: 本文介绍了Stable Diffusion 3.5 Large模型在Hugging Face Diffusers中的集成与使用。SD3.5 Large包含8B参数版本和少步推理蒸馏版本，架构上引入了QK归一化和双重注意力层。文章详细说明了如何通过Diffusers进行模型加载、推理（包括标准40步和蒸馏4步）、量化推理与LoRA训练，并提供了代码示例。该模型为门控访问，需先通过Hugging
  Face表单申请。
categories:
- AI产品
tags:
- Stable Diffusion 3.5
- Diffusers
- 图像生成
- 模型推理
- Hugging Face
draft: false
translated_at: '2026-06-15T07:19:50.448418'
---

# 🧨 Diffusers 欢迎 Stable Diffusion 3.5 Large

Stable Diffusion 3.5 是其前身 Stable Diffusion 3 的改进版本。  
截至目前，这些模型已在 Hugging Face Hub 上提供，并可与 🧨 Diffusers 一起使用。

此次发布包含两个检查点：

- 一个大型（8B）模型
- 一个大型（8B）时间步蒸馏模型，支持少步推理

在本文中，我们将重点介绍如何使用 Diffusers 使用 Stable Diffusion 3.5（SD3.5），涵盖推理和训练。

- 架构变化
- 使用 Diffusers 使用 SD3.5
- 使用量化进行推理
- 使用量化训练 LoRA
- 使用单文件加载
- 重要链接

## 架构变化

SD3.5（大型）的 Transformer 架构与 SD3（中型）非常相似，但有以下变化：

- QK 归一化：对于训练大型 Transformer 模型，QK 归一化现已成为标准，SD3.5 Large 也不例外。
- 双重注意力层：SD3.5 没有在 MMDiT 块中为每种模态流使用单注意力层，而是使用双重注意力层。

其余细节，如文本编码器、VAE 和噪声调度器，与 SD3 Medium 完全相同。有关 SD3 的更多信息，我们建议查看原始论文。

## 使用 Diffusers 使用 SD3.5

确保您安装了最新版本的 diffusers：

```bash
pip install -U diffusers
```

由于该模型是门控的，在使用 diffusers 之前，您首先需要访问 Stable Diffusion 3.5 Large Hugging Face 页面，填写表单并接受门控。  
一旦通过，您需要登录，以便系统知道您已接受门控。使用以下命令登录：

```bash
huggingface-cli login
```

以下代码片段将以 `torch.bfloat16` 精度下载 SD3.5 的 8B 参数版本。  
这是 Stability AI 发布的原始检查点中使用的格式，也是推荐的推理运行方式。

```python
import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16
).to("cuda")

image = pipe(
    prompt="a photo of a cat holding a sign that says hello world",
    negative_prompt="",
    num_inference_steps=40,
    height=1024,
    width=1024,
    guidance_scale=4.5,
).images[0]

image.save("sd3_hello_world.png")
```

![hello_world_cat](/images/posts/ac5599a5d8ca.png)

此次发布还附带了一个“时间步蒸馏”模型，该模型消除了无分类器引导，并允许我们以更少的步骤（通常为 4-8 步）生成图像。

```python
import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large-turbo", torch_dtype=torch.bfloat16
).to("cuda")

image = pipe(
    prompt="a photo of a cat holding a sign that says hello world",
    num_inference_steps=4,
    height=1024,
    width=1024,
    guidance_scale=1.0,
).images[0]

image.save("sd3_hello_world.png")
```

![hello_world_cat_2](/images/posts/824740d0c052.png)

我们 SD3 博客文章和官方 Diffusers 文档中展示的所有示例应该已经适用于 SD3.5。  
特别是，这两个资源都深入探讨了优化内存需求以运行推理。  
由于 SD3.5 Large 明显大于 SD3 Medium，内存优化对于在消费级接口上进行推理变得至关重要。

## 使用量化运行推理

Diffusers 原生支持与 bitsandbytes 量化配合使用，这进一步优化了内存。

首先，确保安装所有必要的库：

```bash
pip install -Uq git+https://github.com/huggingface/transformers@main
pip install -Uq bitsandbytes
```

然后以“NF4”精度加载 Transformer：

```python
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
import torch

model_id = "stabilityai/stable-diffusion-3.5-large"
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model_nf4 = SD3Transformer2DModel.from_pretrained(
    model_id,
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16
)
```

现在，我们准备运行推理：

```python
from diffusers import StableDiffusion3Pipeline

pipeline = StableDiffusion3Pipeline.from_pretrained(
    model_id, 
    transformer=model_nf4,
    torch_dtype=torch.bfloat16
)
pipeline.enable_model_cpu_offload()

prompt = "A whimsical and creative image depicting a hybrid creature that is a mix of a waffle and a hippopotamus, basking in a river of melted butter amidst a breakfast-themed landscape. It features the distinctive, bulky body shape of a hippo. However, instead of the usual grey skin, the creature's body resembles a golden-brown, crispy waffle fresh off the griddle. The skin is textured with the familiar grid pattern of a waffle, each square filled with a glistening sheen of syrup. The environment combines the natural habitat of a hippo with elements of a breakfast table setting, a river of warm, melted butter, with oversized utensils or plates peeking out from the lush, pancake-like foliage in the background, a towering pepper mill standing in for a tree.  As the sun rises in this fantastical world, it casts a warm, buttery glow over the scene. The creature, content in its butter river, lets out a yawn. Nearby, a flock of birds take flight"
image = pipeline(
    prompt=prompt,
    negative_prompt="",
    num_inference_steps=28,
    guidance_scale=4.5,
    max_sequence_length=512,
).images[0]
image.save("whimsical.png")
```

![happy_hippo](/images/posts/ee648e52dbac.png)

您可以在 BitsAndBytesConfig 中控制其他参数。有关详细信息，请参阅文档。

也可以直接加载使用上述相同 nf4_config 量化的模型。  
这对于内存较低的机器特别有用。请参阅此 Colab Notebook 以获取端到端示例。

## 使用量化训练 SD3.5 Large 的 LoRA

得益于 bitsandbytes 和 peft 等库，可以在具有 24GB VRAM 的消费级 GPU 卡上微调像 SD3.5 Large 这样的大型模型。我们已经可以利用现有的 SD3 训练脚本来训练 LoRA。  
以下训练命令已经可以工作：

```bash
accelerate launch train_dreambooth_lora_sd3.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-3.5-large"  \
  --dataset_name="Norod78/Yarn-art-style" \
  --output_dir="yart_art_sd3-5_lora" \
  --mixed_precision="bf16" \
  --instance_prompt="Frog, yarn art style" \
  --caption_column="text"\
  --resolution=768 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --learning_rate=4e-4 \
  --report_to="wandb" \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=700 \
  --rank=16 \
  --seed="0" \
  --push_to_hub
```

然而，为了使其与量化配合使用，我们需要调整一些参数。下面，我们提供如何做到这一点的指导：

- 我们使用量化配置初始化 Transformer，或者直接加载量化检查点。
- 然后，我们使用 peft 中的 `prepare_model_for_kbit_training()` 准备它。
- 其余过程保持不变，这要归功于 peft 对 bitsandbytes 的强大支持！

请参阅此示例脚本以获取更完整的示例。

## 使用单文件加载 Stable Diffusion 3.5 Transformer

您可以使用 Stability AI 发布的原始检查点文件，通过 `from_single_file` 方法加载 Stable Diffusion 3.5 Transformer 模型：

```python
import torch
from diffusers import SD3Transformer2DModel, StableDiffusion3Pipeline
```

transformer = SD3Transformer2DModel.from_single_file(
    "https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo/blob/main/sd3.5_large.safetensors",
    torch_dtype=torch.bfloat16,
)
pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    transformer=transformer,
    torch_dtype=torch.bfloat16,
)
pipe.enable_model_cpu_offload()
image = pipe("一只举着写有“hello world”牌子的猫").images[0]
image.save("sd35.png")

### 重要链接

- Hub上的Stable Diffusion 3.5 Large集合
- Stable Diffusion 3.5的官方Diffusers文档
- 使用量化进行推理的Colab笔记本
- 训练LoRA
- Stable Diffusion 3论文
- Stable Diffusion 3博客文章

致谢：感谢Daniel Frank为本博客文章缩略图提供的背景照片。感谢Pedro Cuenca和Tom Aarsen对文章草稿的审阅。

---

> 本文由AI自动翻译，原文链接：[Diffusers welcomes Stable Diffusion 3.5 Large](https://huggingface.co/blog/sd3-5)
> 
> 翻译时间：2026-06-15 07:19
