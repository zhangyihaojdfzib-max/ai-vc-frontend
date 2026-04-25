---
title: HELMET：全面评估长上下文语言模型的新基准
title_original: 'Introducing HELMET: Holistically Evaluating Long-context Language
  Models'
date: '2025-04-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/helmet
author: ''
summary: HELMET是一个用于全面评估长上下文语言模型（LCLM）的基准，旨在解决现有评估过度依赖合成任务、下游任务覆盖不足、长度限制和指标不可靠等问题。该基准包含多样化任务（如检索增强生成、带引用的生成和摘要），支持可控长度和难度，并兼容基础模型与指令微调模型。通过对59个最新LCLM的评估，发现前沿模型在复杂任务上仍存在局限性。文章还提供了快速入门指南，帮助实践者使用HELMET进行模型评估。
categories:
- AI研究
tags:
- 长上下文语言模型
- 模型评估
- HELMET
- 基准测试
- 自然语言处理
draft: false
translated_at: '2026-04-25T04:36:33.710489'
---

# 介绍 HELMET：全面评估长上下文语言模型

联系方式：hyen@cs.princeton.edu  
论文：https://arxiv.org/abs/2410.02694  
网站：https://princeton-nlp.github.io/HELMET  
代码与数据：https://github.com/princeton-nlp/HELMET

自去年十月我们首次发布 HELMET 以来，长上下文语言模型的发展比以往任何时候都要迅速，我们非常高兴看到社区对 HELMET 的采用，例如微软的 Phi-4 和 AI21 的 Jamba 1.6。
在首次发布之后，我们在评估套件中增加了更多模型，并进行了额外的分析。我们很高兴分享新的结果，并在 ICLR 2025 上展示 HELMET！

在这篇博客中，我们将介绍 HELMET 的构建过程、主要发现，以及实践者如何在未来的研究和应用中使用 HELMET 来区分不同的 LCLM。
最后，我们将提供一个快速入门指南，介绍如何使用 HuggingFace 使用 HELMET。

## 评估长上下文语言模型具有挑战性但很重要

从总结大量法律文档到即时学习新任务，长上下文语言模型（LCLM）在改变我们使用和交互语言模型的方式方面具有巨大潜力。
语言模型一直受到其上下文窗口的限制，大约为 2K 到 8K Token（例如 ChatGPT、Llama-2/3）。
最近，模型开发者不断扩展其模型的上下文窗口，像 GPT-4o、Claude-3 和 Gemini-1.5 等最新模型支持高达数百万 Token 的上下文窗口。

然而，随着上下文窗口的变长，以往的自然语言基准（例如 Scrolls）已不再适用于评估 LCLM。
因此，困惑度和合成任务（例如大海捞针）成为评估最新 LCLM 最流行的指标，但它们通常不能反映真实世界的性能。
模型开发者也可能在其他任意数据集上进行评估，这使得模型比较变得复杂。
此外，现有的 LCLM 基准可能显示出令人困惑且反直觉的结果，使得理解不同模型的优势和劣势变得困难（图 1）。

在这项工作中，我们提出了 HELMET（如何有效且全面地评估长上下文模型），这是一个用于评估 LCLM 的全面基准，在多样性、可控性和可靠性方面对现有基准进行了改进。
我们评估了 59 个最新的 LCLM，发现跨不同应用评估模型以理解其能力至关重要，而前沿 LCLM 在复杂任务上仍然存在局限性。

## 现有评估过度依赖合成任务

随着 LCLM 在工业界和开源社区的发展，拥有可靠的评估和比较这些模型的方法至关重要。然而，当前模型通常在不同的基准上进行评估（表 1）。

评估长上下文语言模型的一种常见做法是使用困惑度或合成任务，例如大海捞针（NIAH）。
然而，最近的研究表明，困惑度与下游性能的相关性不佳（Fang 等人，2024）。
在图 2 中，我们展示了像 NIAH 这样的合成任务与真实世界性能不相关，但更复杂的合成任务与真实世界任务的相关性更高。

在现有的具有真实应用的基准中，例如 ZeroScrolls（Shaman 等人，2023）、LongBench（Bai 等人，2024）和 InfiniteBench（Zhang 等人，2024），仍然存在关键局限性：

- 下游任务覆盖不足：通常集中在特定领域
- 测试前沿 LCLM 的长度不足：较旧的 QA 数据集通常限制在 <32K Token（例如 QASPER、QuALITY）
- 不可靠的指标：像 ROUGE 这样的 N-gram 匹配指标噪声较大——它们与人类判断不相关（Goyal 等人，2023），也无法区分不同模型
- 与基础模型不兼容：需要指令微调，这意味着它们不能用于基础模型开发

因此，我们提出 HELMET 来解决这些局限性，并为 LCLM 提供全面评估。

## 为 LCLM 构建多样化、可控且可靠的评估

我们设计 HELMET 时遵循以下期望：

1. 下游任务的多样化覆盖
2. 可控的长度和复杂度
3. 对基础模型和指令微调模型的可靠评估

表 2 展示了该基准的概览。
在我们的实验中，我们评估了从 8K 到 128K Token 的输入长度，但 HELMET 可以轻松扩展到更长的上下文长度。

### 对现有基准的关键改进

多样化覆盖：HELMET 包含多样化的任务，例如使用真实检索段落的检索增强生成、带引用的生成和摘要。我们精心选择了具有自然长上下文的、反映真实应用的数据集。这些数据集辅以可靠的评估设置，例如基于模型的评估和人工研究。

可控长度和难度：评估 LCLM 时需要考虑的一个重要维度是输入长度，因为更长的输入可以提供更多信息，同时挑战模型处理噪声上下文的能力。在我们的任务中，我们可以通过更改检索段落数量（RAG、Cite、Re-rank）、示例数量（ICL）或输入文档长度（LongQA、Summ）来控制输入长度。虽然 LongQA 和 Summ 不容易扩展到更长的上下文，但我们特意选择了文档长度远超 100K Token 的自然数据集，这样它们仍然可以用于评估前沿 LCLM。

可靠评估：许多现有基准仍然使用基于 N-gram 的指标，例如 ROUGE，尽管它们与人类判断的相关性较差（Goyal 等人，2023）。我们采用基于模型的评估，这些评估在模型之间和不同输入长度之间显示出更好的区分度（图 3）。此外，我们的人工研究表明，我们的指标与人类判断具有高度一致性。

稳健的提示词：现有的长上下文基准通常要求模型遵循指令，但许多模型开发围绕基础模型展开，这些模型必须依赖合成任务或困惑度进行评估。因此，我们通过上下文学习示例为基础模型的部分任务提供支持。这显著提高了基础模型的性能，更能反映真实世界的应用。

## LCLM 在真实世界任务上仍有很长的路要走

我们的实验和分析包括 59 个 LCLM 的全面集合。据我们所知，这是对长上下文模型在不同应用上最全面、最受控的比较。这些模型涵盖了领先的专有模型和开源模型，我们还考虑了不同架构（例如全注意力 Transformer、混合架构）和位置外推技术的模型。在本节中，我们将重点介绍实验中的几个关键发现。

### 评估长上下文能力需要多样化的评估

长上下文基准通常针对特定应用构建，例如摘要或问答，这限制了对 LCLM 在更广泛背景下的理解。我们检查了模型在广泛真实任务上的性能，发现不同类别并不总是相互关联（图 4）。

虽然某些任务由于基于检索的性质而适度相关（例如 RAG 和 MS-MARCO），但其他任务几乎没有相关性（例如 Summ 和 Cite）。值得注意的是，ICL 与其他任务的相关性最低，这表明它是一个独特的任务，需要模型具备不同的能力。因此，模型开发者应该在这些不同的维度上进行评估，以更全面地了解模型的能力。

### 模型随着长度和任务复杂度的增加而退化

我们展示了前沿专有模型以及一些开源模型在HELMET上的结果。更多结果可在论文和网站中查看。

首先，我们观察到开源模型在复杂任务上落后于闭源模型。虽然在简单任务（如Recall）上差距较小，但在更复杂的任务（如Cite）上差距会扩大。

此外，性能随长度增加而下降的情况因类别而异。即使是最先进的模型（如GPT-4o和Gemini），在重排序等任务上性能也会显著下降。这种性能变化无法仅通过观察合成任务的表现来发现。

最后，所有类别中并没有明确的胜出者，因此需要从不同维度进行评估。更多分析（如不同位置外推方法的性能以及"中间丢失"现象）可在论文中找到。

## 使用HELMET进行未来开发

### 如何运行HELMET

使用HELMET非常简单！只需克隆我们的GitHub仓库，设置好环境后即可开始运行！

我们提供了多种加载模型的方式，可在配置文件中进行配置：

1. 使用HuggingFace的transformers库
2. 使用HuggingFace的TGI在本地启动模型端点
3. 使用HuggingFace的Inference Endpoints启动远程模型端点
4. 使用vllm在本地启动模型端点。注意：你可以在Intel Gaudi加速器上启动vllm端点。
5. 使用模型提供商的API

#### 选项1：使用HuggingFace的transformers库

只需使用我们仓库中的配置文件，并通过以下命令运行评估：

```
python eval.py --config configs/rag.yaml --model_name_or_path <model_name>

```

后台会使用HuggingFace的transformers库，并自动支持本地和远程模型。

#### 选项2：使用HuggingFace的TGI

首先，按照TGI GitHub上的说明启动模型端点。然后在配置文件中指定端点URL。例如，你可以创建如下所示的config.yaml文件：

```
input_max_length: 131072
datasets: kilt_nq
generation_max_length: 20
test_files: data/kilt/nq-dev-multikilt_1000_k1000_dep6.jsonl
demo_files: data/kilt/nq-train-multikilt_1000_k3_dep6.jsonl
use_chat_template: true
max_test_samples: 100
shots: 2
stop_new_line: true
model_name_or_path: tgi:meta-llama/Llama-3.1-8B-Instruct # 需要添加"tgi:"前缀
use_tgi_serving: true # 在配置中添加此行

```

然后使用以下命令运行基准测试：

```bash
export LLM_ENPOINT=<your-tgi-endpoint> 
python eval.py --config configs/config.yaml --endpoint_url $LLM_ENDPOINT

```

#### 选项3：使用HuggingFace的Inference Endpoints

首先按照这里的说明设置端点。获取端点URL和API密钥。然后使用选项2中相同的config.yaml文件，运行以下命令：

```bash
export LLM_ENPOINT=<your-hf-inference-endpoint> 
export API_KEY=<your-hf-api-key>
python eval.py --config configs/config.yaml --endpoint_url $LLM_ENDPOINT --api_key $API_KEY

```

#### 选项4：使用VLLM

你可以在系统上使用vllm启动模型端点，包括Intel Gaudi2和Gaudi3加速器。查看这里的说明，了解如何在Intel Gaudi加速器上使用vllm运行HELMET。

你可以使用与选项2相同的示例config.yaml，只需修改以下两行：

```
model_name_or_path: meta-llama/Llama-3.1-8B-Instruct # 无需前缀
use_vllm_serving: true # 使用vllm替代tgi

```

```bash
export LLM_ENPOINT=<your-vllm-endpoint>
python eval.py --config configs/config.yaml --endpoint_url $LLM_ENDPOINT

```

#### 选项5：使用模型提供商的API

我们支持OpenAI、Anthropic、Google和TogetherAI的API。请参考我们仓库中的说明。

### 加速开发

我们建议在模型开发过程中使用Recall和RAG任务进行快速迭代。这些任务在快速评估与其他现实任务的相关性之间取得了良好平衡。你可以通过以下命令轻松运行这些评估：

```bash
python eval.py --config configs/rag.yaml --model_name_or_path <model_name>

```

### 与现有模型的快速比较

运行所有基线来评估长上下文语言模型（LCLM）通常成本高昂，尤其是在长上下文场景下，计算和内存开销巨大。例如，在70B模型上以所有长度运行HELMET需要一个配备8块80GB GPU的节点，耗时数百个GPU小时，成本很高。通过在HELMET上进行评估，研究人员可以直接将他们的模型与现有模型进行比较，只需参考我们的结果即可，这些结果涵盖了59个不同规模和架构的模型。你可以在我们的网站上找到排行榜。

### 未来展望

HELMET是向更全面评估长上下文语言模型迈出的一步，但LCLM还有许多令人兴奋的应用。例如，我们最近发布了LongProc，这是一个用于评估LCLM在长文本生成和遵循指令方面能力的基准测试，这对于开发在思考步骤中生成数万个Token的推理模型至关重要。虽然摘要任务有较长的输出（最多1K Token），但LongProc专注于更长的输出，最多8K Token。与HELMET类似，LongProc也设计了可靠的评估设置和多样化的任务。我们正在努力将LongProc整合到HELMET的评估套件中，希望这能为长文本任务上的LCLM提供更全面的评估。

## 致谢

我们感谢Mengzhou Xia、Howard Chen、Xi Ye、Yinghui He、Lucy He、Alexander Wettig、Sadhika Malladi、Adithya Bhaskar、Joie Zhang以及普林斯顿语言与智能（PLI）小组的其他成员提供的宝贵反馈。本研究得到了微软加速基础模型研究（AFMR）项目提供的Azure OpenAI积分以及Intel的资助。

## 引用

如果你觉得HELMET有用，请考虑引用我们的论文：

```
@inproceedings{yen2025helmet,
      title={HELMET: How to Evaluate Long-Context Language Models Effectively and Thoroughly}, 
      author={Howard Yen and Tianyu Gao and Minmin Hou and Ke Ding and Daniel Fleischer and Peter Izsak and Moshe Wasserblat and Danqi Chen},
      year={2025},
      booktitle={International Conference on Learning Representations (ICLR)},
}

```

---

> 本文由AI自动翻译，原文链接：[Introducing HELMET: Holistically Evaluating Long-context Language Models](https://huggingface.co/blog/helmet)
> 
> 翻译时间：2026-04-25 04:36
