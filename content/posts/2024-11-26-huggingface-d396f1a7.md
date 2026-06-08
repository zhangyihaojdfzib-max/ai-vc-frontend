---
title: SmolVLM：小巧高效的视觉语言模型
title_original: SmolVLM - small yet mighty Vision Language Model
date: '2024-11-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/smolvlm
author: ''
summary: SmolVLM是一个仅2B参数的小型视觉语言模型，在内存占用上达到最先进水平，体积小、速度快且完全开源。该模型基于Idefics3架构，使用SmolLM2
  1.7B作为语言主干，并通过像素洗牌策略将视觉信息压缩9倍。文章介绍了其架构设计、性能基准测试、内存和吞吐量优势，以及三个发布版本：Base、Synthetic和Instruct。所有模型检查点、数据集和训练工具均在Apache
  2.0许可下发布，支持本地部署和边缘设备应用。
categories:
- AI产品
tags:
- 视觉语言模型
- 开源模型
- 边缘部署
- 模型压缩
- 多模态AI
draft: false
translated_at: '2026-06-08T06:33:41.470736'
---

# SmolVLM - 小巧而强大的视觉语言模型

这篇博客文章介绍了SmolVLM，一个2B参数的VLM（视觉语言模型），在其内存占用方面达到了SOTA（最先进水平）。SmolVLM体积小、速度快、内存效率高，并且完全开源。所有模型检查点、VLM数据集、训练方案和工具均在Apache 2.0许可下发布。

![图片描述](/images/posts/098e972fe0ff.png)

## 什么是SmolVLM？

今年，随着许多大型视觉语言模型的发布，多模态AI迎来了蓬勃发展。趋势最初是扩大计算规模，随后通过使用大模型生成合成数据来扩展数据多样性，而最近则是缩小规模以提高这些模型的效率。小型开源模型支持在浏览器或边缘设备上本地部署，降低推理成本，并实现用户定制化。这些模型中的一些显著例子包括PaliGemma 3B、moondream2和Qwen2VL。

在这篇博客文章中，我们介绍SmolVLM，一个全新的2B参数小型视觉语言模型系列，可商用并可部署到较小的本地环境中，且训练流程完全开源。

我们发布了三个模型：**SmolVLM-Base**，可用于下游微调；**SmolVLM-Synthetic**，在合成数据上进行微调的变体；以及**SmolVLM Instruct**，经过微调的指令变体，可直接用于交互式终端用户应用。

此次发布包括集成到transformers中的开源模型、一个基于SmolVLM Instruct构建的演示，以及一个监督微调脚本。我们使用了之前用于Idefics3的数据集：**The Cauldron**和**Docmatix**，这些数据集也完全开源。

- TLDR
- 什么是SmolVLM？模型能力架构
- 性能基准测试内存吞吐量视频VLMEvalKit集成
- 使用Transformers使用SmolVLM
- 训练细节数据集上下文扩展检查点选择
- 微调
- 引用信息
- 总结

- 模型能力
- 架构

- 基准测试
- 内存
- 吞吐量
- 视频
- VLMEvalKit集成

- 数据集
- 上下文扩展
- 检查点选择

## 模型能力

![](/images/posts/b92839f9bd10.jpg)

**主楼**：位于建筑群中心，主楼以精美的瓷砖工艺为特色，覆盖着传统泰国图案，包括龙、神话生物、花卉和几何形状等纹样。屋顶线条设计精巧，多层瓷砖饰以金色点缀。

**塔楼与尖顶**：大皇宫内有几座塔楼，包括那空是贪玛叻国家博物馆塔，馆内展示泰国文化和遗产的展品。另一座著名的塔楼是亚柴蒙考寺塔，那里有描绘佛教神话场景的精美壁画。

**建筑风格**：建筑风格融合了东南亚常见的印度教和高棉元素。您会注意到佛塔（圆顶结构）、莲花雕刻以及这些地区宗教建筑典型的华丽细节。

**游客体验**：游览大皇宫时，游客应注意当局采取的安全措施所规定的某些规则。这些包括在某些区域内禁止摄影，或室外禁止使用闪光灯。此外，旅游旺季可能会有排队情况，如果您计划前往，请提前做好安排。

### 游览大皇宫的旅行贴士：

- **最佳游览时间**：最佳游览时间可能是日出前的清晨，此时气温显著下降，便于步行游览。
- **交通方式**：有公共交通选项，但可能无法直接到达大皇宫；建议乘坐出租车。
- **餐饮选择**：大皇宫附近餐饮设施不多，但当地街头小吃摊提供美味餐食。
- **着装指南**：虽然不是强制要求，但穿着传统泰国服饰（纱笼）可以增加文化沉浸体验。不过，允许穿短裤/长裤，前提是长度不低于膝盖。
- **安全措施**：游客必须遵守指示牌，注意标有"禁止摄影"等限制区域。务必随身携带身份证件。

遵循这些指南，您的旅程无疑将加深对泰国丰富历史画卷的理解，并提升个人体验！

![](/images/posts/1610ddbd29d2.png)

![](/images/posts/ad184797225c.png)

## 架构

![图片描述](/images/posts/e9c10356422b.png)

对于SmolVLM，我们紧密遵循了Idefics3的架构，以至于在transformers中使用了相同的实现。然而，存在几个关键差异：

- 我们将语言主干从Llama 3.1 8B替换为SmolLM2 1.7B。
- 我们通过使用像素洗牌策略将信息压缩9倍，更积极地压缩分块视觉信息，而Idefics3仅为4倍。
- 我们使用384*384的图像块，而不是364x364，因为384能被3整除，这对于我们的像素洗牌策略是必要的。
- 为此，我们将视觉主干更换为使用形状优化的SigLIP，采用384x384像素的图像块和14x14的内部块。

## 性能

### 基准测试

我们展示了训练细节中提到的任务的基准测试结果。

### 内存

![SmolVLM与其他模型的推理GPU内存使用](/images/posts/99f1c74c0be3.png)

SmolVLM在transformers中现有的视觉语言模型套件中提供了最佳的内存使用效率。这使得它能够在设备上高效运行，例如笔记本电脑！您可以在上方看到每个模型的GPU内存使用量（以GB为单位），在推理时使用一张或两张输入图像，并在所有测试中使用相同的图像和文本提示。SmolVLM在图像编码方面的效率是模型内置的。SmolVLM将每个384x384的图像块编码为81个Token。这使得SmolVLM将我们的测试提示和单张图像编码为1.2k个Token，而Qwen2-VL则使用16k个Token。这也解释了为什么Qwen和InternVL在处理两张图像时内存消耗增加如此之多。相比之下，SmolVLM和PaliGemma（使用类似方法）的增长则温和得多。

### 吞吐量

![图片描述](/images/posts/73bb14e86898.png)

SmolVLM极小的内存占用也意味着它需要更少的计算量来进行模型预填充和生成。与Qwen2-VL相比，预填充吞吐量快3.3至4.5倍，生成吞吐量快7.5至16倍。

### 视频

鉴于SmolVLM的长上下文以及调整模型内部帧大小的可能性，我们探索了其作为基本视频分析任务的可访问选项的适用性，特别是在计算资源有限的情况下。

在我们对SmolVLM视频理解能力的评估中，我们实现了一个简单的**视频处理流水线代码**，从每个视频中提取最多50个均匀采样的帧，同时避免内部帧大小调整。
这种简单方法在CinePile基准测试中取得了令人惊讶的竞争性结果，得分为27.14%，这一性能使模型介于InternVL2（2B）和Video LlaVa（7B）之间。

定量结果与我们的定性测试一致，以下是一个来自FineVideo数据集的示例：

```
问题：特写镜头中展示了什么？
助手：特写镜头中，厨房台面上有亨氏番茄酱、蜂蜜、酱油和大蒜的瓶子。

问题：描述视频中发生了什么。
助手：视频显示一名男子在厨房做饭。
  他穿着黑色衬衫和黑色围裙。
  他站在台面前，手里拿着一瓶亨氏番茄酱、
  一瓶蜂蜜、酱油和一碗蒜末。
```

在第二个问题中，我们观察到一些时间理解上的局限性（厨师逐一指向食材，而非同时指向或握住所有食材），但SmolVLM展现了出色的场景理解和物体识别能力。

### VLMEvalKit集成

我们将SmolVLM与VLMEvalKit集成，以便在更多基准测试中轻松进行评估。

通过运行以下命令，您可以评估SmolVLM或您微调后的SmolVLM模型。

```bash
python run.py --data <benchmarks> --model SmolVLM --work-dir <output_directory>

```

例如，在MMMU开发验证集和MathVista迷你集上进行评估，并将结果存储在名为smol的文件夹中。

```bash
python run.py --data MMMU_DEV_VAL MathVista_MINI --model SmolVLM --work-dir smol

```

## 使用Transformers运行SmolVLM

您可以通过Transformers中的Auto类轻松加载SmolVLM。在底层，模型和处理器映射到与Idefics3相同的实现。

```python
from transformers import AutoProcessor, AutoModelForVision2Seq
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
model = AutoModelForVision2Seq.from_pretrained("HuggingFaceTB/SmolVLM-Instruct",
                                                torch_dtype=torch.bfloat16,
                                                _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager").to(DEVICE)

```

图像和文本可以任意交错排列，您也可以传入多张图像。以下是如何使用聊天模板并将格式化输入传递给处理器的方法。

```python
from PIL import Image
from transformers.image_utils import load_image



image1 = load_image("https://huggingface.co/spaces/HuggingFaceTB/SmolVLM/resolve/main/example_images/rococo.jpg")
image2 = load_image("https://huggingface.co/spaces/HuggingFaceTB/SmolVLM/resolve/main/example_images/rococo_1.jpg")


messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "image"},
            {"type": "text", "text": "你能描述一下这两张图片吗？"}
        ]
    },
]


prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image1, image2], return_tensors="pt")
inputs = inputs.to(DEVICE)

```

使用预处理后的输入开始生成，并对生成的输出进行解码。

```python

generated_ids = model.generate(**inputs, max_new_tokens=500)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)

print(generated_texts[0])

```

## 训练细节

### 数据集

首先，我们需要训练SmolLM2以扩展其上下文，这一点将在下一小节讨论。一旦我们拥有了长上下文的SmolLM2，我们便使用与训练Idefics3相同的数据来训练SmolVLM。主要使用了The Cauldron和Docmatix数据集。我们使用的完整数据集列表可在此处查看。

![图片描述](/images/posts/cb62e87f306e.png)

### 上下文扩展

![图片描述](/images/posts/b03b52539c9c.png)

SmolLM2的预训练上下文窗口对于视觉语言模型来说是不够的。图像被编码为许多Token，而我们希望支持多张图像。为了解决这个问题，我们根据“基于RoPE的外推缩放定律”的指导，将RoPE基值从10k增加到273k，从而将上下文窗口扩展到16k Token。我们在长上下文和短上下文数据集的混合数据上对模型进行了微调。
对于长上下文数据集，我们使用了Dolma中的“书籍”子集（主要是Project Gutenberg）以及来自The Stack的包含8k以上Token的代码文档，每个子集在最终混合数据中占比20%。对于短上下文数据集，我们精简了原始的SmolLM2预训练混合数据，使其包含20%的FineWeb-Edu、20%的DCLM以及20%来自我们数学数据集（即将发布）的数据。我们对数学数据集进行了上采样，以缓解在上下文扩展过程中观察到的GSM8k性能下降问题。
所有实验均使用EasyContext代码库实现。

### 检查点选择

在我们的训练过程中，我们每25个优化步骤保存一次检查点，这使我们能够评估并可能恢复模型在不同训练阶段的状态。这种做法对于确定最佳模型版本至关重要，因为训练时间更长并不总能保证更好的性能。
我们在多个视觉语言基准测试上评估了性能，每个基准测试根据其重要性被赋予不同的权重。核心基准测试包括：

- 通用多模态理解（MMMU和MMStar），这是最全面的基准测试。
- 文档和基于文本的视觉问答（DocVQA和TextVQA）
- 数学推理（MathVista）
- 图表理解（AI2D）

为了选择最佳检查点，我们通过手动分配不同权重将这些基准测试组合成一个单一指标，以反映它们在评估模型能力方面的相对重要性。我们使用这个单一指标来选择最佳检查点。通常，模型在更多训练后会在大多数基准测试上表现良好，但它们在DocVQA上的相对性能会显著下降。

## 微调

您可以使用Transformers对SmolVLM进行微调，并使用TRL应用对齐技术 🚀

我们提供了一个笔记本，用于在VQAv2数据集上对其进行微调，可以选择使用LoRA、QLoRA或全量微调。在笔记本中，您可以找到一些技巧，以节省更多内存并获得更大的批次大小，从而将SmolVLM适配到消费级GPU（如L4）中进行训练。使用批次大小为4、8位加载的QLoRA和梯度检查点，我们可以在L4上进行微调，大约消耗16 GB的显存。这使得您可以在Colab中微调您的SmolVLM！您可以调整参数，在训练时长和内存消耗之间找到合适的平衡点。

SmolVLM还集成了TRL，因此您可以通过命令行轻松应用直接偏好优化（DPO）。首先运行pip install trl accelerate peft，然后运行以下命令在RLAIF-V数据集上进行微调：

```bash
accelerate launch \
  --config_file examples/accelerate_configs/multi_gpu.yaml examples/scripts/dpo_vlm.py  \
  --dataset_name HuggingFaceH4/rlaif-v_formatted \
  --model_name_or_path HuggingFaceTB/SmolVLM-Instruct \
  --per_device_train_batch_size 8 \
  --gradient_accumulation_steps 32 \
  --dataset_num_proc 32 \
  --output_dir dpo_smolvlm_rlaif-v \
  --bf16 --torch_dtype bfloat16 \
  --use_peft --lora_target_modules=all-linear 

```

生成的LoRA适配器权重为SmolVLM-Instruct-DPO。关于基于视觉的LLM偏好调整的详细教程可在此处找到：dpo_vlm。

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

## 总结

我们向社区介绍了SmolVLM，一个完全开源、小巧而强大的视觉语言模型！我们还提供了工具供社区使用和定制。我们期待看到您用SmolVLM创造出什么。

以下是一些资源，如果您想了解更多关于SmolVLM的相关信息。

- 通过此演示开始体验SmolVLM。
- 学习如何使用此笔记本在VQAv2上微调SmolVLM。
- 了解更多关于视觉语言模型的信息。

---

> 本文由AI自动翻译，原文链接：[SmolVLM - small yet mighty Vision Language Model](https://huggingface.co/blog/smolvlm)
> 
> 翻译时间：2026-06-08 06:33
