---
title: 3LM：首个阿拉伯语大语言模型STEM与代码基准测试
title_original: '📚 3LM: A Benchmark for Arabic LLMs in STEM and Code'
date: '2025-08-01'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tiiuae/3lm-benchmark
author: ''
summary: 本文介绍了3LM基准测试，这是首个专门用于评估阿拉伯语大语言模型在STEM科目和代码生成方面能力的多组件基准。它包含三个数据集：从真实教育内容提取的“原生STEM”多项选择题、通过LLM生成的“合成STEM”高难度推理题，以及将HumanEval+和MBPP+翻译改编而成的“阿拉伯语代码基准测试”。该基准旨在弥补现有评估在技术领域能力测试上的不足，并已对40多个模型进行了评估，为阿拉伯语NLP在科学推理和编程领域的发展提供了重要工具。
categories:
- AI研究
tags:
- 大语言模型
- 基准测试
- 阿拉伯语NLP
- STEM教育
- 代码生成
draft: false
translated_at: '2026-02-24T04:34:55.313150'
---

# 📚 3LM：面向阿拉伯语大语言模型的STEM与代码基准测试

📄arXiv论文|
📦HuggingFace数据集|
🔧GitHub代码

![image/png](/images/posts/484d62101f1d.png)

## 为何推出3LM？

近年来，阿拉伯语大语言模型取得了显著进展，然而现有的基准测试在评估高价值技术领域的性能方面存在不足。迄今为止，大多数评估都集中在摘要、情感分析或通用问答等通用任务上。然而，从教育到技术问题解决，科学推理和编程能力对于广泛的实际应用至关重要。

为了弥补这一空白，我们推出了 **3LM (علم)**，这是一个多组件的基准测试，专门用于评估阿拉伯语大语言模型在STEM（科学、技术、工程和数学）科目和代码生成方面的能力。3LM是首个此类基准测试，专门设计用于测试阿拉伯语模型在结构化推理和形式逻辑方面的能力，这些领域在阿拉伯语自然语言处理中传统上代表性不足。

## 基准测试包含什么？

3LM由三个数据集组成，每个数据集针对一个特定的评估维度：现实世界的多项选择STEM问题、合成的高难度STEM问题以及翻译后的代码生成任务。

### 1. 原生STEM

原生STEM基准测试包含从真实的阿拉伯语教育内容中提取的865道多项选择题，这些内容涵盖8至12年级的教科书、练习题和试题库。问题涵盖五个核心科目：物理、化学、生物、数学和地理。

每个问题都标注了元数据，包括领域和难度（1-10分制）。数据是通过一个结合了OCR（包括通过Pix2Tex进行LaTeX数学公式解析）、LLM辅助的问答提取以及人工审核的流程获取的。该数据集为使用真实教育材料评估阿拉伯语模型的事实和概念理解能力提供了一个现实的测试平台。

### 2. 合成STEM

为了引入更大的挑战和多样性，我们使用 **YourBench** 流程创建了一个包含1,744道多项选择题的合成子集。该组件基于阿拉伯语教科书文本，经过分块、总结，并用作LLM驱动的题目生成系统的输入。最终得到一组精心策划的题目，侧重于中高难度的推理，包括概念性、分析性和应用型问题。

合成STEM通过探究更深层次的推理能力并最小化答案偏差，为原生多项选择题提供了重要的补充。所有生成的问题都经过了基于清晰度、结构和内容有效性的筛选，随后通过人工审核进行质量保证。

### 3. 阿拉伯语代码基准测试

3LM的第三个组件针对代码生成，这是LLM评估中一个日益重要的领域。我们将广泛使用的HumanEval+和MBPP+基准测试翻译并改编成阿拉伯语，创建了首个用于测试阿拉伯语大语言模型在自然语言编程提示词方面的代码数据集。

我们使用GPT-4o进行提示词翻译，并通过回译流程验证结果，根据ROUGE-L F1阈值（< 0.8）拒绝低质量样本。额外的人工筛选确保了提示词的清晰度和正确性。代码和测试套件保持不变，以保持评分的保真度。评估使用EvalPlus框架进行pass@1和pass@1+指标计算。

## 构建基准测试

3LM中的每个数据集都经历了多阶段的开发过程，以确保数据质量、公平性和代表性。

对于**原生STEM**，我们收集了阿拉伯语PDF源文件，并应用了双重OCR方法来恢复纯文本和数学公式。问题通过基于LLM的分块和模式识别进行提取，随后分类为随机答案顺序的多项选择题格式。最终样本由具有STEM专业知识的阿拉伯语母语者审核，以确认答案的有效性和可读性。

![image/png](/images/posts/cc27a121fdad.png)

对于**合成STEM**，我们调整了YourBench流程以适应阿拉伯语输入。摄取后的源文档首先进行总结、分块，然后输入到代码控制的生成器中以创建多项选择题。我们过滤掉了依赖图像或内容模糊的部分，只保留了目标难度范围内的问题。最终得到了一组干净、高质量的阿拉伯语合成STEM多项选择题。

对于**代码基准测试**，我们的目标是在保留代码逻辑的同时，隔离语言理解的影响。提示词翻译由GPT-4o处理，并通过反向翻译进行验证。代码和测试保持不变，以便与英文版本保持评估一致性。最终得到的基准测试允许使用EvalPlus工具链直接评估阿拉伯语提示词。

## 关键结果

我们评估了超过40个大语言模型，包括阿拉伯语优先、多语言以及通用基础模型和指令微调模型。评估使用了多项选择准确率和生成式完成度指标。

![image/png](/images/posts/d9a0a42d2a81.png)

在**多项选择题**设置中，Qwen2.5-72B-Instruct在原生STEM（71.8%）和合成STEM（67.0%）子集上均取得了最佳性能。在**完成度任务**中，Gemma-3-27B表现最强，在STEM答案上达到43.2%的准确率。

在**代码生成**方面，GPT-4o在HumanEval-ar（83.5% pass@1+）和MBPP-ar（63.6% pass@1+）上都展示了同类最佳的性能。这些结果突显了阿拉伯语和英语pass@1分数之间的强相关性（约0.97），表明特定语言的提示词质量对模型结果有重大影响。

![image/png](/images/posts/9562d5066ad4.png)

我们还研究了**干扰项扰动下的鲁棒性**，发现指令微调模型比其基础模型要稳定得多。提示工程和零样本设计也被证明对阿拉伯语STEM性能有显著影响。

## 评估工具

我们构建的基准测试可以使用标准工具轻松复现：

- **lighteval** 处理STEM数据集的多项选择和开放式问题评估。
- **evalplus** 使用函数级测试进行稳健的pass@1和pass@1+代码评分。

所有脚本、配置和评估流程均可在我们的 **GitHub仓库** 中找到，并可进行调整以评估任何与HuggingFace Transformers或OpenAI API兼容的模型。

## 访问数据集

所有三个数据集都是开源的，并托管在HuggingFace Datasets上：

- 3LM-native-stem
- 3LM-synthetic-stem
- 3LM-code-arabic

## 引用

如果您在研究中使用了3LM，请引用我们：

```bibtex
@inproceedings{boussaha-etal-2025-3lm,
    title = "3{LM}: Bridging {A}rabic, {STEM}, and Code through Benchmarking",
    author = "Boussaha, Basma El Amel  and
      Al Qadi, Leen  and
      Farooq, Mugariya  and
      Alsuwaidi, Shaikha  and
      Campesan, Giulia  and
      Alzubaidi, Ahmed  and
      Alyafeai, Mohammed  and
      Hacid, Hakim",
    booktitle = "Proceedings of The Third Arabic Natural Language Processing Conference",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.arabicnlp-main.4/",
    doi = "10.18653/v1/2025.arabicnlp-main.4",
    pages = "42--63",
    ISBN = "979-8-89176-352-4",
}
```

---

> 本文由AI自动翻译，原文链接：[📚 3LM: A Benchmark for Arabic LLMs in STEM and Code](https://huggingface.co/blog/tiiuae/3lm-benchmark)
> 
> 翻译时间：2026-02-24 04:34
