---
title: PaddleOCR 3.5：集成Transformers后端的OCR与文档解析
title_original: 'PaddleOCR 3.5: Running OCR and Document Parsing Tasks with a Transformers
  Backend'
date: '2026-05-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers
author: ''
summary: PaddleOCR 3.5版本将OCR和文档解析任务更紧密地融入Hugging Face生态系统，支持通过设置engine="transformers"使用Transformers作为推理后端。该版本引入了更灵活的推理引擎接口，开发者可通过engine参数选择后端，并通过engine_config配置dtype、设备放置等选项。这一更新降低了RAG、文档AI和文档Agent等应用在数据摄取环节的集成摩擦，使PP-OCRv5和PaddleOCR-VL
  1.5等模型能更自然地与以Transformers为中心的技术栈协同工作。文章提供了快速安装指南和命令行及Python API使用示例。
categories:
- AI产品
tags:
- PaddleOCR
- OCR
- Transformers
- 文档解析
- Hugging Face
draft: false
translated_at: '2026-05-19T06:11:51.531566'
---

# PaddleOCR 3.5：使用 Transformers 后端运行 OCR 和文档解析任务

PaddleOCR 3.5 将 OCR 和文档解析任务更紧密地融入 Hugging Face 生态系统。通过此版本，支持的 PaddleOCR 模型可以通过以下设置，使用 Hugging Face Transformers 作为推理后端运行：

```python
engine="transformers"
```

PaddleOCR 持续提供如 PP-OCRv5 等 OCR 模型系列以及如 PaddleOCR-VL 1.5 等文档解析模型系列，而 Transformers 成为运行这些模型所支持的推理后端之一。

在 Hugging Face Spaces 上试用在线演示：https://huggingface.co/spaces/PaddlePaddle/paddleocr-3.5-transformers-demo

## 有什么变化？

PaddleOCR 3.5 引入了更灵活的推理引擎接口。开发者可以通过 `engine` 参数选择后端，并通过 `engine_config` 传递后端特定的选项。

在实践中，这意味着：

- 这些任务背后的流水线由 PaddleOCR 管理，因此开发者无需手动调用每个内部组件。
- Transformers 成为运行支持的 PaddleOCR 模型所支持的推理后端之一。
- 开发者可以通过 `engine_config` 配置与后端相关的选项，例如 `dtype`、设备放置和注意力机制实现。

理解这一技术栈的简单方式：

此版本主要涉及推理后端层：PaddleOCR 继续提供 OCR 和文档解析能力，而 Transformers 为支持的 PaddleOCR 模型提供了另一个后端选项，使其能够自然融入以 Hugging Face 为中心的环境。更广泛的文档 AI 工作流仍由开发者和应用构建者掌控。

## 为何重要

对于 RAG（检索增强生成）、文档 AI 和文档 Agent（智能体）应用而言，难点往往在 LLM（大语言模型）之前就已出现。

开发者首先需要将 PDF、扫描文档、截图、表格、图表、公式和复杂的页面布局转化为可靠的结构化数据。如果这一数据摄取环节薄弱，下游的 LLM（大语言模型）工作流可能会遗漏关键信息、检索到错误的上下文，或产生不可靠的答案。

PaddleOCR 通过提供 PP-OCRv5 等 OCR 系列模型以及 PaddleOCR-VL-1.5 等文档解析系列模型，帮助应对这一文档摄取挑战。

借助 PaddleOCR 3.5，这些能力现在可以更轻松地与以 Transformers 为中心的技术栈连接。支持的 PaddleOCR 模型可以使用 Transformers 后端运行，而 PaddleOCR 继续在后台管理 OCR 或文档解析流水线。

对于开发者而言，这意味着更少的集成摩擦，以及从文档到下游 RAG（检索增强生成）、Agent（智能体）、搜索、分析或自动化工作流的更自然路径。

## 快速开始

安装 PaddleOCR 3.5、PaddleX、Transformers 以及适用于你硬件的兼容 PyTorch 版本。

例如，在 CUDA 12.6 环境中：

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
python -m pip install "paddleocr==3.5.0" "paddlex==3.5.2" "transformers>=5.4.0"
```

对于 CPU、ROCm 或其他环境，请安装与目标硬件匹配的 PyTorch 版本。

从命令行运行：

```bash
paddleocr ocr \
  -i https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png \
  --device gpu:0 \
  --engine transformers
```

或使用 Python API：

```python
from paddleocr import PaddleOCR

pipeline = PaddleOCR(
    device="gpu:0",
    engine="transformers",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine_config={
        "dtype": "float32",
    },
)

results = pipeline.predict(
    "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png"
)

for result in results:
    print(result)
```

Hugging Face Space 使用 `float32` 以实现广泛兼容性。对于你自己的硬件，你可以通过 `engine_config` 调整后端特定选项：

```python
engine_config = {
    "dtype": "bfloat16",
    "device_type": "gpu",
    "device_id": 0,
    "attn_implementation": "sdpa",
}
```

最佳配置取决于你的模型、硬件和部署环境。

## 何时应使用 Transformers 后端？

当你希望 PaddleOCR 的 OCR 和文档解析能力更自然地融入以 Hugging Face 为中心的技术栈时，请使用 Transformers 后端。

如果你正在构建 RAG（检索增强生成）、文档 AI、搜索、分析或 Agent（智能体）应用，并且已经依赖 PyTorch / Transformers 基础设施进行模型加载、实验、部署或模型工件管理，这将特别有用。

Transformers 后端在以下情况下是一个不错的选择：

- 对于已经使用 Transformers 的团队，提供更熟悉的开发体验，
- 支持 PaddleOCR 模型的 Hub 兼容模型发现与分发，
- 更易于与现有的 PyTorch / Transformers 服务集成。

当最大化 OCR 或文档解析吞吐量是首要目标时，PaddleOCR 默认的 `paddle_static` 后端通常是推荐选择。

此版本并非要用一个后端取代另一个后端，而是为开发者提供更多灵活性：使用 PaddleOCR 获得 OCR 和文档解析能力，并选择最适合你技术栈的推理后端。

## 立即尝试

在 Hugging Face Spaces 上试用 PaddleOCR 3.5 Transformers 演示：

https://huggingface.co/spaces/PaddlePaddle/paddleocr-3.5-transformers-demo

在 Hub 上探索 PaddleOCR 模型：

https://huggingface.co/PaddlePaddle/models

PaddleOCR 3.5 将 OCR 和文档解析能力更紧密地融入以 Transformers 为中心的工作流，同时赋予开发者围绕这些能力构建更广泛文档 AI 应用的自由。

## 资源

- PaddleOCR 文档：https://www.paddleocr.ai/
- PaddleOCR 在 GitHub 上：https://github.com/PaddlePaddle/PaddleOCR
- PaddlePaddle 在 Hugging Face 上的组织：https://huggingface.co/PaddlePaddle
- PaddleOCR 3.5 Transformers 在 Spaces 上的演示：https://huggingface.co/spaces/PaddlePaddle/paddleocr-3.5-transformers-demo

## 致谢

我们衷心感谢支持 PaddleOCR 3.5 Transformers 集成的 Hugging Face 工程师。

特别感谢 **Anton Vlasjuk** 的全程参与，包括审查和合并所有相关的拉取请求。

我们也感谢 **Raushan Turganbay** 和 **Yoni Gozlan** 提供的宝贵 PR 审查和反馈。

他们的指导帮助提升了 Hugging Face 社区的集成质量、文档和开发者体验。

---

> 本文由AI自动翻译，原文链接：[PaddleOCR 3.5: Running OCR and Document Parsing Tasks with a Transformers Backend](https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers)
> 
> 翻译时间：2026-05-19 06:11
