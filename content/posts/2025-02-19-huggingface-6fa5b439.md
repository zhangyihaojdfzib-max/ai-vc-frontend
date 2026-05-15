---
title: 谷歌发布PaliGemma 2 Mix视觉语言模型
title_original: PaliGemma 2 Mix - New Instruction Vision Language Models by Google
date: '2025-02-19'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/paligemma2mix
author: ''
summary: 谷歌发布了PaliGemma 2 Mix，这是基于SigLIP和Gemma 2的视觉语言模型系列，提供3B、10B、28B三种尺寸及多种分辨率。该模型在OCR、长短描述、视觉问答、目标检测和图像分割等任务上进行了微调，支持开放式提示词，性能优于带任务前缀的提示方式。文章介绍了模型架构、不同变体在通用视觉任务、文档理解、定位和文本识别上的表现，并提供了使用Transformers进行推理和微调的指导。
categories:
- AI产品
tags:
- 谷歌
- 视觉语言模型
- PaliGemma 2
- 多模态AI
- 图像理解
draft: false
translated_at: '2026-05-15T05:56:45.768817'
---

# PaliGemma 2 Mix - 谷歌推出的全新指令视觉语言模型

## 摘要

去年12月，谷歌发布了PaliGemma 2：基于SigLIP和Gemma 2的全新预训练（pt）PaliGemma视觉语言模型（VLM）系列。该系列模型提供三种不同尺寸（3B、10B、28B）和三种不同分辨率（224x224、448x448、896x896）。

今天，谷歌发布了PaliGemma 2 Mix：在多种视觉语言任务上进行微调的版本，包括OCR、长短描述等。

PaliGemma 2预训练（pt）变体是用于迁移到特定任务的优秀视觉语言模型。所有pt检查点均旨在针对下游任务进行微调，并为此目的而发布。

![PaliGemma2架构](/images/posts/5cef8c86f5ac.png)

Mix模型能快速展示将预训练检查点微调到下游任务时可获得的性能。PaliGemma模型系列的主要目的是提供能在下游任务上更好学习的预训练模型，而非提供通用的对话模型。Mix模型能很好地反映pt模型在学术数据集混合微调时的表现。

您可以在这篇博客文章中了解更多关于PaliGemma 2的信息。

您可以在该集合中找到所有Mix模型和演示。

- PaliGemma 2 Mix模型
- PaliGemma 2 Mix变体对比
- 使用Transformers进行推理和微调
- 演示

## PaliGemma 2 Mix模型

PaliGemma 2 Mix模型可完成多种任务。我们可以按子任务分类如下：

- 通用视觉语言相关任务：视觉问答、图像指代
- 文档理解：信息图表、图表和示意图的视觉问答
- 图像中的文本识别：文本检测、含文本图像的描述、含文本图像的视觉问答
- 定位相关任务：目标检测、图像分割

请注意，此子任务列表并非详尽无遗，您可以在PaliGemma 2论文中获取完整任务列表的更多信息。

在使用PaliGemma 2 Mix模型时，我们可以使用开放式提示词。在上一版PaliGemma预训练模型中，我们需要根据特定语言要完成的任务在提示词中添加任务前缀。这种方法仍然有效，但开放式提示词能带来更好的性能。带任务前缀的提示词示例如下：

- "caption {lang}"：简洁的类COCO短描述
- "describe {lang}"：更长、更具描述性的描述
- "ocr"：光学字符识别
- "answer {lang} {question}"：关于图像内容的问答
- "question {lang} {answer}"：针对给定答案生成问题

仅使用任务前缀的两个任务是目标检测和图像分割。提示词如下所示：

- "detect {object description}"：定位图像中列出的对象并返回这些对象的边界框
- "segment {object description}; {object description}"：定位图像中对象所占区域，为该对象创建图像分割

如果您想立即开始，请直接跳转到博客的此部分，或尝试演示。

## PaliGemma 2 Mix变体对比

在本节中，我们将回顾上述能力，PaliGemma 2 Mix在这些能力上的表现，并在几个任务上比较不同尺寸和分辨率的不同变体。这里，我们在一些实际场景示例上测试模型。

### 通用视觉语言任务

![](/images/posts/23d25615febb.jpg)

![](/images/posts/35251fd1163c.jpg)

### 文档理解

![](/images/posts/8f009a9f78f4.png)

![](/images/posts/ca341f09d570.png)

### 定位任务

我们根据定位相关能力评估了PaliGemma 2 Mix变体。给定提示词"detect {object description};{another object description}"及不同的感兴趣对象，PaliGemma可以检测不同的感兴趣对象。这里的提示词不限于"bird"这样的短类别，也可以是"bird on a stick"。

下面，您可以找到不同变体在固定分辨率448x448下的检测和分割输出。为便于可视化，我们放大了感兴趣对象。

![使用PaliGemma 2 Mix进行分割](/images/posts/33c38e234972.png)

![使用PaliGemma 2 Mix进行检测](/images/posts/c12892d76000.png)

### 图像中的文本识别

![](/images/posts/6d2dc54129a4.jpg)

## 使用Transformers进行推理和微调

您可以使用transformers来使用PaliGemma 2 Mix模型。

```python
from transformers import (
    PaliGemmaProcessor,
    PaliGemmaForConditionalGeneration,
)
from transformers.image_utils import load_image
import torch

model_id = "google/paligemma2-10b-mix-224"

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg"
image = load_image(url)


model = PaliGemmaForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto").eval()
processor = PaliGemmaProcessor.from_pretrained(model_id)


prompt = "describe en"
model_inputs = processor(text=prompt, images=image, return_tensors="pt").to(torch.bfloat16).to(model.device)
input_len = model_inputs["input_ids"].shape[-1]


with torch.inference_mode():
    generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
    generation = generation[0][input_len:]
    decoded = processor.decode(generation, skip_special_tokens=True)
    print(decoded)

```

我们有一份关于微调PaliGemma 2的深入教程。同样的笔记本也可用于微调Mix检查点。

我们发布了一个448x448分辨率的10B模型演示。您可以在下方试用，或通过此链接访问应用。

阅读并了解更多关于PaliGemma模型的信息：

- 博客：PaliGemma – 谷歌前沿开源视觉语言模型
- 博客：欢迎PaliGemma 2 – 谷歌全新视觉语言模型
- PaliGemma 2技术报告
- PaliGemma微调教程
- PaliGemma 2 Mix模型发布集合
- PaliGemma 2发布集合
- 试用演示

## 致谢

我们要感谢Sayak Paul和Vaibhav Srivastav对本博客文章的审阅。我们感谢谷歌团队发布了这个优秀且开源的模型系列。

特别感谢Pablo Montalvo将模型集成到transformers中，以及Lysandre、Raushan、Arthur、Yih-Dar和团队其他成员对代码的审阅、测试和及时合并。

---

> 本文由AI自动翻译，原文链接：[PaliGemma 2 Mix - New Instruction Vision Language Models by Google](https://huggingface.co/blog/paligemma2mix)
> 
> 翻译时间：2026-05-15 05:56
