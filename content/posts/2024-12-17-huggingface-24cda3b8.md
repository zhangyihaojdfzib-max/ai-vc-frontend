---
title: GCP第五代至强CPU上语言模型性能基准测试
title_original: Benchmarking Language Model Performance on 5th Gen Xeon at GCP
date: '2024-12-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/intel-gcp-c4
author: ''
summary: 本文在Google Cloud的N2（第三代至强）和C4（第五代至强）实例上，对文本嵌入和文本生成两种AI Agent工作负载进行基准测试。结果显示，C4在文本嵌入吞吐量上比N2高出10-24倍，文本生成高出2.3-3.6倍；考虑价格后，C4在TCO上仍保持7-19倍（嵌入）和1.7-2.9倍（生成）优势。研究表明，在CPU上部署轻量级Agent
  AI解决方案可行，主要得益于第五代至强集成的AMX加速器。
categories:
- AI基础设施
tags:
- 第五代至强
- CPU推理
- Agent AI
- Google Cloud
- 基准测试
draft: false
translated_at: '2026-06-04T06:34:31.200030'
---

# 在 GCP 的第五代至强处理器上对语言模型性能进行基准测试

摘要：我们在两个基于至强处理器的 Google Cloud Compute Engine CPU 实例（即 N2 和 C4）上，对两种具有代表性的 Agent（智能体）AI 工作负载组件（文本嵌入和文本生成）进行了基准测试。结果一致显示，在文本嵌入方面，C4 的吞吐量比 N2 高出 10 倍到 24 倍；在文本生成方面，C4 的吞吐量比 N2 高出 2.3 倍到 3.6 倍。考虑价格因素，C4 的每小时价格约为 N2 的 1.3 倍，从这个意义上说，在文本嵌入方面，C4 相比 N2 保持了 7 倍到 19 倍的 TCO（总拥有成本）优势；在文本生成方面，则保持了 1.7 倍到 2.9 倍的 TCO 优势。结果表明，完全在 CPU 上部署轻量级 Agent（智能体）AI 解决方案是可行的。

## 引言

人们相信人工智能的下一个前沿领域在于 Agent（智能体）AI。这种新范式使用“感知 - 推理 - 行动”流程，将 LLM（大语言模型）复杂的推理和迭代规划能力与强大的上下文理解增强能力相结合。上下文理解能力由向量数据库和传感器输入等工具提供，以创建更具上下文感知能力的 AI 系统，这些系统能够自主解决复杂的多步骤问题。此外，LLM（大语言模型）的函数调用能力使得 AI Agent（智能体）能够直接采取行动，远远超越了聊天机器人所能提供的对话功能。Agent（智能体）AI 为提高各行业的生产力和运营效率带来了令人兴奋的前景。

人们正在将越来越多的工具引入 Agent（智能体）AI 系统，而这些工具目前大多运行在 CPU 上，这引发了一个担忧：在这种范式下，将产生不可忽视的主机与加速器之间的流量开销。与此同时，模型构建者和供应商正在构建更小但功能强大的小型语言模型（SLM），最新的例子是 Meta 的 1B 和 3B 参数的 llama3.2 模型，它们具备先进的 multilingual（多语言）文本生成和工具调用能力。此外，CPU 也在不断发展，开始提供更强的 AI 支持，英特尔在其第四代至强处理器中引入了英特尔高级矩阵扩展（AMX），这是一种新的 AI 张量加速器。将这三条线索结合起来，探讨 CPU 承载整个 Agent（智能体）AI 系统的潜力将非常有趣，尤其是在使用 SLM 时。

在本文中，我们将对 Agent（智能体）AI 的两个代表性组件（文本嵌入和文本生成）进行基准测试，并比较 CPU 在这两个组件上的代际性能提升。我们选择了 Google Cloud Compute Engine 的 C4 实例和 N2 实例进行比较。其逻辑在于：C4 由第五代英特尔至强处理器（代号 Emerald Rapids）驱动，这是 Google Cloud 上可用的最新一代至强 CPU，集成了英特尔 AMX 以提升 AI 性能；而 N2 由第三代英特尔至强处理器（代号 Ice Lake）驱动，这是 Google Cloud 上的上一代至强 CPU，仅支持 AVX-512，没有 AMX。我们将展示 AMX 的优势。

我们将使用 Hugging Face 的统一基准测试库 `optimum-benchmark`（支持多后端和多设备）来测量性能。基准测试在 `optimum-intel` 后端上运行。`optimum-intel` 是一个 Hugging Face 加速库，用于在英特尔架构（CPU、GPU）上加速端到端流程。我们的基准测试案例如下：

- 对于文本嵌入，我们使用 `WhereIsAI/UAE-Large-V1` 模型，输入序列长度为 128，并将 batch size 从 1 扫描到 128。
- 对于文本生成，我们使用 `meta-llama/Llama-3.2-3` 模型，输入序列长度为 256，输出序列长度为 32，并将 batch size 从 1 扫描到 64。

## 创建实例

访问 Google Cloud Console，并在您的项目下点击“创建虚拟机”。然后，按照以下步骤创建一个 96 vCPU 的实例，该实例对应一个英特尔 Ice Lake CPU 插槽。

1. 在“机器配置”选项卡中选择 N2，并将“机器类型”指定为 `n2-standard-96`。然后您需要按下图设置“CPU 平台”：
2. 按下图配置“操作系统和存储”选项卡：
3. 其他配置保持默认
4. 点击“创建”按钮

现在，您拥有了一个 N2 实例。

按照以下步骤创建一个 96 vCPU 的实例，该实例对应一个英特尔 Emerald Rapids 插槽。请注意，在本文中，我们在 C4 和 N2 之间使用相同的 CPU 核心数，以确保进行等核心数的基准测试。

1. 在“机器配置”选项卡中选择 C4，并将“机器类型”指定为 `c4-standard-96`。您还可以设置“CPU 平台”并开启全核睿频以使性能更稳定：
2. 像 N2 一样配置“操作系统和存储”
3. 其他配置保持默认
4. 点击“创建”按钮

现在，您拥有了一个 C4 实例。

## 设置环境

按照以下步骤轻松设置环境。为了可复现性，我们在命令中列出了所使用的版本和提交。

1. SSH 连接到实例
2. `$ git clone https://github.com/huggingface/optimum-benchmark.git`
3. `$ cd ./optimum-benchmark`
4. `$ git checkout d58bb2582b872c25ab476fece19d4fa78e190673`
5. `$ cd ./docker/cpu`
6. `$ sudo docker build . -t <your_docker_image_tag>`
7. `$ sudo docker run -it --rm --privileged -v /home/<your_home_folder>:/workspace <your_docker_image_tag> /bin/bash`

我们现在在容器中，执行以下步骤：

1. `$ pip install "optimum-intel[ipex]"@git+https://github.com/huggingface/optimum-intel.git@6a3b1ba5924b0b017b0b0f5de5b10adb77095b`
2. `$ pip install torch==2.3.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`
3. `$ python -m pip install intel-extension-for-pytorch==2.3.10`
4. `$ cd /workspace/optimum-benchmark`
5. `$ pip install .[ipex]`
6. `$ export OMP_NUM_THREADS=48`
7. `$ export KMP_AFFINITY=granularity=fine,compact,1,0`
8. `$ export KMP_BLOCKTIME=1`
9. `$ pip install huggingface-hub`
10. `$ huggingface-cli login`，然后输入您的 Hugging Face Token 以访问 llama 模型

## 基准测试

### 文本嵌入

您需要按如下方式更新 `optimum-benchmark` 目录中的 `examples/ipex_bert.yaml`，以对 `WhereIsAI/UAE-Large-V1` 进行基准测试。我们将 numa 绑定更改为 `0,1`，因为 N2 和 C4 每个插槽都有 2 个 NUMA 域，您可以使用 `lscpu` 进行双重确认。

```
--- a/examples/ipex_bert.yaml
+++ b/examples/ipex_bert.yaml
@@ -11,8 +11,8 @@ name: ipex_bert
 launcher:
   numactl: true
   numactl_kwargs:
-    cpunodebind: 0
-    membind: 0
+    cpunodebind: 0,1
+    membind: 0,1
 
 scenario:
   latency: true
@@ -26,4 +26,4 @@ backend:
   no_weights: false
   export: true
   torch_dtype: bfloat16
-  model: bert-base-uncased
+  model: WhereIsAI/UAE-Large-V1

```

然后，运行基准测试：`$ optimum-benchmark --config-dir examples/ --config-name ipex_bert`

### 文本生成

您可以按如下方式更新 `examples/ipex_llama.yaml`，以对 `meta-llama/Llama-3.2-3` 进行基准测试。

```
--- a/examples/ipex_llama.yaml
+++ b/examples/ipex_llama.yaml
@@ -11,8 +11,8 @@ name: ipex_llama
 launcher:
   numactl: true
   numactl_kwargs:
-    cpunodebind: 0
-    membind: 0
+    cpunodebind: 0,1
+    membind: 0,1
 
 scenario:
   latency: true
@@ -34,4 +34,4 @@ backend:
   export: true
   no_weights: false
   torch_dtype: bfloat16
-  model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
+  model: meta-llama/Llama-3.2-3B

```

然后，运行基准测试：`$ optimum-benchmark --config-dir examples/ --config-name ipex_llama`

## 结果与结论

### 文本嵌入结果

在文本嵌入基准测试案例中，GCP C4 实例的吞吐量比 N2 高出约 10 倍到 24 倍。

### 文本生成结果

一致地，在文本生成基准测试中，C4 实例的吞吐量比 N2 高出约 2.3 倍到 3.6 倍。在 batch size 为 1 到 16 的范围内，吞吐量提高了 13 倍，同时没有显著影响延迟。这使得在不牺牲用户体验的情况下，能够支持并发查询服务。

### 结论

在这篇文章中，我们在 Google Cloud Compute Engine 的 CPU 实例（C4 和 N2）上对两种具有代表性的 Agent（智能体）AI 工作负载进行了基准测试。结果显示，得益于 Intel Xeon CPU 上的 AMX 和内存能力改进，性能显著提升。Intel 一个月前发布了配备 P 核（代号 Granite Rapids）的 Xeon 6 处理器，在 Llama 3 上实现了约 2 倍的性能提升。我们相信，借助新的 Granite Rapids CPU，可以探索完全在 CPU 上部署轻量级 Agent（智能体）AI 解决方案，从而避免主机与加速器之间繁重的通信开销。一旦 Google Cloud Compute Engine 提供 Granite Rapids 实例，我们将对其进行基准测试并报告结果。

感谢阅读！

---

> 本文由AI自动翻译，原文链接：[Benchmarking Language Model Performance on 5th Gen Xeon at GCP](https://huggingface.co/blog/intel-gcp-c4)
> 
> 翻译时间：2026-06-04 06:34
