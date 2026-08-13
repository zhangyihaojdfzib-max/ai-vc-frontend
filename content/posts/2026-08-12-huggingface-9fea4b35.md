---
title: LFM2.5-VL-3B：边缘设备上的高效视觉语言模型
title_original: LFM2.5-VL-3B for Better and Faster Vision Capabilities for the Edge
date: '2026-08-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b
author: ''
summary: LFM2.5-VL-3B是专为边缘设备设计的视觉-语言模型，通过四项重大改进（屏幕理解、定位、多图像输入和函数调用）提升了性能。该模型采用SigLIP2视觉编码器和LFM2.5文本主干，预训练数据量达34T
  token，视觉数据量是之前的4倍。在基准测试中，它领先于同尺寸模型，并支持CPU和GPU高效推理，在M5 Max上解码速度达228 token/秒。模型发布首日即获得llama.cpp、vLLM等生态支持，适合高吞吐量端侧工作负载。
categories:
- AI产品
tags:
- 视觉语言模型
- 边缘计算
- 模型推理
- 多模态AI
- 端侧部署
draft: false
translated_at: '2026-08-13T04:22:57.430642'
---

# LFM2.5-VL-3B：为边缘设备提供更优、更快的视觉能力

LFM2.5-VL-3B 是我们最强大的视觉-语言模型，您可以在自己的硬件上运行它。它能理解文档和屏幕内容，定位物体，并能调用工具。它直接作答而非进行推理，因此响应速度在实时和端侧应用中依然很快。

LFM2.5-VL-3B 在先前版本的基础上，通过四项重大改进扩展了视觉-语言能力：

- **屏幕/UI 理解**：对不同设备上的数字屏幕有很强的理解能力。
- **定位**：通过自然语言查询，提升了定位和物体检测能力。
- **多图像输入**：改进了跨多张图像的推理能力。
- **函数调用**：在纯文本和视觉-文本场景下的函数调用能力显著增强。

![lfm2_5_vl_3b_task_group_averages](/images/posts/0846e9b1c214.png)

## 我们如何训练这个最强大的视觉-语言模型

LFM2.5-VL-3B 将 SigLIP2 400M NaFlex 视觉编码器与我们 LFM2.5-2.6B 文本模型相同的预训练主干网络配对。它在大约 34T 的 Token 上进行了预训练，视觉数据量是之前的 4 倍，这些数据来自精选和合成的图像-标题、OCR、定位和指令遵循数据集。为了支持非拉丁文字，我们通过就地扩展分词器将词汇量翻倍至 128K，而不是从头重新训练。

后训练分两个阶段进行：首先是监督微调（SFT），包括从更大的教师模型进行知识蒸馏和 Antidoom 训练。其次是多奖励强化学习（RL）。

## 基准测试结果

我们在视觉和文本基准上对 LFM2.5-VL-3B 进行了评估。

**视觉基准**涵盖多语言视觉理解、指令遵循、视觉数学和科学推理、文档理解、物体检测、多图像理解和屏幕理解。LFM2.5-VL-3B 在真实世界图像任务上领先于其尺寸级别，同时也能很好地读取数字内容，从文档、图表到屏幕上的 UI 元素。

*表中的所有值均归一化为 0–100。评估使用 vLLM 0.26.0 以及每个模型推荐的生成参数（如有）进行。所有地方均使用非推理模式，模型被提示直接回答而不进行推理。

我们还在**纯文本基准**上评估了 LFM2.5-VL-3B 的指令遵循和工具使用能力。指令遵循能力全面提升，工具使用能力大幅提升。在工具使用方面，LFM2.5-VL-3B 与 Gemma-4-E2B 和 Qwen3.5-2B 相当。

*InternVL 3.5 模型不支持函数调用。

这些结果表明，LFM2.5-VL-3B 是一个强大的通用视觉-语言模型。它涵盖了日常任务（图像描述、视觉问答、文档理解），并且特别擅长物体定位、读取屏幕和文档以及调用工具。

## CPU 和 GPU 上的推理速度

LFM2.5-VL-3B 在发布首日即获得整个推理生态系统的支持，包括 llama.cpp、MLX、vLLM、SGLang 和 ONNX。

**端侧推理。** LFM2.5-VL-3B 在 M5 Max 上解码速度为 228 Token/秒，在 Ryzen AI Max+ 395 上为 116 Token/秒，内存占用约 3 GB。它甚至在 Galaxy S26 Ultra 上也能达到 20 Token/秒的速度，因此您可以完全在设备端运行它。

![lfm2_5_vl_3b_on-device_inference_TTFT](/images/posts/45226f1b7a56.png)

**GPU 推理。** LFM2.5-VL-3B 始终保持低延迟，并且在多帧输入上速度最快。

![lfm2_5_vl_3b_ttft](/images/posts/abd799e07991.png)

在我们测试的所有模型中，LFM2.5-VL-3B 的输出吞吐量也是最快的，在高并发下可达每秒约 11K Token。这大约是更大的 4B 级模型的 2 倍，甚至超过了更小的 2B 级模型，这意味着在单个 H100 上每天可输出近 10 亿 Token。

![lfm2_5_vl_3b_throughput](/images/posts/84327799d355.png)

## 如何使用 LFM2.5-VL-3B

当您需要为高吞吐量工作负载提供端侧智能时，请选择 LFM2.5-VL-3B。

安装最新版本的 transformers（兼容 transformers>=5.0.0）：

```shell
%pip install -q torch torchvision accelerate "transformers>=5.10.1"

```

然后加载并运行模型：

```py
import torch
from transformers.image_utils import load_image
from transformers import AutoModelForImageTextToText, AutoProcessor
from IPython.display import display

MODEL_ID = "LiquidAI/LFM2.5-VL-3B" 

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_ID,
    device_map="auto",
    dtype="bfloat16",
)

img_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/coco_sample.png"
input_image = load_image(img_url)
display(input_image)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": input_image},
            {"type": "text", "text": "Describe this image in two concise sentences."},
        ],
    }
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        do_sample=True,
        temperature=0.2,
        top_k=50,
        repetition_penalty=1.0,
        max_new_tokens=256,
    )

output = processor.batch_decode(outputs[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
print(output)

```

![cats_image](/images/posts/1e3ca7662687.jpg)

```
Two cats are sleeping on a pink couch with two remote controls.

```

您可以在我们的文档中找到更多关于如何使用 LFM2.5-VL3B 进行多图像输入、定位、OCR、工具调用等的实践示例。查看我们的发布博客以获取视频示例。

## LFM2.5-VL-3B 演示

查看这个浏览器演示，了解 LFM2.5-VL-3B 如何驱动一个支持视觉的聊天界面。它允许您拍摄或上传多张图像，并让模型与之交互，包括定位、OCR 和工具使用。

## 开始使用

LFM2.5-VL-3B 今天已在 Hugging Face 上可用。

通过 LFM2.5，我们正在实现“AI 随处运行”的愿景。这些模型：

- **下载**：在 Hugging Face 上获取 LFM2.5-VL-3B。
- **试用**：在浏览器中运行 WebGPU 演示，无需任何设置。
- **微调**：通过我们的微调教程，将 LFM2.5-VL-3B 适配到您的任务中。

我们迫不及待地想看到您构建的成果。

## 引用

请引用本文为：

```
Liquid AI, "LFM2.5-VL-3B: A Better and Faster Vision-Language Model for the Edge", Liquid AI Blog, Aug 2026.

```

或使用 BibTeX 引用：

```
@article{liquidAI2026VL3B,
  author  = {Liquid AI},
  title   = {LFM2.5-VL-3B: A Better and Faster Vision-Language Model for the Edge},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm2-5-vl-3b},
}

```

---

> 本文由AI自动翻译，原文链接：[LFM2.5-VL-3B for Better and Faster Vision Capabilities for the Edge](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b)
> 
> 翻译时间：2026-08-13 04:22
