---
title: Hugging Face推出AI Sheets：无需代码，用开源模型处理数据集
title_original: 'Introducing AI Sheets: a tool to work with datasets using open AI
  models!'
date: '2025-08-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/aisheets
author: ''
summary: Hugging Face发布了全新的开源工具AI Sheets，它允许用户无需编写代码即可利用开源AI模型构建、转换和丰富数据集。该工具提供类似电子表格的直观界面，支持从Hugging
  Face Hub调用数千个模型，包括OpenAI的gpt-oss，并可本地或云端部署。用户可通过编写提示词创建新列，进行模型比较、提示词优化、数据分类、分析、清理及合成数据生成等操作，特别适合快速实验和小规模数据迭代。
categories:
- AI产品
tags:
- Hugging Face
- 无代码AI
- 数据集处理
- 开源模型
- 提示工程
draft: false
translated_at: '2026-02-21T04:18:08.443689'
---

# 介绍 AI Sheets：一款使用开源 AI 模型处理数据集的工具！

🧭 太长不看版

Hugging Face AI Sheets 是一款全新的开源工具，无需代码即可使用 AI 模型构建、丰富和转换数据集。该工具可以本地部署或在 Hub 上部署。它让你可以通过推理服务提供商或本地模型（包括来自 OpenAI 的 `gpt-oss`！）使用 Hugging Face Hub 上的数千个开源模型。

## 有用链接

免费试用该工具（无需安装）：https://huggingface.co/spaces/aisheets/sheets
本地安装和运行：https://github.com/huggingface/sheets

## 什么是 AI Sheets

AI Sheets 是一款无需代码的工具，用于使用（开源）AI 模型构建、转换和丰富数据集。它与 Hub 和开源 AI 生态系统紧密集成。

AI Sheets 采用易于学习的用户界面，类似于电子表格。该工具围绕快速实验而构建，先从小数据集开始，然后再运行耗时/成本高的数据生成流程。

在 AI Sheets 中，通过编写提示词来创建新列，你可以根据需要迭代多次，并编辑单元格/验证单元格来教导模型你想要什么。但更多内容稍后介绍！

## 我能用它做什么

你可以使用 AI Sheets 来：

**比较和感受测试模型。** 假设你想在你的数据上测试最新模型。你可以导入一个包含提示词/问题的数据集，并使用类似这样的提示词创建多个列（每个模型一列）：`回答以下问题：{{prompt}}`，其中 `prompt` 是你数据集中的一个列。你可以手动验证结果，或者创建一个新列，使用一个 LLM 作为评判提示词，例如：`评估对以下问题的回答：{{prompt}}。回答 1：{{model1}}。回答 2：{{model2}}`，其中 `model1` 和 `model2` 是你数据集中包含不同模型回答的列。

**为你的数据和特定模型改进提示词。** 假设你想构建一个应用程序来处理客户请求并给出自动回复。你可以加载一个包含客户请求的样本数据集，并开始使用不同的提示词和模型进行尝试和迭代以生成回复。AI Sheets 的一个很酷的功能是，你可以通过编辑或验证单元格来提供反馈。这些示例单元格将自动添加到你的提示词中。你可以将其视为一个工具，通过实时查看你的数据，非常高效地微调提示词并为你的提示词添加上下文示例！

**转换数据集。** 假设你想清理数据集中的某一列。你可以添加一个新列，使用类似这样的提示词：`从以下文本中移除多余的标点符号：{{text}}`，其中 `text` 是你数据集中包含要清理文本的列。

**分类数据集。** 假设你想对数据集中的某些内容进行分类。你可以添加一个新列，使用类似这样的提示词：`对以下文本进行分类：{{text}}`，其中 `text` 是你数据集中包含要分类文本的列。

**分析数据集。** 假设你想提取数据集中的主要观点。你可以添加一个新列，使用类似这样的提示词：`从以下内容中提取最重要的观点：{{text}}`，其中 `text` 是你数据集中包含要分析文本的列。

**丰富数据集。** 假设你有一个包含地址但缺少邮政编码的数据集。你可以添加一个新列，使用类似这样的提示词：`查找以下地址的邮政编码：{{address}}`（在这种情况下，你必须启用“搜索网络”选项以确保结果准确）。

**生成合成数据集。** 假设你需要一个包含真实电子邮件的数据集，但由于数据隐私原因无法获得。你可以使用类似这样的提示词创建一个数据集：`写一段关于制药公司领域专业人士的简短描述`，并将该列命名为 `person_bio`。然后，你可以使用类似这样的提示词创建另一列：`写一封由以下人士撰写的真实专业电子邮件：{{person_bio}}`。

现在让我们深入了解如何使用它！

## 如何使用

AI Sheets 为你提供了两种开始方式：导入现有数据或从头开始生成数据集。加载数据后，你可以通过添加列、编辑单元格和重新生成内容来完善它。

![image/png](/images/posts/f8064751989d.png)

### 开始使用

要开始使用，你需要通过自然语言描述从头创建一个数据集，或者导入一个现有数据集。

#### 从头生成数据集

**最适合：** 熟悉 AI Sheets、头脑风暴、快速实验以及创建测试数据集。

可以将其视为自动数据集或提示词到数据集功能——你描述你想要什么，AI Sheets 为你创建整个数据集结构和内容。

**何时使用此功能：**

*   你第一次探索 AI Sheets
*   你需要用于测试或原型设计的合成数据
*   数据准确性和多样性并不关键（例如，头脑风暴用例、快速研究、生成测试数据集）
*   你想快速尝试想法

**工作原理：**

1.  在提示词区域描述你想要的数据集
    示例："一个虚构初创公司的列表，包含名称、行业和口号"
2.  AI Sheets 生成模式并创建 5 个样本行
3.  扩展到最多 1,000 行，或修改提示词以更改结构

**示例**

如果你输入这个提示词：`世界各地的城市，以及它们所属的国家和每个城市的标志性图片，以吉卜力风格生成：`

![image/png](/images/posts/406eed3308f7.png)

AI Sheets 将自动生成一个包含三列的数据集，如下所示：

![image/png](/images/posts/4aeef5779030.png)

这个数据集只包含五行，但你可以通过向下拖动每列（包括图片列！）来添加更多单元格。你也可以在任何单元格中写入项目，并通过拖动来完成其他单元格。

![image/png](/images/posts/3a306400e10b.png)

以下部分将向你展示如何迭代和扩展数据集。

#### 导入你的数据集（推荐）

**最适合：** 大多数你想要转换、分类、丰富和分析真实世界数据的用例。

对于大多数用例，推荐使用此方法，因为与从头开始相比，导入真实数据能给你更多的控制和灵活性。

*   你拥有想要使用 AI 模型转换或丰富的现有数据
*   你想生成合成数据，并且准确性和多样性很重要

1.  以 XLS、TSV、CSV 或 Parquet 格式上传你的数据
2.  确保你的文件至少包含一个列名和一行数据
3.  最多上传 1,000 行（列数不限）
4.  你的数据将以熟悉的电子表格格式显示

**专业提示：** 如果你的文件包含的数据很少，你可以直接在电子表格中输入来手动添加更多条目。

### 处理你的数据集

一旦你的数据加载完成（无论你如何开始），你将在可编辑的电子表格界面中看到它。以下是你需要了解的：

**理解 AI Sheets**

*   **导入的单元格：** 可手动编辑，但不能通过 AI 提示词修改
*   **AI 生成的单元格：** 可以使用提示词和你的反馈（编辑 + 点赞）重新生成和完善
*   **新列：** 始终由 AI 驱动且完全可定制

**开始使用 AI 列**

1.  点击 "+" 按钮添加新列
2.  从推荐操作中选择：
    *   提取特定信息
    *   总结长文本
    *   翻译内容
    *   或者使用“对 {{column}} 执行某些操作”编写自定义提示词

### 完善和扩展数据集

现在你有了 AI 列，你可以改进它们的结果并扩展你的数据。你可以通过手动编辑和点赞提供反馈，或者通过调整列配置来改进结果。两者都需要重新生成才能生效。

![image/png](/images/posts/ab913fa348c8.png)

1.  如何添加更多单元格

-  下拉：从列的最后一个单元格向下拖动，立即生成额外的行
-  无需重新生成 - 新单元格会即时创建
-  你也可以用这个功能来重新生成出错的单元格

2.  手动编辑与反馈

-  编辑单元格：点击任意单元格直接编辑内容 - 这为模型提供了你期望输出的示例
-  点赞结果：使用点赞标记好的输出示例
-  重新生成以将反馈应用到该列的其他单元格。

在底层，这些手动编辑和点赞的单元格将作为小样本示例，用于在你重新生成或在该列添加更多单元格时生成单元格！

3.  调整列配置
    更改提示词、切换模型或提供商，或修改设置，然后重新生成以获得更好的结果。

重写提示词

-  每一列都有其生成提示词
-  随时编辑以更改或改进输出
-  列会重新生成新的结果

切换模型/提供商

-  尝试不同的模型以获得不同的性能或进行比较。
-  对于特定任务，有些模型比其他模型更准确、更有创意或更有条理。
-  有些提供商推理速度更快，上下文长度也不同；可以为选定的模型测试不同的提供商。

切换搜索

-  启用：模型从网络获取最新信息
-  禁用：离线，仅使用模型生成

### 将最终数据集导出到 Hub

当你对新数据集满意后，将其导出到 Hub！这还有一个额外的好处，就是会生成一个配置文件，你可以重复使用它来（1）使用此脚本通过 HF Jobs 生成更多数据，以及（2）为下游应用复用提示词，包括来自你编辑和点赞单元格的小样本。

![image/png](/images/posts/4ed71d740b3d.png)

这是一个使用 AI Sheets 创建的示例数据集，它生成了这个配置文件。

### 使用 HF Jobs 运行数据生成脚本

如果你想生成更大的数据集，可以使用上述配置和脚本，如下所示：

```bash
hf jobs uv run \
-s HF_TOKEN=$HF_TOKEN \
https://huggingface.co/datasets/aisheets/uv-scripts/raw/main/extend_dataset/script.py \ 
--config https://huggingface.co/datasets/dvilasuero/nemotron-personas-kimi-questions/raw/main/config.yml \ 
--num-rows 100 \ 
nvidia/Nemotron-Personas dvilasuero/nemotron-kimi-qa-distilled 

```

## 示例

本节提供了你可以使用 AI Sheets 构建的数据集示例，以激发你的下一个项目灵感。

### 模型氛围测试与比较

如果你想在不同提示词和你关心的数据上测试最新模型，AI Sheets 是你的完美伴侣。

你只需要导入一个数据集（或从头创建一个），然后添加不同的列来测试你想测试的模型。

然后，你可以手动检查结果，或者添加一列使用 LLM 来评判每个模型的质量。

下面是一个比较开源前沿模型用于迷你 Web 应用的示例。AI Sheets 让你可以看到交互式结果并试用每个应用。此外，该数据集包含多个使用 LLM 来评判和比较应用质量的列。

![image/png](/images/posts/bf366a03ad16.png)

从类似我们刚才描述的会话中导出的示例数据集：:https://huggingface.co/datasets/dvilasuero/jsvibes-qwen-gpt-oss-judged

配置：

```yml
columns:
  gpt-oss:
    modelName: openai/gpt-oss-120b
    modelProvider: groq
    userPrompt: Create a complete, runnable HTML+JS file implementing {{description}}
    searchEnabled: false
    columnsReferences:
      - description
  eval-qwen-coder:
    modelName: Qwen/Qwen3-Coder-480B-A35B-Instruct
    modelProvider: cerebras
    userPrompt: "Please compare the two apps and tell me which one is better and why:\n\nApp description:\n\n{{description}}\n\nmodel 1:\n\n{{qwen3-coder}}\n\nmodel 2:\n\n{{gpt-oss}}\n\nKeep it very short and focus on whether they work well for the purpose, make sure they work and are not incomplete, and the code quality, not on visual appeal and unrequested features. Assume the models might provide non working solutions, so be careful to assess that\n\nRespond with:\n\nchosen: {model 1, model 2}\n\nreason: ..."
    searchEnabled: false
    columnsReferences:
      - gpt-oss
      - description
      - qwen3-coder
  eval-gpt-oss:
    modelName: openai/gpt-oss-120b
    modelProvider: groq
    userPrompt: "Please compare the two apps and tell me which one is better and why:\n\nApp description:\n\n{{description}}\n\nmodel 1:\n\n{{qwen3-coder}}\n\nmodel 2:\n\n{{gpt-oss}}\n\nKeep it very short and focus on whether they work well for the purpose, make sure they work and are not incomplete, and the code quality, not on visual appeal and unrequested features. Assume the models might provide non working solutions, so be careful to assess that\n\nRespond with:\n\nchosen: {model 1, model 2}\n\nreason: ..."
    searchEnabled: false
    columnsReferences:
      - gpt-oss
      - description
      - qwen3-coder
  eval-kimi:
    modelName: moonshotai/Kimi-K2-Instruct
    modelProvider: groq
    userPrompt: "Please compare the two apps and tell me which one is better and why:\n\nApp description:\n\n{{description}}\n\nmodel 1:\n\n{{qwen3-coder}}\n\nmodel 2:\n\n{{gpt-oss}}\n\nKeep it very short and focus on whether they work well for the purpose, make sure they work and are not incomplete, and the code quality, not on visual appeal and unrequested features. Assume the models might provide non working solutions, so be careful to assess that\n\nRespond with:\n\nchosen: {model 1, model 2}\n\nreason: ..."
    searchEnabled: false
    columnsReferences:
      - gpt-oss
      - description
      - qwen3-coder

```

### 为 Hub 数据集添加分类

AI Sheets 也可以增强现有数据集，并帮助你进行涉及分析文本数据集的快速数据分析和数据科学项目。

这是一个为现有 Hub 数据集添加分类的示例。

![image/png](/images/posts/ae364610d42f.png)

一个很酷的功能是，你可以验证或手动编辑初始分类输出，并重新生成整个列以改进结果，如下所示：

![image/png](/images/posts/e5733b5c6a15.png)

```yml
columns:
  category:
    modelName: moonshotai/Kimi-K2-Instruct
    modelProvider: groq
    userPrompt: |-
      Categorize the main topics of the following question:

      {{question}}
    prompt: "

      You are a rigorous, intelligent data-processing engine. Generate only the
      requested response format, with no explanations following the user
      instruction. You might be provided with positive, accurate examples of how
      the user instruction must be completed.

      # Examples

      The following are correct, accurate example outputs with respect to the
      user instruction:

      ## Example

      ### Input

      question: Given the area of a parallelogram is 420 square centimeters and
      its height is 35 cm, find the corresponding base. Show all work and label
      your answer.

      ### Output

      Mathematics – Geometry

      ## Example

      ### Input

      question: What is the minimum number of red squares required to ensure
      that each of $n$ green axis-parallel squares intersects 4 red squares,
      assuming the green squares can be scaled and translated arbitrarily
      without intersecting each other?

      ### Output

      Geometry, Combinatorics
      # User instruction

      Categorize the main topics of the following question:

      {{question}}

      # Your response
      "
    searchEnabled: false
    columnsReferences:
      - question

```

### 使用 LLM 作为评判者来评估模型

另一个用例是使用 LLM 作为评判者的方法来评估模型的输出。这对于比较模型或评估现有数据集的质量很有用，例如，在 Hugging Face Hub 上的现有数据集上微调模型。

在第一个示例中，我们将氛围测试与一个评判者 LLM 列结合了起来。这是评判者提示词：

![image/png](/images/posts/e59364e41914.png)

示例数据集：https://huggingface.co/datasets/dvilasuero/jsvibes-qwen-gpt-oss-judged

```yml
columns:
  object_name:
    modelName: meta-llama/Llama-3.3-70B-Instruct
    modelProvider: groq
    userPrompt: 生成一个常见日常物品的名称
    searchEnabled: false
    columnsReferences: []
  object_description:
    modelName: meta-llama/Llama-3.3-70B-Instruct
    modelProvider: groq
    userPrompt: 用形容词和简短的词组（用逗号分隔）描述一个{{object_name}}。不超过10个单词
    searchEnabled: false
    columnsReferences:
      - object_name
  object_image_with_desc:
    modelName: multimodalart/isometric-skeumorphic-3d-bnb
    modelProvider: fal-ai
    userPrompt: RBNBICN, 图标, 白色背景, 等距透视, {{object_name}} , {{object_description}}
    searchEnabled: false
    columnsReferences:
      - object_description
      - object_name
  object_image_without_desc:
    modelName: multimodalart/isometric-skeumorphic-3d-bnb
    modelProvider: fal-ai
    userPrompt: "RBNBICN, 图标, 白色背景, 等距透视, {{object_name}} "
    searchEnabled: false
    columnsReferences:
      - object_name
  glowing_colors:
    modelName: multimodalart/isometric-skeumorphic-3d-bnb
    modelProvider: fal-ai
    userPrompt: "RBNBICN, 图标, 白色背景, 等距透视, {{object_name}}, 发光颜色 "
    searchEnabled: false
    columnsReferences:
      - object_name
  flux:
    modelName: black-forest-labs/FLUX.1-dev
    modelProvider: fal-ai
    userPrompt: 根据{{object_description}}为物品{{object_name}}创建一个等距图标
    searchEnabled: false
    columnsReferences:
      - object_description
      - object_name

```

## 后续步骤

您可以无需安装任何软件即可尝试 AI Sheets，也可以从 GitHub 仓库下载并在本地部署。为了在本地运行并充分利用其功能，我们建议您订阅 PRO 版，以获得每月 20 倍的推理使用量。

如果您有任何问题或建议，请在社区标签页中告知我们，或在 GitHub 上提交 issue。

---

> 本文由AI自动翻译，原文链接：[Introducing AI Sheets: a tool to work with datasets using open AI models!](https://huggingface.co/blog/aisheets)
> 
> 翻译时间：2026-02-21 04:18
