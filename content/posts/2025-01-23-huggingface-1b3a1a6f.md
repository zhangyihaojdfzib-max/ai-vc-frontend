---
title: SmolVLM再变小：256M和500M模型发布
title_original: SmolVLM Grows Smaller – Introducing the 256M & 500M Models!
date: '2025-01-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/smolervlm
author: ''
summary: Hugging Face发布SmolVLM家族新成员：256M和500M参数模型，其中256M模型成为全球最小的视觉语言模型。文章介绍了新模型在保持强大多模态性能的同时，通过采用更小的SigLIP视觉编码器、提升图像分辨率及训练优化技巧，实现了极致的轻量化。新模型支持图像描述、文档问答和基础视觉推理，性能超越17个月前的80B模型，且与SmolLM2系列形成完整的小型LLM+VLM组合。
categories:
- AI产品
tags:
- SmolVLM
- 视觉语言模型
- 轻量化模型
- 多模态AI
- Hugging Face
draft: false
translated_at: '2026-05-30T05:45:48.885109'
---

# SmolVLM 变得更小——推出 256M 和 500M 模型！

我们很高兴地宣布 SmolVLM 家族新增两个成员：SmolVLM-256M 和 SmolVLM-500M。没错——256M 参数，使其成为世界上最小的视觉语言模型！

我们在 SmolVLM 2B 的所有经验基础上，专注于效率、数据混合和新的设计权衡。我们很高兴推出一对模型，它们以极小的体积保留了强大的多模态性能。

此次发布包含四个检查点：两个基础模型和两个指令微调模型，参数规模分别为 256M 和 500M。这些模型可直接加载到 transformers、MLX 和 ONNX 中，我们还提供了 transformers 和 WebGPU（基于 ONNX）的演示。您可以在此处找到所有模型和演示。

![基准测试](/images/posts/d23f24dc5926.png)

- 概述
- 为什么做更小？认识 256M 参数巨兽更进一步：500M
- 自 SmolVLM 2B 以来有哪些变化？
- 更小的多模态检索：ColSmolVLM 256M 和 500M
- 使用更小的 SmolVLM
- 引用信息
- 后续步骤

- 认识 256M 参数巨兽
- 更进一步：500M

## 概述

- **SmolVLM-256M** – 世界上最小的 VLM！
- **SmolVLM-500M** – 一个五亿参数的兄弟模型，在保持超轻量级的同时提供显著的性能提升。
- **新的视觉编码器选择** – 我们比较了 SigLIP 400M SO（用于 SmolVLM 2B 和许多其他大型 VLM）与较小的 SigLIP base patch-16/512。令人惊讶的是，较大的编码器仅带来微乎其微的改进，因此我们在这些新版本中选择了 93M 参数的 SigLIP base patch-16/512。
- **更大的图像分辨率** – 我们较小的视觉编码器以更高的分辨率处理图像（受 Apple 的 VLM 研究和 Google 的 PaliGemma 启发）。这以最小的开销实现了更清晰的图像理解。
- **训练优化** – 一种新的 Token 化技巧显著提升了实际基准测试性能，尽管它在纸面上使训练损失看起来更差。

我们现在与 SmolLM2 家族（135M、360M、1.7B）实现了模型对等，因此您拥有一套完整的小型 LLM + VLM 组合可供使用。

## 为什么做更小？

当我们发布 SmolVLM 2B 时，社区反响极佳：该模型非常轻量、开源且许可宽松，易于集成到现有工作流中。但我们希望为使用受限设备、消费级笔记本电脑甚至可能基于浏览器的推理的用户进一步推进这种方法。这就是我们新的 256M 和 500M 模型的用武之地。另一方面，对于试图处理海量数据的用户来说，这些模型的运行成本仅为 2B 模型的一小部分。

在过去一年中，我们训练了两个 80B VLM 并将其缩减到 8B。然后对于 SmolVLM，我们接受了将其缩减到 2B 的挑战。而我们学到的是，我们可以将前沿推得更远！我们很高兴地展示，在 256M 和 500M 规模下，我们仍然可以获得出色的性能。我们新的 256M 模型是有史以来发布的最小的 VLM，然而它的性能超过了仅 17 个月前我们的 Idefics 80B 模型。

### 认识 256M 参数巨兽

仅凭 2.56 亿个参数，该模型成为有史以来最小的 VLM。尽管体积小，但它却出人意料地强大。它在许多多模态任务上完全胜任，包括：

- **图像描述**：描述图像或短视频。
- **文档问答**：回答关于 PDF 或扫描文本的问题。
- **基础视觉推理**：回答关于图表或示意图的问题。

### 更进一步：500M

如果您需要更高的性能余量，同时保持低内存使用，SmolVLM-500M 是我们的五亿参数折中方案。它比之前的 2B 版本小得多，但在 DocVQA 和 MMMU 等任务上的得分却更接近更大的模型。我们还发现该模型对提示词更加鲁棒，使其开箱即用更适合生产环境。但两个模型在微调后都表现良好。

我们在下图中可视化了不同批次大小下的吞吐量增益。以下数字是在 A100 上运行的吞吐量基准测试。

![基准测试](/images/posts/728ec5efaade.png)

## 自 SmolVLM 2B 以来有哪些变化？

1. **视觉编码器选择**  
   以前，我们使用标准的 SigLIP 400M SO 视觉骨干网络，与许多 VLM 架构中使用的相同。对于这些较小的模型，我们实验了两种配置：
   - SigLIP 400M SO：更高容量，出色性能。
   - SigLIP base patch-16/512 (93M)：小得多，性能却惊人地接近。

   我们发现性能差距不足以证明为我们 256M 和 500M 模型使用更重的编码器是合理的。因此，我们决定在视觉编码器上也选择小型化。额外的好处是，较小的编码器以更高的分辨率处理图像，这（根据 Apple 和 Google 的研究）通常可以在不增加参数数量的情况下带来更好的视觉理解。

2. **数据混合更新**  
   与我们之前的发布类似，我们依赖 The Cauldron 和 Docmatix，并在混合中加入了 MathWriting。

   ![数据混合](/images/posts/4aceae96687c.gif)

   数据集的占比进行了调整，以更加强调文档理解（41%）和图像描述（14%），同时仍然保持对其他关键领域（如视觉推理、图表理解和通用指令遵循）的平衡关注。通过这次更新，模型建立在强大的文档理解基础上，并为微调打开了大门，以调整其对特定任务的理解。

3. **Token 化优化**  
   我们进一步增加了像素洗牌！我们的新模型以每 Token 4096 像素的速率编码图像，而 2B 模型为每 Token 1820 像素。

   为了进一步优化 Token 化，我们添加了特殊 Token，以更高效的方式表示我们的子图像分隔符。这意味着现在像 `<row_1_col_1>` 这样的字符串不再映射为 7 个 Token，而是映射为单个 Token。我们对直到 `<row_6_col_6>` 的字符串也做了同样处理。这导致了模型训练稳定性和结果质量的显著提升。更多细节记录在这篇 LinkedIn 文章中。

4. **完善 SmolLM2-SmolVLM 家族**  
   SmolLM2 有三种尺寸：135M、360M 和 1.7B。通过我们今天发布的两个模型，我们现在拥有一套完整的小型 LLM + VLM 组合可供使用。

## 更小的多模态检索：ColSmolVLM 256M 和 500M

我们还发现微调和实验出奇地容易。ColBERT 类检索模型背后的团队训练了 ColSmolVLM，提供了最先进的多模态检索速度，性能可与规模大 10 倍的模型相媲美。SmolVLM 使得构建可搜索数据库更快、更便宜。我们认为 256M 模型可以成为许多任务的出色专用模型。在后续步骤中查找如何使用新的 ColSmolVLM 与新的 SmolVLM 模型的链接。

![基准测试](/images/posts/eee9d32be504.png)

## SmolDocling

我们与 IBM 合作，为 Docling 构建模型。他们在 256M 模型上的早期结果令人印象深刻。以下是他们与我们分享的一些早期示例。敬请关注更多更新！

![基准测试](/images/posts/5c4e343e5198.png)

![基准测试](/images/posts/f172a9248d92.png)

## 使用更小的 SmolVLM

更新的 SmolVLM 与旧的 SmolVLM 代码开箱即用，因此您可以使用 transformers 和 MLX 进行推理和微调，并使用 TRL 进行对齐 🚀 此外，此版本还附带 ONNX 检查点。

使用 transformers 开始使用 SmolVLM，如下所示。

```python
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq


processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-500M-Instruct",
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
)

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "你能描述一下这张图片吗？"}
        ]
    },
]

prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image], return_tensors="pt")

generated_ids = model.generate(**inputs, max_new_tokens=500)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)
```

通过运行以下 CLI 命令，使用 MLX 运行 SmolVLM：

```bash
python3 -m mlx_vlm.generate --model HuggingfaceTB/SmolVLM-500M-Instruct --max-tokens 400 --temp 0.0 --image https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/vlm_example.jpg --prompt "这张图片里有什么？"
```

![MLX](/images/posts/60d51c5c4f30.gif)

您可以体验 SmolVLM-256M-Instruct 和 SmolVLM-500M-Instruct 的 WebGPU 演示。

有关使用 ColSmolVLM 进行微调和多模态 RAG 的链接，请参见“下一步”。

## 引用信息

您可以通过以下方式引用我们：

```bibtex
@article{marafioti2025smolvlm,
  title={SmolVLM: Redefining small and efficient multimodal models}, 
  author={Andrés Marafioti and Orr Zohar and Miquel Farré and Merve Noyan and Elie Bakouch and Pedro Cuenca and Cyril Zakka and Loubna Ben Allal and Anton Lozhkov and Nouamane Tazi and Vaibhav Srivastav and Joshua Lochner and Hugo Larcher and Mathieu Morlon and Lewis Tunstall and Leandro von Werra and Thomas Wolf},
  journal={arXiv preprint arXiv:2504.05299},
  year={2025}
}
```

## 下一步

- 我们期待您使用 SmollerVLM 的各种方式！从这里开始。
- 在此深入了解 SmolVLM。
- 使用 transformers 对 SmolVLM 进行微调和 QLoRA
- [使用 TRL 对 SmolVLM 进行直接偏好优化](在消费级 GPU 上使用 TRL 对 SmolVLM 进行直接偏好优化（DPO）微调)
- Smol 多模态 RAG：在 Colab 免费 GPU 上使用 ColSmolVLM 和 SmolVLM 构建应用

我们要感谢 ViDoRe 团队训练了 ColSmolVLM：Tony Wu、Manuel Faysse，以及 Joshua Lochner 负责 ONNX 转换和 WebGPU 演示，Vaibhav Srivastav 为本次发布提供的帮助。

---

> 本文由AI自动翻译，原文链接：[SmolVLM Grows Smaller – Introducing the 256M & 500M Models!](https://huggingface.co/blog/smolervlm)
> 
> 翻译时间：2026-05-30 05:45
