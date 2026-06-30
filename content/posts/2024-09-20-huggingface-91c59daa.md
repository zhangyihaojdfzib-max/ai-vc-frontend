---
title: Optimum-Intel与OpenVINO GenAI模型优化部署指南
title_original: Optimize and deploy with Optimum-Intel and OpenVINO GenAI
date: '2024-09-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/deploy-with-openvino
author: ''
summary: 本文介绍了如何使用Optimum-Intel和OpenVINO GenAI在边缘端或客户端优化和部署Hugging Face Transformer模型。文章从环境设置开始，详细说明了将模型导出为OpenVINO
  IR格式的两种方法（Python API和CLI），并强调了模型优化的重要性，特别是仅权重量化技术（如INT8和INT4）。通过结合AWQ、量化尺度估计等方法，可在资源受限设备上实现低延迟、小占用空间的高效AI推理，最小化依赖并提升性能。
categories:
- AI基础设施
tags:
- OpenVINO
- 模型优化
- 边缘部署
- Transformer
- 量化
draft: false
translated_at: '2026-06-30T06:13:47.724297'
---

# 使用 Optimum-Intel 和 OpenVINO GenAI 优化与部署模型

在边缘端或客户端部署 Transformer 模型需要仔细考虑性能和兼容性。Python 虽然功能强大，但在以 C++ 为主的环境中并非总是理想的部署选择。本博客将指导您使用 Optimum-Intel 和 OpenVINO™ GenAI 优化和部署 Hugging Face Transformer 模型，以最小依赖实现高效的 AI 推理。

1. 为何在边缘部署中使用 OpenVINO™
2. 第一步：环境设置
3. 第二步：将模型导出为 OpenVINO IR
4. 第三步：模型优化
5. 第四步：使用 OpenVINO GenAI API 部署
6. 结论

## 为何在边缘部署中使用 OpenVINO™

OpenVINO™ 最初作为 C++ AI 推理解决方案开发，使其成为最小化依赖至关重要的边缘和客户端部署的理想选择。随着 GenAI API 的引入，将大语言模型（LLM）集成到 C++ 或 Python 应用程序变得更加直接，其功能旨在简化部署并提升性能。

## 第一步：环境设置

## 前置条件

首先，确保您的环境已正确配置 Python 和 C++。安装必要的 Python 包：

```sh
pip install --upgrade --upgrade-strategy eager "optimum[openvino]"

```

以下是本博客中使用的具体包：

```
transformers==4.44
openvino==24.3
openvino-tokenizers==24.3
optimum-intel==1.20
lm-eval==0.4.3

```

关于 GenAI C++ 库的安装，请按照此处的说明操作。

## 第二步：将模型导出为 OpenVINO IR

Hugging Face 与 Intel 的合作催生了 Optimum-Intel 项目。该项目旨在优化 Transformer 模型以在 Intel 硬件上进行推理。Optimum-Intel 支持 OpenVINO 作为推理后端，其 API 包含基于 OpenVINO 推理 API 构建的各种模型架构的封装器。所有这些封装器都以 OV 前缀开头，例如 OVModelForCausalLM。除此之外，其 API 与 🤗 Transformers 库的 API 类似。

要将 Transformer 模型导出为 OpenVINO 中间表示（IR），可以使用两种方式：通过 Python 的 `.from_pretrained()` 方法，或通过 Optimum 命令行界面（CLI）。以下是两种方法的示例：

### 使用 Python API

```python
from optimum.intel import OVModelForCausalLM

model_id = "meta-llama/Meta-Llama-3.1-8B"
model = OVModelForCausalLM.from_pretrained(model_id, export=True)
model.save_pretrained("./llama-3.1-8b-ov")

```

### 使用命令行界面（CLI）

```sh
optimum-cli export openvino -m meta-llama/Meta-Llama-3.1-8B ./llama-3.1-8b-ov

```

`./llama-3.1-8b-ov` 文件夹将包含 `.xml` 和 `.bin` IR 模型文件以及来自源模型的必要配置文件。🤗 tokenizer 也将转换为 `openvino-tokenizers` 库的格式，相应的配置文件将在同一文件夹中创建。

## 第三步：模型优化

在资源受限的边缘和客户端设备上运行 LLM 时，强烈建议进行模型优化。仅权重量化是一种主流方法，可显著降低延迟和模型占用空间。Optimum-Intel 通过神经网络压缩框架（NNCF）提供仅权重量化，该框架具有专为 LLM 设计的多种优化技术：从无数据的 INT8 和 INT4 权重量化到数据感知方法，如 AWQ、GPTQ、量化尺度估计、混合精度量化。
默认情况下，参数超过十亿的模型权重会被量化为 INT8 精度，这在准确性方面是安全的。这意味着上述导出步骤会产生具有 8 位权重的模型。然而，4 位整数仅权重量化可以实现更好的准确性-性能权衡。

对于 `meta-llama/Meta-Llama-3.1-8B` 模型，我们建议结合使用 AWQ、量化尺度估计以及使用反映部署用例的校准数据集进行混合精度 INT4/INT8 权重量化。与导出情况类似，有两种方式可以对 LLM 模型应用 4 位仅权重量化：

- 在 `.from_pretrained()` 方法中指定 `quantization_config` 参数。在这种情况下，应创建 `OVWeightQuantizationConfig` 对象并将其设置为此参数，如下所示：

```python
from optimum.intel import OVModelForCausalLM, OVWeightQuantizationConfig

MODEL_ID = "meta-llama/Meta-Llama-3.1-8B"
quantization_config = OVWeightQuantizationConfig(bits=4, awq=True, scale_estimation=True, group_size=64, dataset="c4")
model = OVModelForCausalLM.from_pretrained(MODEL_ID, export=True, quantization_config=quantization_config)
model.save_pretrained("./llama-3.1-8b-ov")

```

### 使用命令行界面（CLI）：

```sh
optimum-cli export openvino -m meta-llama/Meta-Llama-3.1-8B --weight-format int4 --awq --scale-estimation --group-size 64 --dataset wikitext2 ./llama-3.1-8b-ov

```

注意：模型优化过程可能需要时间，因为它会依次应用多种方法，并在指定数据集上使用模型推理。

使用 API 进行模型优化更加灵活，因为它允许使用自定义数据集，这些数据集可以作为可迭代对象传递，例如 🤗 库的 `Dataset` 对象实例或字符串列表。

权重量化通常会导致准确性指标有所下降。为了比较优化后的模型和源模型，我们报告在 Wikitext 数据集上使用 `lm-evaluation-harness` 项目测量的每词困惑度指标，该项目原生支持 🤗 Transformers 和 Optimum-Intel 模型。

## 第四步：使用 OpenVINO GenAI API 部署

转换和优化后，使用 OpenVINO GenAI 部署模型非常简单。OpenVINO GenAI 中的 LLMPipeline 类提供 Python 和 C++ API，支持多种文本生成方法且依赖最小。

### Python API 示例

```python
import argparse
import openvino_genai

device = "CPU"  
pipe = openvino_genai.LLMPipeline(args.model_dir, device)
config = openvino_genai.GenerationConfig()
config.max_new_tokens = 100
print(pipe.generate(args.prompt, config))

```

要运行此示例，您需要在 Python 环境中安装最少的依赖，因为 OpenVINO GenAI 旨在提供轻量级部署。您可以将 OpenVINO GenAI 包安装到相同的 Python 环境中，或创建一个单独的环境以比较应用程序占用空间：

```sh
pip install openvino-genai==24.3

```

### C++ API 示例

让我们看看如何使用 OpenVINO GenAI C++ API 运行相同的流水线。GenAI API 设计直观，并提供从 🤗 Transformers API 的无缝迁移。

注意：在下面的示例中，可以为 "device" 变量指定环境中任何其他可用的设备。例如，如果您使用的是带有集成显卡的 Intel CPU，"GPU" 是一个值得尝试的选项。要检查可用设备，您可以使用 `ov::Core::get_available_devices` 方法（请参阅 query-device-properties）。

```cpp
#include "openvino/genai/llm_pipeline.hpp"
#include <iostream>

int main(int argc, char* argv[]) {
   std::string model_path = "./llama-3.1-8b-ov";
   std::string device = "CPU"  
   ov::genai::LLMPipeline pipe(model_path, device);
   std::cout << pipe.generate("What is LLM model?", ov::genai::max_new_tokens(256));
}

```

### 自定义生成配置

LLMPipeline 还允许通过 `ov::genai::GenerationConfig` 指定自定义生成选项：

```cpp
ov::genai::GenerationConfig config;
config.max_new_tokens = 256;
std::string result = pipe.generate(prompt, config);

```

通过LLMPipeline，用户不仅可以轻松利用束搜索等多种解码算法，还能像以下示例那样使用Streamer构建交互式聊天场景。此外，借助LLMPipeline增强的内部优化功能，用户可以通过聊天方法start_chat()和finish_chat()（参考using-genai-in-chat-scenario）利用先前聊天历史的KV缓存来减少提示词处理时间。

```cpp
ov::genai::GenerationConfig config;
config.max_new_tokens = 100;
config.do_sample = true;
config.top_p = 0.9;
config.top_k = 30;

auto streamer = [](std::string subword) {
    std::cout << subword << std::flush;
    return false;
};

pipe.generate(prompt, config, streamer);
```

最后，让我们看看如何在聊天场景中使用LLMPipeline：

```cpp
pipe.start_chat()
for (size_t i = 0; i < questions.size(); i++) {
   std::cout << "question:\n";
   std::getline(std::cin, prompt);

   std::cout << pipe.generate(prompt) << std::endl;
}
pipe.finish_chat();
```

## 结论

Optimum-Intel与OpenVINO™ GenAI的结合为在边缘端部署Hugging Face模型提供了强大且灵活的解决方案。通过遵循这些步骤，您可以在Python可能不理想的环境中实现优化、高性能的AI推理，确保您的应用程序在英特尔硬件上流畅运行。

## 其他资源

1. 更多详情请参阅本教程。
2. 构建上述C++示例请参考此文档。
3. OpenVINO文档
4. Jupyter Notebooks
5. Optimum文档

![OpenVINO GenAI C++聊天演示](/images/posts/dc767feee1fb.gif)

---

> 本文由AI自动翻译，原文链接：[Optimize and deploy with Optimum-Intel and OpenVINO GenAI](https://huggingface.co/blog/deploy-with-openvino)
> 
> 翻译时间：2026-06-30 06:13
