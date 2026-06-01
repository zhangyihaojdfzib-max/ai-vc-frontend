---
title: Timm与Transformers集成：解锁视觉模型新能力
title_original: 'Timm ❤️ Transformers: Use any timm model with transformers'
date: '2025-01-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/timm-transformers
author: ''
summary: 本文介绍了TimmWrapper工具，它实现了timm库与🤗Transformers生态系统的无缝集成。通过这一集成，用户可以利用Transformers的管道API、Auto类兼容性、快速量化、Trainer微调、torch.compile加速等功能，轻松使用timm中丰富的计算机视觉模型（如MobileNetV4）。文章还展示了实际应用示例，包括图像分类、Gradio演示构建等，强调了该集成在简化工作流程、提升推理速度和模型微调效率方面的变革性意义。
categories:
- AI基础设施
tags:
- timm
- Transformers
- 计算机视觉
- 模型集成
- PyTorch
draft: false
translated_at: '2026-06-01T06:53:11.520537'
---

# Timm ❤️ Transformers: 将任意 timm 模型与 transformers 结合使用

获得闪电般的推理速度、快速量化、torch.compile 加速以及轻松微调任意 timm 模型——全部在友好的 🤗transformers 生态系统中完成。

TimmWrapper 应运而生——一个简单而强大的工具，能够释放这一潜力。

在本文中，我们将介绍：

- timm 集成的工作原理及其为何具有变革意义。
- 如何将 timm 模型与 🤗transformers 集成。
- 实际示例：管道、量化、微调等。

要跟随本文进行操作，请通过运行以下命令安装最新版本的 transformers 和 timm：

```bash
pip install -Uq transformers timm

```

查看包含所有代码示例和笔记本的完整仓库：
🔗TimmWrapper 示例

## 什么是 timm？

PyTorch 图像模型（timm）库提供了丰富的最先进计算机视觉模型集合，以及有用的层、工具、优化器和数据增强方法。截至撰写本文时，该项目拥有超过 32K 个 GitHub 星标和每日超过 20 万次下载，是用于图像分类、目标检测特征提取、分割、图像搜索及其他下游任务的首选资源。

凭借涵盖多种架构的预训练模型，timm 简化了计算机视觉从业者的工作流程。

## 为什么要使用 timm 集成？

虽然 🤗transformers 支持多种视觉模型，但 timm 提供了更广泛的集合，包括许多 transformers 中未提供的移动端友好且高效的模型。

timm 集成弥合了这一差距，融合了两者的优势：

- ✅ 管道 API 支持：轻松将任意 timm 模型插入高级 transformers 管道，实现简化推理。
- 🧩 与 Auto 类的兼容性：虽然 timm 模型原生不兼容 transformers，但集成使其能够与 Auto 类 API 无缝协作。
- ⚡ 快速量化：仅需约 5 行代码，即可量化任意 timm 模型以实现高效推理。
- 🎯 使用 Trainer API 进行微调：使用 Trainer API 微调 timm 模型，甚至可与低秩适配（LoRA）等适配器集成。
- 🔁 往返 timm：将微调后的模型重新用于 timm。
- 🚀 Torch Compile 加速：利用 torch.compile 优化推理时间。

## 管道 API：使用 timm 模型进行图像分类

timm 集成的一个突出特点是允许您利用 🤗pipeline API。pipeline API 抽象了大量复杂性，使您能够通过几行代码轻松加载预训练模型、执行推理并查看结果。

让我们看看如何将 transformers 管道与 MobileNetV4 结合使用。该架构没有原生的 transformers 实现，但可以轻松地从 timm 中使用：

```python
from transformers import pipeline
import requests


image_classifier = pipeline(model="timm/mobilenetv4_conv_medium.e500_r256_in1k")


url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/timm/cat.jpg"


outputs = image_classifier(url)


for output in outputs:
    print(f"标签: {output['label'] :20} 分数: {output['score'] :0.2f}")

```

输出：

```bash
设备设置为使用 cpu
标签: 虎斑猫              分数: 0.69
标签: 虎猫                分数: 0.21
标签: 埃及猫              分数: 0.02
标签: 蜜蜂                分数: 0.00
标签: 狨猴                分数: 0.00

```

## Gradio 集成：构建食物分类器演示 🍣

想要快速创建一个用于图像分类的交互式 Web 应用？Gradio 可以用最少的代码轻松构建用户友好的界面。让我们将 Gradio 与 pipeline API 结合，使用微调后的 timm ViT 模型（我们将在后续部分介绍微调）对食物图像进行分类。

以下是如何使用 timm 模型设置快速演示的方法：

```python
import gradio as gr
from transformers import pipeline


pipe = pipeline(
    "image-classification",
    model="ariG23498/vit_base_patch16_224.augreg2_in21k_ft_in1k.ft_food101"
)

def classify(image):
    return pipe(image)[0]["label"]

demo = gr.Interface(
    fn=classify,
    inputs=gr.Image(type="pil"),
    outputs="text",
    examples=[["./sushi.png", "sushi"]]
)

demo.launch()

```

这是一个托管在 Hugging Face Spaces 上的实时示例。您可以直接在浏览器中测试！

## Auto 类：简化模型加载

🤗transformers 库提供了 Auto 类来抽象加载模型和处理器的复杂性。借助 TimmWrapper，您可以使用 AutoModelForImageClassification 和 AutoImageProcessor 轻松加载任意 timm 模型。

以下是一个快速示例：

```python
from transformers import (
    AutoModelForImageClassification,
    AutoImageProcessor,
)
from transformers.image_utils import load_image

image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/timm/cat.jpg"
image = load_image(image_url)


checkpoint = "timm/mobilenetv4_conv_medium.e500_r256_in1k"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)
model = AutoModelForImageClassification.from_pretrained(checkpoint).eval()


print(type(image_processor))  
print(type(model))            

```

## 运行量化后的 timm 模型

量化是一种强大的技术，可以减少模型大小并加速推理，尤其适用于在资源受限设备上部署。借助 timm 集成，您可以使用 bitsandbytes 中的 BitsAndBytesConfig，仅需几行代码即可即时量化任意 timm 模型。

以下是对 timm 模型进行量化的简单方法：

```python
from transformers import TimmWrapperForImageClassification, BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
checkpoint = "timm/vit_base_patch16_224.augreg2_in21k_ft_in1k"

model = TimmWrapperForImageClassification.from_pretrained(checkpoint).to("cuda")
model_8bit = TimmWrapperForImageClassification.from_pretrained(
    checkpoint,
    quantization_config=quantization_config,
    low_cpu_mem_usage=True,
)

```

```python
original_footprint = model.get_memory_footprint()
quantized_footprint = model_8bit.get_memory_footprint()

print(f"原始模型大小: {original_footprint / 1e6:.2f} MB")
print(f"量化后模型大小: {quantized_footprint / 1e6:.2f} MB")
print(f"减少: {(original_footprint - quantized_footprint) / original_footprint * 100:.2f}%")

```

输出：

```
原始模型大小: 346.27 MB  
量化后模型大小: 88.20 MB  
减少: 74.53%  

```

量化后的模型在推理时性能几乎与全精度模型相同：

## timm 模型的监督微调

使用 🤗transformers 的 Trainer API 微调 timm 模型既直接又高度灵活。您可以使用 Trainer 类在自定义数据集上微调模型，该类负责训练循环、日志记录和评估。此外，您还可以使用 LoRA（低秩适配）进行微调，以更少的参数高效训练。

本节对标准微调和 LoRA 微调进行快速概述，并提供完整代码的链接。

### 使用 Trainer API 的标准微调

Trainer API 使得用最少的代码设置训练变得简单。以下是微调设置的大致框架：

```python
from transformers import TrainingArguments, Trainer


training_args = TrainingArguments(
    output_dir="my_model_output",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    load_best_model_at_end=True,
    push_to_hub=True,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)


trainer.train()

```

这种方法值得注意的地方在于，它镜像了原生 transformers 模型使用的精确工作流程，在不同模型类型之间保持了一致性。

这意味着你可以使用熟悉的`Trainer`API来微调不仅是Transformer模型，还包括任何`timm`模型——只需极少的调整，就能将`timm`库中的强大模型引入Hugging Face生态系统。这极大地扩展了你可以使用相同可靠工具和工作流程进行微调的模型范围。

模型示例：在Food-101上微调的ViT：`vit_base_patch16_224.augreg2_in21k_ft_in1k.ft_food101`

## 用于高效训练的LoRA微调

LoRA（低秩适应）允许你通过仅训练少量额外参数（而非全部模型权重）来高效微调大型模型。这使得微调速度更快，并且可以在消费级硬件上进行。你可以使用PEFT库通过LoRA来微调`timm`模型。

以下是设置方法：

```python
from peft import LoraConfig, get_peft_model

model = AutoModelForImageClassification.from_pretrained(checkpoint, num_labels=num_labels)
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["qkv"],
    lora_dropout=0.1,
    bias="none",
    modules_to_save=["head"],
)

lora_model = get_peft_model(model, lora_config)

lora_model.print_trainable_parameters()
```

使用LoRA的可训练参数：

```bash
trainable params: 667,493 || all params: 86,543,818 || trainable%: 0.77%
```

模型示例：在Food-101上使用LoRA微调的ViT：`vit_base_patch16_224.augreg2_in21k_ft_in1k.lora_ft_food101`

LoRA只是你可以应用于`timm`模型的高效适配器微调方法之一。`timm`与🤗生态系统的集成为你打开了多种参数高效微调（PEFT）技术的大门，让你可以选择最适合自己使用场景的方法。

### 使用LoRA微调模型进行推理

一旦模型完成LoRA微调，我们只需将适配器权重推送到Hugging Face Hub。本节将帮助你下载适配器权重，将适配器权重与基础模型合并，然后执行推理。

```python
from peft import PeftModel, PeftConfig

repo_name = "ariG23498/vit_base_patch16_224.augreg2_in21k_ft_in1k.lora_ft_food101"
config = PeftConfig.from_pretrained(repo_name)

model = AutoModelForImageClassification.from_pretrained(
    config.base_model_name_or_path,
    label2id=label2id,
    num_labels=num_labels,
    id2label=id2label,
    ignore_mismatched_sizes=True,
)
inference_model = PeftModel.from_pretrained(model, repo_name)
```

![来自微调模型的寿司预测图像](/images/posts/77d1596e71cd.png)

## 往返集成

Ross（`timm`的创建者）最喜欢的功能之一是，这种集成保持了完全的“往返”兼容性。也就是说，使用包装器，你可以在新数据集上使用`transformers`的`Trainer`微调`timm`模型，将生成的模型发布到Hugging Face Hub，然后再次使用`timm.create_model('hf-hub:my_org/my_fine_tuned_model', pretrained=True)`将微调后的模型加载回`timm`。

让我们看看如何用`timm`加载我们微调后的模型`ariG23498/vit_base_patch16_224.augreg2_in21k_ft_in1k.ft_food101`：

```python
checkpoint = "ariG23498/vit_base_patch16_224.augreg2_in21k_ft_in1k.ft_food101"

config = AutoConfig.from_pretrained(checkpoint)

model = timm.create_model(f"hf_hub:{checkpoint}", pretrained=True) 
model = model.eval()

image = load_image("https://cdn.britannica.com/52/128652-050-14AD19CA/Maki-zushi.jpg")

data_config = timm.data.resolve_model_data_config(model)
transforms = timm.data.create_transform(**data_config, is_training=False)

output = model(transforms(image).unsqueeze(0))

top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)

for prob, idx in zip(top5_probabilities[0], top5_class_indices[0]):
    print(f"Label: {config.id2label[idx.item()] :20} Score: {prob/100 :0.2f}%")
```

输出结果：

```bash
Label: sushi                Score: 0.98%
Label: spring_rolls         Score: 0.01%
Label: sashimi              Score: 0.00%
Label: club_sandwich        Score: 0.00%
Label: cannoli              Score: 0.00%
```

## Torch Compile：即时加速

借助PyTorch 2.0中的`torch.compile`，你只需一行代码即可编译模型，实现更快的推理。`timm`集成与`torch.compile`完全兼容。以下是一个快速基准测试，使用`TimmWrapper`比较使用和不使用`torch.compile`时的推理时间。

```python
model = TimmWrapperForImageClassification.from_pretrained(checkpoint).to(device)
processed_input = image_processor(image, return_tensors="pt").to(device)

def run_benchmark(model, input_data, warmup_runs=5, benchmark_runs=300):
    model.eval()
    with torch.no_grad():
        for _ in range(warmup_runs):
            _ = model(**input_data)

    times = []
    with torch.no_grad():
        for _ in range(benchmark_runs):
            start_time = time.perf_counter()
            _ = model(**input_data)
            if device.type == "cuda":
                torch.cuda.synchronize(device=device)  
            times.append(time.perf_counter() - start_time)

    avg_time = sum(times) / benchmark_runs
    return avg_time

time_no_compile = run_benchmark(model, processed_input)
compiled_model = torch.compile(model).to(device)
time_compile = run_benchmark(compiled_model, processed_input)

print(f"Without torch.compile: {time_no_compile:.4f} s")
print(f"With torch.compile: {time_compile:.4f} s")
```

![编译时间](/images/posts/a21cebdd54f5.png)

## 总结

`timm`与`transformers`的集成开启了以最小努力利用最先进视觉模型的新大门。无论你是想进行微调、量化，还是仅仅运行推理，这种集成都提供了一个统一的API来简化你的工作流程。

立即开始探索，解锁计算机视觉的新可能！

我们要特别感谢在Transformers PR #34564中促成此次集成的各位。特别感谢Pavel Iakubovskii、Ross Wightman、Lysandre Debut、Pablo Montalvo、Arthur Zucker和Amy Roberts的出色工作。你们的共同努力将这个功能从想法变成了每个人都能享受的成果！

---

> 本文由AI自动翻译，原文链接：[Timm ❤️ Transformers: Use any timm model with transformers](https://huggingface.co/blog/timm-transformers)
> 
> 翻译时间：2026-06-01 06:53
