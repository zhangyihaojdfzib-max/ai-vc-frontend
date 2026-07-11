---
title: Flint：为AI智能体打造的精美图表生成工具
title_original: AI can generate Charts. Flint helps generate better ones.
date: '2026-07-08'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/flint-a-visualization-language-for-the-ai-era/
author: ''
summary: Flint是一种面向AI驱动图表创建的可视化中间语言，帮助智能体从简单、可人工编辑的规格生成富有表现力且视觉精美的图表。它利用语义类型指导设计决策，自动管理尺寸、间距和布局，并支持编译为Vega-Lite、ECharts和Chart.js等多个后端。Flint解决了传统可视化库中简短规格平淡、详细规格脆弱易错的问题，使AI智能体能够可靠创建高质量图表，同时保持人类可读可编辑性。该项目开源，包含flint-chart库和MCP服务器。
categories:
- AI产品
tags:
- Flint
- 图表生成
- AI智能体
- 可视化中间语言
- 开源
draft: false
translated_at: '2026-07-11T05:26:03.572247'
---

## 概览

- 从简单规格生成精美图表。Flint 使 AI 智能体能够根据简单、可人工编辑的规格，可靠地生成富有表现力、视觉精美的图表。
- 语义类型指导设计。Flint 利用语义数据类型来表达数据的含义，帮助编译器选择合适的比例、基线、格式和配色方案。
- 布局自适应数据。Flint 自动管理尺寸、间距、标签和布局，使图表在基数和密度变化时仍保持可读性，无需用户显式配置。
- 一份规格可适配多个后端。单一 Flint 规格可编译为 Vega-Lite、Apache ECharts 或 Chart.js，无需从头重写图表。
- 专为智能体工作流构建。该开源项目包含 flint-chart 库和 flint-chart-mcp 服务器，使智能体能够在聊天或编码环境中直接创建、验证和渲染图表。

![图 1. Flint 通过其简单规格支持多种可视化图表，并可借助 Vega-Lite、ECharts 和 Chart.js 等可视化库进行渲染。](/images/posts/088cb4c056c6.png)

创建一张好图表需要许多设计决策：日期应如何解析、比例是否应从零开始、数值应如何格式化、标签需要多大空间，以及哪些颜色能让数据更易读。现代可视化库（如 Vega-Lite、Apache ECharts 和 Chart.js）提供了这些控制选项，但存在一个权衡：依赖系统默认值的简短规格往往生成平淡无奇的图表，而精美的可视化则需要包含精心选择参数的详细规格，这些规格通常冗长、脆弱且容易出错。

随着大语言模型（LLM）和 AI 智能体承担更多可视化工作，这一权衡变得更加突出。智能体在必须管理复杂、低层次的规格细节时尤其容易出错，由此产生的脆弱代码也难以让人检查、修复或复用。理想情况下，我们需要一种折中方案：一种智能体能够可靠生成、人类可以直接编辑的紧凑规格，并且系统可以将其编译成设计良好的图表。

为应对这一挑战，我们推出了 Flint（在新标签页中打开），这是一种面向 AI 驱动图表创建的可视化中间语言。Flint 帮助 AI 智能体根据简单、可人工编辑的图表规格，创建富有表现力且吸引人的图表。Flint 编译器无需为比例、坐标轴、间距和布局提供冗长的低层次参数，而是从数据、语义类型、图表类型和编码中推导出优化的图表设置。同一份 Flint 规格可通过多个后端渲染，包括 Vega-Lite、Apache ECharts 和 Chart.js。

![图 2. Flint 将一份紧凑、可人工编辑的图表规格编译为完整的后端原生规格及渲染后的可视化图表。在此热力图示例中，Flint 规格指定了语义类型（period 为 YearMonth，newUsers 为 Profit）并将字段映射到视觉通道。编译器推导出 Vega-Lite 的细节，包括时间解析、坐标轴格式化、颜色比例、单元格尺寸、图例配置和布局。](/images/posts/4df438cfce21.png)

## Flint 的工作原理

图 2 展示了 Flint 编译器如何将一份紧凑的图表规格转化为精细的热力图。

传统上，要生成一张高质量的热力图，我们需要通过低层次的图表属性显式告知系统如何处理 period 字段、如何正确标注 MonthYear 值、如何调整热力图单元格大小，以及如何选择能恰当表示正负 newUsers 值的颜色比例。如果没有这些配置，可视化库只能根据字段名称和原始值进行猜测，这可能导致图表在技术上有效但可能具有误导性。虽然这些细节很重要，但硬编码它们既困难又容易出错，而且会使规格变得脆弱，用户难以理解或调整。

在 Flint 中，这些低层次细节被系统化地管理，编译器从高层次的数据和图表规格中推导出它们。其中，数据规格捕获了语义类型和可选元数据，图表规格定义了图表类型并将字段映射到视觉通道（如 x、y、颜色、尺寸或分面）。根据这些信息，编译器推导出解析规则、比例、坐标轴、聚合、格式化、配色方案、布局，并生成后端原生规格，用于渲染最终的精美可视化。这使用户无需显式设置脆弱且容易出错的低层次细节。

此外，由于中间表示与任何单一渲染库分离，Flint 可以针对具有截然不同 API 和编程模型的后端进行编译。用户可以在编译为 Vega-Lite、ECharts 或 Chart.js 时保留相同的紧凑图表意图，并选择能力最适合该可视化的后端。

视频系列

![与 Sinead Bovell 的《再思考》](/images/posts/c0f56ba91e8d.jpg)

## 《再思考》

一个与 Sinead Bovell 合作的视频系列，围绕每个人都在问的关于 AI 的问题展开。来自微软各领域的专家声音，我们将解析这项快速发展的技术所带来的张力与前景，探索正在演变和可能实现的一切。

## Flint 用于 AI 辅助可视化

Flint 非常适合基于 LLM 的图表生成，因为语义类型通常比全套低层次可视化参数更容易让模型推断。字段名称、值模式和常见数据知识可以帮助智能体识别某列是否代表日期、价格、百分比、国家、排名或相关性。一旦这些含义变得明确，编译器就可以处理许多原本会表现为脆弱、库特定代码的设计决策。

在我们的研究实验中，我们将 Flint 与 DirectVL（一种要求模型在 LLM 自我评估流程中直接生成完整（更复杂）Vega-Lite 规格的基线方法）进行了比较。基于 Tidy Tuesdays 测试数据，在三个测试模型上，Flint 获得了更高的整体 LLM 评审分数：GPT-5.1 上为 16.27 对比 15.91，GPT-5-mini 上为 16.16 对比 15.60，GPT-4.1 上为 15.91 对比 15.34。事实上，Flint 非常强大且可靠，现已用于驱动 Data Formulator（在新标签页中打开），这是一个微软研究院的 AI 辅助数据分析和可视化项目。

为了让您的智能体轻松访问 Flint，我们还发布了 flint-chart-mcp，这是一个模型上下文协议（MCP）服务器，允许智能体在聊天或编码环境中创建、验证和渲染图表。MCP 调用可以内联嵌入数据或读取配置好的本地文件，并且服务器可以打开交互式图表视图，以便用户检查和优化结果。

![图 3. 一旦您将 flint-chart-mcp 与您喜爱的 AI 客户端集成，智能体即可生成由 Flint 驱动的交互式可视化，以回答您的数据探索问题。](/images/posts/80be48a8f029.png)

## 尝试 Flint

Flint 是开源的，随时可用：

- 项目网站：https://microsoft.github.io/flint-chart/（在新标签页中打开）
- GitHub：https://github.com/microsoft/flint-chart（在新标签页中打开）
- Flint MCP 服务器说明：https://microsoft.github.io/flint-chart/#/mcp（在新标签页中打开）

Flint 指向了一个共享的可视化语义层，人类和 AI 智能体可以在其中使用紧凑的图表意图，而编译器则处理精细的低层次细节。我们邀请社区探索该项目并在此基础上进行构建。

### 王成龙

高级研究员

### Alper Sarikaya

高级数据可视化工程师

Power BI

### Scott Tsukamaki

高级技术项目经理

### Michel Galley

首席研究经理

### 高剑峰

技术院士 & 公司副总裁

---

> 本文由AI自动翻译，原文链接：[AI can generate Charts. Flint helps generate better ones.](https://www.microsoft.com/en-us/research/blog/flint-a-visualization-language-for-the-ai-era/)
> 
> 翻译时间：2026-07-11 05:26
