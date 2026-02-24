---
title: 在Jetson边缘设备上部署开源视觉语言模型
title_original: Deploying Open Source Vision Language Models (VLM) on Jetson
date: '2026-02-24'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/cosmos-on-jetson
author: ''
summary: 本文是一篇技术教程，详细介绍了如何在NVIDIA Jetson系列边缘计算设备（包括AGX Thor、AGX Orin和Orin Super Nano）上部署开源的视觉语言模型。文章以NVIDIA
  Cosmos Reasoning 2B模型为例，逐步讲解了从安装NGC CLI、下载FP8量化模型权重、拉取适配的vLLM Docker镜像，到最终启动容器并连接实时WebUI界面的完整流程。教程旨在帮助开发者在资源受限的边缘端高效运行融合视觉与语言理解能力的AI模型，适用于机器人、物理AI等实时交互应用场景。
categories:
- AI基础设施
tags:
- 边缘计算
- Jetson
- 视觉语言模型
- 模型部署
- vLLM
draft: false
translated_at: '2026-02-24T04:35:25.186074'
---

# 在 Jetson 上部署开源视觉语言模型

视觉语言模型通过融合视觉感知与语义推理，标志着人工智能领域的一次重大飞跃。它超越了受固定标签限制的传统模型，利用联合嵌入空间，通过自然语言来解读和讨论复杂的、开放式的环境。

推理准确性和效率的快速演进，使得这些模型成为边缘设备的理想选择。NVIDIA Jetson 系列产品，从高性能的 AGX Thor 和 AGX Orin 到紧凑的 Orin Super Nano，专为驱动物理人工智能和机器人技术的加速应用而设计，为领先的开源模型提供了必要的优化运行时环境。

在本教程中，我们将演示如何使用 vLLM 框架，在 Jetson 系列产品上部署 NVIDIA Cosmos Reasoning 2B 模型。我们还将指导您将此模型连接到 Live VLM WebUI，从而启用一个基于网络摄像头的实时界面，用于交互式物理人工智能。

## 前提条件

支持的设备：
- Jetson AGX Thor 开发者套件
- Jetson AGX Orin
- Jetson Orin Super Nano

JetPack 版本：
- JetPack 6 — 适用于 Orin 设备
- JetPack 7 — 适用于 Thor 设备

存储：需要 NVMe SSD
- 约 5 GB 用于 FP8 模型权重
- 约 8 GB 用于 vLLM 容器镜像

账户：
- 创建 NVIDIA NGC 账户以下载模型和 vLLM 容器

## 概述

所有设备的工作流程相同：
1. 通过 NGC CLI 下载 FP8 模型检查点
2. 为您的设备拉取 vLLM Docker 镜像
3. 将模型作为卷挂载并启动容器
4. 将 Live VLM WebUI 连接到 vLLM 端点

## 步骤 1：安装 NGC CLI

NGC CLI 允许您从 NVIDIA NGC 目录下载模型检查点。

### 下载并安装

```
mkdir -p ~/Projects/CosmosReasoning
cd ~/Projects/CosmosReasoning

# Download the NGC CLI for ARM64
# Get the latest installer URL from: https://org.ngc.nvidia.com/setup/installers/cli
wget -O ngccli_arm64.zip https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/4.13.0/files/ngccli_arm64.zip
unzip ngccli_arm64.zip
chmod u+x ngc-cli/ngc

# Add to PATH
export PATH="$PATH:$(pwd)/ngc-cli"

```

### 配置 CLI

```
ngc config set

```

系统将提示您输入：
- API 密钥 — 在 NGC API 密钥设置页面生成
- CLI 输出格式 — 选择 json 或 ascii
- org — 按 Enter 键接受默认值

## 步骤 2：下载模型

下载 FP8 量化检查点。这适用于所有 Jetson 设备：

```
cd ~/Projects/CosmosReasoning
ngc registry model download-version "nim/nvidia/cosmos-reason2-2b:1208-fp8-static-kv8"

```

这将创建一个名为 `cosmos-reason2-2b_v1208-fp8-static-kv8/` 的目录，其中包含模型权重。请记下完整路径 — 您将把它作为卷挂载到 Docker 容器中。

## 步骤 3：拉取 vLLM Docker 镜像

### 对于 Jetson AGX Thor

```
docker pull nvcr.io/nvidia/vllm:26.01-py3

```

### 对于 Jetson AGX Orin / Orin Super Nano

```
docker pull ghcr.io/nvidia-ai-iot/vllm:r36.4-tegra-aarch64-cu126-22.04

```

## 步骤 4：使用 vLLM 服务 Cosmos Reasoning 2B 模型

### 选项 A：Jetson AGX Thor

Thor 拥有充足的 GPU 内存，可以运行具有较大上下文长度的模型。

设置下载模型的路径并释放主机上的缓存内存：

```
MODEL_PATH="$HOME/Projects/CosmosReasoning/cosmos-reason2-2b_v1208-fp8-static-kv8"
sudo sysctl -w vm.drop_caches=3

```

挂载模型并启动容器：

```
docker run --rm -it \
  --runtime nvidia \
  --network host \
  --ipc host \
  -v "$MODEL_PATH:/models/cosmos-reason2-2b:ro" \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  nvcr.io/nvidia/vllm:26.01-py3 \
  bash

```

在容器内部，激活环境并启动模型服务：

```
vllm serve /models/cosmos-reason2-2b \
  --max-model-len 8192 \
  --media-io-kwargs '{"video": {"num_frames": -1}}' \
  --reasoning-parser qwen3 \
  --gpu-memory-utilization 0.8

```

注意：`--reasoning-parser qwen3` 标志启用思维链推理提取。`--media-io-kwargs` 标志配置视频帧处理。

等待直到看到：

```
INFO:     Uvicorn running on http://0.0.0.0:8000

```

### 选项 B：Jetson AGX Orin

AGX Orin 有足够的内存，可以使用与 Thor 相同的宽松参数运行模型。

```
MODEL_PATH="$HOME/Projects/CosmosReasoning/cosmos-reason2-2b_v1208-fp8-static-kv8"
sudo sysctl -w vm.drop_caches=3

```

1. 启动容器：

```
docker run --rm -it \
  --runtime nvidia \
  --network host \
  -v "$MODEL_PATH:/models/cosmos-reason2-2b:ro" \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  ghcr.io/nvidia-ai-iot/vllm:r36.4-tegra-aarch64-cu126-22.04 \
  bash

```

2. 在容器内部，激活环境并启动服务：

```
cd /opt/
source venv/bin/activate

vllm serve /models/cosmos-reason2-2b \
  --max-model-len 8192 \
  --media-io-kwargs '{"video": {"num_frames": -1}}' \
  --reasoning-parser qwen3 \
  --gpu-memory-utilization 0.8

```

```
INFO:     Uvicorn running on http://0.0.0.0:8000

```

### 选项 C：Jetson Orin Super Nano

Orin Super Nano 的 RAM 显著减少，因此我们需要使用激进的内存优化标志。

```
MODEL_PATH="$HOME/Projects/CosmosReasoning/cosmos-reason2-2b_v1208-fp8-static-kv8"
sudo sysctl -w vm.drop_caches=3

```

```
docker run --rm -it \
  --runtime nvidia \
  --network host \
  -v "$MODEL_PATH:/models/cosmos-reason2-2b:ro" \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  ghcr.io/nvidia-ai-iot/vllm:r36.4-tegra-aarch64-cu126-22.04 \
  bash

```

```
cd /opt/
source venv/bin/activate

vllm serve /models/cosmos-reason2-2b \
  --host 0.0.0.0 \
  --port 8000 \
  --trust-remote-code \
  --enforce-eager \
  --max-model-len 256 \
  --max-num-batched-tokens 256 \
  --gpu-memory-utilization 0.65 \
  --max-num-seqs 1 \
  --enable-chunked-prefill \
  --limit-mm-per-prompt '{"image":1,"video":1}' \
  --mm-processor-kwargs '{"num_frames":2,"max_pixels":150528}'

```

关键标志说明：

等待直到看到服务器准备就绪：

```
INFO:     Uvicorn running on http://0.0.0.0:8000

```

### 验证服务器正在运行

在 Jetson 的另一个终端中：

```
curl http://localhost:8000/v1/models

```

您应该在响应中看到列出的模型。

## 步骤 5：通过快速 API 调用进行测试

在连接 WebUI 之前，验证模型是否正确响应：

```
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models/cosmos-reason2-2b",
    "messages": [
      {
        "role": "user",
        "content": "What capabilities do you have?"
      }
    ],
    "max_tokens": 128
  }' | python3 -m json.tool

```

提示：API 请求中使用的模型名称必须与 vLLM 报告的名称匹配。使用 `curl http://localhost:8000/v1/models` 进行验证。

## 步骤 6：连接到 Live VLM WebUI

Live VLM WebUI 提供了一个实时的网络摄像头到 VLM 的界面。通过 vLLM 服务 Cosmos Reasoning 2B 模型，您可以流式传输网络摄像头画面，并获得带有推理的实时 AI 分析。

### 安装 Live VLM WebUI

最简单的方法是使用 pip：

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
cd ~/Projects/CosmosReasoning
uv venv .live-vlm --python 3.12
source .live-vlm/bin/activate
uv pip install live-vlm-webui
live-vlm-webui

```

或者使用 Docker：

```
git clone https://github.com/nvidia-ai-iot/live-vlm-webui.git
cd live-vlm-webui
./scripts/start_container.sh

```

### 配置 WebUI

1. 在浏览器中打开 `https://localhost:8090`
2. 接受自签名证书
3. 在左侧边栏的 VLM API 配置部分：
    - 将 API 基础 URL 设置为 `http://localhost:8000/v1`
    - 点击刷新按钮以检测模型
    - 从下拉菜单中选择 Cosmos Reasoning 2B 模型
4. 选择您的摄像头并点击开始

- 将API基础URL设置为http://localhost:8000/v1
- 点击刷新按钮以检测模型
- 从下拉菜单中选择Cosmos Reasoning 2B模型

WebUI现在会将您的网络摄像头帧流式传输到Cosmos Reasoning 2B，并实时显示模型的分析结果。

### 适用于Orin的推荐WebUI设置

由于Orin运行的上下文长度较短，请在WebUI中调整以下设置：

- 最大Token数：设置为100–150（较短的响应完成得更快）
- 帧处理间隔：设置为60+（为模型提供帧之间的处理时间）

## 故障排除

### Orin上内存不足

问题：vLLM因CUDA内存不足错误而崩溃。

解决方案：

1.  启动前释放系统内存：`sudo sysctl -w vm.drop_caches=3`
2.  降低`--gpu-memory-utilization`（尝试0.55或0.50）
3.  进一步减少`--max-model-len`（尝试128）
4.  确保没有其他GPU密集型进程正在运行

启动前释放系统内存：

```
sudo sysctl -w vm.drop_caches=3

```

降低`--gpu-memory-utilization`（尝试0.55或0.50）

进一步减少`--max-model-len`（尝试128）

确保没有其他GPU密集型进程正在运行

### WebUI中找不到模型

问题：模型未出现在Live VLM WebUI的下拉列表中。

1.  验证vLLM是否正在运行：`curl http://localhost:8000/v1/models`
2.  确保WebUI API基础URL设置为`http://localhost:8000/v1`（而非`https`）
3.  如果vLLM和WebUI位于不同的容器中，请使用`http://<jetson-ip>:8000/v1`代替`localhost`

### Orin上推理速度慢

问题：每个响应需要很长时间。

- 这在内存受限的配置中是预期情况。Orin上的Cosmos Reasoning 2B FP8优先考虑适配内存，而非速度
- 减少WebUI中的`max_tokens`以获得更短、更快的响应
- 增加帧间隔，使模型不会持续处理新帧

### vLLM无法加载模型

问题：vLLM报告模型路径不存在或无法加载。

- 验证NGC下载是否成功完成：`ls ~/Projects/CosmosReasoning/cosmos-reason2-2b_v1208-fp8-static-kv8/`
- 确保您的`docker run`命令中的卷挂载路径正确
- 检查模型目录是否以只读方式挂载（`:ro`），并且容器内的路径与您传递给`vllm serve`的路径匹配

## 总结

在本教程中，我们展示了如何使用vLLM在Jetson系列设备上部署NVIDIA Cosmos Reasoning 2B模型。

Cosmos Reasoning 2B的思维链能力与Live VLM WebUI的实时流式传输相结合，使其成为在边缘原型设计和评估视觉AI应用的理想选择。

## 其他资源

- NVIDIA Build上的Cosmos Reasoning 2B：https://build.nvidia.com/nvidia/cosmos-reason2-2b
- NGC模型目录：https://catalog.ngc.nvidia.com/
- Live VLM WebUI：https://github.com/NVIDIA-AI-IOT/live-vlm-webui
- 适用于Jetson Thor的vLLM容器：https://ghcr.io/nvidia-ai-iot/vllm:r36.4-tegra-aarch64-cu126-22.04
- 适用于Jetson AGX Orin和Orin Super Nano的vLLM容器：https://nvcr.io/nvidia/vllm:26.01-py3
- NGC CLI安装程序：https://org.ngc.nvidia.com/setup/installers/cli
- Jetson支持的开放模型：https://www.jetson-ai-lab.com/models/
- Jetson入门指南：https://www.jetson-ai-lab.com/tutorials/

---

> 本文由AI自动翻译，原文链接：[Deploying Open Source Vision Language Models (VLM) on Jetson](https://huggingface.co/blog/nvidia/cosmos-on-jetson)
> 
> 翻译时间：2026-02-24 04:35
