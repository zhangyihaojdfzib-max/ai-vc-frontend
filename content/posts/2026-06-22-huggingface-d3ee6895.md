---
title: PP-OCRv6登陆Hugging Face：多语言OCR模型系列
title_original: 'PP-OCRv6 on Hugging Face: 50-Language OCR from 1.5M to 34.5M Parameters'
date: '2026-06-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/PaddlePaddle/pp-ocrv6
author: ''
summary: PP-OCRv6是PaddleOCR最新通用OCR模型系列，已登陆Hugging Face平台。该系列提供tiny、small、medium三个等级，参数规模从1.5M到34.5M，支持50种语言（含中、英、日及46种拉丁语系语言）。模型采用PPLCNetV4骨干网络，检测模块升级为RepLKFPN，识别模块使用EncoderWithLightSVTR，在官方基准测试中，medium版本检测Hmean达86.2%，识别准确率83.2%，较前代分别提升4.6和5.1个百分点。文章介绍了模型架构改进、多语言支持及快速集成方法。
categories:
- AI产品
tags:
- PP-OCRv6
- OCR
- PaddleOCR
- 多语言识别
- Hugging Face
draft: false
translated_at: '2026-06-23T06:08:13.634139'
---

# PP-OCRv6 登陆 Hugging Face：从 1.5M 到 34.5M 参数的 50 种语言 OCR

在线评估 PP-OCRv6，然后通过 PaddlePaddle、Transformers 或 ONNX Runtime 后端集成轻量级、生产就绪的 OCR。

PP-OCRv6 是 PaddleOCR 通用 OCR 模型系列的最新版本。它专为文档、截图、多语言图像、数字显示屏、工业标签和场景文本中的真实文本检测与识别而设计。

![ppocrv6_det_vis](/images/posts/85f16eb1fb07.jpg)

该模型系列的参数规模从 1.5M 到 34.5M，分为三个等级：tiny、small 和 medium。medium 和 small 等级支持 50 种语言，包括简体中文、繁体中文、英语、日语以及 46 种拉丁字母语言。快速在线体验 PP-OCRv6：PP-OCRv6 在线演示。

![ocrv6_models](/images/posts/85e9a2d48d5c.jpg)

在 PaddleOCR 官方内部多场景 OCR 基准测试中，PP-OCRv6_medium 达到了 86.2% 的检测 Hmean 和 83.2% 的识别准确率。与 PP-OCRv5_server 相比，文本检测提升了 +4.6 个百分点，文本识别提升了 +5.1 个百分点。

![v6acc_opt](/images/posts/a71b42664b9f.png)

PP-OCRv6 聚焦于一个实际的 OCR 需求：通过小型模型和灵活的部署选项，生成准确、结构化的文本输出。关于为何在 VLM 时代专用 OCR 模型仍然有用的深入讨论，请参阅我们之前的博客：PP-OCRv5 登陆 Hugging Face：一种专用 OCR 方法。

## PP-OCRv6 的新特性

PP-OCRv6 在检测和识别方面引入了架构、训练和数据的改进。主要设计目标是在保持模型大小适合不同部署场景的同时，提升 OCR 准确率。

### 三个模型等级

PP-OCRv6 提供三个模型等级，涵盖不同的模型大小和 OCR 准确率水平。

### PPLCNetV4 骨干网络

PP-OCRv6 使用 PPLCNetV4 作为文本检测和文本识别的统一骨干网络。

对于开发者而言，主要好处是整个模型系列的一致性。tiny、small 和 medium 等级并非互不相关的模型；它们属于同一个 OCR 系列，共享共同的架构方向。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzQ2ODgzNWViOTJhYjMzZDUxNTMyY2RlMzdhMDAwZmNfZWJmZGY5NTljOWJlY2YyODVhYzg0N2NhNTk3MjQwMTRfSUQ6NzY1MjcxNjg0NDE1OTMyMzA5N18xNzgxODE5MjkwOjE3ODE5MDU2OTBfVjM)

### 用于文本检测的 RepLKFPN

文本检测是 OCR 流程的第一阶段。检测质量会影响送入识别器的裁剪区域，而质量差的裁剪区域通常会导致较差的识别效果。

PP-OCRv6 使用 RepLKFPN 升级了检测模块，这是一种轻量级的大核特征金字塔网络，专为多尺度文本检测设计，同时保持推理高效。

这对于真实世界的 OCR 输入至关重要，因为文本可能较小、密集、旋转、低分辨率或嵌入复杂背景中。

![ppocrv6_det_pip_ori](/images/posts/8edbeb3680d3.png)

### 用于识别的 EncoderWithLightSVTR

对于文本识别，PP-OCRv6 使用 EncoderWithLightSVTR。它将局部上下文建模与全局注意力相结合，以提升具有挑战性的文本裁剪区域的识别质量。

识别方面的改进尤其适用于多语言文本、屏幕文本、工业字符、特殊符号、密集文本和噪声图像区域。

![rec](/images/posts/3ab53ea38148.png)

### 统一的多语言 OCR

medium 和 small 等级在一个模型系列中支持 50 种语言，涵盖简体中文、繁体中文、英语、日语以及 46 种拉丁字母语言。

这有助于减少在常见的多语言 OCR 场景中需要单独 OCR 模型的需求。

## 使用 PaddleOCR 快速上手

安装 PaddleOCR：

```Bash
pip install paddleocr

```

使用 Paddle 推理（默认后端）运行 OCR：

```Python
from paddleocr import PaddleOCR



ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
result = ocr.predict("https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png")

for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")

```

OCR 结果可以保存为可视化图像和结构化的 JSON 输出。结构化输出随后可供下游系统使用，例如文档解析、搜索、提取、RAG、分析或 Agent 工作流。

## 可用的推理后端

通过 PaddleOCR，PP-OCRv6 可与多种推理后端一起使用。PaddleOCR 3.7 提供了统一的推理引擎接口，其中 engine 选择底层运行时，相关配置可通过 pipeline 或模块 API 传递。

对于 Hugging Face 用户，PaddleOCR 支持使用 Transformers 后端运行选定的 OCR 和文档解析模型。可以通过以下方式启用：

```Python
engine="transformers"

```

有关 Transformers 后端在 PaddleOCR 中如何工作的更多详细信息，请参阅：

PaddleOCR：使用 Transformers 后端运行 OCR 和文档解析任务

使用 Transformer 后端运行 PP-OCRv6 示例：

```Python

from paddleocr import PaddleOCR



ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="transformers",
)
result = ocr.predict("https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png")

```

PP-OCRv6 系列中也提供了 ONNX 变体，适用于通过 engine="onnxruntime" 使用 ONNX Runtime 的环境：

```Python
from paddleocr import PaddleOCR



ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="onnxruntime",
)
result = ocr.predict("https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png")

```

这些后端选项共同使 PP-OCRv6 能够在不同的运行时环境中使用，同时在 Hugging Face Hub 上保持相同的 OCR 模型系列。

PP-OCRv6 通过一个轻量级、多语言的 OCR 模型系列扩展了 PaddleOCR，用于真实世界的文本检测与识别。

该版本包括三个模型等级，参数规模从 1.5M 到 34.5M，支持多达 50 种语言的 OCR，相比 PP-OCRv5_server 提升了检测和识别准确率，并在 Hugging Face Hub 上提供了多种模型格式，包括 safetensors、Paddle 推理模型和 ONNX 模型。

结合托管的 Hugging Face Space 和可用的 PaddleOCR 推理后端，PP-OCRv6 提供了多个评估和集成的入口点：

- 在线演示：PP-OCRv6 在线演示
- 模型系列：PP-OCRv6 系列
- Transformers 后端博客：PaddleOCR with Transformers Backend
- PaddleOCR 文档：PP-OCRv6 文档
- PaddleOCR 官方网站：https://www.paddleocr.com

在线演示：PP-OCRv6 在线演示

模型系列：PP-OCRv6 系列

Transformers 后端博客：PaddleOCR with Transformers Backend

PaddleOCR 文档：PP-OCRv6 文档

PaddleOCR 官方网站：https://www.paddleocr.com

您可以通过在线演示评估 PP-OCRv6，探索系列中可用的模型资产，并使用与您自身 OCR 工作流相匹配的推理后端。

---

> 本文由AI自动翻译，原文链接：[PP-OCRv6 on Hugging Face: 50-Language OCR from 1.5M to 34.5M Parameters](https://huggingface.co/blog/PaddlePaddle/pp-ocrv6)
> 
> 翻译时间：2026-06-23 06:08
