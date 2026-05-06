---
title: Open R1第四次更新：DeepSeek-V30324模型解析
title_original: 'Open R1: Update #4'
date: '2025-03-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/open-r1/update-4
author: ''
summary: 本文介绍了DeepSeek-V3的更新版本V30324，该模型采用MIT许可证，在指令遵循、代码和数学能力上显著提升。基准测试显示，MMLU-Pro、GPQA、AIME和LiveCodeBench均有大幅进步，尤其在Web开发、中文写作、函数调用等方面优化。文章推测改进源于持续预训练和优化后训练，并提供了使用Hugging
  Face推理服务及TGI部署的示例。
categories:
- AI产品
tags:
- DeepSeek-V3
- 模型更新
- 基准测试
- 开源AI
- 推理模型
draft: false
translated_at: '2026-05-06T05:28:06.790645'
---

# Open R1：第四次更新

![image/png](/images/posts/2cc34413da2c.png)

## 欢迎 DeepSeek-V30324

本周，DeepSeek 的一个新模型悄然上线 Hub。这是 DeepSeek-V3 的更新版本，即 R1 推理模型所基于的基础模型。关于这个新模型目前分享的信息不多，但我们确实知道一些情况！

## 我们目前所知

该模型与原始 DeepSeek-V3 具有相同的架构，现在也采用了 MIT 许可证，而之前的 V3 模型使用的是自定义模型许可证。本次模型发布的重点是改进指令遵循能力以及代码和数学能力。让我们来看看！

### 它有多好？

DeepSeek 团队在一系列数学和编程任务上对该模型进行了评估，我们可以看到该模型相比其他前沿模型具有强大的能力：

![image/png](/images/posts/cfec83011906.png)

显然，该模型处于顶级水平：通常与 GPT-4.5 相当，并且普遍强于 Claude-Sonnet-3.7。

总结来说，该模型在各项基准测试中都有显著提升：

- MMLU-Pro：75.9 → 81.2（+5.3）（衡量综合理解能力的好基准）
- GPQA：59.1 → 68.4（+9.3）
- AIME：39.6 → 59.4（+19.8）（数学能力的代理指标）
- LiveCodeBench：39.2 → 49.2（+10.0）（编程能力的指标）

具体来说，在模型卡片中，DeepSeek 提到了以下领域的针对性改进：

- 前端 Web 开发
  - 代码可执行性提升
  - 更美观的网页和游戏前端
- 中文写作能力
  - 风格和内容质量提升
  - 与 R1 写作风格对齐
  - 中长篇写作质量提升
- 功能增强
  - 改进的多轮交互式重写
  - 优化的翻译质量和信件写作
- 中文搜索能力
  - 增强的报告分析请求，输出更详细
- 函数调用改进
  - 函数调用准确性提升，修复了之前 V3 版本中的问题

那么问题可能来了：他们到底是怎么做到的？让我们来推测一下！

### 他们是如何做到的？

鉴于命名和架构，可以相当安全地假设新模型基于之前的 V3 模型并在其之上进行训练。他们改进模型有两个可能的方面：

- 持续预训练：从 V3 模型开始，可以继续预训练过程，使用 a）更新的、更及时的数据，以及 b）经过更好筛选从而质量更高的数据。这将提高对近期事件的事实准确性，并普遍提升能力。
- 改进的后训练：特别是在指令遵循和风格的时代，后训练起着最重要的作用。他们很可能改进了后训练数据的混合方式，甚至可能改进了算法。

在团队发布技术报告之前，我们无法确切知道他们调整了什么，但后训练流程的可能性很大，并且可能还增加了一些预训练。接下来看看如何使用这些模型吧！

## 如何使用该模型

### 推理服务提供商

您可以使用 Hugging Face 的推理服务提供商来快速体验该模型。该模型可通过 Fireworks、Hyperbolic 和 Novita 使用。

以下是使用 `huggingface_hub` 库的示例。您也可以像这个示例中那样使用 OpenAI 客户端库。

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    
)

messages = [
    {
        "role": "user",
        "content": "My first is second in line; I send shivers up your spine; not quite shining bright. I glitter in the light."
    }
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324",
    messages=messages,
    temperature=0.3,
)

print(completion.choices[0].message['content'])


```

### 文本生成推理

TGI 的最新版本也支持运行 DeepSeek V3-0324。您可以在 H100 节点上直接使用标记的 Docker 镜像运行它。

```bash
docker run --gpus all --shm-size 1g -p 8080:80 -v $ volume:/data \
    ghcr.io/huggingface/text-generation-inference:3.2.1 --model-id deepseek-ai/DeepSeek-V3-0324

```

SGLang

SGLang 支持开箱即用地运行 DeepSeek V3-0324，同时支持多头潜在注意力和数据并行优化。要使用，您只需在 H100 节点上运行以下命令即可。更多信息请点击此处查看。

```bash
docker pull lmsysorg/sglang:latest

docker run --gpus all --shm-size 32g -p 30000:30000 -v ~/.cache/huggingface:/root/.cache/huggingface --ipc=host --network=host --privileged lmsysorg/sglang:latest \
    python3 -m sglang.launch_server --model deepseek-ai/DeepSeek-V3-0324 --tp 8 --trust-remote-code --port 30000

```

来自 Unsloth 和 Llama.cpp 的动态量化

运行像 DeepSeek V3-0324 这样的大型 LLM 可能需要大量计算资源，并且需要大量 GPU 显存。这时量化就派上用场了，它允许最终用户使用相同的模型，但显存消耗大大降低，而下游性能的牺牲很小。

Unsloth AI 创建了动态量化，使得可以在仅需一个 H100 节点一半计算资源的情况下运行 DeepSeek V3，并且可以在 llama.cpp 上运行，而基准测试性能下降不大。在此了解更多信息：https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF

## 它安全吗？

自从第一个 GPT 模型发布以来，安全地运行语言模型一直是关注的中心。随着 DeepSeek 模型的巨大流行及其来源，这个问题重新引起了关注。让我们梳理一下哪些事情是安全的，哪些领域需要谨慎。这并非 DeepSeek 特有，而是适用于任何开源模型！

首先——下载模型本身是否安全？

### 下载和运行模型

是的，下载模型是安全的。Hub 方面采取了一些预防措施，确保下载和运行模型是安全的：

- Safetensors：使用 `safetensors` 格式在 Hub 上存储 DeepSeek 模型权重，确保无法隐藏代码执行；而旧的 PyTorch `pickle` 格式存在这种风险。因此，权重文件中无法隐藏恶意代码。更多信息请阅读 Safetensors 博客。
- 建模代码：要运行模型，建模代码也需要与权重文件一起下载。这里有三种机制来提高安全性：1. 文件在 Hub 上完全可见；2. 用户需要显式设置 `trust_remote_code=True` 才能执行与模型相关的任何代码；3. 安全扫描器会扫描 Hub 上的文件，并标记任何恶意代码文件。如果您想格外小心，可以使用 `revision` 设置固定模型版本，以确保下载经过审查的建模代码版本。

因此，下载权重是安全的，并且在代码审查后，执行建模代码也是安全的。这意味着您可以在本地运行 DeepSeek 模型，而无需担心后门或恶意代码执行的风险。

那么，除了下载和运行模型之外，主要风险是什么？这取决于您如何处理模型输出！

### 模型输出

以下建议并非针对特定模型，同时适用于开源和闭源模型：无论是考虑模型内置的隐蔽行为所引发的风险，还是模型意外产生不良输出的风险。

我们将从三个领域探讨风险：对齐、代码生成和Agent（智能体）。

对齐偏差：每个模型提供商都会选择其模型的对齐方式及对齐价值观。这些价值观是什么、如何选择通常不透明，并且可能随时间变化（参见此项研究）。开源模型的优势在于，其对齐方式可以在后续阶段通过自定义微调进行更改，正如Perplexity的DeepSeek 1776示例所示。

![GPT-3.5-turbo中的经济与社会价值偏移](/images/posts/ecc17ab36d39.png)

![DeepSeek模型与Perplexity的R1 1776模型的拒绝频率对比](/images/posts/f643f7c177b5.png)

作为一般规则，用户应意识到任何LLM（大语言模型）都会以某种方式存在偏差，并据此对待模型输出。

代码生成：LLM（大语言模型）最流行的用例之一是作为编程助手。然而，这也是不加区分地使用模型输出可能产生最负面影响的领域。模型在大量已发布的代码（包括新旧代码）上进行训练。这些代码通常包含潜在的恶意代码或含有已知漏洞的代码。因此，模型在提出代码解决方案时可能产生类似的漏洞。

那么，在使用LLM（大语言模型）进行代码开发时，如何防止安全问题？对建议的更改进行彻底的代码审查，并使用适当的工具扫描代码中的漏洞，就像对待任何其他代码贡献一样。

Agent（智能体）：在过去几个月中，Agent（智能体）应用引起了极大关注，赋予LLM（大语言模型）更多自主权和代理能力也带来了风险。重要的是要谨慎对待Agent（智能体）拥有的系统访问权限以及你提供给它们的信息。一些良好实践包括：

- 沙箱：不要在拥有计算机访问和控制权限的本地机器上运行Agent（智能体）。这可以避免泄露私人信息或意外删除重要文件。
- 私人信息：不要与LLM（大语言模型）共享登录信息等私人数据。如果需要让模型访问系统，请使用具有严格访问规则的专用访问密钥。
- 人机协同：对于希望通过Agent（智能体）自动化的高风险流程，确保在最终确认环节有人类参与。

TL;DR：运行模型安全吗？是的，下载和运行模型是安全的，但与任何模型一样，你应该采取预防措施，在适当的安全措施下使用模型生成的内容。

---

> 本文由AI自动翻译，原文链接：[Open R1: Update #4](https://huggingface.co/blog/open-r1/update-4)
> 
> 翻译时间：2026-05-06 05:28
