---
title: Databricks提示词缓存加速开源LLM推理
title_original: Accelerating LLM Inference with Prompt Caching for Open‑Source Models
  on Databricks
date: '2026-05-22'
source: Databricks Blog
source_url: https://www.databricks.com/blog/accelerating-llm-inference-prompt-caching-open-source-models-databricks
author: ''
summary: Databricks将提示词缓存功能扩展至开源模型，通过自动复用重复提示词的KV缓存，显著提升LLM推理性能。在生产环境中，GPT-OSS模型的吞吐量提升2.5倍，P50延迟降低3倍，且无需任何配置。该功能支持批量推理、按Token计费和预置吞吐量工作负载，缓存仅驻留于易失性内存，确保安全性。提示词缓存可降低延迟、提高吞吐量，并分摊领域特定系统提示词的计算成本，使开源模型在企业任务中表现更优。
categories:
- AI基础设施
tags:
- 提示词缓存
- LLM推理
- Databricks
- 开源模型
- 性能优化
draft: false
translated_at: '2026-05-23T05:40:47.656171'
---

- 提示词缓存会复用重复的提示词前缀，从而使LLM运行更快。它能自动降低延迟并提升吞吐量。
- Databricks现在支持在批量推理、按Token计费和预置工作负载中，为开源模型提供提示词缓存。无需任何设置。
- 在GPT-OSS的生产环境中，提示词缓存将吞吐量提升了2.5倍，并将P50延迟降低了3倍。

## 为什么提示词缓存很重要

大语言模型（LLM）的推理过程常常涉及重复的提示词——试想相同的系统提示词或指令提示词出现在数千个请求中。每次调用都重新处理相同的前缀会浪费计算周期、增加延迟并提高成本。

提示词缓存消除了这种冗余，带来以下优势：

- 更低的延迟——命中缓存时可跳过预填充阶段。
- 更高的吞吐量——每个模型单元可处理更多Token。

提示词缓存可以成为一种强大的技术，在不影响模型Token吞吐量的前提下，提升模型在特定领域的质量。查询可以共享一个大型的领域特定系统提示词，该共享提示词的计算成本会在所有查询中被分摊。前沿模型（如Claude）在底层使用了长达数千Token的系统提示词。此外，在我们最近发表的研究中，我们展示了自动提示词优化如何使开源模型在企业任务中超越前沿模型的质量。

## 功能可用性

Databricks已为专有模型（GPT、Gemini、Claude）提供内置的提示词缓存。我们现在已将此功能扩展到为我们的基础模型API（FMAPI）提供支持的开源权重模型，适用于批量推理、按Token计费和预置吞吐量工作负载。该功能同样适用于所有由基础模型驱动的更高级别服务，例如Agent Bricks、Genie、AI Functions。

提示词缓存现在支持以下托管在Databricks上的开源模型：

- GPT‑OSS 20B和120B
- 经过微调的Llama 3.1 8B（通过PEFT服务）
- Llama 3.1 8B和3.3 70B

我们将继续在我们的其他模型中推出此功能。安全性是Databricks的首要关注点。提示词缓存是隔离的，仅驻留在易失性内存中，并且永远不会持久化。重要的是，缓存是隐式的：客户无需配置任何内容，我们的系统已构建为自动运行提示词缓存并复用以提升吞吐量。

## 实际影响：GPT OSS上的批量推理

我们首先将提示词缓存部署到我们的GPT‑OSS模型，并立即在一个大规模生产级批量推理管道中看到了可衡量的收益：

- 每个副本的输入Token吞吐量提升了2.5倍
- P50延迟降低了3倍
- 所有这些都是在相对较低的30%缓存命中率下实现的

![提示词缓存 GPT‑OSS 模型](/images/posts/6274cc502a2f.png)

## 总结

通过自动复用相同提示词的KV缓存，Databricks使您能够更快、更具成本效益且更安全地运行开源LLM——所有这些都无需任何额外配置。无论您是在提供实时聊天、批量处理大型文档集合，还是构建AI Agent，提示词缓存都能将优秀的推理管道转变为卓越的管道。在您的下一次开源模型部署中尝试一下，看看性能指标如何攀升。

### 在您的收件箱中获取最新文章

订阅我们的博客，让最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Accelerating LLM Inference with Prompt Caching for Open‑Source Models on Databricks](https://www.databricks.com/blog/accelerating-llm-inference-prompt-caching-open-source-models-databricks)
> 
> 翻译时间：2026-05-23 05:40
