---
title: Granite 4.0 Nano发布：IBM推出迄今最小模型，专为边缘计算设计
title_original: 'Granite 4.0 Nano: Just how small can you go?'
date: '2025-10-28'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-granite/granite-4-nano
author: ''
summary: IBM发布了Granite 4.0模型家族中最小的成员——Granite 4.0 Nano系列，包含15亿参数和3.5亿参数两种规格的稠密LLM，以及对应的传统Transformer版本。这些模型专为边缘和设备端应用优化，采用改进的训练方法和超过15T
  Token的数据训练，并在Apache 2.0许可证下开源。在通用知识、数学、代码和安全基准测试中，该系列模型以极少的参数量实现了显著的性能提升，尤其在指令遵循和工具调用任务上表现突出，已获得ISO
  42001负责任AI开发认证。
categories:
- AI产品
tags:
- Granite 4.0
- 边缘AI
- 小参数模型
- 开源模型
- IBM
draft: false
translated_at: '2026-01-08T04:43:30.972960'
---

# Granite 4.0 Nano：模型究竟可以做到多小？


![](/images/posts/9bc3346835fd.jpg)

![](/images/posts/ac0e506ba48d.jpg)

![](/images/posts/0b27d2d98618.jpg)

![](/images/posts/ed23d04248c4.jpg)

![](/images/posts/5a2e0b6d591e.jpg)


今天我们很高兴地分享 Granite 4.0 Nano，这是我们迄今为止最小的模型，作为 IBM Granite 4.0 模型家族的一部分发布。这些模型专为边缘和设备端应用设计，在其尺寸级别上展现出卓越的性能，体现了 IBM 持续致力于开发强大、实用且无需数千亿参数即可完成任务的模型。

与所有 Granite 4.0 模型一样，Nano 模型在 Apache 2.0 许可证下发布，并在 vLLM、llama.cpp 和 MLX 等流行运行时上提供原生架构支持。这些模型采用了与原始 Granite 4.0 模型相同的改进训练方法、流水线以及超过 15T Token 的训练数据进行训练。此版本包含受益于 Granite 4.0 新型高效混合架构的变体，并且与所有 Granite 语言模型一样，Granite 4.0 Nano 模型也获得了 IBM 负责任模型开发的 ISO 42001 认证，让用户更有信心相信这些模型的构建和管理符合全球标准。

具体而言，Granite 4.0 Nano 包含 4 个指令模型及其对应的基础模型：

- Granite 4.0 H 1B – 一个约 15 亿参数的稠密 LLM，采用基于混合 SSM 的架构。
- Granite 4.0 H 350M – 一个约 3.5 亿参数的稠密 LLM，采用基于混合 SSM 的架构。
- Granite 4.0 1B 和 Granite 4.0 350M – 我们 10 亿和 3.5 亿参数 Nano 模型的替代传统 Transformer 版本，旨在支持混合架构可能尚未获得优化支持的工作负载（例如 Llama.cpp）。

构建十亿参数以下至约十亿参数的模型是一个活跃且竞争激烈的领域，阿里巴巴（Qwen）、LiquidAI（LFM）、谷歌（Gemma）等多家模型开发商近期在性能和架构方面都取得了进展。与这些其他模型相比，Granite 4.0 Nano 模型在通用知识、数学、代码和安全领域的一系列通用基准测试中表明，能够以最小的参数量实现能力的显著提升。

图表 1. 0.2B–2B 参数模型在知识、数学、代码和安全基准测试中的平均准确率。完整细节见附录 I。

![granite-4-nano-chart1](/images/posts/3ec3e57b929d.png)

除了更通用的基准测试外，Granite Nano 模型在对于智能体工作流至关重要的任务上，包括遵循指令和工具调用（通过 IFEval 和伯克利函数调用排行榜 v3 基准测试衡量），表现优于多个尺寸相似的模型。

图表 2. IFEval 和 BFCLv3 基准测试的准确率。

![granite-4-nano-chart2](/images/posts/53bb5c6cd18c.png)

Granite 4.0 Nano 的完整细节可在 Hugging Face 模型卡片上找到。展望未来，随着我们持续壮大 Granite 4.0 家族并努力使 AI 成为开发者更高效、更有效的工具，请期待 IBM 的更多发布。

附录 I. 通用性能基准测试细分

![granite-4-nano-chart3](/images/posts/f400053b4a58.png)

![](/images/posts/96ede6a1ba57.png)

![](/images/posts/42e89a375726.jpg)

![](/images/posts/d0ac0931dbea.jpg)


![](/images/posts/3df41d9e86ff.png)

我们刚刚在 Word 中测试了本地 granite-4-h-tiny 模型进行合同分析：https://youtu.be/acX1CqF8TDA

令人印象深刻。我们计划很快尝试 nano 模型。

![1762166798800.Screenshot_20251103-154413](/images/posts/3d851fb4d049.jpg)

整个 Granite 系列都被低估了。我一直在训练 Granite 3 和 4 的小模型，它们学习速度非常快。它们是我执行专业任务的首选模型。

· 注册或登录以评论


![](/images/posts/287c63ff9896.jpg)

![](/images/posts/31b82c1d66b3.jpg)

![](/images/posts/71bf66847b57.jpg)

![](/images/posts/78bab46e000b.jpg)

![](/images/posts/8b621b556332.jpg)


> 本文由AI自动翻译，原文链接：[Granite 4.0 Nano: Just how small can you go?](https://huggingface.co/blog/ibm-granite/granite-4-nano)
> 
> 翻译时间：2026-01-08 04:43
