---
title: 消费级硬件微调FLUX.1-dev：QLoRA与FP8实践指南
title_original: (LoRA) Fine-Tuning FLUX.1-dev on Consumer Hardware
date: '2025-06-19'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/flux-qlora
author: ''
summary: 本文详细介绍了如何在消费级GPU上使用QLoRA和FP8技术对FLUX.1-dev扩散模型进行高效微调。文章重点阐述了通过量化加载基础模型、仅微调Transformer组件、使用8位优化器等关键技术，将峰值显存控制在约10GB内的方法。同时提供了在NVIDIA
  RTX 4090上的实践步骤、优化技巧及推理方案，使开发者能够在有限硬件资源下实现模型定制化训练。
categories:
- AI基础设施
tags:
- 模型微调
- LoRA/QLoRA
- FLUX模型
- 消费级硬件
- Diffusers
draft: false
translated_at: '2026-03-29T05:02:55.328482'
---

# 在消费级硬件上对 FLUX.1-dev 进行 (LoRA) 微调

在我们之前的文章《探索 Diffusers 中的量化后端》中，我们深入探讨了各种量化技术如何缩小像 FLUX.1-dev 这样的扩散模型，使其在**推理**时更容易使用，而不会显著影响性能。我们看到了 **bitsandbytes**、**torchao** 等工具如何减少生成图像时的内存占用。

执行推理很酷，但要让这些模型真正为我们所用，我们还需要能够对它们进行**微调**。因此，在本文中，我们将探讨如何在单个 GPU 上使用约 10 GB 的 VRAM 峰值内存，对这些模型进行**高效**微调。本文将指导您使用 QLoRA 和 **diffusers** 库对 FLUX.1-dev 进行微调。我们将展示在 NVIDIA RTX 4090 上的结果。我们还将重点介绍使用 **torchao** 进行 FP8 训练如何进一步优化兼容硬件上的速度。

- 数据集
- FLUX 架构
- 使用 Diffusers 对 FLUX.1-dev 进行 QLoRA 微调
    - 关键优化技术
    - 设置与结果
- 使用 torchao 进行 FP8 微调
- 使用训练好的 LoRA 适配器进行推理
    - 选项 1：加载 LoRA 适配器
    - 选项 2：将 LoRA 合并到基础模型中
- 在 Google Colab 上运行
- 结论

## 数据集

我们的目标是使用一个**小型数据集**，对 **black-forest-labs/FLUX.1-dev** 进行微调，使其采用阿尔丰斯·慕夏的艺术风格。

## FLUX 架构

该模型由三个主要组件组成：

1.  文本编码器（CLIP 和 T5）
2.  Transformer（主模型 - Flux Transformer）
3.  变分自编码器（VAE）

在我们的 QLoRA 方法中，我们**仅专注于微调 Transformer 组件**。文本编码器和 VAE 在整个训练过程中保持冻结状态。

## 使用 Diffusers 对 FLUX.1-dev 进行 QLoRA 微调

我们使用了一个 **diffusers** 训练脚本（从此处稍作修改），该脚本专为 FLUX 模型的 DreamBooth 风格 LoRA 微调而设计。此外，用于重现本博文结果（并在 Google Colab 中使用）的简化版本可在此处获取。让我们检查一下 QLoRA 和内存效率的关键部分：

### 关键优化技术

**LoRA（低秩适应）深入解析**：LoRA 通过使用低秩矩阵跟踪权重更新，使模型训练更加高效。LoRA 不是更新完整的权重矩阵 WWW，而是学习两个较小的矩阵 AAA 和 BBB。模型的权重更新为 ΔW=BA\Delta W = B AΔW=BA，其中 A∈Rr×kA \in \mathbb{R}^{r \times k}A∈Rr×k 且 B∈Rd×rB \in \mathbb{R}^{d \times r}B∈Rd×r。数字 rrr（称为秩）远小于原始维度，这意味着需要更新的参数更少。最后，α\alphaα 是 LoRA 激活的缩放因子。这会影响 LoRA 对更新的影响程度，通常设置为与 rrr 相同的值或其倍数。它有助于平衡预训练模型和 LoRA 适配器的影响。有关该概念的通用介绍，请查看我们之前的博文：《使用 LoRA 进行高效的 Stable Diffusion 微调》。

![LoRA 在冻结权重矩阵周围注入两个低秩矩阵的图示](/images/posts/d09cc631be14.png)

**QLoRA：效率的强大引擎**：QLoRA 通过首先以量化格式（通常通过 bitsandbytes 进行 4 位量化）加载预训练的基础模型，极大地减少了基础模型的内存占用。然后，它在这个量化的基础上训练 LoRA 适配器（通常使用 FP16/BF16）。这显著降低了保存基础模型所需的 VRAM。

例如，在 HiDream 的 DreamBooth 训练脚本中，使用 bitsandbytes 进行 4 位量化将 LoRA 微调的峰值内存使用量从约 60GB 降低到约 37GB，而质量下降可以忽略不计甚至没有。我们正是应用了相同的原理，在消费级硬件上对 FLUX.1 进行微调。

**8 位优化器（AdamW）**：标准的 AdamW 优化器为每个参数维护 32 位（FP32）的第一和第二矩估计，这会消耗大量内存。8 位 AdamW 使用分块量化以 8 位精度存储优化器状态，同时保持训练稳定性。与标准的 FP32 AdamW 相比，这种技术可以将优化器内存使用量减少约 75%。在脚本中启用它很简单：

```python
if args.use_8bit_adam:
    optimizer_class = bnb.optim.AdamW8bit
else:
    optimizer_class = torch.optim.AdamW

optimizer = optimizer_class(
    params_to_optimize,
    betas=(args.adam_beta1, args.adam_beta2),
    weight_decay=args.adam_weight_decay,
    eps=args.adam_epsilon,
)
```

**梯度检查点**：在前向传播过程中，中间激活值通常被存储起来用于反向传播的梯度计算。梯度检查点通过仅存储某些**检查点激活值**并在反向传播期间重新计算其他激活值，以计算换取内存。

```python
if args.gradient_checkpointing:
    transformer.enable_gradient_checkpointing()
```

**缓存潜在表示**：这种优化技术在训练开始前，通过 VAE 编码器预处理所有训练图像。它将生成的潜在表示存储在内存中。在训练期间，直接使用缓存的潜在表示，而不是实时编码图像。这种方法有两个主要好处：

1.  消除了训练期间冗余的 VAE 编码计算，加快了每个训练步骤。
2.  允许在缓存后将 VAE 完全从 GPU 内存中移除。代价是增加了存储所有缓存潜在表示的 RAM 使用量，但对于小型数据集来说，这通常是可管理的。

```python
    if args.cache_latents:
        latents_cache = []
        for batch in tqdm(train_dataloader, desc="Caching latents"):
            with torch.no_grad():
                batch["pixel_values"] = batch["pixel_values"].to(
                    accelerator.device, non_blocking=True, dtype=weight_dtype
                )
                latents_cache.append(vae.encode(batch["pixel_values"]).latent_dist)
        
        del vae
        free_memory()
```

**设置 4 位量化（BitsAndBytesConfig）**：

此部分演示了基础模型的 QLoRA 配置：

```python
bnb_4bit_compute_dtype = torch.float32
if args.mixed_precision == "fp16":
    bnb_4bit_compute_dtype = torch.float16
elif args.mixed_precision == "bf16":
    bnb_4bit_compute_dtype = torch.bfloat16

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
)

transformer = FluxTransformer2DModel.from_pretrained(
    args.pretrained_model_name_or_path,
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=bnb_4bit_compute_dtype,
)

transformer = prepare_model_for_kbit_training(transformer, use_gradient_checkpointing=False)
```

**定义 LoRA 配置（LoraConfig）**：将适配器添加到量化后的 Transformer：

```python
transformer_lora_config = LoraConfig(
    r=args.rank,
    lora_alpha=args.rank, 
    init_lora_weights="gaussian",
    target_modules=["to_k", "to_q", "to_v", "to_out.0"], 
)
transformer.add_adapter(transformer_lora_config)
print(f"trainable params: {transformer.num_parameters(only_trainable=True)} || all params: {transformer.num_parameters()}")
```

只有这些 LoRA 参数是可训练的。

### 预计算文本嵌入（CLIP/T5）

在启动 QLoRA 微调之前，我们可以通过一次性缓存文本编码器的输出来节省大量的 VRAM 和挂钟时间。

在训练时，数据加载器只需读取缓存的嵌入，而不是重新编码标题，因此 CLIP/T5 编码器永远不需要驻留在 GPU 内存中。

```python
import argparse

import pandas as pd
import torch
from datasets import load_dataset
from huggingface_hub.utils import insecure_hashlib
from tqdm.auto import tqdm
from transformers import T5EncoderModel

from diffusers import FluxPipeline


MAX_SEQ_LENGTH = 77
OUTPUT_PATH = "embeddings.parquet"
```

```python
def generate_image_hash(image):
    return insecure_hashlib.sha256(image.tobytes()).hexdigest()


def load_flux_dev_pipeline():
    id = "black-forest-labs/FLUX.1-dev"
    text_encoder = T5EncoderModel.from_pretrained(id, subfolder="text_encoder_2", load_in_8bit=True, device_map="auto")
    pipeline = FluxPipeline.from_pretrained(
        id, text_encoder_2=text_encoder, transformer=None, vae=None, device_map="balanced"
    )
    return pipeline


@torch.no_grad()
def compute_embeddings(pipeline, prompts, max_sequence_length):
    all_prompt_embeds = []
    all_pooled_prompt_embeds = []
    all_text_ids = []
    for prompt in tqdm(prompts, desc="Encoding prompts."):
        (
            prompt_embeds,
            pooled_prompt_embeds,
            text_ids,
        ) = pipeline.encode_prompt(prompt=prompt, prompt_2=None, max_sequence_length=max_sequence_length)
        all_prompt_embeds.append(prompt_embeds)
        all_pooled_prompt_embeds.append(pooled_prompt_embeds)
        all_text_ids.append(text_ids)

    max_memory = torch.cuda.max_memory_allocated() / 1024 / 1024 / 1024
    print(f"Max memory allocated: {max_memory:.3f} GB")
    return all_prompt_embeds, all_pooled_prompt_embeds, all_text_ids


def run(args):
    dataset = load_dataset("Norod78/Yarn-art-style", split="train")
    image_prompts = {generate_image_hash(sample["image"]): sample["text"] for sample in dataset}
    all_prompts = list(image_prompts.values())
    print(f"{len(all_prompts)=}")

    pipeline = load_flux_dev_pipeline()
    all_prompt_embeds, all_pooled_prompt_embeds, all_text_ids = compute_embeddings(
        pipeline, all_prompts, args.max_sequence_length
    )

    data = []
    for i, (image_hash, _) in enumerate(image_prompts.items()):
        data.append((image_hash, all_prompt_embeds[i], all_pooled_prompt_embeds[i], all_text_ids[i]))
    print(f"{len(data)=}")

    
    embedding_cols = ["prompt_embeds", "pooled_prompt_embeds", "text_ids"]
    df = pd.DataFrame(data, columns=["image_hash"] + embedding_cols)
    print(f"{len(df)=}")

    
    for col in embedding_cols:
        df[col] = df[col].apply(lambda x: x.cpu().numpy().flatten().tolist())

    
    df.to_parquet(args.output_path)
    print(f"Data successfully serialized to {args.output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_sequence_length",
        type=int,
        default=MAX_SEQ_LENGTH,
        help="Maximum sequence length to use for computing the embeddings. The more the higher computational costs.",
    )
    parser.add_argument("--output_path", type=str, default=OUTPUT_PATH, help="Path to serialize the parquet file.")
    args = parser.parse_args()

    run(args)

```

### 使用方法

```bash
python compute_embeddings.py \
  --max_sequence_length 77 \
  --output_path embeddings_alphonse_mucha.parquet

```

将此方法与缓存的 VAE 潜在表示（`--cache_latents`）结合使用，可以将活跃模型精简至仅包含量化后的 Transformer 和 LoRA 适配器，使得整个微调过程轻松控制在 10 GB 的 GPU 内存以内。

### 设置与结果

在此演示中，我们利用 NVIDIA RTX 4090（24GB 显存）来探索其性能。使用 `accelerate` 的完整训练命令如下所示。

```bash


accelerate launch --config_file=accelerate.yaml \
  train_dreambooth_lora_flux_miniature.py \
  --pretrained_model_name_or_path="black-forest-labs/FLUX.1-dev" \
  --data_df_path="embeddings_alphonse_mucha.parquet" \
  --output_dir="alphonse_mucha_lora_flux_nf4" \
  --mixed_precision="bf16" \
  --use_8bit_adam \
  --weighting_scheme="none" \
  --width=512 \
  --height=768 \
  --train_batch_size=1 \
  --repeats=1 \
  --learning_rate=1e-4 \
  --guidance_scale=1 \
  --report_to="wandb" \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \ 
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --cache_latents \
  --rank=4 \
  --max_train_steps=700 \
  --seed="0"

```

RTX 4090 配置：在我们的 RTX 4090 上，我们使用了 `train_batch_size` 为 1，`gradient_accumulation_steps` 为 4，`mixed_precision="bf16"`，`gradient_checkpointing=True`，`use_8bit_adam=True`，LoRA 的 `rank` 为 4，分辨率为 512x768。潜在表示通过 `cache_latents=True` 进行缓存。

内存占用（RTX 4090）：

- QLoRA：QLoRA 微调的峰值显存使用量约为 9GB。
- BF16 LoRA：在同一设置上运行标准 LoRA（基础 FLUX.1-dev 为 FP16 精度）消耗了 26 GB 显存。
- BF16 全量微调：在不进行内存优化的情况下，估计需要约 120 GB 显存。

训练时间（RTX 4090）：在 RTX 4090 上，使用 `train_batch_size` 为 1 和分辨率为 512x768 的设置，对 Alphonse Mucha 数据集进行 700 步的微调大约需要 41 分钟。

输出质量：最终的衡量标准是生成的艺术作品。以下是我们 QLoRA 微调模型在 `derekl35/alphonse-mucha-style` 数据集上的样本：

此表比较了主要的 `bf16` 精度结果。微调的目标是教会模型 Alphonse Mucha 的独特风格。

![Base model output for the first prompt](/images/posts/bff31fd8698c.png)

![QLoRA model output for the first prompt](/images/posts/b19be0ba9483.png)

![Base model output for the second prompt](/images/posts/1ff0e67ff491.png)

![QLoRA model output for the second prompt](/images/posts/8099c9f50796.png)

![Base model output for the third prompt](/images/posts/1973cab98278.png)

![QLoRA model output for the third prompt](/images/posts/59c96f5d8237.png)

微调后的模型很好地捕捉了 Mucha 标志性的新艺术风格，体现在装饰图案和独特的调色板上。QLoRA 过程在学习新风格的同时保持了出色的保真度。

结果几乎相同，表明 QLoRA 在 `fp16` 和 `bf16` 混合精度下都能有效运行。

### 模型比较：基础模型 vs. QLoRA 微调模型（fp16）

![Base model output for the first prompt](/images/posts/e00e026a3aaa.png)

![QLoRA model output for the first prompt](/images/posts/b5d61d5b6d3a.png)

![Base model output for the second prompt](/images/posts/93fbca08b49f.png)

![QLoRA model output for the second prompt](/images/posts/ec98530bc972.png)

![Base model output for the third prompt](/images/posts/047a3b606f84.png)

![QLoRA model output for the third prompt](/images/posts/76a0c7b70822.png)

## 使用 TorchAO 进行 FP8 微调

对于拥有计算能力 8.9 或更高（例如 H100、RTX 4090）的 NVIDIA GPU 用户，通过 `torchao` 库利用 FP8 训练可以实现更高的速度效率。

我们在 H100 SXM GPU 上对 FLUX.1-dev LoRA 进行了微调，略微修改了 `diffusers-torchao` 的训练脚本。使用的命令如下：

```bash
accelerate launch train_dreambooth_lora_flux.py \
  --pretrained_model_name_or_path=black-forest-labs/FLUX.1-dev \
  --dataset_name=derekl35/alphonse-mucha-style --instance_prompt="a woman, alphonse mucha style" --caption_column="text" \
  --output_dir=alphonse_mucha_fp8_lora_flux \
  --mixed_precision=bf16 --use_8bit_adam \
  --weighting_scheme=none \
  --height=768 --width=512 --train_batch_size=1 --repeats=1 \
  --learning_rate=1e-4 --guidance_scale=1 --report_to=wandb \
  --gradient_accumulation_steps=1 --gradient_checkpointing \
  --lr_scheduler=constant --lr_warmup_steps=0 --rank=4 \
  --max_train_steps=700 --checkpointing_steps=600 --seed=0 \
  --do_fp8_training --push_to_hub

```

此次训练运行的峰值内存使用量为 36.57 GB，大约在 20 分钟内完成。

此 FP8 微调模型的定性结果也已提供：

![FP8 model outputs](/images/posts/d78d5d725fb7.png)

使用 `torchao` 启用 FP8 训练的关键步骤包括：

1.  使用 `torchao.float8` 中的 `convert_to_float8_training` 将 FP8 层注入模型。
2.  定义一个 `module_filter_fn` 来指定哪些模块应该或不应该转换为 FP8。

更详细的指南和代码片段，请参考此要点和 `diffusers-torchao` 仓库。

## 使用训练好的 LoRA 适配器进行推理

训练好你的LoRA适配器后，主要有两种推理方法。

### 选项一：加载LoRA适配器

一种方法是在基础模型之上**加载你训练好的LoRA适配器**。

**加载LoRA的优势：**

*   **灵活性：** 无需重新加载基础模型，即可轻松在不同LoRA适配器之间切换
*   **实验性：** 通过更换适配器来测试多种艺术风格或概念
*   **模块化：** 使用 `set_adapters()` 组合多个LoRA适配器，实现创意融合
*   **存储效率：** 只需保存一个基础模型和多个小型适配器文件

```python
from diffusers import FluxPipeline, FluxTransformer2DModel, BitsAndBytesConfig
import torch 

ckpt_id = "black-forest-labs/FLUX.1-dev"
pipeline = FluxPipeline.from_pretrained(
    ckpt_id, torch_dtype=torch.float16
)
pipeline.load_lora_weights("derekl35/alphonse_mucha_qlora_flux", weight_name="pytorch_lora_weights.safetensors")

pipeline.enable_model_cpu_offload()

image = pipeline(
    "a puppy in a pond, alphonse mucha style", num_inference_steps=28, guidance_scale=3.5, height=768, width=512, generator=torch.manual_seed(0)
).images[0]
image.save("alphonse_mucha.png")

```

### 选项二：将LoRA合并到基础模型中

如果你希望以单一风格获得最高效率，可以将**LoRA权重合并**到基础模型中。

**合并LoRA的优势：**

*   **显存效率：** 推理时没有适配器权重带来的额外内存开销
*   **速度：** 由于无需应用适配器计算，推理速度稍快
*   **量化兼容性：** 可以对合并后的模型重新量化，以实现最高的内存效率

```python
from diffusers import FluxPipeline, AutoPipelineForText2Image, FluxTransformer2DModel, BitsAndBytesConfig
import torch 

ckpt_id = "black-forest-labs/FLUX.1-dev"
pipeline = FluxPipeline.from_pretrained(
    ckpt_id, text_encoder=None, text_encoder_2=None, torch_dtype=torch.float16
)
pipeline.load_lora_weights("derekl35/alphonse_mucha_qlora_flux", weight_name="pytorch_lora_weights.safetensors")
pipeline.fuse_lora()
pipeline.unload_lora_weights()

pipeline.transformer.save_pretrained("fused_transformer")

bnb_4bit_compute_dtype = torch.bfloat16

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
)
transformer = FluxTransformer2DModel.from_pretrained(
    "fused_transformer",
    quantization_config=nf4_config,
    torch_dtype=bnb_4bit_compute_dtype,
)

pipeline = AutoPipelineForText2Image.from_pretrained(
    ckpt_id, transformer=transformer, torch_dtype=bnb_4bit_compute_dtype
)
pipeline.enable_model_cpu_offload()

image = pipeline(
    "a puppy in a pond, alphonse mucha style", num_inference_steps=28, guidance_scale=3.5, height=768, width=512, generator=torch.manual_seed(0)
).images[0]
image.save("alphonse_mucha_merged.png")

```

## 在Google Colab上运行

虽然我们展示的结果是在RTX 4090上运行的，但同样的代码也可以在更易获取的硬件上运行，例如**Google Colab**免费提供的T4 GPU。

在T4上，相同步数的微调过程预计会显著延长，大约需要4小时。这是为了可访问性所做的权衡，但它使得无需高端硬件也能进行自定义微调。如果在Colab上运行，请注意使用限制，因为4小时的训练可能会触及这些限制。

## 结论

QLoRA与 **`diffusers`** 库相结合，极大地普及了定制像FLUX.1-dev这样的尖端模型的能力。正如在RTX 4090上所展示的，高效的微调触手可及，并能产生高质量的风格化适配。此外，对于拥有最新NVIDIA硬件的用户，**`torchao`** 通过FP8精度实现了更快的训练。

### 在Hub上分享你的创作！

分享你微调好的LoRA适配器是为开源社区做贡献的绝佳方式。它能让其他人轻松尝试你的风格，在你的工作基础上继续构建，并有助于创建一个充满活力的创意AI工具生态系统。

如果你为FLUX.1-dev训练了一个LoRA，我们鼓励你**分享**它。最简单的方法是在训练脚本中添加 `--push_to_hub` 标志。或者，如果你已经训练好一个模型并想上传它，可以使用以下代码片段。

```python





from huggingface_hub import create_repo, upload_folder

repo_id = "your-username/alphonse_mucha_qlora_flux"
create_repo(repo_id, exist_ok=True)

upload_folder(
    repo_id=repo_id,
    folder_path="alphonse_mucha_qlora_flux",
    commit_message="Add Alphonse Mucha LoRA adapter"
)

```

查看我们的 [Mucha LoRA](https://huggingface.co/derekl35/alphonse_mucha_qlora_flux) 和 [TorchAO FP8 LoRA](https://huggingface.co/derekl35/alphonse_mucha_qlora_flux_fp8)。你可以在 [这个合集](https://huggingface.co/collections/black-forest-labs/flux-1-loras-66b4c2c0a7a7b1a5e6e5e5e5) 中找到这两个以及其他适配器。

我们迫不及待想看到你的创作！

---

> 本文由AI自动翻译，原文链接：[(LoRA) Fine-Tuning FLUX.1-dev on Consumer Hardware](https://huggingface.co/blog/flux-qlora)
> 
> 翻译时间：2026-03-29 05:02
