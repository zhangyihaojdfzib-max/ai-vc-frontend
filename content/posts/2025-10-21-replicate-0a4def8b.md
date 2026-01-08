---
title: 使用Datalab Marker与OCR模型高效提取文档图像文本
title_original: Extract text from documents and images with Datalab Marker and OCR
  – Replicate blog
date: '2025-10-21'
source: Replicate Blog
source_url: https://replicate.com/blog/datalab-marker-and-ocr-fast-parsing
author: ''
summary: 本文介绍了Datalab在Replicate平台发布的两款先进文档解析模型：Marker和OCR。Marker能够将PDF、DOCX、PPTX及图像等多种格式转换为结构化的Markdown或JSON，支持表格、公式、代码的格式化以及基于JSON
  Schema的特定字段提取。OCR模型则专注于从图像和文档中检测多达90种语言的文本，并识别阅读顺序与表格网格。文章通过代码示例展示了其使用方法，并指出这些基于开源项目的模型在速度和准确性上超越了Tesseract等传统工具，Marker在基准测试中表现优异。
categories:
- AI产品
tags:
- OCR
- 文档解析
- 文本提取
- Replicate
- Datalab
draft: false
translated_at: '2026-01-08T04:44:53.544213'
---

-   Replicate
-   Blog

# 使用 Datalab Marker 和 OCR 从文档与图像中提取文本

-   andreasjansson

Datalab 先进的文档解析与文本提取模型现已登陆 Replicate。

![OCR](/images/posts/859c24fa28b8.webp)

**Marker** 能将 PDF、DOCX、PPTX、图像（以及更多格式！）转换为 Markdown 或 JSON。它能格式化表格、数学公式和代码，提取图像，并且当您传入 JSON Schema 时，可以提取特定字段。

**OCR** 能从图像和文档中检测九十种语言的文本，并返回阅读顺序和表格网格。

Marker 模型基于广受欢迎的开源 **Marker** 项目（29k GitHub stars），OCR 则基于 **Surya**（19k GitHub stars）。

在 Replicate 上运行 Marker 和 OCR：

*   Marker：replicate.com/datalab-to/marker
*   OCR：replicate.com/datalab-to/ocr

```
import replicate

output = replicate.run(
    "datalab-to/marker",
    input={
        "file": open("report.pdf", "rb"),
        "mode": "balanced",  # fast / balanced / accurate
        "include_metadata": True,  # return page-level JSON metadata
    },
)
print(output["markdown"][:400])
```

```
import replicate

output = replicate.run(
    "datalab-to/ocr",
    input={
        "file": open("receipt.jpg", "rb"),
        "visualize": True,  # return the input image with red polygons around detected text
        "return_pages": True,  # return layout data
    },
)
print(output["text"][:200])
```

访问 Replicate 上的模型页面，获取其他语言的代码片段。

这些模型既快速又准确。它们超越了 Tesseract 等成熟工具，处理时间短。Marker 处理一页大约需要 0.18 秒，批量处理时每秒可达 120 页。

## 结构化提取

Marker 一个特别强大的功能是结构化提取。例如，您可以从发票中提取特定字段：

```
import json
import replicate

schema = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "invoice_number": {"type": "string"},
        "date": {"type": "string"},
        "total": {"type": "number"}
    }
}

output = replicate.run(
    "datalab-to/marker",
    input={
        "file": "https://multimedia-example-files.replicate.dev/replicator-invoice.1page.pdf",
        "page_schema": json.dumps(schema),
    }
)
structured_data = json.loads(output["extraction_schema_json"])
print(structured_data)
```

Marker 的性能使用 **olmOCR-Bench** 基准进行评估，该数据集包含 1,403 个 PDF 文件和 7,010 个单元测试用例，用于评估 OCR 系统在将 PDF 文档准确转换为 Markdown 格式的同时，保留关键文本和结构信息的能力。

Marker 的表现优于所有测试模型，包括 GPT-4o、Deepseek OCR、Mistral OCR 和 olmOCR。

*   在 `fast` 和 `balanced` 模式下，不使用 `page_schema` 时，每 1000 页 4 美元。
*   使用 `page_schema` 进行结构化提取时，每 1000 页 6 美元。
*   在 `accurate` 模式下，每 1000 页 6 美元。

OCR 每 1000 页收费 2 美元。

---

> 本文由AI自动翻译，原文链接：[Extract text from documents and images with Datalab Marker and OCR – Replicate blog](https://replicate.com/blog/datalab-marker-and-ocr-fast-parsing)
> 
> 翻译时间：2026-01-08 04:44
