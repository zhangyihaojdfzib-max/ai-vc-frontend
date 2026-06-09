---
title: Judge Arena：LLM作为评估者的基准测试平台
title_original: 'Judge Arena: Benchmarking LLMs as Evaluators'
date: '2024-11-19'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/arena-atla
author: ''
summary: Judge Arena是一个众包平台，用于比较不同LLM作为评估者的能力。用户可在测试样本上运行两个评判者模型，并投票选出更符合自己判断的结果。平台包含18个最先进模型（如GPT-4、Claude、Llama、Qwen等），并基于Elo评分生成排行榜。早期结果显示，专有与开源模型表现混合，GPT-4
  Turbo领先，但Llama和Qwen模型极具竞争力，较小模型也表现突出。该项目旨在帮助开发者选择最佳评估模型，并计划分享部分匿名数据以支持社区研究。
categories:
- AI产品
tags:
- LLM评估
- 基准测试
- 众包
- 模型对比
- 开源
draft: false
translated_at: '2026-06-09T06:07:24.316109'
---

# Judge Arena: 将LLM作为评估者的基准测试

LLM-as-a-Judge（LLM作为评判者）已成为评估LLM应用自然语言输出的一种流行方式，但我们如何知道哪些模型是最佳评判者？

我们很高兴推出Judge Arena——一个让任何人都能轻松并排比较模型作为评判者的平台。只需在测试样本上运行评判者，然后投票选出你最认同的评判者。结果将整理成一个排行榜，展示最佳评判者。

## Judge Arena

众包、随机对战已被证明是LLM基准测试的有效方法。LMSys的Chatbot Arena已收集超过200万票，并被高度认可为识别最佳语言模型的实地测试。由于LLM评估旨在捕捉人类偏好，直接的人类反馈也是确定哪些AI评判者最有帮助的关键。

### 运作方式

1. 选择你的评估样本：

- 让系统随机生成一个 👩 用户输入 / 🤖 AI 回复 对
- 或者输入你自己的自定义样本

1. 两个LLM评判者将：

- 对回复进行评分
- 提供评分的推理依据

1. 查看两位评判者的评估，并投票选出最符合你判断的那一位（我们建议先查看评分，再比较评语）

查看两位评判者的评估，并投票选出最符合你判断的那一位

（我们建议先查看评分，再比较评语）

每次投票后，你可以：

- 重新生成评判者：获取对同一样本的新评估
- 开始🎲 新回合：随机生成一个新样本进行评估
- 或者，输入一个新的自定义样本进行评估

为避免偏见和潜在滥用，模型名称仅在投票提交后才显示。

## 选定模型

Judge Arena专注于LLM-as-a-Judge方法，因此仅包含生成式模型（排除仅输出分数的分类器模型）。我们将AI评判者的选择标准正式化为以下两点：

1. 模型应具备有效评分和评语其他模型输出的能力。
2. 模型应能通过提示词以不同评分格式、针对不同标准进行评估。

我们为排行榜选择了18个最先进的LLM。虽然许多是权重公开的开源模型，我们也纳入了专有API模型，以便直接比较开源和闭源方法。

- OpenAI（GPT-4o、GPT-4 Turbo、GPT-3.5 Turbo）
- Anthropic（Claude 3.5 Sonnet / Haiku、Claude 3 Opus / Sonnet / Haiku）
- Meta（Llama 3.1 Instruct Turbo 405B / 70B / 8B）
- Alibaba（Qwen 2.5 Instruct Turbo 7B / 72B、Qwen 2 Instruct 72B）
- Google（Gemma 2 9B / 27B）
- Mistral（Instruct v0.3 7B、Instruct v0.1 7B）

当前列表代表了AI评估流程中最常用的模型。如果我们的排行榜被证明有用，我们期待添加更多模型。

## 排行榜

从Judge Arena收集的投票将被整理并显示在一个专门的公共排行榜上。我们为每个模型计算Elo分数，并将每小时更新排行榜。

## 早期洞察

这些只是非常早期的结果，但以下是我们迄今为止观察到的：

- 专有和开源模型中的顶级表现者混合：GPT-4 Turbo以微弱优势领先，但Llama和Qwen模型极具竞争力，超越了大多数专有模型
- 较小模型表现令人印象深刻：Qwen 2.5 7B和Llama 3.1 8B表现异常出色，与更大的模型竞争。随着我们收集更多数据，我们希望更好地理解模型规模与评判能力之间的关系
- 对新兴研究的初步实证支持：LLM-as-a-Judge文献表明，Llama模型非常适合作为基础模型，在评估基准上表现出强大的开箱即用性能。包括Lynx、Auto-J和SFR-LLaMA-3.1-Judge在内的几种方法选择以Llama模型为起点，再进行评估能力的后训练。我们的初步结果与此趋势一致，显示Llama 3.1 70B和405B分别排名第二和第三

随着排行榜在未来几周内逐渐成型，我们期待在我们的博客上分享进一步的分析结果。

## 如何贡献

我们希望Judge Arena成为社区的有用资源。通过为这个排行榜做出贡献，你将帮助开发者确定在评估流程中使用哪些模型。我们承诺在未来几个月内分享20%的匿名投票数据，希望开发者、研究人员和用户能够利用我们的发现构建更对齐的评估者。

我们期待听到你的反馈！对于一般功能请求或提交/建议加入竞技场的新模型，请在社区标签中发起讨论，或在Discord上与我们交流。如有任何问题或建议，请随时通过X/Twitter给我们发消息。

Atla目前自费资助该项目。我们正在寻找API积分（无附加条件）来支持这项社区工作——如果你有兴趣合作，请通过support@atla-ai.com联系我们 🤗

## 致谢

感谢所有帮助测试此竞技场的人，并向LMSYS团队致敬，感谢他们的启发。特别感谢Clémentine Fourrier和Hugging Face团队使这一切成为可能！

---

> 本文由AI自动翻译，原文链接：[Judge Arena: Benchmarking LLMs as Evaluators](https://huggingface.co/blog/arena-atla)
> 
> 翻译时间：2026-06-09 06:07
