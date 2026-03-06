---
title: NVIDIA NIM 微服务加速 Hugging Face 上十万大模型部署
title_original: Accelerate a World of LLMs on Hugging Face with NVIDIA NIM
date: '2025-07-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/multi-llm-nim
author: ''
summary: 本文介绍了 NVIDIA 推出的 NIM 推理微服务如何简化在 Hugging Face 平台上超过 10 万个大型语言模型的部署流程。NIM 通过单一
  Docker 容器整合了 TensorRT-LLM、vLLM 等主流推理框架，支持多种模型权重格式，并自动进行性能优化，无需手动配置。文章详细说明了环境设置步骤，并提供了从
  Hugging Face 部署 Codestral-22B 等模型的具体操作示例，旨在帮助开发者快速、可靠地将多样化的 LLM 投入实际应用。
categories:
- AI基础设施
tags:
- NVIDIA NIM
- 大语言模型
- 模型部署
- Hugging Face
- 推理加速
draft: false
translated_at: '2026-03-06T04:35:20.552573'
---

# 借助 NVIDIA NIM 在 Hugging Face 上加速 LLM 世界的发展

AI 开发者希望选择最新的大语言模型架构和专用变体，以用于 AI Agent 及其他应用程序，但处理所有这些多样性可能会拖慢测试和部署流程。特别是，管理和优化不同的推理软件框架，以在各种 LLM 和服务要求下实现最佳性能，是将高性能 AI 应用交付到最终用户手中的一个耗时瓶颈。

NVIDIA AI 客户和生态系统合作伙伴利用 NVIDIA NIM 推理微服务，在 NVIDIA 加速基础设施上简化最新 AI 模型的部署，这些模型包括来自 NVIDIA、Meta、Mistral AI、Google 以及数百家其他创新模型构建者的 LLM、多模态和特定领域模型。我们已经看到客户和合作伙伴通过简化、可靠的模型部署方法，更快地交付了更多创新。今天，我们很高兴地宣布，通过 NIM 解锁 Hugging Face 上超过 100,000 个 LLM，以实现快速、可靠的部署。

## 用于部署广泛 LLM 的单一 NIM 微服务

NIM 现在提供一个单一的 Docker 容器，用于部署由 NVIDIA 和社区领先的推理框架支持的广泛 LLM，这些框架包括 NVIDIA TensorRT-LLM、vLLM 和 SGLang。当向 NIM 容器提供 LLM 时，它会执行几个步骤进行部署和性能优化，无需手动配置：

表 1. NVIDIA NIM LLM 适配阶段和功能

单一的 NIM 容器支持常见的 LLM 权重格式，包括：

- Hugging Face Transformers 检查点：可以直接从 Hugging Face 仓库部署带有 `.safetensors` 文件的 LLM，无需复杂的转换。
- GGUF 检查点：支持模型架构的量化 GGUF 检查点可以直接从 HuggingFace 或本地下载的文件部署。
- TensorRT-LLM 检查点：可以部署打包在 `trtllm_ckpt` 目录中、针对 TensorRT-LLM 优化的模型。
- TensorRT-LLM 引擎：可以使用来自 `trtllm_engine` 目录的预构建 TensorRT-LLM 引擎，在 NVIDIA GPU 上实现峰值性能。

## 开始使用

要使用 NIM，请确保您的环境具备带有适当驱动程序的 NVIDIA GPU（CUDA 12.1+）、已安装 Docker、用于 NIM Docker 镜像的 NVIDIA NGC 账户和 API 密钥，以及用于需要身份验证的模型的 Hugging Face 账户和 API 令牌。在 NIM 文档中了解更多关于环境先决条件的信息。

环境设置涉及设置环境变量和创建持久缓存目录。确保 `nim_cache` 目录具有正确的 Unix 权限，最好由启动 Docker 容器的同一 Unix 用户拥有，以防止权限问题。命令使用 `-u $(id -u)` 来管理这一点。

为方便起见，让我们将一些常用信息存储在环境变量中。

```bash

NIM_IMAGE=llm-nim

HF_TOKEN=<your_huggingface_token>

```

### 示例 1：部署模型

以 Codestral-22B 为例，演示如何从 Hugging Face 部署 LLM：

```bash
docker run --rm --gpus all \
  --shm-size=16GB \
  --network=host \
  -u $(id -u) \
  -v $(pwd)/nim_cache:/opt/nim/.cache \
  -v $(pwd):$(pwd) \
  -e HF_TOKEN=$HF_TOKEN \
  -e NIM_TENSOR_PARALLEL_SIZE=1 \
  -e NIM_MODEL_NAME="hf://mistralai/Codestral-22B-v0.1" \
  $NIM_IMAGE

```

对于本地下载的模型，将 `NIM_MODEL_NAME` 指向路径并挂载目录：

```bash
docker run --rm --gpus all \
  --shm-size=16GB \
  --network=host \
  -u $(id -u) \
  -v $(pwd)/nim_cache:/opt/nim/.cache \
  -v $(pwd):$(pwd) \
  -v /path/to/model/dir:/path/to/model/dir \
  -e HF_TOKEN=$HF_TOKEN \
  -e NIM_TENSOR_PARALLEL_SIZE=1 \
  -e NIM_MODEL_NAME="/path/to/model/dir/mistralai-Codestral-22B-v0.1" \
  $NIM_IMAGE

```

部署模型时，可以随时检查输出日志，以了解 NIM 在模型部署过程中所做的选择。部署的模型可通过 `http://localhost:8000` 访问，API 端点在 `http://localhost:8000/docs`。

底层引擎提供了额外的参数。您可以通过在容器中运行 `nim-run --help` 来检查此类参数的完整列表，如下所示。

```bash
docker run --rm --gpus all \
  --network=host \
  -u $(id -u) \
  $NIM_IMAGE nim-run --help

```

### 示例 2：指定后端

要检查兼容的后端或选择特定的后端，请使用 `list-model-profiles`：

```bash
docker run --rm --gpus all \
  --shm-size=16GB \
  --network=host \
  -u $(id -u) \
  -v $(pwd)/nim_cache:/opt/nim/.cache \
  -v $(pwd):$(pwd) \
  -e HF_TOKEN=$HF_TOKEN \
  $NIM_IMAGE list-model-profiles --model "hf://meta-llama/Llama-3.1-8B-Instruct"

```

此命令显示兼容的配置文件，包括用于 LoRA 适配器的配置文件。要使用特定后端（如 vLLM）进行部署，请使用 `NIM_MODEL_PROFILE` 环境变量，并使用 `list-model-profiles` 提供的输出：

```bash
docker run --rm --gpus all \
  --shm-size=16GB \
  --network=host \
  -u $(id -u) \
  -v $(pwd)/nim_cache:/opt/nim/.cache \
  -v $(pwd):$(pwd) \
  -e HF_TOKEN=$HF_TOKEN \
  -e NIM_TENSOR_PARALLEL_SIZE=1 \
  -e NIM_MODEL_NAME="hf://meta-llama/Llama-3.1-8B-Instruct" \
  -e NIM_MODEL_PROFILE="e2f00b2cbfb168f907c8d6d4d40406f7261111fbab8b3417a485dcd19d10cc98" \
  $NIM_IMAGE

```

### 示例 3：量化模型部署

NIM 便于部署量化模型。它会自动检测量化格式（例如，GGUF、AWQ），并使用标准部署命令选择适当的后端：

```bash




docker run --rm --gpus all \
  --shm-size=16GB \
  --network=host \
  -u $(id -u) \
  -v $(pwd)/nim_cache:/opt/nim/.cache \
  -v $(pwd):$(pwd) \
  -e HF_TOKEN=$HF_TOKEN \
  -e NIM_TENSOR_PARALLEL_SIZE=1 \
  -e NIM_MODEL_NAME=$MODEL \
  $NIM_IMAGE

```

对于高级用户，NIM 通过环境变量提供自定义功能，例如用于上下文长度的 `NIM_MAX_MODEL_LEN`。对于大型 LLM，`NIM_TENSOR_PARALLEL_SIZE` 支持多 GPU 部署。确保将 `--shm-size=<shared memory size>` 传递给 Docker 以进行多 GPU 通信。

NIM 容器支持 NVIDIA TensorRT-LLM、vLLM 和 SGLang 支持的广泛 LLM，包括 Hugging Face 上的流行 LLM 和专用变体。有关支持的 LLM 的更多详细信息，请参阅文档。

## 与 Hugging Face 和 NVIDIA 共同构建

NIM 旨在简化 NVIDIA 加速基础设施上的 AI 模型部署，为高性能 AI 开发者和企业 AI 团队加速创新和价值实现时间。我们期待与 Hugging Face 社区的互动和反馈。

在 NVIDIA 托管的计算环境中，通过开发者示例开始使用，请访问 build.nvidia.com。

---

> 本文由AI自动翻译，原文链接：[Accelerate a World of LLMs on Hugging Face with NVIDIA NIM](https://huggingface.co/blog/nvidia/multi-llm-nim)
> 
> 翻译时间：2026-03-06 04:35
